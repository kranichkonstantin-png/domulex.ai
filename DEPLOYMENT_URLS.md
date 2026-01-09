# DOMULEX.ai - Deployment URLs

## 🚀 Live Production Deployment

**Frontend (Streamlit):**  
https://domulex-frontend-841507936108.europe-west3.run.app

**Backend API (FastAPI):**  
https://domulex-backend-841507936108.europe-west3.run.app

**API Documentation:**  
https://domulex-backend-841507936108.europe-west3.run.app/docs

**Health Check:**  
https://domulex-backend-841507936108.europe-west3.run.app/health

---

## 🔧 Configuration

### Backend
- **Platform:** Google Cloud Run (europe-west3)
- **AI Model:** Gemini 2.5 Flash
- **API Key:** Configured as environment variable
- **Vector DB:** Qdrant (Optional - graceful degradation)
- **Mode:** Gemini-only (no document retrieval yet)

### Frontend
- **Platform:** Google Cloud Run (europe-west3)
- **Framework:** Streamlit 1.39.0
- **Mode:** Connected to live backend
- **Environment Variables:**
  - `MOCK_MODE=false`
  - `API_BASE_URL=https://domulex-backend-841507936108.europe-west3.run.app`

---

## 📝 Next Steps

### Phase 1: Enable Full RAG
1. Deploy Qdrant vector database
2. Ingest legal documents (DE/US/ES)
3. Enable document retrieval in queries

### Phase 2: Advanced Features
1. PDF upload & analysis
2. Contract comparison
3. Dispute resolution workflow

### Phase 3: Production Hardening
1. Add Firebase Authentication
2. Enable Redis caching
3. Set up monitoring (Sentry)
4. Configure custom domain

---

## 🎯 Current Status

✅ Frontend deployed with subscription system  
✅ Backend deployed with Gemini API  
✅ 4 role-specific UIs working  
✅ Real AI responses (Gemini-only mode)  
✅ All jurisdictions supported (DE/US/ES)  
✅ Subscription & billing UI integrated  
✅ Query quota management active  
⏳ Qdrant Vector DB (requires Cloud setup)  
⚠️ No document retrieval yet (Qdrant pending)

---

## 💡 Usage Example

1. Open https://domulex-frontend-841507936108.europe-west3.run.app
2. Choose role (Tenant/Investor/Manager/Lawyer)
3. Select jurisdiction (Germany/USA/Spain)
4. Ask legal question
5. Get AI-powered answer with disclaimer

**Example Questions:**
- DE: "Was ist eine Eigenbedarfskündigung?"
- US: "What is a security deposit limit in California?"
- ES: "¿Qué es un desahucio por impago?"

---

**Deployed:** 2025-12-27  
**Region:** europe-west3 (Frankfurt)  
**Project:** domulex-ai
