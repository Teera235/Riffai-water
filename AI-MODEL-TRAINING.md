# 🤖 AI Model Training Guide

คู่มือการฝึกและ deploy AI models สำหรับ RiffAI Platform

---

## 📋 Prerequisites

### 1. ติดตั้ง Dependencies
```bash
cd ai-engine
pip install -r requirements.txt
pip install asyncpg psycopg2-binary sqlalchemy google-cloud-storage
```

### 2. ตั้งค่า Database Connection
```bash
# Windows
set DATABASE_URL=postgresql+asyncpg://riffai:riffai123@34.21.160.173/riffai

# Linux/Mac
export DATABASE_URL=postgresql+asyncpg://riffai:riffai123@34.21.160.173/riffai
```

### 3. ตั้งค่า GCP Credentials (สำหรับ upload models)
```bash
gcloud auth application-default login
```

---

## 🚀 Quick Start

### วิธีที่ 1: ใช้ Batch Script (Windows)

```bash
# 1. ฝึกโมเดลทั้ง 3 ลุ่มน้ำ
train-models.bat

# 2. Upload models ไป Cloud Storage
upload-models.bat
```

### วิธีที่ 2: รัน Manual

```bash
cd ai-engine

# ฝึกโมเดลเดียว
python training/train_model.py --basin mekong_north --epochs 50 --batch-size 32

# ฝึกทั้งหมด
python training/train_model.py --basin all --epochs 50 --batch-size 32
```

---

## 📊 Training Process

### Step 1: Load Data from Database

Script จะดึงข้อมูลจาก Cloud SQL:
- Water level records (ระดับน้ำ)
- Rainfall records (ปริมาณฝน)
- ย้อนหลัง 365 วัน

### Step 2: Prepare Features

**Input Features (24 hours):**
- Rainfall (mm)
- Water level (m)
- Evapotranspiration (mm/month)
- Previous water level

**Output (24 hours ahead):**
- Future water level (m)

### Step 3: Train LSTM Model

**Architecture:**
- Encoder-Decoder LSTM
- 128 units per layer
- Dropout 0.2
- Adam optimizer

**Training:**
- 80% train, 20% validation split
- Default: 50 epochs
- Batch size: 32

### Step 4: Evaluate & Save

**Metrics:**
- MSE (Mean Squared Error)
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score (target > 0.85)

**Saved Files:**
- `model.h5` - Trained model
- `scalers.pkl` - Data scalers
- `metrics.txt` - Performance metrics

---

## 📁 Model Storage

### Local Storage
```
ai-engine/models/trained/
├── mekong_north/
│   ├── model.h5
│   ├── scalers.pkl
│   └── metrics.txt
├── eastern_coast/
│   ├── model.h5
│   ├── scalers.pkl
│   └── metrics.txt
└── southern_east/
    ├── model.h5
    ├── scalers.pkl
    └── metrics.txt
```

### Cloud Storage
```
gs://riffai-ai-models/
├── mekong_north/
│   ├── model.h5
│   ├── scalers.pkl
│   └── metrics.txt
├── eastern_coast/
└── southern_east/
```

---

## 🔄 Deploy Models to Production

### Step 1: Upload to Cloud Storage

```bash
# Windows
upload-models.bat

# Manual
gsutil cp ai-engine/models/trained/mekong_north/* gs://riffai-ai-models/mekong_north/
gsutil cp ai-engine/models/trained/eastern_coast/* gs://riffai-ai-models/eastern_coast/
gsutil cp ai-engine/models/trained/southern_east/* gs://riffai-ai-models/southern_east/
```

### Step 2: Restart Backend Service

Backend จะโหลดโมเดลใหม่เมื่อ restart:

```bash
# Redeploy backend
cd backend
gcloud run deploy riffai-backend --source . --region=asia-southeast1 --project=trim-descent-452802-t2
```

หรือ restart service:
```bash
gcloud run services update riffai-backend --region=asia-southeast1 --project=trim-descent-452802-t2
```

### Step 3: Verify Model Loading

ตรวจสอบ logs:
```bash
gcloud run services logs read riffai-backend --region=asia-southeast1 --project=trim-descent-452802-t2 --limit=50
```

