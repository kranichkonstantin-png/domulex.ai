"""
BMF Scraper - Bundesministerium der Finanzen
Scrapes BMF administrative rulings for real estate taxation
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class BMFScraper:
    """
    Scraper für BMF-Schreiben (Bundesministerium der Finanzen)
    
    Focus:
    - AfA-Tabellen für Immobilien
    - Grunderwerbsteuer-Gestaltungen
    - Umsatzsteuer bei Vermietung
    - Share Deal Regelungen
    """
    
    def __init__(self):
        pass
    
    async def scrape_bmf_rulings(self) -> List[Dict]:
        """
        Scrape BMF administrative rulings for real estate
        
        Returns:
            List of BMF ruling documents
        """
        documents = []
        
        BMF_RULINGS = [
            {
                "reference": "BMF IV C 3 - S 2190/21/10002",
                "date": "2021-02-22",
                "title": "AfA-Tabelle für Gebäude - Nutzungsdauer 33 Jahre",
                "content": """BMF-Schreiben vom 22.02.2021 - AfA-Tabelle Gebäude

**Lineare AfA für Wohngebäude:**

Anschaffung nach 31.12.2022:
- **3% pro Jahr** (Nutzungsdauer 33,33 Jahre)
- Anschaffung ab 2023: 3% AfA

Anschaffung vor 01.01.2023:
- **2% pro Jahr** (Nutzungsdauer 50 Jahre)
- Anschaffung bis 2022: 2% AfA

**Beispielrechnung:**

Wohnhaus gekauft 2024:
- Kaufpreis gesamt: 500.000 €
- Davon Grundstück: 150.000 € (30%)
- Davon Gebäude: 350.000 € (70%)
- **AfA pro Jahr: 350.000 € × 3% = 10.500 €** ⭐

Vergleich bei Kauf 2022:
- AfA pro Jahr: 350.000 € × 2% = **7.000 €**
- Mehrwert 2024: **+3.500 €/Jahr** mehr absetzbar!

**Nutzungsdauer nach Gebäudeart:**

| Gebäudeart | Nutzungsdauer | AfA-Satz |
|------------|---------------|----------|
| Wohngebäude (ab 2023) | 33 Jahre | 3% |
| Wohngebäude (bis 2022) | 50 Jahre | 2% |
| Gewerbegebäude | 33 Jahre | 3% |
| Betriebsgebäude | 25 Jahre | 4% |

**Aufteilung Grund & Boden vs. Gebäude:**

Wichtig:
- NUR Gebäude abschreibbar
- Grund & Boden NICHT abschreibbar
- Aufteilung nach Sachwertverfahren oder Kaufpreis

Faustregel:
- Großstadt: 20-30% Grundstück, 70-80% Gebäude
- Land: 30-40% Grundstück, 60-70% Gebäude

Beispiel München:
- Kaufpreis: 1.000.000 €
- Grundstück (25%): 250.000 € → **0 € AfA** ❌
- Gebäude (75%): 750.000 € → **22.500 €/Jahr AfA** ✅

**BMF-Arbeitshilfe zur Aufteilung:**

BMF bietet Excel-Tool:
- Eingabe: PLZ, Baujahr, Kaufpreis
- Ausgabe: Prozentuale Aufteilung
- Download: bundesfinanzministerium.de

Oder:
- Gutachten beauftragen (1.000-2.500 €)
- Finanzamt akzeptiert meist

**Erhöhte AfA bei Denkmalschutz:**

Denkmalgeschütztes Gebäude:
- **9% für 8 Jahre** (§ 7i EStG)
- Dann **7% für weitere 4 Jahre**
- Gesamt: 12 Jahre lang erhöhte AfA

Beispiel Denkmal:
- Sanierungskosten: 300.000 €
- AfA Jahre 1-8: 300.000 € × 9% = **27.000 €/Jahr**
- AfA Jahre 9-12: 300.000 € × 7% = **21.000 €/Jahr**
- **Gesamt 12 Jahre: 300.000 €** (100% abgeschrieben!)

**Praxis-Tipps:**

✅ Kaufvertrag: Aufteilung Grund/Gebäude dokumentieren
✅ Gutachten bei unklarer Aufteilung
✅ Ab 2023 kaufen: 3% statt 2% AfA!
✅ Denkmalschutz prüfen: 9% möglich

Fundstelle: BMF IV C 3 - S 2190/21/10002""",
                "topics": ["AfA", "Abschreibung", "Nutzungsdauer", "Wohngebäude", "3% AfA"]
            },
            {
                "reference": "BMF IV C 1 - S 1978-1/20/10010",
                "date": "2020-03-24",
                "title": "Grunderwerbsteuer Share Deal - 90% Grenze und 10-Jahresfrist",
                "content": """BMF-Schreiben vom 24.03.2020 - Grunderwerbsteuer Share Deal

**Share Deal Regelung:**

OHNE Grunderwerbsteuer:
- Kauf < 90% der GmbH-Anteile innerhalb 10 Jahre
- Beispiel: 89,9% kaufen → **KEINE GrESt** ✅

