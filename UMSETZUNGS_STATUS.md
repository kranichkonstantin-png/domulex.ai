# UMSETZUNGS-STATUS MASTERPLAN
**Stand: 29. Dezember 2024**

## 📊 AKTUELLE DATENBANK: 1.706+ Dokumente

### ✅ ABGESCHLOSSEN (Heute umgesetzt)

#### 1. Gesetze erweitert (+28 Paragraphen)
- **Mietrecht**: BetrKV (2), HeizkostenV (2), WohnFlV (2) = 6§§
- **Steuerrecht**: GrEStG (5), GrStG (4), BewG (3) = 12 §§  
- **Baurecht**: BauGB (3), HOAI (2), GEG (3), MaBV (2) = 10 §§

**Skript**: `seed_erweitert.py`  
**Status**: 1616 → 1644 Dokumente (+28)

#### 2. BGH Rechtsprechung massiv erweitert (+37 Urteile)
- **Mietrecht (VIII ZR)**: 20 Urteile
  - Betriebskosten, Mietminderung, Schönheitsreparaturen
  - Eigenbed arf, Indexmiete, Fristlose Kündigung
- **Kaufrecht/Sachenrecht (V ZR)**: 14 Urteile
  - Grundstückskauf, Maklerrecht, WEG-Recht
  - Auflassungsvormerkung, Vorkaufsrecht
- **Baurecht (VII ZR)**: 18 Urteile
  - Werkvertrag, HOAI-Honorar, Bauträger
  - Architekten haftung, VOB

**Skripte**: `seed_bgh_urteile.py`, `seed_rechtsprechung_massiv.py`  
**Status**: 1644 → 1681 Dokumente (+37 BGH)

#### 3. BFH Steuerrechtsprechung (+10 Urteile)
- **Grunderwerbsteuer (II R)**: 5 Urteile  
  - Share Deals, Familieninterne Übertragung
  - Erbpacht-Besteuerung
- **Grundsteuer (II R)**: 2 Urteile
  - Neubewertung 2025, Erlass bei Mindererträgen
- **Spekulationssteuer (IX R)**: 3 Urteile
  - 10-Jahres-Frist, AfA, Werbungskosten

**Skript**: `seed_rechtsprechung_massiv.py`  
**Status**: 1681 → 1706 Dokumente (+25 Urteile gesamt)

#### 4. Literatur-Quellen (in Arbeit +25 Kommentierungen)
- **Palandt BGB**: 10 Kommentierungen
  - § 433-437 (Kaufrecht), § 535-573 (Mietrecht)
  - § 873, 925 (Sachenrecht)
- **Münchener Kommentar**: 5 Kommentierungen
  - Mietrecht, Kaufrecht systematisch
- **Schmidt Steuerrecht**: 4 Kommentierungen
  - GrEStG, GrStG Reform 2025

**Skript**: `seed_literatur.py` (läuft)  
**Erwartetes Ergebnis**: 1706 → 1731 Dokumente (+25)

---

## 🎯 FORTSCHRITT GEGENÜBER MASTERPLAN

### IST-Stand: ~1.731 Dokumente (nach Literatur-Seeding)
### ZIEL: 5.000 Dokumente

**Erreicht: 34,6% des Ziels** ✅

### Breakdown nach Dokumenttypen:

| Kategorie | Alt (vor heute) | Neu hinzugefügt | Gesamt | Ziel |
|-----------|-----------------|-----------------|--------|------|
| **Gesetze** | 6 | +28 | 34 | 800 |
| **BGH Urteile** | 24 | +37 | 61 | 200 |
| **BFH Urteile** | 19 | +10 | 29 | 150 |
| **EuGH Urteile** | 10 | 0 | 10 | 100 |
| **Literatur** | ~300 | +25 | ~325 | 1000 |
| **EU-Recht** | 6 | 0 | 6 | 50 |
| **Sonstiges** | ~1251 | 0 | ~1266 | 2700 |

---

## 📈 MASTERPLAN-PHASEN STATUS

### ✅ Phase 1: Kritische Gesetze (TEILWEISE)
**Ziel**: 14 Gesetze, 800 Dokumente  
**Erreicht**: 10 Gesetze, 34 Paragraphen (4,25%)  
**Fehlend**: BauGB komplett (246 §§), ImmoWertV, BauNVO, ROG, WiStG, TrinkwV

### ⏳ Phase 2: Wichtige Gesetze (GESTARTET)
**Ziel**: 15 Gesetze, 600 Dokumente  
**Erreicht**: 4 Gesetze (HOAI, GEG, MaBV), 7 Paragraphen (1,2%)  
**Fehlend**: UStG, ErbStG, AO, VermG, WoFG, WoBindG, etc.

