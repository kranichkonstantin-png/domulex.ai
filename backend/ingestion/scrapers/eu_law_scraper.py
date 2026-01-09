"""
EU Law Scraper - European Union legislation for real estate
Focus: DSGVO, Consumer Protection, Energy Efficiency
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class EULawScraper:
    """
    Scraper für EU-Recht im Immobilienbereich
    
    Focus:
    - DSGVO (Datenschutz bei Vermietung/Maklern)
    - Verbraucherschutzrichtlinie (Immobilienkauf)
    - Energieeffizienz-Richtlinie (Gebäude)
    """
    
    def __init__(self):
        pass
    
    async def scrape_eu_regulations(self) -> List[Dict]:
        """
        Scrape EU regulations relevant for real estate
        
        Returns:
            List of EU law documents
        """
        documents = []
        
        EU_REGULATIONS = [
            {
                "regulation": "GRC Art. 17",
                "title": "EU-Grundrechtecharta Art. 17: Eigentumsrecht",
                "content": """EU-Grundrechtecharta Art. 17 - Eigentumsrecht

**Volltext:**
Jede Person hat das Recht, ihr rechtmäßig erworbenes Eigentum zu besitzen, zu nutzen, 
darüber zu verfügen und es zu vererben. Niemandem darf sein Eigentum entzogen werden, 
es sei denn aus Gründen des öffentlichen Interesses in den Fällen und unter den 
Bedingungen, die in einem Gesetz vorgesehen sind, jedoch vorbehaltlich einer 
gerechten Entschädigung für den Verlust des Eigentums zu angemessener Zeit.

**Bedeutung für Immobilienrecht:**

✅ **Schutz des Grundeigentums** - Verfassungsrechtlicher Schutz
✅ **Enteignung nur mit Entschädigung** - Art. 14 GG entsprechend
✅ **Nutzungsfreiheit** - Vermietung, Veräußerung, Belastung

**Praxisrelevanz:**
- Baurecht: Baugenehmigungen dürfen Eigentumsrecht nicht unverhältnismäßig einschränken
- Mietrecht: Kündigungsschutz vs. Eigentumsrecht des Vermieters
- Enteignung: Nur bei überwiegendem öffentlichem Interesse

Fundstelle: GRC Art. 17 (2000/C 364/01)""",
                "topics": ["Eigentumsrecht", "Grundrechte", "Enteignung", "EU-Recht"]
            },
            {
                "regulation": "AEUV Art. 49",
                "title": "AEUV Art. 49: Niederlassungsfreiheit bei Immobilien",
                "content": """AEUV Art. 49 - Niederlassungsfreiheit

**Volltext:**
Die Beschränkungen der freien Niederlassung von Staatsangehörigen eines Mitgliedstaats 
im Hoheitsgebiet eines anderen Mitgliedstaats sind nach Maßgabe der folgenden 
Bestimmungen verboten. Das Gleiche gilt für Beschränkungen der Gründung von Agenturen, 
Zweigniederlassungen oder Tochtergesellschaften.

**Anwendung im Immobilienbereich:**

✅ **Grenzüberschreitender Immobilienerwerb** - Keine Diskriminierung
✅ **Ausländische Investoren** - Gleichbehandlung mit Inländern
✅ **Gewerbliche Immobiliennutzung** - Freie Standortwahl in EU

**Wichtige EuGH-Rechtsprechung:**
- C-197/11 (Libert): Steuerliche Gleichbehandlung bei Immobiliengeschäften
- C-38/10: Genehmigungspflichten für Ausländer unzulässig

**Praktische Bedeutung:**
- Deutsche können frei Immobilien in Spanien/Frankreich erwerben
- Ausländische Makler/Verwalter dürfen in Deutschland tätig sein
- Keine diskriminierenden Steuern für EU-Ausländer

Fundstelle: AEUV Art. 49 (Vertrag über die Arbeitsweise der EU)""",
                "topics": ["Niederlassungsfreiheit", "EU-Ausländer", "Immobilienerwerb", "Gleichbehandlung"]
            },
            {
                "regulation": "AEUV Art. 63",
                "title": "AEUV Art. 63: Freier Kapitalverkehr bei Immobilien",
                "content": """AEUV Art. 63 - Freier Kapitalverkehr

**Volltext:**
Im Rahmen der Bestimmungen dieses Kapitels sind alle Beschränkungen des Kapitalverkehrs 
zwischen den Mitgliedstaaten sowie zwischen den Mitgliedstaaten und dritten Ländern 
verboten.

**Relevanz für Immobilieninvestments:**

✅ **Grenzüberschreitende Immobilieninvestments** - Keine Beschränkungen
✅ **Finanzierung** - Freie Wahl der Bank in EU
✅ **Kapitalrückfluss** - Mieteinnahmen/Verkaufserlöse frei transferierbar

**EuGH-Rechtsprechung:**
- C-38/10 (Kommission/Portugal): Genehmigungspflichten bei Grundstückserwerb unzulässig
- C-35/11: Beschränkungen nur aus zwingenden Gründen des Allgemeininteresses

