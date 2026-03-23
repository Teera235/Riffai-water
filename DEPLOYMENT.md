# RIFFAI Deployment Guide

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed
- Docker installed
- Terraform installed (optional)

## Local Development

```bash
cd infrastructure/docker
docker compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs

## Deploy to GCP Cloud Run

### 1. Setup GCP Project

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable pubsub.googleapis.com
```

### 2. Create Cloud SQL Instance

```bash
# Create PostgreSQL instance with PostGIS
gcloud sql instances create riffai-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-southeast1 \
  --root-password=YOUR_SECURE_PASSWORD

# Create database
gcloud sql databases create riffai --instance=riffai-db

# Create user
gcloud sql users create riffai \
  --instance=riffai-db \
  --password=YOUR_SECURE_PASSWORD
```

### 3. Create Redis Instance

```bash
gcloud redis instances create riffai-cache \
  --size=1 \
  --region=asia-southeast1 \
  --redis-version=redis_7_0
```

### 4. Create Cloud Storage Buckets

```bash
# Satellite images
gsutil mb -l asia-southeast1 gs://riffai-satellite-images

# AI models
gsutil mb -l asia-southeast1 gs://riffai-models

# Reports
gsutil mb -l asia-southeast1 gs://riffai-reports
```

### 5. Deploy Backend to Cloud Run

```bash
cd backend

# Build and deploy
gcloud run deploy riffai-backend \
  --source . \
  --region=asia-southeast1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars="DATABASE_URL=postgresql+asyncpg://riffai:PASSWORD@/riffai?host=/cloudsql/PROJECT:REGION:riffai-db" \
  --set-env-vars="REDIS_HOST=REDIS_IP" \
  --set-env-vars="GCP_PROJECT_ID=YOUR_PROJECT_ID" \
  --add-cloudsql-instances=PROJECT:REGION:riffai-db \
  --memory=1Gi \
  --cpu=1 \
  --timeout=300 \
  --max-instances=10
```

### 6. Deploy Frontend (Vercel)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://riffai-backend-xxx.run.app
```

### 7. Setup Cloud Scheduler

```bash
# Fetch water data every hour
gcloud scheduler jobs create http fetch-water \
  --schedule="0 * * * *" \
  --uri="https://riffai-backend-xxx.run.app/api/pipeline/fetch-water" \
  --http-method=POST \
  --location=asia-southeast1

# Fetch satellite data daily
gcloud scheduler jobs create http fetch-satellite \
  --schedule="0 2 * * *" \
  --uri="https://riffai-backend-xxx.run.app/api/pipeline/fetch-satellite" \
  --http-method=POST \
  --location=asia-southeast1

# Run predictions daily
gcloud scheduler jobs create http daily-prediction \
  --schedule="0 6 * * *" \
  --uri="https://riffai-backend-xxx.run.app/api/predict/flood?basin_id=mekong_north" \
  --http-method=POST \
  --location=asia-southeast1

# Check alerts every 15 minutes
gcloud scheduler jobs create http check-alerts \
  --schedule="*/15 * * * *" \
  --uri="https://riffai-backend-xxx.run.app/api/alerts/check" \
  --http-method=POST \
  --location=asia-southeast1
```

### 8. Setup Pub/Sub for Alerts

```bash
# Create topic
gcloud pubsub topics create flood-alerts

# Create subscription
gcloud pubsub subscriptions create flood-alerts-sub \
  --topic=flood-alerts

# Setup Cloud Function for LINE Notify (optional)
# See: https://cloud.google.com/functions/docs/quickstart
```

## Using Terraform (Recommended)

```bash
cd infrastructure/terraform

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply

# Destroy (cleanup)
terraform destroy
```

## Database Migrations

```bash
# Run migrations on Cloud SQL
gcloud sql connect riffai-db --user=riffai

# Or use Cloud SQL Proxy
cloud_sql_proxy -instances=PROJECT:REGION:riffai-db=tcp:5432

# Then run migrations
cd backend
alembic upgrade head
```

## Monitoring & Logging

### View Logs
```bash
# Backend logs
gcloud run logs read riffai-backend --limit=50

# Follow logs
gcloud run logs tail riffai-backend
```

### Setup Alerts
```bash
# Create alert policy for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05
```

## Cost Optimization

### Free Tier Limits
- Cloud Run: 2M requests/month
- Cloud SQL: db-f1-micro free
- Cloud Storage: 5GB free
- Pub/Sub: 10GB/month free

### Estimated Monthly Cost
- Cloud Run: $10-30
- Cloud SQL: $20-50
- Redis: $30-50
- Storage: $5-10
- **Total: ~$65-140/month**

## Security Checklist

- [ ] Enable Cloud Armor (DDoS protection)
- [ ] Setup VPC Service Controls
- [ ] Enable Cloud SQL SSL
- [ ] Rotate secrets regularly
- [ ] Enable audit logging
- [ ] Setup IAM roles properly
- [ ] Enable Secret Manager
- [ ] Configure CORS properly

## Backup Strategy

```bash
# Automated backups (Cloud SQL)
gcloud sql instances patch riffai-db \
  --backup-start-time=02:00 \
  --enable-bin-log

# Manual backup
gcloud sql backups create --instance=riffai-db

# Restore from backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=riffai-db \
  --backup-id=BACKUP_ID
```

## Rollback Procedure

```bash
# Rollback Cloud Run deployment
gcloud run services update-traffic riffai-backend \
  --to-revisions=PREVIOUS_REVISION=100

# Rollback database migration
alembic downgrade -1
```

## Support

- GCP Console: https://console.cloud.google.com
- Cloud Run Docs: https://cloud.google.com/run/docs
- Support: support@riffai.org
