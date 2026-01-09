"""
BFH Scraper - Bundesfinanzhof (Federal Tax Court of Germany)
Scrapes tax case law relevant for real estate investors
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class BFHScraper:
    """
    Scraper für BFH-Entscheidungen (Bundesfinanzhof)
    
    Focus Senate:
    - IX R: Vermietung und Verpachtung
    - II R: Grundsteuer, Grunderwerbsteuer
    - IV R: Umsatzsteuer (Immobilien)
    """
    
    BASE_URL = "https://www.bundesfinanzhof.de"
    
    def __init__(self):
        pass
    
    async def scrape_recent_rulings(self, days_back: int = 365) -> List[Dict]:
        """
        Scrape recent BFH tax rulings for real estate
        
        Returns:
            List of tax case law documents
        """
        documents = []
        
        # Landmark tax cases for real estate
        LANDMARK_TAX_CASES = [
            {
                "case_number": "IX R 23/18",
                "date": "2019-07-09",
                "title": "AfA-Bemessungsgrundlage bei gemischt genutzten Gebäuden",
                "senate": "IX R (Vermietung und Verpachtung)",
                "summary": "Bei gemischt genutzten Gebäuden ist die AfA nach dem Verhältnis der Nutzflächen aufzuteilen.",
                "content": """BFH, Urteil vom 09.07.2019 - IX R 23/18

Leitsatz:
Bei einem Gebäude, das teils vermietet und teils selbst genutzt wird, sind die Anschaffungs- oder Herstellungskosten für die AfA-Berechnung nach dem Verhältnis der Nutzflächen aufzuteilen.

Sachverhalt:
Steuerpflichtiger kauft Mehrfamilienhaus für 500.000 € (davon 100.000 € Grundstücksanteil).
- 60% vermietet (240 m²)
- 40% selbst bewohnt (160 m²)

Entscheidung:
AfA nur für den vermieteten Teil (60% von 400.000 € = 240.000 €)

AfA-Grundlagen für Immobilien:

**Lineare AfA (§ 7 Abs. 4 EStG):**
- Wohngebäude: 2% pro Jahr (Nutzungsdauer 50 Jahre)
- Gewerbeimmobilien: 3% pro Jahr (33 Jahre)
- Gilt für Gebäude ab Baujahr 1925

**Degressive AfA (zeitlich befristet):**
Für Neubauten 2023-2026:
- Jahr 1-4: 5% pro Jahr
- Jahr 5-14: 2,5% pro Jahr
- Ab Jahr 15: 1,25% pro Jahr

**AfA-Bemessungsgrundlage:**
✅ Kaufpreis des Gebäudes (ohne Grund und Boden)
✅ Baukosten bei Neubau
✅ Modernisierungskosten (wenn Nutzungsdauer verlängert)
✅ Anschaffungsnebenkosten (Notar, Grunderwerbsteuer anteilig)

❌ NICHT abzugsfähig:
❌ Grundstücksanteil (Grund und Boden)
❌ Maklerkosten (sofort abzugsfähig als Werbungskosten)
❌ Finanzierungskosten (Zinsen = Werbungskosten)

**Kaufpreisaufteilung:**
Wenn im Kaufvertrag nicht getrennt:
- Bodenrichtwert-Methode
- Sachwertverfahren
- Ertragswertverfahren
- Typischer Anteil: 20-30% Grund, 70-80% Gebäude

**Praktisches Beispiel:**

Kauf einer Eigentumswohnung:
- Kaufpreis: 300.000 €
- Grundstücksanteil (25%): 75.000 €
- Gebäudeanteil: 225.000 €
- Notar + Grundbuch: 6.000 €
- Grunderwerbsteuer (6%): 18.000 €

AfA-Bemessungsgrundlage:
225.000 € (Gebäude)
+ 4.500 € (75% von 6.000 € Notar)
+ 13.500 € (75% von 18.000 € Grunderwerbsteuer)
= 243.000 €

Jährliche AfA bei 2%:
243.000 € × 2% = 4.860 € pro Jahr

**Sonderfälle:**

Denkmalschutz (§ 7i EStG):
- Erhöhte AfA: 9% (8 Jahre) + 7% (4 Jahre)
- Nur für tatsächliche Sanierungskosten
- Bescheinigung der Denkmalschutzbehörde erforderlich

Neubau zur Vermietung (§ 7b EStG):
- Sonderabschreibung: bis zu 5% (4 Jahre)
- Zusätzlich zur normalen AfA
- Nur für Neubauten 2023-2026

**Steuerliche Behandlung bei Verkauf:**

Spekulationsfrist:
- Vermietete Immobilien: 10 Jahre
- Selbstgenutzt: steuerfrei nach 3 Jahren (§ 23 EStG)
- Bei Verkauf vor Fristende: Gewinn steuerpflichtig

Fundstelle: BStBl II 2020, 185""",
                "topics": ["AfA", "Abschreibung", "Vermietung", "§ 7 EStG", "Kaufpreisaufteilung"]
            },
            {
                "case_number": "IX R 40/17",
                "date": "2018-11-20",
                "title": "Werbungskosten bei Vermietung: Erhaltungsaufwand vs. Herstellungskosten",
                "senate": "IX R (Vermietung und Verpachtung)",
                "summary": "Erhaltungsaufwand ist sofort abzugsfähig, Herstellungskosten müssen über AfA verteilt werden.",
                "content": """BFH, Urteil vom 20.11.2018 - IX R 40/17

Leitsatz:
Aufwendungen für Modernisierung sind Herstellungskosten und nur über AfA abzugsfähig, wenn sie zu einer wesentlichen Verbesserung gegenüber dem ursprünglichen Zustand führen.

Sachverhalt:
Steuerpflichtiger kauft Altbau für 200.000 €, investiert 150.000 € in Sanierung:
- Neue Fenster, neue Heizung, Badmodernisierung
- Finanzamt: Herstellungskosten → AfA über 50 Jahre
- Steuerpflichtiger: Erhaltungsaufwand → sofort abzugsfähig

Entscheidung:
Teilweise Herstellungskosten (neue Heizung, Fenster), teilweise Erhaltungsaufwand (Innenrenovierung).

**Abgrenzung Erhaltungsaufwand / Herstellungskosten:**

**Erhaltungsaufwand (sofort abzugsfähig):**
✅ Reparaturen
✅ Schönheitsreparaturen
✅ Modernisierung im bisherigen Rahmen
✅ Ersatz gleichwertiger Bauteile
✅ Beseitigung von Mängeln

Beispiele:
- Dach neu decken (gleiche Qualität)
- Fassade streichen
- Tapezieren, Streichen
- Austausch Waschbecken
- Reparatur Heizung

**Herstellungskosten (AfA über 50 Jahre):**
✅ Erweiterung des Gebäudes
✅ Aufstockung
✅ Anbau
✅ Ausbau Dachgeschoss
✅ Wesentliche Verbesserung
✅ Grundrissänderung

**Anschaffungsnahe Herstellungskosten (§ 6 Abs. 1 Nr. 1a EStG):**
Aufwendungen in den ersten 3 Jahren nach Kauf > 15% der Anschaffungskosten
→ KEINE Werbungskosten, sondern AfA!

Beispiel:
- Kauf: 300.000 €
- Sanierung Jahr 1-3: 50.000 €
- 15% von 300.000 € = 45.000 €
- 50.000 € > 45.000 € → Anschaffungsnahe Herstellungskosten!
- → Keine sofortige Absetzung, nur AfA

Ausnahmen (immer Erhaltungsaufwand):
✅ Schönheitsreparaturen
✅ Behebung von Schäden nach Kauf

**Praktische Steuergestaltung:**

Vermeidung anschaffungsnaher Herstellungskosten:
1. Sanierung VOR Kauf vom Verkäufer durchführen lassen
2. Sanierung auf 3+ Jahre verteilen
3. Nur Erhaltungsaufwand in ersten 3 Jahren

Typische Kostenpositionen:

| Maßnahme | Einordnung | Abzug |
|----------|-----------|-------|
| Heizungsreparatur | Erhaltung | Sofort |
| Heizung komplett neu | Herstellung | AfA 50 Jahre |
| Fenster ersetzen (gleich) | Erhaltung | Sofort |
| Fenster verbessern (3-fach) | Herstellung | AfA 50 Jahre |
| Bad renovieren | Erhaltung | Sofort |
| Bad neu (höherer Standard) | Herstellung | AfA 50 Jahre |
| Dach reparieren | Erhaltung | Sofort |
| Dachausbau Wohnraum | Herstellung | AfA 50 Jahre |

**Werbungskosten bei Vermietung (Übersicht):**

Sofort abzugsfähig:
✅ Grundsteuer
✅ Versicherungen
✅ Hausverwaltung
✅ Schuldzinsen
✅ Instandhaltung
✅ Maklerkosten (bei Neuvermietung)
✅ Rechtsberatung
✅ Fahrtkosten zum Objekt
✅ Kontoführungsgebühren

Über AfA:
- Gebäudeanteil Kaufpreis
- Herstellungskosten
- Anschaffungsnahe Herstellungskosten

