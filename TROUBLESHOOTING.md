# 🔧 RIFFAI Platform - Troubleshooting Guide

## 🚨 ปัญหาที่พบบ่อย

### 1. โหลดข้อมูลแผนที่ล้มเหลว (Failed to load map data)

#### สาเหตุ:
- Backend ไม่ได้รัน
- Port ไม่ตรงกัน (Frontend เรียก 8080 แต่ Backend รันที่ 8000)
- Database connection ปิดไปแล้ว
- CORS issues

#### วิธีแก้:

**ขั้นตอนที่ 1: เช็คว่า Backend รันหรือไม่**
```bash
# เปิด browser ไปที่
http://localhost:8000/health

# หรือใช้ curl
curl http://localhost:8000/health
```

ถ้าไม่ได้ response แสดงว่า backend ไม่ทำงาน

**ขั้นตอนที่ 2: รัน Backend**
```bash
cd backend
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**ขั้นตอนที่ 3: ทดสอบ API Endpoints**
```bash
# ใช้ script ที่เตรียมไว้
.\test-backend.bat

# หรือทดสอบแต่ละ endpoint
curl http://localhost:8000/api/map/rivers
curl http://localhost:8000/api/map/dams
curl http://localhost:8000/api/map/basins
```

**ขั้นตอนที่ 4: เช็ค Frontend Config**
```bash
# ดูไฟล์ frontend/.env.local
# ต้องเป็น:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**ขั้นตอนที่ 5: Restart Frontend**
```bash
cd frontend
npm run dev
```

---

### 2. Port Already in Use

#### Error Message:
```
Error: listen EADDRINUSE: address already in use :::8000
```

#### วิธีแก้:

**วิธีที่ 1: ใช้ Script (แนะนำ)**
```bash
.\kill-ports.bat
```

**วิธีที่ 2: Manual**
```bash
# หา process ที่ใช้ port 8000
netstat -ano | findstr :8000

# ปิด process (เปลี่ยน PID)
taskkill /F /PID <PID>
```

---

### 3. ERR_CONNECTION_REFUSED

#### สาเหตุ:
- Backend ไม่ได้รัน
- Port ผิด
- Firewall block

#### วิธีแก้:

1. **เช็คว่า Backend รัน:**
```bash
# ดู process
tasklist | findstr python

# ดู port
netstat -ano | findstr :8000
```

2. **รัน Backend ใหม่:**
```bash
cd backend
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. **เช็ค Firewall:**
- เปิด Windows Defender Firewall
- Allow Python through firewall

---

### 4. Database Connection Closed

#### Error Message:
```
sqlalchemy.exc.InvalidRequestError: This Connection is closed
```

#### สาเหตุ:
- Connection pool หมด
- Session ไม่ได้ปิดอย่างถูกต้อง

#### วิธีแก้:

**แก้ไขแล้ว!** ไฟล์ `backend/app/models/database.py` ได้รับการปรับปรุง:
- เพิ่ม pool_size=10
- เพิ่ม max_overflow=20
- เพิ่ม pool_pre_ping=True
- เพิ่ม proper session management

ถ้ายังมีปัญหา ให้ restart backend:
```bash
# กด Ctrl+C ใน terminal ที่รัน backend
# แล้วรันใหม่
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 5. CORS Error

#### Error Message:
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

#### วิธีแก้:

**แก้ไขแล้ว!** ไฟล์ `backend/app/main.py` มี CORS middleware:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

ถ้ายังมีปัญหา ให้ restart backend

---

### 6. Module Not Found

#### Error Message:
```
ModuleNotFoundError: No module named 'fastapi'
```

#### วิธีแก้:

```bash
cd backend
py -3 -m pip install -r requirements.txt
```

---

### 7. npm ERR! Missing script: "dev"

#### วิธีแก้:

```bash
cd frontend
npm install
npm run dev
```

---

### 8. Database Not Found

#### Error Message:
```
sqlite3.OperationalError: unable to open database file
```

#### วิธีแก้:

```bash
cd backend

# สร้าง database
py -3 -m alembic upgrade head

# Seed ข้อมูล
py -3 app/seed.py
```

---

## 🔍 การ Debug

