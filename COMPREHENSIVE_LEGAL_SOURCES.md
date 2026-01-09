# DOMULEX - Vollständige Rechtsquellen-Architektur

## 🌍 Jurisdiktionen & Rechtsquellen

### 🇩🇪 **DEUTSCHLAND**

#### Bundesrecht (Federal Law)
| Quelle | Typ | Scraping-Frequenz | Priorität |
|--------|-----|-------------------|-----------|
| **BGB** (Bürgerliches Gesetzbuch) | Gesetz | Wöchentlich | 🔴 KRITISCH |
| **WEG** (Wohnungseigentumsgesetz) | Gesetz | Wöchentlich | 🔴 KRITISCH |
| **BauGB** (Baugesetzbuch) | Gesetz | Wöchentlich | 🟠 HOCH |
| **GrStG** (Grundsteuergesetz) | Gesetz | Wöchentlich | 🟠 HOCH |
| **MietRÄndG** (Mietrechtsänderungsgesetz) | Gesetz | Wöchentlich | 🔴 KRITISCH |
| **BetrKV** (Betriebskostenverordnung) | Verordnung | Monatlich | 🟠 HOCH |

**Quelle:** https://www.gesetze-im-internet.de

#### Höchstrichterliche Rechtsprechung
| Gericht | Zuständigkeit | Scraping | Priorität |
|---------|---------------|----------|-----------|
| **BGH** (Bundesgerichtshof) | Zivilrecht (Mietrecht, Immobilienrecht) | Alle 4 Stunden | 🔴 KRITISCH |
| **BFH** (Bundesfinanzhof) | Steuerrecht (AfA, Grundsteuer, Vermietungseinkünfte) | Täglich | 🔴 KRITISCH |
| **BVerfG** (Bundesverfassungsgericht) | Verfassungsrecht (Mietpreisbremse, Enteignung) | Wöchentlich | 🟡 MITTEL |

**Quellen:**
- BGH: https://www.bundesgerichtshof.de
- BFH: https://www.bundesfinanzhof.de
- BVerfG: https://www.bundesverfassungsgericht.de

#### Landesrecht (16 Bundesländer)
| Bundesland | Bauordnung | Priorität |
|------------|------------|-----------|
| **Bayern** | BayBO (Bayerische Bauordnung) | 🟠 HOCH |
| **NRW** | BauO NRW | 🟠 HOCH |
| **Baden-Württemberg** | LBO BW | 🟠 HOCH |
| **Berlin** | BauO Bln | 🟠 HOCH |
| **Hamburg** | HBauO | 🟠 HOCH |
| Alle anderen 11 | Landesbauordnungen | 🟡 MITTEL |

**Themen:**
- Abstandsflächen
- Stellplatzpflicht
- Denkmalschutz
- Wohnflächenberechnung

#### Kommunalrecht
| Ebene | Beispiele | Scraping |
|-------|-----------|----------|
| **Gemeindesatzungen** | Stellplatzsatzung, Gestaltungssatzung | Bei Bedarf |
| **Bebauungspläne** | B-Pläne (GIS-Daten) | Bei Bedarf |
| **Mietspiegel** | Qualifizierte Mietspiegel (München, Berlin, Hamburg) | Jährlich |

---

### 🇪🇺 **EUROPÄISCHE UNION**

#### EU-Gerichte
| Gericht | Zuständigkeit | Relevanz |
|---------|---------------|----------|
| **EuGH** (Europäischer Gerichtshof) | EU-Recht (Verbraucherschutz, Dienstleistungsfreiheit) | 🟠 HOCH |
| **EuG** (Gericht der EU) | Wettbewerbsrecht | 🟡 MITTEL |

**Quelle:** https://curia.europa.eu

#### EU-Verordnungen (direkt anwendbar)
| Verordnung | Thema | Priorität |
|------------|-------|-----------|
| **DSGVO** | Datenschutz (Mieterdaten) | 🔴 KRITISCH |
| **EU-Gebäuderichtlinie** | Energieeffizienz (ESG) | 🟠 HOCH |
| **MiFID II** | Immobilieninvestments | 🟡 MITTEL |