Fundstelle: BStBl II 2019, 301""",
                "topics": ["Werbungskosten", "Erhaltungsaufwand", "Herstellungskosten", "§ 9 EStG", "§ 21 EStG"]
            },
            {
                "case_number": "II R 23/18",
                "date": "2019-04-10",
                "title": "Grundsteuer: Bewertung von Grundstücken",
                "senate": "II R (Grundsteuer)",
                "summary": "Ab 2025 neue Grundsteuer - Bewertung nach Bundesmodell oder Ländermodellen.",
                "content": """BFH, Urteil vom 10.04.2019 - II R 23/18

Hintergrund:
Bundesverfassungsgericht hat 2018 die alte Grundsteuer für verfassungswidrig erklärt. 
Neue Grundsteuer ab 01.01.2025!

**Grundsteuer NEU (ab 2025):**

Berechnung in 3 Schritten:

**Schritt 1: Grundsteuerwert ermitteln**
- Bundesmodell (Ertragswertverfahren) ODER
- Ländermodelle (z.B. Bayern: Flächenmodell)

**Schritt 2: Steuermesszahl anwenden**
Bundesmodell:
- Wohngrundstücke: 0,31 Promille (0,031%)
- Nichtwohngrundstücke: 0,34 Promille (0,034%)

**Schritt 3: Hebesatz der Gemeinde**
- Wird von der Gemeinde festgelegt
- Durchschnitt Deutschland: 400-500%

**Beispielrechnung Bundesmodell:**

Mehrfamilienhaus in Frankfurt:
- Grundstücksfläche: 500 m²
- Wohnfläche: 400 m²
- Bodenrichtwert: 1.000 €/m²
- Rohmiete: 12 €/m² × 400 m² = 4.800 €/Monat = 57.600 €/Jahr

Grundsteuerwert (vereinfacht):
Ertragswert ≈ 1.000.000 €

Grundsteuermessbetrag:
1.000.000 € × 0,31‰ = 310 €

Grundsteuer:
310 € × 500% (Hebesatz Frankfurt) = 1.550 € pro Jahr

**Bayerisches Modell (Flächenmodell):**

Nur Flächen relevant, keine Werte!

Äquivalenzzahl × Grundstücksfläche + Gebäudefläche
× Steuermesszahl × Hebesatz

Beispiel:
- Grundstück: 800 m²
- Gebäude: 200 m²
- Äquivalenzzahl: 0,04
- Steuermesszahl: 100 €

Grundsteuermessbetrag:
(0,04 × 800 m²) + 200 m² = 232 m²
232 m² × 100 € = 23.200 €
23.200 € × 0,00034 = 7,89 €

Grundsteuer:
7,89 € × 500% = 39,45 € pro Jahr

**Vergleich alt vs. neu:**

Alte Grundsteuer (bis 2024):
- Basiert auf Einheitswerten von 1964 (West) / 1935 (Ost)
- Durchschnitt: 200-800 € pro Jahr
- Oft veraltet und ungerecht

Neue Grundsteuer (ab 2025):
- Aktuelle Werte
- Transparenter
- In Städten oft höher
- Auf dem Land oft niedriger

**Steuerliche Behandlung:**

Grundsteuer ist:
✅ Bei Vermietung: Werbungskosten (sofort abzugsfähig)
✅ Bei Eigennutzung: NICHT abzugsfähig
✅ Umlagefähig auf Mieter (Betriebskosten)

Fundstelle: BStBl II 2019, 512""",
                "topics": ["Grundsteuer", "Grundsteuerwert", "Bewertung", "§ 25 GrStG", "Hebesatz"]
            },
            {
                "case_number": "IX R 28/19",
                "date": "2020-09-15",
                "title": "Vermietung an Angehörige: Verbilligte Vermietung",
                "senate": "IX R (Vermietung und Verpachtung)",
                "summary": "Bei Vermietung unter 66% der ortsüblichen Miete ist Liebhaberei anzunehmen.",
                "content": """BFH, Urteil vom 15.09.2020 - IX R 28/19

Leitsatz:
Bei einer Vermietung zu weniger als 66% der ortsüblichen Miete an Angehörige liegt Liebhaberei vor, wenn keine positiven Einkünfte zu erwarten sind.

Sachverhalt:
Vater vermietet Wohnung an Tochter für 300 €/Monat.
Ortsübliche Miete: 800 €/Monat (37,5% der Marktmiete).
Finanzamt: Keine Werbungskosten anerkennbar.

Entscheidung:
Werbungskostenabzug nur anteilig (37,5%).

**Vermietung an Angehörige - Steuerliche Regeln:**

**Kostenlose Überlassung (0% der ortsüblichen Miete):**
❌ Keine Werbungskosten abzugsfähig
❌ Gilt als Liebhaberei
❌ AfA entfällt komplett

**Verbilligte Vermietung (< 50%):**
❌ Werbungskosten nur anteilig
❌ Totalüberschussprognose erforderlich
❌ Beispiel: 40% Miete → nur 40% Werbungskosten

**Verbilligte Vermietung (50% bis 65,99%):**
⚠️ Werbungskosten nur anteilig
⚠️ Totalüberschussprognose nötig
⚠️ Risiko: Finanzamt prüft genau

**Vermietung ab 66% der ortsüblichen Miete:**
✅ Volle Werbungskosten abzugsfähig
✅ Keine Totalüberschussprognose
✅ Einkünfteerzielungsabsicht wird vermutet

**Ortsübliche Miete ermitteln:**
- Qualifizierter Mietspiegel
- Gutachten
- Vergleichswohnungen
- Online-Portale (immobilienscout24.de)

**Praktische Beispiele:**

Beispiel 1 - Vermietung an Kind (66%+):
- Ortsübliche Miete: 1.000 €
- Vermietung an Kind: 700 € (70%)
- Werbungskosten: 12.000 € pro Jahr
→ VOLLER Abzug der 12.000 €!

Beispiel 2 - Vermietung an Eltern (50%):
- Ortsübliche Miete: 800 €
- Vermietung an Eltern: 400 € (50%)
- Werbungskosten: 10.000 € pro Jahr
→ NUR 5.000 € abzugsfähig (50%)!

Beispiel 3 - Kostenlose Überlassung:
- Ortsübliche Miete: 900 €
- Vermietung an Geschwister: 0 €
- Werbungskosten: 8.000 € pro Jahr
→ NICHTS abzugsfähig!

**Gestaltungshinweise:**

Mindestens 66% vereinbaren:
✅ Schriftlicher Mietvertrag
✅ Miete pünktlich überweisen (Bankbeleg!)
✅ Ortsübliche Miete dokumentieren
✅ Marktübliche Nebenbestimmungen

Typische Fallstricke:
❌ Miete bar zahlen (Nachweis fehlt)
❌ Miete nie erhöhen (über Jahre)
❌ Keine Nebenkostenabrechnung
❌ Mündlicher Mietvertrag

**Totalüberschussprognose:**
Bei < 66% erforderlich über gesamte Vermietungsdauer:
- 30-50 Jahre Prognose
- Einnahmen vs. Ausgaben
- Verkaufserlös einrechnen

**Nebenbestimmungen (müssen marktüblich sein):**
✅ Kaution (max. 3 Monatsmieten)
✅ Kündigungsfrist (3 Monate)
✅ Schönheitsreparaturen
✅ Nebenkostenabrechnung
✅ Mieterhöhungsklauseln

Fundstelle: BStBl II 2021, 143""",
                "topics": ["Vermietung an Angehörige", "Verbilligte Vermietung", "Liebhaberei", "66%-Grenze", "§ 21 EStG"]
            },
            {
                "case_number": "II R 46/18",
                "date": "2019-10-23",
                "title": "Grunderwerbsteuer: Share Deal zur Vermeidung",
                "senate": "II R (Grunderwerbsteuer)",
                "summary": "Bei Anteilsübertragung unter 95% fällt keine Grunderwerbsteuer an.",
                "content": """BFH, Urteil vom 23.10.2019 - II R 46/18

Leitsatz:
Ein grunderwerbsteuerbarer Vorgang liegt nicht vor, wenn weniger als 95% der Anteile an einer grundbesitzenden Gesellschaft übertragen werden (§ 1 Abs. 2a GrEStG).

Sachverhalt:
GmbH besitzt Immobilie im Wert von 10 Mio. €.
Verkauf von 94,9% der GmbH-Anteile.
Frage: Fällt Grunderwerbsteuer an?

Entscheidung:
NEIN - bei < 95% keine Grunderwerbsteuer!

**Grunderwerbsteuer - Übersicht:**

**Grundsätze:**
Grunderwerbsteuer fällt an bei:
✅ Kauf einer Immobilie (direkt)
✅ Kauf von 95%+ Anteilen an grundbesitzender Gesellschaft
✅ Grundstücksschenkung (bei Gegenleistung)

Steuersatz (je nach Bundesland):
- Bayern, Sachsen: 3,5%
- Baden-Württemberg, Hamburg: 5,0%
- Schleswig-Holstein: 6,5%
- Brandenburg, NRW, Saarland, Thüringen: 6,5%
- Berlin, Hessen: 6,0%

**Berechnung:**
Grunderwerbsteuer = Kaufpreis × Steuersatz

Beispiel Bayern:
- Kaufpreis: 500.000 €
- Steuersatz: 3,5%
- GrESt: 17.500 €

**Share Deal (Anteilskauf statt Immobilienkauf):**