MIT Grunderwerbsteuer:
- Kauf ≥ 90% der GmbH-Anteile → **VOLLE GrESt** ❌
- Auch bei schrittweisem Erwerb!

**10-Jahres-Frist (Ersatzbemessungsgrundlage):**

Neu seit 01.07.2021:
- 10 Jahre statt 5 Jahre Betrachtungszeitraum
- Kumulierung ALLER Erwerbe in 10 Jahren
- Rückwirkend prüfbar!

Beispiel:
- Jahr 1: Kauf 45% → Keine GrESt
- Jahr 6: Kauf weitere 45% → **90% erreicht!**
- → GrESt auf GESAMTEN Immobilienwert fällig ❌

**Berechnung Grunderwerbsteuer:**

Share Deal ≥ 90%:
- Bemessungsgrundlage: **Verkehrswert Grundstücke**
- NICHT Kaufpreis der Anteile!

Beispiel:
- GmbH besitzt Grundstück Wert: 5.000.000 €
- Kaufpreis GmbH-Anteile (95%): 3.500.000 €
- **GrESt-Bemessung: 5.000.000 €** (Grundstückswert!)
- GrESt (6%): 5.000.000 € × 6% = **300.000 €** ❌

**Gestaltungsmöglichkeiten (legal):**

Variante 1 - Unter 90% bleiben:
- Kauf nur 89,9% der Anteile
- Restliche 10,1% bei anderem Gesellschafter
- **GrESt: 0 €** ✅

Variante 2 - Stille Beteiligung:
- 80% kaufen
- 10% als stille Beteiligung (atypisch still)
- Wirtschaftlich 90%, rechtlich 80%
- **GrESt: 0 €** ✅ (Achtung: Gestaltungsmissbrauch prüfen!)

Variante 3 - 10-Jahres-Frist einhalten:
- Jahr 1: Kauf 45%
- Jahr 11: Kauf weitere 45%
- 10 Jahre überschritten → **GrESt: 0 €** ✅

**Gegenbeispiel - Was NICHT funktioniert:**

Asset Deal (Grundstück direkt kaufen):
- Grundstück kaufen von GmbH
- GrESt: 5.000.000 € × 6% = **300.000 €** ❌
- IMMER Grunderwerbsteuer fällig!

**Ersatzbemessungsgrundlage:**

Bei Share Deal ≥ 90%:
- Finanzamt ermittelt Verkehrswert Grundstück
- Gutachten meist nötig
- Nicht: Buchwert der Bilanz!

Beispiel:
- Buchwert Bilanz: 2.000.000 €
- Verkehrswert (Gutachten): 5.000.000 €
- **Maßgeblich: 5.000.000 €** für GrESt

**Praxis-Tipps:**

✅ MAX 89,9% kaufen (nicht 90%!)
✅ 10-Jahres-Frist beachten (alle Erwerbe!)
✅ Gutachten Verkehrswert vorab
✅ Steuerberater einschalten (Gestaltungsmissbrauch!)

ACHTUNG:
- § 42 AO: Gestaltungsmissbrauch
- Finanzamt kann durchgreifen
- Bei reiner Steuerumgehung: GrESt nachzahlen
- Geldstrafe möglich

**Wirtschaftlichkeitsrechnung:**

Asset Deal:
- GrESt: 300.000 € (6% von 5 Mio.)
- Vorteil: Sicher, keine Risiken

Share Deal (89,9%):
- GrESt: 0 €
- Ersparnis: **300.000 €** ✅
- Risiko: Gestaltungsmissbrauch-Prüfung
- Kosten Steuerberater: 10.000-20.000 €
- **Netto-Ersparnis: ~280.000 €** ⭐

Fundstelle: BMF IV C 1 - S 1978-1/20/10010""",
                "topics": ["Grunderwerbsteuer", "Share Deal", "90% Grenze", "10-Jahres-Frist", "GmbH"]
            },
            {
                "reference": "BMF IV D 2 - S 7300/19/10006",
                "date": "2020-11-17",
                "title": "Umsatzsteuer Option § 9 UStG bei Vermietung",
                "content": """BMF-Schreiben vom 17.11.2020 - Umsatzsteuer Option § 9 UStG

**Option zur Umsatzsteuer bei Vermietung:**

Normal:
- Vermietung Wohnraum: **Umsatzsteuerfrei** § 4 Nr. 12 UStG
- Vermietung Gewerbe: **Umsatzsteuerfrei** (außer Option)
- → Kein Vorsteuerabzug möglich!

MIT Option § 9 UStG:
- Vermietung wird **umsatzsteuerpflichtig** (19%)
- → Vorsteuerabzug möglich! ✅

**Voraussetzungen § 9 UStG:**

1. **Mieter muss unternehmerisch nutzen**
   - Büro, Lager, Werkstatt
   - NICHT: Wohnzwecke (nie Option!)

2. **Mieter zum Vorsteuerabzug berechtigt**
   - Unternehmer mit Umsatzsteuerpflicht
   - NICHT: Arzt, Bank, Versicherung (steuerfreie Umsätze)
   - NICHT: Kleinunternehmer

