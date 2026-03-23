# 🚀 RIFFAI Platform - Deployment Checklist

## Pre-Deployment Checklist

### ✅ Prerequisites
- [ ] Google Cloud Platform account with billing enabled
- [ ] `gcloud` CLI installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
- [ ] Docker installed and running
- [ ] Git repository ready
- [ ] Domain name (optional, for custom domain)

### ✅ Local Testing
- [ ] Docker services running: `docker compose ps`
- [ ] Backend accessible: http://localhost:8080/docs
- [ ] Frontend accessible: http://localhost:3000
- [ ] Database seeded with data

---

## Phase 1: GCP Project Setup (15 minutes)

### Step 1.1: Login to GCP
```bash
# Login
gcloud auth login

# Set your project ID (replace with your project)
export PROJECT_ID="riffai-platform"
gcloud config set project $PROJECT_ID

# If project doesn't exist, create it
gcloud projects create $PROJECT_ID --name="RIFFAI Platform"
```

### Step 1.2: Enable Required APIs
```bash
# Enable all required APIs at once
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  redis.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  cloudscheduler.googleapis.com \
  compute.googleapis.com
```

### Step 1.3: Set Region
```bash
# Set default region (Singapore)
gcloud config set run/region asia-southeast1
export REGION="asia-southeast1"
```

---

## Phase 2: Database Setup (20 minutes)

### Step 2.1: Create Cloud SQL Instance
```bash
# Create PostgreSQL instance with PostGIS
gcloud sql instances create riffai-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --root-password="CHANGE_THIS_PASSWORD" \
  --database-flags=cloudsql.iam_authentication=on

# Wait for instance to be ready (takes 5-10 minutes)
gcloud sql instances describe riffai-db --format="value(state)"
```

### Step 2.2: Create Database and User
```bash
# Create database
gcloud sql databases create riffai --instance=riffai-db

# Create user
gcloud sql users create riffai \
  --instance=riffai-db \
  --password="CHANGE_THIS_PASSWORD"
```

### Step 2.3: Enable PostGIS Extension
```bash
# Connect to database
gcloud sql connect riffai-db --user=postgres --database=riffai

# In psql prompt, run:
# CREATE EXTENSION IF NOT EXISTS postgis;
# \q
```

---

## Phase 3: Storage Setup (10 minutes)

### Step 3.1: Create Cloud Storage Buckets
```bash
# Satellite images bucket
gsutil mb -l $REGION gs://${PROJECT_ID}-satellite-images
gsutil iam ch allUsers:objectViewer gs://${PROJECT_ID}-satellite-images

# AI models bucket
gsutil mb -l $REGION gs://${PROJECT_ID}-models

# Reports bucket
gsutil mb -l $REGION gs://${PROJECT_ID}-reports
```

---

## Phase 4: Backend Deployment (30 minutes)

### Step 4.1: Prepare Environment Variables
Create `backend/.env.production`:
```bash
DATABASE_URL=postgresql+asyncpg://riffai:PASSWORD@/riffai?host=/cloudsql/PROJECT_ID:REGION:riffai-db
REDIS_HOST=REDIS_IP
SECRET_KEY=GENERATE_RANDOM_SECRET_KEY
GCP_PROJECT_ID=PROJECT_ID
GCS_BUCKET_SATELLITE=PROJECT_ID-satellite-images
GCS_BUCKET_MODELS=PROJECT_ID-models
GCS_BUCKET_REPORTS=PROJECT_ID-reports
ENVIRONMENT=production
```

### Step 4.2: Build and Deploy Backend
```bash
cd backend

# Build container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/riffai-backend

# Deploy to Cloud Run
gcloud run deploy riffai-backend \
  --image gcr.io/$PROJECT_ID/riffai-backend \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:riffai-db \
  --set-env-vars="DATABASE_URL=postgresql+asyncpg://riffai:PASSWORD@/riffai?host=/cloudsql/$PROJECT_ID:$REGION:riffai-db" \
  --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
  --set-env-vars="ENVIRONMENT=production" \
  --memory=1Gi \
  --cpu=1 \
  --timeout=300 \
  --max-instances=10 \
  --min-instances=0

# Get backend URL
export BACKEND_URL=$(gcloud run services describe riffai-backend --region=$REGION --format="value(status.url)")
echo "Backend URL: $BACKEND_URL"
```

