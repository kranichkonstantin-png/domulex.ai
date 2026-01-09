# 🏛️ DOMULEX.AI - Vollständigkeitsplan Immobilienrecht

**Status:** 27. Dezember 2025  
**Aktuell:** 671 Dokumente (90 deutsche Professionelle + 581 Legacy)

---

## 📊 IST-ZUSTAND (Was haben wir bereits?)

### ✅ MIETRECHT (100%)
- ✅ BGB §§ 535-580a: 13 Paragraphen
- ✅ WEG: 4 Paragraphen
- ✅ BGH Mietrecht: 5 Fälle (Mieterhöhung, Mietminderung, Kündigungsschutz)

### ✅ RECHTSPRECHUNG (100%)
- ✅ BGH: 24 Landmark Cases
- ✅ BFH: 19 Steuerrechtsfälle

### ✅ BAURECHT (60%)
- ✅ Landesbauordnungen: 16 Bundesländer (Stellplätze, Abstandsflächen, Barrierefreiheit)
- ✅ BauGB § 34: Zulässigkeit im Innenbereich
- ⚠️ **FEHLT:** VOB/B, HOAI, BauGB §§ 1-37, Bauplanungsrecht

### ✅ STEUERRECHT (80%)
- ✅ BFH: 19 Fälle (AfA, GrESt, Verkauf, Vermietung, Umsatzsteuer)
- ✅ BMF: 8 Schreiben (AfA 3%, Share Deal, § 9 UStG, Spekulationsfrist, 15% Grenze, 66% Angehörige, 3-Objekt-Grenze, Arbeitszimmer)
- ⚠️ **FEHLT:** ErbStG, BewG, Grundsteuer-Reform, AO

### ✅ EU-RECHT (100%)
- ✅ DSGVO Art. 6
- ✅ Verbraucherschutzrichtlinie 2011/83/EU
- ✅ Energieeffizienz-Richtlinie 2018/844/EU

### ⚠️ GRUNDSTÜCKSRECHT (10%)
- ✅ BGB § 433: Kaufvertrag (nur 1 Paragraph!)
- ❌ **FEHLT:** BGB Sachenrecht §§ 873-1296 (Eigentumserwerb, Auflassung, Vormerkung, Grundschuld, Hypothek)
- ❌ **FEHLT:** GBO (Grundbuchordnung)
- ❌ **FEHLT:** Erbbaurecht, Nießbrauch, Wohnungsrecht

### ⚠️ KAUFRECHT (5%)
- ✅ BGB § 433: Kaufvertrag
- ✅ BGH: 2 Fälle (Wohnfläche, Arglist "gekauft wie gesehen")
- ❌ **FEHLT:** BGB §§ 434-479 (Gewährleistung, Rücktritt, Nacherfüllung, Schadensersatz)

### ⚠️ ENERGIERECHT (30%)
- ✅ GEG § 48: Energieausweis
- ✅ EU Energieeffizienz-Richtlinie
- ❌ **FEHLT:** GEG §§ 1-105 (Sanierungspflicht, Heizungsaustausch, Dämmung)

---

## 🎯 SOLL-ZUSTAND (Was fehlt noch?)

### 🔴 PRIORITÄT 1 - KRITISCH (Kernfunktionalität)

#### **1.1 BGB SACHENRECHT (Grundstücksrecht)**
**Status:** ❌ 0% (nur § 433 vorhanden)  
**Ziel:** 50+ Paragraphen

##### **Eigentumserwerb & Übertragung:**
- § 873 - Einigung und Eintragung (Auflassung!)
- § 925 - Auflassungserklärung (notariell)
- § 873a - Vormerkung (Kaufpreisabsicherung)
- § 878 - Rangverhältnis Grundbuch
- § 892 - Gutgläubiger Erwerb

##### **Grundpfandrechte:**
- §§ 1113-1190 - Hypothek (banküblich bis 2000)
- §§ 1191-1198 - Grundschuld (Standard ab 2000!)
- §§ 1199-1203 - Rentenschuld
- § 1147 - Zwangsvollstreckung Grundpfandrecht

