# DOMULEX.ai - Global Real Estate Legal Assistant

🏛️ **KI-gestützte Rechtsberatung für Immobilien über Ländergrenzen hinweg**

[![CI/CD](https://github.com/kranichkonstantin-png/domulex.ai/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/kranichkonstantin-png/domulex.ai/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌍 Über DOMULEX

DOMULEX ist eine Legal-Tech-Plattform, die internationale Immobilieninvestoren, Vermieter und Mieter bei rechtlichen Fragen in Deutschland 🇩🇪, Spanien 🇪🇸 und den USA 🇺🇸 unterstützt.

### ✨ Hauptfunktionen

- **💬 Mehrsprachige Rechtsberatung**: Stelle Fragen auf Deutsch, erhalte Antworten zu US-Recht (Cultural Bridge)
- **📄 PDF-Vertragsanalyse**: Upload Mietverträge → Automatische Risikobewertung (🟢🟡🔴)
- **⚖️ Konfliktlösung**: Neutrale KI-Mediation mit Erfolgswahrscheinlichkeiten
- **🔍 Jurisdiktions-Filter**: Strikte Trennung (DE/ES/US) verhindert rechtliche Halluzinationen

### 🏢 Professional-Features (Objektverwaltung)

- **📊 Portfolio-Dashboard**: Alle Objekte auf einen Blick mit Mieteinnahmen-Tracking
- **📬 Mahnwesen**: 3-stufiges System (Erinnerung → Mahnung → Letzte Mahnung)
- **📊 Zählerstandserfassung**: 5 Zählertypen mit automatischer Verbrauchsberechnung
- **📋 WEG-Beschlussbuch**: Eigentümerbeschlüsse verwalten & Umsetzung tracken
- **🔧 Handwerker-Kontakte**: 9 Kategorien zentral verwalten
- **📈 Mieterhöhung-Rechner**: Index- & Mietspiegelberechnung mit Kappungsgrenze
- **💰 Steuer-Optimierung**: AfA-Berechnung, Spekulationsfrist, Grunderwerbsteuer

### 📚 Rechtsquellen-Datenbank

**Stand:** 1.610 Dokumente (29.12.2025)

- **Gesetze:** BGB, WEG, ZPO, EStG, GRC, AEUV, GBO, BeurkG, GNotKG
- **Rechtsprechung:** EuGH (10), BGH (24), BFH (19), OLG/LG/AG
- **Literatur:** Palandt, MüKo, Staudinger, Schmidt
- **Verwaltung:** BMF-Schreiben (8), EU-Richtlinien (6)

**🎯 Ziel:** 5.000+ Dokumente bis Q1/2026 → [DATENBANK_MASTERPLAN.md](DATENBANK_MASTERPLAN.md)

---

## 🚀 Schnellstart

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Google Gemini API Key ([Get Key](https://makersuite.google.com/app/apikey))

### Installation

```bash
# 1. Repository klonen
git clone https://github.com/kranichkonstantin-png/domulex.ai.git
cd domulex.ai

# 2. Backend einrichten
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Umgebungsvariablen konfigurieren
cp .env.example .env
# .env editieren und GEMINI_API_KEY einfügen

# 4. Qdrant & Redis starten
docker-compose up -d

# 5. Backend starten
uvicorn main:app --reload

# 6. In neuem Terminal: Daten indexieren
curl -X POST http://localhost:8000/ingest/run \
  -H "Content-Type: application/json" \
  -d '{"jurisdiction":"DE", "max_documents": 20}'

# 7. Frontend starten (Option A: Streamlit)
cd ..
streamlit run frontend_app.py

# Frontend starten (Option B: Next.js)
npm install
npm run dev
```

**Zugriff:**
- Backend API: http://localhost:8000/docs
- Streamlit UI: http://localhost:8501
- Next.js UI: http://localhost:3000

---

## 🏗️ Architektur

```
┌─────────────────────────────────────────────────┐
│           Frontend (Next.js / Streamlit)         │
│  💬 Chat │ 📄 Contracts │ ⚖️ Disputes │          │
└──────────────────┬──────────────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────────────┐
│           Backend (FastAPI + Python)             │
│  ┌─────────────────────────────────────────┐    │
│  │   RAG Engine (Gemini 1.5 Pro)           │    │
│  │   • Query Embedding                      │    │
│  │   • Jurisdiction Filtering               │    │
│  │   • Cultural Bridge Prompts              │    │
│  └────────────┬────────────────────────────┘    │
└───────────────┼─────────────────────────────────┘
                │
     ┌──────────┴──────────┐
     │                     │
┌────▼─────┐      ┌────────▼────────┐
│  Qdrant  │      │  Redis Cache     │
│ Vector DB│      │  (Optional)      │
└──────────┘      └─────────────────┘
```

### Tech Stack

**Frontend:**
- Next.js 14 (App Router, TypeScript, Tailwind CSS)
- Streamlit (MVP/Prototyping)
- Firebase Hosting & Auth

**Backend:**
- FastAPI (Async Python)
- Google Gemini 1.5 Pro (LLM + Embeddings)
- Qdrant (Vektordatenbank)
- Redis (Caching)
- PyMuPDF (PDF-Analyse)

**Data Sources:**
- 🇩🇪 rechtsprechung-im-internet.de (XML RSS)
- 🇺🇸 CourtListener API + Florida Statutes
- 🇪🇸 BOE.es (Ley de Arrendamientos Urbanos)

---

## 📖 Nutzung

### 1. Rechtsabfrage (Chat)

```bash
# API Request
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Was sind meine Rechte als Mieter in Florida?",
    "target_jurisdiction": "US",
    "user_role": "TENANT",
    "user_language": "de"
  }'
```

**Erwartete Antwort:**
- Erklärt Florida Statutes §83.xx auf Deutsch
- Vergleicht mit deutschen BGB-Konzepten ("Security Deposit" = "Kaution")
- Listet relevante Rechtsprechung

### 2. PDF-Vertragsanalyse

```bash
curl -X POST http://localhost:8000/analyze_contract \
  -F "file=@mietvertrag.pdf" \
  -F "jurisdiction=DE" \
  -F "user_role=TENANT"
```

**Ergebnis:**
- Extrahiert Klauseln (Kündigungsfrist, Kaution, Nebenkostenbeteiligung)
- Vergleicht mit geltendem Recht
- Risikobewertung: 🟢 Konform | 🟡 Potenziell problematisch | 🔴 Rechtswidrig

### 3. Konfliktlösung

```bash
curl -X POST http://localhost:8000/resolve_conflict \
  -H "Content-Type: application/json" \
  -d '{
    "party_a_statement": "Mieter zahlt seit 2 Monaten keine Miete",
    "party_b_statement": "Heizung ist seit 3 Monaten kaputt",
    "jurisdiction": "DE",
    "party_a_label": "Vermieter",
    "party_b_label": "Mieter"
  }'
```

**Analyse:**
- Rechtliche Argumente für beide Seiten
- Erfolgswahrscheinlichkeiten (z.B. Vermieter: 30%, Mieter: 65%, Vergleich: 80%)
- Neutrale Empfehlung mit konkreten Handlungsvorschlägen

---

## 🧪 Testing

```bash
# Backend Tests
cd backend
pytest tests/ -v --cov=. --cov-report=html

# Coverage Report
open htmlcov/index.html
```

**Test-Umfang:**
- ✅ API Endpoints (Validierung, Fehlerbehandlung)
- ✅ Pydantic Models (Datenintegrität)
- ✅ Scraper (Keyword-Extraktion)
- ✅ PDF Parser (Textextraktion)

---

## 🚢 Deployment

### Docker Production

```bash
# Build & Start
docker-compose -f docker-compose.prod.yml up -d

# Services:
# - Backend: http://localhost:8000
# - Qdrant: http://localhost:6333
# - Redis: localhost:6379
# - Nginx: http://localhost (Reverse Proxy)
```

### Firebase Hosting

```bash
# Build Next.js
npm run build

# Deploy
firebase deploy --only hosting
```

### Cloud Run (Backend)

```bash
# Build & Push
docker build -t gcr.io/domulex-ai/backend:latest ./backend
docker push gcr.io/domulex-ai/backend:latest

# Deploy
gcloud run deploy domulex-backend \
  --image gcr.io/domulex-ai/backend:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

---

## 🔧 Konfiguration

### Umgebungsvariablen (`.env`)

```bash
# Essentiell
GEMINI_API_KEY=your_api_key_here

# Optional
ENABLE_CACHE=true           # Redis aktivieren
COURTLISTENER_API_KEY=...   # US Rechtsprechung
SENTRY_DSN=...              # Error Monitoring
```

### Feature Flags

- `ENABLE_PDF_ANALYSIS`: PDF-Upload aktivieren/deaktivieren
- `ENABLE_CONFLICT_RESOLUTION`: Mediation-Modus
- `ENABLE_AUTO_INGESTION`: Automatisches tägliches Scraping

---

## 📊 Performance

- **Query Latency**: ~2-3s (mit Qdrant Cache <1s)
- **Embedding Cache Hit Rate**: ~85% (Redis)
- **Concurrent Users**: 100+ (4 Uvicorn Workers)
- **Vector Search**: <50ms (768-dim Cosine Similarity)

---

## 🛡️ Sicherheit & Compliance

- ✅ **Jurisdiktions-Isolation**: Verhindert Vermischung von DE/ES/US Recht
- ✅ **Firebase Auth**: OAuth 2.0, JWT-Tokens
- ✅ **HTTPS**: TLS 1.3 (Nginx Reverse Proxy)
- ✅ **Rate Limiting**: 60 req/min (pro User)
- ✅ **GDPR-konform**: Keine Speicherung von Nutzerdaten (stateless)

⚠️ **Disclaimer**: DOMULEX ist ein KI-Assistent und ersetzt keine Rechtsberatung. Konsultiere immer einen lizenzierten Anwalt.

---

## 🤝 Contributing

```bash
# 1. Fork & Clone
git clone https://github.com/your-username/domulex.ai.git

# 2. Create Feature Branch
git checkout -b feature/new-jurisdiction

# 3. Make Changes & Test
pytest tests/

# 4. Commit mit konventionellen Commits
git commit -m "feat: Add French jurisdiction support"

# 5. Push & Create PR
git push origin feature/new-jurisdiction
```

**Code Style:**
- Python: `black`, `flake8`
- TypeScript: `eslint`, `prettier`

---

## 📜 Lizenz

MIT License - siehe [LICENSE](LICENSE)

---

## 🙏 Credits

- **Google Gemini 1.5 Pro**: LLM & Embeddings
- **Qdrant**: Vector Database
- **CourtListener**: US Rechtsprechung API
- **rechtsprechung-im-internet.de**: Deutsche Gesetze

---

## 📞 Kontakt

- **Website**: https://domulex-ai.web.app
- **GitHub**: https://github.com/kranichkonstantin-png/domulex.ai
- **E-Mail**: support@domulex.ai

---

**Made with ❤️ for global real estate investors**


### Next.js Frontend (Production)
- `npm run dev` - Start Next.js development server (port 3000)
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Backend
- `uvicorn main:app --reload` - Start FastAPI dev server (port 8000)
- `python seed_data.py` - Load sample legal documents into Qdrant
- `docker-compose up -d` - Start Qdrant + Backend
- `docker-compose down` - Stop all services
- `docker-compose logs -f backend` - View backend logs

### Firebase
- `firebase emulators:start` - Start Firebase emulators locally
- `firebase deploy --only hosting` - Deploy frontend to Firebase Hosting
- `firebase deploy --only functions` - Deploy Cloud Functions

## 🔧 Key Features

### The "Cultural Bridge"

Domulex translates legal concepts across jurisdictions:

**Example Query:**
```
User: "Was ist der Unterschied zwischen Security Deposit in Florida und Kaution in Deutschland?"
Language: German
Target Jurisdiction: US
```

**Response:**
- Retrieves ONLY US law (strict Qdrant filtering)
- Explains in German
- Compares: "Security Deposit" (FL: 1-2 months, no interest) vs "Kaution" (DE: max 3 months, §551 BGB)
- Warns: "Florida law differs from New York!"

### Jurisdiction-Specific Scrapers

- **GermanScraper**: gesetze-im-internet.de, BGB, BFH
- **SpanishScraper**: BOE.es, LAU, Código Civil
- **USScraper**: CourtListener, State Statutes (FL/NY/CA)

## 📡 API Endpoints

Base URL: `http://localhost:8000`

### `POST /query`
Query legal documents with RAG.

**Request:**
```json
{
  "query": "What are my rights as a tenant in Florida?",
  "target_jurisdiction": "US",
  "user_role": "TENANT",
  "user_language": "en",
  "sub_jurisdiction": "Florida"
}
```

**Response:**
```json
{
  "answer": "In Florida, tenants have the following rights...",
  "sources": [
    {
      "title": "Florida Statutes § 83.51",
      "jurisdiction": "US",
      "publication_date": "2024-01-01",
      "source_url": "https://..."
    }
  ],
  "jurisdiction_warning": null
}
```

### Other Endpoints
- `GET /health` - Health check
- `GET /jurisdictions` - List supported jurisdictions
- `POST /ingest/run` - Trigger data ingestion (admin)

## 🔐 Firebase Setup

### Get Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/project/domulex-ai)
2. Navigate to Project Settings > General
3. Under "Your apps", the web app is already created
4. Credentials are already in `.env.local`

### Deploy to Firebase

```bash
# Build the Next.js app
npm run build

# Deploy to Firebase Hosting
firebase deploy --only hosting

# Deploy Cloud Functions (if any)
firebase deploy --only functions
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild backend after code changes
docker-compose up -d --build backend

# Access Qdrant UI
open http://localhost:6333/dashboard
```

## 🧪 Testing

### Full System Test

```bash
# 1. Start all services
docker-compose up -d

# 2. Seed data
python seed_data.py

# 3. Start Streamlit UI
streamlit run frontend_app.py

# 4. Open browser at http://localhost:8501
```

**Test Scenario - Cultural Bridge:**
1. In Streamlit sidebar:
   - Role: Tenant
   - Country: 🇺🇸 United States
   - Region: Florida
   - Language: 🇩🇪 Deutsch
2. Ask: "Was ist der Unterschied zwischen Security Deposit in Florida und Kaution in Deutschland?"
3. Expected: Answer in German explaining US law with comparison to German concepts

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# List jurisdictions
curl http://localhost:8000/jurisdictions

# Query example
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the security deposit limit in Florida?",
    "target_jurisdiction": "US",
    "user_role": "TENANT",
    "user_language": "en",
    "sub_jurisdiction": "Florida"
  }'
```

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Firebase Documentation](https://firebase.google.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Google Gemini API](https://ai.google.dev/)