### Step 4.3: Test Backend
```bash
# Health check
curl $BACKEND_URL/health

# API docs
echo "API Docs: $BACKEND_URL/docs"
```

---

## Phase 5: Frontend Deployment (20 minutes)

### Option A: Deploy to Vercel (Recommended - Free)

#### Step 5.1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 5.2: Deploy Frontend
```bash
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL production
# Enter: YOUR_BACKEND_URL (from Phase 4)
```

### Option B: Deploy to Cloud Run

```bash
cd frontend

# Build container
gcloud builds submit --tag gcr.io/$PROJECT_ID/riffai-frontend

# Deploy
gcloud run deploy riffai-frontend \
  --image gcr.io/$PROJECT_ID/riffai-frontend \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL" \
  --memory=512Mi \
  --cpu=1

# Get frontend URL
export FRONTEND_URL=$(gcloud run services describe riffai-frontend --region=$REGION --format="value(status.url)")
echo "Frontend URL: $FRONTEND_URL"
```

---

## Phase 6: Database Migration & Seeding (10 minutes)

### Step 6.1: Run Migrations
```bash
# Connect via Cloud SQL Proxy
cloud_sql_proxy -instances=$PROJECT_ID:$REGION:riffai-db=tcp:5432 &

# Run migrations
cd backend
alembic upgrade head

# Seed database
python -m app.seed
```

---

## Phase 7: Automated Jobs Setup (15 minutes)

### Step 7.1: Create Cloud Scheduler Jobs
```bash
# Fetch water data every hour
gcloud scheduler jobs create http fetch-water \
  --schedule="0 * * * *" \
  --uri="$BACKEND_URL/api/pipeline/fetch-water" \
  --http-method=POST \
  --location=$REGION

# Fetch satellite data daily at 2 AM
gcloud scheduler jobs create http fetch-satellite \
  --schedule="0 2 * * *" \
  --uri="$BACKEND_URL/api/pipeline/fetch-satellite" \
  --http-method=POST \
  --location=$REGION

# Run predictions daily at 6 AM
gcloud scheduler jobs create http daily-prediction-mekong \
  --schedule="0 6 * * *" \
  --uri="$BACKEND_URL/api/predict/flood?basin_id=mekong_north" \
  --http-method=POST \
  --location=$REGION

# Check alerts every 15 minutes
gcloud scheduler jobs create http check-alerts \
  --schedule="*/15 * * * *" \
  --uri="$BACKEND_URL/api/alerts/check" \
  --http-method=POST \
  --location=$REGION
```

---

## Phase 8: Monitoring & Logging (10 minutes)

### Step 8.1: Setup Cloud Logging
```bash
# View logs
gcloud run logs read riffai-backend --limit=50

# Follow logs in real-time
gcloud run logs tail riffai-backend
```

### Step 8.2: Setup Alerts
```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="RIFFAI High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05
```

---

## Phase 9: Security Hardening (15 minutes)

### Step 9.1: Setup IAM Roles
```bash
# Create service account
gcloud iam service-accounts create riffai-backend \
  --display-name="RIFFAI Backend Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:riffai-backend@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:riffai-backend@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### Step 9.2: Enable Cloud Armor (DDoS Protection)
```bash
# Create security policy
gcloud compute security-policies create riffai-policy \
  --description="RIFFAI DDoS protection"

# Add rate limiting rule
gcloud compute security-policies rules create 1000 \
  --security-policy=riffai-policy \
  --expression="true" \
  --action=rate-based-ban \
  --rate-limit-threshold-count=100 \
  --rate-limit-threshold-interval-sec=60
