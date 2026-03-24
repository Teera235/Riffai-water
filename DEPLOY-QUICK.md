# 🚀 Quick Deploy Guide - RIFFAI Platform

## 📋 สถานะปัจจุบัน

### ✅ สิ่งที่พร้อมแล้ว:
- Backend code พร้อม deploy
- Frontend code พร้อม deploy
- Docker images พร้อม
- Deployment scripts พร้อม
- Database schema พร้อม
- AI models พร้อม (3 models)
- Satellite integration พร้อม (Earth Engine authenticated)

### 🌐 URLs ที่ Deploy แล้ว:
- **Backend**: https://riffai-backend-715107904640.asia-southeast1.run.app
- **Frontend**: https://riffai-frontend-715107904640.asia-southeast1.run.app
- **API Docs**: https://riffai-backend-715107904640.asia-southeast1.run.app/docs

---

## 🎯 วิธี Deploy (3 ขั้นตอน)

### ขั้นตอนที่ 1: เปิด PowerShell
```powershell
cd C:\Users\User\Desktop\riffai-platform\riffai-platform
```

### ขั้นตอนที่ 2: รัน Deploy Script
```powershell
# ใน PowerShell ต้องใช้ .\ ข้างหน้า
.\deploy-all.bat
```

### ขั้นตอนที่ 3: รอให้เสร็จ
- Backend จะ build และ deploy ก่อน (~5-10 นาที)
- Frontend จะ build และ deploy ตามมา (~3-5 นาที)
- รวมประมาณ 10-15 นาที

---

## 📝 หรือ Deploy แยกทีละตัว

### Deploy Backend อย่างเดียว:
```powershell
cd backend
.\deploy-backend.bat
```

### Deploy Frontend อย่างเดียว:
```powershell
cd frontend
.\deploy-frontend.bat
```

---

## 🔍 ตรวจสอบสถานะ

### ดู Backend URL:
```bash
gcloud run services describe riffai-backend --region asia-southeast1 --format "value(status.url)"
```

### ดู Frontend URL:
```bash
gcloud run services describe riffai-frontend --region asia-southeast1 --format "value(status.url)"
```

### ทดสอบ Backend:
```bash
curl https://riffai-backend-715107904640.asia-southeast1.run.app/health
```

---

## ⚠️ ข้อควรระวัง

### 1. PowerShell Execution Policy
ถ้าไม่สามารถรัน .bat ได้ ให้ใช้:
```powershell
# วิธีที่ 1: เรียกผ่าน cmd
cmd /c deploy-all.bat

# วิธีที่ 2: เปลี่ยน execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. GCloud Authentication
ตรวจสอบว่า login แล้ว:
```bash
gcloud auth list
gcloud config get-value project
```

ถ้ายังไม่ได้ login:
```bash
gcloud auth login
gcloud config set project trim-descent-452802-t2
```

### 3. Docker Authentication
ถ้า push image ไม่ได้:
```bash
gcloud auth configure-docker
```

---

## 🐛 แก้ปัญหา

### ปัญหา: "deploy-all.bat is not recognized"
**สาเหตุ**: ใน PowerShell ต้องใช้ `.\` ข้างหน้า

**แก้ไข**:
```powershell
.\deploy-all.bat
```

### ปัญหา: "Permission denied"
**แก้ไข**:
```powershell
cmd /c deploy-all.bat
```

### ปัญหา: "Docker build failed"
**แก้ไข**:
```bash
# ตรวจสอบ Docker Desktop ทำงานหรือไม่
docker ps