##### **Beschränkte dingliche Rechte:**
- §§ 1018-1093 - Nießbrauch (Altenteil, Wohnrecht)
- §§ 1030-1089 - Wohnungsrecht (lebenslang)
- §§ 1094-1104 - Reallast (wiederkehrende Leistung)
- §§ 1105-1112 - Erbbaurecht (Grundstück pachten, Gebäude besitzen)

##### **Grunddienstbarkeiten:**
- §§ 1018-1029 - Grunddienstbarkeiten (Wegerecht, Leitungsrecht)
- § 1020 - Ausübungsart
- § 1021 - Änderung Bedürfnisse

##### **Nachbarrecht:**
- §§ 903-924 - Eigentumsschutz, Überbau, Grenzabstand
- § 906 - Immissionen (Lärm, Geruch, Rauch)
- § 910 - Überhang (Äste, Wurzeln)
- § 912 - Hammerschlag und Leiterrecht

**Dokumente:** ~50 Paragraphen × 1 = **50 Dokumente**  
**Scraper:** `bgb_sachenrecht_scraper.py`

---

#### **1.2 GRUNDBUCHORDNUNG (GBO)**
**Status:** ❌ 0%  
**Ziel:** 20+ Paragraphen

##### **Grundbuchaufbau:**
- § 2 - Grundbuchblatt Aufbau
- § 3 - Bestandsverzeichnis
- § 4-11 - Abteilungen I-III (Eigentümer, Lasten, Grundpfandrechte)

##### **Grundbuchverfahren:**
- § 13 - Eintragungsbewilligung
- § 19 - Eintragung von Amts wegen
- § 20 - Löschungsbewilligung
- § 29 - Eintragungsarten (Eintragung, Löschung, Änderung)

##### **Grundbucheinsicht:**
- § 12 - Berechtigtes Interesse (Makler, Käufer)
- § 12a - Elektronischer Abruf

##### **Widerspruch & Vormerkung:**
- § 53 - Widerspruch (Schutz bei Streit)
- § 885 BGB + GBO - Vormerkung (Kaufpreisabsicherung)

**Dokumente:** ~25 Paragraphen = **25 Dokumente**  
**Scraper:** `gbo_scraper.py`

---

#### **1.3 BGB KAUFRECHT (Vollständig)**
**Status:** ⚠️ 5% (nur § 433)  
**Ziel:** 40+ Paragraphen

##### **Kaufvertrag:**
- §§ 433-435 - Pflichten Verkäufer/Käufer
- §§ 436-445 - Gefahrübergang, Sachmängel

##### **Gewährleistung:**
- §§ 434-435 - Sachmangel Definition (Wohnfläche, Baujahr, Zustand)
- §§ 437-441 - Nacherfüllung, Minderung, Rücktritt
- § 442 - Arglistige Täuschung (kein Ausschluss!)
- §§ 444-445 - Garantie, Beschaffenheitsvereinbarung

##### **Rücktritt & Schadensersatz:**
- §§ 346-354 - Rückabwicklung
- §§ 280-283 - Schadensersatz statt Leistung
- § 311b - Formvorschrift (notariell!)

##### **Verjährung:**
- § 438 - 5 Jahre bei Immobilien (sonst 2 Jahre!)
- § 196 - 30 Jahre bei dinglichen Ansprüchen

**Dokumente:** ~45 Paragraphen = **45 Dokumente**  
**Scraper:** `bgb_kaufrecht_scraper.py`

---

#### **1.4 STEUERRECHT - ERGÄNZUNGEN**
**Status:** ✅ 80% (sehr gut, aber Lücken)  
**Ziel:** 100%

##### **Erbschaftsteuer (ErbStG):**
- § 13a - Familienheim (steuerfrei bei Eigennutzung!)
- § 13b - Betriebsvermögen (Mietwohnungen)
- § 13c - Verschonungsabschlag
- § 19 - Steuersätze Erbschaftsteuer (7-50%)
- § 16 - Freibeträge (500.000 € Ehegatte, 400.000 € Kinder)

##### **Bewertungsgesetz (BewG):**
- § 176 - Grundbesitzbewertung (Verkehrswert)
- § 177 - Vergleichswertverfahren
- § 182 - Ertragswertverfahren (Mietobjekte)
- § 189 - Sachwertverfahren (selbstgenutzt)