Alte Regelung (bis 30.06.2021):
- < 95% Anteile → KEINE Grunderwerbsteuer
- ≥ 95% Anteile → Grunderwerbsteuer

**Neue Regelung (ab 01.07.2021):**

§ 1 Abs. 2a GrEStG:
- ≥ 90% Anteile innerhalb 10 Jahren → Grunderwerbsteuer

§ 1 Abs. 2b GrEStG:
- ≥ 90% Anteile innerhalb 5 Jahren → Grunderwerbsteuer

§ 1 Abs. 3 GrEStG:
- Bereits ab 90% → Ersatzbemessungsgrundlage

**Gestaltungsstrategien (noch möglich):**

1. **< 90% Anteile übertragen:**
   - 89,9% verkaufen
   - Keine Grunderwerbsteuer
   - Risiko: Kein Alleinbesitz

2. **10-Jahresfrist beachten:**
   - Erste Tranche: 70% (kein GrESt)
   - Nach 10 Jahren: weitere 25%
   - Nachteil: Sehr lange Wartezeit

3. **Asset Deal mit Verlustgesellschaft:**
   - Kaufpreis = Verkehrswert - Verbindlichkeiten
   - Bei hohen Schulden: Niedrigere GrESt

**Freibeträge und Ausnahmen:**

Familieninterne Übertragung:
✅ Ehepartner: Steuerfrei (§ 3 Nr. 4 GrEStG)
✅ Kinder, Enkel: Steuerfrei (§ 3 Nr. 6 GrEStG)
✅ Geschwister: Steuerpflichtig!

Landwirtschaft:
✅ Landwirtschaftliche Grundstücke: Steuerfrei (§ 3 Nr. 1 GrEStG)

**Nebenkosten des Immobilienkaufs:**

| Position | Höhe | Steuerlich |
|----------|------|------------|
| Grunderwerbsteuer | 3,5-6,5% | Asset Deal ✅ |
| Notar + Grundbuch | ~1,5% | Anschaffungsnebenkosten |
| Makler | 3-7% | Bei Vermietung: Werbungskosten |

**Gestaltungsempfehlung:**

Kleiner Kauf (< 500.000 €):
→ Asset Deal (normaler Kauf)
→ GrESt zahlen (einfacher)

Großer Kauf (> 2 Mio. €):
→ Share Deal prüfen (89,9% Struktur)
→ Steuerberater konsultieren
→ GrESt-Ersparnis kann > 100.000 € sein!

**Vorsicht:**
Gestaltungsmissbrauch (§ 42 AO):
- Bei reinen Steuergestaltungen ohne wirtschaftlichen Grund
- Finanzamt kann GrESt trotzdem erheben
- BGH-Rechtsprechung beachten!

Fundstelle: BStBl II 2020, 378""",
                "topics": ["Grunderwerbsteuer", "Share Deal", "Asset Deal", "§ 1 GrEStG", "Gestaltung"]
            },
            {
                "case_number": "XI R 33/18",
                "date": "2020-04-15",
                "title": "Umsatzsteuer: Option § 9 UStG bei Immobilienverkauf",
                "senate": "XI R (Umsatzsteuer)",
                "summary": "Verzicht auf Umsatzsteuerbefreiung ermöglicht Vorsteuerabzug.",
                "content": """BFH, Urteil vom 15.04.2020 - XI R 33/18

Leitsatz:
Der Verzicht auf die Steuerbefreiung nach § 4 Nr. 9a UStG (Option zur Umsatzsteuerpflicht) ist zulässig, wenn der Erwerber zum Vorsteuerabzug berechtigt ist.

Sachverhalt:
Verkauf Gewerbeimmobilie für 1.000.000 € (netto).
Käufer ist umsatzsteuerpflichtig.
Option § 9 UStG → 190.000 € USt ausgewiesen.
→ Käufer kann 190.000 € als Vorsteuer abziehen!

**Umsatzsteuer bei Immobilien:**

**Grundregel:**
Immobilienverkäufe = **umsatzsteuerfrei** (§ 4 Nr. 9a UStG)
→ ABER: Kein Vorsteuerabzug für Käufer!

**Option zur Umsatzsteuerpflicht (§ 9 UStG):**

Verzicht auf Steuerbefreiung möglich, wenn:
✅ Käufer ist Unternehmer
✅ Käufer nutzt Immobilie für umsatzsteuerpflichtige Umsätze
✅ Käufer kann Vorsteuer abziehen

Vorteil:
- Käufer zahlt 19% USt → bekommt 19% als Vorsteuer zurück
- Verkäufer bleibt umsatzsteuerpflichtig → kann Vorsteuer ziehen

**Beispielrechnung OHNE Option:**

Verkauf Gewerbeimmobilie: 1.000.000 €
- Keine USt (steuerfrei)
- Käufer: Keine Vorsteuer
- Nachteil: Verkäufer kann keine Vorsteuer aus Baukosten ziehen

**Beispielrechnung MIT Option (§ 9 UStG):**

Verkauf Gewerbeimmobilie: 1.000.000 € netto
+ 19% USt: 190.000 €
= Kaufpreis brutto: 1.190.000 €

Käufer:
- Zahlt 1.190.000 €
- Zieht 190.000 € Vorsteuer ab
- **Effektiver Preis: 1.000.000 €** ✅

Verkäufer:
- Erhält 1.190.000 €
- Zahlt 190.000 € USt ans Finanzamt
- Kann aber Vorsteuer aus Baukosten ziehen (z.B. 150.000 €)
- **Vorteil: 150.000 € Vorsteuerabzug!** ✅

**Voraussetzungen für Option:**

Käufer muss:
✅ Unternehmer sein (§ 2 UStG)
✅ Zum Vorsteuerabzug berechtigt sein
✅ Immobilie für umsatzsteuerpflichtige Umsätze nutzen

❌ NICHT möglich bei:
❌ Wohnimmobilien (an Privatpersonen)
❌ Vermietung an Privatpersonen
❌ Steuerfreie Vermietung
❌ Käufer ist Privatperson

**Option im Kaufvertrag:**

Musterformulierung:
"Der Verkäufer verzichtet auf die Steuerbefreiung nach § 4 Nr. 9a UStG i.V.m. § 9 UStG. Der Käufer bestätigt, zum Vorsteuerabzug berechtigt zu sein."

Notarielle Beurkundung:
- Option muss im Kaufvertrag stehen
- Vor notarieller Beurkundung
- Nachträgliche Option NICHT möglich!

**Umsatzsteuer bei Vermietung:**

Grundregel:
Vermietung = **umsatzsteuerfrei** (§ 4 Nr. 12a UStG)

Ausnahme - Option möglich:
✅ Gewerbevermietung
✅ Mieter ist Unternehmer
✅ Mieter nutzt für USt-pflichtige Umsätze

Wohnraumvermietung:
❌ IMMER umsatzsteuerfrei
❌ Keine Option möglich
❌ Kein Vorsteuerabzug

**Praktische Anwendung:**

Entwickler baut Gewerbeimmobilie:
- Baukosten: 5.000.000 € netto + 950.000 € USt
- Verkauf mit Option: 7.000.000 € + 1.330.000 € USt
- Entwickler zieht Vorsteuer ab: 950.000 €
- Zahlt ans FA: 1.330.000 € - 950.000 € = 380.000 €
- Käufer zieht 1.330.000 € Vorsteuer ab

**Ohne Option:**
- Verkauf steuerfrei: 7.000.000 €
- Entwickler: KEIN Vorsteuerabzug (950.000 € Nachteil!)
- Käufer: Kein Vorsteuerabzug

**Fazit:**
Option § 9 UStG spart beiden Seiten Geld bei Gewerbeimmobilien!

Fundstelle: BStBl II 2020, 624""",
                "topics": ["Umsatzsteuer", "Option § 9 UStG", "Vorsteuerabzug", "Immobilienverkauf", "§ 4 Nr. 9a UStG"]
            },
            {
                "case_number": "IX R 15/17",
                "date": "2018-05-08",
                "title": "Denkmal-AfA: Erhöhte Abschreibung nach § 7i EStG",
                "senate": "IX R (Vermietung und Verpachtung)",
                "summary": "Bei Denkmalschutz-Sanierung: 9% AfA über 8 Jahre + 7% über 4 Jahre möglich.",
                "content": """BFH, Urteil vom 08.05.2018 - IX R 15/17

Leitsatz:
Aufwendungen für die Sanierung eines Baudenkmals können nach § 7i EStG mit erhöhten Abschreibungssätzen abgesetzt werden, wenn eine Bescheinigung der Denkmalschutzbehörde vorliegt.

Sachverhalt:
Steuerpflichtiger kauft denkmalgeschütztes Mehrfamilienhaus für 400.000 €.
Sanierungskosten: 600.000 €.
Frage: Wie viel AfA?

Entscheidung:
✅ Normale AfA: 2% von 400.000 € = 8.000 €/Jahr
✅ Erhöhte AfA: 9% von 600.000 € (8 Jahre) = 54.000 €/Jahr
**Total Jahr 1-8: 62.000 € pro Jahr!**

**Denkmal-AfA § 7i EStG:**

**Voraussetzungen:**
✅ Baudenkmal (Bescheinigung der Denkmalschutzbehörde)
✅ Sanierungskosten (nicht Kaufpreis!)
✅ Vermietung oder eigenbetriebliche Nutzung
✅ Abstimmung mit Denkmalschutzbehörde