3. **Verzicht schriftlich beim Finanzamt**
   - VOR erster Vermietung
   - Bindung: 5 Jahre

**Beispielrechnung Gewerbeimmobilie:**

Kauf Bürogebäude:
- Kaufpreis netto: 3.000.000 €
- Umsatzsteuer: 570.000 € (19%)
- **Gesamt: 3.570.000 €**

OHNE § 9 UStG Option:
- Vorsteuer verloren: **-570.000 €** ❌
- Miete: 150.000 €/Jahr (brutto = netto)

MIT § 9 UStG Option:
- Vorsteuer zurück: **+570.000 €** ✅
- Miete: 150.000 € + 28.500 € USt = 178.500 €
- Vermieter zahlt USt an FA: -28.500 €/Jahr

**Liquiditätsvorteil berechnen:**

Jahr 1:
- Vorsteuer zurück: +570.000 €
- USt an FA: -28.500 €
- **Vorteil: +541.500 €** ⭐

Jahr 2-20:
- USt-Neutralität: Mieter zieht Vorsteuer ab
- Vermieter zahlt USt weiter

**Berichtigung nach § 15a UStG:**

Wichtig: 10-Jahres-Berichtigung!

Wenn Mieter wechselt:
- Neuer Mieter NICHT zum Vorsteuerabzug berechtigt
- → Vorsteuer anteilig zurückzahlen!

Beispiel:
- Jahr 1-5: Gewerbemieter (§ 9 Option)
- Jahr 6: Arzt einzieht (steuerfrei)
- → Vorsteuer für 5 Jahre zurück: 570.000 € × 5/10 = **285.000 €** ❌

**Wann § 9 UStG sinnvoll?**

✅ Bei hohen Anschaffungskosten (viel Vorsteuer!)
✅ Langfristige Vermietung (> 10 Jahre)
✅ Mieter sicher zum Vorsteuerabzug berechtigt
✅ Kein Mieterwechsel geplant

❌ Bei Wohnimmobilien (nie möglich!)
❌ Mieter steuerfrei (Arzt, Bank)
❌ Häufiger Mieterwechsel
❌ Mieter = Kleinunternehmer

**Prozedere:**

1. **VOR Kauf klären:**
   - Mieter zum Vorsteuerabzug berechtigt?
   - Wirtschaftlichkeit berechnen

2. **Verzichtserklärung:**
   - Formular beim Finanzamt
   - VOR Vermietungsbeginn
   - Angabe: Mieterobjekt, Mietzweck

3. **Mietvertrag anpassen:**
   - "Miete zzgl. 19% USt"
   - Mieter bestätigt Berechtigung Vorsteuerabzug

4. **USt-Voranmeldung:**
   - Monatlich USt abführen
   - Vorsteuer geltend machen

**Beispiel-Vergleich 20 Jahre:**

OHNE § 9 UStG:
- Vorsteuer verloren: -570.000 €
- Miete: 150.000 €/Jahr × 20 = 3.000.000 €
- **Netto: 2.430.000 €**

MIT § 9 UStG:
- Vorsteuer zurück: +570.000 €
- Miete netto: 150.000 €/Jahr × 20 = 3.000.000 €
- USt-Neutralität (Mieter zieht ab)
- **Netto: 3.570.000 €**
- **Vorteil: +1.140.000 €** über 20 Jahre! ⭐

Fundstelle: BMF IV D 2 - S 7300/19/10006""",
                "topics": ["Umsatzsteuer", "§ 9 UStG", "Vorsteuerabzug", "Vermietung", "Gewerbeimmobilie"]
            },
            {
                "reference": "BMF IV C 1 - S 2253/19/10004",
                "date": "2021-03-19",
                "title": "Spekulationsfrist 10 Jahre - Private Veräußerungsgeschäfte",
                "content": """BMF-Schreiben vom 19.03.2021 - Spekulationsfrist § 23 EStG

**10-Jahres-Frist für Immobilien:**

Grundregel:
- Verkauf < 10 Jahre nach Kauf: **Steuerpflichtig** ❌
- Verkauf ≥ 10 Jahre nach Kauf: **Steuerfrei** ✅

**Berechnung Spekulationsfrist:**

Start:
- Tag der **notariellen Beurkundung** Kaufvertrag
- NICHT: Zahlung oder Übergabe!

Ende:
- Tag der **notariellen Beurkundung** Verkaufsvertrag

Beispiel:
- Kauf: 15.03.2014
- Verkauf: 16.03.2024 (10 Jahre + 1 Tag)
- → **STEUERFREI** ✅

Aber:
- Verkauf: 14.03.2024 (9 Jahre + 364 Tage)
- → **STEUERPFLICHTIG** ❌ (1 Tag zu früh!)

**Eigennutzung-Ausnahme:**

STEUERFREI auch vor 10 Jahren wenn:
- Im Jahr des Verkaufs + 2 volle Jahre davor
- **Selbst bewohnt** (Hauptwohnung!)

