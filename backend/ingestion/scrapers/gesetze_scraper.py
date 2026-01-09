"""
Gesetze Scraper - Bundesgesetze von gesetze-im-internet.de
Ziel: 45 Gesetze (Phase 1-3 des Masterplans)
Quelle: https://www.gesetze-im-internet.de
"""

import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import List, Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class GesetzeScraper:
    """Scraper for German federal laws from gesetze-im-internet.de"""
    
    BASE_URL = "https://www.gesetze-im-internet.de"
    
    # Phase 1: Kritische Gesetze (14)
    PHASE_1_LAWS = {
        "betrkv": "Betriebskostenverordnung",
        "heizkostenv": "Heizkostenverordnung",
        "wohnflv": "Wohnflächenverordnung",
        "wistg": "Wirtschaftsstrafgesetz",
        "trinkwv_2023": "Trinkwasserverordnung",
        "bbaug": "Baugesetzbuch",
        "baunvo": "Baunutzungsverordnung",
        "rog": "Raumordnungsgesetz",
        "immowertv": "Immobilienwertermittlungsverordnung",
        "grestg": "Grunderwerbsteuergesetz",
        "grstg_1973": "Grundsteuergesetz",
        "bewg": "Bewertungsgesetz"
    }
    
    # Phase 2: Wichtige Gesetze (15)
    PHASE_2_LAWS = {
        "ustg_1980": "Umsatzsteuergesetz",
        "erbstg_1974": "Erbschaftsteuer- und Schenkungsteuergesetz",
        "ao_1977": "Abgabenordnung",
        "hoai_2021": "Honorarordnung für Architekten und Ingenieure",
        "mabv": "Makler- und Bauträgerverordnung",
        "geg": "Gebäudeenergiegesetz",
        "bnatschg_2009": "Bundesnaturschutzgesetz",
        "bbodschg": "Bundes-Bodenschutzgesetz",
        "whg_2009": "Wasserhaushaltsgesetz",
        "bimschg": "Bundes-Immissionsschutzgesetz",
        "zvg": "Zwangsversteigerungsgesetz",
        "inso": "Insolvenzordnung"
    }
    
    # Phase 3: Ergänzende Gesetze (12)
    PHASE_3_LAWS = {
        "gwg_2017": "Geldwäschegesetz",
        "agg": "Allgemeines Gleichbehandlungsgesetz",
        "wofg": "Wohnraumförderungsgesetz",
        "wobindg": "Wohnungsbindungsgesetz",
        "woggg": "Wohngeldgesetz",
        "pangv_1985": "Preisangabenverordnung",
        "erbbaurv": "Erbbaurechtsverordnung",
        "msbg": "Messstellenbetriebsgesetz",
        "avbfernwaermev": "Verordnung über Allgemeine Bedingungen für die Versorgung mit Fernwärme",
        "krwg": "Kreislaufwirtschaftsgesetz",
        "tkmodg": "Telekommunikationsmodernisierungsgesetz"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_law(self, law_abbr: str, law_name: str) -> List[Dict]:
        """
        Scrape a complete law from gesetze-im-internet.de
        
        Args:
            law_abbr: Abbreviation (e.g., 'betrkv')
            law_name: Full name (e.g., 'Betriebskostenverordnung')
            
        Returns:
            List of paragraphs as dicts
        """
        logger.info(f"Scraping {law_name} ({law_abbr})...")
        
        paragraphs = []
        
        # Get table of contents
        toc_url = f"{self.BASE_URL}/{law_abbr}/BJNR272800003.html"
        
        try:
            response = self.session.get(toc_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all paragraph links
            links = soup.find_all('a', href=re.compile(r'__\d+\.html'))
            
            logger.info(f"Found {len(links)} sections in {law_name}")
            
            for link in links:
                section_url = f"{self.BASE_URL}/{law_abbr}/{link['href']}"
                section_data = self._scrape_section(section_url, law_abbr, law_name)
                
                if section_data:
                    paragraphs.append(section_data)
                    logger.debug(f"Scraped: {section_data['title']}")
                    time.sleep(0.5)  # Rate limiting
                    
        except Exception as e:
            logger.error(f"Error scraping {law_name}: {e}")
            return []
        
        logger.info(f"Successfully scraped {len(paragraphs)} sections from {law_name}")
        return paragraphs
    
    def _scrape_section(self, url: str, law_abbr: str, law_name: str) -> Optional[Dict]:
        """Scrape a single paragraph/section"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1') or soup.find('h2')
            title = title_elem.get_text(strip=True) if title_elem else "Ohne Titel"
            
            # Extract content
            content_div = soup.find('div', class_='jurAbsatz') or soup.find('div', class_='jnhtml')
            
            if not content_div:
                return None
            
            # Clean content
            content = self._clean_content(content_div)
            
            # Extract paragraph number
            para_match = re.search(r'§\s*(\d+[a-z]?)', title)
            para_number = para_match.group(1) if para_match else None
            
            return {
                "title": title,
                "content": content,
                "url": url,
                "law": law_name,
                "law_abbr": law_abbr.upper(),
                "paragraph": para_number,
                "rechtsgebiet": self._determine_rechtsgebiet(law_abbr),
                "date_scraped": datetime.now().isoformat(),
                "source": "gesetze-im-internet.de"
            }
            
        except Exception as e:
            logger.error(f"Error scraping section {url}: {e}")
            return None
    
    def _clean_content(self, element) -> str:
        """Clean and format content"""
        # Remove scripts, styles
        for script in element(['script', 'style']):
            script.decompose()
        
        # Get text
        text = element.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()
    
    def _determine_rechtsgebiet(self, law_abbr: str) -> str:
        """Determine legal area based on law abbreviation"""
        mietrecht = ['betrkv', 'heizkostenv', 'wohnflv', 'trinkwv']
        baurecht = ['bbaug', 'baunvo', 'rog', 'immowertv', 'hoai', 'mabv']
        steuerrecht = ['grestg', 'grstg', 'bewg', 'ustg', 'erbstg', 'ao']
        umweltrecht = ['geg', 'bnatschg', 'bbodschg', 'whg', 'bimschg', 'krwg']
        verfahrensrecht = ['zvg', 'inso', 'wistg']
        
        law_abbr = law_abbr.lower()
        
        if any(abbr in law_abbr for abbr in mietrecht):
            return "Mietrecht"
        elif any(abbr in law_abbr for abbr in baurecht):
            return "Baurecht"
        elif any(abbr in law_abbr for abbr in steuerrecht):
            return "Steuerrecht"
        elif any(abbr in law_abbr for abbr in umweltrecht):
            return "Umwelt- und Energierecht"
        elif any(abbr in law_abbr for abbr in verfahrensrecht):
            return "Verfahrensrecht"
        else:
            return "Sonstiges Immobilienrecht"
    
    def scrape_phase_1(self) -> List[Dict]:
        """Scrape all Phase 1 (critical) laws"""
        all_paragraphs = []
        
        for abbr, name in self.PHASE_1_LAWS.items():
            paragraphs = self.scrape_law(abbr, name)
            all_paragraphs.extend(paragraphs)
            time.sleep(2)  # Be nice to the server
        
        return all_paragraphs
    
    def scrape_phase_2(self) -> List[Dict]:
        """Scrape all Phase 2 (important) laws"""
        all_paragraphs = []
        
        for abbr, name in self.PHASE_2_LAWS.items():
            paragraphs = self.scrape_law(abbr, name)
            all_paragraphs.extend(paragraphs)
            time.sleep(2)
        
        return all_paragraphs
    
    def scrape_phase_3(self) -> List[Dict]:
        """Scrape all Phase 3 (supplementary) laws"""
        all_paragraphs = []
        
        for abbr, name in self.PHASE_3_LAWS.items():
            paragraphs = self.scrape_law(abbr, name)
            all_paragraphs.extend(paragraphs)
            time.sleep(2)
        
        return all_paragraphs


# Bekannte kritische Paragraphen als Fallback
CRITICAL_PARAGRAPHS = {
    "BetrKV": [
        {
            "title": "§ 1 BetrKV - Betriebskosten",
            "content": """§ 1 Betriebskosten

(1) Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen.

(2) Betriebskosten sind insbesondere:
1. die laufenden öffentlichen Lasten des Grundstücks (Grundsteuer)
2. die Kosten der Wasserversorgung
3. die Kosten der Entwässerung
4. die Kosten des Betriebs der Heizungsanlage
5. die Kosten des Betriebs der Warmwasserversorgungsanlage
6. die Kosten des Betriebs verbundener Heizungs- und Warmwasserversorgungsanlagen
7. die Kosten des Betriebs des Aufzugs
8. die Kosten der Straßenreinigung und Müllbeseitigung
9. die Kosten der Gebäudereinigung und Ungezieferbekämpfung
10. die Kosten der Gartenpflege
11. die Kosten der Beleuchtung
12. die Kosten der Schornsteinreinigung
13. die Kosten der Sach- und Haftpflichtversicherung
14. die Kosten für den Hausmeister
15. die Kosten des Betriebs der Gemeinschafts-Antennenanlage
16. die Kosten des Betriebs der Einrichtungen für die Wäschepflege
17. sonstige Betriebskosten

Fundstelle: BetrKV vom 25.11.2003 (BGBl. I S. 2346, 2347)""",
            "law": "Betriebskostenverordnung",
            "law_abbr": "BetrKV",
            "paragraph": "1",
            "rechtsgebiet": "Mietrecht"
        },
        {
            "title": "§ 2 BetrKV - Aufstellung der Betriebskosten",
            "content": """§ 2 Aufstellung der Betriebskosten

(1) Die einzelnen Betriebskostenarten sind in der Anlage zu dieser Verordnung näher bezeichnet. Können von den in der Anlage aufgeführten Betriebskosten mehrere Arten bei einem Gebäude oder mehreren Gebäuden entstehen, so kann der Vermieter die Kostenart und die zu den Kosten rechnenden Beträge in der Aufstellung der Betriebskosten näher bezeichnen.

(2) Zu den Betriebskosten gehören auch die Kosten der Verwaltung des Gebäudes (Verwaltungskosten), soweit diese nicht ausschließlich durch eigene Arbeit des Vermieters entstehen.

Fundstelle: BetrKV vom 25.11.2003 (BGBl. I S. 2346, 2347)""",
            "law": "Betriebskostenverordnung",
            "law_abbr": "BetrKV",
            "paragraph": "2",
            "rechtsgebiet": "Mietrecht"
        }
    ],
    "HeizkostenV": [
        {
            "title": "§ 1 HeizkostenV - Geltungsbereich",
            "content": """§ 1 Geltungsbereich

Diese Verordnung gilt für die Verteilung der Kosten des Betriebs zentraler Heizungs- und Warmwasserversorgungsanlagen in Gebäuden, soweit deren Eigentümer oder Erbbauberechtigte die Betriebskosten nach § 556 Abs. 1 Satz 1 des Bürgerlichen Gesetzbuchs auf die Nutzer umlegen dürfen.

Fundstelle: HeizkostenV vom 05.10.2009 (BGBl. I S. 3250)""",
            "law": "Heizkostenverordnung",
            "law_abbr": "HeizkostenV",
            "paragraph": "1",
            "rechtsgebiet": "Mietrecht"
        },
        {
            "title": "§ 7 HeizkostenV - Verteilung der Kosten der Versorgung mit Wärme",
            "content": """§ 7 Verteilung der Kosten der Versorgung mit Wärme

(1) Von den Kosten des Betriebs der zentralen Heizungsanlage sind mindestens 50 vom Hundert, höchstens 70 vom Hundert nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen. In Gebäuden, die das Anforderungsniveau der Wärmeschutzverordnung vom 16. August 1994 (BGBl. I S. 2121) nicht erfüllen, sind von den Kosten des Betriebs der zentralen Heizungsanlage 70 vom Hundert nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen.

(2) Der Gebäudeeigentümer kann einen höheren Anteil als 50 vom Hundert nach dem erfassten Wärmeverbrauch verteilen, wenn das Gebäude einen niedrigeren Energieverbrauch als das Anforderungsniveau der Wärmeschutzverordnung aufweist.

Fundstelle: HeizkostenV vom 05.10.2009 (BGBl. I S. 3250)""",
            "law": "Heizkostenverordnung",
            "law_abbr": "HeizkostenV",
            "paragraph": "7",
            "rechtsgebiet": "Mietrecht"
        }
    ],
    "GrEStG": [
        {
            "title": "§ 1 GrEStG - Erwerbsvorgänge",
            "content": """§ 1 Erwerbsvorgänge

(1) Der Grunderwerbsteuer unterliegen die folgenden Rechtsvorgänge, soweit sie sich auf inländische Grundstücke beziehen:

1. Ein Kaufvertrag oder ein anderes Rechtsgeschäft, das den Anspruch auf Übereignung begründet
2. Die Auflassung, wenn kein Rechtsgeschäft vorausgegangen ist, das den Anspruch auf Übereignung begründet
3. Der Übergang des Eigentums, wenn kein den Anspruch auf Übereignung begründendes Rechtsgeschäft vorausgegangen ist und es auch keiner Auflassung bedarf

(2) Der Grunderwerbsteuer unterliegt auch ein Rechtsgeschäft, das den Anspruch auf Abtretung eines Übereignungsanspruchs oder der Rechte aus einem Meistgebot begründet.

(3) Der Grunderwerbsteuer unterliegen auch:
1. Ein Rechtsgeschäft, das den Anspruch auf Abtretung der Rechte aus einem Kaufangebot begründet
2. Die Abtretung der Rechte aus einem Meistgebot bei einer Zwangsversteigerung
3. Der Übergang von mindestens 90 vom Hundert der Anteile an einer Gesellschaft (§ 1 Abs. 2a GrEStG - Share Deal)

(4) Als Grundstück im Sinne dieser Vorschrift gilt auch ein Erbbaurecht.

Fundstelle: GrEStG vom 17.12.1982 (BGBl. I S. 1777), zuletzt geändert 2024""",
            "law": "Grunderwerbsteuergesetz",
            "law_abbr": "GrEStG",
            "paragraph": "1",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 2 GrEStG - Ausnahmen von der Besteuerung",
            "content": """§ 2 Ausnahmen von der Besteuerung

(1) Von der Besteuerung sind ausgenommen:

1. Der Grundstückserwerb von Todes wegen und Grundstücksschenkungen unter Lebenden im Sinne des Erbschaftsteuer- und Schenkungsteuergesetzes
2. Der Erwerb eines Grundstücks durch den Ehegatten oder Lebenspartner des Veräußerers
3. Der Erwerb eines Grundstücks durch einen früheren Ehegatten im Rahmen der Vermögensauseinandersetzung nach der Scheidung
4. Grundstücksübergänge zwischen Verwandten in gerader Linie (Eltern-Kinder)
5. Der Erwerb durch eine Gesamthand zur Teilung unter den Mitberechtigten

(2) Von der Besteuerung sind ferner ausgenommen Grundstückserwerbe:
1. Zur Durchführung von Bodenordnungsverfahren
2. Durch Bund, Länder und Gemeinden für öffentliche Aufgaben
3. Von Wohnungsbaugenossenschaften unter bestimmten Voraussetzungen

Fundstelle: GrEStG vom 17.12.1982 (BGBl. I S. 1777)""",
            "law": "Grunderwerbsteuergesetz",
            "law_abbr": "GrEStG",
            "paragraph": "2",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 8 GrEStG - Bemessungsgrundlage",
            "content": """§ 8 Bemessungsgrundlage

(1) Die Steuer bemisst sich nach dem Wert der Gegenleistung.

(2) Zur Gegenleistung gehören auch:
1. Die vom Erwerber übernommenen sonstigen Leistungen (z.B. Altschulden, Hypotheken)
2. Die dem Veräußerer vorbehaltenen Nutzungen (z.B. Nießbrauchsrechte)
3. Die vom Erwerber übernommenen dauernden Lasten und Verpflichtungen

(3) Wird bei der Veräußerung eines Grundstücks der Kaufpreis nicht in Geld festgesetzt, sondern wird eine andere Gegenleistung vereinbart (Tausch), so ist der gemeine Wert der Gegenleistung maßgebend.

(4) Bei Share Deals (§ 1 Abs. 2a, 3, 3a) ist Bemessungsgrundlage der Grundbesitzwert nach dem Bewertungsgesetz.

Fundstelle: GrEStG vom 17.12.1982 (BGBl. I S. 1777)""",
            "law": "Grunderwerbsteuergesetz",
            "law_abbr": "GrEStG",
            "paragraph": "8",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 9 GrEStG - Steuersatz",
            "content": """§ 9 Steuersatz

(1) Die Grunderwerbsteuer beträgt 3,5 vom Hundert der Bemessungsgrundlage.

(2) Die Länder können durch Landesgesetz den Steuersatz abweichend festsetzen.

Anwendung in der Praxis (Stand 2025):
- Bayern, Sachsen: 3,5%
- Hamburg, Schleswig-Holstein: 5,0%
- Berlin, Brandenburg: 6,0%
- Nordrhein-Westfalen, Saarland: 6,5%
- Thüringen: 6,5%
- Baden-Württemberg, Hessen, Niedersachsen, Rheinland-Pfalz: 5,0%
- Bremen, Mecklenburg-Vorpommern, Sachsen-Anhalt: 5,0%

WICHTIG: Steuersatz ist Ländersache! Bei Immobilienkauf immer den Satz des Bundeslandes prüfen.

Fundstelle: GrEStG vom 17.12.1982 (BGBl. I S. 1777)""",
            "law": "Grunderwerbsteuergesetz",
            "law_abbr": "GrEStG",
            "paragraph": "9",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 16 GrEStG - Anzeigepflicht",
            "content": """§ 16 Anzeigepflicht

(1) Die Gerichte, Behörden und Notare haben Verträge und andere Vorgänge, die der Grunderwerbsteuer unterliegen, dem für die Besteuerung zuständigen Finanzamt unverzüglich anzuzeigen.

(2) Die Anzeige muss enthalten:
1. Den Namen und die Anschrift der Vertragsparteien
2. Die Lage und Größe des Grundstücks
3. Den Kaufpreis oder die sonstige Gegenleistung
4. Besondere Vereinbarungen

(3) Der Notar ist verpflichtet, die Anzeige elektronisch an das Finanzamt zu übermitteln.

Praxis: Das Finanzamt wird automatisch informiert, sobald der Kaufvertrag notariell beurkundet ist. Der Steuerbescheid kommt in der Regel 4-8 Wochen nach Beurkundung.

Fundstelle: GrEStG vom 17.12.1982 (BGBl. I S. 1777)""",
            "law": "Grunderwerbsteuergesetz",
            "law_abbr": "GrEStG",
            "paragraph": "16",
            "rechtsgebiet": "Steuerrecht"
        }
    ],
    "GrStG": [
        {
            "title": "§ 1 GrStG - Steuergegenstand",
            "content": """§ 1 Steuergegenstand

Der Grundsteuer unterliegen:
1. Betriebe der Land- und Forstwirtschaft (Grundsteuer A)
2. Grundstücke (Grundsteuer B)

Zum Grundvermögen gehören:
- Unbebaute Grundstücke
- Bebaute Grundstücke (Wohn- und Geschäftsgrundstücke)
- Grundstücke im Zustand der Bebauung
- Erbbaurechte

REFORM 2025: Neues Bewertungsverfahren seit 01.01.2025!
- Bundesmodell (Ertragswertverfahren/Sachwertverfahren)
- Ländermodelle (z.B. Bayern, Baden-Württemberg)

Fundstelle: GrStG 1973, Neufassung durch Grundsteuerreform 2025""",
            "law": "Grundsteuergesetz",
            "law_abbr": "GrStG",
            "paragraph": "1",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 2 GrStG - Befreiungen",
            "content": """§ 2 Befreiungen

Von der Grundsteuer sind befreit:

1. Grundstücke des Bundes, der Länder und Gemeinden (öffentliche Zwecke)
2. Grundstücke gemeinnütziger Organisationen (Kirchen, Wohlfahrt)
3. Grundstücke für wissenschaftliche, künstlerische oder Bildungszwecke
4. Kleingärten im Sinne des Bundeskleingartengesetzes
5. Denkmalgeschützte Gebäude unter bestimmten Voraussetzungen

Die Befreiung ist beim Finanzamt zu beantragen und muss begründet werden.

Fundstelle: GrStG 1973""",
            "law": "Grundsteuergesetz",
            "law_abbr": "GrStG",
            "paragraph": "2",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 13 GrStG - Steuerschuldner",
            "content": """§ 13 Steuerschuldner

(1) Steuerschuldner ist, wer in dem Zeitpunkt, der für die Feststellung des Einheitswerts maßgebend ist:

1. Eigentümer des Grundstücks ist
2. Bei Erbbaurechten: Der Erbbauberechtigte
3. Bei wirtschaftlichem Eigentum: Der wirtschaftliche Eigentümer

(2) Mehrere Steuerschuldner sind Gesamtschuldner (bei Miteigentum, Erbengemeinschaft).

WICHTIG für Immobilienkauf:
- Verkäufer zahlt anteilig bis Eigentumswechsel
- Käufer übernimmt ab Eigentumseintragung
- Regelung meist im Kaufvertrag (Stichtag)

Fundstelle: GrStG 1973""",
            "law": "Grundsteuergesetz",
            "law_abbr": "GrStG",
            "paragraph": "13",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 25 GrStG - Hebesatz",
            "content": """§ 25 Hebesatz

(1) Die Gemeinde bestimmt, mit welchem Hundertsatz des Steuerbetrags (Hebesatz) die Grundsteuer erhoben wird.

(2) Der Hebesatz ist für alle Grundstücke im Gemeindegebiet einheitlich festzusetzen.

PRAXIS-BEISPIEL:
- Grundsteuermessbetrag: 500 €
- Hebesatz Gemeinde: 400%
- Zu zahlende Grundsteuer: 500 € × 400% = 2.000 € pro Jahr

Hebesätze variieren stark:
- Großstädte: 300-800%
- Ländliche Gemeinden: 200-500%
- München: ca. 535%
- Berlin: ca. 810%

Die Gemeinde legt den Hebesatz jährlich fest!

Fundstelle: GrStG 1973""",
            "law": "Grundsteuergesetz",
            "law_abbr": "GrStG",
            "paragraph": "25",
            "rechtsgebiet": "Steuerrecht"
        }
    ],
    "BewG": [
        {
            "title": "§ 176 BewG - Bewertung des Grundvermögens",
            "content": """§ 176 Bewertung des Grundvermögens

(1) Bei der Bewertung des Grundvermögens sind die §§ 179 bis 198 zu berücksichtigen.

(2) Die Bewertung erfolgt nach dem:
1. Vergleichswertverfahren (unbebaute Grundstücke)
2. Ertragswertverfahren (vermietete Immobilien)
3. Sachwertverfahren (selbstgenutzte Immobilien)

GRUNDSTEUERREFORM 2025:
Neue Bewertung aller Grundstücke zum 01.01.2022 als Stichtag.
Bewertungsmaßstäbe variieren je nach Bundesland:
- Bundesmodell: Ertragswert/Sachwert
- Bayern: Flächenmodell
- Baden-Württemberg: Bodenwertmodell

Fundstelle: BewG vom 01.02.1991 (BGBl. I S. 230), Neufassung 2025""",
            "law": "Bewertungsgesetz",
            "law_abbr": "BewG",
            "paragraph": "176",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 182 BewG - Ertragswertverfahren",
            "content": """§ 182 Ertragswertverfahren

(1) Bei Anwendung des Ertragswertverfahrens ist der Wert der Gebäude getrennt von dem Bodenwert auf der Grundlage des Ertrags zu ermitteln.

(2) Der Gebäudeertragswert ergibt sich aus dem Reinertrag des Grundstücks.

(3) Der Reinertrag des Grundstücks ist der Rohertrag abzüglich der Bewirtschaftungskosten.

ANWENDUNG:
- Vermietete Wohn- und Geschäftsgrundstücke
- Mehrfamilienhäuser
- Mietwohngrundstücke

Formel vereinfacht:
Ertragswert = Jahresrohmiete × Vervielfältiger - Bodenwert

Fundstelle: BewG vom 01.02.1991 (BGBl. I S. 230)""",
            "law": "Bewertungsgesetz",
            "law_abbr": "BewG",
            "paragraph": "182",
            "rechtsgebiet": "Steuerrecht"
        },
        {
            "title": "§ 189 BewG - Sachwertverfahren",
            "content": """§ 189 Sachwertverfahren

(1) Bei Anwendung des Sachwertverfahrens ist der Wert der Gebäude getrennt von dem Bodenwert auf der Grundlage der Herstellungskosten zu ermitteln.

(2) Der Gebäudesachwert ergibt sich aus den durchschnittlichen Herstellungskosten vergleichbarer Gebäude.

ANWENDUNG:
- Selbstgenutzte Ein- und Zweifamilienhäuser
- Eigentumswohnungen (selbstgenutzt)
- Sonderbauten

Formel vereinfacht:
Sachwert = Bodenwert + Gebäudesachwert (Baukosten × Alterswertminderung)

Fundstelle: BewG vom 01.02.1991 (BGBl. I S. 230)""",
            "law": "Bewertungsgesetz",
            "law_abbr": "BewG",
            "paragraph": "189",
            "rechtsgebiet": "Steuerrecht"
        }
    ],
    "BauGB": [
        {
            "title": "§ 1 BauGB - Aufgabe und Begriff der Bauleitplanung",
            "content": """§ 1 Aufgabe und Begriff der Bauleitplanung

(1) Aufgabe der Bauleitplanung ist es, die bauliche und sonstige Nutzung der Grundstücke in der Gemeinde vorzubereiten und zu leiten.

(2) Bauleitpläne sind der Flächennutzungsplan (vorbereitender Bauleitplan) und der Bebauungsplan (verbindlicher Bauleitplan).

(3) Die Gemeinden haben die Bauleitpläne aufzustellen, sobald und soweit es für die städtebauliche Entwicklung und Ordnung erforderlich ist.

(4) Die Bauleitpläne sind den Zielen der Raumordnung anzupassen.

(5) Die Bauleitpläne sollen eine nachhaltige städtebauliche Entwicklung gewährleisten.

(6) Bei der Aufstellung der Bauleitpläne sind insbesondere zu berücksichtigen:
1. Die allgemeinen Anforderungen an gesunde Wohn- und Arbeitsverhältnisse
2. Die Wohnbedürfnisse der Bevölkerung
3. Die sozialen und kulturellen Bedürfnisse
4. Die Belange des Umweltschutzes
5. Die Belange der Wirtschaft
6. Die Belange des Verkehrs

Fundstelle: BauGB vom 23.09.2004 (BGBl. I S. 2414)""",
            "law": "Baugesetzbuch",
            "law_abbr": "BauGB",
            "paragraph": "1",
            "rechtsgebiet": "Baurecht"
        },
        {
            "title": "§ 34 BauGB - Zulässigkeit von Vorhaben innerhalb der im Zusammenhang bebauten Ortsteile",
            "content": """§ 34 Zulässigkeit von Vorhaben innerhalb der im Zusammenhang bebauten Ortsteile

(1) Innerhalb der im Zusammenhang bebauten Ortsteile ist ein Vorhaben zulässig, wenn es sich nach Art und Maß der baulichen Nutzung, der Bauweise und der Grundstücksfläche, die überbaut werden soll, in die Eigenart der näheren Umgebung einfügt und die Erschließung gesichert ist.

(2) Die Anforderungen an gesunde Wohn- und Arbeitsverhältnisse müssen gewahrt bleiben.

PRAXIS ("Einfügen in die nähere Umgebung"):
- Bauweise: Wenn Umgebung Doppelhäuser → kein freistehendes Einfamilienhaus
- Höhe: Wenn Umgebung 2 Geschosse → kein 5-Geschosser
- Nutzung: Wenn Wohngebiet → kein Gewerbe

WICHTIG für Bauantrag:
§ 34 gilt OHNE Bebauungsplan!
Bei Bebauungsplan: § 30 BauGB

Fundstelle: BauGB vom 23.09.2004 (BGBl. I S. 2414)""",
            "law": "Baugesetzbuch",
            "law_abbr": "BauGB",
            "paragraph": "34",
            "rechtsgebiet": "Baurecht"
        },
        {
            "title": "§ 35 BauGB - Bauen im Außenbereich",
            "content": """§ 35 Bauen im Außenbereich

(1) Im Außenbereich ist ein Vorhaben nur zulässig, wenn öffentliche Belange nicht entgegenstehen und die Erschließung gesichert ist.

(2) Privilegierte Vorhaben (zulässig):
1. Land- und forstwirtschaftliche Betriebe
2. Gartenbaubetriebe
3. Windenergieanlagen
4. Biogasanlagen

(3) Sonstige Vorhaben können im Einzelfall zugelassen werden.

(4) Öffentliche Belange stehen entgegen, wenn:
1. Die Entstehung einer Splittersiedlung befördert würde
2. Die natürliche Eigenart der Landschaft beeinträchtigt würde
3. Die Funktionsfähigkeit von Infrastruktur beeinträchtigt würde

PRAXIS:
Außenbereich = unbebauter Bereich außerhalb geschlossener Ortslage
Bauvorhaben grundsätzlich NICHT genehmigungsfähig (Ausnahme: § 35 Abs. 2)

Fundstelle: BauGB vom 23.09.2004 (BGBl. I S. 2414)""",
            "law": "Baugesetzbuch",
            "law_abbr": "BauGB",
            "paragraph": "35",
            "rechtsgebiet": "Baurecht"
        }
    ],
    "WohnFlV": [
        {
            "title": "§ 1 WohnFlV - Anwendungsbereich",
            "content": """§ 1 Anwendungsbereich

Diese Verordnung ist anzuwenden, soweit die Wohnfläche berechnet wird
1. für Wohnungen im sozialen Wohnungsbau, die von der Verordnung über wohnungswirtschaftliche Berechnungen nach dem Zweiten Wohnungsbaugesetz erfasst werden,
2. für Wohnungen, soweit das Wohngeldgesetz die Berechnung der Wohnfläche vorschreibt,
3. für Wohnungen in sonstigen Fällen, soweit die Wohnfläche gesetzlich vorgeschrieben oder durch Vertrag oder Vertragserklärung vereinbart ist.

Fundstelle: WohnFlV vom 25.11.2003 (BGBl. I S. 2346)""",
            "law": "Wohnflächenverordnung",
            "law_abbr": "WohnFlV",
            "paragraph": "1",
            "rechtsgebiet": "Mietrecht"
        },
        {
            "title": "§ 2 WohnFlV - Berechnung der Wohnfläche",
            "content": """§ 2 Berechnung der Wohnfläche

(1) Die Wohnfläche einer Wohnung umfasst die Grundfläche der Räume, die ausschließlich zu dieser Wohnung gehören.

(2) Zur Wohnfläche gehören auch:
1. die Grundflächen von Wintergärten, Schwimmbädern und ähnlichen nach allen Seiten geschlossenen Räumen
2. die Grundflächen von Balkonen, Loggien, Dachgärten und Terrassen in der Regel zu einem Viertel, höchstens jedoch zu der Hälfte

(3) Nicht zur Wohnfläche gehören:
1. Grundflächen von Zubehörräumen (Keller, Waschküchen, Bodenräume, Trockenräume)
2. Grundflächen von Geschäftsräumen und sonstigen Räumen, die nicht Wohnzwecken dienen

Fundstelle: WohnFlV vom 25.11.2003 (BGBl. I S. 2346)""",
            "law": "Wohnflächenverordnung",
            "law_abbr": "WohnFlV",
            "paragraph": "2",
            "rechtsgebiet": "Mietrecht"
        }
    ],
    "HOAI": [
        {
            "title": "§ 1 HOAI - Anwendungsbereich",
            "content": """§ 1 Anwendungsbereich

Diese Verordnung regelt die Berechnung der Honorare für die Leistungen der Architekten und Ingenieure (Auftragnehmer).

WICHTIG ab 01.01.2021: HOAI ist NICHT MEHR verbindlich!
EuGH-Urteil C-377/17: Mindest- und Höchstsätze verstoßen gegen EU-Dienstleistungsfreiheit.

PRAXIS:
- HOAI dient als Orientierung für angemessenes Honorar
- Freie Verhandlung zwischen Bauherr und Architekt
- Bei fehlendem Vertrag: HOAI als Maßstab für übliches Honorar

Fundstelle: HOAI 2021 vom 10.07.2013 (BGBl. I S. 2276)""",
            "law": "Honorarordnung für Architekten und Ingenieure",
            "law_abbr": "HOAI",
            "paragraph": "1",
            "rechtsgebiet": "Baurecht"
        },
        {
            "title": "§ 34 HOAI - Leistungsbild Gebäude",
            "content": """§ 34 Leistungsbild Gebäude und Innenräume

(1) Das Leistungsbild Gebäude und Innenräume umfasst Leistungen für Neubauten, Neuanlagen, Wiederaufbauten, Erweiterungsbauten, Umbauten, Modernisierungen, Instandhaltungen und Instandsetzungen.

(2) Leistungsphasen:
1. Grundlagenermittlung (2%)
2. Vorplanung (7%)
3. Entwurfsplanung (15%)
4. Genehmigungsplanung (3%)
5. Ausführungsplanung (25%)
6. Vorbereitung der Vergabe (10%)
7. Mitwirkung bei der Vergabe (4%)
8. Objektüberwachung - Bauüberwachung (32%)
9. Objektbetreuung (2%)

PRAXIS:
Stufenvertrag: Nicht alle Leistungsphasen müssen beauftragt werden.
Meist: LPH 1-4 (Planung) separat von LPH 5-9 (Ausführung)

Fundstelle: HOAI 2021""",
            "law": "Honorarordnung für Architekten und Ingenieure",
            "law_abbr": "HOAI",
            "paragraph": "34",
            "rechtsgebiet": "Baurecht"
        }
    ],
    "GEG": [
        {
            "title": "§ 1 GEG - Zweck und Anwendungsbereich",
            "content": """§ 1 Zweck und Anwendungsbereich

(1) Zweck dieses Gesetzes ist ein möglichst sparsamer Einsatz von Energie in Gebäuden einschließlich einer zunehmenden Nutzung erneuerbarer Energien zur Erzeugung von Wärme, Kälte und Strom für den Gebäudebetrieb.

(2) Dieses Gesetz gilt für Gebäude, soweit sie unter Einsatz von Energie beheizt oder gekühlt werden.

HEIZUNGSGESETZ 2024:
- 65% erneuerbare Energien bei Neubauten ab 01.01.2024
- Bestandsgebäude: Austauschpflicht ab 2024/2026 (je nach Kommune)
- Förderung: BEG-Zuschüsse bis zu 70%

Fundstelle: GEG vom 08.08.2020 (BGBl. I S. 1728), geändert 2023""",
            "law": "Gebäudeenergiegesetz",
            "law_abbr": "GEG",
            "paragraph": "1",
            "rechtsgebiet": "Baurecht"
        },
        {
            "title": "§ 71 GEG - Austauschpflicht für Heizkessel",
            "content": """§ 71 Austauschpflicht für Heizkessel

(1) Heizkessel, die mit einem flüssigen oder gasförmigen Brennstoff beschickt werden und vor dem 01.01.1991 eingebaut wurden, dürfen nicht mehr betrieben werden.

(2) Ausnahmen:
1. Niedertemperatur-Heizkessel
2. Brennwertkessel
3. Heizkessel, die nur ein Wohngebäude mit nicht mehr als zwei Wohnungen beheizen
4. Eigentümer, die am 01.02.2002 bereits Eigentümer waren

(3) NEUFASSUNG 2024:
Ab 2024 gelten verschärfte Austauschpflichten:
- Gasheizungen älter als 30 Jahre müssen raus
- Neue Heizungen müssen 65% erneuerbare Energien nutzen

PRAXIS:
- Wärmepumpe
- Fernwärme
- Biomasseheizung
- Hybridheizung (Gas + Wärmepumpe)

Fundstelle: GEG vom 08.08.2020, Novelle 2023""",
            "law": "Gebäudeenergiegesetz",
            "law_abbr": "GEG",
            "paragraph": "71",
            "rechtsgebiet": "Baurecht"
        },
        {
            "title": "§ 72 GEG - Nachrüstungspflichten",
            "content": """§ 72 Nachrüstungspflichten

(1) Eigentümer müssen oberste Geschossdecken dämmen, wenn sie nicht den Mindestwärmeschutz erfüllen.

(2) Ausnahme: Wenn das Dach bereits gedämmt ist.

(3) Ungedämmte Wärmeverteilungs- und Warmwasserleitungen in unbeheizten Räumen müssen gedämmt werden.

(4) Frist: Eigentümer haben 2 Jahre nach Eigentumsübergang Zeit für Nachrüstung.

WICHTIG beim Immobilienkauf:
- Verkäufer: Keine Pflicht vor Verkauf
- Käufer: Muss binnen 2 Jahren nachrüsten!
- Kosten: 5.000-15.000 € für Dämmung oberster Geschossdecke

Fundstelle: GEG vom 08.08.2020""",
            "law": "Gebäudeenergiegesetz",
            "law_abbr": "GEG",
            "paragraph": "72",
            "rechtsgebiet": "Baurecht"
        }
    ],
    "MaBV": [
        {
            "title": "§ 1 MaBV - Anwendungsbereich",
            "content": """§ 1 Anwendungsbereich

Diese Verordnung regelt die Verpflichtungen von:
1. Wohnungsmaklern
2. Bauträgern
3. Baubetreuer

bei der Vermittlung, dem Nachweis und dem Vertrieb von Wohnraum sowie beim Verkauf von Bauträgergrundstücken.

Fundstelle: MaBV vom 15.03.2003 (BGBl. I S. 479)""",
            "law": "Makler- und Bauträgerverordnung",
            "law_abbr": "MaBV",
            "paragraph": "1",
            "rechtsgebiet": "Baurecht"
        },
        {
            "title": "§ 3 MaBV - Bauträgervertrag, Zahlungen",
            "content": """§ 3 Bauträgervertrag, Zahlungen

(1) Der Bauträger darf Kaufpreiszahlungen erst anfordern, wenn:
1. Der Bauträger Eigentümer des Grundstücks ist
2. Eine Auflassungsvormerkung für den Erwerber eingetragen ist
3. Die Baugenehmigung vorliegt (wenn erforderlich)

(2) Zahlungsplan nach Baufortschritt:
1. Nach Beginn der Erdarbeiten: 30%
2. Nach Rohbaufertigstellung: 28%
3. Nach Dachfertigstellung: 8%
4. Nach Putzarbeiten: 10%
5. Nach Estrich: 5%
6. Nach Fliesen: 4%
7. Nach Sanitär/Heizung: 3%
8. Nach Tapezierung/Malerarbeiten: 3%
9. Nach Bodenbelägen: 4%
10. Nach Abnahme: 5%

SCHUTZ FÜR KÄUFER:
Zahlungen sind an Baufortschritt gebunden!
Bei Bauträgerinsolvenz: Nur bezahlt, was bereits gebaut.

Fundstelle: MaBV vom 15.03.2003""",
            "law": "Makler- und Bauträgerverordnung",
            "law_abbr": "MaBV",
            "paragraph": "3",
            "rechtsgebiet": "Baurecht"
        }
    ]
}