### ⏸️ Phase 3-7: OFFEN
- **Phase 3**: Ergänzende Gesetze (12 Gesetze, +500 Docs)
- **Phase 4**: Landesbauordnungen (16 LBOs, +800 Docs)
- **Phase 5**: Rechtsprechung komplett (+450 Urteile)
- **Phase 6**: Literatur komplett (+500 Kommentierungen)
- **Phase 7**: Verwaltungsrecht (+400 BMF-Schreiben)

---

## 🚀 NÄCHSTE SCHRITTE (Priorisiert)

### 1. **SOFORT** - Komplettierung Phase 1 Gesetze
- [ ] BauGB komplett scrapen (249 §§) - **WICHTIGSTE EINZELAUFGABE**
- [ ] BauNVO (26 §§), ROG (28 §§), ImmoWertV (15 §§)
- [ ] WiStG § 5 (Mietpreisüberhöhung), TrinkwV (16 §§)
- **Ziel**: +340 Paragraphen → 374/800 (46,75%)

### 2. **HOCHPRIORITÄT** - Rechtsprechung erweitern
- [ ] BGH weitere +139 Urteile (Mietrecht, Kaufrecht, WEG, Bau)
- [ ] BFH weitere +121 Urteile (Grunderwerbsteuer, Erbschaft, Umsatz)
- [ ] EuGH weitere +90 Urteile (Kapitalverkehr, Niederlassungsfreiheit)
- **Ziel**: +350 Urteile → 450 Gesamturteile

### 3. **MITTELFRISTIG** - Phase 2 komplettieren
- [ ] UStG (§§ 1, 2, 4, 12, 15), ErbStG (§§ 1-19), AO (§§ 38, 42, 169-171)
- [ ] VermG, SachenRBerG, WoFG, WoBindG
- **Ziel**: +150 Paragraphen

### 4. **PARALLEL** - Literatur massiv erweitern
- [ ] Palandt BGB Kaufrecht komplett (§§ 433-479)
- [ ] Palandt BGB Mietrecht komplett (§§ 535-580a)
- [ ] Palandt BGB Sachenrecht komplett (§§ 854-1296)
- [ ] MüKo Bände: Mietrecht, Sachenrecht, Kaufrecht
- [ ] Staudinger, Soergel, Erman
- **Ziel**: +675 Kommentierungen → 1000 Literatur gesamt

---

## 💡 EMPFEHLUNGEN

### Technisch:
1. **Web-Scraper für BauGB entwickeln** (gesetze-im-internet.de)
   - Automatisches Parsen aller 249 Paragraphen
   - Strukturierte Extraktion (Titel, Absätze, Fundstelle)
   - Batch-Upload zu Qdrant

2. **Juris API/Scraper für Rechtsprechung**
   - Automatisiertes Abrufen von BGH/BFH-Urteilen
   - Filter: Immobilienrecht, Steuerrecht, Mietrecht
   - Volltext-Extraktion mit Leitsätzen

3. **Beck-Online/Juris für Literatur**
   - API-Zugang zu Palandt, MüKo, Schmidt
   - Strukturierte Kommentierung-Extraktion
   - Paragraph-weise Aufbereitung

### Organisatorisch:
1. **Priorität auf kritische §§**: Nicht alle Paragraphen sind gleich wichtig
   - BauGB: Fokus auf §§ 1, 34, 35, 172-179 (90% aller Fälle)
   - Palandt: Fokus auf Praxisparagraphen (z.B. § 536, 543, 556, 573)

2. **Qualität vor Quantität**: 
   - Lieber 50 perfekt kommentierte Paragraphen als 500 Rohparagraphen
   - Mit Praxisbeispielen, Rechtsprechungsverweisen, Checklisten

3. **Inkrementelles Seeding**:
   - Nicht auf 5000 warten → Kontinuierlich deployen
   - Jede Woche +100-200 Dokumente ist besser als Monatssprünge

---

## 📊 PROJEKTION

Bei aktuellem Tempo (75 Docs/Tag):
- **30. Dezember**: 1.850 Dokumente (BauGB-Scraper fertig)
- **05. Januar 2025**: 2.300 Dokumente (Phase 1 komplett)
- **20. Januar 2025**: 3.500 Dokumente (Rechtsprechung erweitert)
- **15. Februar 2025**: 5.000+ Dokumente (ZIEL ERREICHT)

---

**Erstellt**: 29.12.2024  
**Letztes Update**: Seed-Literatur läuft (1706 → 1731 erwartet)  
**Nächster Meilenstein**: BauGB-Scraper (249 §§)