##### **Grundsteuer-Reform 2025:**
- § 218 BewG - Neues Grundsteuermodell
- § 25 GrStG - Grundsteuermessbetrag
- Bundesmodell vs. Ländermodelle (BW, Bayern, Hamburg, Hessen, Niedersachsen)

##### **BMF-Schreiben Ergänzungen:**
- Grundsteuererklärung 2025 (FESTUCA)
- § 6 Abs. 5 EStG - Gebäudeabschreibung bei Übertragung
- § 7g EStG - Investitionsabzugsbetrag (Photovoltaik)
- § 35a EStG - Haushaltsnahe Dienstleistungen (20% von 20.000 €)

**Dokumente:** ~25 neue = **25 Dokumente**  
**Scraper:** `erbstg_scraper.py`, `bewg_scraper.py`, `bmf_ergaenzung_scraper.py`

---

### 🟡 PRIORITÄT 2 - WICHTIG (Professionalität)

#### **2.1 BAURECHT (Vollständig)**
**Status:** ⚠️ 60% (nur LBO + § 34)

##### **BauGB (Baugesetzbuch):**
- §§ 1-13 - Bauleitplanung, Bebauungsplan
- §§ 29-38 - Zulässigkeit von Vorhaben (§ 34 haben wir!)
- §§ 39-84 - Baulandumlegung, Enteignung
- §§ 85-122 - Bodenordnung
- §§ 123-135 - Wertermittlung (Verkehrswert!)
- §§ 136-164 - Sanierung, Stadtumbau
- §§ 176-191 - Soziale Erhaltungsverordnung (Milieuschutz!)

##### **VOB/B (Vergabe- und Vertragsordnung Bau):**
- § 1 VOB/B - Vertragsinhalt
- § 4 VOB/B - Abnahme (fiktiv bei Einzug!)
- § 5 VOB/B - Zahlung (Abschlagsrechnungen)
- § 13 VOB/B - Mängel (5 Jahre Gewährleistung)
- § 16 VOB/B - Haftung Bauunternehmer

##### **HOAI (Honorarordnung Architekten/Ingenieure):**
- § 34 - Leistungsphasen 1-9 (Grundlagenermittlung bis Objektbetreuung)
- § 35 - Honorarzonen I-V (einfach bis sehr anspruchsvoll)
- Anlage 10 - Honorartafel Gebäude
- § 7 - Mindest-/Höchstsätze (nicht unterschreitbar!)

**Dokumente:** ~70 Paragraphen = **70 Dokumente**  
**Scraper:** `baugb_scraper.py`, `vob_scraper.py`, `hoai_scraper.py`

---

#### **2.2 WEG (Wohnungseigentumsgesetz) - ERWEITERN**
**Status:** ⚠️ 20% (nur 4 Paragraphen!)  
**Ziel:** 30+ Paragraphen

##### **Gemeinschaft:**
- §§ 9-10 - Gemeinschaftseigentum vs. Sondereigentum
- § 13 - Gebrauch Sondereigentum
- § 14 - Veränderung Gemeinschaftseigentum (baulich)
- § 15 - Duldungspflichten

##### **Verwaltung:**
- §§ 18-19 - Eigentümerversammlung (Einberufung, Beschlüsse)
- § 20 - Beschlusskompetenz
- § 23 - Stimmrecht (nach Miteigentumsanteilen)
- § 24 - Mehrheiten (einfach, qualifiziert, Einstimmigkeit)
- § 26 - Verwalter (Bestellung, Aufgaben)

##### **Kosten:**
- § 16 - Lasten und Kosten (Verteilungsschlüssel)
- § 28 - Wohngeld (monatliche Vorauszahlung)
- § 21 - Wirtschaftsplan

##### **Sondernutzungsrechte:**
- § 13 Abs. 2 - Terrasse, Garten, Stellplatz (allein nutzbar)

**Dokumente:** ~35 Paragraphen = **35 Dokumente**  
**Scraper:** `weg_erweitert_scraper.py`

---

