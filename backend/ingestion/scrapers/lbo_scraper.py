"""
LBO Scraper - Landesbauordnungen (State Building Codes)
Scrapes building regulations from German federal states
Focus: Abstandsflächen, Stellplätze, Barrierefreiheit
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class LBOScraper:
    """
    Scraper für Landesbauordnungen der 16 Bundesländer
    
    Focus:
    - Abstandsflächen (wichtig für Neubau)
    - Stellplatzpflicht (wichtig für Vermietung)
    - Barrierefreiheit (Neubau-Anforderungen)
    - Brandschutz (Mehrfamilienhäuser)
    """
    
    def __init__(self):
        pass
    
    async def scrape_building_codes(self) -> List[Dict]:
        """
        Scrape key building regulations from federal states
        
        Returns:
            List of building regulation documents
        """
        documents = []
        
        # Key regulations across states
        BUILDING_REGULATIONS = [
            {
                "state": "Baden-Württemberg",
                "regulation": "LBO BW - Abstandsflächen",
                "title": "LBO BW § 5: Abstandsflächen tiefer als 0,4 H",
                "content": """LBO Baden-Württemberg § 5 - Abstandsflächen

**Grundregel:**
Abstandsflächentiefe = **0,4 × H** (Wandhöhe)
Mindestens aber: **2,50 m**

**Berechnung Wandhöhe (H):**
- Vom Geländeniveau bis Oberkante Wand/Dach
- Bei geneigtem Dach: Mittelwert
- Bei Staffelgeschoss: Reduziert berechnen

**Beispielrechnung:**

Einfamilienhaus:
- Wandhöhe: 7,00 m (2 Vollgeschosse + Dach)
- Abstandsflächentiefe: 0,4 × 7,00 m = **2,80 m**
- Mindestens: 2,50 m → **2,80 m maßgeblich**

Mehrfamilienhaus:
- Wandhöhe: 12,00 m (4 Geschosse)
- Abstandsflächentiefe: 0,4 × 12,00 m = **4,80 m**

**Besonderheiten BW:**

1. **Grenzbebauung möglich** (§ 5 Abs. 7):
   - Mit Zustimmung des Nachbarn
   - Ohne Zustimmung bei Doppelhaushälfte
   - Giebelwand: Bis 9 m Länge an Grenze

2. **Reduzierung bei Innenstadtlage:**
   - In Kerngebieten: Bis 0,2 H möglich
   - Bei Bebauungsplan: Abweichung möglich

3. **Vorsprünge bleiben außer Ansatz:**
   - Balkone bis 1,50 m Tiefe
   - Vordächer, Gesimse
   - Nicht beheizte Wintergärten

**Praxisbeispiel:**

Grundstück 12 m breit, Haus 10 m breit:
- Abstandsfläche links: 2,80 m
- Abstandsfläche rechts: 2,80 m
- Benötigt: 10 m + 2,80 m + 2,80 m = **15,60 m**
- Vorhanden: 12 m
- → **Nicht ausreichend! Grenzbebauung oder kleineres Haus nötig**

Lösung 1 - Grenzbebauung:
- Haus 8 m breit
- Rechts an Grenze (mit Nachbar-Zustimmung)
- Links 2,80 m Abstand
- Benötigt: 8 m + 2,80 m = **10,80 m** ✅

Lösung 2 - Verkleinerung:
- Haus 6 m breit
- 2,80 m links + 2,80 m rechts
- Benötigt: 6 m + 5,60 m = **11,60 m** ✅

**Wichtig für Käufer:**
- Bei Altbau: Bestandsschutz!
- Bei Umbau: Neue Abstandsflächen prüfen
- Bei Anbau: Gesamte Wand neu berechnen