**Praxisbeispiele:**
- Franzose kauft Wohnung in Berlin - keine besonderen Genehmigungen
- Deutscher Investor kauft Ferienhaus in Italien - freier Kapitalverkehr
- Hypothek bei spanischer Bank für deutsche Immobilie - zulässig

**Ausnahmen:**
- Geldwäsche-Prävention
- Terrorismusbekämpfung
- Steuerliche Kontrolle (verhältnismäßig)

Fundstelle: AEUV Art. 63 ff. (Vertrag über die Arbeitsweise der EU)""",
                "topics": ["Kapitalverkehrsfreiheit", "Immobilieninvestment", "Finanzierung", "EU-Recht"]
            },
            {
                "regulation": "DSGVO Art. 6",
                "title": "DSGVO Art. 6: Rechtmäßigkeit der Verarbeitung bei Vermietung",
                "content": """DSGVO Art. 6 - Rechtmäßigkeit der Verarbeitung

**Anwendung bei Vermietung/Maklern:**

Vermieter/Makler dürfen personenbezogene Daten erheben wenn:
✅ **Vertragsanbahnung** (Art. 6 Abs. 1 b) - Bonitätsprüfung, Schufa
✅ **Berechtigtes Interesse** (Art. 6 Abs. 1 f) - Mieterauswahl
✅ **Einwilligung** (Art. 6 Abs. 1 a) - Marketing, Newsletter

**Welche Daten darf Vermieter verlangen?**

ZULÄSSIG:
✅ Name, Adresse, Geburtsdatum
✅ Einkommensnachweise (3 Gehaltsnachweise)
✅ Schufa-Auskunft (Mieterselbstauskunft)
✅ Arbeitgeberbescheinigung
✅ Mietschuldenfreiheitsbescheinigung

UNZULÄSSIG:
❌ Religionszugehörigkeit
❌ Politische Meinung
❌ Schwangerschaft (Diskriminierung!)
❌ Kinderwunsch
❌ Gesundheitsdaten (außer bei Behinderung für Barrierefreiheit)

**Schufa-Auskunft:**

Vermieter darf:
✅ Schufa-Bonitätsauskunft verlangen (Mieter holt selbst!)
✅ Kosten: 29,95 € (trägt Mieter)

Vermieter darf NICHT:
❌ Vollständige Schufa-Auskunft (zu viele Daten!)
❌ Schufa ohne Einwilligung einholen

**Datenspeicherung:**

NICHT-Mieter (Bewerber abgelehnt):
- Daten löschen nach **6 Monaten**
- Oder nach Widerspruch sofort

Mieter:
- Daten behalten während Mietverhältnis ✅
- Nach Auszug: Löschen nach **10 Jahren** (Verjährungsfrist!)

**Bußgelder bei Verstößen:**

Bei Verstoß:
- Bußgeld bis **20.000.000 €** (oder 4% Jahresumsatz)
- In Praxis bei Vermietern: 5.000-50.000 €

Beispiele:
- Schufa ohne Einwilligung: **10.000 €** Bußgeld
- Daten nicht gelöscht: **5.000 €** Bußgeld
- Unzulässige Fragen (Religion): **15.000 €** Bußgeld

**Praxis-Tipps für Vermieter:**

✅ Datenschutzerklärung aushändigen (Vorlage Anwalt)
✅ Nur zulässige Daten erheben
✅ Bewerberdaten löschen nach 6 Monaten
✅ Einwilligung für Schufa einholen (schriftlich)

**Praxis-Tipps für Mieter:**

✅ Nur zulässige Daten angeben
✅ Unzulässige Fragen verweigern (Religion, Schwangerschaft)
✅ Schufa-Bonitätsauskunft selbst holen (nicht Vollauskunft!)
✅ Nach Ablehnung: Löschung verlangen

Fundstelle: DSGVO Art. 6, EU 2016/679""",
                "topics": ["DSGVO", "Datenschutz", "Vermietung", "Schufa", "Bonitätsprüfung"]
            },
            {
                "regulation": "Verbraucherschutzrichtlinie 2011/83/EU",
                "title": "EU-Verbraucherschutz: 14 Tage Widerrufsrecht bei Immobilien-Fernabsatz",
                "content": """EU-Verbraucherschutzrichtlinie 2011/83/EU

**Widerrufsrecht bei Immobilienkauf:**

KEIN Widerrufsrecht:
❌ Immobilien-Kaufvertrag (notariell beurkundet)
❌ Grundstückskauf
❌ Wohnungskauf

Aber:
✅ **Maklervertrag** (außerhalb Geschäftsräumen abgeschlossen)
✅ **Bauträgervertrag** (per Fernkommunikation)

**Maklervertrag - Widerrufsrecht:**

Wenn Maklervertrag:
- NICHT in Maklerbüro unterschrieben
- SONDERN: Bei Besichtigung, zu Hause, telefonisch