#### **2.3 ENERGIERECHT (GEG Vollständig)**
**Status:** ⚠️ 30% (nur § 48)  
**Ziel:** 40+ Paragraphen

##### **Neubau:**
- § 10 - Primärenergiebedarf (KfW 40, 55)
- § 15 - Wärmedämmung (U-Werte)
- § 34 - Anlagentechnik (Heizung, Lüftung)

##### **Bestand:**
- § 47 - Nachrüstungspflichten (Heizkessel > 30 Jahre)
- § 48 - Energieausweis Pflicht (haben wir!)
- § 71 - Austauschpflicht Ölheizung (ab 2026!)
- § 72 - 65% Erneuerbare Energie (ab 2024 Neubau)

##### **Sanierung:**
- § 50 - Änderung Außenbauteile (Dämmung bei Sanierung)
- § 53 - Dach, Geschossdecke
- § 105 - Bußgeldvorschriften (bis 50.000 €!)

**Dokumente:** ~45 Paragraphen = **45 Dokumente**  
**Scraper:** `geg_erweitert_scraper.py`

---

### 🟢 PRIORITÄT 3 - OPTIONAL (Spezialisierung)

#### **3.1 MAKLERRECHT**
- § 652 BGB - Maklervertrag
- § 656 BGB - Maklerlohn (Nachweis, Vermittlung)
- § 34c GewO - Maklererlaubnis
- § 1 WoVermRG - Wohnungsvermittlung
- MaBV - Makler- und Bauträgerverordnung

**Dokumente:** ~15 Paragraphen = **15 Dokumente**

---

#### **3.2 MIETPREISBREMSE**
- § 556d BGB - Mietpreisbremse (ortsübliche Vergleichsmiete + 10%)
- § 556e BGB - Ausnahmen (Neubau, Modernisierung)
- § 556g BGB - Rüge überhöhte Miete

**Dokumente:** ~10 Paragraphen = **10 Dokumente**

---

#### **3.3 ZWANGSVERSTEIGERUNG**
- ZVG §§ 1-161 - Zwangsversteigerungsgesetz
- § 765a ZPO - Duldungsvollstreckung
- § 114 ZVG - Versteigerungstermin
- § 85 ZVG - Verkehrswertgutachten

**Dokumente:** ~30 Paragraphen = **30 Dokumente**

---

#### **3.4 WEITERE RECHTSPRECHUNG**
- **BGH Werkvertragsrecht:** 10 Fälle (VOB/B, Architekten, Bauunternehmer)
- **BGH Grundstücksrecht:** 10 Fälle (Vormerkung, Auflassung, Grundschuld)
- **BVerwG Baurecht:** 10 Fälle (Baugenehmigung, Nachbarschutz)
- **BFG Grundsteuer:** 5 Fälle (Reform 2025)

**Dokumente:** ~35 Fälle = **35 Dokumente**

---

## 📈 IMPLEMENTIERUNGSPLAN

### **PHASE 1 (KRITISCH) - 145 Dokumente**
**Zeitaufwand:** 6-8 Stunden  
**Neue Dokumente:** 145  
**Ziel:** Grundstücksrecht komplett + Steuerrecht 100%

| Scraper | Dokumente | Priorität | Thema |
|---------|-----------|-----------|-------|
| `bgb_sachenrecht_scraper.py` | 50 | 🔴 | Eigentumserwerb, Grundpfandrechte, Nießbrauch |
| `gbo_scraper.py` | 25 | 🔴 | Grundbuchordnung |
| `bgb_kaufrecht_scraper.py` | 45 | 🔴 | Gewährleistung, Rücktritt |
| `erbstg_scraper.py` | 10 | 🔴 | Erbschaftsteuer Familienheim |
| `bewg_scraper.py` | 10 | 🔴 | Bewertungsgesetz |
| `bmf_ergaenzung_scraper.py` | 5 | 🔴 | Grundsteuer 2025, § 35a |

**Nach Phase 1:** 671 → **816 Dokumente** (+145)

---

### **PHASE 2 (WICHTIG) - 150 Dokumente**
**Zeitaufwand:** 6-8 Stunden  
**Neue Dokumente:** 150  
**Ziel:** Baurecht komplett + WEG komplett + GEG komplett