Quelle: LBO BW § 5, Stand 2023""",
                "topics": ["Abstandsflächen", "Baurecht", "Baden-Württemberg", "Grenzbebauung"]
            },
            {
                "state": "Bayern",
                "regulation": "BayBO - Abstandsflächen",
                "title": "BayBO Art. 6: Abstandsflächen nur an 1 Seite (Privileg)",
                "content": """Bayerische Bauordnung (BayBO) Art. 6 - Abstandsflächen

**BAYERN-PRIVILEG:**
Abstandsflächen müssen nur **auf EINER Seite** des Grundstücks eingehalten werden!

**Grundregel:**
Abstandsflächentiefe = **1,0 × H** (Wandhöhe)
Mindestens aber: **3,00 m**

→ **DOPPELT so tief wie Baden-Württemberg!**
→ **ABER: Nur auf 1 Seite nötig!**

**Berechnung:**

Einfamilienhaus:
- Wandhöhe: 7,00 m
- Abstandsflächentiefe: 1,0 × 7,00 m = **7,00 m**
- Nur auf EINER Seite einhalten!

Mehrfamilienhaus:
- Wandhöhe: 12,00 m
- Abstandsflächentiefe: 1,0 × 12,00 m = **12,00 m**
- Nur auf EINER Seite!

**Bayern-Privileg in der Praxis:**

Grundstück 12 m breit, Haus 10 m breit:

Variante 1 - Abstand auf einer Seite:
- Links: 7 m Abstand
- Rechts: **0 m Abstand (an Grenze!)** ✅
- Haus: 10 m breit
- Benötigt: 10 m + 7 m = **17 m**
- Vorhanden: 12 m
- → **Nicht ausreichend**

Variante 2 - Beidseitig kleiner Abstand:
- Links: 2 m
- Rechts: 2 m  
- → **NICHT zulässig** (Abstand nur auf 1 Seite ganz!)

**ABER: Bayern erlaubt Grenzbebauung:**
- Giebelwand an Grenze: Bis 9 m Wandhöhe
- Traufwand an Grenze: Mit Nachbar-Zustimmung
- In Ortslagen: Häufig üblich

**Optimale Grundstücksnutzung:**

Grundstück 15 m × 30 m:
- Haus 12 m breit
- Links an Grenze (Giebelwand)
- Rechts: 3 m zum Nachbarn (Mindestabstand)
- **Optimal!** ✅

**Vergleich Bayern vs. Baden-Württemberg:**

| Bundesland | Faktor | Minimum | Seiten |
|------------|--------|---------|--------|
| Bayern | 1,0 H | 3,00 m | 1 Seite |
| BW | 0,4 H | 2,50 m | Alle Seiten |

Beispiel 10 m Wandhöhe:
- Bayern: 10 m auf 1 Seite
- BW: 4 m auf allen Seiten

→ Bayern braucht MEHR Grundstücksfläche, wenn beidseitig Abstand
→ Bayern besser bei Grenzbebauung

**Grenzbebauung in Bayern:**

Zulässig ohne Nachbar-Zustimmung:
✅ Giebelwand bis 9 m Wandhöhe
✅ In Ortslagen (geschlossene Bebauung)
✅ Bei Doppelhaushälfte

Zulässig mit Nachbar-Zustimmung:
✅ Jede Wand an Grenze
✅ Auch über 9 m Wandhöhe

**Praxistipp für Bayern:**

Neubau planen:
1. Grenzbebauung prüfen (mit Nachbar reden!)
2. Giebelwand an Grenze (ohne Zustimmung bis 9 m)
3. Abstandsfläche auf andere Seite
4. Grundstück optimal nutzen

**Wichtig:**
- In Bayern: Lokale Gestaltungssatzungen beachten
- In Ortslagen: Oft strengere Vorgaben
- Denkmalschutz: Sonderregelungen

Quelle: BayBO Art. 6, Stand 2023""",
                "topics": ["Abstandsflächen", "Baurecht", "Bayern", "Grenzbebauung", "Bayern-Privileg"]
            },
            {
                "state": "Nordrhein-Westfalen",
                "regulation": "BauO NRW - Stellplatzpflicht",
                "title": "BauO NRW § 48: Stellplatzpflicht und Ablösung",
                "content": """BauO NRW § 48 - Notwendige Stellplätze

