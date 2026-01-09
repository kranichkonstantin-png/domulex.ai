# 🚀 DOMULEX Deep Adaptive UI - Quick Start

## Was ist neu?

DOMULEX hat jetzt **4 komplett verschiedene Interfaces** je nach Benutzerrolle:

```
👤 TENANT    →  🛡️ Guardian (WhatsApp-Style)
💼 INVESTOR  →  💼 Deal Room (Dashboard)
⚙️ MANAGER   →  ⚙️ Cockpit (Forms & Tools)
⚖️ LAWYER    →  ⚖️ Workbench (Split-Screen)
```

---

## ⚡ Sofort starten (Offline Demo)

```bash
# 1. Navigate to project
cd /Users/konstantinkranich/domulex.ai

# 2. Run Streamlit (Mock Mode ist bereits aktiviert!)
streamlit run frontend_app.py

# 3. Browser öffnet automatisch auf http://localhost:8501
```

**Keine Backend-Installation erforderlich!** Mock Mode ist standardmäßig aktiviert.

---

## 🎮 Die 4 UIs testen

### 1. TENANT UI (Guardian) 🛡️

**So testen:**
1. Sidebar → Role: "👤 Tenant (Mieter)" wählen
2. Klick auf **[💧 Mold/Schimmel]** Button
3. Sofort Antwort zu Mieterrechten erhalten
4. Klick auf **[📜 Eviction]** oder **[💰 Rent]** für andere Themen
5. Oder eigene Frage in Chat eingeben

**Was Sie sehen sollten:**
- Große SOS-Buttons oben
- WhatsApp-ähnlicher Chat
- Quellen in Expander versteckt
- Einfache Sprache

---

### 2. INVESTOR UI (Deal Room) 💼

**So testen:**
1. Sidebar → Role: "💼 Investor" wählen
2. Klick auf **PDF Upload** → Beliebige PDF hochladen
3. Klick auf **[🔍 Analyze Investment]**
4. Metriken erscheinen:
   - ⚖️ Legal Risk: 45%
   - 💰 Tax Impact: 78%
   - 💧 Liquidity: 82%
   - 📈 ROI: 6.2%
5. Red Flag Reports expandieren

**Was Sie sehen sollten:**
- 2-Spalten Layout (Input | Analysis)
- 4 Risk Meters mit Deltas
- Status-Boxen mit Empfehlungen
- Professionelles Dashboard-Design

---

### 3. MANAGER UI (Cockpit) ⚙️

**So testen:**
1. Sidebar → Role: "⚙️ Property Manager" wählen
2. Tab: **"📝 Document Generator"**
3. Document Type: "Rent Increase Notice" wählen
4. Formular ausfüllen:
   - Current Rent: 1000 €
   - New Rent: 1100 €
   - Legal Basis: "Comparison Rent (Mietspiegel)"
   - Tenant Name: "Max Mustermann"
5. Klick auf **[🚀 Generate Document]**
6. Rechtssicheres Dokument erscheint
7. Klick auf **[📥 Download as TXT]**

**Was Sie sehen sollten:**
- 3 Tabs (Generator, Assistant, Portfolio)
- Formular mit Dropdown & Inputs
- Generiertes Dokument mit BGB-Referenzen
- Download-Button

---

### 4. LAWYER UI (Workbench) ⚖️

**So testen:**
1. Sidebar → Role: "⚖️ Lawyer (Anwalt)" wählen
2. Im **linken Editor** tippen:
   ```
   Der Mieter ist gemäß BGB §535 verpflichtet,
   Schönheitsreparaturen durchzuführen.
   ```
3. Text markieren & kopieren
4. Im **rechten Panel** → Tab "🔍 Research"
5. Text in "Text to research" einfügen
6. Klick auf **[🔍 Analyze]**
7. Zitate erscheinen (BGH-Urteile etc.)
8. Selben Text in **"⚠️ Devil's Advocate"** Tab einfügen
9. Klick auf **[⚔️ Attack]**
10. Kritik in roter Box lesen

**Was Sie sehen sollten:**
- 2-Spalten Layout (Editor 60% | Counsel 40%)
- 600px großer Text-Editor
- 3 Tabs: Research, Devil's Advocate, Precedents
- Wort-/Zeichenzähler
- Präzise Zitate mit Court & Date

---

## 🔄 Zwischen Rollen wechseln

**Live-Demo:**
1. Starte als "Tenant" → Siehst Guardian-UI
2. Sidebar → Role: "Investor" wählen
3. **Komplette UI ändert sich sofort!**
4. Wechsel zu "Manager" → Wieder komplett andere UI
5. Wechsel zu "Lawyer" → Split-Screen erscheint

**Jede Rolle = Komplett neues Interface!**

---

## 🔧 Mit Backend verbinden (Optional)

Wenn Sie mit echten Daten testen wollen:

```python
# 1. In frontend_app.py ändern (Zeile ~21):
MOCK_MODE = False  # ← Von True zu False

# 2. Backend starten:
cd backend
source venv/bin/activate
uvicorn main:app --reload

# 3. Frontend neu starten:
streamlit run frontend_app.py
```

Dann werden echte RAG-Queries an Qdrant gesendet.

---

## 📁 Wichtige Dateien

| Datei | Beschreibung |
|-------|--------------|
| `frontend_app.py` | Neue Deep Adaptive UI (aktiv) |
| `frontend_app_old.py` | Original-Version (Backup) |
| `DEEP_ADAPTIVE_UI.md` | Vollständige Dokumentation |
| `QUICK_START.md` | Diese Datei |