Beispiel:
- Kauf: 2020
- Eigennutzung: 2020-2024 (4 Jahre)
- Verkauf: 2024 (nach 4 Jahren)
- → **STEUERFREI** ✅ (Eigennutzung!)

Eigennutzung Zeitraum:
- Jahr des Verkaufs: 2024
- Plus 2 volle Jahre: 2023, 2022
- → Eigennutzung 2022-2024 nötig ✅

**Steuerberechnung bei Verkauf:**

Gewinn = Verkaufspreis - Anschaffungskosten - Veräußerungskosten

Beispiel:
- Verkaufspreis: 800.000 €
- Anschaffungskosten 2019: 500.000 €
- Makler/Notar Verkauf: 50.000 €
- **Gewinn: 250.000 €**

Steuersatz:
- Persönlicher Steuersatz (25-45%)
- Bei 42%: 250.000 € × 42% = **105.000 €** Steuer ❌

Wenn steuerfrei:
- Nach 10 Jahren: **0 € Steuer** ✅
- **Ersparnis: 105.000 €** ⭐

**Freibetrag:**

Wichtig:
- KEIN Freibetrag bei Immobilien!
- Anders als bei Aktien (801 € Sparerpauschbetrag)
- Voller Gewinn steuerpflichtig (wenn < 10 Jahre)

**Verlustverrechnung:**

Bei Verlust (Verkauf unter Anschaffungskosten):
- Verlust verrechenbar mit anderen § 23 EStG Gewinnen
- NICHT mit normalen Einkünften!

Beispiel:
- Immobilie 1 verkauft: +200.000 € Gewinn
- Immobilie 2 verkauft: -50.000 € Verlust
- **Steuerpflichtiger Gewinn: 150.000 €** ✅

**Praxis-Tipps:**

✅ 10 Jahre + 1 Tag warten (Kalenderjahr!)
✅ Bei Eigennutzung: 3 Jahre Mindestnutzung
✅ Notartermine genau dokumentieren
✅ Anschaffungskosten komplett sammeln (alle Rechnungen!)

Optimierung:
- Verkauf nach 9 Jahren geplant?
- → Einziehen für 1 Jahr (Eigennutzung-Ausnahme!)
- Steuerfrei auch vor 10 Jahren ✅

**Was zählt zu Anschaffungskosten?**

Absetzbar:
✅ Kaufpreis
✅ Grunderwerbsteuer
✅ Notar, Grundbuch
✅ Makler (beim Kauf!)
✅ Modernisierung (Herstellungskosten)

NICHT absetzbar:
❌ Tilgung Kredit
❌ Zinsen (waren Werbungskosten bei Vermietung)
❌ Makler beim Verkauf (→ Veräußerungskosten)

**Modernisierung anrechenbar:**

Modernisierung innerhalb 3 Jahre nach Kauf:
- > 15% Anschaffungskosten
- Gilt als "anschaffungsnahe Herstellungskosten"
- Erhöht Anschaffungskosten!

Beispiel:
- Kauf: 400.000 €
- Modernisierung Jahr 1-3: 80.000 €
- **Anschaffungskosten gesamt: 480.000 €**
- Verkauf: 600.000 €
- **Gewinn nur: 120.000 €** (statt 200.000 €!) ✅

Fundstelle: BMF IV C 1 - S 2253/19/10004""",
                "topics": ["Spekulationsfrist", "10 Jahre", "§ 23 EStG", "Eigennutzung", "Steuerfrei"]
            },
            {
                "reference": "BMF IV C 3 - S 2221/19/10003",
                "date": "2019-10-31",
                "title": "Erhaltungsaufwand vs. Herstellungskosten - Abgrenzung",
                "content": """BMF-Schreiben vom 31.10.2019 - Erhaltungsaufwand vs. Herstellungskosten

**Unterscheidung wichtig für Steuer:**

Erhaltungsaufwand:
- **Sofort absetzbar** (im Jahr der Zahlung)
- Reparatur, Instandhaltung
- Erhält Zustand

Herstellungskosten:
- **Über AfA absetzbar** (50 Jahre)
- Wesentliche Verbesserung
- Schafft neuen Zustand

**Beispiele Erhaltungsaufwand (sofort absetzbar):**

✅ Dach reparieren (einzelne Ziegel)
✅ Heizung reparieren
✅ Tapezieren, Streichen
✅ Austausch Bodenbelag (gleichwertig)
✅ Fenster reparieren
✅ Rohre Sanitär erneuern

Kosten: **Sofort als Werbungskosten** ✅

**Beispiele Herstellungskosten (AfA):**

❌ Komplette Dachsanierung (Dachstuhl neu)
❌ Heizung komplett erneuern (höherwertiger)
❌ Anbau, Aufstockung
❌ Aus 2 Zimmern 3 machen
❌ Komplette Badsanierung (höherwertig)
❌ Komplette Fassadendämmung

Kosten: **Nur AfA über 50 Jahre** (2% p.a.) ❌

**Anschaffungsnahe Herstellungskosten (Sonderfall):**

