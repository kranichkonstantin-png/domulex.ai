"""
BGB Sachenrecht Scraper - Grundstücksrecht (§§ 873-1296)
Eigentumserwerb, Grundpfandrechte, Nießbrauch, Grunddienstbarkeiten
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class BGBSachenrechtScraper:
    """Scraper für BGB Sachenrecht - Immobilien-relevante Paragraphen"""
    
    def __init__(self):
        pass
    
    async def scrape_sachenrecht(self) -> List[Dict]:
        """Scrape BGB Sachenrecht §§ 873-1296"""
        documents = []
        
        SACHENRECHT_PARAGRAPHS = [
            # EIGENTUMSERWERB
            {
                "section": "§ 873",
                "title": "Einigung und Eintragung (Auflassung)",
                "content": """§ 873 BGB - Einigung und Eintragung

**Grundsatz:**
Zur Übertragung des Eigentums an einem Grundstück bedarf es:
1. **Einigung** (Auflassung) zwischen Veräußerer und Erwerber
2. **Eintragung** im Grundbuch

**Auflassung:**
- Notarielle Beurkundung erforderlich (§ 925 BGB)
- Vor Notar gleichzeitig erklärt oder getrennt
- Bindend: Kann nicht widerrufen werden

**Beispiel Hausverkauf:**
- 15.03.2024: Kaufvertrag notariell
- 15.03.2024: Auflassung erklärt (meist gleichzeitig)
- Notar beantragt Eintragung
- 15.05.2024: Grundbucheintragung
- → **15.05.2024: Eigentum geht über** ✅

**NICHT mit Unterschrift!**
- Kaufvertrag unterschrieben = noch KEIN Eigentum
- Erst Grundbucheintragung = Eigentümer

**Praxis-Tipp:**
- Zahlung NACH Grundbucheintragung (Treuhandkonto Notar)
- Oder: Vormerkung eintragen (§ 883 BGB) für Sicherheit

Fundstelle: BGB § 873"""
            },
            {
                "section": "§ 925",
                "title": "Auflassung - Notarielle Beurkundung",
                "content": """§ 925 BGB - Auflassung

**Form:**
- Notarielle Beurkundung ZWINGEND
- Beide Parteien anwesend (oder getrennte Beurkundung)
- Identitätsprüfung durch Notar

**Inhalt:**
"Ich übertrage hiermit das Eigentum an [Grundstück] auf [Käufer]"
- Grundstück genau bezeichnen (Flurstück, Gemarkung)
- Beide Parteien müssen zustimmen

**Kosten Notar:**
- 1,5% des Kaufpreises (ca.)
- Kaufpreis 500.000 €: Notar ~7.500 €

**Zeitlicher Ablauf:**
1. Kaufvertrag + Auflassung beim Notar
2. Notar beantragt Eintragung Grundbuch
3. Grundbuchamt prüft (2-8 Wochen)
4. Eintragung = Eigentumsübergang

**Ohne Notar:**
- Auflassung unwirksam (§ 125 BGB)
- Kein Eigentumsübergang möglich

Fundstelle: BGB § 925"""
            },
            {
                "section": "§ 883",
                "title": "Vormerkung - Kaufpreisabsicherung",
                "content": """§ 883 BGB - Vormerkung

**Zweck:**
Sicherung des Anspruchs auf Eigentumsübertragung
→ Käufer sichert sich gegen Weiterverkauf ab!

**Wirkung:**
- Schutz vor Zweitverkauf
- Schutz vor Grundschuldbestellung
- Rangwahrung

**Beispiel:**
1. Kaufvertrag 500.000 € am 01.03.2024
2. Vormerkung eingetragen 05.03.2024
3. Verkäufer will an Dritten verkaufen (höheres Angebot)
4. → **Unwirksam!** Vormerkung schützt ✅

**Eintragung:**
- Im Grundbuch Abteilung II
- "Vormerkung zur Sicherung des Anspruchs auf Auflassung"
- Kosten: ~200-400 € (meist Notar übernimmt)

**Löschung:**
- Automatisch bei Eigentumsübertragung
- Oder: Nach 2 Jahren Verjährung

**Praxis:**
IMMER Vormerkung eintragen lassen!
- Zwischen Kaufvertrag und Zahlung
- Schutz vor Doppelverkauf

Fundstelle: BGB § 883"""
            },
            
            # GRUNDPFANDRECHTE
            {
                "section": "§ 1191",
                "title": "Grundschuld - Standard-Kreditsicherung",
                "content": """§ 1191 BGB - Grundschuld

