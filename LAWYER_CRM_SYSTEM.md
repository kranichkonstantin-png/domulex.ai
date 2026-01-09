# Lawyer CRM & Document Management System

## 🎯 Überblick

Das **domulex.ai Lawyer Pro** System bietet Anwälten eine vollständige Praxisverwaltung mit KI-Integration:

1. **Mandantenverwaltung (CRM)** - Clients & Mandates verwalten
2. **Dokumentenmanagement** - Intelligente Akten-Organisation
3. **KI-Integration** - Smart insights, Suche & Analysen

---

## 🏛️ Architektur

### Backend
- **Models**: `/backend/models/crm.py`
- **Service**: `/backend/services/crm_service.py`
- **API Endpoints**: `/backend/main.py` (CRM-Sektion)

### Datenbank
- **Firestore Collections**:
  - `clients` - Mandanten
  - `mandates` - Mandate/Fälle
  - `documents` - Dokumente

### Storage
- **Firebase Storage**: PDF-Uploads, Dokumente

---

## 📋 Features

### 1. Mandantenverwaltung (CRM)

#### Client Management
```json
{
  "client_id": "uuid",
  "lawyer_id": "firebase_uid",
  "first_name": "Max",
  "last_name": "Mustermann",
  "email": "max@example.com",
  "phone": "+49 123 456789",
  "company_name": "Musterfirma GmbH",
  "address_street": "Musterstraße 1",
  "address_city": "Berlin",
  "address_zip": "10115",
  "status": "ACTIVE | INACTIVE | ARCHIVED | PROSPECT",
  "tags": ["Mietrecht", "Stammkunde"],
  "notes": "Wichtige Notizen...",
  "ai_summary": "KI-generierte Zusammenfassung",
  "risk_assessment": "KI-Risikobewertung",
  "client_since": "2024-01-01T00:00:00Z"
}
```

**Endpoints:**
- `POST /crm/clients` - Neuen Mandanten anlegen
- `GET /crm/clients` - Alle Mandanten auflisten
- `GET /crm/clients/{id}` - Mandant abrufen
- `PUT /crm/clients/{id}` - Mandant aktualisieren
- `DELETE /crm/clients/{id}` - Mandant archivieren

#### Mandate Management
```json
{
  "mandate_id": "uuid",
  "lawyer_id": "firebase_uid",
  "client_id": "uuid",
  "title": "Mietminderung wegen Schimmel",
  "mandate_type": "MIETRECHT | KAUFRECHT | WEG | BAURECHT | PROZESSFUEHRUNG | BERATUNG",
  "status": "NEW | IN_PROGRESS | WAITING | COMPLETED | CLOSED",
  "summary": "Mandant hat Schimmel in der Wohnung...",
  "case_number": "123 C 456/24",
  "opposing_party": "Vermieterin Müller",
  "start_date": "2024-01-01",
  "expected_end_date": "2024-06-30",
  "deadlines": [
    {
      "title": "Klagefrist",
      "due_date": "2024-02-15",
      "priority": "URGENT",
      "completed": false,
      "notes": "Unbedingt einhalten!"
    }
  ],
  "hourly_rate": 250.00,
  "estimated_hours": 20,
  "total_billed": 5000.00,
  "tags": ["Mietrecht", "Schimmel"],
  "priority": "HIGH",
  "ai_strategy": "KI-generierte Strategie...",
  "ai_risk_assessment": "KI-Risikobewertung...",
  "success_probability": 0.75
}
```

**Endpoints:**
- `POST /crm/mandates` - Neues Mandat anlegen
- `GET /crm/mandates` - Alle Mandate auflisten (Filter: client_id, status)
- `GET /crm/mandates/{id}` - Mandat abrufen
- `PUT /crm/mandates/{id}` - Mandat aktualisieren
- `POST /crm/mandates/deadlines` - Frist hinzufügen
- `GET /crm/deadlines/upcoming?days_ahead=30` - Kommende Fristen

---

### 2. Dokumentenmanagement

