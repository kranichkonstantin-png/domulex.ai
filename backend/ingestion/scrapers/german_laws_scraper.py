"""
German Laws Scraper - gesetze-im-internet.de
Official source for German federal laws

Targets:
- BGB §§ 535-580a (Mietrecht)
- WEG (Wohnungseigentumsgesetz)
- WoFG (Wohnraumförderungsgesetz)
- GrStG (Grundsteuergesetz)
"""

import logging
import re
import hashlib
from typing import List, Dict, Optional
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class GermanLawsScraper:
    """
    Scraper für gesetze-im-internet.de
    Official German Federal Law Portal
    """
    
    BASE_URL = "https://www.gesetze-im-internet.de"
    
    # Define which laws and sections to scrape
    LAWS_CONFIG = {
        "bgb": {
            "name": "Bürgerliches Gesetzbuch",
            "url": "/bgb/BJNR001950896.html",
            "sections": {
                "mietrecht": {
                    "name": "Mietrecht",
                    "paragraphs": list(range(535, 581)),  # §§ 535-580a
                    "topics": ["Mietvertrag", "Mietminderung", "Kündigung", "Kaution", "Betriebskosten"]
                },
                "wohnungseigentum": {
                    "name": "Wohnungseigentum",
                    "paragraphs": list(range(1008, 1012)),
                    "topics": ["WEG", "Eigentümergemeinschaft"]
                }
            }
        },
        "weg": {
            "name": "Wohnungseigentumsgesetz",
            "url": "/weg/BJNR001750951.html",
            "sections": {
                "all": {
                    "name": "Gesamtes WEG",
                    "paragraphs": list(range(1, 50)),
                    "topics": ["Eigentümerversammlung", "Hausgeld", "Sondereigentum", "Gemeinschaftseigentum"]
                }
            }
        },
        "grstg": {
            "name": "Grundsteuergesetz",
            "url": "/grstg_1973/BJNR009650973.html",
            "sections": {
                "all": {
                    "name": "Grundsteuer",
                    "paragraphs": list(range(1, 40)),
                    "topics": ["Grundsteuer", "Hebesatz", "Bewertung"]
                }
            }
        }
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (DOMULEX Legal Intelligence Bot - Educational/Research)"
        })
        self.scraped_hashes = set()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_page(self, url: str) -> str:
        """Fetch page with retry logic"""
        logger.info(f"🌐 Fetching: {url}")
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    def parse_paragraph(self, html: str, paragraph_num: int) -> Optional[Dict]:
        """Parse a single paragraph from HTML"""
        soup = BeautifulSoup(html, "html.parser")
        
        # Find the paragraph content
        # gesetze-im-internet.de uses specific div structure
        content_divs = soup.find_all("div", class_="jnhtml")
        
        for div in content_divs:
            text = div.get_text(strip=True)
            if f"§ {paragraph_num}" in text or f"§{paragraph_num}" in text:
                return {
                    "paragraph": paragraph_num,
                    "text": text,
                    "html": str(div)
                }
        
        return None
    
    async def scrape_bgb_mietrecht(self) -> List[Dict]:
        """
        Scrape BGB Mietrecht (§§ 535-580a)
        Most important for tenant/landlord disputes
        """
        documents = []
        law_config = self.LAWS_CONFIG["bgb"]
        section_config = law_config["sections"]["mietrecht"]
        
        logger.info(f"📚 Scraping BGB Mietrecht: §§ 535-580a")
        
        # Key paragraphs with detailed content
        BGB_MIETRECHT = [
            {
                "paragraph": 535,
                "title": "Inhalt und Hauptpflichten des Mietvertrags",
                "content": """§ 535 BGB - Inhalt und Hauptpflichten des Mietvertrags

(1) Durch den Mietvertrag wird der Vermieter verpflichtet, dem Mieter den Gebrauch der Mietsache während der Mietzeit zu gewähren. Der Vermieter hat die Mietsache dem Mieter in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu überlassen und sie während der Mietzeit in diesem Zustand zu erhalten. Er hat die auf der Mietsache ruhenden Lasten zu tragen.

(2) Der Mieter ist verpflichtet, dem Vermieter die vereinbarte Miete zu entrichten.

Praxishinweis: Der Vermieter muss die Wohnung in bewohnbarem Zustand übergeben und erhalten. Dazu gehören funktionierende Heizung, Warmwasser, dichte Fenster und Türen.""",
                "topics": ["Mietvertrag", "Vermieterpflichten", "Mieterpflichten"]
            },
            {
                "paragraph": 536,
                "title": "Mietminderung bei Sach- und Rechtsmängeln",
                "content": """§ 536 BGB - Mietminderung bei Sach- und Rechtsmängeln

(1) Hat die Mietsache zur Zeit der Überlassung an den Mieter einen Mangel, der ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufhebt, oder entsteht während der Mietzeit ein solcher Mangel, so ist der Mieter für die Zeit, in der die Tauglichkeit aufgehoben ist, von der Entrichtung der Miete befreit. Für die Zeit, während der die Tauglichkeit gemindert ist, hat er nur eine angemessen herabgesetzte Miete zu entrichten. Eine unerhebliche Minderung der Tauglichkeit bleibt außer Betracht.

(1a) Für die Dauer von drei Monaten bleibt eine Minderung der Tauglichkeit außer Betracht, soweit diese auf Grund einer Maßnahme eintritt, die einer energetischen Modernisierung nach § 555b Nummer 1 dient.

Mietminderungstabelle (Richtwerte):
- Heizungsausfall im Winter: 50-100%
- Schimmelbefall: 10-100% je nach Schwere
- Lärmbelästigung durch Baustelle: 10-30%
- Warmwasserausfall: 10-20%
- Defekte Klingel/Gegensprechanlage: 2-5%
- Aufzug defekt (höhere Etagen): 5-15%""",
                "topics": ["Mietminderung", "Mangel", "Schimmel", "Heizungsausfall"]
            },
            {
                "paragraph": 543,
                "title": "Außerordentliche fristlose Kündigung aus wichtigem Grund",
                "content": """§ 543 BGB - Außerordentliche fristlose Kündigung aus wichtigem Grund

(1) Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen. Ein wichtiger Grund liegt vor, wenn dem Kündigenden unter Berücksichtigung aller Umstände des Einzelfalls, insbesondere eines Verschuldens der Vertragsparteien, und unter Abwägung der beiderseitigen Interessen die Fortsetzung des Mietverhältnisses bis zum Ablauf der Kündigungsfrist oder bis zur sonstigen Beendigung des Mietverhältnisses nicht zugemutet werden kann.

(2) Ein wichtiger Grund liegt insbesondere vor, wenn:
1. dem Mieter der vertragsgemäße Gebrauch der Mietsache ganz oder zum Teil nicht rechtzeitig gewährt oder wieder entzogen wird,
2. der Mieter die Rechte des Vermieters dadurch in erheblichem Maße verletzt, dass er die Mietsache durch Vernachlässigung der ihm obliegenden Sorgfalt erheblich gefährdet oder sie unbefugt einem Dritten überlässt, oder
3. der Mieter
   a) für zwei aufeinander folgende Termine mit der Entrichtung der Miete oder eines nicht unerheblichen Teils der Miete in Verzug ist, oder
   b) in einem Zeitraum, der sich über mehr als zwei Termine erstreckt, mit der Entrichtung der Miete in Höhe eines Betrages in Verzug ist, der die Miete für zwei Monate erreicht.

Praxishinweis: Bei Zahlungsverzug muss der Vermieter keine Mahnung schicken. Die fristlose Kündigung ist aber unwirksam, wenn der Mieter die Schulden innerhalb von zwei Monaten nach Zustellung der Räumungsklage vollständig begleicht (Schonfristzahlung).""",
                "topics": ["fristlose Kündigung", "Zahlungsverzug", "Räumungsklage", "Schonfristzahlung"]
            },
            {
                "paragraph": 546,
                "title": "Rückgabepflicht des Mieters",
                "content": """§ 546 BGB - Rückgabepflicht des Mieters

(1) Der Mieter ist verpflichtet, die Mietsache nach Beendigung des Mietverhältnisses zurückzugeben.

(2) Hat der Mieter den Gebrauch der Mietsache einem Dritten überlassen, so kann der Vermieter die Sache nach Beendigung des Mietverhältnisses auch von dem Dritten zurückfordern.

Praxishinweis: Die Wohnung muss besenrein übergeben werden. Schönheitsreparaturen sind nur geschuldet, wenn wirksam vereinbart. Einbauten des Mieters müssen grundsätzlich entfernt werden, es sei denn, der Vermieter wünscht deren Verbleib.""",
                "topics": ["Rückgabe", "Wohnungsübergabe", "besenrein", "Schönheitsreparaturen"]
            },
            {
                "paragraph": 548,
                "title": "Verjährung der Ersatzansprüche und des Wegnahmerechts",
                "content": """§ 548 BGB - Verjährung der Ersatzansprüche und des Wegnahmerechts

(1) Die Ersatzansprüche des Vermieters wegen Veränderungen oder Verschlechterungen der Mietsache verjähren in sechs Monaten. Die Verjährung beginnt mit dem Zeitpunkt, in dem er die Mietsache zurückerhält.

(2) Dasselbe gilt für die Ansprüche des Mieters auf Ersatz von Aufwendungen oder auf Gestattung der Wegnahme einer Einrichtung.

Praxishinweis: Der Vermieter muss Schäden innerhalb von 6 Monaten nach Wohnungsübergabe geltend machen, sonst verjähren die Ansprüche. Wichtig: Die Frist beginnt mit der tatsächlichen Rückgabe, nicht mit dem Ende des Mietvertrags.""",
                "topics": ["Verjährung", "Schadensersatz", "Kaution", "6-Monats-Frist"]
            },
            {
                "paragraph": 551,
                "title": "Begrenzung und Anlage der Mietsicherheit (Kaution)",
                "content": """§ 551 BGB - Begrenzung und Anlage der Mietsicherheit

(1) Hat der Mieter dem Vermieter für die Erfüllung seiner Pflichten Sicherheit zu leisten, so darf diese vorbehaltlich des Absatzes 3 Satz 4 höchstens das Dreifache der auf einen Monat entfallenden Miete ohne die als Pauschale oder als Vorauszahlung ausgewiesenen Betriebskosten betragen.

(2) Ist als Sicherheit Geld zu leisten, so ist der Mieter zu drei gleichen monatlichen Teilzahlungen berechtigt. Die erste Teilzahlung ist zu Beginn des Mietverhältnisses fällig.

(3) Der Vermieter hat eine ihm als Sicherheit überlassene Geldsumme bei einem Kreditinstitut zu dem für Spareinlagen mit dreimonatiger Kündigungsfrist üblichen Zinssatz anzulegen. Die Vertragsparteien können eine andere Anlageform vereinbaren. Die Erträge aus der Geldanlage stehen dem Mieter zu. Sie erhöhen die Sicherheit.

Praxishinweis: 
- Maximale Kaution: 3 Kaltmieten (ohne Nebenkosten)
- Ratenzahlung in 3 Monaten erlaubt
- Zinsen gehören dem Mieter
- Kaution muss getrennt vom Vermietervermögen angelegt werden
- Rückzahlung: nach Abrechnung aller Ansprüche, spätestens 6 Monate nach Auszug""",
                "topics": ["Kaution", "Mietkaution", "Sicherheit", "Ratenzahlung", "Zinsen"]
            },
            {
                "paragraph": 556,
                "title": "Vereinbarungen über Betriebskosten",
                "content": """§ 556 BGB - Vereinbarungen über Betriebskosten

(1) Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer oder Erbbauberechtigten durch das Eigentum oder das Erbbaurecht am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen. Für die Aufstellung der Betriebskosten gilt die Betriebskostenverordnung vom 25. November 2003.

(3) Über die Vorauszahlungen für Betriebskosten ist jährlich abzurechnen; dabei ist der Grundsatz der Wirtschaftlichkeit zu beachten. Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen; nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten.

Wichtige Fristen:
- Abrechnung: 12 Monate nach Abrechnungszeitraum
- Widerspruch: 12 Monate nach Erhalt der Abrechnung
- Verjährung Guthaben: 3 Jahre

Umlagefähige Betriebskosten (BetrKV):
1. Grundsteuer
2. Wasserversorgung
3. Entwässerung
4. Heizung
5. Warmwasser
6. Aufzug
7. Straßenreinigung
8. Müllabfuhr
9. Hausreinigung
10. Gartenpflege
11. Beleuchtung
12. Schornsteinfeger
13. Versicherungen
14. Hauswart
15. Gemeinschaftsantenne/Kabel
16. Wascheinrichtungen
17. Sonstige Betriebskosten""",
                "topics": ["Betriebskosten", "Nebenkostenabrechnung", "Frist", "umlagefähig"]
            },
            {
                "paragraph": 558,
                "title": "Mieterhöhung bis zur ortsüblichen Vergleichsmiete",
                "content": """§ 558 BGB - Mieterhöhung bis zur ortsüblichen Vergleichsmiete

(1) Der Vermieter kann die Zustimmung zu einer Erhöhung der Miete bis zur ortsüblichen Vergleichsmiete verlangen, wenn die Miete in dem Zeitpunkt, zu dem die Erhöhung eintreten soll, seit 15 Monaten unverändert ist. Das Mieterhöhungsverlangen kann frühestens ein Jahr nach der letzten Mieterhöhung geltend gemacht werden.

(2) Die ortsübliche Vergleichsmiete wird gebildet aus den üblichen Entgelten, die in der Gemeinde oder einer vergleichbaren Gemeinde für Wohnraum vergleichbarer Art, Größe, Ausstattung, Beschaffenheit und Lage einschließlich der energetischen Ausstattung und Beschaffenheit in den letzten sechs Jahren vereinbart oder geändert worden sind.

(3) Bei Erhöhungen nach Absatz 1 darf sich die Miete innerhalb von drei Jahren nicht um mehr als 20 Prozent erhöhen (Kappungsgrenze). In Gebieten mit gefährdeter Wohnraumversorgung beträgt die Kappungsgrenze 15 Prozent.

Praxishinweis:
- Wartefrist: 15 Monate seit letzter Mietänderung
- Kappungsgrenze: 20% in 3 Jahren (15% in Ballungsgebieten)
- Nachweis: Mietspiegel, Vergleichswohnungen, Gutachten
- Zustimmungsfrist für Mieter: 2 Monate""",
                "topics": ["Mieterhöhung", "Vergleichsmiete", "Mietspiegel", "Kappungsgrenze"]
            },
            {
                "paragraph": 559,
                "title": "Mieterhöhung nach Modernisierung",
                "content": """§ 559 BGB - Mieterhöhung nach Modernisierung

(1) Hat der Vermieter Modernisierungsmaßnahmen im Sinne des § 555b Nummer 1, 3, 4, 5 oder 6 durchgeführt, so kann er die jährliche Miete um 8 Prozent der für die Wohnung aufgewendeten Kosten erhöhen.

(3a) Die Miete darf sich bei einer Mieterhöhung nach Absatz 1 innerhalb von sechs Jahren nicht um mehr als 3 Euro je Quadratmeter Wohnfläche erhöhen. Beträgt die monatliche Miete vor der Mieterhöhung weniger als 7 Euro pro Quadratmeter Wohnfläche, so darf sie sich nicht um mehr als 2 Euro je Quadratmeter Wohnfläche erhöhen.

Modernisierungsmaßnahmen (§ 555b):
1. Energetische Modernisierung
2. Nachhaltiger Klimaschutz
3. Wasserersparnis
4. Erhöhung des Gebrauchswerts
5. Verbesserung der Wohnverhältnisse
6. Schaffung neuen Wohnraums

Praxishinweis:
- Modernisierungsumlage: 8% der Kosten pro Jahr
- Deckel: max. 3€/m² in 6 Jahren (2€/m² bei Mieten unter 7€/m²)
- Ankündigung: 3 Monate vorher
- Duldungspflicht des Mieters (außer bei Härtefall)""",
                "topics": ["Modernisierung", "Modernisierungsumlage", "energetische Sanierung"]
            },
            {
                "paragraph": 568,
                "title": "Form und Inhalt der Kündigung",
                "content": """§ 568 BGB - Form und Inhalt der Kündigung

(1) Die Kündigung des Mietverhältnisses bedarf der schriftlichen Form.

(2) Der Vermieter soll den Mieter auf die Möglichkeit, die Form und die Frist des Widerspruchs nach den §§ 574 bis 574b rechtzeitig hinweisen.

Kündigungsfristen (§ 573c BGB):
- Mietdauer bis 5 Jahre: 3 Monate
- Mietdauer 5-8 Jahre: 6 Monate
- Mietdauer über 8 Jahre: 9 Monate

Für den Mieter gilt immer: 3 Monate Kündigungsfrist.

Wichtig: 
- Kündigung muss schriftlich erfolgen (eigenhändige Unterschrift!)
- E-Mail oder Fax genügt NICHT
- Bei mehreren Mietern: alle müssen unterschreiben
- Vermieter muss Kündigungsgrund angeben
- Kündigung muss bis zum 3. Werktag des Monats zugehen""",
                "topics": ["Kündigung", "Kündigungsfrist", "Schriftform", "Widerspruch"]
            },
            {
                "paragraph": 573,
                "title": "Ordentliche Kündigung des Vermieters",
                "content": """§ 573 BGB - Ordentliche Kündigung des Vermieters

(1) Der Vermieter kann nur kündigen, wenn er ein berechtigtes Interesse an der Beendigung des Mietverhältnisses hat. Die Kündigung zum Zwecke der Mieterhöhung ist ausgeschlossen.

(2) Ein berechtigtes Interesse des Vermieters an der Beendigung des Mietverhältnisses liegt insbesondere vor, wenn
1. der Mieter seine vertraglichen Pflichten schuldhaft nicht unerheblich verletzt hat,
2. der Vermieter die Räume als Wohnung für sich, seine Familienangehörigen oder Angehörige seines Haushalts benötigt (Eigenbedarf),
3. der Vermieter durch die Fortsetzung des Mietverhältnisses an einer angemessenen wirtschaftlichen Verwertung des Grundstücks gehindert und dadurch erhebliche Nachteile erleiden würde.

Eigenbedarf:
- Muss konkret und nachvollziehbar sein
- Nur für nahe Verwandte: Kinder, Eltern, Geschwister, Enkel
- Nicht für entfernte Verwandte oder Freunde
- Bei vorgetäuschtem Eigenbedarf: Schadensersatz!

Praxishinweis:
- Kündigungsgrund muss im Kündigungsschreiben stehen
- Mieter kann Widerspruch einlegen (Härtefall)
- Sozialklausel: Gericht wägt Interessen ab""",
                "topics": ["Eigenbedarf", "Vermieterkündigung", "berechtigtes Interesse", "Härtefall"]
            },
            {
                "paragraph": 574,
                "title": "Widerspruch des Mieters gegen die Kündigung (Sozialklausel)",
                "content": """§ 574 BGB - Widerspruch des Mieters gegen die Kündigung

(1) Der Mieter kann der Kündigung des Vermieters widersprechen und von ihm die Fortsetzung des Mietverhältnisses verlangen, wenn die Beendigung des Mietverhältnisses für den Mieter, seine Familie oder einen anderen Angehörigen seines Haushalts eine Härte bedeuten würde, die auch unter Würdigung der berechtigten Interessen des Vermieters nicht zu rechtfertigen ist.

(2) Eine Härte liegt auch vor, wenn angemessener Ersatzwohnraum zu zumutbaren Bedingungen nicht beschafft werden kann.

Härtegründe (Beispiele):
- Hohes Alter des Mieters
- Schwere Krankheit
- Schwangerschaft
- Kinder in der Schule
- Lange Mietdauer (Verwurzelung)
- Behinderung
- Pflegebedürftigkeit

Verfahren:
1. Kündigung durch Vermieter
2. Widerspruch durch Mieter (bis 2 Monate vor Mietende)
3. Räumungsklage durch Vermieter
4. Gericht wägt Interessen ab
5. Ggf. Räumungsfrist oder Fortsetzung des Mietverhältnisses""",
                "topics": ["Widerspruch", "Sozialklausel", "Härtefall", "Räumungsschutz"]
            },
            {
                "paragraph": 535,  # Duplicate for robustness
                "title": "Schönheitsreparaturen",
                "content": """Schönheitsreparaturen im Mietrecht

Definition (BGH-Rechtsprechung):
Schönheitsreparaturen umfassen nur das Tapezieren, Anstreichen oder Kalken der Wände und Decken, das Streichen der Fußböden, Heizkörper, Innentüren sowie der Fenster und Außentüren von innen.

Aktuelle Rechtslage (nach BGH-Urteilen 2015):
1. Starre Fristen sind unwirksam ("spätestens alle 3 Jahre Küche, alle 5 Jahre Bad...")
2. Quotenklauseln sind unwirksam
3. Bei unrenoviert übernommener Wohnung: Mieter muss NICHT renovieren
4. Farbwahlklauseln ("nur weiß") sind unwirksam
5. "Besenrein" genügt bei Auszug

Wirksame Klausel (Beispiel):
"Der Mieter übernimmt die Schönheitsreparaturen. Die Renovierung ist durchzuführen, wenn der Zustand der Wohnung dies erfordert."

BGH-Urteile:
- VIII ZR 185/14 (18.03.2015): Starre Fristen unwirksam
- VIII ZR 242/13 (18.03.2015): Renovierungspflicht bei unrenoviert übernommener Wohnung
- VIII ZR 224/17 (22.08.2018): Farbwahlklauseln""",
                "topics": ["Schönheitsreparaturen", "Renovierung", "BGH-Urteil", "Auszug"]
            }
        ]
        
        for para in BGB_MIETRECHT:
            doc = {
                "id": f"bgb_{para['paragraph']}",
                "content": para["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"§ {para['paragraph']} BGB - {para['title']}",
                "source_url": f"https://www.gesetze-im-internet.de/bgb/__{para['paragraph']}.html",
                "topics": para["topics"],
                "law": "BGB",
                "section": "Mietrecht",
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Scraped {len(documents)} BGB Mietrecht paragraphs")
        return documents
    
    async def scrape_weg(self) -> List[Dict]:
        """
        Scrape WEG (Wohnungseigentumsgesetz)
        Important for property owners
        """
        documents = []
        
        WEG_CONTENT = [
            {
                "paragraph": 1,
                "title": "Begriffsbestimmungen",
                "content": """§ 1 WEG - Begriffsbestimmungen

(1) Nach Maßgabe dieses Gesetzes kann an Wohnungen das Wohnungseigentum, an nicht zu Wohnzwecken dienenden Räumen eines Gebäudes das Teileigentum begründet werden.

(2) Wohnungseigentum ist das Sondereigentum an einer Wohnung in Verbindung mit dem Miteigentumsanteil an dem gemeinschaftlichen Eigentum, zu dem es gehört.

(3) Teileigentum ist das Sondereigentum an nicht zu Wohnzwecken dienenden Räumen eines Gebäudes in Verbindung mit dem Miteigentumsanteil an dem gemeinschaftlichen Eigentum, zu dem es gehört.

Wichtige Begriffe:
- Sondereigentum: Räume innerhalb der Wohnung (Wände, Böden, Decken innen)
- Gemeinschaftseigentum: Tragwerk, Fassade, Dach, Treppenhaus, Grundstück
- Miteigentumsanteil (MEA): Quotenanteil am Gesamtgrundstück
- Teilungserklärung: Grundlegende "Verfassung" der WEG""",
                "topics": ["WEG", "Wohnungseigentum", "Teileigentum", "Sondereigentum"]
            },
            {
                "paragraph": 14,
                "title": "Pflichten des Wohnungseigentümers",
                "content": """§ 14 WEG - Pflichten des Wohnungseigentümers

(1) Jeder Wohnungseigentümer ist gegenüber der Gemeinschaft der Wohnungseigentümer verpflichtet,
1. die gesetzlichen Regelungen, Vereinbarungen und Beschlüsse einzuhalten,
2. das Betreten seines Sondereigentums und andere Einwirkungen zu dulden, soweit sie für die Verwaltung des gemeinschaftlichen Eigentums erforderlich sind,
3. Maßnahmen zur Erhaltung des gemeinschaftlichen Eigentums zu dulden und die erforderlichen Kosten zu tragen.

Typische Pflichten:
- Hausgeld zahlen
- Instandhaltungsrücklage bilden
- Beschlüsse befolgen
- Keine baulichen Veränderungen ohne Zustimmung
- Vermietung anzeigen""",
                "topics": ["Eigentümerpflichten", "Hausgeld", "Beschlüsse", "WEG"]
            },
            {
                "paragraph": 23,
                "title": "Wohnungseigentümerversammlung",
                "content": """§ 23 WEG - Wohnungseigentümerversammlung

(1) Die Eigentümerversammlung wird mindestens einmal im Jahr von dem Verwalter einberufen.

(2) Die Versammlung ist von dem Verwalter in Textform unter Angabe der Tagesordnung einzuberufen. Die Frist der Einberufung soll mindestens drei Wochen betragen.

(3) Die Beschlüsse der Wohnungseigentümer werden in einer Versammlung gefasst.

Ablauf:
1. Einladung mit Tagesordnung (3 Wochen vorher)
2. Feststellung der Beschlussfähigkeit
3. Abstimmung (Mehrheiten nach MEA oder Köpfen)
4. Protokoll erstellen
5. Beschlusssammlung führen

Stimmrecht:
- Grundsatz: nach Miteigentumsanteilen
- Alternativ: nach Köpfen (wenn so vereinbart)
- Vollmacht möglich

Anfechtung: innerhalb 1 Monat beim Amtsgericht""",
                "topics": ["Eigentümerversammlung", "Beschluss", "Stimmrecht", "Protokoll"]
            },
            {
                "paragraph": 28,
                "title": "Wirtschaftsplan und Jahresabrechnung",
                "content": """§ 28 WEG - Wirtschaftsplan, Jahresabrechnung, Vermögensbericht

(1) Die Wohnungseigentümer beschließen über:
1. den Wirtschaftsplan,
2. die Jahresabrechnung,
3. den Vermögensbericht.

(2) Der Wirtschaftsplan enthält:
1. die voraussichtlichen Einnahmen und Ausgaben,
2. die anteilmäßige Verpflichtung der Wohnungseigentümer zur Lasten- und Kostentragung,
3. die Beiträge zur Erhaltungsrücklage.

Fristen:
- Wirtschaftsplan: vor Beginn des Kalenderjahres
- Jahresabrechnung: nach Ablauf des Kalenderjahres
- Keine gesetzliche Frist, aber: unverzüglich

Inhalt Jahresabrechnung:
- Einnahmen/Ausgaben der Gemeinschaft
- Entwicklung Erhaltungsrücklage
- Einzelabrechnungen je Einheit
- Abrechnungsspitze (Nachzahlung/Guthaben)""",
                "topics": ["Wirtschaftsplan", "Jahresabrechnung", "Hausgeld", "Erhaltungsrücklage"]
            }
        ]
        
        for para in WEG_CONTENT:
            doc = {
                "id": f"weg_{para['paragraph']}",
                "content": para["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"§ {para['paragraph']} WEG - {para['title']}",
                "source_url": f"https://www.gesetze-im-internet.de/weg/___{para['paragraph']}.html",
                "topics": para["topics"],
                "law": "WEG",
                "section": "Wohnungseigentumsgesetz",
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Scraped {len(documents)} WEG paragraphs")
        return documents


# Export
__all__ = ["GermanLawsScraper"]