ควรเห็น:
```
✅ mekong_north model loaded from GCS
✅ eastern_coast model loaded from GCS
✅ southern_east model loaded from GCS
✅ Loaded 3 AI models
```

---

## 🧪 Testing Models

### Test Prediction API

```bash
curl -X POST "https://riffai-backend-715107904640.asia-southeast1.run.app/api/predict/flood" \
  -H "Content-Type: application/json" \
  -d '{
    "basin_id": "mekong_north",
    "days_ahead": 30
  }'
```

### Check Model Version

```bash
curl "https://riffai-backend-715107904640.asia-southeast1.run.app/api/predict/accuracy"
```

ควรเห็น model version เปลี่ยนจาก `rule-based-v1` เป็น `hydro-lstm-v1`

---

## 📈 Model Performance

### Target Metrics
- **R² Score**: > 0.85
- **RMSE**: < 0.5 m (water level)
- **MAE**: < 0.3 m (water level)

### Monitoring

ตรวจสอบ accuracy ผ่าน API:
```bash
GET /api/predict/accuracy
```

Response:
```json
{
  "models": [
    {
      "version": "hydro-lstm-v1",
      "avg_accuracy": 0.87,
      "predictions": 150,
      "avg_confidence": 0.82
    }
  ]
}
```

---

## 🔧 Troubleshooting

### ปัญหา: Insufficient Data

```
❌ Insufficient data for training (need at least 100 records)
```

**แก้ไข:**
- รัน data pipeline เพื่อดึงข้อมูลเพิ่ม
- ใช้ historical data fetch

```bash
curl -X POST "https://riffai-backend-715107904640.asia-southeast1.run.app/api/pipeline/fetch-historical" \
  -H "Content-Type: application/json" \
  -d '{"basin_id": "mekong_north", "years": 2}'
```

### ปัญหา: Low R² Score

```
R²: 0.45 (target > 0.85)
```

**แก้ไข:**
1. เพิ่ม epochs: `--epochs 100`
2. ปรับ learning rate
3. เพิ่มข้อมูล training
4. Feature engineering

### ปัญหา: Model Not Loading

```
⚠️ Could not load AI models
```

**แก้ไข:**
1. ตรวจสอบว่า models อยู่ใน GCS
2. ตรวจสอบ GCP credentials
3. ตรวจสอบ bucket permissions

```bash
# List models in GCS
gsutil ls gs://riffai-ai-models/

# Check permissions
gsutil iam get gs://riffai-ai-models/
```

---

## 🔄 Retraining Schedule

### Recommended Schedule

- **Weekly**: Retrain with latest data
- **Monthly**: Full retraining with extended history
- **Quarterly**: Model architecture review

### Automated Retraining (Future)

สร้าง Cloud Scheduler job:

```bash
gcloud scheduler jobs create http retrain-models-weekly \
  --location=asia-southeast1 \
  --schedule="0 2 * * 0" \
  --uri="https://riffai-backend-715107904640.asia-southeast1.run.app/api/train/batch" \
  --http-method=POST \
  --time-zone="Asia/Bangkok" \
  --project=trim-descent-452802-t2
```

---

## 📚 References

### Papers
1. Xiang et al. (2020) - LSTM-based sequence-to-sequence learning for rainfall-runoff
2. Xiang & Demir (2020) - Distributed long-term hourly streamflow predictions

### Code
- HydroLSTM: https://github.com/uihilab/HydroLSTM
- TensorFlow: https://www.tensorflow.org/

---

## ✅ Checklist

### Before Training
- [ ] Database has sufficient data (>100 records per basin)
- [ ] Dependencies installed
- [ ] Database connection configured

### After Training
- [ ] Models saved locally
- [ ] Metrics reviewed (R² > 0.85)
- [ ] Models uploaded to GCS
- [ ] Backend restarted
- [ ] Predictions tested

### Production
- [ ] Model loading verified in logs
- [ ] Prediction API working
- [ ] Accuracy monitoring setup
- [ ] Retraining schedule planned

---

**🎯 Goal: Achieve R² > 0.85 for accurate flood predictions!**

*Last Updated: March 23, 2026*