### ดู Backend Logs:
```bash
# รัน backend แล้วดู output ใน terminal
# จะเห็น:
# - Request logs
# - Error messages
# - SQL queries (ถ้า DEBUG=True)
```

### ดู Frontend Logs:
```bash
# เปิด Browser DevTools (F12)
# ไปที่ Console tab
# จะเห็น:
# - API calls
# - Errors
# - Network requests
```

### ดู Network Requests:
```bash
# เปิด Browser DevTools (F12)
# ไปที่ Network tab
# Refresh page
# ดู requests ที่ล้มเหลว (สีแดง)
```

---

## 📋 Checklist ก่อนรัน

- [ ] Python 3.11+ ติดตั้งแล้ว (`py -3 --version`)
- [ ] Node.js 20+ ติดตั้งแล้ว (`node --version`)
- [ ] Backend dependencies ติดตั้งแล้ว (`pip list | findstr fastapi`)
- [ ] Frontend dependencies ติดตั้งแล้ว (`dir frontend\node_modules`)
- [ ] Database มีอยู่ (`dir backend\riffai.db`)
- [ ] Port 8000 ว่าง (`netstat -ano | findstr :8000`)
- [ ] Port 3000 ว่าง (`netstat -ano | findstr :3000`)
- [ ] `.env.local` ตั้งค่าถูกต้อง

---

## 🚀 Quick Fix Commands

```bash
# 1. Kill all ports
.\kill-ports.bat

# 2. Start backend
cd backend
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Start frontend (terminal ใหม่)
cd frontend
npm run dev

# 4. Test backend
.\test-backend.bat

# 5. Open browser
# http://localhost:3000
```

---

## 🆘 ยังแก้ไม่ได้?

### ลองขั้นตอนนี้:

1. **Clean Restart:**
```bash
# Kill all
.\kill-ports.bat

# Delete cache
rmdir /s /q backend\__pycache__
rmdir /s /q frontend\.next

# Restart
.\start-local.bat
```

2. **Reinstall Dependencies:**
```bash
# Backend
cd backend
py -3 -m pip install --upgrade -r requirements.txt

# Frontend
cd frontend
rmdir /s /q node_modules
npm install
```

3. **Reset Database:**
```bash
cd backend
del riffai.db
py -3 -m alembic upgrade head
py -3 app/seed.py
```

4. **Check Logs:**
- ดู terminal output
- ดู browser console (F12)
- ดู network tab (F12)

---

## 📞 Common Error Messages

### "Failed to load resources: net::ERR_CONNECTION_REFUSED"
→ Backend ไม่ทำงาน รัน backend ก่อน

### "TypeError: Failed to fetch"
→ API URL ผิด เช็ค `.env.local`

### "404 Not Found"
→ Endpoint ไม่มี เช็ค API path

### "500 Internal Server Error"
→ Backend error ดู backend logs

### "CORS policy"
→ CORS ไม่ถูกต้อง restart backend

---

## ✅ ทดสอบว่าทำงานหรือไม่

### Backend:
```bash
curl http://localhost:8000/health
# ควรได้: {"status":"healthy","version":"1.0.0"}
```

### Frontend:
```bash
# เปิด browser: http://localhost:3000
# ควรเห็นหน้า Dashboard
```

### API Endpoints:
```bash
curl http://localhost:8000/api/map/rivers
curl http://localhost:8000/api/map/dams
curl http://localhost:8000/api/map/basins
# ควรได้ GeoJSON data
```

---

## 🎯 Best Practices

1. **รัน Backend ก่อนเสมอ** แล้วค่อยรัน Frontend
2. **เช็ค port ก่อนรัน** ใช้ `kill-ports.bat` ถ้าจำเป็น
3. **ดู logs** เพื่อ debug ปัญหา
4. **ใช้ API Docs** ที่ http://localhost:8000/docs เพื่อทดสอบ
5. **Restart เมื่อแก้ code** (หรือใช้ --reload)

---

## 📚 เอกสารเพิ่มเติม

- `START-LOCAL.md` - วิธีรันโลคอล
- `DEPLOY-QUICK.md` - วิธี deploy
- `README.md` - ภาพรวมโปรเจค
- API Docs: http://localhost:8000/docs

---

🎉 **หวังว่าจะช่วยแก้ปัญหาได้!**
