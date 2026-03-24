# 🚀 วิธีรัน RIFFAI Platform แบบ Local

## ⚡ Quick Start (แบบง่าย)

### วิธีที่ 1: ใช้ Batch File (แนะนำ)
```bash
# เปิด Command Prompt หรือ PowerShell
cd C:\Users\User\Desktop\riffai-platform\riffai-platform

# รัน script (ใน PowerShell ใช้ .\ ข้างหน้า)
.\start-local.bat
```

Script นี้จะเปิด 2 terminal windows:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 📝 วิธีที่ 2: รันแยกทีละตัว

### 1. รัน Backend (Terminal 1)
```bash
cd C:\Users\User\Desktop\riffai-platform\riffai-platform\backend
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

เมื่อเห็นข้อความนี้แสดงว่าพร้อมแล้ว:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. รัน Frontend (Terminal 2 - เปิดใหม่)
```bash
cd C:\Users\User\Desktop\riffai-platform\riffai-platform\frontend
npm run dev
```

เมื่อเห็นข้อความนี้แสดงว่าพร้อมแล้ว:
```
  ▲ Next.js 14.2.0
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

---

## 🌐 เข้าใช้งาน

เปิด browser แล้วไปที่:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

---

## 🔍 ตรวจสอบว่าทำงานหรือไม่

### ทดสอบ Backend:
```bash
curl http://localhost:8000/health
```

ควรได้:
```json
{"status":"healthy","version":"1.0.0"}
```

### ทดสอบ Frontend:
เปิด browser ไปที่ http://localhost:3000 ควรเห็นหน้า Dashboard

---

## 🛑 หยุดการทำงาน

กด `Ctrl + C` ใน terminal ที่รัน backend และ frontend

---

## ⚠️ แก้ปัญหา

### ปัญหา: Port ถูกใช้งานอยู่แล้ว

**Backend (Port 8000):**
```bash
# หา process ที่ใช้ port 8000
netstat -ano | findstr :8000

# ปิด process (เปลี่ยน PID เป็นเลขที่ได้)
taskkill /PID <PID> /F
```

**Frontend (Port 3000):**
```bash
# หา process ที่ใช้ port 3000
netstat -ano | findstr :3000

# ปิด process
taskkill /PID <PID> /F
```

### ปัญหา: Python ไม่เจอ

ตรวจสอบว่าติดตั้ง Python แล้ว:
```bash
py -3 --version
```

ถ้าไม่เจอ ให้ติดตั้ง Python 3.11+ จาก https://www.python.org/downloads/

### ปัญหา: Node.js ไม่เจอ

ตรวจสอบว่าติดตั้ง Node.js แล้ว:
```bash
node --version
npm --version
```

ถ้าไม่เจอ ให้ติดตั้ง Node.js 20+ จาก https://nodejs.org/

### ปัญหา: Dependencies ไม่ครบ

**Backend:**
```bash
cd backend
py -3 -m pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### ปัญหา: Database ไม่มี

```bash
cd backend
py -3 -m alembic upgrade head
py -3 app/seed.py
```

---

## 🐳 วิธีที่ 3: ใช้ Docker (ถ้าต้องการ)

```bash
# รัน Docker Compose
.\docker-start.bat

# หรือ
docker-compose up
```

---

## 📊 Features ที่ใช้งานได้

เมื่อรันแล้ว คุณสามารถใช้งาน:

1. **Dashboard** - ภาพรวมข้อมูลน้ำท่วม
2. **Map** - แผนที่แสดงสถานี แม่น้ำ เขื่อน และ Heatmap
3. **Predict** - ทำนายน้ำท่วมด้วย AI
4. **Analytics** - วิเคราะห์ข้อมูลเชิงลึก
5. **Alerts** - ระบบแจ้งเตือน
6. **Time-lapse** - ดูข้อมูลย้อนหลัง

---

## 🎯 Next Steps

หลังจากรันโลคอลสำเร็จแล้ว คุณสามารถ:

1. ทดสอบ features ต่างๆ
2. แก้ไข code และดูผลแบบ real-time (hot reload)
3. Deploy ขึ้น Google Cloud Run เมื่อพร้อม

---

## 🚀 Deploy to Google Cloud

เมื่อทดสอบโลคอลเรียบร้อยแล้ว ให้ deploy:

```bash
# Deploy ทั้งหมด
.\deploy-all.bat

# หรือ deploy แยก
cd backend
.\deploy-backend.bat

cd frontend
.\deploy-frontend.bat
```

---

## 💡 Tips

- ใช้ `--reload` กับ uvicorn เพื่อ auto-reload เมื่อแก้ code
- ใช้ `npm run dev` เพื่อ hot reload ใน Next.js
- เปิด API Docs ที่ http://localhost:8000/docs เพื่อทดสอบ API
- ดู logs ใน terminal เพื่อ debug

---

## 📞 ต้องการความช่วยเหลือ?

ถ้ามีปัญหา:
1. ดู error message ใน terminal
2. ตรวจสอบว่า dependencies ติดตั้งครบ
3. ตรวจสอบว่า port ไม่ถูกใช้งาน
4. ลองรีสตาร์ท terminal

---

## ✅ Checklist

ก่อนรัน ตรวจสอบว่า:

- [ ] Python 3.11+ ติดตั้งแล้ว
- [ ] Node.js 20+ ติดตั้งแล้ว
- [ ] Backend dependencies ติดตั้งแล้ว (`pip install -r requirements.txt`)
- [ ] Frontend dependencies ติดตั้งแล้ว (`npm install`)
- [ ] Database มีอยู่แล้ว (`riffai.db`)
- [ ] Port 8000 และ 3000 ว่าง

---

🎉 **พร้อมแล้ว! ลองรันดูได้เลย**