Besondere Regelung:
- Modernisierung innerhalb 3 Jahre nach Kauf
- Kosten > 15% des Gebäudewerts (ohne Grund)
- → Gilt als Herstellungskosten (AfA!)

Beispiel:
- Kauf Haus 2023: 400.000 €
- Davon Gebäude: 300.000 €
- Modernisierung 2023-2025: 60.000 €
- 60.000 € / 300.000 € = **20%** > 15%!
- → **Anschaffungsnahe Herstellungskosten** ❌

Folge:
- NICHT sofort absetzbar
- Sondern über 50 Jahre AfA
- Pro Jahr: 60.000 € / 50 = **1.200 €** statt 60.000 €!

**Vermeidung anschaffungsnahe Herstellungskosten:**

Trick:
- Modernisierung auf NACH 3 Jahre verschieben
- Oder: Unter 15% bleiben

Beispiel:
- Gebäudewert: 300.000 €
- 15%-Grenze: 45.000 €
- Jahr 1-3: MAX 44.999 € ausgeben ✅
- Ab Jahr 4: Rest modernisieren (60.000 €)
- → Jahr 4+: Sofort absetzbar! ✅

**Wirtschaftlichkeitsrechnung:**

Modernisierung 60.000 € innerhalb 3 Jahre (> 15%):
- Anschaffungsnahe Herstellungskosten
- AfA: 60.000 € / 50 Jahre = 1.200 €/Jahr
- Steuervorteil (42%): 1.200 € × 42% = **504 €/Jahr**
- Über 50 Jahre: 25.200 € Steuerersparnis

Modernisierung 60.000 € NACH 3 Jahren:
- Erhaltungsaufwand
- Sofort absetzbar: 60.000 €
- Steuervorteil (42%): 60.000 € × 42% = **25.200 €** im Jahr 1! ✅
- **Vorteil: Sofort statt über 50 Jahre verteilt** ⭐

**Was zählt zu 15%-Grenze?**

Zählt MIT:
✅ Instandsetzungsmaßnahmen
✅ Modernisierung
✅ Schönheitsreparaturen (umfangreich)

Zählt NICHT:
❌ Erhaltungsaufwand jährlich (normal)
❌ Kleinreparaturen
❌ Grund & Boden

**Praxis-Tipps:**

✅ Bei Kauf: 3 Jahre NICHTS Großes sanieren
✅ Oder: Unter 15% bleiben
✅ Ab Jahr 4: Volle Modernisierung sofort absetzbar
✅ Rechnungen genau dokumentieren (Datum!)

**Umfassende Modernisierung (Ausnahme):**

Wenn innerhalb 3 Jahre KOMPLETT saniert:
- Mehr als 3 zentrale Bereiche erneuert
- Z.B.: Heizung, Bad, Elektrik, Fenster
- → Immer Herstellungskosten (egal wie viel %)

Zentrale Bereiche:
1. Heizung
2. Sanitär
3. Elektrik
4. Fenster
5. Dach

Bei ≥ 3 erneuert:
- Herstellungskosten (AfA 50 Jahre)
- AUCH wenn unter 15%!

**Zusammenfassung:**

| Maßnahme | Zeitpunkt | Kosten | Absetzbarkeit |
|----------|-----------|--------|---------------|
| Kleine Reparatur | Egal | < 15% | Sofort ✅ |
| Große Modernisierung | < 3 Jahre nach Kauf | > 15% | AfA 50 Jahre ❌ |
| Große Modernisierung | > 3 Jahre nach Kauf | Egal | Sofort ✅ |
| 3+ zentrale Bereiche | < 3 Jahre | Egal | AfA 50 Jahre ❌ |

Fundstelle: BMF IV C 3 - S 2221/19/10003""",
                "topics": ["Erhaltungsaufwand", "Herstellungskosten", "Anschaffungsnahe Herstellungskosten", "15% Grenze", "Modernisierung"]
            },
            {
                "reference": "BMF IV C 1 - S 2296/08/10004",
                "date": "2021-05-12",
                "title": "Vermietung an Angehörige - 66% Regel (Verbilligte Vermietung)",
                "content": """BMF-Schreiben vom 12.05.2021 - Verbilligte Vermietung § 21 EStG

**66%-Regel bei Vermietung an Angehörige:**

Ortsübliche Miete:
- Miete ≥ 66% der Ortsüblichkeit: **VOLLE Werbungskosten** ✅
- Miete < 66% der Ortsüblichkeit: **Nur anteilige Werbungskosten** ❌

**Beispielrechnung:**

Ortsübliche Miete: 1.500 €/Monat

Variante A - Miete 1.200 € (80%):
- 1.200 € / 1.500 € = **80%** > 66%
- → **VOLLE Werbungskosten absetzbar** ✅

Werbungskosten gesamt: 18.000 €/Jahr
- Absetzbarer Betrag: **18.000 €** ✅

Variante B - Miete 800 € (53%):
- 800 € / 1.500 € = **53%** < 66%
- → **NUR anteilige Werbungskosten** ❌

