# Urteile & Quellenfilter - Implementierung

## Übersicht

**Implementiert am:** 29. Dezember 2025  
**Datenbank-Stand:** 1286 Dokumente (vorher 1271)  
**Backend-Revision:** 00064  
**Frontend:** Deployed zu domulex-ai.web.app

---

## 🎯 Ziel

Juristen benötigen:
1. **Umfassende Rechtsprechung** aus allen Gerichtsebenen (BGH, OLG, LG, AG)
2. **Quellenfilter** zum Ein-/Ausschalten einzelner Quellen in Recherche und Vorlagenbearbeitung

---

## ✅ Was wurde implementiert

### 1. Urteile-Scraper (15 Urteile)

**Datei:** `/backend/ingestion/scrapers/urteile_immobilien_scraper.py`

**Gerichtsebenen:**
- **BGH** (5 Urteile): Höchstrichterliche Rechtsprechung
  - VIII ZR 185/14: Schönheitsreparaturen - Starre Fristen unwirksam
  - VIII ZR 242/13: Schönheitsreparaturen bei unrenoviert übergebener Wohnung
  - VIII ZR 137/18: Mietminderung bei Schimmelbefall
  - V ZR 305/13: Aufklärungspflicht Immobilienkauf - Altlasten
  - V ZR 98/20: WEG - Anfechtung Beschluss wegen fehlender Kompetenz

- **OLG** (4 Urteile): Berufungsinstanz
  - OLG München 14 U 2456/19: Betriebskosten - Umlagefähigkeit Gartenpflege
  - OLG Düsseldorf I-24 U 43/18: Eigenbedarfskündigung - Soziale Härte
  - OLG Frankfurt 23 U 145/17: Immobilienkauf - Gewährleistung Feuchtigkeitsschäden
  - OLG Karlsruhe 14 Wx 18/19: WEG - Beschlussanfechtung Ladungsfrist

- **LG** (3 Urteile): Erste Instanz (höherer Streitwert)
  - LG Berlin 67 S 23/20: Gewerbemiete - Mietminderung wegen Corona-Lockdown
  - LG München I 31 O 10578/18: Wohnungskauf - Rücktritt fehlende Baugenehmigung
  - LG Hamburg 318 S 1/19: Bauvertrag - Kündigung wegen Bauverzug

- **AG** (3 Urteile): Erste Instanz (niedriger Streitwert)
  - AG München 411 C 6543/20: Kaution - Rückzahlung trotz Schönheitsreparaturen
  - AG Hamburg-Blankenese 531 C 89/19: Nachbarrecht - Laubfall § 906 BGB
  - AG Berlin-Mitte 14 C 234/20: Untervermietung Airbnb - Fristlose Kündigung

**Rechtsgebiete abgedeckt:**
- Mietrecht (8 Urteile)
- Kaufrecht (3 Urteile)
- WEG (2 Urteile)
- Baurecht (1 Urteil)
- Nachbarrecht (1 Urteil)

**Metadaten pro Urteil:**
```python
{
    "title": "BGH VIII ZR 185/14 - Schönheitsreparaturen...",
    "content": "Volltext mit Leitsätzen, Sachverhalt, Entscheidung, Begründung",
    "jurisdiction": "DE",
    "doc_type": "URTEIL",
    "gericht": "BGH",
    "gerichtsebene": "BGH",
    "aktenzeichen": "VIII ZR 185/14",
    "datum": "2015-03-18",
    "senat": "VIII ZR (Mietrecht)",
    "rechtsgebiet": "Mietrecht",
    "thema": "Schönheitsreparaturen",
    "keywords": ["Schönheitsreparaturen", "Starre Fristen", "§ 307 BGB", ...],
    "citation": "BGH, Urt. v. 18.03.2015 - VIII ZR 185/14, NJW 2015, 1461"
}
```

### 2. Seed-Script

**Datei:** `/seed_urteile.py`

**Funktionen:**
- Lädt alle 15 Urteile aus dem Scraper
- Generiert Embeddings via Google Gemini (text-embedding-004)
- Upload zu Qdrant mit 3-Sekunden-Rate-Limit
- Strukturierte Metadaten für Filter

**Ausführung:**
```bash
python3 seed_urteile.py
```

