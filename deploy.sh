#!/bin/bash
# DOMULEX Deployment Script for Google Cloud Run
# This script builds and deploys the Streamlit frontend to Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 DOMULEX Deployment Script${NC}"
echo "=================================="

# Configuration
PROJECT_ID="domulex-ai"
REGION="europe-west3"
SERVICE_NAME="domulex-frontend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: gcloud CLI not found${NC}"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is logged in
echo -e "${YELLOW}🔐 Checking authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}📝 Please login to Google Cloud...${NC}"
    gcloud auth login
fi

# Set project
echo -e "${YELLOW}📦 Setting project to ${PROJECT_ID}...${NC}"
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build Docker image
echo -e "${YELLOW}🏗️  Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:latest .

# Test image locally (optional)
read -p "🧪 Test image locally before deploying? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🧪 Starting local test on port 8501...${NC}"
    echo "Press Ctrl+C to stop and continue with deployment"
    docker run -p 8501:8501 ${IMAGE_NAME}:latest
fi

# Push to Google Container Registry
echo -e "${YELLOW}📤 Pushing image to Google Container Registry...${NC}"
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
echo -e "${YELLOW}🚢 Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME}:latest \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "MOCK_MODE=false,API_BASE_URL=https://domulex-backend-url.run.app"

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo "=================================="
echo -e "${GREEN}🌐 Your app is live at:${NC}"
echo -e "${GREEN}${SERVICE_URL}${NC}"
echo ""
echo "📝 Next steps:"
echo "1. Update API_BASE_URL environment variable with your backend URL"
echo "2. Test all 4 UIs (Tenant, Investor, Manager, Lawyer)"
echo "3. Set up custom domain (optional)"
echo ""
echo "💡 Useful commands:"
echo "  View logs:    gcloud run services logs read ${SERVICE_NAME} --region ${REGION}"
echo "  Update env:   gcloud run services update ${SERVICE_NAME} --region ${REGION} --set-env-vars KEY=VALUE"
echo "  Scale down:   gcloud run services update ${SERVICE_NAME} --region ${REGION} --max-instances 1"
echo ""