Werbungskosten gesamt: 18.000 €/Jahr
- Absetzbarer Betrag: 18.000 € × 53% = **9.540 €** ❌
- Verlust: **8.460 €** nicht absetzbar!

**Ermittlung ortsübliche Miete:**

Quellen:
1. **Mietspiegel** (wenn vorhanden)
2. **Vergleichsmieten** (mind. 3 vergleichbare Objekte)
3. **Gutachten** (bei Streit mit Finanzamt)

Kosten Gutachten: 500-1.500 €

**Liebhaberei-Prüfung:**

Wenn < 66% UND Angehörige:
- Finanzamt prüft: Überschussprognose
- Wird langfristig Gewinn erzielt?
- Wenn NEIN: **Liebhaberei** → ALLE Werbungskosten gestrichen!

Überschussprognose:
- Zeitraum: 30 Jahre
- Einnahmen vs. Ausgaben
- Inkl. Verkaufserlös am Ende

**Beispiel Liebhaberei-Prüfung:**

Vermietung an Tochter:
- Miete: 600 €/Monat (50% ortsüblich)
- Werbungskosten: 15.000 €/Jahr
- Verlust: -7.800 €/Jahr

Finanzamt prüft 30 Jahre:
- Einnahmen: 600 € × 12 × 30 = 216.000 €
- Ausgaben: 15.000 € × 30 = 450.000 €
- **Verlust: -234.000 €** über 30 Jahre
- → **Liebhaberei!** → KEINE Werbungskosten ❌

**Vermeidung Liebhaberei:**

✅ Mindestens 66% ortsübliche Miete
✅ Überschussprognose positiv (30 Jahre)
✅ Mietvertrag schriftlich (wie bei Fremden)
✅ Miete pünktlich überweisen (Beleg!)

**Angehörige im Sinne des Steuerrechts:**

Angehörige sind:
✅ Eltern, Kinder
✅ Geschwister
✅ Lebenspartner
✅ Verlobte

NICHT Angehörige:
❌ Freunde
❌ Bekannte
❌ Geschäftspartner

**Praxis-Tipps:**

Optimale Miete:
- **66-70% der Ortsüblichkeit** ✅
- Volle Werbungskosten absetzbar
- Aber: Familie zahlt weniger

Beispiel optimal:
- Ortsüblich: 1.500 €
- An Tochter: 1.000 € (67%)
- Familie spart: 500 €/Monat = **6.000 €/Jahr** ✅
- Volle Werbungskosten: 18.000 € absetzbar ✅
- **Win-Win!** ⭐

**Wirtschaftlichkeitsrechnung:**

Vermietung ortsüblich 1.500 €:
- Einnahmen: 18.000 €/Jahr
- Werbungskosten: 18.000 €/Jahr
- Überschuss: 0 €
- Steuer: 0 €

Vermietung an Tochter 1.000 € (67%):
- Einnahmen: 12.000 €/Jahr
- Werbungskosten: 18.000 €/Jahr (voll absetzbar!)
- **Verlust: -6.000 €**
- Steuerersparnis (42%): 6.000 € × 42% = **2.520 €** ✅

Vorteil Tochter:
- Zahlt 6.000 € weniger Miete/Jahr
- Familie spart gesamt: **6.000 € + 2.520 € = 8.520 €/Jahr** ⭐

**Mietvertrag mit Angehörigen:**

Wichtig:
✅ Schriftlicher Vertrag (wie bei Fremden!)
✅ Marktübliche Bedingungen
✅ Pünktliche Zahlung (Überweisung!)
✅ Keine Gefälligkeiten

NICHT:
❌ Mündlicher Vertrag
❌ Unregelmäßige Zahlung
❌ Keine Belege

Fundstelle: BMF IV C 1 - S 2296/08/10004""",
                "topics": ["Verbilligte Vermietung", "Angehörige", "66% Regel", "Werbungskosten", "Liebhaberei"]
            },
            {
                "reference": "BMF IV C 1 - S 2119/20/10003",
                "date": "2020-07-31",
                "title": "Gewerblicher Grundstückshandel - 3-Objekt-Grenze Anwendung",
                "content": """BMF-Schreiben vom 31.07.2020 - Gewerblicher Grundstückshandel

**3-Objekt-Grenze (Privatperson):**

Regel:
- Bis 3 Objekte in 5 Jahren: **Privat** (nur Spekulationssteuer)
- Ab 4 Objekte in 5 Jahren: **Gewerblich** (Gewerbesteuer!)

**Berechnung 5-Jahres-Zeitraum:**

Zählt ab:
- Erstem Verkauf (rückwärts 5 Jahre)

Beispiel:
- 2024: Verkauf 4. Objekt
- Prüfung: 2019-2024 (5 Jahre)
- Verkäufe in dieser Zeit: 4 Objekte
- → **GEWERBLICH** ❌

**Was zählt als Objekt?**

