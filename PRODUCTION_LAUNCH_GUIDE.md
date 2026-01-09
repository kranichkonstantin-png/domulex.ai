# 🚀 DOMULEX.ai - Produktions-Deployment Guide

## ✅ Was bereits deployed ist

### Frontend (Streamlit)
- **URL:** https://domulex-frontend-841507936108.europe-west3.run.app
- **Features:**
  - ✅ 4 Role-Specific UIs (Tenant/Investor/Manager/Lawyer)
  - ✅ Subscription & Billing System
  - ✅ Query Quota Management
  - ✅ Multi-Jurisdiction (DE/US/ES mit allen Sub-Regionen)
  - ✅ 7-Tage PRO Trial

### Backend API (FastAPI)
- **URL:** https://domulex-backend-841507936108.europe-west3.run.app
- **Features:**
  - ✅ Gemini 2.5 Flash Integration
  - ✅ Graceful Degradation (funktioniert ohne Qdrant)
  - ✅ Strict Grounding (Anti-Hallucination)
  - ✅ Cultural Bridge Prompts

### Qdrant Vector DB
- **Status:** Container deployed, aber nicht vom Backend erreichbar
- **URL:** https://domulex-qdrant-841507936108.europe-west3.run.app
- **Problem:** Cloud Run Services können sich nicht direkt verbinden (VPC Connector benötigt)

---

## 🔧 Fehlende Schritte für vollständige Produktion

### 1. Qdrant Setup (Wähle eine Option)

#### Option A: Qdrant Cloud (EMPFOHLEN - Einfachste Lösung)
```bash
# 1. Gehe zu https://cloud.qdrant.io/
# 2. Erstelle kostenlosen Account (1GB Free Tier)
# 3. Erstelle Cluster in eu-central Region
# 4. Kopiere Cluster URL und API Key
# 5. Update Backend Environment:

gcloud run services update domulex-backend \
  --region europe-west3 \
  --set-env-vars "QDRANT_HOST=your-cluster-id.eu-central.aws.cloud.qdrant.io,QDRANT_PORT=6333,QDRANT_USE_HTTPS=true,QDRANT_API_KEY=your-api-key"
```

#### Option B: Cloud Run mit VPC Connector (Komplex)
```bash
# 1. VPC Connector erstellen
gcloud compute networks vpc-access connectors create domulex-connector \
  --region=europe-west3 \
  --range=10.8.0.0/28

# 2. Qdrant Service mit VPC verbinden
gcloud run services update domulex-qdrant \
  --region europe-west3 \
  --vpc-connector domulex-connector

# 3. Backend mit VPC verbinden
gcloud run services update domulex-backend \
  --region europe-west3 \
  --vpc-connector domulex-connector \
  --set-env-vars "QDRANT_HOST=domulex-qdrant,QDRANT_PORT=6333,QDRANT_USE_HTTPS=false"
```

#### Option C: Lokales Development
```bash
# Starte Qdrant lokal
docker-compose -f qdrant-docker-compose.yml up -d

# Ingest Sample Data
python seed_data.py
```

---

### 2. Legal Documents Ingestion

Nach Qdrant-Setup:

```bash
# Sample Data (4 Dokumente für schnellen Test)
python seed_data.py

# Oder: Vollständige Ingestion mit Celery Worker (24/7 Auto-Update)
cd backend
celery -A ingestion.celery_worker worker --loglevel=info

# Starte Tasks:
# - German: Celery Beat Task für BGB, ZPO etc.
# - US: CourtListener API Integration
# - Spanish: BOE Scraper
```

**Verfügbare Quellen:**
- 🇩🇪 Deutschland: BGB, ZPO, GVG (via gesetze-im-internet.de)
- 🇺🇸 USA: CourtListener API (Rechtsprechung)  
- 🇪🇸 Spanien: BOE (Boletin Oficial del Estado)

---

### 3. Firebase Authentication (Optional aber empfohlen)

```bash
# 1. Firebase Console: Authentication aktivieren
# 2. Email/Password Provider aktivieren
# 3. Service Account Key herunterladen
# 4. Backend updaten:

gcloud run services update domulex-backend \
  --region europe-west3 \
  --set-env-vars "FIREBASE_PROJECT_ID=domulex-ai,FIREBASE_PRIVATE_KEY_ID=...,FIREBASE_CLIENT_EMAIL=..."
```

**Frontend Integration:**
- Login/Signup UI in Streamlit
- Session Management
- User Profile & Subscription Tracking

---

### 4. Redis Caching (Performance)

```bash
# Option A: Cloud Run Redis (Memorystore)
gcloud redis instances create domulex-cache \
  --size=1 \
  --region=europe-west3 \
  --redis-version=redis_6_x

# Option B: Redis Labs Cloud (Free 30MB)
# https://redis.com/try-free/

# Backend Environment:
gcloud run services update domulex-backend \
  --region europe-west3 \
  --set-env-vars "REDIS_HOST=<redis-ip>,REDIS_PORT=6379,ENABLE_CACHE=true"
```

---

### 5. Monitoring & Logging