#### EU-Richtlinien (Umsetzung in nationales Recht)
| Richtlinie | Thema | Status |
|------------|-------|--------|
| **Wohnimmobilienkreditrichtlinie** | Finanzierung | Umgesetzt |
| **Energieeffizienz-Richtlinie** | Gebäudesanierung | Umgesetzt |

**Quelle:** https://eur-lex.europa.eu

---

### 🇺🇸 **UNITED STATES**

#### Federal Law
| Quelle | Typ | Priorität |
|--------|-----|-----------|
| **U.S. Code Title 26** | Federal Tax Code (Depreciation, 1031 Exchange) | 🔴 KRITISCH |
| **Fair Housing Act** | Anti-Diskriminierung | 🟠 HOCH |
| **ADA** (Americans with Disabilities Act) | Barrierefreiheit | 🟠 HOCH |

#### Supreme Court & Federal Courts
| Gericht | Zuständigkeit | Scraping |
|---------|---------------|----------|
| **U.S. Supreme Court** | Verfassungsrecht | Wöchentlich |
| **Federal Courts of Appeals** | Bundesberufungsgerichte | Wöchentlich |
| **U.S. Tax Court** | Steuerstreitigkeiten | Täglich |

**Quelle:** https://www.courtlistener.com (API)

#### State Law (Focus: Real Estate Hotspots)
| Staat | Statutes | Common Law | Priorität |
|-------|----------|------------|-----------|
| **Florida** | Florida Statutes Chapter 83 (Landlord-Tenant) | Case Law | 🔴 KRITISCH |
| **New York** | NY Real Property Law | Rent Control Cases | 🔴 KRITISCH |
| **California** | CA Civil Code (Security Deposits) | Eviction Moratorium | 🔴 KRITISCH |
| **Texas** | TX Property Code | HOA Disputes | 🟠 HOCH |
| **Nevada** | NV Landlord-Tenant Law | Short-Term Rentals | 🟠 HOCH |

#### Municipal Codes
| Stadt | Code | Beispiel |
|-------|------|----------|
| **Miami** | Miami Code | Short-Term Rental Regulations |
| **NYC** | NYC Administrative Code | Rent Stabilization |
| **San Francisco** | SF Municipal Code | Eviction Protections |

**Quellen:**
- State Legislatures: https://www.ncsl.org
- Municipal Codes: https://www.municode.com

---

### 🇪🇸 **SPANIEN**

#### Nationales Recht
| Quelle | Typ | Priorität |
|--------|-----|-----------|
| **LAU** (Ley de Arrendamientos Urbanos) | Mietrecht | 🔴 KRITISCH |
| **Ley Hipotecaria** | Hypothekenrecht | 🟠 HOCH |
| **LIRPF** (Impuesto sobre la Renta) | Einkommensteuer (Vermietung) | 🟠 HOCH |
| **IBI** (Impuesto sobre Bienes Inmuebles) | Grundsteuer | 🟠 HOCH |

#### Gerichte
| Gericht | Zuständigkeit | Scraping |
|---------|---------------|----------|
| **Tribunal Supremo** | Höchstes Gericht | Wöchentlich |
| **Audiencias Provinciales** | Berufungsgerichte | Monatlich |

**Quelle:** https://www.boe.es (Boletín Oficial del Estado)

#### Regionales Recht (Comunidades Autónomas)
| Region | Besonderheiten | Priorität |
|--------|----------------|-----------|
| **Cataluña** | Eigenes Zivilrecht (Código Civil de Cataluña) | 🟠 HOCH |
| **País Vasco** | Steuerautonomie | 🟠 HOCH |
| **Andalucía** | Tourismuswohnungen | 🟡 MITTEL |

---

### 🇦🇪 **UAE / DUBAI** (NEU!)

#### Federal Law
| Quelle | Typ | Priorität |
|--------|-----|-----------|
| **UAE Federal Law No. 5/1985** | Civil Transactions Law | 🔴 KRITISCH |
| **UAE Property Law** | Real Estate Ownership (Freehold) | 🔴 KRITISCH |
| **Strata Law** | Gemeineigentum (wie WEG) | 🟠 HOCH |