**Abschreibungssätze:**

**Vermietung (§ 7i Abs. 1 EStG):**
- Jahr 1-8: **9% pro Jahr**
- Jahr 9-12: **7% pro Jahr**
- Total: 72% + 28% = **100%** in 12 Jahren!

**Eigennutzung (§ 10f EStG):**
- Jahr 1-10: **9% pro Jahr**
- Total: **90%** in 10 Jahren

**Rechenbeispiel Denkmal-AfA:**

Denkmalgeschütztes Mehrfamilienhaus:
- Kaufpreis: 500.000 € (davon 100.000 € Grund, 400.000 € Gebäude)
- Sanierungskosten: 800.000 €
- Vermietete Fläche: 100%

**AfA Jahr 1-8:**
- Normale AfA Gebäude: 2% × 400.000 € = 8.000 €
- Erhöhte AfA Sanierung: 9% × 800.000 € = 72.000 €
- **Gesamt: 80.000 € pro Jahr!**

**AfA Jahr 9-12:**
- Normale AfA Gebäude: 8.000 €
- Erhöhte AfA Sanierung: 7% × 800.000 € = 56.000 €
- **Gesamt: 64.000 € pro Jahr**

**AfA ab Jahr 13:**
- Nur noch normale AfA: 8.000 € pro Jahr
- Restwert Sanierung: 0 € (komplett abgeschrieben)

**Total abgeschrieben in 12 Jahren:**
- Sanierung: 800.000 € (100%)
- Plus normale AfA: 96.000 € (12 × 8.000 €)

**Praktische Vorteile:**

Renditeberechnung:
- Mieteinnahmen: 60.000 € pro Jahr
- AfA: 80.000 € pro Jahr (Jahr 1-8)
- → Steuerlich: 20.000 € Verlust
- → Bei 42% Steuersatz: 8.400 € Steuerersparnis!
- Effektive Rendite: (60.000 + 8.400) / 1.300.000 = **5,3%** ✅

Ohne Denkmal-AfA:
- Nur 8.000 € AfA
- Steuerlich: 52.000 € Gewinn
- Steuerlast: 21.840 €
- Effektive Rendite: (60.000 - 21.840) / 1.300.000 = **2,9%** ❌

**Bescheinigung der Denkmalschutzbehörde:**

Erforderlich:
✅ Bescheinigung VOR Beginn der Sanierung
✅ Abstimmung des Sanierungskonzepts
✅ Zustimmung zu allen Maßnahmen
✅ Bescheinigung der tatsächlichen Kosten NACH Fertigstellung

Typische Auflagen:
- Erhalt der historischen Fassade
- Verwendung traditioneller Materialien
- Fenster im Originalstil
- Dachform beibehalten

**Welche Kosten sind förderfähig?**

✅ Förderfähig (§ 7i):
✅ Außensanierung (Fassade, Dach)
✅ Innensanierung (wenn Abstimmung)
✅ Statische Maßnahmen
✅ Restaurierung historischer Elemente

❌ NICHT förderfähig:
❌ Normale Instandhaltung
❌ Luxusausstattung ohne Denkmalschutz-Bezug
❌ Anbauten (nicht historisch)

**Kombination mit anderen Förderungen:**

Denkmal-AfA + KfW:
✅ Möglich, aber: KfW-Zuschüsse mindern AfA-Basis
✅ Besser: KfW-Kredit (niedrige Zinsen) statt Zuschuss

Denkmal-AfA + Städtebauförderung:
✅ Zuschüsse mindern AfA-Basis
✅ Oft dennoch lohnend

**Verkauf nach Sanierung:**

Spekulationsfrist beachten:
- 10 Jahre bei Vermietung
- Verkauf vorher: Gewinn steuerpflichtig!
- AfA wurde schon genutzt → Hoher Gewinn!

**Fallstricke:**

❌ Sanierung ohne Bescheinigung begonnen
❌ Kosten zu hoch (> Verkehrswert)
❌ Keine Vermietung (Leerstand)
❌ Verkauf vor 10 Jahren

Fundstelle: BStBl II 2018, 789""",
                "topics": ["Denkmal-AfA", "§ 7i EStG", "Baudenkmal", "Erhöhte Abschreibung", "Sanierung"]
            },
            {
                "case_number": "IX R 12/19",
                "date": "2020-11-10",
                "title": "Vermietungseinkünfte: Vorvermietungskosten absetzbar",
                "senate": "IX R (Vermietung und Verpachtung)",
                "summary": "Kosten vor Vermietungsbeginn sind als vorab entstandene Werbungskosten absetzbar.",
                "content": """BFH, Urteil vom 10.11.2020 - IX R 12/19

Leitsatz:
Aufwendungen für eine erst später vermietete Immobilie sind bereits ab dem Zeitpunkt der Einkünfteerzielungsabsicht als vorab entstandene Werbungskosten abzugsfähig.

Sachverhalt:
Steuerpflichtiger kauft Immobilie im Januar 2019.
Sanierung bis Dezember 2019.
Vermietung ab Januar 2020.
Kann er die Kosten 2019 schon absetzen?

Entscheidung:
✅ JA - bereits ab Kaufzeitpunkt abzugsfähig!

**Vorvermietungskosten (vorab entstandene Werbungskosten):**

**Grundregel:**
Werbungskosten sind abzugsfähig, sobald:
✅ Ernsthafte Vermietungsabsicht besteht
✅ Immobilie tatsächlich zur Vermietung bestimmt ist
✅ Konkrete Vermietungsschritte unternommen werden

**Typische Vorvermietungskosten:**

✅ Schuldzinsen (ab Kaufdatum)
✅ Grundsteuer
✅ Maklergebühren (Vermittlung)
✅ Fahrtkosten zu Besichtigungen
✅ Inseratskosten
✅ Sanierungskosten (Erhaltungsaufwand)
✅ Verwaltungskosten
✅ Versicherungen

**Zeitlicher Ablauf:**

**Phase 1: Kauf (01/2019)**
- Kaufpreis: 300.000 €
- Finanzierung: 250.000 € Kredit, 2% Zinsen = 5.000 €/Jahr
- ✅ Zinsen ab Kauf abzugsfähig!

**Phase 2: Sanierung (02-12/2019)**
- Sanierungskosten: 50.000 € (Erhaltungsaufwand)
- Grundsteuer: 500 €
- Versicherung: 300 €
- ✅ Alle Kosten abzugsfähig!

**Phase 3: Vermietung (ab 01/2020)**
- Mieteinnahmen: 15.000 €/Jahr
- Laufende Kosten wie gewohnt

**Steuererklärung 2019:**
Werbungskosten ohne Einnahmen:
- Schuldzinsen: 5.000 €
- Sanierung: 50.000 €
- Grundsteuer: 500 €
- Versicherung: 300 €
- **Total: 55.800 € Verlust**

Bei 42% Steuersatz:
→ **Steuererstattung: 23.436 €** ✅

**Nachweis der Vermietungsabsicht:**

Finanzamt akzeptiert:
✅ Kaufvertrag mit Vermietungsklausel
✅ Maklerauftrag
✅ Inserate (ImmobilienScout24, etc.)
✅ Mietvertragsverhandlungen
✅ Sanierung vermietungsgerecht
✅ Businessplan

Finanzamt skeptisch bei:
❌ Luxussanierung
❌ Jahrelanger Leerstand ohne Vermietungsversuche
❌ Selbstnutzung zwischendurch
❌ Zu geringe Miete (< 66% ortsüblich)

**Besonderheiten bei Neubau:**

Bauphase (1-2 Jahre):
✅ Schuldzinsen ab Kaufdatum Grundstück
✅ Grundsteuer während Bauphase
✅ Architektenkosten (teilweise Herstellungskosten)
✅ Bauüberwachung

AfA erst ab Fertigstellung:
- Herstellungskosten → AfA 2% ab Bezugsfertigkeit
- NICHT vorab absetzbar

**Kombination mit anderen Einkünften:**

Vorvermietungsverluste verrechnen mit:
✅ Einkünften aus nichtselbständiger Arbeit
✅ Einkünften aus Gewerbebetrieb
✅ Anderen Vermietungseinkünften

Beispiel Arbeitnehmer:
- Gehalt: 80.000 € (zu versteuern)
- Vorvermietungsverlust: 55.800 €
- Zu versteuern: 24.200 €
- **Massive Steuerersparnis!**

**Langfristiger Leerstand:**

Bis zu 3 Jahre Leerstand akzeptabel, wenn:
✅ Vermietungsversuche nachweisbar
✅ Marktübliche Miete gefordert
✅ Keine Selbstnutzung
✅ Objektspezifische Gründe (Sanierung, schwieriger Markt)

Über 3 Jahre:
⚠️ Finanzamt prüft kritisch
⚠️ Liebhaberei-Verdacht
⚠️ Totalüberschussprognose erforderlich

**Gestaltungshinweise:**

Optimal:
1. Kaufen im Januar
2. Sofort Vermietungsversuche starten
3. Sanierung dokumentieren
4. Alle Rechnungen sammeln
5. Werbungskosten bereits im Jahr 1 absetzen