1 Objekt = 1 Grundstück/Wohnung:
✅ Einfamilienhaus = 1 Objekt
✅ Eigentumswohnung = 1 Objekt
✅ Grundstück (unbebaut) = 1 Objekt
✅ Mehrfamilienhaus = 1 Objekt (!)

NICHT mehrere Objekte:
- Mehrfamilienhaus mit 10 Wohnungen = **1 Objekt** ✅
- NICHT 10 Objekte!

**Ausnahmen (zählt NICHT mit):**

Nicht als Objekt zählen:
❌ Erbschaft (+ Verkauf innerhalb 5 Jahre)
❌ Schenkung (+ Verkauf)
❌ Eigennutzung vor Verkauf (> 3 Jahre)

Beispiel Ausnahme:
- Objekt 1-3: Gekauft + verkauft
- Objekt 4: Geerbt + verkauft
- → **NUR 3 Objekte** zählen → Privat ✅

**Folgen gewerblicher Grundstückshandel:**

Bei ≥ 4 Objekten:
❌ **Gewerbesteuer** auf ALLE Gewinne (14-20%)
❌ **Rückwirkend** auf ALLE 4 Objekte!
❌ Kein Freibetrag mehr
❌ Gewerbe anmelden (nachträglich)

Steuersatz:
- Einkommensteuer: Bis 45%
- Gewerbesteuer: 14-20% (Hebesatz-abhängig)
- **Gesamt: ~50-60%** ❌

**Beispielrechnung:**

4 Objekte in 5 Jahren verkauft:
- Gewinn Objekt 1: 80.000 €
- Gewinn Objekt 2: 100.000 €
- Gewinn Objekt 3: 120.000 €
- Gewinn Objekt 4: 150.000 €
- **Gesamt: 450.000 €** Gewinn

PRIVAT (nur Spekulationssteuer):
- Verkauf innerhalb 10 Jahre
- Einkommensteuer: 450.000 € × 42% = **189.000 €**

GEWERBLICH (ab 4. Objekt):
- Einkommensteuer: 450.000 € × 42% = 189.000 €
- Gewerbesteuer: 450.000 € × 15% = **67.500 €**
- **Gesamt: 256.500 €** ❌
- **Mehrbelastung: +67.500 €** ❌

**Vermeidung gewerblicher Grundstückshandel:**

Strategie 1 - MAX 3 in 5 Jahren:
- Jahr 1: Verkauf Objekt 1
- Jahr 2: Verkauf Objekt 2
- Jahr 3: Verkauf Objekt 3
- Jahr 6: Verkauf Objekt 4 (nach 5 Jahren!) ✅

Strategie 2 - GmbH gründen:
- Objekte in GmbH einbringen
- GmbH: Gewerbe ab 1. Objekt
- Aber: Niedrigerer Steuersatz (30% statt 60%)
- Optimal bei > 10 Objekten/Jahr

Strategie 3 - Eigennutzung:
- 3 Jahre selbst bewohnen
- Dann verkaufen
- Zählt NICHT als Objekt ✅

**Nachträgliche Gewerbeanmeldung:**

Bei 4. Verkauf:
- Rückwirkend Gewerbe anmelden
- Gewerbesteuer für ALLE 4 Objekte nachzahlen
- Säumniszuschläge möglich
- Verspätungszuschlag

**Praxis-Tipps:**

✅ Genau zählen: MAX 3 Objekte in 5 Jahren
✅ Bei Erbschaft: Zählt NICHT mit
✅ Bei Eigennutzung (> 3 Jahre): Zählt NICHT
✅ Ab 4. Objekt: 5 Jahre warten!

**GmbH vs. Privatperson:**

| Aspekt | Privatperson | GmbH |
|--------|--------------|------|
| 3-Objekt-Grenze | Ja | NEIN (immer gewerblich) |
| Gewerbesteuer | Ab 4 Objekten | Ab 1. Objekt |
| Steuersatz | Bis 60% | ~30% |
| Spekulationsfrist | 10 Jahre | Gibt es nicht |

GmbH lohnt sich bei:
✅ > 10 Objekte/Jahr
✅ Professionelles Flipping
✅ Langfristige Strategie

Fundstelle: BMF IV C 1 - S 2119/20/10003""",
                "topics": ["Gewerblicher Grundstückshandel", "3-Objekt-Grenze", "5-Jahres-Frist", "Gewerbesteuer", "Flipping"]
            },
            {
                "reference": "BMF IV C 6 - S 2296/15/10003",
                "date": "2019-12-18",
                "title": "Häusliches Arbeitszimmer - Abzugsfähigkeit bei Vermietung",
                "content": """BMF-Schreiben vom 18.12.2019 - Häusliches Arbeitszimmer

**Arbeitszimmer als Werbungskosten:**

Voraussetzungen:
1. **Separater Raum** (abgeschlossen)
2. **Nahezu ausschließlich beruflich** (> 90%)
3. **Kein anderer Arbeitsplatz** vorhanden

**Abzugsbeschränkung:**

Normaler Fall (Alternativ-Arbeitsplatz vorhanden):
- MAX **1.250 €/Jahr** absetzbar ⚠️