#### Document Model
```json
{
  "document_id": "uuid",
  "lawyer_id": "firebase_uid",
  "client_id": "uuid",
  "mandate_id": "uuid",
  "filename": "mietvertrag.pdf",
  "original_filename": "Mietvertrag_Max_Mustermann.pdf",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "storage_path": "lawyers/{lawyer_id}/documents/{doc_id}.pdf",
  "category": "CONTRACT | CORRESPONDENCE | COURT_FILING | EVIDENCE | INVOICE | NOTE | TEMPLATE",
  "tags": ["Mietvertrag", "2024"],
  "title": "Mietvertrag Mustermann",
  "description": "Hauptmietvertrag",
  "ai_summary": "KI-Zusammenfassung des Dokuments",
  "ai_key_points": ["Kaltmiete 800€", "Kaution 2400€"],
  "ai_legal_issues": ["Schönheitsreparaturklausel unwirksam"],
  "ai_risks": ["Fristlose Kündigung möglich"],
  "extracted_text": "Volltext...",
  "version": 1,
  "is_latest": true
}
```

**Endpoints:**
- `GET /crm/documents` - Dokumente auflisten (Filter: client_id, mandate_id, category)
- `POST /crm/documents/search` - KI-Suche durch Dokumente
- `POST /crm/chat` - Chat mit Dokumenten-Kontext

---

### 3. KI-Integration

#### A) Mandate Insights
**Automatische Fall-Analyse:**
```bash
POST /crm/mandates/{mandate_id}/insights
```

**Generiert:**
- ✅ **Rechtsstrategie** - Empfohlenes Vorgehen
- ✅ **Risikobewertung** - Mögliche Probleme
- ✅ **Erfolgswahrscheinlichkeit** - AI-Schätzung (0-1)
- ✅ **Ähnliche Fälle** - IDs vergleichbarer Mandate

**Beispiel-Response:**
```json
{
  "mandate_id": "uuid",
  "strategy": "1. Mängelanzeige mit Fristsetzung (14 Tage)\n2. Bei Nichterfolg: Mietminderung 20%\n3. Parallel Selbstvornahme androhen...",
  "risk_assessment": "Hauptrisiko: Beweislast für Schimmelursache. Empfehlung: Sachverständigengutachten einholen...",
  "success_probability": 0.78,
  "key_considerations": [
    "Frist für Mängelbeseitigung setzen",
    "Fotodokumentation sichern",
    "Sachverständigen beauftragen"
  ],
  "recommended_actions": [
    "Schriftliche Mängelanzeige versenden",
    "Frist 14 Tage setzen",
    "Mietminderung ab Zugang ankündigen"
  ]
}
```

#### B) Document Search AI
**Semantische Suche:**
```bash
POST /crm/documents/search
{
  "query": "Alle Verträge mit Schönheitsreparaturklauseln",
  "mandate_id": "optional",
  "category": "optional",
  "limit": 10
}
```

**Response:**
```json
[
  {
    "document": { ... },
    "relevance_score": 0.92,
    "matching_excerpt": "§ 5 Schönheitsreparaturen...",
    "ai_explanation": "Dokument enthält umfassende Schönheitsreparaturklausel in § 5..."
  }
]
```

#### C) Chat with Documents
**Kontextbasierter Chat:**
```bash
POST /crm/chat
{
  "query": "Welche Fristen muss ich bei diesem Fall beachten?",
  "mandate_id": "uuid",
  "document_ids": ["doc1", "doc2"],
  "client_id": "uuid"
}
```

**Response:**
```json
{
  "answer": "Bei diesem Mandat sind folgende Fristen relevant:\n1. Fristsetzung Mängelbeseitigung: 14 Tage (bereits gesetzt)\n2. Klagefrist: 15.02.2024 (siehe Deadline)\n3. Verjährungsfrist: 31.12.2027...",
  "sources_used": [
    "Mandat: Mietminderung wegen Schimmel",
    "mietvertrag.pdf",
    "Mandant: Max Mustermann"
  ],
  "confidence": 0.85,
  "follow_up_questions": [
    "Welche rechtlichen Schritte sind als nächstes zu empfehlen?",
    "Gibt es ähnliche Präzedenzfälle?",
    "Welche Fristen sind zu beachten?"
  ]
}
```

---

## 🔐 Sicherheit & Zugriff

### Tier-Beschränkung
- ✅ **Alle CRM-Features**: Nur Lawyer Pro (49€/Monat)
- ❌ Free, Mieter Plus, Professional: Kein Zugriff (403 Error)