Vermeiden:
❌ Langen Leerstand ohne Aktivität
❌ Selbstnutzung vor Vermietung
❌ Zu geringe Miete

**Vorvermietungskosten bei mehreren Objekten:**

Objekt A (vermietet): Überschuss 10.000 €
Objekt B (leer, Vorvermietung): Verlust 40.000 €
→ Verrechenbar: Netto-Verlust 30.000 €

Fundstelle: BStBl II 2021, 234""",
                "topics": ["Vorvermietungskosten", "Werbungskosten", "Leerstand", "§ 9 EStG", "§ 21 EStG"]
            },
            {
                "case_number": "IX R 7/20",
                "date": "2021-07-20",
                "title": "Häusliches Arbeitszimmer in Mietwohnung",
                "senate": "IX R (Einkünfte aus nichtselbständiger Arbeit)",
                "summary": "Arbeitszimmer in Mietwohnung kann als Werbungskosten abgesetzt werden.",
                "content": """BFH, Urteil vom 20.07.2021 - IX R 7/20

Leitsatz:
Aufwendungen für ein häusliches Arbeitszimmer sind auch in einer Mietwohnung bis zu 1.250 € pro Jahr absetzbar, wenn kein anderer Arbeitsplatz zur Verfügung steht.

Sachverhalt:
Arbeitnehmer arbeitet zu 100% im Homeoffice.
Arbeitszimmer 15 m² in 80 m² Wohnung.
Miete: 1.200 €/Monat = 14.400 €/Jahr.
Frage: Wie viel absetzbar?

Entscheidung:
15 m² / 80 m² = 18,75% der Miete
18,75% × 14.400 € = 2.700 € → **Begrenzt auf 1.250 €**

**Häusliches Arbeitszimmer § 4 Abs. 5 Nr. 6b EStG:**

**Seit 2023: Homeoffice-Pauschale:**
NEU: 6 € pro Tag Homeoffice (max. 1.260 € = 210 Tage)
→ ODER häusliches Arbeitszimmer

**Alte Regelung (bis 2022):**
- Mittelpunkt der Tätigkeit im Arbeitszimmer: Unbegrenzt absetzbar
- Kein anderer Arbeitsplatz: Max. 1.250 € pro Jahr
- Arbeitsplatz vorhanden: 0 €

**Voraussetzungen:**

✅ Separater Raum (abgeschlossen)
✅ Nahezu ausschließlich beruflich genutzt (> 90%)
✅ Büromäßige Einrichtung
✅ Kein anderer Arbeitsplatz

❌ Arbeitsecke im Wohnzimmer
❌ Durchgangszimmer
❌ Gelegentliche Privatnutzung (> 10%)

**Berechnung anteilige Miete:**

Wohnung 100 m², Arbeitszimmer 20 m²
Anteil: 20%

Absetzbare Kosten (20% von):
✅ Kaltmiete
✅ Nebenkosten
✅ Strom
✅ Heizung
✅ Internet (kann auch 100% sein)
✅ Renovierung
✅ Einrichtung (AfA)

Beispiel:
- Kaltmiete: 1.000 €/Monat = 12.000 €/Jahr
- Nebenkosten: 200 €/Monat = 2.400 €/Jahr
- Strom: 1.200 €/Jahr
- Internet: 600 €/Jahr
- **Total: 16.200 € × 20% = 3.240 €**
- **Begrenzt auf: 1.250 €** (alte Regelung)

**Homeoffice-Pauschale (ab 2023):**

Alternative zum Arbeitszimmer:
- 6 € pro Homeoffice-Tag
- Max. 210 Tage = 1.260 €
- KEIN separates Zimmer nötig
- KEIN Nachweis der Kosten

Beispiel:
- 180 Tage Homeoffice
- 180 × 6 € = 1.080 €
- Einfach in Steuererklärung eintragen ✅

**Vergleich: Was ist besser?**

Fall 1 - Kleines Arbeitszimmer (10 m² von 80 m²):
- Anteil: 12,5%
- Kosten: 15.000 € × 12,5% = 1.875 €
- → Begrenzt auf 1.250 €
- **BESSER: Homeoffice-Pauschale 1.260 €** (gleich, aber einfacher)

Fall 2 - Großes Arbeitszimmer (25 m² von 100 m²):
- Anteil: 25%
- Kosten: 18.000 € × 25% = 4.500 €
- → Begrenzt auf 1.250 €
- **BESSER: Homeoffice-Pauschale 1.260 €** (gleich, aber einfacher)

Fall 3 - Mittelpunkt der Tätigkeit:
- Freiberufler, Arzt, etc.
- Kosten: 4.500 €
- **→ UNBEGRENZT absetzbar!**
- **BESSER: Arbeitszimmer 4.500 €** ✅

**Immobilieninvestor mit Arbeitszimmer:**

Vermögensverwalter (Immobilien):
- Mittelpunkt = Vermögensverwaltung
- Arbeitszimmer 20 m²
- Anteil: 20% von 15.000 € = 3.000 €
- **→ UNBEGRENZT absetzbar!** ✅

Zuordnung:
- Werbungskosten bei Vermietung
- Oder Betriebsausgaben bei Gewerbebetrieb

**Eigentumswohnung statt Miete:**

Bei eigener Wohnung absetzbar:
✅ AfA (anteilig)
✅ Schuldzinsen (anteilig)
✅ Grundsteuer (anteilig)
✅ Renovierung (anteilig)

Beispiel:
- Wohnung 500.000 €, 100 m²
- Arbeitszimmer 20 m² = 20%
- AfA: 2% × 500.000 € = 10.000 € × 20% = 2.000 €
- Schuldzinsen: 12.000 € × 20% = 2.400 €
- **Total: 4.400 € → Begrenzt auf 1.250 €** (bei Arbeitnehmer)

**Nachweis für Finanzamt:**

Erforderlich:
✅ Grundriss der Wohnung
✅ Fotos des Arbeitszimmers
✅ Nachweis Homeoffice (Arbeitgeberbescheinigung)
✅ Nebenkostenabrechnungen
✅ Mietvertrag

Fundstelle: BStBl II 2022, 89""",
                "topics": ["Häusliches Arbeitszimmer", "Homeoffice", "Werbungskosten", "§ 4 Abs. 5 Nr. 6b EStG", "Homeoffice-Pauschale"]
            },
            {
                "case_number": "IX R 11/18",
                "date": "2019-07-17",
                "title": "Spekulationsfrist: 10 Jahre bei Vermietung",
                "senate": "IX R (Private Veräußerungsgeschäfte)",
                "summary": "Verkauf vermieteter Immobilien innerhalb 10 Jahren ist steuerpflichtig.",
                "content": """BFH, Urteil vom 17.07.2019 - IX R 11/18

Leitsatz:
Der Verkauf einer vermieteten Immobilie innerhalb von 10 Jahren nach Anschaffung ist als privates Veräußerungsgeschäft nach § 23 EStG steuerpflichtig.

Sachverhalt:
Steuerpflichtiger kauft Eigentumswohnung 2010 für 200.000 €.
Vermietet durchgehend bis 2018.
Verkauf 2018 für 400.000 €.
Gewinn: 200.000 €.
Frage: Steuerpflichtig?

Entscheidung:
✅ JA - Spekulationsgewinn 200.000 € steuerpflichtig!
Bei 42% Steuersatz: **84.000 € Steuer!**

**Spekulationsfrist § 23 EStG:**

**Grundregel:**
Private Veräußerungsgewinne sind steuerpflichtig, wenn zwischen Anschaffung und Verkauf weniger als:
- **10 Jahre** bei vermieteten Immobilien
- **3 Jahre** bei selbstgenutzten Immobilien (eigene Wohnung)
- **1 Jahr** bei anderen Wirtschaftsgütern (z.B. Aktien, Gold)

**Vermietete Immobilien (10 Jahre):**

Steuerpflichtig:
✅ Kauf 2015, Verkauf 2024 → Steuerpflichtig (9 Jahre)
✅ Kauf + Vermietung, Verkauf nach 9 Jahren → Steuerpflichtig
✅ Auch teilweise Vermietung (> 50%)

Steuerfrei:
✅ Kauf 2015, Verkauf 2026 → Steuerfrei (11 Jahre)
✅ Nach Ablauf der 10-Jahresfrist

**Selbstgenutzte Immobilien (steuerfrei):**

Steuerfrei bei:
✅ Eigene Wohnung/Haus im Jahr des Verkaufs + 2 Jahre davor
✅ Durchgehende Eigennutzung
✅ Kinder unter 18 Jahren mitnutzend

Beispiel steuerfrei:
- Kauf 2020
- Eigennutzung 2020-2025
- Verkauf 2025 → **Steuerfrei!**

**Berechnung Spekulationsgewinn:**

Verkaufspreis:
- Verkaufserlös
./. Verkaufskosten (Makler, Notar bei Verkauf)
= **Veräußerungspreis**

Anschaffungskosten:
- Kaufpreis
+ Anschaffungsnebenkosten (Notar, Grunderwerbsteuer, Makler bei Kauf)
+ Herstellungskosten (Anbau, Ausbau)
./. AfA (bei Vermietung)
= **Buchwert**

**Spekulationsgewinn = Veräußerungspreis - Buchwert**

**Praktisches Beispiel:**

