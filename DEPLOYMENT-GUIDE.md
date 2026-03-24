# 🚀 RIFFAI Platform - Deployment Guide

## 📋 Prerequisites

### Required Tools:
- ✅ Docker Desktop
- ✅ Google Cloud SDK (gcloud CLI)
- ✅ Git
- ✅ Node.js 20+ (for local development)
- ✅ Python 3.11+ (for local development)

### Google Cloud Setup:
1. GCP Project: `trim-descent-452802-t2`
2. Region: `asia-southeast1`
3. APIs enabled:
   - Cloud Run API
   - Container Registry API
   - Cloud Build API

---

## 🐳 Option 1: Docker Compose (Local Testing)

### Quick Start:
```bash
# Start all services
docker-start.bat

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## ☁️ Option 2: Google Cloud Run (Production)

### 1. Deploy Backend Only:
```bash
cd backend
deploy-backend.bat
```

**What it does:**
1. Builds Docker image
2. Pushes to Google Container Registry
3. Deploys to Cloud Run
4. Configures:
   - Memory: 2Gi
   - CPU: 2
   - Max instances: 10
   - Timeout: 300s

### 2. Deploy Frontend Only:
```bash
cd frontend
deploy-frontend.bat
```

**What it does:**
1. Builds Next.js Docker image
2. Pushes to GCR
3. Deploys to Cloud Run
4. Connects to backend API

### 3. Deploy Everything:
```bash
deploy-all.bat
```

**What it does:**
1. Deploys backend first
2. Waits for backend to be ready
3. Deploys frontend
4. Shows all URLs

---

## 🔧 Configuration

### Backend Environment Variables:
```bash
DATABASE_URL=sqlite+aiosqlite:///./riffai.db
DEBUG=False
ENVIRONMENT=production
PORT=8080
```

### Frontend Environment Variables:
```bash
NEXT_PUBLIC_API_URL=https://riffai-backend-xxx.run.app
PORT=8080
```

---

## 📦 Docker Images

### Backend Image:
- Base: `python:3.11-slim`
- Size: ~500MB
- Includes: FastAPI, SQLAlchemy, Earth Engine

### Frontend Image:
- Base: `node:20-alpine`
- Size: ~200MB
- Multi-stage build
- Standalone Next.js output

---

## 🚀 Deployment Steps (Detailed)

### Step 1: Authenticate with GCP
```bash
gcloud auth login
gcloud config set project trim-descent-452802-t2
```

### Step 2: Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 3: Configure Docker for GCR
```bash
gcloud auth configure-docker
```

### Step 4: Deploy Backend
```bash
cd backend
docker build -t gcr.io/trim-descent-452802-t2/riffai-backend .
docker push gcr.io/trim-descent-452802-t2/riffai-backend

gcloud run deploy riffai-backend \
  --image gcr.io/trim-descent-452802-t2/riffai-backend \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

### Step 5: Get Backend URL
```bash
gcloud run services describe riffai-backend \
  --region asia-southeast1 \
  --format "value(status.url)"
```

### Step 6: Deploy Frontend
```bash
cd frontend
docker build -t gcr.io/trim-descent-452802-t2/riffai-frontend .
docker push gcr.io/trim-descent-452802-t2/riffai-frontend

gcloud run deploy riffai-frontend \
  --image gcr.io/trim-descent-452802-t2/riffai-frontend \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars "NEXT_PUBLIC_API_URL=<BACKEND_URL>"
```

---

## 🔍 Monitoring & Logs

### View Logs:
```bash
# Backend logs
gcloud run services logs read riffai-backend --region asia-southeast1

# Frontend logs
gcloud run services logs read riffai-frontend --region asia-southeast1

# Follow logs (real-time)
gcloud run services logs tail riffai-backend --region asia-southeast1
```

### Check Service Status:
```bash
gcloud run services describe riffai-backend --region asia-southeast1
gcloud run services describe riffai-frontend --region asia-southeast1
```

---

## 🔄 Update Deployment

### Update Backend:
```bash
cd backend
deploy-backend.bat
```

### Update Frontend:
```bash
cd frontend
deploy-frontend.bat
```

### Rollback:
```bash
# List revisions
gcloud run revisions list --service riffai-backend --region asia-southeast1

# Rollback to previous revision
gcloud run services update-traffic riffai-backend \
  --to-revisions <REVISION_NAME>=100 \
  --region asia-southeast1
```

---

## 💰 Cost Optimization

### Cloud Run Pricing:
- **Free tier**: 2 million requests/month
- **CPU**: $0.00002400/vCPU-second
- **Memory**: $0.00000250/GiB-second
- **Requests**: $0.40/million requests

### Estimated Monthly Cost:
- Low traffic: $5-10/month
- Medium traffic: $20-50/month
- High traffic: $100+/month

### Tips:
1. Set `--max-instances` to control costs
2. Use `--min-instances 0` for auto-scaling to zero
3. Enable request timeout
4. Monitor usage in GCP Console

---

## 🔒 Security

### Best Practices:
1. ✅ Use environment variables for secrets
2. ✅ Enable HTTPS (automatic on Cloud Run)
3. ✅ Set up CORS properly
4. ✅ Use service accounts
5. ✅ Enable Cloud Armor (optional)

### Secrets Management:
```bash
# Create secret
gcloud secrets create database-url --data-file=-

# Use in Cloud Run
gcloud run deploy riffai-backend \
  --set-secrets DATABASE_URL=database-url:latest
```

---

## 🐛 Troubleshooting

### Issue: Build fails
**Solution**: Check Docker logs
```bash
docker build -t test . --progress=plain
```

### Issue: Deployment fails
**Solution**: Check Cloud Run logs
```bash
gcloud run services logs read riffai-backend --region asia-southeast1 --limit 50
```

### Issue: Frontend can't connect to backend
**Solution**: Check CORS settings and backend URL
```bash
# Verify backend URL
echo $NEXT_PUBLIC_API_URL

# Test backend
curl https://riffai-backend-xxx.run.app/health
```

### Issue: Out of memory
**Solution**: Increase memory allocation
```bash
gcloud run services update riffai-backend \
  --memory 4Gi \
  --region asia-southeast1
```

---

## 📊 Health Checks

### Backend Health:
```bash
curl https://riffai-backend-xxx.run.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Frontend Health:
```bash
curl https://riffai-frontend-xxx.run.app
```

Expected: HTTP 200 OK

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Update environment variables
- [ ] Set up Cloud SQL (if needed)
- [ ] Configure custom domain
- [ ] Set up SSL certificate
- [ ] Enable monitoring
- [ ] Set up alerts
- [ ] Configure backups
- [ ] Test all features
- [ ] Load testing
- [ ] Security audit

---

## 📞 Support

### Useful Commands:
```bash
# List all services
gcloud run services list --region asia-southeast1

# Delete service
gcloud run services delete riffai-backend --region asia-southeast1

# Update service
gcloud run services update riffai-backend --memory 4Gi --region asia-southeast1

# View service details
gcloud run services describe riffai-backend --region asia-southeast1
```

### Resources:
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Docker Documentation](https://docs.docker.com)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎉 Success!

Your RIFFAI Platform is now deployed and ready to use!

**URLs:**
- Backend: https://riffai-backend-715107904640.asia-southeast1.run.app
- Frontend: https://riffai-frontend-xxx.asia-southeast1.run.app
- API Docs: https://riffai-backend-715107904640.asia-southeast1.run.app/docs

**Next Steps:**
1. Test all features
2. Monitor performance
3. Set up custom domain (optional)
4. Configure alerts
5. Enjoy! 🚀