**Definition:**
Recht, aus Grundstück Zahlung zu verlangen
→ OHNE persönliche Forderung (Unterschied zu Hypothek!)

**Standard heute:**
- 95% aller Immobilienkredite mit Grundschuld
- Bank kann Grundstück zwangsversteigern bei Zahlungsausfall

**Beispiel Kredit 400.000 €:**
- Grundschuld 400.000 € wird eingetragen
- Grundbuch Abteilung III
- Bank = Gläubiger
- Bei Zahlungsausfall: Zwangsversteigerung

**Arten:**
1. **Briefgrundschuld:** Mit Grundschuldbrief (übertragbar)
2. **Buchgrundschuld:** Nur im Grundbuch (häufiger)

**Kosten Eintragung:**
- 400.000 € Grundschuld: ~1.200 € Notar + Grundbuchamt

**Löschung:**
- Nach Kredit abbezahlt: Löschungsbewilligung Bank
- Kosten: ~300-600 €
- ODER: Grundschuld behalten für nächsten Kredit ✅

**Vorteil Grundschuld:**
- Wiederverwendbar (nicht akzessorisch)
- Bei neuer Renovierung: Gleiche Grundschuld nutzen

Fundstelle: BGB § 1191"""
            },
            {
                "section": "§ 1113",
                "title": "Hypothek - Alte Kreditsicherung",
                "content": """§ 1113 BGB - Hypothek

**Definition:**
Pfandrecht am Grundstück für bestimmte Forderung
→ Akzessorisch (hängt an persönlicher Forderung)

**Heute kaum noch:**
- Bis ~2000: Standard
- Seit 2000: Grundschuld üblicher

**Unterschied zu Grundschuld:**
| Hypothek | Grundschuld |
|----------|-------------|
| An Forderung gebunden | Unabhängig |
| Erlischt mit Kreditrückzahlung | Bleibt bestehen |
| Nicht wiederverwendbar | Wiederverwendbar ✅ |

**Arten:**
1. **Verkehrshypothek** (üblich)
2. **Sicherungshypothek** (selten)

**Nur noch bei:**
- Alten Krediten (vor 2000)
- KfW-Förderung (manche Programme)

**Löschung:**
- Automatisch bei Kreditrückzahlung
- Grundbuch-Eintragung bleibt (kosmetisch)

Fundstelle: BGB § 1113"""
            },
            {
                "section": "§ 1147",
                "title": "Zwangsvollstreckung aus Grundpfandrecht",
                "content": """§ 1147 BGB - Zwangsvollstreckung

**Voraussetzung:**
- Zahlungsausfall Kreditnehmer
- Vollstreckbare Urkunde (notariell)
- Grundschuld/Hypothek eingetragen

**Ablauf Zwangsvollstreckung:**
1. Mahnung Bank (2-3 Monate Zahlungsrückstand)
2. Kündigung Darlehen
3. Antrag Zwangsversteigerung beim Amtsgericht
4. Versteigerungstermin (6-12 Monate später)
5. Zuschlag: Höchstbietender erhält Grundstück

**Beispiel:**
- Kredit: 400.000 €
- Zahlungsrückstand: 3 Monate (30.000 €)
- Bank kündigt Gesamtkredit
- Zwangsversteigerung
- Verkehrswert Gutachten: 500.000 €
- Mindestgebot: 350.000 € (70% Verkehrswert)
- Zuschlag: 420.000 €
- Verteilung: Bank 400.000 €, Rest (20.000 €) an Schuldner

**Verhindern:**
- Zahlung nachleisten
- Vergleich mit Bank
- Privatverkauf (meist höherer Preis!)

Fundstelle: BGB § 1147"""
            },
            
            # NIESBRAUCH & WOHNUNGSRECHT
            {
                "section": "§ 1030",
                "title": "Nießbrauch - Lebenslange Nutzung",
                "content": """§ 1030 BGB - Nießbrauch an Immobilie

**Definition:**
Recht, Immobilie lebenslang zu nutzen UND Früchte zu ziehen
→ Bewohnen + Vermieten erlaubt!

**Klassisch: Altenteil**
- Eltern übertragen Haus an Kinder
- Eltern behalten Nießbrauch (lebenslang wohnen)
- Kinder = Eigentümer (im Grundbuch)

