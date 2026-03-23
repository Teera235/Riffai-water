# 🚀 Deploy ขึ้น GCP Cloud Run (ฉบับเร็ว)

## ขั้นตอนที่ 1: ติดตั้ง gcloud CLI

ถ้ายังไม่มี ให้ติดตั้งก่อน:
- Windows: https://cloud.google.com/sdk/docs/install
- หรือใช้ Cloud Shell ใน GCP Console (ไม่ต้องติดตั้ง)

## ขั้นตอนที่ 2: Login และสร้าง Project

```bash
# Login
gcloud auth login

# สร้าง project ใหม่ (หรือใช้ project เดิม)
gcloud projects create riffai-platform --name="RIFFAI Platform"

# ตั้งเป็น project ปัจจุบัน
gcloud config set project riffai-platform

# Enable APIs ที่จำเป็น
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

## ขั้นตอนที่ 3: Deploy Backend

```bash
cd riffai-platform/backend

# Build และ Deploy
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=1Gi

# เก็บ URL ไว้
export BACKEND_URL=$(gcloud run services describe riffai-backend --region=asia-southeast1 --format="value(status.url)")
echo $BACKEND_URL
```

## ขั้นตอนที่ 4: Deploy Frontend

```bash
cd ../frontend

# แก้ไข .env.local ให้ชี้ไป Backend URL
echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" > .env.production

# Build และ Deploy
gcloud run deploy riffai-frontend \
  --source . \
  --region=asia-southeast1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL"

# เก็บ URL
export FRONTEND_URL=$(gcloud run services describe riffai-frontend --region=asia-southeast1 --format="value(status.url)")
echo $FRONTEND_URL
```

## ✅ เสร็จแล้ว!

เปิดเว็บได้ที่:
- **Frontend**: `$FRONTEND_URL`
- **Backend API**: `$BACKEND_URL/docs`

---

## 💰 ค่าใช้จ่าย

Cloud Run มี Free Tier:
- 2 ล้าน requests/เดือน (ฟรี)
- 360,000 GB-seconds/เดือน (ฟรี)

ถ้าใช้น้อยๆ = **ฟรี 100%**

---

## ⚠️ หมายเหตุ

ตอนนี้ Backend ใช้ SQLite ในหน่วยความจำ (ข้อมูลหายเมื่อ restart)

ถ้าต้องการเก็บข้อมูลถาวร ต้องเชื่อม Cloud SQL:

```bash
# สร้าง Cloud SQL
gcloud sql instances create riffai-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-southeast1

# สร้าง database
gcloud sql databases create riffai --instance=riffai-db

# Deploy backend พร้อม Cloud SQL
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --add-cloudsql-instances=riffai-platform:asia-southeast1:riffai-db \
  --set-env-vars="DATABASE_URL=postgresql+asyncpg://postgres:PASSWORD@/riffai?host=/cloudsql/riffai-platform:asia-southeast1:riffai-db"
```

---

## 🔧 Troubleshooting

### Build ล้มเหลว
```bash
# ดู logs
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

### Service ไม่ทำงาน
```bash
# ดู logs
gcloud run logs read riffai-backend --limit=50
gcloud run logs tail riffai-backend
```

### ลบทิ้งเริ่มใหม่
```bash
gcloud run services delete riffai-backend --region=asia-southeast1
gcloud run services delete riffai-frontend --region=asia-southeast1
```

---

## 📚 เอกสารเพิ่มเติม

- [DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md) - คู่มือแบบละเอียด
- [Cloud Run Docs](https://cloud.google.com/run/docs)