### Datensicherheit
- Jeder Anwalt sieht nur **eigene** Mandanten/Mandate/Dokumente
- `lawyer_id` Check bei allen Abfragen
- Firebase Security Rules für Firestore
- Firebase Storage Rules für Dokumente

---

## 💡 KI-Funktionen im Detail

### 1. Client Summary (Auto)
Bei Anlage eines Mandanten mit Notizen:
```
Input: "Herr Müller hat Probleme mit Vermieter. Schimmel in Wohnung seit 6 Monaten."

KI generiert:
"Mietrechtlicher Mandat. Mandant meldet langanhaltenden Schimmelproblem. Vermieterpflicht zur Mängelbeseitigung verletzt. Prüfung Mietminderung und Schadensersatz empfohlen."
```

### 2. Mandate Strategy (On-Demand)
Bei Anforderung von Insights:
```
Input: Mandat-Details + Dokumente

KI generiert:
1. Rechtliche Einordnung (BGB §§)
2. Empfohlenes Vorgehen (Step-by-Step)
3. Wichtige Punkte zu beachten
4. Mögliche Fallstricke
```

### 3. Document Auto-Categorization
Bei Upload (zukünftig):
```
PDF-Analyse → KI erkennt:
- "Mietvertrag" → Category: CONTRACT
- "Schreiben an Gericht" → Category: COURT_FILING
- "Rechnung 12/2024" → Category: INVOICE
```

### 4. Smart Deadlines
KI scannt Dokumente nach Fristen:
```
"Die Frist zur Klageerhebung endet am 15.02.2024"
→ Auto-Deadline: {title: "Klagefrist", due_date: "2024-02-15", priority: "URGENT"}
```

---

## 📊 Anwendungsfälle

### Use Case 1: Neuer Mandant
1. Anwalt legt Mandant an: `POST /crm/clients`
2. KI generiert Summary aus Notizen
3. Anwalt erstellt Mandat: `POST /crm/mandates`
4. KI generiert Strategie: `POST /crm/mandates/{id}/insights`
5. Dokumente hochladen (PDFs)
6. KI analysiert & kategorisiert automatisch

### Use Case 2: Fristenverwaltung
1. Anwalt fügt Deadline hinzu: `POST /crm/mandates/deadlines`
2. Dashboard zeigt: `GET /crm/deadlines/upcoming?days_ahead=7`
3. KI-Email-Reminder (zukünftig): "Klagefrist in 3 Tagen!"

### Use Case 3: Akten durchsuchen
1. Anwalt: "Wo ist die Schönheitsreparaturklausel?"
2. `POST /crm/documents/search` mit Query
3. KI rankt alle Dokumente nach Relevanz
4. Top-Match: "mietvertrag.pdf, § 5, Relevanz: 0.95"

### Use Case 4: Fall-Insights
1. Anwalt bereitet Verhandlung vor
2. `POST /crm/chat` mit mandate_id + documents
3. KI analysiert alle relevanten Dokumente
4. Antwort: Strategie, Risiken, Argumente

---

## 🚀 Implementierungsstatus

### ✅ Fertig implementiert
- [x] Client CRUD (Create, Read, Update, Delete)
- [x] Mandate CRUD
- [x] Deadline Management
- [x] Document Listing
- [x] AI Client Summary
- [x] AI Mandate Insights (Strategy, Risk, Success Probability)
- [x] AI Document Search
- [x] AI Chat with Documents Context
- [x] Tier-based Access Control (Lawyer only)
- [x] Security (lawyer_id verification)

### 🔄 In Entwicklung
- [ ] Document Upload Endpoint mit Firebase Storage
- [ ] Automatische PDF-Analyse bei Upload
- [ ] Auto-Categorization
- [ ] Auto-Deadline-Extraction
- [ ] Similar Cases Finder
- [ ] Email-Reminders für Fristen
- [ ] Time Tracking Integration
- [ ] Billing Integration

### 💡 Geplant
- [ ] Calendar Integration
- [ ] Template Library
- [ ] Conflict Checking (Interessenskonflikte)
- [ ] Multi-Lawyer Support (Kanzlei)
- [ ] Client Portal (Mandanten-Zugang)
- [ ] Mobile App

---

## 🔧 Technische Details

### Dependencies
```python
# Neu hinzugefügt:
- firebase-admin (Firestore, Storage)
- google-generativeai (Gemini AI)
- pydantic (Data validation)
- uuid (ID generation)
```