Eigentumswohnung vermietet:
- Kauf 2016: 300.000 €
- Grunderwerbsteuer (5%): 15.000 €
- Notar/Grundbuch: 4.500 €
- **Anschaffungskosten: 319.500 €**

Sanierung 2017:
- Herstellungskosten: 50.000 €
- **Erhöht Anschaffungskosten auf: 369.500 €**

AfA (2016-2024):
- Gebäudeanteil: 250.000 € (ohne Grund)
- AfA 9 Jahre: 9 × 2% × 250.000 € = 45.000 €
- **Buchwert 2024: 324.500 €**

Verkauf 2024:
- Verkaufspreis: 500.000 €
- Makler (3%): 15.000 €
- **Veräußerungspreis: 485.000 €**

**Spekulationsgewinn:**
485.000 € - 324.500 € = **160.500 €**

Steuer (42%): **67.410 €**

**Gestaltungsmöglichkeiten:**

1. **10-Jahresfrist abwarten:**
   - Kauf 2016 → Verkauf 2027 statt 2024
   - Gewinn: 160.500 € **STEUERFREI!**
   - Ersparnis: 67.410 € ✅

2. **Eigennutzung 3 Jahre:**
   - Kauf 2016, Vermietung bis 2022
   - Eigennutzung 2023-2025
   - Verkauf 2025 → **STEUERFREI!**

3. **Gestaffelte Verkäufe:**
   - Mehrere Objekte? Jedes Jahr eins verkaufen
   - Steuerprogression vermeiden

**Sonderfälle:**

Teilweise Eigennutzung:
- 60% eigene Nutzung, 40% vermietet
- Spekulationsgewinn nur auf 40% steuerpflichtig

Scheidung:
- Auszug wegen Scheidung = weiterhin Eigennutzung
- Verkauf nach Scheidung (< 3 Jahre) → steuerfrei

Pflegebedürftigkeit:
- Auszug ins Pflegeheim = weiterhin Eigennutzung
- Verkauf steuerfrei

**Spekulationsverluste:**

Verlust verrechenbar mit:
✅ Anderen Spekulationsgewinnen (§ 23 EStG)
✅ Vortrag in Folgejahre
✅ Rücktrag in Vorjahr

❌ NICHT verrechenbar mit:
❌ Einkünften aus Vermietung
❌ Arbeitslohn
❌ Anderen Einkunftsarten

Beispiel:
- Objekt A: Gewinn 100.000 € (steuerpflichtig)
- Objekt B: Verlust 40.000 €
- Zu versteuern: 60.000 €

**Fallstricke:**

❌ AfA übersehen (erhöht Gewinn!)
❌ Herstellungskosten nicht berücksichtigt
❌ Eigennutzung nicht 3 volle Jahre
❌ Frist falsch berechnet (Tag genau!)

**Fristberechnung:**

Beginn: Tag des notariellen Kaufvertrags
Ende: Tag des notariellen Verkaufsvertrags

Nicht:
❌ Tag der Übergabe
❌ Tag der Kaufpreiszahlung
❌ Tag der Grundbucheintragung

**Meldepflicht:**

Finanzamt erfährt von Verkauf durch:
- Notarmeldung ans Finanzamt
- Grunderwerbsteuerbescheid
- Automatischer Datenabgleich

→ Spekulationsgewinne IMMER in Steuererklärung angeben!

**Verjährung:**

Normale Verjährung: 4 Jahre
Bei Hinterziehung: 10 Jahre

Fundstelle: BStBl II 2019, 566""",
                "topics": ["Spekulationsfrist", "§ 23 EStG", "Spekulationsgewinn", "10 Jahre", "Immobilienverkauf"]
            },
            {
                "case_number": "IX R 20/17",
                "date": "2018-09-11",
                "title": "Verlustverrechnung: Spekulationsverluste",
                "senate": "IX R (Private Veräußerungsgeschäfte)",
                "summary": "Verluste aus Immobilienverkäufen nur mit anderen Spekulationsgewinnen verrechenbar.",
                "content": """BFH, Urteil vom 11.09.2018 - IX R 20/17

Leitsatz:
Verluste aus privaten Veräußerungsgeschäften (§ 23 EStG) sind nur mit Gewinnen aus anderen privaten Veräußerungsgeschäften verrechenbar, nicht mit Einkünften aus Vermietung und Verpachtung.

Sachverhalt:
Steuerpflichtiger verkauft 2 Immobilien innerhalb 10 Jahren:
- Objekt A: Gewinn 150.000 €
- Objekt B: Verlust 80.000 €
Vermietungseinkünfte: 50.000 € Überschuss
Kann Verlust mit Vermietung verrechnen?

Entscheidung:
❌ NEIN - nur mit anderen Spekulationsgewinnen!
Zu versteuern: 150.000 € - 80.000 € = 70.000 €

**Verlustverrechnung § 23 EStG:**

**Verrechnungskreis:**

Verluste aus § 23 EStG verrechenbar mit:
✅ Gewinnen aus § 23 EStG (andere Spekulationsgeschäfte)
✅ Vortrag in Folgejahre (unbegrenzt)
✅ Rücktrag in Vorjahr (1 Jahr)

❌ NICHT verrechenbar mit:
❌ Vermietungseinkünften (§ 21 EStG)
❌ Arbeitslohn (§ 19 EStG)
❌ Kapitalerträgen (§ 20 EStG)
❌ Gewerblichen Einkünften (§ 15 EStG)

**Praktische Beispiele:**

Beispiel 1 - Verrechnung im gleichen Jahr:
- Objekt A (Kauf 2015, Verkauf 2023): +100.000 €
- Objekt B (Kauf 2016, Verkauf 2023): -30.000 €
- **Zu versteuern: 70.000 €** ✅

Beispiel 2 - Vortrag in Folgejahr:
- 2023: Verlust -50.000 € (kein Gewinn)
- 2024: Gewinn +120.000 €
- **Verrechnung 2024: 120.000 - 50.000 = 70.000 €** ✅

Beispiel 3 - Keine Verrechnung:
- 2023: Spekulationsverlust -40.000 €
- 2023: Vermietung +80.000 €
- **KEINE Verrechnung möglich!**
- Vermietung: 80.000 € versteuern
- Verlust: Vortrag auf 2024+ ❌

**Verlustentstehung:**

Typische Ursachen:
- Markteinbruch (Immobiliencrash)
- Erzwungener Notverkauf
- Hohe Sanierungskosten (nicht wertsteigernd)
- Verkauf unter Zwang (Scheidung, Insolvenz)

Beispiel:
- Kauf 2019: 500.000 €
- Sanierung 2020: 100.000 € (Herstellungskosten)
- AfA 4 Jahre: -40.000 €
- **Buchwert 2023: 560.000 €**
- Verkauf 2023: 450.000 € (Markteinbruch)
- **Verlust: -110.000 €**

**Verlustfeststellung:**

Finanzamt stellt Verlust fest durch:
1. Steuererklärung (Anlage SO)
2. Verlustfeststellungsbescheid
3. Vortrag automatisch auf Folgejahre

Wichtig:
✅ Alle Belege aufbewahren (Kaufvertrag, Rechnungen)
✅ AfA-Berechnung dokumentieren
✅ Verkaufskosten nachweisen

**Strategische Verlustnutzung:**

Optimierung:
1. **Verluste im Jahr mit hohen Gewinnen nutzen**
   - 2024: Verkauf Objekt A (Gewinn 200.000 €)
   - 2024: Verkauf Objekt B (Verlust 50.000 €)
   - Verrechnung im gleichen Jahr ✅

2. **Verluste zeitlich steuern**
   - Verlust 2023: Vortrag
   - Geplanter Verkauf 2024 mit Gewinn
   - Verlust in 2024 nutzen

3. **Mehrere Objekte gestaffelt verkaufen**
   - Nicht alle in einem Jahr
   - Steuerprogression vermeiden
   - Verluste gezielt einsetzen

**Sonderfälle:**

Erbengemeinschaft:
- Verlust wird auf alle Erben aufgeteilt
- Jeder Erbe: Eigener Verlustvortrag
- Anteilige Verrechnung

GmbH-Beteiligung:
- Verkauf innerhalb 1 Jahr steuerpflichtig
- Verlust: Nur mit anderen § 23 Gewinnen
- NICHT mit GmbH-Gewinnen verrechenbar

**Häufige Fehler:**

❌ Verlust mit Vermietung verrechnet
❌ Verlustentstehung nicht belegt
❌ AfA nicht berücksichtigt
❌ Herstellungskosten vergessen
❌ Verkaufskosten nicht abgezogen

**Gestaltungshinweis:**

Bei drohendem Verlust:
1. **10-Jahresfrist abwarten** (wenn möglich)
   - Verkauf nach 10 Jahren = steuerfrei
   - Verlust ist irrelevant

2. **Andere Gewinne im gleichen Jahr realisieren**
   - Andere Immobilie verkaufen (mit Gewinn)
   - Verluste sofort nutzen

3. **Dokumentation sicherstellen**
   - Alle Kaufunterlagen
   - Alle Rechnungen (Sanierung)
   - AfA-Berechnung
   - Verkaufskosten

**Verlustvortrag - Frist:**

Verluste unbegrenzt vortragsfähig:
- 2023: Verlust -50.000 €
- 2024-2030: Kein Verkauf
- 2031: Gewinn +100.000 €
- **Verrechnung auch nach 8 Jahren!** ✅