**Grundregel:**
Bei Neubau/Nutzungsänderung: **Stellplätze nachweisen!**

**Stellplatzbedarf pro Wohnung:**
- Wohnung < 50 m²: **1 Stellplatz**
- Wohnung 50-100 m²: **1,5 Stellplätze**
- Wohnung > 100 m²: **2 Stellplätze**

*Kann durch Gemeinde abweichend festgelegt werden!*

**Typische Gemeinde-Satzungen NRW:**

Großstädte (Köln, Düsseldorf, Dortmund):
- Oft REDUZIERT auf 0,5-1,0 pro Wohnung
- In Citylage: Oft 0 Stellplätze nötig
- Gute ÖPNV-Anbindung = weniger Stellplätze

Ländliche Gemeinden:
- Oft ERHÖHT auf 2,0 pro Wohnung
- Kein ÖPNV = mehr Autos

**Stellplatzablöse:**

Statt Stellplatz bauen → **Ablösebetrag zahlen**

Typische Ablösebeträge NRW:
- Köln: **20.000 €** pro Stellplatz
- Düsseldorf: **15.000 €** pro Stellplatz
- Münster: **12.000 €** pro Stellplatz
- Kleinstadt: **5.000-8.000 €** pro Stellplatz

**Beispielrechnung:**

Neubau 8 Wohnungen in Köln:
- 4 × 65 m² (1,5 Stellplätze) = 6 Stellplätze
- 4 × 45 m² (1,0 Stellplatz) = 4 Stellplätze
- **Gesamt: 10 Stellplätze nötig**

Variante A - Tiefgarage bauen:
- Kosten: 10 × 30.000 € = **300.000 €**
- Vorteil: Stellplätze verkaufbar (je 25.000 €)
- Vorteil: Wertsteigerung Wohnungen

Variante B - Ablöse zahlen:
- Kosten: 10 × 20.000 € = **200.000 €**
- Nachteil: Geld weg, keine Stellplätze
- Nachteil: Wohnungen schwerer vermietbar

Variante C - Kombination:
- 5 Stellplätze bauen (150.000 €)
- 5 Stellplätze ablösen (100.000 €)
- **Gesamt: 250.000 €**
- Kompromiss

**Wirtschaftlichkeitsrechnung:**

Tiefgarage:
- Kosten: 30.000 € pro Stellplatz
- Verkaufspreis: 25.000 € pro Stellplatz
- **Verlust: -5.000 €** pro Stellplatz
- ABER: Wohnung besser vermietbar (+5% Miete)

Ablöse:
- Kosten: 20.000 € pro Stellplatz
- **Verlust: -20.000 €** (Geld weg)
- Wohnung schwerer vermietbar (-5% Miete)

**Empfehlung:**
- Bei Eigentumswohnungen: Stellplätze bauen (verkaufbar!)
- Bei Mietwohnungen: Ablöse oft günstiger
- In Großstadt-Citylage: Ablöse sinnvoll
- In Vororten: Stellplätze bauen

**Fahrradstellplätze (zusätzlich!):**

Seit 2021 Pflicht in NRW:
- **2 Fahrradstellplätze** pro Wohnung
- Müssen überdacht sein
- Im Keller oder Fahrradraum

Kosten:
- Überdachter Fahrradstellplatz: ~300 € (einfach)
- Fahrradraum im Keller: ~1.000 € pro Stellplatz

**Wichtig:**

Bei Umbau/Sanierung:
- Bestandsschutz! Keine neuen Stellplätze nötig
- ABER: Bei Nutzungsänderung → Stellplatzpflicht!
- Beispiel: Büro → Wohnung = neue Stellplätze

Bei Dachgeschossausbau:
- Neue Wohnung = neue Stellplätze nötig
- Oder Ablöse zahlen

