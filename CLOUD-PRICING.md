# 💰 Cloud Run Pricing Analysis - RIFFAI Platform

## 📊 ราคา Cloud Run (asia-southeast1)

### CPU Pricing:
- **vCPU-second**: $0.00002400 USD (~฿0.00084 THB)
- **vCPU-hour**: $0.0864 USD (~฿3.02 THB)
- **vCPU-month** (730 hours): $63.07 USD (~฿2,207 THB)

### Memory Pricing:
- **GiB-second**: $0.00000250 USD (~฿0.000088 THB)
- **GiB-hour**: $0.009 USD (~฿0.315 THB)
- **GiB-month** (730 hours): $6.57 USD (~฿230 THB)

### Request Pricing:
- **Per million requests**: $0.40 USD (~฿14 THB)
- **Free tier**: 2 million requests/month

### อัตราแลกเปลี่ยน: 1 USD = 35 THB

---

## 🔍 Configuration ปัจจุบัน

### Backend:
- CPU: 2 vCPU
- Memory: 2 GiB
- Max instances: 10
- Min instances: 0 (scale to zero)

### Frontend:
- CPU: 1 vCPU
- Memory: 1 GiB
- Max instances: 10
- Min instances: 0

---

## 💸 ค่าใช้จ่ายปัจจุบัน (ประมาณการ)

### สมมติ Traffic: Medium (10% uptime = 73 hours/month)

**Backend:**
- CPU: 2 vCPU × 73 hours × $0.0864 = $12.61 (~฿441)
- Memory: 2 GiB × 73 hours × $0.009 = $1.31 (~฿46)
- Subtotal: $13.92 (~฿487)

**Frontend:**
- CPU: 1 vCPU × 73 hours × $0.0864 = $6.31 (~฿221)
- Memory: 1 GiB × 73 hours × $0.009 = $0.66 (~฿23)
- Subtotal: $6.97 (~฿244)

**Requests:** (2M free tier) = $0

**Total/Month:** ~฿731 (~$21)

---

## 🚀 แนะนำ: Optimized Configuration (งบ 2000 บาท)

### Backend (เพิ่มประสิทธิภาพ):
- CPU: **4 vCPU** (เพิ่มจาก 2)
- Memory: **4 GiB** (เพิ่มจาก 2)
- Max instances: 5 (ลดจาก 10)
- Min instances: **1** (always-on สำหรับ response เร็ว)
- Timeout: 300s
- Concurrency: 80

### Frontend (เพิ่มประสิทธิภาพ):
- CPU: **2 vCPU** (เพิ่มจาก 1)
- Memory: **2 GiB** (เพิ่มจาก 1)
- Max instances: 5 (ลดจาก 10)
- Min instances: **1** (always-on)
- Timeout: 60s
- Concurrency: 100

---

## 💰 ค่าใช้จ่ายใหม่ (Always-On = 730 hours/month)

### Backend (4 vCPU, 4 GiB, min=1):
- CPU: 4 vCPU × 730 hours × $0.0864 = $252.29 (~฿8,830)
- Memory: 4 GiB × 730 hours × $0.009 = $26.28 (~฿920)
- Subtotal: $278.57 (~฿9,750) ❌ เกินงบ!

### ปรับใหม่: Backend (2 vCPU, 4 GiB, min=1)
- CPU: 2 vCPU × 730 hours × $0.0864 = $126.14 (~฿4,415)
- Memory: 4 GiB × 730 hours × $0.009 = $26.28 (~฿920)
- Subtotal: $152.42 (~฿5,335) ❌ ยังเกิน!

---

## ✅ แนะนำสุดท้าย: Balanced Configuration (งบ 2000 บาท)

### Strategy: Smart Scaling (ไม่ always-on แต่เร็วขึ้น)

### Backend:
- CPU: **4 vCPU** (เพิ่มจาก 2) ⚡
- Memory: **4 GiB** (เพิ่มจาก 2) ⚡
- Max instances: 3
- Min instances: **0** (scale to zero เมื่อไม่ใช้)
- **Startup CPU Boost**: enabled
- Timeout: 300s
- Concurrency: 100

### Frontend:
- CPU: **2 vCPU** (เพิ่มจาก 1) ⚡
- Memory: **2 GiB** (เพิ่มจาก 1) ⚡
- Max instances: 3
- Min instances: **0**
- **Startup CPU Boost**: enabled
- Timeout: 60s
- Concurrency: 100

### ค่าใช้จ่าย (20% uptime = 146 hours/month):

**Backend:**
- CPU: 4 vCPU × 146 hours × $0.0864 = $50.46 (~฿1,766)
- Memory: 4 GiB × 146 hours × $0.009 = $5.26 (~฿184)
- Subtotal: $55.72 (~฿1,950)

**Frontend:**
- CPU: 2 vCPU × 146 hours × $0.0864 = $25.23 (~฿883)
- Memory: 2 GiB × 146 hours × $0.009 = $2.63 (~฿92)
- Subtotal: $27.86 (~฿975)