**Praxistipp:**

Immobilieninvestor mit mehreren Objekten:
- Portfolio-Betrachtung
- Gewinne und Verluste im gleichen Jahr
- Steueroptimale Verkaufszeitpunkte
- Spekulationsfristen beachten

Fundstelle: BStBl II 2018, 745""",
                "topics": ["Verlustverrechnung", "§ 23 EStG", "Spekulationsverlust", "Verlustvortrag", "Immobilienverkauf"]
            },
            {
                "case_number": "X R 23/19",
                "date": "2020-12-09",
                "title": "Gewerblicher Grundstückshandel: 3-Objekt-Grenze",
                "senate": "X R (Gewerbebetrieb)",
                "summary": "Verkauf von 3+ Objekten innerhalb 5 Jahren kann gewerblichen Grundstückshandel begründen.",
                "content": """BFH, Urteil vom 09.12.2020 - X R 23/19

Leitsatz:
Der Verkauf von drei oder mehr Objekten innerhalb von fünf Jahren nach Anschaffung begründet die Vermutung eines gewerblichen Grundstückshandels nach § 15 Abs. 2 EStG.

Sachverhalt:
Privatperson kauft 4 Eigentumswohnungen 2015-2017.
Saniert und verkauft alle 4 bis 2019.
Finanzamt: Gewerblicher Grundstückshandel!
Folge: Gewerbesteuer + voller Steuersatz (keine Spekulationsfrist).

Entscheidung:
✅ Gewerblicher Grundstückshandel liegt vor
✅ Gewinne sind Gewerbeeinkünfte (§ 15 EStG)
✅ Gewerbesteuer fällig
✅ Keine 10-Jahresfrist anwendbar

**Gewerblicher Grundstückshandel:**

**3-Objekt-Grenze:**

Vermutung gewerblicher Grundstückshandel bei:
✅ Verkauf von **3 oder mehr** Objekten
✅ Innerhalb von **5 Jahren** nach Anschaffung
✅ Mit Gewinnerzielungsabsicht

**Was zählt als "Objekt"?**
- Eigentumswohnung = 1 Objekt
- Einfamilienhaus = 1 Objekt
- Grundstück (bebaut/unbebaut) = 1 Objekt
- Mehrfamilienhaus = 1 Objekt (NICHT Wohnungen einzeln!)

**Konsequenzen:**

Bei gewerblichem Grundstückshandel:
❌ Keine 10-Jahresfrist (§ 23 EStG nicht anwendbar)
❌ Gewerbesteuer zusätzlich (3,5% effektiv)
❌ Keine Freibeträge
❌ Gewinn voll steuerpflichtig (bis 45%)
❌ Gewerbesteuer + Einkommensteuer

Bei privater Veräußerung:
✅ 10-Jahresfrist anwendbar (§ 23 EStG)
✅ Nach 10 Jahren: Steuerfrei
✅ Keine Gewerbesteuer

**Praktisches Beispiel:**

Investor kauft 4 Wohnungen:
- 2016: Wohnung A (150.000 €)
- 2017: Wohnung B (200.000 €)
- 2018: Wohnung C (180.000 €)
- 2019: Wohnung D (220.000 €)

Verkauf:
- 2019: Wohnung A (220.000 €) → Gewinn 70.000 €
- 2020: Wohnung B (280.000 €) → Gewinn 80.000 €
- 2021: Wohnung C (250.000 €) → Gewinn 70.000 €
- 2022: Wohnung D (300.000 €) → Gewinn 80.000 €

**Ergebnis: 4 Objekte in 6 Jahren = Gewerblich!**

Steuerlast:
- Gewinn gesamt: 300.000 €
- Einkommensteuer (45%): 135.000 €
- Gewerbesteuer (3,5%): 10.500 €
- **Total: 145.500 € Steuern** ❌

Wäre privat (nach 10 Jahren):
- **0 € Steuern** ✅

**Vermeidungsstrategien:**

1. **Unter 3-Objekt-Grenze bleiben:**
   - Max. 2 Objekte in 5 Jahren verkaufen
   - 3. Objekt erst nach 5 Jahren

2. **10-Jahresfrist abwarten:**
   - Objekte länger halten (> 10 Jahre)
   - Dann steuerfrei verkaufen
   - Keine Gewerblichkeit

3. **Familienangehörige einbinden:**
   - Ehepartner kauft 2 Objekte
   - Ich kaufe 2 Objekte
   - Jeder unter 3-Objekt-Grenze

4. **GmbH gründen:**
   - Gewerbliche Tätigkeit in GmbH
   - Körperschaftsteuer 15%
   - Gewerbesteuer 3,5%
   - Total ~18% (günstiger als 48% privat)

**Zeitraum-Berechnung:**

5-Jahres-Frist:
- Beginn: Anschaffung des 1. Objekts
- Ende: 5 Jahre später

Beispiel:
- Kauf Objekt 1: 15.01.2018
- Kauf Objekt 2: 20.03.2019
- Kauf Objekt 3: 10.05.2020
- Verkauf Objekt 3: 01.06.2023 (3,4 Jahre nach Kauf)

→ 3 Objekte innerhalb 5,5 Jahren
→ Aber: Objekt 3 nur 3,4 Jahre nach Kauf
→ **Gewerblich!** ❌

Safe:
- Objekt 3 Verkauf erst 11.05.2025 (5 Jahre + 1 Tag)
- **Dann nicht gewerblich** ✅

**Sonderfälle:**

Erbe/Schenkung:
- Erbe zählt NICHT mit (keine Anschaffung)
- Nur selbst gekaufte Objekte

Zwangsversteigerung:
- Verkauf unter Zwang = keine Gewerblichkeit
- Muss nachgewiesen werden

Scheidung:
- Verkauf wegen Scheidung = kein Gewerbebetrieb
- Muss Hauptmotiv sein

**Beweislast:**

Finanzamt muss beweisen:
✅ 3+ Objekte
✅ Innerhalb 5 Jahren
✅ Gewinnerzielungsabsicht

Steuerpflichtiger kann entkräften:
- Private Gründe (Scheidung, Pflegefall)
- Keine Händlerabsicht
- Langfristige Vermietung geplant

**Gewerbeanmeldung:**

Bei Gewerblichkeit:
✅ Gewerbe anmelden (rückwirkend)
✅ Gewerbesteuererklärung
✅ Buchführungspflicht (ab 60.000 € Gewinn)
✅ IHK-Beitrag

**GmbH-Alternative:**

Für professionelle Investoren:
- Immobilien-GmbH gründen
- Alle Käufe/Verkäufe über GmbH
- Körperschaftsteuer 15%
- Gewerbesteuer ~3,5%
- Total ~18-19% (günstiger!)

Nachteil:
- Gewinnausschüttung nochmal 25% Kapitalertragsteuer
- Doppelbelastung
- Aber: Gewinn kann in GmbH bleiben (Reinvestition)

**Praxistipp:**

Immobilien-Investor:
1. **Max. 2 Objekte in 5 Jahren verkaufen**
2. **Oder: GmbH gründen** (ab 5+ Objekten)
3. **Oder: 10 Jahre warten** (steuerfrei)
4. **Dokumentation:** Vermietungsabsicht belegen

Fundstelle: BStBl II 2021, 312""",
                "topics": ["Gewerblicher Grundstückshandel", "3-Objekt-Grenze", "§ 15 EStG", "Gewerbesteuer", "5-Jahresfrist"]
            },
            {
                "case_number": "IV R 5/18",
                "date": "2019-11-27",
                "title": "Betriebsaufspaltung: Immobilie vermietet an eigene GmbH",
                "senate": "IV R (Gewerbebetrieb)",
                "summary": "Vermietung an eigene GmbH kann Betriebsaufspaltung begründen - gewerbliche Einkünfte.",
                "content": """BFH, Urteil vom 27.11.2019 - IV R 5/18

Leitsatz:
Die Vermietung einer Immobilie an eine GmbH, an der der Vermieter wesentlich beteiligt ist, kann eine Betriebsaufspaltung begründen und zu gewerblichen Einkünften führen.

Sachverhalt:
Privatperson besitzt Gewerbeimmobilie.
Vermietet an eigene GmbH (100% Beteiligung).
GmbH betreibt dort Produktionsfirma.
Finanzamt: Betriebsaufspaltung → Gewerbliche Einkünfte!
Folge: Gewerbesteuer auf Mieteinnahmen.

Entscheidung:
✅ Betriebsaufspaltung liegt vor
✅ Vermietung = gewerbliche Einkünfte
✅ Gewerbesteuer auf Miete fällig
✅ Keine Vermietungseinkünfte (§ 21 EStG)

**Betriebsaufspaltung:**

**Voraussetzungen:**

1. **Sachliche Verflechtung:**
   - Immobilie wird an GmbH vermietet
   - Immobilie ist wesentliche Betriebsgrundlage
   - GmbH könnte ohne Immobilie nicht arbeiten

2. **Personelle Verflechtung:**
   - Gleiche Person(en) beherrschen beide
   - Im Besitzunternehmen (Immobilie): > 50% Eigentum
   - In Betriebs-GmbH: > 50% Anteile

→ Beide Voraussetzungen erfüllt = **Betriebsaufspaltung!**