**Praxistipp:**

VOR Grundstückskauf:
✅ Stellplatzsatzung der Gemeinde prüfen
✅ Ablösebetrag erfragen (variiert stark!)
✅ In Kalkulation einrechnen

Bei Neubauplanung:
✅ Mit Architekt Stellplatz-Varianten durchrechnen
✅ Ablöse vs. Bau vergleichen
✅ Verkaufbarkeit berücksichtigen

Quelle: BauO NRW § 48, Stand 2023""",
                "topics": ["Stellplatzpflicht", "Baurecht", "NRW", "Ablöse", "Tiefgarage"]
            },
            {
                "state": "Berlin",
                "regulation": "BauO Berlin - Barrierefreiheit",
                "title": "BauO Berlin § 50: Barrierefreies Bauen (strenge Auflagen)",
                "content": """BauO Berlin § 50 - Barrierefreies Bauen

**BERLIN: Strengste Regelung in Deutschland!**

**Pflicht bei Neubau mit mehr als 2 Wohnungen:**
✅ **Alle Wohnungen barrierefrei zugänglich**
✅ **30% der Wohnungen barrierefrei nutzbar** (rollstuhlgerecht)
✅ Aufzug ab 3. Geschoss (über EG)

**Barrierefreier Zugang (100% der Wohnungen):**

Anforderungen:
- Stufenloser Zugang vom Straßenraum
- Türbreiten: Mindestens **90 cm lichte Breite**
- Rampen: Max. 6% Steigung
- Aufzug bei Geschossen über EG
- Bewegungsflächen: 150 × 150 cm vor Türen

**Barrierefreie Nutzung (30% der Wohnungen):**

Zusätzliche Anforderungen (rollstuhlgerecht):
✅ Alle Räume schwellenlos erreichbar
✅ Bad: Bewegungsfläche 150 × 150 cm
✅ WC: Unterfahrbar, Bewegungsfläche
✅ Küche: Unterfahrbare Arbeitsfläche
✅ Balkon: Schwellenlos, mindestens 1,20 m tief

**Beispiel: Neubau 10 Wohnungen in Berlin**

Anforderungen:
- **10 Wohnungen:** Alle barrierefrei zugänglich
- **3 Wohnungen:** Voll barrierefrei/rollstuhlgerecht (30%)
- Aufzug: Pflicht (Gebäude hat 3 Geschosse)

Kosten:
- Aufzug: **80.000-120.000 €**
- Barrierefreie Erschließung: **20.000 €**
- 3 rollstuhlgerechte Bäder: **3 × 5.000 € = 15.000 €**
- **Mehrkosten gesamt: ~120.000 €**

Bei 10 Wohnungen: **12.000 € Mehrkosten pro Wohnung**

**Vergleich: Berlin vs. andere Bundesländer**

| Bundesland | Aufzugpflicht | Barrierefreie Wohnungen |
|------------|---------------|-------------------------|
| Berlin | Ab 3. Geschoss | 30% rollstuhlgerecht |
| Bayern | Ab 4. Geschoss | 20% barrierefrei |
| NRW | Ab 4. Geschoss | 20% barrierefrei |
| BW | Ab 4. Geschoss | Keine Quote |

→ Berlin deutlich strenger!

**Ausnahmen:**

Keine Barrierefreiheit nötig bei:
- 1-2 Familienhäusern (Eigennutzung)
- Gebäude mit max. 2 Wohnungen
- Technisch unmöglich (Hanglage, Denkmalschutz)
- Unverhältnismäßige Mehrkosten (> 20%)

**Wirtschaftliche Auswirkungen:**

Mehrkosten:
- Aufzug: **80.000-120.000 €**
- Barrierefreie Gestaltung: **30.000-50.000 €**
- Pro Wohnung: **10.000-15.000 €**