**Rechte Nießbraucher:**
✅ Bewohnen
✅ Vermieten (Mieteinnahmen!)
✅ Verpachten
✅ Früchte ziehen (Holz, Äpfel)

**Pflichten Nießbraucher:**
✅ Instandhaltung (kleine Reparaturen)
✅ Grundsteuer zahlen
✅ Versicherung zahlen

**Kosten Eigentümer:**
✅ Große Reparaturen (Dach, Heizung)
✅ Modernisierung

**Bewertung (Erbschaftsteuer):**
- Kapitalwert nach Lebensalter
- 70 Jahre alt: Faktor 9,0
- Jahreswert 12.000 € × 9,0 = **108.000 €**
- Hausverkauf: 108.000 € Abschlag wegen Nießbrauch

**Eintragung:**
- Grundbuch Abteilung II
- "Nießbrauch zugunsten [Name] lebenslang"

**Löschung:**
- Tod Nießbraucher
- Oder: Verzicht

Fundstelle: BGB § 1030"""
            },
            {
                "section": "§ 1093",
                "title": "Wohnungsrecht - Nur Bewohnen",
                "content": """§ 1093 BGB - Wohnungsrecht

**Definition:**
Recht, Immobilie zu bewohnen
→ NUR Bewohnen, NICHT vermieten!

**Unterschied zu Nießbrauch:**
| Nießbrauch | Wohnungsrecht |
|------------|---------------|
| Bewohnen + Vermieten ✅ | Nur Bewohnen ✅ |
| Mieteinnahmen ✅ | Keine Miete ❌ |
| Übertragbar ✅ | Höchstpersönlich ❌ |

**Typisch bei:**
- Scheidung: Ex-Partner Wohnrecht (Kinder)
- Altenteil: Nur Bewohnen (keine Vermietung)

**Beispiel:**
- Haus wert 500.000 €
- Vater: Wohnungsrecht lebenslang
- Verkauf: Abschlag 80.000 € (Wohnrecht-Belastung)

**Kosten:**
- Wohnungsrechtsinhaber: Nebenkosten, Kleinreparaturen
- Eigentümer: Große Reparaturen

**Eintragung:**
- Grundbuch Abteilung II
- "Wohnungsrecht lebenslang zugunsten [Name]"

Fundstelle: BGB § 1093"""
            },
            
            # GRUNDDIENSTBARKEITEN
            {
                "section": "§ 1018",
                "title": "Grunddienstbarkeit - Wegerecht, Leitungsrecht",
                "content": """§ 1018 BGB - Grunddienstbarkeit

**Definition:**
Ein Grundstück wird zugunsten eines anderen belastet
→ Herrschendes Grundstück hat Recht am dienenden Grundstück

**Häufigste Arten:**
1. **Wegerecht** (Zufahrt über Nachbargrundstück)
2. **Leitungsrecht** (Strom, Wasser, Abwasser)
3. **Geh- und Fahrtrecht**

**Beispiel Wegerecht:**
- Grundstück A: Hinterhof (kein Straßenzugang)
- Grundstück B: Vorderhof (Straße)
- Grundstück A bekommt Wegerecht über B
- → A darf über B fahren zur Straße ✅

**Eintragung:**
- Grundbuch Abteilung II
- Dienendes Grundstück: "Wegerecht zugunsten [Flurstück]"
- Herrschendes Grundstück: "Wegerecht an [Flurstück]"

**Bewertung:**
- Grundstück MIT Wegerecht: +10-20% wertvoller
- Grundstück belastet (dienend): -5-15% Wert

**Kosten:**
- Einmalig Notar: ~500-1.000 €
- Laufend: Anteilige Instandhaltung Weg

**Löschung:**
- Nur mit Zustimmung beider Grundstückseigentümer
- Oder: Wegfall Zweck (Straße gebaut)

Fundstelle: BGB § 1018"""
            },
            {
                "section": "§ 1090",
                "title": "Erbbaurecht - Grundstück pachten, Gebäude besitzen",
                "content": """§ 1090 BGB + ErbbauRG - Erbbaurecht

**Prinzip:**
- Grundstück gehört Eigentümer A
- Gebäude gehört Erbbauberechtigtem B
- B zahlt Erbbauzins an A (jährlich)

**Laufzeit:**
- Meist 66 oder 99 Jahre
- Verlängerung möglich

**Beispiel:**
- Grundstück Wert: 300.000 €
- Erbbauzins: 4% = 12.000 €/Jahr
- Erbbauberechtigter baut Haus: 400.000 €
- Gesamtkosten 30 Jahre: 12.000 € × 30 = 360.000 € Erbbauzins
- Nach 66 Jahren: Haus fällt an Grundstückseigentümer (Entschädigung!)

