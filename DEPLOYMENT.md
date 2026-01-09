# 🚀 DOMULEX Deployment Guide

## Übersicht

DOMULEX ist jetzt deployment-ready für **Google Cloud Run**. Diese Anleitung zeigt alle Schritte zum Live-Deployment.

---

## ⚡ Quick Start (Empfohlen)

### Option 1: Automatisches Deployment

```bash
# 1. Navigate to project
cd /Users/konstantinkranich/domulex.ai

# 2. Run deployment script
./deploy.sh
```

Das Script erledigt automatisch:
- ✅ Authentication Check
- ✅ API Activation
- ✅ Docker Build
- ✅ Image Push
- ✅ Cloud Run Deployment

---

## 📋 Manuelle Deployment-Schritte

Falls Sie jeden Schritt kontrollieren möchten:

### 1. Vorbereitung

```bash
# Install gcloud CLI (falls noch nicht installiert)
# Download: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set project
gcloud config set project domulex-ai

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Docker Image bauen

```bash
# Build image
docker build -t gcr.io/domulex-ai/domulex-frontend:latest .

# Test locally (optional)
docker run -p 8501:8501 gcr.io/domulex-ai/domulex-frontend:latest
# Visit http://localhost:8501
```

### 3. Push to Google Container Registry

```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Push image
docker push gcr.io/domulex-ai/domulex-frontend:latest
```

### 4. Deploy to Cloud Run

```bash
gcloud run deploy domulex-frontend \
    --image gcr.io/domulex-ai/domulex-frontend:latest \
    --platform managed \
    --region europe-west3 \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "MOCK_MODE=false,API_BASE_URL=https://your-backend-url.run.app"
```

---

## 🔧 Konfiguration

### Environment Variables

Wichtige Variablen für Cloud Run:

```bash
# Set during deployment
--set-env-vars "MOCK_MODE=false,API_BASE_URL=https://backend-url.run.app"

# Update after deployment
gcloud run services update domulex-frontend \
    --region europe-west3 \
    --set-env-vars "API_BASE_URL=https://new-backend-url.run.app"
```

### Backend URL ändern

In `frontend_app.py` (Zeile ~21):

```python
# Development
API_BASE_URL = "http://localhost:8000"

# Production
API_BASE_URL = os.getenv("API_BASE_URL", "https://backend-url.run.app")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
```

---

## 🌐 Backend Deployment (Optional)

Falls Backend noch nicht deployed ist:

```bash
# Navigate to backend
cd backend

# Deploy backend to Cloud Run
gcloud run deploy domulex-backend \
    --source . \
    --platform managed \
    --region europe-west3 \
    --allow-unauthenticated \
    --port 8000 \
    --memory 4Gi \
    --cpu 4 \
    --timeout 300 \
    --set-env-vars "QDRANT_HOST=your-qdrant-url,GEMINI_API_KEY=your-key"
```

Dann Backend-URL in Frontend setzen.

---

## 📊 Deployment-Optionen Vergleich

| Option | Kosten | Komplexität | Empfehlung |
|--------|--------|-------------|------------|
| **Cloud Run** | €€ (Pay-per-use) | Mittel | ✅ Empfohlen |
| **Streamlit Cloud** | Kostenlos | Einfach | Nur für Testing |
| **Heroku** | €€€ | Einfach | Alternative |
| **Docker VPS** | €€ | Hoch | Für Experten |

**Warum Cloud Run?**
- ✅ Automatisches Scaling (0 → 10 Instances)
- ✅ Nur bezahlen bei Nutzung
- ✅ Integriert mit Firebase/GCP
- ✅ HTTPS automatisch
- ✅ Gesundheitschecks integriert

---

## 🧪 Testing nach Deployment

### 1. Health Check

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe domulex-frontend \
    --region europe-west3 \
    --format 'value(status.url)')

# Test health endpoint
curl ${SERVICE_URL}/_stcore/health
```

### 2. UI Testing

Besuchen Sie `${SERVICE_URL}` und testen Sie alle 4 UIs:

- [ ] **Tenant UI:** SOS Buttons funktionieren
- [ ] **Investor UI:** PDF Upload + Metrics angezeigt
- [ ] **Manager UI:** Document Generator erstellt Dokument
- [ ] **Lawyer UI:** Research Tab findet Quellen

### 3. Performance Testing

```bash
# Load test (optional, requires Apache Bench)
ab -n 100 -c 10 ${SERVICE_URL}/

# Monitor logs
gcloud run services logs read domulex-frontend --region europe-west3 --limit 50
```

---

## 💰 Kosten-Schätzung

### Cloud Run Pricing (Stand 2024)

**Kostenlose Tier:**
- 2 Million requests/Monat
- 360,000 GB-Sekunden/Monat
- 180,000 vCPU-Sekunden/Monat

**Bei 2GB RAM, 2 vCPU:**
- Durchschnittliche Request-Zeit: 2s
- 1000 Requests/Tag = ~60 GB-Sekunden/Request
- **Kosten: ~€5-10/Monat** (innerhalb Free Tier möglich!)

### Optimierungen

```bash
# Für geringen Traffic: Kosten senken
gcloud run services update domulex-frontend \
    --region europe-west3 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 3

# Für hohen Traffic: Performance erhöhen
gcloud run services update domulex-frontend \
    --region europe-west3 \
    --memory 4Gi \
    --cpu 4 \
    --max-instances 50 \
    --min-instances 1  # Warm instances
```

---

## 🔐 Sicherheit

### 1. Authentication aktivieren (optional)