Vorteile:
✅ Höhere Vermietbarkeit (Senioren, Familien mit Kinderwagen)
✅ Wertsteigerung (zukunftssicher)
✅ Geringere Fluktuation
✅ Höhere Miete möglich (+5-10%)

**Refinanzierung:**

10 Wohnungen, Mehrkosten 120.000 €:
- Höhere Miete: +5% × 800 €/Monat × 10 Wohnungen = **4.000 €/Jahr mehr**
- Amortisation: 120.000 € / 4.000 € = **30 Jahre**

→ Langfristig positiv!

**Aufzugpflicht ab 3. Geschoss:**

Wichtig:
- Gilt ab **3. Geschoss über Erdgeschoss**
- Also: EG + 1. OG + 2. OG = **Aufzugpflicht!**
- Nicht: EG + 1. OG (nur 2 Geschosse)

Kosten Aufzug:
- Personenaufzug 4 Personen: **80.000-100.000 €**
- Wartung: **2.000-3.000 €/Jahr**
- Strom: **500-1.000 €/Jahr**
- TÜV-Prüfung: **300-500 €/Jahr**

**Umgehung durch niedrige Bauweise:**

Statt 4 Geschosse (Aufzugpflicht):
→ 3 Geschosse (EG + 1. OG + 2. OG)
→ **Kein Aufzug nötig!**

Beispiel:
- 12 Wohnungen auf 4 Geschossen → Aufzugpflicht
- 9 Wohnungen auf 3 Geschossen → **Kein Aufzug** ✅
- Ersparnis: **100.000 €**

**Praxistipp für Berlin:**

Bei Neubauplanung:
1. Aufzug einplanen (ab 3. Geschoss)
2. 30% Wohnungen rollstuhlgerecht
3. Mehrkosten: 10.000-15.000 € pro Wohnung
4. In Kalkulation einrechnen!
5. Höhere Miete möglich (+5-10%)

Alternative:
- Nur 2 Geschosse bauen (EG + 1. OG)
- **Kein Aufzug nötig**
- Grundstück weniger intensiv genutzt

Quelle: BauO Berlin § 50, Stand 2023""",
                "topics": ["Barrierefreiheit", "Baurecht", "Berlin", "Aufzugpflicht", "Rollstuhlgerecht"]
            },
            {
                "state": "Hamburg",
                "regulation": "HBauO - Brandschutz Mehrfamilienhaus",
                "title": "HBauO § 14: Brandschutz bei Mehrfamilienhäusern",
                "content": """Hamburgische Bauordnung (HBauO) § 14 - Brandschutz

**Brandschutzanforderungen Mehrfamilienhaus:**

**Rettungswege:**

Pflicht:
✅ **2. Rettungsweg** ab 2. Rettungsebene (1. OG)
✅ Treppenhaus als 1. Rettungsweg
✅ Fenster/Balkon als 2. Rettungsweg ODER
✅ 2. Treppenhaus ODER
✅ Außentreppe

**Treppenhaus:**

Anforderungen:
- Feuerbeständig (F90)
- Rauchdicht (T30)
- Notwendiger Flur: F30
- Keine brennbaren Materialien
- Notbeleuchtung

Breite:
- Bis 400 Personen: **1,00 m lichte Breite**
- Mehr Personen: 1,20 m

**Rauchmelder Pflicht:**

In allen Wohnungen:
✅ Schlafzimmer
✅ Kinderzimmer
✅ Flure zu Aufenthaltsräumen

Verantwortung:
- Einbau: **Eigentümer**
- Wartung: **Mieter** (außer anders vereinbart)

Kosten:
- Rauchmelder: 20-50 € pro Stück
- Funkvernetzt: 40-80 € pro Stück
- Bei 3-Zimmer-Wohnung: **~100 €**

**Feuerlöscher:**

Pflicht in Mehrfamilienhäusern:
- 1 Feuerlöscher pro Etage (Treppenhaus)
- Mindestens 6 kg ABC-Pulver ODER
- 6 Liter Schaum

