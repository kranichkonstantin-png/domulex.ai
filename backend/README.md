# DOMULEX Backend

Legal-Tech RAG System for Real Estate, Construction, and Tax Law across DE, ES, and US jurisdictions.

## Architecture

```
backend/
├── models/              # Pydantic data models
├── ingestion/           # Legal data scrapers
├── rag/                 # RAG engine & prompts
├── api/                 # FastAPI routes
├── config/              # Settings & environment
└── main.py              # Application entry point
```

## Tech Stack

- **Python:** 3.11+
- **API:** FastAPI (Async)
- **LLM:** Google Gemini 1.5 Pro
- **Vector DB:** Qdrant (Docker)
- **Data Models:** Pydantic V2

## Supported Jurisdictions

1. **Germany (DE):** BGB, BFH, BGH
2. **Spain (ES):** Código Civil, Ley de Arrendamientos Urbanos
3. **USA (US):** Federal + State Law (FL, NY, CA)

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

Create `.env` file:

```env
GEMINI_API_KEY=your_key_here
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=legal_documents
```

## Run

```bash
# Start Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# Start API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /query` - Query legal documents
- `POST /ingest/run` - Trigger data ingestion (Admin)