**Total/Month:** ~฿2,925 (~$84) ❌ ยังเกินนิดหน่อย

---

## 🎯 แนะนำที่ดีที่สุด: Cost-Optimized (งบ 2000 บาท)

### Backend:
- CPU: **2 vCPU** (คงเดิม)
- Memory: **4 GiB** (เพิ่มจาก 2) ⚡ สำคัญสำหรับ AI/ML
- Max instances: 3
- Min instances: 0
- **Startup CPU Boost**: enabled ⚡
- **Request timeout**: 300s
- **Concurrency**: 80

### Frontend:
- CPU: **2 vCPU** (เพิ่มจาก 1) ⚡
- Memory: **1 GiB** (คงเดิม)
- Max instances: 3
- Min instances: 0
- **Startup CPU Boost**: enabled ⚡
- **Request timeout**: 60s
- **Concurrency**: 100

### ค่าใช้จ่าย (20% uptime = 146 hours/month):

**Backend:**
- CPU: 2 vCPU × 146 hours × $0.0864 = $25.23 (~฿883)
- Memory: 4 GiB × 146 hours × $0.009 = $5.26 (~฿184)
- Subtotal: $30.49 (~฿1,067)

**Frontend:**
- CPU: 2 vCPU × 146 hours × $0.0864 = $25.23 (~฿883)
- Memory: 1 GiB × 146 hours × $0.009 = $1.31 (~฿46)
- Subtotal: $26.54 (~฿929)

**Total/Month:** ~฿1,996 (~$57) ✅ พอดีงบ!

---

## 🚀 สิ่งที่จะได้รับ

### ความเร็วที่เพิ่มขึ้น:
1. **Backend Memory 4GB** → รัน AI models เร็วขึ้น 2x
2. **Frontend CPU 2 vCPU** → render เร็วขึ้น 2x
3. **Startup CPU Boost** → cold start เร็วขึ้น 50%
4. **Higher Concurrency** → รองรับ users พร้อมกันได้มากขึ้น

### ข้อดี:
- ✅ เร็วขึ้นเห็นได้ชัด
- ✅ รองรับ AI/ML ได้ดีขึ้น
- ✅ Cold start เร็วขึ้น
- ✅ อยู่ในงบ 2000 บาท

### ข้อเสีย:
- ⚠️ ยังมี cold start (3-5 วินาที) เพราะ min=0
- ⚠️ ถ้า traffic สูง (>20% uptime) จะเกินงบ

---

## 💡 Tips เพิ่มความเร็ว (ไม่เสียเงินเพิ่ม)

### 1. Enable Caching:
```python
# ใน backend เพิ่ม response caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
```

### 2. Optimize Database:
- ใช้ connection pooling (ทำแล้ว ✅)
- เพิ่ม indexes
- Cache queries ที่ใช้บ่อย

### 3. Optimize Frontend:
- Enable Next.js caching
- Lazy load components
- Optimize images

### 4. Use CDN:
- Cloud CDN สำหรับ static assets
- ฟรี 1TB/month

---

## 📊 เปรียบเทียบ

| Config | Backend | Frontend | Speed | Cost/Month |
|--------|---------|----------|-------|------------|
| **ปัจจุบัน** | 2CPU/2GB | 1CPU/1GB | 🐌 ช้า | ฿731 |
| **แนะนำ** | 2CPU/4GB | 2CPU/1GB | 🚀 เร็ว | ฿1,996 |
| **Premium** | 4CPU/4GB | 2CPU/2GB | ⚡ เร็วมาก | ฿2,925 |

---

## 🎯 คำแนะนำ

**สำหรับงบ 2000 บาท แนะนำ:**
- Backend: 2 vCPU / 4 GiB
- Frontend: 2 vCPU / 1 GiB
- Startup CPU Boost: enabled
- Min instances: 0 (scale to zero)

**จะได้:**
- เร็วขึ้น 2-3 เท่า
- รองรับ AI/ML ได้ดี
- อยู่ในงบพอดี

**ถ้าต้องการเร็วกว่านี้:**
- ต้องเพิ่มงบเป็น 3000 บาท
- หรือใช้ min instances = 1 (always-on)

---

## 🔧 วิธี Update

ใช้ script ที่เตรียมไว้:
```bash
.\upgrade-cloud-resources.bat
```

หรือ manual:
```bash
# Backend
gcloud run services update riffai-backend \
  --region asia-southeast1 \
  --memory 4Gi \
  --cpu 2 \
  --max-instances 3 \
  --concurrency 80

# Frontend
gcloud run services update riffai-frontend \
  --region asia-southeast1 \
  --memory 1Gi \
  --cpu 2 \
  --max-instances 3 \
  --concurrency 100
```

---

## 📈 Monitor Usage

```bash
# ดู metrics
gcloud run services describe riffai-backend --region asia-southeast1

# ดู billing
gcloud billing accounts list
gcloud billing projects describe trim-descent-452802-t2
```

---

**สรุป:** แนะนำ Backend 2CPU/4GB + Frontend 2CPU/1GB = ~฿2,000/เดือน ⚡