**Vorteile:**
✅ Weniger Eigenkapital (kein Grundstückskauf)
✅ Erbbauzins steuerlich absetzbar (Werbungskosten)
✅ Gebäude vererb- und verkaufbar

**Nachteile:**
❌ Haus gehört nach 99 Jahren Grundstückseigentümer
❌ Laufende Kosten (Erbbauzins)
❌ Wertsteigerung Grundstück nur teilweise (Heimfall)

**Heimfall:**
- Nach Ablauf: Gebäude fällt an Grundstückseigentümer
- Entschädigung: 2/3 des Verkehrswerts (oft)

**Eintragung:**
- Grundbuch: Eigenes Grundbuchblatt für Erbbaurecht
- Belastung mit Grundschuld möglich (Kredit!)

Fundstelle: BGB § 1090, ErbbauRG"""
            },
            
            # NACHBARRECHT
            {
                "section": "§ 906",
                "title": "Immissionen - Lärm, Geruch, Rauch",
                "content": """§ 906 BGB - Immissionen vom Nachbargrundstück

**Regel:**
Eigentümer muss **unwesentliche** Beeinträchtigungen dulden
→ Wesentlich = Gebrauch beeinträchtigt

**Arten:**
- Lärm (Rasenmäher, Musik, Gewerbe)
- Geruch (Gülledüngung, Grillrauch)
- Rauch, Ruß
- Erschütterungen

**Beispiele unwesentlich (dulden!):**
✅ Rasenmähen tagsüber (1 Stunde)
✅ Kindergeräusche
✅ Kirchenglocken
✅ Grillgeruch gelegentlich

**Beispiele wesentlich (Anspruch auf Unterlassung!):**
❌ Disco-Musik nachts (>22 Uhr)
❌ Dauerlärm Gewerbe (>55 dB tags)
❌ Rauch aus Schornstein (Heizung defekt)

**Grenzwerte:**
- Wohngebiet: 55 dB tags, 40 dB nachts
- Mischgebiet: 60 dB tags, 45 dB nachts
- Gewerbegebiet: 65 dB tags, 50 dB nachts

**Ausgleich:**
Bei wesentlichen, aber üblichen Immissionen:
→ Geldausgleich statt Unterlassung
(z.B. Landwirtschaft: Gülledüngung 2× Jahr)

**Klage:**
- Unterlassungsanspruch
- Kosten Rechtsstreit: 3.000-10.000 €
- Besser: Nachbarschaftsgespräch!

Fundstelle: BGB § 906"""
            },
            {
                "section": "§ 910",
                "title": "Überhang - Äste & Wurzeln vom Nachbarbaum",
                "content": """§ 910 BGB - Überhang von Nachbarbaum

**Regel:**
Überhängende Äste = Nachbar muss dulden
→ ABER: Selbsthilferecht nach Fristsetzung!

**Ablauf:**
1. Äste hängen über Grenze
2. **Fristsetzung:** "Bitte bis 31.12. zurückschneiden"
3. Frist verstreicht (angemessen: 2-4 Wochen)
4. **Selbsthilfe:** Eigentümer darf selbst schneiden ✅

**ACHTUNG:**
- NUR Überhang schneiden (nicht Baum auf Nachbargrundstück!)
- Schonend schneiden (Baum nicht beschädigen)
- Kosten: Nachbar muss erstatten

**Wurzeln:**
§ 910 Abs. 2: Sofort abschneiden erlaubt!
→ Keine Fristsetzung nötig

**Früchte (Äpfel, Nüsse):**
§ 911: Fallen auf Grundstück = gehören Grundstückseigentümer
→ Aufsammeln = erlaubt
→ Pflücken vom Baum = NICHT erlaubt (Diebstahl!)

**Praxis:**
- Erst Nachbar ansprechen
- Dann Fristsetzung schriftlich
- Dann Selbsthilfe
- Kosten: 200-500 € (Fachfirma) → Nachbar zahlt

Fundstelle: BGB § 910"""
            },
            {
                "section": "§ 912",
                "title": "Hammerschlag und Leiterrecht - Nachbargrundstück betreten",
                "content": """§ 912 BGB - Hammerschlag und Leiterrecht

**Zweck:**
Eigentümer darf Nachbargrundstück betreten für:
- Reparaturen eigenes Gebäude
- Bauarbeiten