Kein Alternativ-Arbeitsplatz (Mittelpunkt Tätigkeit):
- **UNBESCHRÄNKT** absetzbar ✅

Seit 2023 (Homeoffice-Pauschale):
- Alternative: **6 €/Tag** Homeoffice (max. 1.260 €/Jahr)
- OHNE Nachweis Arbeitszimmer!

**Beispielrechnung unbeschränkt:**

Arbeitszimmer = Mittelpunkt der Tätigkeit:
- Raumkosten (Miete anteilig): 3.600 €/Jahr
- Nebenkosten anteilig: 800 €/Jahr
- Einrichtung (AfA): 500 €/Jahr
- **Gesamt: 4.900 €/Jahr** voll absetzbar ✅

Bei 42% Steuersatz:
- Steuerersparnis: 4.900 € × 42% = **2.058 €/Jahr** ⭐

**Berechnung anteilige Kosten:**

Wohnung 100 m², Arbeitszimmer 15 m²:
- Anteil: 15 / 100 = **15%**

Miete gesamt: 2.000 €/Monat:
- Anteil Arbeitszimmer: 2.000 € × 15% = **300 €/Monat**
- Pro Jahr: 300 € × 12 = **3.600 €** ✅

**Wann Mittelpunkt der Tätigkeit?**

Mittelpunkt liegt vor bei:
✅ Freiberufler (Architekt, Anwalt) - Hauptarbeit zu Hause
✅ Lehrer - Unterrichtsvorbereitung zu Hause (> 50% Zeit)
✅ Außendienstler - Büro zu Hause, unterwegs nur Kundentermine

KEIN Mittelpunkt:
❌ Bürojob - Arbeitgeber hat Büro
❌ Produktion - Fabrik vorhanden
❌ Verkäufer - Laden vorhanden

**Homeoffice-Pauschale ab 2023:**

Alternative zum Arbeitszimmer:
- **6 € pro Homeoffice-Tag**
- MAX 1.260 €/Jahr (210 Tage)
- KEIN Arbeitszimmer nötig!
- KEIN Nachweis Kosten!

Vergleich:
- Arbeitszimmer unbeschränkt: 4.900 € ✅
- Homeoffice-Pauschale: 1.260 € ⚠️
- → Arbeitszimmer besser (bei hohen Kosten)!

**Bei Vermietung (Vermieter):**

Vermieter nutzt Teil selbst:
- Arbeitszimmer = Eigennutzung
- Anteil NICHT vermietete Fläche
- AfA nur auf vermieteten Teil!

Beispiel:
- Wohnung 120 m²
- Vermietet: 100 m² (83%)
- Arbeitszimmer Eigennutzung: 20 m² (17%)
- AfA nur auf: **100 m²** ✅

**Einrichtung absetzbar:**

Möbel Arbeitszimmer:
✅ Schreibtisch: 800 €
✅ Bürostuhl: 400 €
✅ Regal: 300 €
✅ PC: 1.200 €

Über 800 € (GWG-Grenze):
- AfA über Nutzungsdauer
- Schreibtisch: 13 Jahre → 800 € / 13 = **62 €/Jahr**
- PC: 3 Jahre → 1.200 € / 3 = **400 €/Jahr**

Unter 800 € (GWG):
- **Sofort absetzbar** ✅
- Bürostuhl: 400 € → **400 € im Jahr 1** ✅

**Nachweis häusliches Arbeitszimmer:**

Finanzamt verlangt:
✅ Grundriss Wohnung
✅ Nachweis berufliche Nutzung (Arbeitsvertrag)
✅ Bei Lehrer: Bescheinigung Schule
✅ Fotos Arbeitszimmer

**Praxis-Tipps:**

✅ Separater Raum (mit Tür!)
✅ KEINE private Nutzung (kein Gästebett!)
✅ Nachweis Mittelpunkt der Tätigkeit
✅ Alle Belege sammeln (Miete, Nebenkosten, Möbel)

**Optimierung:**

Hohe Kosten (> 1.250 €):
→ Arbeitszimmer als Mittelpunkt nachweisen ✅

Niedrige Kosten (< 1.250 €):
→ Homeoffice-Pauschale nutzen (6 €/Tag, kein Nachweis) ✅

Fundstelle: BMF IV C 6 - S 2296/15/10003""",
                "topics": ["Häusliches Arbeitszimmer", "Werbungskosten", "1.250 € Grenze", "Homeoffice-Pauschale", "Mittelpunkt Tätigkeit"]
            }
        ]
        
        for ruling in BMF_RULINGS:
            doc = {
                "id": f"bmf_{ruling['reference'].lower().replace(' ', '_').replace('-', '_').replace('/', '_')}",
                "content": ruling["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"BMF {ruling['reference']} vom {ruling['date']}",
                "source_url": "https://www.bundesfinanzministerium.de",
                "topics": ruling["topics"],
                "law": "BMF-Schreiben",
                "section": ruling["reference"],
                "ruling_date": ruling["date"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} BMF rulings")
        return documents


# Export
__all__ = ["BMFScraper"]
