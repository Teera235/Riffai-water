#!/bin/bash

# RIFFAI Platform - GCP Cloud Run Deployment Script
# ใช้สคริปต์นี้เพื่อ deploy ขึ้น Google Cloud Run

set -e

# สี
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 RIFFAI Platform - GCP Deployment${NC}"
echo ""

# ตรวจสอบ gcloud CLI
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI ไม่ได้ติดตั้ง${NC}"
    echo "ติดตั้งที่: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# ตั้งค่า Project ID
read -p "GCP Project ID: " PROJECT_ID
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ กรุณาใส่ Project ID${NC}"
    exit 1
fi

gcloud config set project $PROJECT_ID
REGION="asia-southeast1"

echo -e "${YELLOW}📦 กำลัง build และ deploy Backend...${NC}"

# Build Backend
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/riffai-backend

# Deploy Backend
gcloud run deploy riffai-backend \
  --image gcr.io/$PROJECT_ID/riffai-backend \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --memory=1Gi \
  --cpu=1 \
  --timeout=300 \
  --max-instances=10 \
  --min-instances=0

BACKEND_URL=$(gcloud run services describe riffai-backend --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Backend deployed: $BACKEND_URL${NC}"

cd ..

echo -e "${YELLOW}📦 กำลัง build และ deploy Frontend...${NC}"

# Build Frontend
cd frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/riffai-frontend \
  --substitutions=_NEXT_PUBLIC_API_URL=$BACKEND_URL

# Deploy Frontend
gcloud run deploy riffai-frontend \
  --image gcr.io/$PROJECT_ID/riffai-frontend \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL" \
  --memory=512Mi \
  --cpu=1

FRONTEND_URL=$(gcloud run services describe riffai-frontend --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Frontend deployed: $FRONTEND_URL${NC}"

cd ..

echo ""
echo -e "${GREEN}🎉 Deployment สำเร็จ!${NC}"
echo ""
echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo "API Docs: $BACKEND_URL/docs"
echo ""
echo -e "${YELLOW}⚠️  หมายเหตุ: ยังไม่ได้เชื่อม Cloud SQL${NC}"
echo "ตอนนี้ใช้ SQLite ชั่วคราว ถ้าต้องการใช้ Cloud SQL:"
echo "1. สร้าง Cloud SQL instance"
echo "2. เพิ่ม --add-cloudsql-instances flag"
echo "3. ตั้งค่า DATABASE_URL environment variable"
