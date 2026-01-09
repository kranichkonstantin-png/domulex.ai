#!/bin/bash
# DOMULEX Backend Deployment Script for Google Cloud Run
# Mit allen Stripe-Produktionsvariablen

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 DOMULEX Backend Deployment Script${NC}"
echo "========================================"

# Configuration
PROJECT_ID="domulex-ai"
REGION="europe-west3"
SERVICE_NAME="domulex-backend"

# Stripe Produktions-Konfiguration
# ⚠️ SECRETS AUS GOOGLE CLOUD SECRET MANAGER LADEN
# Setze diese Werte über: gcloud secrets oder .env.local (NICHT committen!)
STRIPE_SECRET_KEY="${STRIPE_SECRET_KEY:-}"
STRIPE_WEBHOOK_SECRET="${STRIPE_WEBHOOK_SECRET:-}"
STRIPE_PRICE_TENANT="price_1Sj8l83LV15CfXasN3zUqv2v"      # Basis: 19€/Monat
STRIPE_PRICE_PRO="price_1Siuom3LV15CfXasXmpE2LCt"         # Professional: 39€/Monat
STRIPE_PRICE_LAWYER="price_1Siutl3LV15CfXas4Mxel6SS"      # Lawyer Pro: 69€/Monat

# Gemini & Qdrant
# ⚠️ AUCH GEMINI KEY SOLLTE AUS SECRET MANAGER KOMMEN
GEMINI_API_KEY="${GEMINI_API_KEY:-}"
QDRANT_HOST="domulex-qdrant-841507936108.europe-west3.run.app"
QDRANT_USE_HTTPS="true"

# CORS
CORS_ORIGINS="https://domulex-frontend-841507936108.europe-west3.run.app,https://domulex-ai.web.app"

echo -e "${YELLOW}📦 Setting project to ${PROJECT_ID}...${NC}"
gcloud config set project ${PROJECT_ID}

echo -e "${YELLOW}🚢 Deploying Backend to Cloud Run with Stripe configuration...${NC}"
cd backend

gcloud run deploy ${SERVICE_NAME} \
    --source . \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8000 \
    --memory 4Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY}" \
    --set-env-vars "QDRANT_HOST=${QDRANT_HOST}" \
    --set-env-vars "QDRANT_USE_HTTPS=${QDRANT_USE_HTTPS}" \
    --set-env-vars "CORS_ORIGINS=${CORS_ORIGINS}" \
    --set-env-vars "STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}" \
    --set-env-vars "STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}" \
    --set-env-vars "STRIPE_PRICE_TENANT=${STRIPE_PRICE_TENANT}" \
    --set-env-vars "STRIPE_PRICE_PRO=${STRIPE_PRICE_PRO}" \
    --set-env-vars "STRIPE_PRICE_LAWYER=${STRIPE_PRICE_LAWYER}" \
    --set-env-vars "ENVIRONMENT=production" \
    --quiet

cd ..

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}✅ Backend Deployment successful!${NC}"
echo "========================================"
echo -e "${GREEN}🌐 Backend URL: ${SERVICE_URL}${NC}"
echo ""
echo -e "${GREEN}💳 Stripe Konfiguration:${NC}"
echo "  Basis (19€):        ${STRIPE_PRICE_TENANT}"
echo "  Professional (39€): ${STRIPE_PRICE_PRO}"
echo "  Lawyer Pro (69€):   ${STRIPE_PRICE_LAWYER}"
echo ""
echo "📝 Nächste Schritte:"
echo "1. Webhook URL in Stripe Dashboard konfigurieren:"
echo "   ${SERVICE_URL}/stripe/webhook"
echo "2. Frontend deployen: firebase deploy --only hosting"
echo "3. Testen: https://domulex-ai.web.app"
echo ""