```

---

## Phase 10: Custom Domain (Optional - 20 minutes)

### Step 10.1: Map Custom Domain
```bash
# Map domain to Cloud Run service
gcloud run domain-mappings create \
  --service=riffai-backend \
  --domain=api.riffai.org \
  --region=$REGION

gcloud run domain-mappings create \
  --service=riffai-frontend \
  --domain=riffai.org \
  --region=$REGION
```

### Step 10.2: Update DNS Records
Add the following DNS records at your domain registrar:
```
Type: CNAME
Name: api
Value: ghs.googlehosted.com

Type: CNAME  
Name: www
Value: ghs.googlehosted.com
```

---

## Post-Deployment Verification

### ✅ Backend Checks
- [ ] Health endpoint: `curl $BACKEND_URL/health`
- [ ] API docs accessible: `$BACKEND_URL/docs`
- [ ] Dashboard API: `curl $BACKEND_URL/api/dashboard/overview`
- [ ] Database connection working
- [ ] Cloud Storage accessible

### ✅ Frontend Checks
- [ ] Homepage loads: `$FRONTEND_URL`
- [ ] Dashboard displays data
- [ ] Map renders correctly
- [ ] Predict form works
- [ ] Alerts page loads
- [ ] Reports page loads

### ✅ Automated Jobs
- [ ] Scheduler jobs created
- [ ] Jobs running successfully
- [ ] Check job logs: `gcloud scheduler jobs describe fetch-water --location=$REGION`

### ✅ Monitoring
- [ ] Logs accessible in Cloud Console
- [ ] Alerts configured
- [ ] Error tracking enabled

---

## Estimated Costs (Monthly)

### Free Tier Usage
- Cloud Run: 2M requests/month (FREE)
- Cloud Storage: 5GB (FREE)
- Cloud Logging: 50GB (FREE)

### Paid Services
- **Cloud SQL (db-f1-micro)**: ~$10-15/month
- **Cloud Run (beyond free tier)**: ~$5-10/month
- **Cloud Storage (beyond 5GB)**: ~$0.02/GB/month
- **Cloud Scheduler**: $0.10/job/month (~$0.40/month)

**Total Estimated Cost: $15-30/month**

---

## Rollback Procedure

### If deployment fails:

#### Rollback Backend
```bash
# List revisions
gcloud run revisions list --service=riffai-backend --region=$REGION

# Rollback to previous revision
gcloud run services update-traffic riffai-backend \
  --to-revisions=PREVIOUS_REVISION=100 \
  --region=$REGION
```

#### Rollback Frontend (Vercel)
```bash
# List deployments
vercel ls

# Rollback to previous deployment
vercel rollback DEPLOYMENT_URL
```

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
gcloud run logs read riffai-backend --limit=100

# Common issues:
# - Database connection: Check DATABASE_URL
# - Missing env vars: Check all required vars are set
# - Memory limit: Increase --memory flag
```

### Database connection fails
```bash
# Test connection
gcloud sql connect riffai-db --user=riffai

# Check Cloud SQL proxy
cloud_sql_proxy -instances=$PROJECT_ID:$REGION:riffai-db=tcp:5432
```

### Frontend can't reach backend
```bash
# Check CORS settings in backend
# Verify NEXT_PUBLIC_API_URL is correct
# Check Cloud Run allows unauthenticated requests
```

---

## Support & Resources

- **GCP Console**: https://console.cloud.google.com
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Cloud SQL Docs**: https://cloud.google.com/sql/docs
- **Vercel Docs**: https://vercel.com/docs

---

## Next Steps After Deployment

1. **Monitor for 24 hours** - Check logs and metrics
2. **Test all features** - Verify everything works in production
3. **Setup backups** - Configure automated database backups
4. **Performance tuning** - Optimize based on real usage
5. **Security audit** - Review IAM roles and permissions
6. **Documentation** - Update team documentation with URLs

---

**Deployment Complete! 🎉**

Your RIFFAI platform is now live and ready for production use.