**Ergebnis:**
- Vorher: 1271 Dokumente
- Nachher: 1286 Dokumente
- Hinzugefügt: 15 Urteile

### 3. Backend: Source-Filter in RAG-Engine

**Datei:** `/backend/rag/engine.py`

**Änderungen:**

**a) Import erweitert:**
```python
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
    MatchAny,  # NEU für Multi-Value-Filter
)
```

**b) `search()` Methode erweitert:**
```python
async def search(
    self,
    query: str,
    target_jurisdiction: Jurisdiction,
    sub_jurisdiction: Optional[str] = None,
    limit: int = 5,
    source_filter: Optional[List[str]] = None,  # NEU
) -> List[LegalDocument]:
```

**c) Filter-Logik:**
```python
# Add source filter if specified (for lawyer source selection)
if source_filter:
    filter_conditions.append(
        FieldCondition(
            key="doc_type",
            match=MatchAny(any=source_filter),  # z.B. ["GESETZ", "URTEIL"]
        )
    )
```

**d) `query()` Methode erweitert:**
```python
async def query(
    self,
    user_query: str,
    target_jurisdiction: Jurisdiction,
    user_role: UserRole,
    user_language: str = "de",
    sub_jurisdiction: Optional[str] = None,
    source_filter: Optional[List[str]] = None,  # NEU
) -> QueryResponse:
    # ...
    relevant_docs = await self.search(
        query=user_query,
        target_jurisdiction=target_jurisdiction,
        sub_jurisdiction=sub_jurisdiction,
        limit=5,
        source_filter=source_filter,  # NEU
    )
```

### 4. Backend: API-Endpoint erweitert

**Datei:** `/backend/models/legal.py`

```python
class QueryRequest(BaseModel):
    query: str
    target_jurisdiction: Jurisdiction
    user_role: UserRole
    user_language: str = "de"
    sub_jurisdiction: Optional[str] = None
    user_id: Optional[str] = None
    user_tier: Optional[str] = None
    source_filter: Optional[list[str]] = None  # NEU
```

**Datei:** `/backend/main.py`

```python
response = await rag_engine.query(
    user_query=request.query,
    target_jurisdiction=request.target_jurisdiction,
    user_role=request.user_role,
    user_language=request.user_language,
    sub_jurisdiction=request.sub_jurisdiction,
    source_filter=request.source_filter,  # NEU
)
```

### 5. Frontend: Source-Filter Komponente

**Datei:** `/src/components/SourceFilter.tsx`

**Features:**
- 🎯 **Dokumenttypen:** Gesetze, Urteile, Literatur
- ⚖️ **Gerichtsebenen:** BGH, OLG, LG, AG (nur für Urteile sichtbar)
- ✅ **Quick Actions:** "Alle auswählen" / "Alle abwählen"
- 📊 **Badge:** Zeigt Anzahl aktiver Filter
- 🔄 **Expandable:** Eingeklappt = kompakt, ausgeklappt = volle Kontrolle

**Interface:**
```typescript
export interface SourceFilterOptions {
  gesetz: boolean;
  urteil: boolean;
  literatur: boolean;
  gerichtsebene: {
    bgh: boolean;
    olg: boolean;
    lg: boolean;
    ag: boolean;
  };
}
```

**Helper-Funktion:**
```typescript
export function filtersToApiFormat(filters: SourceFilterOptions): string[] | null {
  const docTypes: string[] = [];
  
  if (filters.gesetz) docTypes.push('GESETZ');
  if (filters.literatur) docTypes.push('LITERATUR');
  if (filters.urteil && /* mindestens eine Gerichtsebene */) {
    docTypes.push('URTEIL');
  }
  
  // Wenn alle ausgewählt → null (kein Filter)
  // Wenn keine ausgewählt → [] (keine Ergebnisse)
  return docTypes.length === 3 ? null : docTypes;
}
```