#### Dubai-Spezifische Gesetze
| Quelle | Beschreibung | Priorität |
|--------|--------------|-----------|
| **RERA** (Real Estate Regulatory Authority) | Mietstreitigkeiten, Mietindex | 🔴 KRITISCH |
| **Dubai Land Department** | Grundbuchrecht, Ejari (Mietregistrierung) | 🔴 KRITISCH |
| **Dubai Municipality** | Bauvorschriften | 🟠 HOCH |

#### Gerichte
| Gericht | Zuständigkeit | Sprache |
|---------|---------------|---------|
| **Dubai Courts** | Zivilrecht, Mietstreitigkeiten | Arabisch + Englisch |
| **DIFC Courts** (Dubai International Financial Centre) | Common Law (Englisch) | Englisch |

**Quellen:**
- https://www.dxbcourts.gov.ae
- https://www.difccourts.ae
- https://dubailand.gov.ae

#### Besonderheiten
- **Ejari:** Pflichtregistrierung aller Mietverträge
- **Rental Index:** Staatlich festgelegte Mietobergrenzen
- **Service Charges:** WEG-ähnliche Nebenkosten
- **Cooling Fees:** Dubai-spezifische Klimatisierungskosten

---

## 📊 **Priorisierte Implementierung**

### **Phase 1: FOUNDATION (Woche 1-2)** ✅ TEILWEISE FERTIG
- [x] BGB Mietrecht (§§ 535-580a) - **17 Paragraphen geseedet**
- [x] WEG (Grundlagen) - **4 Paragraphen geseedet**
- [ ] Florida Statutes Chapter 83
- [ ] LAU (Spanisches Mietrecht)

### **Phase 2: CRITICAL JURISPRUDENCE (Woche 3-4)**
- [ ] BGH Mietrecht-Urteile (letzte 5 Jahre)
- [ ] BFH Steuerrecht-Urteile (AfA, Grundsteuer)
- [ ] U.S. Supreme Court (Real Estate Cases)
- [ ] Tribunal Supremo (LAU-Rechtsprechung)

### **Phase 3: TAX & BUILDING LAW (Woche 5-6)**
- [ ] GrStG (Grundsteuergesetz)
- [ ] BauGB (Baugesetzbuch)
- [ ] IRC (U.S. Tax Code - 1031, Depreciation)
- [ ] LIRPF (Spanische Einkommensteuer)

### **Phase 4: EU LAW (Woche 7-8)**
- [ ] EuGH-Rechtsprechung (Verbraucherschutz)
- [ ] DSGVO (Datenschutz)
- [ ] Gebäudeeffizienz-Richtlinien

### **Phase 5: REGIONAL LAW (Woche 9-12)**
- [ ] Landesbauordnungen (16 Bundesländer)
- [ ] State Statutes (50 US-Staaten - Fokus auf Top 10)
- [ ] Comunidades Autónomas (Spanien)

### **Phase 6: DUBAI/UAE (Woche 13-14)**
- [ ] UAE Federal Law
- [ ] RERA Regulations
- [ ] Dubai Courts Precedents
- [ ] Ejari System Integration

### **Phase 7: MUNICIPAL LAW (Ongoing)**
- [ ] Mietspiegel (Top 20 deutsche Städte)
- [ ] NYC Rent Stabilization
- [ ] SF Eviction Protections
- [ ] Madrid Rental Regulations

---

## 🔄 **Automatisierte Ingestion-Pipelines**

### Deutsche Quellen
```python
# BGH (Alle 4 Stunden)
scrape_bgh_cases() → Filter: "Miet", "WEG", "Immobilien" → Embed → Qdrant

# BFH (Täglich)
scrape_bfh_rulings() → Filter: "AfA", "Grundsteuer", "Vermietung" → Embed → Qdrant

# Gesetze (Wöchentlich)
scrape_gesetze_im_internet(["bgb", "weg", "baugb", "grstg"]) → Embed → Qdrant
```