```bash
# Nur für authentifizierte Nutzer
gcloud run services update domulex-frontend \
    --region europe-west3 \
    --no-allow-unauthenticated

# Firebase Auth Integration in frontend_app.py:
import firebase_admin
from firebase_admin import auth
```

### 2. CORS konfigurieren

In `frontend_app.py`:

```python
# Streamlit CORS ist automatisch konfiguriert
# Siehe .streamlit/config.toml
```

### 3. Secrets Management

```bash
# Store API keys in Secret Manager
gcloud secrets create gemini-api-key --data-file=-

# Mount in Cloud Run
gcloud run services update domulex-frontend \
    --update-secrets=GEMINI_API_KEY=gemini-api-key:latest
```

---

## 📈 Monitoring & Logs

### Real-time Logs

```bash
# Stream logs
gcloud run services logs tail domulex-frontend --region europe-west3

# Filter errors only
gcloud run services logs read domulex-frontend \
    --region europe-west3 \
    --filter='severity>=ERROR'
```

### Metrics Dashboard

1. Öffnen: https://console.cloud.google.com/run
2. Service: `domulex-frontend` auswählen
3. Tab: "Metrics" → Requests, Latency, Errors

### Alerts einrichten

```bash
# Alert bei hoher Fehlerrate
gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="DOMULEX High Error Rate" \
    --condition-display-name="Error rate > 5%" \
    --condition-threshold-value=0.05
```

---

## 🔄 Updates & Rollbacks

### Neue Version deployen

```bash
# Rebuild & deploy
docker build -t gcr.io/domulex-ai/domulex-frontend:v2 .
docker push gcr.io/domulex-ai/domulex-frontend:v2

gcloud run deploy domulex-frontend \
    --image gcr.io/domulex-ai/domulex-frontend:v2 \
    --region europe-west3
```

### Rollback

```bash
# List revisions
gcloud run revisions list --service domulex-frontend --region europe-west3

# Rollback to previous version
gcloud run services update-traffic domulex-frontend \
    --to-revisions=domulex-frontend-00001-abc=100 \
    --region europe-west3
```

### Blue/Green Deployment

```bash
# Deploy new version with no traffic
gcloud run deploy domulex-frontend \
    --image gcr.io/domulex-ai/domulex-frontend:v2 \
    --no-traffic \
    --region europe-west3

# Gradually shift traffic
gcloud run services update-traffic domulex-frontend \
    --to-revisions=domulex-frontend-00002-xyz=50 \
    --region europe-west3
```

---

## 🌍 Custom Domain (Optional)

### 1. Domain Mapping

```bash
# Map custom domain
gcloud run domain-mappings create \
    --service domulex-frontend \
    --domain app.domulex.ai \
    --region europe-west3

# Verify domain ownership
# Add DNS records as instructed by Cloud Run
```

### 2. SSL Certificate

- Cloud Run provisions SSL certificates automatically
- HTTPS erzwungen
- Renews automatisch

---

## ❓ Troubleshooting

### Problem: "Service not found"

```bash
# Check if service exists
gcloud run services list --region europe-west3

# Re-deploy if missing
./deploy.sh
```

### Problem: "Memory limit exceeded"

```bash
# Increase memory
gcloud run services update domulex-frontend \
    --region europe-west3 \
    --memory 4Gi
```

### Problem: "Cold start latency"

```bash
# Add minimum instances (costs more!)
gcloud run services update domulex-frontend \
    --region europe-west3 \
    --min-instances 1
```

### Problem: "Backend connection failed"

1. Check `API_BASE_URL` environment variable
2. Verify backend is deployed and accessible
3. Check CORS settings in backend

```bash
# Update backend URL
gcloud run services update domulex-frontend \
    --set-env-vars "API_BASE_URL=https://correct-url.run.app"
```

---

## 📁 Deployment-Dateien

| Datei | Zweck |
|-------|-------|
| `Dockerfile` | Container-Build für Streamlit App |
| `.dockerignore` | Ausschluss unnötiger Dateien |
| `.streamlit/config.toml` | Streamlit Produktions-Config |
| `deploy.sh` | Automatisches Deployment-Script |
| `DEPLOYMENT.md` | Diese Anleitung |

---

## ✅ Post-Deployment Checklist

- [ ] App ist unter Service-URL erreichbar
- [ ] Alle 4 UIs funktionieren (Tenant, Investor, Manager, Lawyer)
- [ ] Backend-Verbindung funktioniert (oder Mock Mode aktiv)
- [ ] Logs zeigen keine kritischen Fehler
- [ ] Performance ist akzeptabel (<3s Ladezeit)
- [ ] HTTPS funktioniert
- [ ] Environment Variables korrekt gesetzt
- [ ] Kosten-Alerts aktiviert (optional)
- [ ] Custom Domain gemappt (optional)
- [ ] Backup/Rollback-Plan dokumentiert

---

## 🎉 Erfolg!

Ihre DOMULEX App ist jetzt live auf Google Cloud Run!

**Service URL:** `https://domulex-frontend-XXXXX-ew.a.run.app`

**Nächste Schritte:**
1. Backend deployen (falls noch nicht geschehen)
2. `MOCK_MODE=false` setzen
3. Produktions-Tests durchführen
4. Custom Domain hinzufügen
5. Monitoring Dashboard einrichten

---

**Stand:** 27. Dezember 2024  
**Platform:** Google Cloud Run  
**Region:** europe-west3 (Frankfurt)  
**Status:** ✅ Production Ready