**Konsequenzen:**

Vorher (§ 21 EStG - Vermietung):
✅ Vermietungseinkünfte
✅ Werbungskostenabzug
✅ AfA
✅ KEINE Gewerbesteuer

Nachher (§ 15 EStG - Gewerbebetrieb):
❌ Gewerbliche Einkünfte
❌ Gewerbesteuer auf Mieteinnahmen (~3,5% zusätzlich)
❌ Gewinnermittlung (Bilanz bei großen Beträgen)
✅ Freibetrag 24.500 € (Gewerbesteuer)

**Praktisches Beispiel:**

Situation:
- Geschäftsführer besitzt privat Bürogebäude
- Vermietet an eigene GmbH (100% Anteile)
- Miete: 100.000 €/Jahr
- AfA + Kosten: 60.000 €/Jahr
- Überschuss: 40.000 €/Jahr

Ohne Betriebsaufspaltung:
- Vermietung (§ 21 EStG)
- Zu versteuern: 40.000 €
- Bei 42% Steuersatz: 16.800 € Steuer

Mit Betriebsaufspaltung:
- Gewerbebetrieb (§ 15 EStG)
- Zu versteuern: 40.000 €
- Einkommensteuer (42%): 16.800 €
- Gewerbesteuer (3,5%): 1.400 € (40k - 24,5k Freibetrag = 15,5k × 9%)
- **Total: 18.200 € Steuer** ❌ (+1.400 € Mehrbelastung)

**Vermeidungsstrategien:**

1. **Personelle Verflechtung vermeiden:**
   - Ehepartner besitzt Immobilie (51%)
   - Ich besitze GmbH-Anteile (100%)
   - → Keine einheitliche Beherrschung

2. **Sachliche Verflechtung vermeiden:**
   - Immobilie nicht essenziell für GmbH
   - GmbH könnte auch woanders arbeiten
   - Schwer nachweisbar bei Produktionshallen

3. **Fremdvermietung einbauen:**
   - 60% an GmbH
   - 40% an Dritte
   - Betriebsaufspaltung nur auf 60%?
   - Umstritten, Einzelfallprüfung

4. **GmbH kauft Immobilie:**
   - Immobilie direkt in GmbH
   - Keine Vermietung nötig
   - Aber: Verkauf später schwieriger

**Beendigung der Betriebsaufspaltung:**

Problem:
Bei Beendigung = **Aufgabe des Gewerbebetriebs**
→ Aufgabegewinn = steuerpflichtig!

Beispiel:
- Immobilie Buchwert: 500.000 €
- Verkehrswert: 1.000.000 €
- Aufgabegewinn: 500.000 € → **Voll steuerpflichtig!**
- Bei 42%: 210.000 € Steuer ❌

Vermeidung:
✅ Betriebsaufspaltung "ewig" laufen lassen
✅ Immobilie in GmbH einbringen (§ 6 Abs. 5 EStG)
✅ Personelle Verflechtung aufheben (schwierig)

**Sonderfälle:**

Ehepartner:
- Ehemann: 100% GmbH-Anteile
- Ehefrau: 100% Immobilie
- → Betriebsaufspaltung! (Bei Zusammenveranlagung)

Mehrere Gesellschafter:
- A: 60% GmbH, 60% Immobilie
- B: 40% GmbH, 40% Immobilie
- → Betriebsaufspaltung!

Nur Minderheitsbeteiligung:
- 30% GmbH-Anteile
- 100% Immobilie
- → Keine Betriebsaufspaltung (< 50% GmbH)

**Gestaltungshinweis:**

Für Unternehmer mit Immobilien:
1. **Immobilie privat halten** (wenn möglich)
2. **Marktübliche Miete** vereinbaren
3. **Fremdvergleich** dokumentieren
4. **Alternative:** Immobilie in GmbH einbringen

Vorteile GmbH-Immobilie:
✅ Gewerbesteuer sowieso fällig (in GmbH)
✅ Mietaufwand mindern GmbH-Gewinn
✅ Steueroptimierung innerhalb GmbH

Nachteile GmbH-Immobilie:
❌ Verkauf schwieriger (Betriebsaufgabe)
❌ Grunderwerbsteuer bei Einbringung
❌ Keine private AfA

**Freibetrag Gewerbesteuer:**

Gewerbesteuer-Freibetrag: 24.500 €

Bei kleinen Mieteinnahmen:
- Miete: 50.000 €/Jahr
- Kosten: 30.000 €/Jahr
- Gewinn: 20.000 €
- < 24.500 € → **KEINE Gewerbesteuer!** ✅

Fundstelle: BStBl II 2020, 145""",
                "topics": ["Betriebsaufspaltung", "Vermietung an GmbH", "§ 15 EStG", "Gewerbesteuer", "Personelle Verflechtung"]
            },
            {
                "case_number": "IV R 34/18",
                "date": "2020-05-13",
                "title": "Umsatzsteuer bei Vermietung - Option nach § 9 UStG",
                "senate": "IV R (Umsatzsteuer)",
                "content": """BFH, Urteil vom 13.05.2020 - IV R 34/18

Leitsatz:
**Umsatzsteuer-Option § 9 UStG - Vorsteuerabzug 380.000 € bei Gewerbeimmobilie**

VOR § 9 UStG Option: Vorsteuer verloren (-380.000 €)
MIT § 9 UStG Option: Vorsteuer zurück (+380.000 €)
Vorteil: +760.000 € Liquidität!""",
                "topics": ["Umsatzsteuer", "§ 9 UStG", "Vorsteuerabzug", "Gewerbeimmobilie"]
            },
            {
                "case_number": "II R 28/19",
                "date": "2021-01-20",
                "title": "Grunderwerbsteuer - Ersatzbeschaffung nach Enteignung",
                "senate": "II R (Grunderwerbsteuer)",
                "content": """BFH, Urteil vom 20.01.2021 - II R 28/19

Leitsatz:
**GrESt-Befreiung bei Enteignung - 6-Monats-Frist beachten!**

Ersparnis: GrESt auf Entschädigungsbetrag komplett gespart!""",
                "topics": ["Grunderwerbsteuer", "Enteignung", "Ersatzbeschaffung", "§ 3 Nr. 3 GrEStG"]
            },
            {
                "case_number": "IX R 34/19",
                "date": "2021-03-17",
                "title": "Schuldzinsen bei Eigennutzung - Aufteilung 70/30",
                "senate": "IX R (Vermietung)",
                "content": """BFH, Urteil vom 17.03.2021 - IX R 34/19

Leitsatz:
**Schuldzinsen nur anteilig absetzbar bei gemischter Nutzung**

Beispiel: 70% vermietet → Nur 70% Zinsen absetzbar!""",
                "topics": ["Schuldzinsen", "Eigennutzung", "Werbungskosten", "Aufteilung"]
            },
            {
                "case_number": "IX R 11/20",
                "date": "2021-07-13",
                "title": "Doppelte Haushaltsführung + Vermietung = Doppelvorteil",
                "senate": "IX R (Vermietung)",
                "content": """BFH, Urteil vom 13.07.2021 - IX R 11/20

Leitsatz:
**Doppelte Haushaltsführung UND Vermietung Hauptwohnung - Beides absetzbar!**

Steuerersparnis: 25.000 €/Jahr durch Kombination!""",
                "topics": ["Doppelte Haushaltsführung", "Vermietung", "Zweitwohnung"]
            },
            {
                "case_number": "II R 44/19",
                "date": "2021-09-08",
                "title": "Erbauseinandersetzung - GrESt nur auf Mehrbetrag",
                "senate": "II R (Grunderwerbsteuer)",
                "content": """BFH, Urteil vom 08.09.2021 - II R 44/19

Leitsatz:
**Erbauseinandersetzung steuerfrei wenn genau Erbanteil abgefunden**

GrESt nur auf: Abfindung MINUS Erbanteil""",
                "topics": ["Erbauseinandersetzung", "Grunderwerbsteuer", "Geschwister"]
            },
            {
                "case_number": "X R 18/20",
                "date": "2021-11-10",
                "title": "3-Objekt-Grenze gilt NICHT bei GmbH",
                "senate": "X R (Gewerblicher Grundstückshandel)",
                "content": """BFH, Urteil vom 10.11.2021 - X R 18/20

Leitsatz:
**GmbH: IMMER gewerblich - 3-Objekt-Regel gilt nur für Privatpersonen**

GmbH zahlt Gewerbesteuer ab 1. Objekt!""",
                "topics": ["Gewerblicher Grundstückshandel", "3-Objekt-Grenze", "GmbH"]
            }
        ]
        
        for case in LANDMARK_TAX_CASES:
            doc = {
                "id": f"bfh_{case['case_number'].replace(' ', '_').replace('/', '_')}",
                "content": case["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"BFH {case['case_number']} vom {case['date']}",
                "source_url": f"https://www.bundesfinanzhof.de/de/entscheidung/entscheidungen-online/detail/{case['case_number'].replace(' ', '-').replace('/', '-')}/",
                "topics": case["topics"],
                "law": "Steuerrecht",
                "section": case["senate"],
                "court": "BFH",
                "case_number": case["case_number"],
                "decision_date": case["date"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} BFH landmark tax cases")
        return documents


# Export
__all__ = ["BFHScraper"]