---

## 🎯 Was zu beachten ist

### Session State
Jede UI speichert eigene Daten:
- **Tenant:** `st.session_state.messages`
- **Investor:** `st.session_state.investor_metrics`
- **Manager:** `st.session_state.generated_document`
- **Lawyer:** `st.session_state.lawyer_draft`

**Reset-Button** in Sidebar löscht alles.

### Mock Mode
Aktuell aktiv (MOCK_MODE = True):
- Keine Backend-Verbindung nötig
- Simulierte Antworten
- 1 Sekunde künstliche Verzögerung
- Mock-Daten in MOCK_RESPONSES definiert

### Jurisdictions
Funktioniert mit allen 3:
- 🇩🇪 Germany
- 🇺🇸 United States
- 🇪🇸 Spain

Wechsel in Sidebar ändert Rechtsgrundlagen.

---

## ❓ Troubleshooting

### "streamlit: command not found"
```bash
pip install streamlit
# oder
pip3 install streamlit
```

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests
```

### UI lädt nicht / Fehler im Terminal
```bash
# Syntax prüfen:
python3 -m py_compile frontend_app.py

# Sollte keine Ausgabe geben (= OK)
```

### Wechsel zwischen Rollen funktioniert nicht
- Browser-Cache löschen (Cmd+Shift+R)
- Streamlit neu starten

### Mock-Antworten nicht relevant
Normal! Mock-Daten sind Platzhalter. Für echte Antworten:
```python
MOCK_MODE = False  # In frontend_app.py
```

---

## 🎉 Features im Überblick

| Feature | Tenant | Investor | Manager | Lawyer |
|---------|--------|----------|---------|--------|
| **SOS Buttons** | ✅ | ❌ | ❌ | ❌ |
| **Risk Meters** | ❌ | ✅ | ❌ | ❌ |
| **Doc Generator** | ❌ | ❌ | ✅ | ❌ |
| **Split-Screen** | ❌ | ❌ | ❌ | ✅ |
| **Chat** | ✅ | ✅ | ✅ | ❌ |
| **PDF Upload** | ❌ | ✅ | ❌ | ❌ |
| **Forms** | ❌ | ❌ | ✅ | ❌ |
| **Devil's Advocate** | ❌ | ❌ | ❌ | ✅ |

---

## 📸 Screenshots (Beschreibung)

### Tenant UI
```
┌────────────────────────────────────┐
│ 🛡️ DOMULEX Guardian                │
│ Your Tenant Rights Assistant       │
├────────────────────────────────────┤
│ ⚡ Quick Help                       │
│ [💧 Mold] [📜 Eviction] [💰 Rent] │
├────────────────────────────────────┤
│ 💬 Chat with Guardian              │
│ User: "I have mold in bathroom"    │
│ Bot: "Your rights..."              │
│     📚 Legal Sources (expand)      │
└────────────────────────────────────┘
```

### Investor UI
```
┌───────────────────┬────────────────────┐
│ INPUT             │ ANALYSIS           │
├───────────────────┼────────────────────┤
│ 📄 Upload PDF     │ ⚖️ Legal Risk 45%  │
│ [Choose File]     │ 💰 Tax Impact 78%  │
│                   │ 💧 Liquidity 82%   │
│ 💬 Quick Query    │ 📈 ROI 6.2%        │
│ [Ask...]          │                    │
│                   │ 🚩 Red Flags       │
│                   │ ⚠️ High Tax Burden │
└───────────────────┴────────────────────┘
```

### Manager UI
```
┌────────────────────────────────────┐
│ ⚙️ DOMULEX Cockpit                 │
│ [📝 Generator] [💬 Assistant]      │
├────────────────────────────────────┤
│ Document Type: Rent Increase ▼     │
│ Current Rent: 1000 €               │
│ New Rent: 1100 €                   │
│ Reason: Mietspiegel ▼              │
│ [🚀 Generate Document]             │
├────────────────────────────────────┤
│ MIETERHÖHUNGSERKLÄRUNG             │
│ gemäß § 558 BGB...                 │
│ [📥 Download]                      │
└────────────────────────────────────┘
```

### Lawyer UI
```
┌──────────────────────┬─────────────────┐
│ 📝 Editor            │ 🧠 AI Counsel   │
├──────────────────────┼─────────────────┤
│ [600px Text Area]    │ [Research]      │
│ Der Mieter ist...    │ [Devil's Adv.]  │
│                      │ [Precedents]    │
│                      │                 │
│                      │ Text to analyze │
│                      │ [Paste here...] │
│ 1,234 words          │ [🔍 Analyze]    │
└──────────────────────┴─────────────────┘
```

---

## ✅ Checkliste für erste Demo

- [ ] `streamlit run frontend_app.py` startet ohne Fehler
- [ ] Tenant UI: SOS Button "Mold" funktioniert
- [ ] Investor UI: Upload + Analyze zeigt Metriken
- [ ] Manager UI: Document Generator erstellt Text
- [ ] Lawyer UI: Research Tab findet Quellen
- [ ] Sidebar: Role-Wechsel ändert komplette UI
- [ ] Mock Mode: Funktioniert ohne Backend
- [ ] Reset Button: Löscht alle Session-Daten

---

**🎉 Viel Erfolg mit der neuen Deep Adaptive UI!**

Bei Fragen: Siehe `DEEP_ADAPTIVE_UI.md` für Details.

---

**Stand:** 27. Dezember 2024  
**Version:** 1.0 (Deep Adaptive Interface)  
**Author:** GitHub Copilot (Claude Sonnet 4.5)
