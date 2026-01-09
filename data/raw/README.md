# DOMULEX Sample Legal Documents

This directory contains sample legal texts for testing the multi-jurisdiction RAG system.

## Files

### 1. `sample_de.txt` - German Civil Code (BGB)
**Jurisdiction:** Germany (DE)  
**Language:** German (de)  
**Content:** Excerpts from BGB relating to rental law (Mietrecht):
- § 535: Content and main obligations of rental contract
- § 536: Rent reduction for defects
- § 543: Termination for important reasons
- § 551: Security deposit limits (max 3 months)
- § 573: Ordinary termination by landlord

**Key Concepts:**
- "Kaution" (security deposit): Max 3 months
- "Mietminderung" (rent reduction)
- "Eigenbedarf" (owner's own use as termination reason)

---

### 2. `sample_us.txt` - Florida Statutes Chapter 83
**Jurisdiction:** United States (US)  
**Sub-jurisdiction:** Florida  
**Language:** English (en)  
**Content:** Florida Landlord-Tenant Law:
- 83.43: Landlord's maintenance obligations
- 83.49: Security deposit requirements (no interest requirement in FL!)
- 83.56: Termination notice periods
- 83.60: Defenses to eviction
- 83.63: Casualty damage

**Key Concepts:**
- "Security Deposit": No mandatory interest in Florida (unlike NY)
- Notice periods: 15 days for month-to-month
- Landlord must maintain premises in safe condition

---

### 3. `sample_es.txt` - Ley de Arrendamientos Urbanos (LAU)
**Jurisdiction:** Spain (ES)  
**Language:** Spanish (es)  
**Content:** Spanish Urban Rental Law (LAU 29/1994):
- Artículo 5: Fianza (security deposit) - 1 month
- Artículo 9: Contract duration (min 5 years for natural persons, 7 for companies)
- Artículo 10: Tenant's right to terminate (after 6 months)
- Artículo 19: Maintenance and repairs
- Artículo 27: Landlord's grounds for termination

**Key Concepts:**
- "Fianza": 1 month (vs. 3 in Germany!)
- Minimum contract: 5 years (auto-renewal)
- Tenant can exit after 6 months with 30 days notice

---

## Testing Multi-Jurisdiction Filtering

These files demonstrate the CRITICAL feature of DOMULEX:

**Scenario 1: German user asks about US law**
```bash
python seed_data.py  # Load all 3 files into Qdrant

# Query in German about US law
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Was ist der Unterschied zwischen Security Deposit in Florida und Kaution?",
    "target_jurisdiction": "US",
    "user_role": "TENANT",
    "user_language": "de"
  }'
```

**Expected Result:**
- Retrieves ONLY `sample_us.txt` (strict Qdrant filter: jurisdiction=US)
- Explains in German
- Compares: "Security Deposit (FL: no interest) vs. Kaution (DE: max 3 months, §551 BGB)"

**Scenario 2: Spanish comparison**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Cuál es la diferencia entre la fianza en España y Alemania?",
    "target_jurisdiction": "ES",
    "user_role": "TENANT",
    "user_language": "es"
  }'
```

**Expected Result:**
- Retrieves ONLY `sample_es.txt`
- Explains: "Fianza en España: 1 mes (Art. 5 LAU) vs. Alemania: hasta 3 meses (§551 BGB)"

---

## Seeding Instructions

```bash
# 1. Ensure Qdrant is running
docker-compose up -d qdrant

# 2. Set up environment
cp .env.example .env
# Edit .env and add GOOGLE_API_KEY

# 3. Run seeding script
python seed_data.py
```

**Output:**
```
📄 Processing: sample_de.txt
   Jurisdiction: DE
   Language: de
   Chunks created: 4
   ✅ Uploaded 4 chunks

📄 Processing: sample_us.txt
   Jurisdiction: US
   Language: en
   Chunks created: 5
   ✅ Uploaded 5 chunks

📄 Processing: sample_es.txt
   Jurisdiction: ES
   Language: es
   Chunks created: 5
   ✅ Uploaded 5 chunks

Total: 14 chunks uploaded
```

---

## Verification

```bash
# Check Qdrant collection
curl http://localhost:6333/collections/domulex_legal_docs

# Search by jurisdiction (should return only German chunks)
curl -X POST http://localhost:6333/collections/domulex_legal_docs/points/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],  # Dummy vector
    "filter": {
      "must": [
        {"key": "jurisdiction", "match": {"value": "DE"}}
      ]
    },
    "limit": 5
  }'
```