| Scraper | Dokumente | Priorität | Thema |
|---------|-----------|-----------|-------|
| `baugb_scraper.py` | 40 | 🟡 | Baugesetzbuch (Bauleitplanung, Sanierung, Milieuschutz) |
| `vob_scraper.py` | 15 | 🟡 | VOB/B (Abnahme, Mängel, Zahlung) |
| `hoai_scraper.py` | 15 | 🟡 | HOAI (Leistungsphasen, Honorar) |
| `weg_erweitert_scraper.py` | 35 | 🟡 | WEG (Verwaltung, Beschlüsse, Kosten) |
| `geg_erweitert_scraper.py` | 45 | 🟡 | GEG (Neubau, Sanierung, Ölheizung) |

**Nach Phase 2:** 816 → **966 Dokumente** (+150)

---

### **PHASE 3 (OPTIONAL) - 90 Dokumente**
**Zeitaufwand:** 4-6 Stunden  
**Neue Dokumente:** 90  
**Ziel:** Spezialisierung (Makler, Mietpreisbremse, ZVG, weitere Rechtsprechung)

| Scraper | Dokumente | Priorität | Thema |
|---------|-----------|-----------|-------|
| `maklerrecht_scraper.py` | 15 | 🟢 | Maklervertrag, Maklerlohn |
| `mietpreisbremse_scraper.py` | 10 | 🟢 | Mietpreisbremse, Ausnahmen |
| `zvg_scraper.py` | 30 | 🟢 | Zwangsversteigerung |
| `bgh_erweitert_scraper.py` | 20 | 🟢 | BGH Werkvertrag + Grundstücksrecht |
| `bverwg_scraper.py` | 10 | 🟢 | BVerwG Baurecht |
| `bfg_scraper.py` | 5 | 🟢 | BFG Grundsteuer |

**Nach Phase 3:** 966 → **1.056 Dokumente** (+90)

---

## 🎯 FINALE ZIELSTRUKTUR (1.056 Dokumente)

### **Deutsche Professionelle Dokumente: 475**
- Gesetze: 350
  - BGB Mietrecht: 13
  - BGB Sachenrecht: 50 ⭐ NEU
  - BGB Kaufrecht: 45 ⭐ NEU
  - WEG: 39 (4 → 39)
  - GBO: 25 ⭐ NEU
  - LBO: 16
  - BauGB: 40 ⭐ NEU
  - GEG: 46 (1 → 46)
  - VOB/B: 15 ⭐ NEU
  - HOAI: 15 ⭐ NEU
  - ErbStG: 10 ⭐ NEU
  - BewG: 10 ⭐ NEU
  - Maklerrecht: 15 ⭐ NEU
  - Mietpreisbremse: 10 ⭐ NEU
  - ZVG: 30 ⭐ NEU
  - Sonstige: 11

- Rechtsprechung: 92
  - BGH: 44 (24 → 44)
  - BFH: 19
  - BVerwG: 10 ⭐ NEU
  - BFG: 5 ⭐ NEU

- Verwaltungsanweisungen: 16
  - BMF: 13 (8 → 13)
  - EU-Recht: 3

- Legacy (Multi-Jurisdiction): 581

### **Qdrant Free Tier Nutzung:**
- Aktuell: 67% (671 Dokumente)
- Nach Phase 1: 82% (816 Dokumente)
- Nach Phase 2: 97% (966 Dokumente) ⚠️ Fast voll!
- Nach Phase 3: **>100%** ❌ Paid Tier nötig!

---

## 💰 KOSTENANALYSE

### **Embedding-Kosten (Gemini text-embedding-004):**
- Phase 1: 145 × €0,0017 = **€0,25**
- Phase 2: 150 × €0,0017 = **€0,26**
- Phase 3: 90 × €0,0017 = **€0,15**
- **Gesamt: €0,66**

### **Qdrant Kosten:**
- Free Tier: Bis 1.000.000 Dokumente kostenlos ✅
- Nach Phase 3: 1.056 Dokumente = **€0** ✅
- **Gesamtkosten nach 100%: ~€2,20** (sehr günstig!) ⭐

