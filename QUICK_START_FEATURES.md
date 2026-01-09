# 🚀 Quick Start - Neue Features nutzen

## 1. Document Upload (ALLE Nutzer)

### Im Chat verwenden:
1. Gehe zu https://domulex-ai.web.app/app
2. Scrolle zum Chat-Eingabefeld
3. Klicke auf "Dokument hochladen" oder drag & drop
4. Wähle PDF, DOCX, TXT, JPG oder PNG
5. Warte auf Upload (zeigt Vorschau)
6. Stelle deine Frage - KI nutzt Dokument als Kontext!

**Beispiel:**
```
📎 Mietvertrag.pdf hochgeladen
💬 "Ist die Kündigungsfrist in meinem Vertrag korrekt?"
→ KI analysiert das hochgeladene Dokument
```

## 2. Schriftsatzgenerator (Lawyer Pro)

### Dokument erstellen:
1. Gehe zu `/app/documents/generate`
2. Wähle Vorlage (z.B. "Klage Mietrecht")
3. **Optional:** Lade Kontext-Dokumente hoch
4. Fülle Felder aus:
   - Manuell eingeben ODER
   - Klicke "✨ KI-Assistent" für Auto-Completion
5. Klicke "Dokument generieren"
6. Bearbeite im Editor
7. Export als DOCX oder PDF

**Tipp:** KI-Assistent funktioniert am besten mit hochgeladenen Dokumenten!

## 3. Erweiterte Rechtsprechung

### Neue Quellen durchsuchen:
- EuGH-Urteile jetzt verfügbar (nach Seeding)
- 350+ neue AG-Urteile (Mietrecht, WEG, Baurecht)
- Vollständige Abdeckung: EuGH → BGH → OLG → LG → AG

**Suche:**
```
"EuGH Niederlassungsfreiheit Immobilie"
"AG Mietminderung Schimmel"
"Grunderwerbsteuer Ausländer EuGH"
```

## 4. Admin: Datenbank erweitern

### Seeding ausführen:

1. **API Keys setzen** in `/backend/.env`:
```bash
GEMINI_API_KEY=your_gemini_key
QDRANT_API_KEY=your_qdrant_key
QDRANT_HOST=your_cluster.gcp.cloud.qdrant.io
```

2. **Scraper testen:**
```bash
cd /Users/konstantinkranich/domulex.ai
python3 test_scrapers.py
```

3. **Volles Seeding:**
```bash
python3 seed_comprehensive_case_law.py
```

**Dauer:** ~30-45 Minuten für 350 Urteile (Embedding-Generierung)

**Ergebnis:** 1,286 → 1,636 Dokumente in Qdrant

## 5. Testing

### Upload testen:
```bash
# Curl test (wenn Backend deployed)
curl -X POST https://domulex-backend-xxx.run.app/upload/document \
  -F "file=@test.pdf" \
  -F "user_id=test123" \
  -F "session_id=session456"
```

### Templates testen:
```bash
curl https://domulex-backend-xxx.run.app/templates
```

### Generierung testen:
```bash
curl -X POST https://domulex-backend-xxx.run.app/documents/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "klage_mietrecht",
    "field_values": {
      "gericht": "Amtsgericht Berlin-Mitte",
      "klaeger_name": "Max Mustermann"
    }
  }'
```

## 📊 Feature-Matrix

| Feature | Basis | Professional | Lawyer Pro |
|---------|-------|--------------|------------|
| Upload PDF/DOCX | ✅ (3 max) | ✅ (5 max) | ✅ (10 max) |
| Upload JPG/PNG + OCR | ✅ (3 max) | ✅ (5 max) | ✅ (10 max) |
| Chat mit Dokumenten | ✅ | ✅ | ✅ |
| Schriftsatzgenerator | ❌ | ❌ | ✅ |
| KI-Feldgenerierung | ❌ | ❌ | ✅ |
| DOCX/PDF Export | ❌ | ❌ | ✅ |
| Quellenfilter | ❌ | ❌ | ✅ |

## 🐛 Troubleshooting

**Upload funktioniert nicht:**
- Prüfe Dateigröße (max 10MB)
- Prüfe Format (PDF, DOCX, TXT, JPG, PNG)
- Prüfe Browser Console für Fehler

**KI-Assistent generiert nichts:**
- Mindestens 1 Dokument hochladen
- Warte auf Upload-Completion
- Prüfe Backend-Logs

**Seeding schlägt fehl:**
- `GEMINI_API_KEY` in .env gesetzt?
- `QDRANT_API_KEY` korrekt?
- Qdrant Cluster erreichbar?

## 📚 Weitere Infos

- **Implementation:** `IMPLEMENTATION_COMPLETE.md`
- **Scraper Test:** `python3 test_scrapers.py`
- **Seeding Log:** `seeding_log.txt` (nach Ausführung)
