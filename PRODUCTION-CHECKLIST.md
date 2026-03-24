# ✅ Production Deployment Checklist

## 🔍 Pre-Deployment Checks

### 1. Code Quality
- [x] All fixes applied
- [x] Database connection pool configured
- [x] Error handling added
- [x] CORS configured
- [x] API endpoints working
- [x] Map data loading fixed

### 2. Configuration
- [ ] Frontend API URL points to production backend
- [ ] Environment variables set correctly
- [ ] Database configured (Cloud SQL or SQLite)
- [ ] Secrets managed properly
- [ ] CORS allows production domains

### 3. Performance
- [x] Backend: 2 vCPU / 4 GiB
- [x] Frontend: 2 vCPU / 1 GiB
- [x] Startup CPU Boost enabled
- [x] Connection pooling configured
- [x] Max instances: 3

### 4. Security
- [ ] No hardcoded secrets
- [ ] HTTPS enabled (automatic on Cloud Run)
- [ ] Authentication working
- [ ] Input validation
- [ ] SQL injection prevention

### 5. Monitoring
- [ ] Logging configured
- [ ] Error tracking
- [ ] Performance monitoring
- [ ] Cost alerts set

---

## 🚀 Deployment Steps

### Step 1: Update Frontend API URL
```bash
# Frontend needs to point to production backend
NEXT_PUBLIC_API_URL=https://riffai-backend-715107904640.asia-southeast1.run.app
```

### Step 2: Build & Deploy Backend
```bash
cd backend
docker build -t gcr.io/trim-descent-452802-t2/riffai-backend .
docker push gcr.io/trim-descent-452802-t2/riffai-backend
gcloud run deploy riffai-backend --image gcr.io/trim-descent-452802-t2/riffai-backend --region asia-southeast1
```

### Step 3: Build & Deploy Frontend
```bash
cd frontend
docker build -t gcr.io/trim-descent-452802-t2/riffai-frontend .
docker push gcr.io/trim-descent-452802-t2/riffai-frontend
gcloud run deploy riffai-frontend --image gcr.io/trim-descent-452802-t2/riffai-frontend --region asia-southeast1
```

### Step 4: Verify Deployment
```bash
# Test backend
curl https://riffai-backend-715107904640.asia-southeast1.run.app/health

# Test frontend
curl https://riffai-frontend-715107904640.asia-southeast1.run.app
```

---

## 📋 Current Status

### Backend:
- URL: https://riffai-backend-715107904640.asia-southeast1.run.app
- CPU: 2 vCPU
- Memory: 4 GiB
- Status: ✅ Upgraded

### Frontend:
- URL: https://riffai-frontend-715107904640.asia-southeast1.run.app
- CPU: 2 vCPU
- Memory: 1 GiB
- Status: ✅ Upgraded

### Cost:
- Estimated: ~฿2,000/month
- Within budget: ✅

---

## ⚠️ Issues to Fix Before Deploy

### 1. Frontend Environment Variable
**Issue:** Frontend .env.local points to localhost

**Fix:** Update for production
```env
NEXT_PUBLIC_API_URL=https://riffai-backend-715107904640.asia-southeast1.run.app
```

### 2. Database
**Issue:** Using SQLite (not suitable for production)

**Options:**
- Keep SQLite (simple, but limited)
- Migrate to Cloud SQL (better, but costs more)

**Recommendation:** Keep SQLite for now, migrate later if needed

### 3. Secrets
**Issue:** No secrets management

**Fix:** Use environment variables in Cloud Run

---

## 🎯 Ready to Deploy?

Run this command:
```bash
.\deploy-all.bat
```

This will:
1. Build backend Docker image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Build frontend Docker image
5. Push to GCR
6. Deploy to Cloud Run
7. Show URLs

---

## 📊 Post-Deployment Verification

### 1. Test Backend:
```bash
curl https://riffai-backend-715107904640.asia-southeast1.run.app/health
curl https://riffai-backend-715107904640.asia-southeast1.run.app/api/map/rivers
curl https://riffai-backend-715107904640.asia-southeast1.run.app/api/map/dams
```

### 2. Test Frontend:
- Open: https://riffai-frontend-715107904640.asia-southeast1.run.app
- Check map page loads
- Check data displays
- Check all features work

### 3. Monitor:
```bash
# View logs
gcloud run services logs read riffai-backend --region asia-southeast1 --limit 50

# Check metrics
gcloud run services describe riffai-backend --region asia-southeast1
```

---

## 💰 Cost Monitoring

Set up budget alert:
```bash
gcloud billing budgets create \
  --billing-account=<YOUR_BILLING_ACCOUNT> \
  --display-name="RIFFAI Budget" \
  --budget-amount=2000THB \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
```

---

## 🔄 Rollback Plan

If something goes wrong:
```bash
# List revisions
gcloud run revisions list --service riffai-backend --region asia-southeast1

# Rollback to previous
gcloud run services update-traffic riffai-backend \
  --to-revisions <PREVIOUS_REVISION>=100 \
  --region asia-southeast1
```

---

## ✅ Final Checklist

Before going live:
- [ ] All code changes deployed
- [ ] Frontend points to production backend
- [ ] All features tested
- [ ] Performance acceptable
- [ ] No errors in logs
- [ ] Cost within budget
- [ ] Monitoring set up
- [ ] Backup plan ready

---

**Status:** Ready to deploy! 🚀