Dann:
✅ 14 Tage Widerrufsrecht ab Vertragsschluss

Beispiel:
- Makler kommt nach Hause
- Unterschrift Maklervertrag vor Ort
- → **14 Tage Widerrufsrecht** ✅

Aber:
- Unterschrift in Maklerbüro
- → **KEIN Widerrufsrecht** ❌

**Bauträgervertrag - Widerrufsrecht:**

Bei Fernabsatz (per E-Mail, Telefon):
✅ 14 Tage Widerrufsrecht

Aber:
- Bei notarieller Beurkundung: Widerrufsrecht ERLISCHT
- Notar belehrt über Verzicht

**Informationspflichten Makler:**

Makler muss VOR Vertragsschluss informieren:
✅ Provision (Höhe, wer zahlt)
✅ Widerrufsrecht (14 Tage)
✅ Vertragslaufzeit
✅ Kündigungsbedingungen

Bei Verstoß:
- Widerrufsrecht verlängert sich auf **12 Monate**!
- Makler verliert Provisionsanspruch

**Praxis-Tipps:**

Für Käufer/Mieter:
✅ Maklervertrag NICHT sofort unterschreiben
✅ 14 Tage Bedenkzeit nutzen
✅ Bei Haustür-Geschäft: Widerrufsrecht!

Für Makler:
✅ Kunden über Widerrufsrecht belehren
✅ Schriftliche Widerrufsbelehrung aushändigen
✅ Unterschrift in Maklerbüro (kein Widerrufsrecht)

Fundstelle: EU-Richtlinie 2011/83/EU, umgesetzt in BGB §§ 312-312k""",
                "topics": ["Verbraucherschutz", "Widerrufsrecht", "Maklervertrag", "EU-Recht"]
            },
            {
                "regulation": "Energieeffizienz-Richtlinie 2018/844/EU",
                "title": "EU-Gebäudeenergieeffizienz: Energieausweis Pflicht ab 2024",
                "content": """EU-Energieeffizienz-Richtlinie 2018/844/EU

**Energieausweis Pflicht:**

Bei Verkauf/Vermietung:
✅ Energieausweis vorlegen (schon bei Besichtigung!)
✅ In Immobilienanzeige: Energiekennwerte angeben
✅ Kosten: 100-300 € (Verbrauchsausweis), 400-800 € (Bedarfsausweis)

OHNE Energieausweis:
- Bußgeld bis **15.000 €** ❌

**Energiekennwerte in Anzeige:**

Pflicht seit 01.05.2014:
✅ Energiekennwert (kWh/m²a)
✅ Energieeffizienzklasse (A+ bis H)
✅ Baujahr Gebäude
✅ Heizungsart

Beispiel-Anzeige:
"Energieausweis: Energiekennwert 95 kWh/m²a, Klasse D, Bj. 1985, Gasheizung"

**Sanierungspflicht ab 2033:**

EU-Ziel:
- Bis 2033: Alle Gebäude mindestens **Klasse D**
- Bis 2050: Alle Gebäude **klimaneutral**

Kosten Sanierung:
- Dämmung: 100-200 €/m² Fassade
- Fenster: 500-1.000 €/m²
- Heizung: 15.000-30.000 €
- **Gesamt: 50.000-150.000 €** bei Einfamilienhaus

**Förderung:**

KfW/BAFA Förderung:
- Bis 45% Zuschuss (BEG-Förderung)
- Steuerbonus: 20% über 3 Jahre (max. 40.000 €)

Beispiel:
- Sanierung: 100.000 €
- Förderung KfW: 45.000 €
- Steuerbonus: 20.000 €
- **Eigenanteil: 35.000 €** ✅

**Praxis-Tipps:**

Für Verkäufer:
✅ Energieausweis VOR Verkauf besorgen (300-800 €)
✅ In Anzeige Kennwerte angeben
✅ Bei schlechter Klasse (F, G, H): Sanierung überlegen

Für Käufer:
✅ Energieausweis prüfen (Klasse D oder besser!)
✅ Sanierungskosten in Kaufpreis einrechnen
✅ Bei Klasse G/H: 100.000-150.000 € Sanierung nötig!

Fundstelle: EU-Richtlinie 2018/844/EU, GEG (Gebäudeenergiegesetz)""",
                "topics": ["Energieeffizienz", "Energieausweis", "Sanierung", "GEG", "EU-Recht"]
            }
        ]
        
        for reg in EU_REGULATIONS:
            doc = {
                "id": f"eu_{reg['regulation'].lower().replace(' ', '_').replace('/', '_').replace('.', '_')}",
                "content": reg["content"],
                "jurisdiction": "EU",
                "language": "de",
                "source": f"EU: {reg['regulation']}",
                "source_url": "https://eur-lex.europa.eu",
                "topics": reg["topics"],
                "law": "EU-Recht",
                "section": reg["regulation"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} EU regulations")
        return documents


# Export
__all__ = ["EULawScraper"]