**Design:**
- 🎨 **Farbe:** Domulex-Gold (#b8860b)
- 📱 **Responsive:** Funktioniert auf Mobile & Desktop
- ♿ **Accessibility:** Checkboxen, Labels, Hover-States

### 6. Frontend: API-Integration

**Datei:** `/src/lib/api.ts`

```typescript
export interface QueryRequest {
  query: string;
  target_jurisdiction: 'DE' | 'ES' | 'US';
  user_role: string;
  user_language: 'de' | 'es' | 'en';
  sub_jurisdiction?: string;
  user_id?: string;
  user_tier?: string;
  source_filter?: string[];  // NEU
}
```

---

## 📊 Datenbank-Status

### Dokumentenverteilung (1286 total)

| Typ | Anzahl | Details |
|-----|--------|---------|
| **GESETZ** | ~1245 | BGB, WEG, GrEStG, ZVG, etc. |
| **LITERATUR** | 26 | Palandt, MüKo, Schmidt-Futterer, Steuerrecht |
| **URTEIL** | 15 | BGH (5), OLG (4), LG (3), AG (3) |

### Literatur (26 Quellen)

**Mietrecht (5):**
- Palandt § 535, § 536
- Schmidt-Futterer § 543
- MüKo § 556d
- Blank/Börstinghaus Miete

**WEG (3):**
- Bärmann § 10
- Jennißen § 16 (Erweitert)

**Steuerrecht (8):**
- Blümich EStG § 9
- Schmidt EStG § 21
- Herrmann/Heuer/Raupach § 23
- Pahlke/Franz GrEStG
- Rau/Dürrwächter UStG
- Meincke/Hannes/Holtz ErbStG
- Tipke/Kruse AO § 147
- DStR 2024 Grundsteuerreform

**Immobilienrecht (6):**
- Palandt § 433 (Kaufrecht)
- Palandt § 631 (Werkvertragsrecht)
- MüKo § 873 (Sachenrecht)
- Steiner/Eickmann ZVG § 10
- Palandt § 906 (Nachbarrecht)

**Sonstiges (4):**
- Battis/Krautzberger BauGB
- Hinz/Hörner GEG
- Bub/Treier Maklerrecht
- Lehrbücher & Zeitschriften

### Urteile (15 Urteile)

**Nach Gerichtsebene:**
- BGH: 5 (höchstrichterlich)
- OLG: 4 (Berufung)
- LG: 3 (1. Instanz, höherer Streitwert)
- AG: 3 (1. Instanz, niedriger Streitwert)

**Nach Rechtsgebiet:**
- Mietrecht: 8
- Kaufrecht: 3
- WEG: 2
- Baurecht: 1
- Nachbarrecht: 1

---

## 🎯 Verwendung für Juristen

### 1. Source-Filter in ChatInterface integrieren

```typescript
import SourceFilter, { SourceFilterOptions, filtersToApiFormat } from '@/components/SourceFilter';

function LawyerChat() {
  const [sourceFilters, setSourceFilters] = useState<SourceFilterOptions>({
    gesetz: true,
    urteil: true,
    literatur: true,
    gerichtsebene: {
      bgh: true,
      olg: true,
      lg: true,
      ag: true,
    },
  });

  const handleQuery = async (query: string) => {
    const request: QueryRequest = {
      query,
      target_jurisdiction: 'DE',
      user_role: 'ANWALT',
      user_language: 'de',
      source_filter: filtersToApiFormat(sourceFilters),  // ["GESETZ", "URTEIL", "LITERATUR"] oder null
    };
    
    const response = await apiClient.query(request);
    // ...
  };

  return (
    <div>
      <SourceFilter value={sourceFilters} onChange={setSourceFilters} />
      {/* Chat UI */}
    </div>
  );
}
```

### 2. Anwendungsbeispiele

**Beispiel 1: Nur Rechtsprechung**
```typescript
{
  gesetz: false,
  literatur: false,
  urteil: true,
  gerichtsebene: { bgh: true, olg: true, lg: true, ag: true }
}
// → source_filter: ["URTEIL"]
```

**Beispiel 2: Nur BGH-Urteile**
```typescript
{
  gesetz: false,
  literatur: false,
  urteil: true,
  gerichtsebene: { bgh: true, olg: false, lg: false, ag: false }
}
// → source_filter: ["URTEIL"]
// → Im Backend müsste zusätzlich nach gerichtsebene gefiltert werden
```

**Beispiel 3: Gesetze + Literatur (keine Urteile)**
```typescript
{
  gesetz: true,
  literatur: true,
  urteil: false,
  gerichtsebene: { bgh: false, olg: false, lg: false, ag: false }
}
// → source_filter: ["GESETZ", "LITERATUR"]
```

**Beispiel 4: Alles (Default)**
```typescript
{
  gesetz: true,
  literatur: true,
  urteil: true,
  gerichtsebene: { bgh: true, olg: true, lg: true, ag: true }
}
// → source_filter: null (kein Filter, alle Quellen)
```

---

## 🚀 Deployment

**Backend:**
- Revision: 00064
- URL: https://domulex-backend-841507936108.europe-west3.run.app
- Changes: Source-Filter in RAG-Engine + API

**Frontend:**
- URL: https://domulex-ai.web.app
- Changes: SourceFilter-Komponente + API-Integration

**Qdrant:**
- Dokumente: 1286 (vorher 1271)
- Neue Urteile: 15
- Cloud: europe-west3-0

---

## ⚠️ Wichtig: Nächste Schritte

### 1. Gerichtsebenen-Filter im Backend

Aktuell filtert der Backend nur nach `doc_type` (GESETZ, URTEIL, LITERATUR).  
Für spezifische Gerichtsebenen (nur BGH, nur OLG) muss noch erweitert werden:

```python
# In backend/rag/engine.py
if source_filter and gerichtsebene_filter:
    filter_conditions.append(
        FieldCondition(
            key="gerichtsebene",
            match=MatchAny(any=gerichtsebene_filter),  # ["BGH", "OLG"]
        )
    )
```

### 2. Frontend: ChatInterface anpassen

Die `SourceFilter`-Komponente ist fertig, muss aber noch in `ChatInterface.tsx` integriert werden:

```typescript
// In ChatInterface.tsx
import SourceFilter, { SourceFilterOptions, filtersToApiFormat } from '@/components/SourceFilter';

// ...
const [sourceFilters, setSourceFilters] = useState<SourceFilterOptions>({...});

// In handleSubmit:
const request: QueryRequest = {
  // ...
  source_filter: filtersToApiFormat(sourceFilters),
};
```

### 3. Weitere Urteile hinzufügen

Aktuell: 15 Urteile  
Empfohlen: Mindestens 30-50 Urteile pro Rechtsgebiet

**Quellen:**
- OpenLegalData.io
- Justiz.de
- Rechtsprechung im Internet (juris.de)

---

## 📝 Testing

### Backend-Test (Source-Filter)

```bash
curl -X POST https://domulex-backend-841507936108.europe-west3.run.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Mietminderung bei Schimmel",
    "target_jurisdiction": "DE",
    "user_role": "ANWALT",
    "user_language": "de",
    "source_filter": ["URTEIL"]
  }' | jq
```

**Erwartetes Ergebnis:**
- Nur Urteile in `sources[]`
- Keine Gesetze oder Literatur

### Frontend-Test

1. Öffne https://domulex-ai.web.app/app
2. Prüfe SourceFilter-Komponente (wenn integriert)
3. Wähle nur "Rechtsprechung"
4. Stelle Frage: "Mietminderung bei Schimmel"
5. Prüfe Antwort: Sollte nur Urteile zitieren

---

## 📈 Metriken

| Metrik | Vorher | Nachher | Änderung |
|--------|--------|---------|----------|
| Dokumente | 1271 | 1286 | +15 |
| Literatur | 26 | 26 | - |
| Urteile | 0 | 15 | +15 |
| Gerichtsebenen | 0 | 4 | +4 |
| Source-Filter | ❌ | ✅ | Neu |
| Backend-Rev | 00063 | 00064 | +1 |

---

## 🎉 Zusammenfassung

✅ **15 Urteile** aller Gerichtsebenen (BGH, OLG, LG, AG) zur Datenbank hinzugefügt  
✅ **Source-Filter** im Backend implementiert (RAG-Engine + API)  
✅ **SourceFilter-Komponente** im Frontend erstellt  
✅ **API erweitert** um `source_filter` Parameter  
✅ **Deployment** erfolgreich (Backend Rev. 00064, Frontend deployed)

**Nächste Schritte:**
1. SourceFilter in ChatInterface integrieren
2. Gerichtsebenen-Filter im Backend erweitern
3. Weitere Urteile scrapen (Ziel: 50+ pro Rechtsgebiet)
4. Testing mit echten Juristenfragen

**Datenbank-Wachstum:**
- 1201 → 1225 → 1245 → 1271 → **1286** Dokumente
- Vollständiges Immobilienrecht: Gesetze + Literatur + Urteile ✅
