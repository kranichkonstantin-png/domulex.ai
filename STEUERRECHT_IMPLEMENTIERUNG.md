# Steuerrecht-Implementierungsplan für Domulex.ai

## Status: IN ARBEIT 🔄

## 1. Problemanalyse

**Aktueller Stand:**
- ✅ Backend hat bereits Steuerrecht-Inhalte (BFH-Urteile, BMF-Schreiben, AfA, Grundsteuer)
- ❌ Landing Page bewirbt Steuerrecht NICHT
- ❌ Dashboards zeigen keine Steuer-spezifischen Features
- ❌ AGB/Rechtsdokumente erwähnen Steuerrecht nicht explizit
- ❌ Support Bot kennt Steuer-Features nicht

**Warum ist Steuerrecht wichtig?**
- Enormes Attraktivitätspotenzial für Basis & Professional
- Investoren suchen aktiv nach Steueroptimierung
- USP: "Spare 10.000-100.000€ Steuern mit der richtigen AfA-Strategie"

---

## 2. Marketing: Landing Page Erweiterungen

### 2.1 Hero Section - Ergänzung
```
"Mietrecht • Kaufrecht • **Steueroptimierung** • WEG • Baurecht"
```

### 2.2 Vorteile-Section - Neues Feature-Card
```javascript
{
  icon: '💰',
  title: 'Steuer-Optimierung',
  description: 'AfA-Berechnung, Grunderwerbsteuer, Spekulationsfristen, Werbungskosten – fundierte Steuerinfos für Immobilieninvestoren.'
}
```

### 2.3 Zielgruppen-Section - Ergänzung bei Investoren
```javascript
{
  icon: '📈',
  title: 'Investoren & Vermieter',
  description: 'Renditeoptimierung, Steuergestaltung, AfA-Strategien, Mieterhöhung, Vertragsgestaltung',
  highlight: 'Professional'
}
```

### 2.4 Preis-Features - Steuer-Mention
- **Basis:** "Grundlegende Steuer-Infos (AfA, Werbungskosten)"
- **Professional:** "Erweiterte Steuer-Analysen (Spekulationsfrist, Share Deal, Grunderwerbsteuer)"
- **Lawyer Pro:** "Umfassende Steuer-Expertise für Mandanten-Beratung"

### 2.5 FAQ - Neue Frage
```javascript
{
  q: 'Kann domulex.ai bei Steuerfragen helfen?',
  a: 'Ja! Wir haben über 100 BFH-Urteile und BMF-Schreiben zu Immobilien-Steuerrecht. AfA-Berechnung, Spekulationsfristen, Grunderwerbsteuer-Optimierung und mehr. Wichtig: Für verbindliche Steuerberatung wenden Sie sich an einen Steuerberater.'
}
```

### 2.6 Value Proposition Box (NEU)
```jsx
<section className="py-16 px-4 bg-gradient-to-r from-green-50 to-emerald-50">
  <div className="max-w-4xl mx-auto text-center">
    <h2>💰 Steuer-Potenzial für Immobilien-Investoren</h2>
    <div className="grid md:grid-cols-3 gap-6">
      <div>
        <span className="text-3xl font-bold text-green-600">+3.500€/Jahr</span>
        <p>Mehr Abschreibung durch 3% AfA statt 2%</p>
      </div>
      <div>
        <span className="text-3xl font-bold text-green-600">Bis zu 6,5%</span>
        <p>Grunderwerbsteuer sparen durch Share Deal</p>
      </div>
      <div>
        <span className="text-3xl font-bold text-green-600">100% steuerfrei</span>
        <p>Verkauf nach 10 Jahren Haltefrist</p>
      </div>
    </div>
  </div>
</section>
```

---

## 3. Dashboard-Funktionserweiterungen

### 3.1 Steuer-Quick-Actions (für alle Tarife)
- "AfA-Check: Welche Abschreibung gilt für mein Gebäude?"
- "Spekulationsfrist prüfen"
- "Werbungskosten bei Vermietung"

### 3.2 Steuer-Rechner Widgets (Professional)
- AfA-Kalkulator: Gebäudealter → AfA-Satz → Jahresabschreibung
- Spekulationsfristen-Tracker
- Grunderwerbsteuer nach Bundesland

### 3.3 Steuer-Dokumente (Lawyer Pro)
- Mandanten-Steuerinfos exportieren
- Steuer-Checklisten generieren

---

## 4. Support Bot Aktualisierung

### Ergänzung in personas.py:
```python
5. **Steuerrecht** (alle Tarife)
   - AfA-Tabellen (2%, 2.5%, 3% je nach Baujahr)
   - Spekulationsfrist (§ 23 EStG)
   - Werbungskosten (§ 9 EStG)
   - Grunderwerbsteuer (Bundesland-spezifisch)
   - BFH-Urteile zu Immobilien-Besteuerung
```

---

## 5. Rechtsdokumente-Prüfung

### AGB § 2 Leistungsbeschreibung erweitern:
```
- KI-Chat zur Beantwortung von Fragen zum deutschen Immobilienrecht
  **einschließlich Immobilien-Steuerrecht (AfA, Grunderwerbsteuer, Spekulationsfrist)**
```

### Hinweis ergänzen:
```
Die von domulex.ai bereitgestellten Informationen stellen KEINE RECHTS- 
ODER STEUERBERATUNG dar. Für steuerrechtlich verbindliche Auskünfte 
wenden Sie sich an einen Steuerberater.
```

---

## 6. Implementierungs-Reihenfolge

### Phase 1: Marketing (Sofort) ✅
1. Landing Page Feature-Cards ergänzen
2. Zielgruppen-Beschreibung updaten  
3. FAQ Steuer-Frage hinzufügen
4. Preis-Features aktualisieren

### Phase 2: Rechtsdokumente (Sofort)
1. AGB Leistungsbeschreibung erweitern
2. Disclaimer anpassen
3. Support Bot aktualisieren

### Phase 3: Dashboard (Später)
1. Steuer-Quick-Actions
2. AfA-Rechner Widget
3. Spekulationsfristen-Tracker

---

## 7. Content-Basis (bereits vorhanden)

Das Backend hat bereits:
- **19+ BFH-Urteile** zu Immobilien-Steuerrecht
- **8+ BMF-Schreiben** (AfA, Grundsteuer, etc.)
- **Relevante Gesetze:** EStG, GrEStG, GrStG, BewG

Diese Inhalte werden bereits über den RAG-Engine ausgeliefert, aber nicht aktiv beworben!

---

## 8. Erfolgsmetriken

- 📈 Conversion-Rate Basis/Professional erhöhen
- 📈 "Steuer" als Keyword in Anfragen tracken
- 📈 Zielgruppe Investoren besser ansprechen
