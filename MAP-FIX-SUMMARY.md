# 🗺️ Map Display Fix Summary

## ✅ สิ่งที่แก้ไขแล้ว

### 1. API Service (frontend/src/services/api.ts)
**ปัญหา:** ไม่มี tiles endpoints

**แก้ไข:** เพิ่ม endpoints:
```typescript
tiles: (riskLevel?: string) => api.get("/api/map/tiles", { params: { risk_level: riskLevel } }),
tilesSummary: () => api.get("/api/map/tiles/summary"),
tile: (tileId: string) => api.get(`/api/map/tiles/${tileId}`),
tileHistory: (tileId: string, days = 7) => api.get(`/api/map/tiles/${tileId}/history`, { params: { days } }),
```

### 2. Map Page (frontend/src/app/map/page.tsx)
**ปัญหา:** Hardcoded URL `http://localhost:8000` แทนที่จะใช้ `mapAPI`

**แก้ไข:**
```typescript
// Before
fetch("http://localhost:8000/api/map/tiles/summary").then(res => res.json())

// After
mapAPI.tilesSummary()
```

**เพิ่ม:** Console logging เพื่อ debug
```typescript
console.log("Map data loaded:", { basins: b.data, rivers: r.data, dams: d.data });
```

### 3. Tools สำหรับ Debug
สร้าง scripts ใหม่:
- `test-map-data.bat` - ทดสอบ API endpoints
- `fix-map-display.bat` - ตรวจสอบและแก้ปัญหา

---

## 🔍 วิธีตรวจสอบปัญหา

### ขั้นตอนที่ 1: เช็ค Backend
```bash
# ทดสอบ health
curl http://localhost:8000/health

# ทดสอบ map endpoints
.\test-map-data.bat
```

### ขั้นตอนที่ 2: เช็ค Frontend
```bash
# เปิด browser
http://localhost:3000/map

# กด F12 → Console tab
# ดู error messages

# กด F12 → Network tab
# ดู failed requests (สีแดง)
```

### ขั้นตอนที่ 3: ดู Console Logs
ใน browser console ควรเห็น:
```
Map data loaded: {
  basins: { type: "FeatureCollection", features: [...] },
  rivers: { type: "FeatureCollection", features: [...] },
  dams: { type: "FeatureCollection", features: [...] }
}
```

---

## 🐛 สาเหตุที่เป็นไปได้

### 1. Backend ไม่ทำงาน
**อาการ:** ไม่เห็นอะไรเลยบนแผนที่

**แก้ไข:**
```bash
cd backend
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Database ไม่มีข้อมูล
**อาการ:** แผนที่โหลดได้แต่ไม่มี markers

**แก้ไข:**
```bash
cd backend
py -3 app/seed.py
```

### 3. CORS Issues
**อาการ:** Console แสดง CORS errors

**แก้ไข:** ตรวจสอบ `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Port ไม่ตรงกัน
**อาการ:** ERR_CONNECTION_REFUSED

**แก้ไข:** ตรวจสอบ `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Frontend Cache
**อาการ:** แก้แล้วแต่ยังไม่เห็นผล

**แก้ไข:**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Restart frontend (Ctrl+C แล้ว `npm run dev` ใหม่)

---

## 🚀 วิธีแก้ปัญหาแบบเร็ว

### Quick Fix:
```bash
# 1. Kill all ports
.\kill-ports.bat

# 2. Start backend
cd backend
py -3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Start frontend (terminal ใหม่)
cd frontend
npm run dev

# 4. Test endpoints
.\test-map-data.bat

# 5. Open browser
http://localhost:3000/map
```

### ถ้ายังไม่ได้:
```bash
# Run diagnostic
.\fix-map-display.bat

# ดู output และทำตามคำแนะนำ
```

---

## 📊 ข้อมูลที่ควรเห็นบนแผนที่

### Rivers (แม่น้ำ):
- เจ้าพระยา (Chao Phraya)
- โขง (Mekong)
- ชี (Chi)
- มูล (Mun)
- ปิง (Ping)
- น่าน (Nan)
- ยม (Yom)

### Dams (เขื่อน):
- ภูมิพล (Bhumibol)
- สิริกิติ์ (Sirikit)
- แควน้อยบำรุงแดน (Khao Laem)
- ศรีนครินทร์ (Srinakarin)
- รัชชประภา (Ratchaprapha)
- อุบลรัตน์ (Ubolratana)
- ป่าสักชลสิทธิ์ (Pa Sak)
- ห้วยกุ่ม (Huai Kum)

### Basins (ลุ่มน้ำ):
- Mekong North
- Eastern Coast
- Southern East

### Tiles (Grid Heatmap):
- ควรเห็น grid tiles ครอบคลุมประเทศไทย
- สีต่างๆ แสดงระดับความเสี่ยง

---

## ✅ Checklist

ก่อนเปิด map page ตรวจสอบ:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database has data (`backend/riffai.db` exists)
- [ ] `.env.local` has correct API URL
- [ ] No CORS errors in console
- [ ] API endpoints return data (test with curl)

---

## 🎯 Expected Behavior

### เมื่อเปิด Map Page:
1. แผนที่โหลดขึ้นมา (OpenStreetMap)
2. เห็น rivers (เส้นสีน้ำเงิน)
3. เห็น dams (ไอคอน 🏗️)
4. เห็น grid tiles (สี่เหลี่ยมสีต่างๆ)
5. เห็น water level markers (จุดสีต่างๆ)
6. Sidebar แสดง summary statistics

### เมื่อคลิก:
- Rivers → แสดง popup ข้อมูลแม่น้ำ
- Dams → แสดง popup ข้อมูลเขื่อน
- Tiles → แสดง detail panel
- Markers → แสดง station info

---

## 📞 Debug Commands

```bash
# Test backend health
curl http://localhost:8000/health

# Test rivers
curl http://localhost:8000/api/map/rivers

# Test dams
curl http://localhost:8000/api/map/dams

# Test basins
curl http://localhost:8000/api/map/basins

# Test tiles
curl http://localhost:8000/api/map/tiles/summary

# View backend logs
# (ดูใน terminal ที่รัน backend)

# View frontend logs
# (กด F12 → Console tab)
```

---

## 💡 Tips

1. **ใช้ Browser DevTools** (F12) เพื่อ debug
2. **ดู Network tab** เพื่อเช็ค API calls
3. **ดู Console tab** เพื่อเช็ค errors
4. **Hard refresh** (Ctrl+F5) หลังแก้ code
5. **Clear cache** ถ้าแก้แล้วไม่เห็นผล

---

## 🎉 สรุป

การแก้ไขครั้งนี้:
- ✅ แก้ hardcoded URL
- ✅ เพิ่ม tiles endpoints
- ✅ เพิ่ม error logging
- ✅ สร้าง debug tools

ตอนนี้ map ควรแสดงข้อมูลได้ถูกต้อง!

**Next Steps:**
1. รัน `.\fix-map-display.bat` เพื่อตรวจสอบ
2. เปิด http://localhost:3000/map
3. ดูว่าข้อมูลแสดงหรือไม่
4. ถ้ายังไม่ได้ ดู console errors

---

**หมายเหตุ:** ถ้ายังมีปัญหา ให้ส่ง screenshot ของ:
1. Browser console (F12 → Console)
2. Network tab (F12 → Network)
3. Backend terminal output