```bash
# Sentry für Error Tracking
gcloud run services update domulex-backend \
  --region europe-west3 \
  --set-env-vars "SENTRY_DSN=https://your-sentry-dsn,SENTRY_ENVIRONMENT=production"

# Cloud Logging bereits aktiv:
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=domulex-backend" --limit 50
```

---

### 6. Custom Domain & SSL

```bash
# 1. Domain in Cloud Run mappieren
gcloud run domain-mappings create \
  --service domulex-frontend \
  --domain app.domulex.ai \
  --region europe-west3

# 2. DNS konfigurieren (bei Domain-Registrar)
# Typ: CNAME
# Name: app
# Wert: ghs.googlehosted.com

# SSL Certificate wird automatisch von Google bereitgestellt
```

---

### 7. Stripe Payment Integration (Subscription Billing)

```python
# Backend: Stripe Integration
# 1. Stripe Account erstellen
# 2. API Keys kopieren
# 3. Webhooks konfigurieren für subscription updates

# Environment Variables:
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_PRO=price_...
STRIPE_PRICE_ID_ENTERPRISE=price_...
```

**Frontend Changes Needed:**
- Ersetze Mock-Checkout mit echtem Stripe Checkout
- Payment Success/Cancel Redirects
- Subscription Management Page

---

## 📊 Cost Breakdown (Monatlich)

| Service | Free Tier | Paid (bei Wachstum) |
|---------|-----------|---------------------|
| **Cloud Run Frontend** | 2M Requests frei | $0.40/M Requests |
| **Cloud Run Backend** | 2M Requests frei | $0.40/M Requests |
| **Qdrant Cloud** | 1GB frei | $25/Monat (5GB) |
| **Gemini API** | 1500 Queries/Tag frei | $7/1K Queries |
| **Firebase Auth** | 50K Users frei | $0.0055/User |
| **Redis (Memorystore)** | - | ~$30/Monat (1GB) |
| **Domain** | - | ~$12/Jahr |
| **Stripe** | - | 1.4% + €0.25/Transaktion |

**Geschätzte Kosten für 1000 aktive User:** €50-100/Monat

**Subscription Preise (optimiert für deutschen Markt):**
- **FREE:** 0€ - 10 Fragen/Monat (Lead-Generation)
- **PRO:** 29€ - 500 Fragen/Monat (Privatpersonen & kleine Vermieter)
- **BUSINESS:** 99€ - 2.500 Fragen/Monat + API (Immobilienverwalter & kleine Firmen)

**Break-Even Analyse:**
- Bei 100 PRO-Kunden: 2.900€ Umsatz → profitabel ✅
- Bei 20 BUSINESS-Kunden: 1.980€ Umsatz → profitabel ✅

---

## 🎯 Prioritäten für Go-Live

### KRITISCH (vor Launch):
1. ✅ Frontend deployed
2. ✅ Backend deployed  
3. ✅ Subscription UI
4. ⚠️ **Qdrant Cloud Setup** (für echte RAG-Antworten)
5. ⚠️ **Legal Documents Ingestion** (mind. 100 Dokumente)
6. ⚠️ **Stripe Integration** (für echte Zahlungen)

### WICHTIG (innerhalb 2 Wochen):
7. ⏳ Firebase Authentication
8. ⏳ Redis Caching
9. ⏳ Custom Domain
10. ⏳ Error Monitoring (Sentry)

### NICE-TO-HAVE (innerhalb 1 Monat):
11. ⏳ Celery Auto-Ingestion (24/7 Updates)
12. ⏳ Email Notifications
13. ⏳ User Dashboard
14. ⏳ Admin Panel

---

## 🚀 Quick Launch Checklist

```bash
# Tag 1: Qdrant Setup
□ Qdrant Cloud Account erstellen
□ Cluster konfigurieren
□ Backend Environment updaten
□ Test-Query durchführen

# Tag 2: Data Ingestion
□ seed_data.py ausführen (4 Beispieldokumente)
□ Erweiterte Scraper konfigurieren
□ 100+ Dokumente ingesten (DE/US/ES mix)

# Tag 3: Payment Setup
□ Stripe Account erstellen
□ Products & Prices konfigurieren
□ Checkout Flow implementieren
□ Test-Zahlung durchführen

# Tag 4: Final Testing
□ Alle 4 UIs testen
□ Query Limits überprüfen
□ Subscription Flow testen
□ RAG-Antworten validieren

# Tag 5: LAUNCH! 🚀
□ Custom Domain aktivieren
□ Monitoring alerts konfigurieren
□ Marketing Material vorbereiten
□ Social Media ankündigen
```

---

## 📞 Support & Next Steps

Bei Fragen oder Problemen:
1. Logs prüfen: `gcloud logging read ...`
2. Health Endpoints checken
3. Dokumentation in /backend/README.md

**Deployed:** 2025-12-27  
**Status:** 🟡 Beta (Gemini-only, kein RAG)  
**Next:** ✅ Qdrant Cloud + Data Ingestion für vollständige RAG-Funktionalität