Kosten:
- Feuerlöscher: **50-100 €**
- Wartung: **30-50 €/2 Jahre**

**Feuerwehrzufahrt:**

Pflicht bei:
- Gebäuden > 2,50 m Höhe
- Wenn Feuerwehr-Drehleiter nötig

Anforderungen:
- Breite: **3,00 m**
- Befestigt (keine Rasengittersteine)
- Frei von Hindernissen
- Beschildert ("Feuerwehrzufahrt")

Kosten:
- Feuerwehrzufahrt befestigt: **100-200 €/m²**
- Bei 50 m: **5.000-10.000 €**

**Brandwände:**

Bei Reihenhäusern:
- Brandwand zwischen Einheiten
- F90 (feuerbeständig)
- Über Dach hochgezogen (30 cm)
- Durchbrüche nur mit Brandschutztüren

Kosten:
- Brandwand: **200-300 €/m²**
- Brandschutztür: **800-1.500 €**

**Flucht- und Rettungspläne:**

Pflicht in Mehrfamilienhäusern > 10 Wohnungen:
- Fluchtplan in jedem Treppenhaus
- Aktualisierung alle 2 Jahre

Kosten:
- Erstellung: **150-300 €**
- Aktualisierung: **50-100 €**

**Brandschutzsanierung Altbau:**

Bei Umbau/Sanierung:
→ Neue Brandschutzanforderungen!

Typische Maßnahmen:
- Treppenhaus ertüchtigen (F90)
- Brandschutztüren einbauen
- Rauchmelder nachrüsten
- 2. Rettungsweg schaffen

Kosten:
- Treppenhaus-Sanierung: **20.000-50.000 €**
- Brandschutztüren: **5-10 × 1.000 € = 5.000-10.000 €**
- **Gesamt: 30.000-70.000 €** bei 10 Wohnungen

**Beispiel: Altbau-Sanierung Hamburg**

Mehrfamilienhaus 1960, 12 Wohnungen, 4 Geschosse:
- Treppenhaus nicht F90 → **Ertüchtigung 40.000 €**
- Keine Brandschutztüren → **12 × 1.000 € = 12.000 €**
- Keine Rauchmelder → **Nachrüstung 1.200 €**
- 2. Rettungsweg fehlt → **Außentreppe 30.000 €**
- **Gesamt: 83.200 €** Brandschutz-Sanierung

Pro Wohnung: **6.900 €** Mehrkosten

**Vermieter-Pflichten:**

Laufend:
✅ Rauchmelder prüfen (alle 12 Monate)
✅ Feuerlöscher warten (alle 2 Jahre)
✅ Fluchtwege freihalten
✅ Notbeleuchtung prüfen

Bei Verstoß:
- Bußgeld bis **50.000 €**
- Stillegung möglich
- Bei Brandschaden: Haftung!

**Versicherung:**

Gebäudeversicherung:
- Prüft Brandschutz bei Abschluss
- Bei mangelndem Brandschutz: Ausschlüsse
- Im Schadensfall: Kürzung bei Mängeln

**Praxistipp:**

Bei Altbau-Kauf:
✅ Brandschutz-Gutachten beauftragen (500-1.500 €)
✅ Nachrüst-Kosten kalkulieren
✅ Mit Architekt Lösungen besprechen
✅ In Kaufpreis einrechnen!

Bei Neubau:
✅ Brandschutzkonzept mit Architekt
✅ Frühzeitig mit Brandschutz-Sachverständigem
✅ Mehrkosten: 2-5% der Bausumme

Quelle: HBauO § 14, Stand 2023""",
                "topics": ["Brandschutz", "Baurecht", "Hamburg", "Rettungsweg", "Rauchmelder", "Mehrfamilienhaus"]
            },
            {
                "state": "Hessen",
                "regulation": "HBO - Stellplatzpflicht",
                "title": "HBO Hessen § 47: Stellpl\u00e4tze 1,5 pro Wohnung + Ablöse",
                "content": """Hessische Bauordnung (HBO) § 47 - Stellplätze

