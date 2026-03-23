# 🚀 วิธี Deploy RIFFAI Platform

มี 3 วิธีให้เลือก:

## 1. 🎯 แบบง่ายสุด - Cloud Run (แนะนำ)

ใช้เวลา 10-15 นาที, ฟรี (ถ้าใช้น้อย)

```bash
# 1. Login GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 3. Deploy Backend
cd riffai-platform/backend
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --allow-unauthenticated

# 4. เก็บ Backend URL
export BACKEND_URL=$(gcloud run services describe riffai-backend --region=asia-southeast1 --format="value(status.url)")

# 5. Deploy Frontend
cd ../frontend
gcloud run deploy riffai-frontend \
  --source . \
  --region=asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL"

# ✅ เสร็จแล้ว!
```

**ข้อดี:**
- ✅ ฟรี (2M requests/เดือน)
- ✅ Auto-scale
- ✅ ไม่ต้องจัดการ server
- ✅ Deploy ง่าย

**ข้อเสีย:**
- ⚠️ ข้อมูลหายเมื่อ restart (ใช้ SQLite ในหน่วยความจำ)
- ⚠️ Cold start ~2-3 วินาที

---

## 2. 💪 แบบมี Database - Cloud Run + Cloud SQL

ใช้เวลา 30-45 นาที, ~$15-20/เดือน

```bash
# 1. สร้าง Cloud SQL
gcloud sql instances create riffai-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-southeast1 \
  --root-password="YOUR_PASSWORD"

# 2. สร้าง database
gcloud sql databases create riffai --instance=riffai-db

# 3. Deploy Backend พร้อม Cloud SQL
cd riffai-platform/backend
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --allow-unauthenticated \
  --add-cloudsql-instances=YOUR_PROJECT:asia-southeast1:riffai-db \
  --set-env-vars="DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@/riffai?host=/cloudsql/YOUR_PROJECT:asia-southeast1:riffai-db"

# 4. Deploy Frontend (เหมือนวิธีที่ 1)
```

**ข้อดี:**
- ✅ ข้อมูลถาวร
- ✅ PostgreSQL + PostGIS
- ✅ Backup อัตโนมัติ

**ข้อเสีย:**
- 💰 มีค่าใช้จ่าย ~$15-20/เดือน

---

## 3. 🏢 แบบเต็มรูปแบบ - Production Ready

ใช้เวลา 2-3 ชั่วโมง, ~$30-50/เดือน

ดูคู่มือละเอียดที่: [DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md)

รวม:
- Cloud SQL (PostgreSQL + PostGIS)
- Cloud Storage (ภาพดาวเทียม)
- Cloud Scheduler (ดึงข้อมูลอัตโนมัติ)
- Monitoring & Logging
- Custom Domain
- SSL Certificate

---

## 📊 เปรียบเทียบ

| คุณสมบัติ | วิธีที่ 1 | วิธีที่ 2 | วิธีที่ 3 |
|----------|----------|----------|----------|
| เวลา Deploy | 10-15 นาที | 30-45 นาที | 2-3 ชั่วโมง |
| ค่าใช้จ่าย | ฟรี | ~$15-20 | ~$30-50 |
| ข้อมูลถาวร | ❌ | ✅ | ✅ |
| Auto-scale | ✅ | ✅ | ✅ |
| Monitoring | พื้นฐาน | พื้นฐาน | ครบถ้วน |
| Custom Domain | ❌ | ❌ | ✅ |

---

## 🎯 แนะนำ

- **ทดสอบ/Demo**: ใช้วิธีที่ 1
- **ใช้งานจริง (ข้อมูลน้อย)**: ใช้วิธีที่ 2
- **Production (ข้อมูลเยอะ)**: ใช้วิธีที่ 3

---

## 📚 เอกสารเพิ่มเติม

- [DEPLOY-QUICK.md](./DEPLOY-QUICK.md) - คำสั่งแบบละเอียด
- [DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md) - Production deployment
- [Cloud Run Docs](https://cloud.google.com/run/docs)

---

## 🆘 ช่วยเหลือ

### ❌ Build ล้มเหลว
```bash
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

### ❌ Service ไม่ทำงาน
```bash
gcloud run logs read riffai-backend --limit=50
```

### ❌ ลบทิ้งเริ่มใหม่
```bash
gcloud run services delete riffai-backend --region=asia-southeast1
gcloud run services delete riffai-frontend --region=asia-southeast1
```
