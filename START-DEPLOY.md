# 🚀 เริ่ม Deploy ใน 3 ขั้นตอน

## ขั้นที่ 1: ติดตั้ง gcloud CLI

**Windows:**
1. ดาวน์โหลด: https://cloud.google.com/sdk/docs/install
2. รันไฟล์ติดตั้ง
3. เปิด Command Prompt ใหม่

**หรือใช้ Cloud Shell** (ไม่ต้องติดตั้ง):
- เปิด https://console.cloud.google.com
- คลิก ปุ่ม Cloud Shell ขวาบน

---

## ขั้นที่ 2: Login และสร้าง Project

```bash
# Login
gcloud auth login

# สร้าง project (ใช้ชื่ออื่นก็ได้)
gcloud projects create riffai-platform-demo

# ตั้งเป็น project ปัจจุบัน
gcloud config set project riffai-platform-demo
```

---

## ขั้นที่ 3: รันสคริปต์ Deploy

**Windows:**
```cmd
cd riffai-platform
deploy-gcp.bat
```

**Linux/Mac:**
```bash
cd riffai-platform
chmod +x deploy-gcp.sh
./deploy-gcp.sh
```

**หรือ Deploy ด้วยมือ:**
```bash
# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Deploy Backend
cd backend
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --allow-unauthenticated

# เก็บ Backend URL
export BACKEND_URL=$(gcloud run services describe riffai-backend --region=asia-southeast1 --format="value(status.url)")

# Deploy Frontend
cd ../frontend
gcloud run deploy riffai-frontend \
  --source . \
  --region=asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL"
```

---

## ✅ เสร็จแล้ว!

รอ 5-10 นาที แล้วจะได้ URL:
- **Frontend**: https://riffai-frontend-xxxxx.run.app
- **Backend**: https://riffai-backend-xxxxx.run.app/docs

---

## 💰 ค่าใช้จ่าย

Cloud Run Free Tier:
- 2 ล้าน requests/เดือน
- 360,000 GB-seconds/เดือน

**= ใช้ฟรีถ้าใช้น้อยๆ**

---

## ⚠️ หมายเหตุ

ตอนนี้ใช้ SQLite ในหน่วยความจำ (ข้อมูลหายเมื่อ restart)

ถ้าต้องการเก็บข้อมูลถาวร ดูคู่มือ:
- [DEPLOY-QUICK.md](./DEPLOY-QUICK.md) - Deploy พร้อม Cloud SQL
- [DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md) - Production แบบเต็ม

---

## 🆘 ติดปัญหา?

```bash
# ดู logs
gcloud run logs read riffai-backend --limit=50

# ลบทิ้งเริ่มใหม่
gcloud run services delete riffai-backend --region=asia-southeast1
gcloud run services delete riffai-frontend --region=asia-southeast1
```

---

## 📚 เอกสารทั้งหมด

1. **START-DEPLOY.md** (ไฟล์นี้) - เริ่มต้นง่ายๆ
2. **DEPLOY-README.md** - เปรียบเทียบวิธี deploy
3. **DEPLOY-QUICK.md** - คำสั่งละเอียด + Cloud SQL
4. **DEPLOYMENT-CHECKLIST.md** - Production แบบเต็ม
