# DOMULEX.ai - Setup Guide

## Schnellstart (5 Minuten)

### 1. Prerequisites
```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Docker & Docker Compose
docker --version
docker-compose --version
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

**Gemini API Key erhalten:**
1. Besuche https://makersuite.google.com/app/apikey
2. Erstelle neuen API Key
3. Füge in `.env` ein: `GEMINI_API_KEY=dein_key_hier`

### 3. Qdrant Vector Database starten

```bash
# Im Root-Verzeichnis
docker-compose up -d

# Prüfen ob läuft
curl http://localhost:6333/collections
```

### 4. Backend starten

```bash
cd backend
uvicorn main:app --reload

# Backend läuft auf: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 5. Erste Daten laden (wichtig!)

```bash
# In neuem Terminal
# Deutsche Rechtsdokumente
curl -X POST http://localhost:8000/ingest/run \
  -H "Content-Type: application/json" \
  -d '{"jurisdiction":"DE", "max_documents": 20}'

# US Rechtsdokumente
curl -X POST http://localhost:8000/ingest/run \
  -H "Content-Type: application/json" \
  -d '{"jurisdiction":"US", "max_documents": 20}'

# Spanische Rechtsdokumente
curl -X POST http://localhost:8000/ingest/run \
  -H "Content-Type: application/json" \
  -d '{"jurisdiction":"ES", "max_documents": 20}'
```

### 6. Frontend starten

**Option A: Streamlit (schneller MVP)**
```bash
# Im Root-Verzeichnis
streamlit run frontend_app.py

# Öffnet automatisch: http://localhost:8501
```

**Option B: Next.js (Produktion)**
```bash
npm install
npm run dev

# Läuft auf: http://localhost:3000
```

---

## Erste Schritte

### Test 1: Einfache Rechtsabfrage
1. Öffne http://localhost:8501
2. Wähle Rolle: **Tenant**
3. Wähle Jurisdiction: **🇺🇸 United States**
4. Wähle Language: **🇩🇪 Deutsch**
5. Frage: "Was sind meine Rechte als Mieter in Florida?"
6. Erwarte: Antwort auf Deutsch mit Florida-Gesetzen

### Test 2: PDF-Vertragsanalyse
1. Gehe zu Sidebar → "Contract Analysis"
2. Upload einen Mietvertrag (PDF)
3. Klicke "Analyze Contract"
4. Erwarte: Risikobewertung (🟢🟡🔴)

### Test 3: Konfliktlösung
1. Wechsle zu Tab "⚖️ Dispute Resolver"
2. Party A (Landlord): "Mieter zahlt seit 2 Monaten keine Miete"
3. Party B (Tenant): "Heizung kaputt seit 3 Monaten"
4. Klicke "Analyze Legal Situation"
5. Erwarte: Neutrale Mediation mit Erfolgswahrscheinlichkeiten

---

## Erweiterte Konfiguration

### Firebase Setup (für Authentifizierung)

1. **Firebase Service Account erstellen:**
   ```bash
   # In Firebase Console:
   # Project Settings → Service Accounts → Generate New Private Key
   ```

2. **Credentials in .env einfügen:**
   ```bash
   FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   ```

### Redis Cache aktivieren (optional)

```bash
# In docker-compose.yml ist Redis bereits definiert
docker-compose up -d redis

# In .env aktivieren
ENABLE_CACHE=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

### CourtListener API (US Rechtsprechung)

```bash
# Registriere dich auf: https://www.courtlistener.com/
# Erhalte API Key
# In .env einfügen:
COURTLISTENER_API_KEY=dein_key
```

---

## Troubleshooting

### Problem: "Cannot connect to Qdrant"
```bash
# Prüfe ob Container läuft
docker ps | grep qdrant

# Neustarten
docker-compose restart qdrant

# Logs prüfen
docker logs domulex-qdrant
```

### Problem: "No documents found"
```bash
# Daten neu indexieren
curl -X POST http://localhost:8000/ingest/run \
  -H "Content-Type: application/json" \
  -d '{"jurisdiction":"DE", "force_refresh": true}'
```

### Problem: "Gemini API Error"
```bash
# API Key prüfen
echo $GEMINI_API_KEY

# Quota prüfen auf: https://makersuite.google.com/app/apikey
```

### Problem: "ModuleNotFoundError"
```bash
# Virtual environment aktiv?
which python
# Sollte zeigen: .../venv/bin/python

# Dependencies neu installieren
pip install -r requirements.txt --force-reinstall
```

---

## Produktionsdeployment

### Docker Production Build

```bash
# Build alle Services
docker-compose -f docker-compose.prod.yml up -d

# Prüfe Health
curl http://localhost:8000/health
```

### Firebase Hosting Deploy

```bash
# Next.js build
npm run build

# Firebase deploy
firebase deploy --only hosting
```

### Backend auf Cloud Run

```bash
# Build Docker Image
docker build -t gcr.io/domulex-ai/backend:latest ./backend

# Push zu GCR
docker push gcr.io/domulex-ai/backend:latest

# Deploy
gcloud run deploy domulex-backend \
  --image gcr.io/domulex-ai/backend:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

---

## Entwicklung

### Tests ausführen

```bash
# Backend Tests
cd backend
pytest tests/ -v

# Frontend Tests
npm test

# E2E Tests
npm run test:e2e
```

### Linting & Formatting

```bash
# Python
black backend/
flake8 backend/

# TypeScript
npm run lint
npm run format
```

### Neue Jurisdiction hinzufügen

1. `backend/models/legal.py` → `Jurisdiction` Enum erweitern
2. `backend/ingestion/scraper_factory.py` → Neuen Scraper erstellen
3. `backend/rag/prompts.py` → Cultural Bridge Prompts hinzufügen
4. Daten indexieren: `POST /ingest/run`

---

## Support

- **Dokumentation:** [README.md](README.md)
- **API Docs:** http://localhost:8000/docs
- **GitHub Issues:** https://github.com/kranichkonstantin-png/domulex.ai/issues