### Firestore Schema

#### Collection: `clients`
```
clients/{client_id}
├── lawyer_id: string
├── first_name: string
├── last_name: string
├── email: string
├── status: string
├── ai_summary: string
└── ...
```

#### Collection: `mandates`
```
mandates/{mandate_id}
├── lawyer_id: string
├── client_id: string (reference to clients/{id})
├── title: string
├── mandate_type: string
├── status: string
├── deadlines: array
│   └── [{ title, due_date, priority, completed }]
├── ai_strategy: string
├── ai_risk_assessment: string
├── success_probability: float
└── ...
```

#### Collection: `documents`
```
documents/{document_id}
├── lawyer_id: string
├── client_id: string (optional)
├── mandate_id: string (optional)
├── filename: string
├── storage_path: string
├── category: string
├── ai_summary: string
├── ai_key_points: array
├── extracted_text: string (full PDF text)
└── ...
```

---

## 📈 Pricing Integration

### Lawyer Pro Features
```typescript
lawyer: {
  price: 49,
  features: [
    '1.000 Anfragen pro Monat',
    'Anwalts-Modus',
    'PDF-Vertragsanalyse',
    'Schriftsatz-Generierung',
    '⭐ Mandantenverwaltung (CRM) mit KI',
    '⭐ Dokumentenmanagement',
    '⭐ KI-Aktenanalyse & Fall-Insights'
  ]
}
```

Das CRM-System rechtfertigt den **49€** Preis deutlich:
- Erspart externe CRM-Software (50-200€/Monat)
- KI-gestützte Analysen (unbezahlbar)
- Vollständig integriert mit Legal-AI
- Zeitsparend durch Automatisierung

---

## 🎓 Best Practices

### 1. Mandanten sauber strukturieren
- Aussagekräftige Tags verwenden
- Notizen pflegen → bessere AI-Summaries
- Status aktuell halten

### 2. Mandate detailliert beschreiben
- Gute Summary schreiben
- Alle Dokumente verknüpfen
- Fristen sofort eintragen

### 3. Dokumente richtig kategorisieren
- Korrekte Category wählen
- Sprechende Titel vergeben
- Tags für schnelle Suche

### 4. KI-Features nutzen
- Regelmäßig Insights generieren
- AI-Suche statt manuellem Durchforsten
- Chat-Funktion für schnelle Antworten

---

## 🔗 API-Beispiele

### Mandant anlegen
```bash
curl -X POST https://domulex-backend.../crm/clients \
  -F "user_id=firebase_uid" \
  -F "user_tier=lawyer" \
  -F "first_name=Max" \
  -F "last_name=Mustermann" \
  -F "email=max@example.com" \
  -F "notes=Mieter mit Schimmelproblem"
```

### Mandate auflisten
```bash
curl -X GET "https://domulex-backend.../crm/mandates?user_id=firebase_uid&user_tier=lawyer&status=IN_PROGRESS"
```

### KI-Insights generieren
```bash
curl -X POST https://domulex-backend.../crm/mandates/abc123/insights \
  -F "user_id=firebase_uid" \
  -F "user_tier=lawyer" \
  -F "include_strategy=true" \
  -F "include_risk_assessment=true" \
  -F "include_success_probability=true"
```

### Mit Akten chatten
```bash
curl -X POST https://domulex-backend.../crm/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "firebase_uid",
    "user_tier": "lawyer",
    "query": "Welche Argumente habe ich gegen die Kündigung?",
    "mandate_id": "abc123",
    "document_ids": ["doc1", "doc2"]
  }'
```

---

## 🎯 Zusammenfassung

Das **domulex.ai Lawyer CRM** bietet Anwälten:

✅ **Vollständiges Praxismanagement** - Clients, Mandates, Deadlines
✅ **Intelligente Akten** - AI-Analyse, Smart Search, Auto-Kategorisierung
✅ **KI-Rechtsassistent** - Strategien, Risiken, Erfolgswahrscheinlichkeiten
✅ **Alles in einem System** - Keine externe Software nötig
✅ **Datenschutz** - Deutsche Server, vollständige Kontrolle

**Für nur 49€/Monat** - deutlich günstiger als separate CRM + DMS + AI-Tools!