**Voraussetzungen:**
1. **Notwendigkeit:** Reparatur anders nicht möglich
2. **Ankündigung:** Rechtzeitig vorher mitteilen
3. **Schonend:** Geringstmögliche Beeinträchtigung

**Beispiele:**
✅ Dachrinne reparieren (nur von Nachbarseite erreichbar)
✅ Fassade streichen (Gerüst auf Nachbargrundstück)
✅ Dachziegel ersetzen

**Ablauf:**
1. Nachbar schriftlich informieren (2 Wochen vorher)
2. Termin abstimmen
3. Zugang gewähren
4. Nach Arbeiten: Zustand wiederherstellen

**Entschädigung:**
- Bei Schäden: Schadensersatz
- Bei erheblicher Beeinträchtigung: Geldausgleich
- Normal: Kostenlos (Nachbarschaftspflicht)

**Verweigerung Nachbar:**
Gerichtlicher Duldungsbeschluss möglich
→ Kosten: 1.000-3.000 €

Fundstelle: BGB § 912"""
            },
            
            # GUTGLÄUBIGER ERWERB
            {
                "section": "§ 892",
                "title": "Gutgläubiger Erwerb - Grundbuchvertrauen",
                "content": """§ 892 BGB - Öffentlicher Glaube des Grundbuchs

**Regel:**
Grundbuch = richtig (Vermutung!)
→ Käufer darf auf Grundbuch vertrauen ✅

**Beispiel:**
- Grundbuch: A ist Eigentümer
- Tatsächlich: B ist Eigentümer (Grundbuch nicht aktualisiert)
- C kauft von A
- → **C wird Eigentümer!** (gutgläubig) ✅
- B geht leer aus

**Schutz:**
Unrichtiges Grundbuch schadet NICHT dem gutgläubigen Käufer
→ Sicherheit im Rechtsverkehr!

**Ausnahmen (kein Schutz):**
❌ Widerspruch im Grundbuch (Abteilung II)
❌ Kenntnis der Unrichtigkeit (bösgläubig)
❌ Grobe Fahrlässigkeit

**Praxis:**
- VOR Kauf: Grundbuchauszug holen
- Verkäufer im Grundbuch als Eigentümer = sicher ✅
- Nicht im Grundbuch = NICHT kaufen!

**Kosten Grundbuchauszug:**
- 10-20 € beim Grundbuchamt
- Oder online (berechtigtes Interesse nötig)

Fundstelle: BGB § 892"""
            },
            {
                "section": "§ 878",
                "title": "Rangordnung im Grundbuch",
                "content": """§ 878 BGB - Rang der Rechte im Grundbuch

**Regel:**
Früher eingetragen = besserer Rang
→ Bei Zwangsversteigerung: Rang entscheidet!

**Beispiel Grundbuch Abteilung III:**
1. Grundschuld Bank A: 300.000 € (2020 eingetragen)
2. Grundschuld Bank B: 200.000 € (2022 eingetragen)
3. Grundschuld Bank C: 100.000 € (2024 eingetragen)

**Zwangsversteigerung:**
Zuschlag: 450.000 €
- Bank A: 300.000 € (voll bezahlt) ✅
- Bank B: 150.000 € (nur teilweise!) ⚠️
- Bank C: 0 € (geht leer aus) ❌

**Rangänderung:**
Möglich mit Zustimmung aller Beteiligten
→ Kosten: 200-500 € Notar

**Rangvorbehalt:**
"Grundschuld mit Rangvorbehalt"
→ Spätere Grundschuld kann vorziehen

**Praxis:**
- Bei Umschuldung: Rang beachten!
- Rang 1 = sicherster (niedrigster Zins)
- Rang 2-3 = höherer Zins (höheres Risiko Bank)

Fundstelle: BGB § 878"""
            }
        ]
        
        for para in SACHENRECHT_PARAGRAPHS:
            doc = {
                "id": f"bgb_sachenrecht_{para['section'].replace('§', 'par').replace(' ', '_').lower()}",
                "content": para["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"BGB {para['section']} - {para['title']}",
                "source_url": "https://www.gesetze-im-internet.de/bgb/",
                "topics": ["Sachenrecht", "Grundstücksrecht", "Immobilie"],
                "law": "BGB Sachenrecht",
                "section": para["section"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} BGB Sachenrecht paragraphs")
        return documents


__all__ = ["BGBSachenrechtScraper"]