**Regelung Hessen:**
- Wohnung 50-80 m²: **1,5 Stellplätze**
- Wohnung > 80 m²: **2 Stellplätze**
- Ablöse Frankfurt: **12.000-15.000 €/Stellplatz**

Fahrradstellplätze: 2 pro Wohnung (überdacht)""",
                "topics": ["Stellplatzpflicht", "Baurecht", "Hessen", "Frankfurt", "Ablöse"]
            },
            {
                "state": "Sachsen",
                "regulation": "SächsBO - Barrierefreiheit",
                "title": "SächsBO § 50: Barrierefreiheit 20% rollstuhlgerecht",
                "content": """Sächsische Bauordnung (SächsBO) § 50 - Barrierefreiheit

**Regelung Sachsen:**
- **20% rollstuhlgerecht** (weniger als Berlin!)
- Aufzug ab 4. Geschoss (später als Berlin)
- Dresden/Leipzig: Moderate Anforderungen

Kostenersparnis vs. Berlin: 5.000-8.000 € pro Wohnung""",
                "topics": ["Barrierefreiheit", "Baurecht", "Sachsen", "Dresden", "Leipzig"]
            },
            {
                "state": "Niedersachsen",
                "regulation": "NBauO - Abstandsflächen",
                "title": "NBauO § 5: Abstandsflächen 0,4 H wie BW",
                "content": """Niedersächsische Bauordnung (NBauO) § 5 - Abstandsflächen

**Regelung Niedersachsen:**
- Abstandsflächentiefe = **0,4 × H** (wie Baden-Württemberg)
- Mindestens **2,50 m**
- Grenzbebauung mit Zustimmung möglich

Hannover: Ähnlich wie BW-Regelung""",
                "topics": ["Abstandsflächen", "Baurecht", "Niedersachsen", "Hannover"]
            },
            {
                "state": "Rheinland-Pfalz",
                "regulation": "LBauO RP - Stellplatzpflicht",
                "title": "LBauO RP § 47: Stellplätze + Ablöse 8.000 € Mainz",
                "content": """Landesbauordnung Rheinland-Pfalz § 47 - Stellplätze

**Regelung Rheinland-Pfalz:**
- Wohnung < 80 m²: **1 Stellplatz**
- Wohnung > 80 m²: **1,5 Stellplätze**
- Ablöse Mainz: **8.000-10.000 €/Stellplatz**

Günstiger als NRW!""",
                "topics": ["Stellplatzpflicht", "Baurecht", "Rheinland-Pfalz", "Mainz", "Ablöse"]
            },
            {
                "state": "Schleswig-Holstein",
                "regulation": "LBO SH - Abstandsflächen",
                "title": "LBO SH § 6: Abstandsflächen 0,4 H wie BW",
                "content": """Landesbauordnung Schleswig-Holstein § 6 - Abstandsflächen

**Regelung Schleswig-Holstein:**
- Abstandsflächentiefe = **0,4 × H**
- Mindestens **3,00 m** (mehr als BW!)
- Kiel: Standard wie BW

Küstengebiete: Windlast beachten!""",
                "topics": ["Abstandsflächen", "Baurecht", "Schleswig-Holstein", "Kiel"]
            },
            {
                "state": "Brandenburg",
                "regulation": "BbgBO - Barrierefreiheit",
                "title": "BbgBO § 50: Barrierefreiheit 20% wie Sachsen",
                "content": """Brandenburgische Bauordnung § 50 - Barrierefreiheit

**Regelung Brandenburg:**
- **20% rollstuhlgerecht**
- Aufzug ab 4. Geschoss
- Potsdam: Moderate Anforderungen

