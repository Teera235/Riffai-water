# 🌍 Google Earth Engine Authentication Guide

มี 2 วิธีในการ authenticate Earth Engine:

## 🔧 วิธีที่ 1: User Authentication (Local Development)

ใช้สำหรับทดสอบและพัฒนาบนเครื่อง local

### ขั้นตอน:

1. **ติดตั้ง Earth Engine API**
```bash
pip install earthengine-api geemap
```

2. **Authenticate**
```bash
earthengine authenticate
```
- จะเปิด browser ให้ login ด้วย Google account
- เลือก account ที่มีสิทธิ์ใช้ Earth Engine
- Copy authorization code กลับมาใส่ใน terminal

3. **ทดสอบ**
```bash
python -c "import ee; ee.Initialize(); print('Success!')"
```

4. **หรือใช้ script อัตโนมัติ**
```bash
.\setup-earth-engine.bat
```

### ข้อดี:
- ✅ ง่าย รวดเร็ว
- ✅ เหมาะสำหรับ development

### ข้อเสีย:
- ❌ ใช้ไม่ได้บน production/Cloud Run
- ❌ ต้อง authenticate ใหม่ทุกครั้งที่เปลี่ยนเครื่อง

---

## 🔐 วิธีที่ 2: Service Account (Production)

ใช้สำหรับ production deployment บน Cloud Run

### ขั้นตอน:

#### 1. สร้าง Service Account

```bash
# Set variables
set PROJECT_ID=trim-descent-452802-t2
set SA_NAME=earth-engine-sa
set SA_EMAIL=%SA_NAME%@%PROJECT_ID%.iam.gserviceaccount.com

# Create service account
gcloud iam service-accounts create %SA_NAME% ^
    --display-name="Earth Engine Service Account" ^
    --project=%PROJECT_ID%
```

#### 2. Grant Permissions

```bash
# Earth Engine viewer role
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SA_EMAIL%" ^
    --role="roles/earthengine.viewer"

# Storage access (for satellite data)
gcloud projects add-iam-policy-binding %PROJECT_ID% ^
    --member="serviceAccount:%SA_EMAIL%" ^
    --role="roles/storage.objectViewer"
```

#### 3. Create Key File

```bash
gcloud iam service-accounts keys create earth-engine-key.json ^
    --iam-account=%SA_EMAIL% ^
    --project=%PROJECT_ID%
```

#### 4. Register with Earth Engine

**Option A: ผ่าน Web Console**
1. ไปที่: https://code.earthengine.google.com/
2. Sign in ด้วย Google account
3. คลิก "Assets" tab
4. คลิก "NEW" > "Cloud Project"
5. ใส่ Project ID: `trim-descent-452802-t2`
6. Service account จะถูก register อัตโนมัติ

**Option B: ผ่าน Command Line**
```bash
earthengine set_project trim-descent-452802-t2
```

#### 5. Upload to Secret Manager

```bash
# Create secret
gcloud secrets create earth-engine-key ^
    --data-file=earth-engine-key.json ^
    --project=%PROJECT_ID% ^
    --replication-policy="automatic"

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding earth-engine-key ^
    --member="serviceAccount:715107904640-compute@developer.gserviceaccount.com" ^
    --role="roles/secretmanager.secretAccessor" ^
    --project=%PROJECT_ID%
```

#### 6. Update Cloud Run Deployment

แก้ไข `backend/cloudbuild.yaml`:

```yaml
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'riffai-backend'
      - '--source=.'
      - '--region=asia-southeast1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=2Gi'
      - '--cpu=2'
      - '--set-env-vars=GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com'
      - '--set-secrets=GEE_KEY_FILE=earth-engine-key:latest'
```

#### 7. Redeploy

```bash
cd backend
gcloud builds submit --config=cloudbuild.yaml --region=asia-southeast1
```

### หรือใช้ script อัตโนมัติ:

```bash
.\setup-earth-engine-service-account.bat
```

---

## 🧪 Testing

### Local Testing (User Auth)

```bash
# Test connection
python test-satellite-indices.py

# Or via API
cd backend
.\start-local.bat

# Then test
curl http://localhost:8000/api/pipeline/test-ee
```

### Production Testing (Service Account)

```bash
# Test Earth Engine
curl https://riffai-backend-715107904640.asia-southeast1.run.app/api/pipeline/test-ee

# Fetch real Sentinel-2 data
curl -X POST "https://riffai-backend-715107904640.asia-southeast1.run.app/api/pipeline/fetch-satellite?basin_id=mekong_north"

# Fetch real Sentinel-1 SAR data
curl -X POST "https://riffai-backend-715107904640.asia-southeast1.run.app/api/pipeline/fetch-sar?basin_id=mekong_north"
```

---

## 📝 Environment Variables

### Local (.env file)

```bash
# User authentication (automatic after earthengine authenticate)
# No env vars needed

# OR Service account
GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com
GEE_KEY_FILE=earth-engine-key.json
```

### Cloud Run (Environment Variables)

```bash
GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com
```

### Cloud Run (Secrets)

```bash
GEE_KEY_FILE=/secrets/earth-engine-key
```

---

## 🔍 Troubleshooting

### Error: "Project not found"

**Solution:**
```bash
earthengine set_project trim-descent-452802-t2
```

### Error: "Service account not registered"

**Solution:**
1. ไปที่ https://code.earthengine.google.com/
2. Register project ใหม่
3. รอ 5-10 นาที

### Error: "Permission denied"

**Solution:**
```bash
# Check permissions
gcloud projects get-iam-policy trim-descent-452802-t2 ^
    --flatten="bindings[].members" ^
    --filter="bindings.members:earth-engine-sa@*"

# Re-grant if needed
gcloud projects add-iam-policy-binding trim-descent-452802-t2 ^
    --member="serviceAccount:earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com" ^
    --role="roles/earthengine.viewer"
```

### Error: "Secret not found"

**Solution:**
```bash
# List secrets
gcloud secrets list --project=trim-descent-452802-t2

# Create if missing
gcloud secrets create earth-engine-key ^
    --data-file=earth-engine-key.json ^
    --project=trim-descent-452802-t2
```

---

## 📊 Verification

หลังจาก authenticate แล้ว ควรเห็น:

### Mock Mode (ก่อน authenticate)
```
⚠️  Earth Engine not authenticated
    Running in MOCK mode
```

### Real Mode (หลัง authenticate)
```
✅ Earth Engine initialized with default credentials
🛰️  Satellite Service initialized (Earth Engine)
```

### API Response

**Mock:**
```json
{
  "status": "mock",
  "message": "Running in mock mode"
}
```

**Real:**
```json
{
  "status": "connected",
  "message": "Earth Engine is connected and working"
}
```

---

## 🎯 Next Steps

หลังจาก authenticate แล้ว:

1. ✅ ทดสอบดึงข้อมูลจริง
2. ✅ ดู satellite images บน map
3. ✅ ฝึก AI model ด้วยข้อมูลจริง
4. ✅ Deploy production พร้อม real data

---

## 📚 Resources

- [Earth Engine Signup](https://earthengine.google.com/signup/)
- [Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install)
- [Service Account Guide](https://developers.google.com/earth-engine/guides/service_account)
- [GCP Secret Manager](https://cloud.google.com/secret-manager/docs)
