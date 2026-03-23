# 🛰️ Google Earth Engine Setup Guide

คู่มือการตั้งค่า Google Earth Engine สำหรับ RiffAI Platform

---

## 📋 Prerequisites

1. Google Account
2. Google Cloud Project
3. Earth Engine API enabled

---

## 🚀 Quick Setup (Local Development)

### Step 1: Install Earth Engine

```bash
pip install earthengine-api geemap
```

### Step 2: Authenticate

```bash
earthengine authenticate
```

จะเปิด browser ให้ login และ authorize

### Step 3: Test Connection

```bash
cd backend
python -c "import ee; ee.Initialize(); print('✅ Earth Engine connected!')"
```

---

## 🔧 Production Setup (Service Account)

### Step 1: Create Service Account

```bash
# Set project
PROJECT_ID=trim-descent-452802-t2

# Create service account
gcloud iam service-accounts create earth-engine-sa \
  --display-name="Earth Engine Service Account" \
  --project=$PROJECT_ID

# Get service account email
SA_EMAIL=earth-engine-sa@$PROJECT_ID.iam.gserviceaccount.com
```

### Step 2: Grant Permissions

```bash
# Grant Earth Engine permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/earthengine.viewer"

# Grant Storage permissions (for caching)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/storage.objectViewer"
```

### Step 3: Create Key File

```bash
# Create key
gcloud iam service-accounts keys create ee-key.json \
  --iam-account=$SA_EMAIL \
  --project=$PROJECT_ID

# Move to secure location
mv ee-key.json backend/ee-key.json
```

### Step 4: Register with Earth Engine

1. Go to: https://code.earthengine.google.com/
2. Click "Register a noncommercial or commercial Cloud project"
3. Select your project: `trim-descent-452802-t2`
4. Accept terms and register

### Step 5: Set Environment Variables

```bash
# Windows
set GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com
set GEE_KEY_FILE=backend/ee-key.json

# Linux/Mac
export GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com
export GEE_KEY_FILE=backend/ee-key.json
```

---

## 🧪 Testing

### Test 1: Local Test Script

Create `test_ee.py`:

```python
import ee

# Initialize
try:
    ee.Initialize()
    print("✅ Earth Engine initialized")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test query
try:
    # Get a Sentinel-2 image
    image = ee.Image('COPERNICUS/S2_SR_HARMONIZED/20230101T000000_20230101T000000_T47NQH')
    info = image.getInfo()
    print(f"✅ Successfully queried image: {info['id']}")
except Exception as e:
    print(f"❌ Query failed: {e}")
    exit(1)

print("\n🎉 All tests passed!")
```

Run:
```bash
python test_ee.py
```

### Test 2: API Test

Start backend:
```bash
cd backend
uvicorn app.main:app --reload
```

Test endpoint:
```bash
curl http://localhost:8080/api/pipeline/test-ee
```

Expected response:
```json
{
  "status": "connected",
  "message": "Earth Engine is connected and working",
  "initialized": true
}
```

### Test 3: Fetch Real Data

```bash
curl -X POST "http://localhost:8080/api/pipeline/fetch-satellite" \
  -H "Content-Type: application/json" \
  -d '{
    "basin_id": "mekong_north",
    "start_date": "2024-01-01",
    "end_date": "2024-01-10"
  }'
```

---

## 📊 Data Available

### Sentinel-2 (Optical)
- **Resolution**: 10m
- **Bands**: RGB, NIR, SWIR
- **Revisit**: 5 days
- **Indices**: NDVI, NDWI, MNDWI

### Sentinel-1 (SAR)
- **Resolution**: 10-20m
- **All-weather**: Works through clouds
- **Revisit**: 6-12 days
- **Use**: Water detection, flood mapping

---

## 🔍 Troubleshooting

### Error: "Earth Engine not authenticated"

**Solution:**
```bash
earthengine authenticate
```

### Error: "Project not registered"

**Solution:**
1. Go to https://code.earthengine.google.com/
2. Register your project
3. Wait 5-10 minutes for activation

### Error: "Permission denied"

**Solution:**
```bash
# Check service account permissions
gcloud projects get-iam-policy trim-descent-452802-t2 \
  --flatten="bindings[].members" \
  --filter="bindings.members:earth-engine-sa@*"
```

### Error: "No images found"

**Possible causes:**
- Date range too narrow
- Cloud coverage too high
- Area outside Sentinel coverage

**Solution:**
- Expand date range
- Increase cloud coverage threshold
- Check bbox coordinates

---

## 📈 Usage Limits

### Free Tier
- **Compute**: 10,000 requests/day
- **Storage**: 250 GB
- **Export**: 10 concurrent tasks

### Commercial
- Contact Google for pricing
- Higher limits available

---

## 🔐 Security Best Practices

### 1. Protect Service Account Key

```bash
# Never commit to git
echo "ee-key.json" >> .gitignore

# Set proper permissions
chmod 600 ee-key.json
```

### 2. Use Secret Manager (Production)

```bash
# Store key in Secret Manager
gcloud secrets create ee-service-account-key \
  --data-file=ee-key.json \
  --project=trim-descent-452802-t2

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding ee-service-account-key \
  --member="serviceAccount:715107904640-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=trim-descent-452802-t2
```

### 3. Rotate Keys Regularly

```bash
# Create new key
gcloud iam service-accounts keys create ee-key-new.json \
  --iam-account=$SA_EMAIL

# Delete old key
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=$SA_EMAIL
```

---

## 🚀 Deploy to Cloud Run

### Update Backend Dockerfile

Add to `backend/Dockerfile`:
```dockerfile
# Copy Earth Engine key
COPY ee-key.json /app/ee-key.json

# Set environment variables
ENV GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com
ENV GEE_KEY_FILE=/app/ee-key.json
```

### Deploy

```bash
cd backend
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --set-env-vars="GEE_SERVICE_ACCOUNT=earth-engine-sa@trim-descent-452802-t2.iam.gserviceaccount.com,GEE_KEY_FILE=/app/ee-key.json" \
  --project=trim-descent-452802-t2
```

---

## 📚 Resources

### Documentation
- Earth Engine: https://developers.google.com/earth-engine
- Python API: https://developers.google.com/earth-engine/guides/python_install
- Datasets: https://developers.google.com/earth-engine/datasets

### Tutorials
- Get Started: https://developers.google.com/earth-engine/tutorials/tutorial_api_01
- Image Collections: https://developers.google.com/earth-engine/guides/ic_creating
- Reducers: https://developers.google.com/earth-engine/guides/reducers_intro

### Community
- Forum: https://groups.google.com/g/google-earth-engine-developers
- Stack Overflow: https://stackoverflow.com/questions/tagged/google-earth-engine

---

## ✅ Checklist

### Local Development
- [ ] Earth Engine API installed
- [ ] Authenticated with `earthengine authenticate`
- [ ] Test script runs successfully
- [ ] API endpoint returns real data

### Production
- [ ] Service account created
- [ ] Permissions granted
- [ ] Key file secured
- [ ] Project registered with Earth Engine
- [ ] Environment variables set
- [ ] Backend deployed with credentials
- [ ] Real data fetching verified

---

**🎯 Goal: Fetch real satellite data for accurate flood predictions!**

*Last Updated: March 23, 2026*