# ถ้าไม่ทำงาน ให้เปิด Docker Desktop
```

### ปัญหา: "gcloud command not found"
**แก้ไข**:
```bash
# ติดตั้ง Google Cloud SDK
# Download จาก: https://cloud.google.com/sdk/docs/install
```

---

## 📊 ขั้นตอนการ Deploy (รายละเอียด)

### Backend Deployment:
1. ✅ Build Docker image (~3-5 นาที)
2. ✅ Push to Google Container Registry (~2-3 นาที)
3. ✅ Deploy to Cloud Run (~2-3 นาที)
4. ✅ Configure environment variables
5. ✅ Set memory (2Gi) and CPU (2)

### Frontend Deployment:
1. ✅ Build Next.js app (~1-2 นาที)
2. ✅ Build Docker image (~1-2 นาที)
3. ✅ Push to GCR (~1-2 นาที)
4. ✅ Deploy to Cloud Run (~1-2 นาที)
5. ✅ Connect to backend API

---

## 💰 ค่าใช้จ่าย (ประมาณการ)

### Cloud Run Pricing:
- **Free tier**: 2 million requests/month
- **ค่าใช้จ่ายต่อเดือน**: $5-50 (ขึ้นกับ traffic)

### ประหยัดค่าใช้จ่าย:
- ✅ Auto-scale to zero (ไม่มี traffic = ไม่เสียเงิน)
- ✅ Pay per use (จ่ายเฉพาะเมื่อมีคนใช้)
- ✅ Free tier 2M requests/month

---

## 🎉 หลัง Deploy สำเร็จ

### ทดสอบ Features:
1. เปิด Frontend URL
2. ทดสอบ Login (admin/admin123)
3. ดู Dashboard
4. ทดสอบ Map (rivers, dams, heatmap)
5. ทดสอบ Predict
6. ดู Analytics
7. ทดสอบ Alerts

### Monitor:
```bash
# ดู logs
gcloud run services logs read riffai-backend --region asia-southeast1 --limit 50

# ดู metrics
gcloud run services describe riffai-backend --region asia-southeast1
```

---

## 🔄 Update Deployment

เมื่อแก้ code แล้วต้องการ deploy ใหม่:

```powershell
# Deploy ทั้งหมด
.\deploy-all.bat

# หรือ deploy เฉพาะที่แก้
cd backend
.\deploy-backend.bat
```

---

## 📞 Commands ที่ใช้บ่อย

```bash
# ดู services ทั้งหมด
gcloud run services list --region asia-southeast1

# ดู logs แบบ real-time
gcloud run services logs tail riffai-backend --region asia-southeast1

# Update memory/CPU
gcloud run services update riffai-backend --memory 4Gi --region asia-southeast1

# Rollback
gcloud run revisions list --service riffai-backend --region asia-southeast1
gcloud run services update-traffic riffai-backend --to-revisions <REVISION>=100 --region asia-southeast1

# Delete service
gcloud run services delete riffai-backend --region asia-southeast1
```

---

## ✅ Deployment Checklist

ก่อน deploy ตรวจสอบ:

- [ ] Docker Desktop ทำงาน
- [ ] gcloud CLI ติดตั้งแล้ว
- [ ] gcloud auth login แล้ว
- [ ] Project ID ถูกต้อง (trim-descent-452802-t2)
- [ ] Docker authentication ตั้งค่าแล้ว
- [ ] Code commit แล้ว (ถ้าใช้ git)

หลัง deploy ตรวจสอบ:

- [ ] Backend URL ทำงาน
- [ ] Frontend URL ทำงาน
- [ ] API Docs เปิดได้
- [ ] Login ได้
- [ ] Features ทำงานปกติ

---

## 🚀 Ready to Deploy!

เมื่อพร้อมแล้ว ให้รัน:

```powershell
cd C:\Users\User\Desktop\riffai-platform\riffai-platform
.\deploy-all.bat
```

แล้วรอ 10-15 นาที จะได้ platform ที่พร้อมใช้งาน! 🎉

---

## 📚 เอกสารเพิ่มเติม

- `DEPLOYMENT-GUIDE.md` - คู่มือ deploy แบบละเอียด
- `START-LOCAL.md` - วิธีรันโลคอล
- `README.md` - ภาพรวมโปรเจค
- `docker-compose.yml` - สำหรับรัน Docker local