### US-Quellen
```python
# CourtListener API (Stündlich)
scrape_courtlistener(jurisdictions=["fl", "ny", "ca", "tx", "nv"]) → Embed → Qdrant

# State Statutes (Wöchentlich)
scrape_state_codes() → Embed → Qdrant
```

### EU-Quellen
```python
# EUR-Lex (Wöchentlich)
scrape_eur_lex(topics=["real_estate", "consumer_protection"]) → Embed → Qdrant

# EuGH (Wöchentlich)
scrape_curia_eu() → Embed → Qdrant
```

### Dubai-Quellen
```python
# RERA (Täglich)
scrape_rera_regulations() → Translate (AR→EN) → Embed → Qdrant

# Dubai Courts (Wöchentlich)
scrape_dubai_courts() → Translate → Embed → Qdrant
```

---

## 🗂️ **Datenbank-Struktur**

### Qdrant Collections
```
legal_documents (Main Collection)
├── Payload Schema:
│   ├── jurisdiction: "DE" | "EU" | "US" | "ES" | "AE"
│   ├── sub_jurisdiction: "Bayern" | "Florida" | "Cataluña" | "Dubai"
│   ├── source_type: "statute" | "case_law" | "regulation" | "municipal"
│   ├── court: "BGH" | "BFH" | "Supreme Court" | "EuGH" | "Dubai Courts"
│   ├── legal_area: "mietrecht" | "tax" | "baurecht" | "ejari"
│   ├── language: "de" | "en" | "es" | "ar"
│   ├── content: "Full text..."
│   ├── topics: ["Mietminderung", "Security Deposit", "IBI"]
│   └── last_updated: "2025-12-27T..."
```

---

## 🌐 **UI-Erweiterung für Dubai**

### Frontend-Änderungen
```typescript
// Jurisdictions erweitern
export enum Jurisdiction {
  DE = "DE",  // Deutschland
  EU = "EU",  // Europäische Union
  US = "US",  // United States
  ES = "ES",  // Spanien
  AE = "AE",  // UAE/Dubai (NEU!)
}

// Sub-Jurisdictions
export const SUB_JURISDICTIONS = {
  DE: ["Bayern", "NRW", "Berlin", "Hamburg", ...],
  US: ["Florida", "New York", "California", "Texas", "Nevada"],
  ES: ["Cataluña", "Madrid", "Andalucía", "Valencia"],
  AE: ["Dubai", "Abu Dhabi", "Sharjah"],  // NEU!
}
```

### Flaggen & Labels
```tsx
<Flag 
  code="AE" 
  label="Dubai/UAE"
  icon="🇦🇪"
/>

// Sprach-Unterstützung
const LANGUAGES = {
  de: "Deutsch",
  en: "English", 
  es: "Español",
  ar: "العربية"  // Arabisch für Dubai (optional)
}
```

---

## 📈 **Skalierungs-Strategie**

### Kosten-Schätzung (Gemini Embeddings)
| Phase | Dokumente | Tokens (ca.) | Kosten @ $0.025/1M |
|-------|-----------|--------------|---------------------|
| Phase 1 | 100 | 500K | $0.01 |
| Phase 2 | 5,000 | 25M | $0.63 |
| Phase 3-7 | 50,000 | 250M | $6.25 |
| **Total** | **~55,000** | **~275M** | **~$7** |

### Qdrant Cloud Storage
- Free Tier: 1GB (ca. 10,000 Dokumente)
- Paid Tier: $25/Monat für 100GB (1M+ Dokumente)

### Cloud Run Kosten
- Backend: ~$10-20/Monat (bei 1000 Requests/Tag)
- Cloud Scheduler: $0.10/Job/Monat × 20 Jobs = $2/Monat

**TOTAL MONTHLY: ~$27-47/Monat**

---

## ✅ **Nächste Schritte**

1. **Sofort:** BFH + BGH Scraper implementieren
2. **Diese Woche:** Florida + LAU Scraper
3. **Nächste Woche:** Dubai/RERA Integration
4. **Danach:** EU-Recht (EuGH + Verordnungen)

**Soll ich mit Phase 2 (BGH/BFH Rechtsprechung) anfangen?**