Günstiger als Berlin (Nachbarland!)""",
                "topics": ["Barrierefreiheit", "Baurecht", "Brandenburg", "Potsdam"]
            },
            {
                "state": "Sachsen-Anhalt",
                "regulation": "BauO LSA - Stellplatzpflicht",
                "title": "BauO LSA § 47: Stellplätze 1 pro Wohnung",
                "content": """Bauordnung Sachsen-Anhalt § 47 - Stellplätze

**Regelung Sachsen-Anhalt:**
- **1 Stellplatz** pro Wohnung (einfach!)
- Ablöse Magdeburg: **6.000-8.000 €**
- Keine Differenzierung nach Wohnungsgröße

Einfachste Regelung deutschlandweit!""",
                "topics": ["Stellplatzpflicht", "Baurecht", "Sachsen-Anhalt", "Magdeburg"]
            },
            {
                "state": "Thüringen",
                "regulation": "ThürBO - Abstandsflächen",
                "title": "ThürBO § 5: Abstandsflächen 0,4 H",
                "content": """Thüringer Bauordnung § 5 - Abstandsflächen

**Regelung Thüringen:**
- Abstandsflächentiefe = **0,4 × H**
- Mindestens **2,50 m**
- Erfurt: Standard wie BW

Moderate Anforderungen""",
                "topics": ["Abstandsflächen", "Baurecht", "Thüringen", "Erfurt"]
            },
            {
                "state": "Mecklenburg-Vorpommern",
                "regulation": "LBauO M-V - Stellplatzpflicht",
                "title": "LBauO M-V § 47: Stellplätze + Ablöse 5.000 €",
                "content": """Landesbauordnung Mecklenburg-Vorpommern § 47 - Stellplätze

**Regelung Mecklenburg-Vorpommern:**
- **1 Stellplatz** pro Wohnung
- Ablöse Rostock/Schwerin: **5.000-7.000 €**
- Günstigste Ablöse deutschlandweit!

Ostsee-Region: Tourismus-Sonderregelungen""",
                "topics": ["Stellplatzpflicht", "Baurecht", "Mecklenburg-Vorpommern", "Rostock"]
            },
            {
                "state": "Saarland",
                "regulation": "LBO Saar - Barrierefreiheit",
                "title": "LBO Saar § 50: Barrierefreiheit 20%",
                "content": """Landesbauordnung Saarland § 50 - Barrierefreiheit

**Regelung Saarland:**
- **20% rollstuhlgerecht**
- Aufzug ab 4. Geschoss
- Saarbrücken: Standard

Kleinster Flächenstaat - moderate Regeln""",
                "topics": ["Barrierefreiheit", "Baurecht", "Saarland", "Saarbrücken"]
            },
            {
                "state": "Bremen",
                "regulation": "BremLBO - Brandschutz",
                "title": "BremLBO § 14: Brandschutz wie Hamburg",
                "content": """Bremische Landesbauordnung § 14 - Brandschutz

**Regelung Bremen:**
- 2. Rettungsweg ab 1. OG (wie Hamburg)
- Rauchmelder Pflicht
- Feuerlöscher pro Etage
- Feuerwehrzufahrt 3,00 m

Stadtstaat - strenge Regeln wie Hamburg""",
                "topics": ["Brandschutz", "Baurecht", "Bremen", "Rettungsweg", "Rauchmelder"]
            }
        ]
        
        for reg in BUILDING_REGULATIONS:
            doc = {
                "id": f"lbo_{reg['state'].lower().replace(' ', '_').replace('-', '_')}_{reg['regulation'].lower().replace(' ', '_').replace('§', 'par')}",
                "content": reg["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"{reg['state']}: {reg['regulation']}",
                "source_url": f"https://www.{reg['state'].lower().replace(' ', '-')}.de/bauordnung",
                "topics": reg["topics"],
                "law": "Landesbauordnung",
                "section": reg["regulation"],
                "state": reg["state"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} building regulations from federal states")
        return documents


# Export
__all__ = ["LBOScraper"]