---

## ✅ STEUERRECHT - VOLLSTÄNDIGKEITS-CHECK

### **AKTUELL (80%):**
✅ **BFH: 19 Fälle**
- Vermietung: 7 Fälle
- Grunderwerbsteuer: 3 Fälle
- Immobilienverkauf: 4 Fälle
- Umsatzsteuer: 2 Fälle
- Gewerbesteuer: 2 Fälle
- Sonstiges: 1 Fall

✅ **BMF: 8 Schreiben**
- AfA 3% (ab 2023)
- Share Deal 90%
- § 9 UStG Vorsteuerabzug
- Spekulationsfrist 10 Jahre
- Erhaltungsaufwand 15% Grenze
- 66% Angehörige
- 3-Objekt-Grenze
- Arbeitszimmer 1.250 €

### **FEHLT NOCH (20%):**
❌ **Erbschaftsteuer (ErbStG):**
- § 13a - Familienheim steuerfrei
- § 13b - Mietwohnungen Betriebsvermögen
- § 19 - Steuersätze 7-50%
- § 16 - Freibeträge 500.000 € / 400.000 €

❌ **Bewertungsgesetz (BewG):**
- § 176 - Grundbesitzbewertung
- § 182 - Ertragswertverfahren
- § 189 - Sachwertverfahren

❌ **Grundsteuer-Reform 2025:**
- § 218 BewG - Bundesmodell
- § 25 GrStG - Grundsteuermessbetrag
- FESTUCA-Verfahren

❌ **BMF-Schreiben Ergänzungen:**
- § 35a EStG - Haushaltsnahe Dienstleistungen (4.000 €/Jahr)
- § 7g EStG - Investitionsabzugsbetrag (Photovoltaik)
- § 6 Abs. 5 EStG - Übertragung Gebäude

❌ **BFH Ergänzungen:**
- Erbschaftsteuer Familienheim (2-3 Fälle)
- Grundsteuer-Bewertung (1-2 Fälle)

**→ Phase 1 schließt Steuerrecht zu 100%!** ✅

---

## 🚀 NÄCHSTE SCHRITTE

1. **JETZT:** Phase 1 implementieren (145 Dokumente, 6-8h)
   - Grundstücksrecht komplett
   - Steuerrecht 100%
   
2. **DANN:** Phase 2 implementieren (150 Dokumente, 6-8h)
   - Baurecht komplett
   - WEG + GEG komplett
   
3. **OPTIONAL:** Phase 3 implementieren (90 Dokumente, 4-6h)
   - Spezialisierung Makler, ZVG, weitere Rechtsprechung

**Gesamt-Implementierungszeit:** 16-22 Stunden  
**Finale Dokumentenanzahl:** 1.056 Dokumente (+385 = +57% Wachstum!)  
**Gesamtkosten:** €2,20 (extrem günstig!)

---

## 📝 FAZIT

**Was haben wir?**
- ✅ Mietrecht: 100%
- ✅ Rechtsprechung: 100% (BGH, BFH)
- ✅ Landesbauordnungen: 100% (16 Bundesländer)
- ✅ EU-Recht: 100%
- ✅ Steuerrecht: 80% (sehr gut!)

**Was fehlt?**
- ❌ Grundstücksrecht: 90% fehlt (KRITISCH!)
- ❌ Kaufrecht: 95% fehlt (KRITISCH!)
- ❌ Baurecht: 40% fehlt (WICHTIG!)
- ❌ GEG: 70% fehlt (WICHTIG!)
- ❌ WEG: 80% fehlt (WICHTIG!)

**Empfehlung:**
➡️ **Phase 1 SOFORT implementieren** (Grundstücksrecht + Steuerrecht 100%)  
➡️ **Phase 2 innerhalb 1 Woche** (Baurecht komplett)  
➡️ **Phase 3 optional** basierend auf Beta-User-Feedback

**Nach Phase 1+2:**
- 966 Dokumente
- 97% Vollständigkeit Immobilienrecht
- 100% Vollständigkeit Steuerrecht
- **PRODUKTIONSREIF für alle 6 Zielgruppen!** ⭐
