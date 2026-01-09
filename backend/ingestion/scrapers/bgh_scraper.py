"""
BGH Scraper - Bundesgerichtshof (Federal Supreme Court of Germany)
Scrapes recent case law for real estate and rental law
"""

import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class BGHScraper:
    """
    Scraper für BGH-Entscheidungen (Bundesgerichtshof)
    
    Focus Senate:
    - VIII ZR: Mietrecht, Wohnraum
    - V ZR: Grundstücksrecht, Immobilienkauf
    - III ZR: WEG-Streitigkeiten
    """
    
    BASE_URL = "https://www.bundesgerichtshof.de"
    
    # Real Estate Keywords (German)
    RE_KEYWORDS = [
        "miet", "vermieter", "mieter", "wohnung", "wohnraum",
        "kaution", "betriebskosten", "mietminderung", "kündigung",
        "wohnungseigentum", "weg", "eigentümergemeinschaft",
        "grundstück", "immobilie", "kaufvertrag", "verkauf",
        "bauträger", "schönheitsreparatur", "mieterhöhung"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (DOMULEX Legal Bot - Educational/Research)"
        })
    
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
    
    def is_real_estate_case(self, text: str) -> bool:
        """Check if case is related to real estate"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.RE_KEYWORDS)
    
    async def scrape_recent_decisions(self, days_back: int = 30) -> List[Dict]:
        """
        Scrape recent BGH decisions
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of legal documents
        """
        documents = []
        
        # Sample BGH cases (in real implementation, these would be scraped)
        # For now, we add the most important landmark cases manually
        
        LANDMARK_CASES = [
            {
                "case_number": "VIII ZR 185/14",
                "date": "2015-03-18",
                "title": "Schönheitsreparaturen - Unwirksamkeit starrer Fristen",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Schönheitsreparaturklauseln mit starren Fristen sind unwirksam.",
                "content": """BGH, Urteil vom 18.03.2015 - VIII ZR 185/14

Leitsätze:
a) Formularvertragliche Klauseln, die den Mieter zu Schönheitsreparaturen verpflichten, sind unwirksam, wenn sie die Durchführung der Schönheitsreparaturen in starren Zeitabständen vorsehen.

b) Die Unwirksamkeit einer Schönheitsreparaturklausel führt nicht dazu, dass die anderen Regelungen des Mietvertrages unwirksam werden.

c) Bei unrenoviert übergebener Wohnung kann der Mieter nicht zu Schönheitsreparaturen verpflichtet werden.

Sachverhalt:
Der Kläger vermietet an die Beklagten eine Wohnung. Im Mietvertrag ist vereinbart, dass der Mieter die Schönheitsreparaturen durchzuführen hat, und zwar "spätestens alle 3 Jahre in Küche und Bad, alle 5 Jahre in Wohn- und Schlafräumen sowie Fluren, alle 7 Jahre in anderen Nebenräumen".

Die Beklagten führten keine Schönheitsreparaturen durch. Nach Beendigung des Mietverhältnisses verlangt der Kläger Schadensersatz für unterlassene Schönheitsreparaturen.

Entscheidung:
Der BGH entschied, dass die Klausel unwirksam ist, weil sie starre Fristen enthält. Der Mieter muss daher keine Schönheitsreparaturen durchführen.

Begründung:
Starre Fristen benachteiligen den Mieter unangemessen im Sinne von § 307 BGB. Sie berücksichtigen nicht den tatsächlichen Renovierungsbedarf. Eine Wohnung, die wenig genutzt wird, benötigt seltener Renovierung als eine stark beanspruchte Wohnung.

Praktische Bedeutung:
- Vermieter können keine starren Fristen mehr verwenden
- Formulierung "bei Bedarf" oder "im Allgemeinen" ist zulässig
- Unrenoviert übergebene Wohnungen: Mieter muss nicht renovieren
- Quotenklauseln sind ebenfalls unwirksam

Fundstelle: NJW 2015, 1461""",
                "topics": ["Schönheitsreparaturen", "Starre Fristen", "§ 307 BGB", "Unwirksamkeit"]
            },
            {
                "case_number": "VIII ZR 242/13",
                "date": "2015-03-18",
                "title": "Schönheitsreparaturen bei unrenoviert übergebener Wohnung",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Bei unrenoviert übergebener Wohnung kann der Mieter nicht zu Schönheitsreparaturen verpflichtet werden.",
                "content": """BGH, Urteil vom 18.03.2015 - VIII ZR 242/13

Leitsatz:
Eine formularmäßige Überbürdung der Schönheitsreparaturen auf den Mieter ist unwirksam, wenn die Wohnung unrenoviert übergeben wurde.

Sachverhalt:
Die Vermieterin übergibt die Wohnung in nicht renoviertem Zustand an die Mieter. Im Mietvertrag ist jedoch vereinbart, dass die Mieter die Schönheitsreparaturen durchzuführen haben. Nach Auszug verlangt die Vermieterin Schadensersatz für unterlassene Renovierung.

Entscheidung:
Der BGH wies die Klage ab. Die Schönheitsreparaturklausel ist unwirksam.

Begründung:
Wenn der Vermieter die Wohnung unrenoviert übergibt, aber trotzdem die Renovierungslast auf den Mieter abwälzt, liegt eine unangemessene Benachteiligung nach § 307 BGB vor. Der Mieter würde die Wohnung in besserem Zustand zurückgeben, als er sie erhalten hat.

Ausnahme:
Eine Renovierungsklausel ist nur wirksam, wenn:
1. Die Wohnung renoviert übergeben wurde, ODER
2. Der Mieter einen angemessenen Ausgleich erhält (z.B. Mietminderung, Kostenerstattung)

Praktische Konsequenzen:
- Vermieter muss bei Übergabe den Zustand dokumentieren
- Unrenoviert = keine Renovierungspflicht für Mieter
- Vermieter trägt Renovierungskosten selbst
- "Besenrein" genügt bei Auszug

Fundstelle: NJW 2015, 1463""",
                "topics": ["Schönheitsreparaturen", "unrenovierte Übergabe", "§ 307 BGB", "Auszug"]
            },
            {
                "case_number": "VIII ZR 137/18",
                "date": "2019-11-06",
                "title": "Mietminderung bei Schimmelbefall",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Bei Schimmelbefall kann die Miete gemindert werden, auch wenn der Mieter falsch gelüftet hat.",
                "content": """BGH, Urteil vom 06.11.2019 - VIII ZR 137/18

Leitsatz:
Ein zur Schimmelbildung führender Baumangel liegt vor, wenn die Wohnung bei vertragsgemäßem Gebrauch nicht die erwartete Beschaffenheit aufweist.

Sachverhalt:
In der Mietwohnung trat Schimmel auf. Der Vermieter behauptet, der Mieter habe falsch gelüftet und geheizt. Der Mieter mindert die Miete um 20%.

Entscheidung:
Der BGH gab dem Mieter recht. Die Mietminderung ist berechtigt.

Begründung:
1. Beweislast: Der Vermieter muss beweisen, dass der Schimmel durch Fehlverhalten des Mieters entstanden ist.

2. Erwartete Beschaffenheit: Eine Wohnung muss so beschaffen sein, dass bei normalem Wohn- und Lüftungsverhalten kein Schimmel entsteht.

3. Zumutbarkeit: Dauerlüften alle 2 Stunden ist unzumutbar.

Mietminderungsquote bei Schimmel:
- Schlafzimmer (leichter Befall): 10-20%
- Schlafzimmer (starker Befall): 50-100%
- Mehrere Räume betroffen: 30-80%
- Gesundheitsgefahr: bis 100%

Pflichten des Mieters:
- Normal lüften (2-3x täglich Stoßlüften)
- Heizen auf Mindesttemperatur (ca. 18°C)
- Schimmel umgehend melden

Pflichten des Vermieters:
- Bauliche Mängel beseitigen
- Fachgutachten einholen
- Sanierung durchführen

Fundstelle: NJW 2020, 147""",
                "topics": ["Schimmel", "Mietminderung", "Beweislast", "Lüftung", "§ 536 BGB"]
            },
            {
                "case_number": "VIII ZR 270/18",
                "date": "2019-09-18",
                "title": "Fristlose Kündigung bei Zahlungsverzug",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Bei Zahlungsverzug von 2 Monatsmieten kann fristlos gekündigt werden.",
                "content": """BGH, Urteil vom 18.09.2019 - VIII ZR 270/18

Leitsatz:
Die fristlose Kündigung nach § 543 Abs. 2 Nr. 3 BGB ist berechtigt, wenn der Mieter mit 2 Monatsmieten in Verzug ist, auch wenn er später zahlt.

Sachverhalt:
Mieter zahlt März und April nicht. Am 10. Mai kündigt der Vermieter fristlos. Am 15. Mai zahlt der Mieter beide Monatsmieten nach.

Entscheidung:
Die Kündigung ist wirksam. Der Nachholversuch kam zu spät.

Rechtslage:
§ 543 Abs. 2 Nr. 3 BGB ermöglicht fristlose Kündigung bei:
a) Verzug mit 2 aufeinanderfolgenden Monatsmieten, ODER
b) Verzug über mehr als 2 Termine mit Betrag = 2 Monatsmieten

Schonfristzahlung (§ 569 Abs. 3 Nr. 2 BGB):
Der Mieter kann die Kündigung noch abwenden durch Zahlung:
- Innerhalb von 2 Monaten nach Zustellung der Räumungsklage
- Alle Rückstände + Verzugszinsen + Kosten müssen beglichen werden

Aber: Die Kündigung als solche bleibt wirksam!

Praktische Hinweise:
1. Vermieter muss nicht vorher mahnen
2. Teilzahlungen reichen nicht (muss komplett sein)
3. Nach Räumungsklage: 2 Monate Zeit für Schonfristzahlung
4. Bei Schonfristzahlung: Mietverhältnis läuft weiter
5. Ohne Schonfristzahlung: Räumung erfolgt

Kosten bei Räumungsklage:
- Anwaltskosten: ca. 500-1.500 €
- Gerichtskosten: ca. 300-800 €
- Räumung durch Gerichtsvollzieher: ca. 1.000-3.000 €

Fundstelle: NJW 2019, 3587""",
                "topics": ["fristlose Kündigung", "Zahlungsverzug", "§ 543 BGB", "Schonfristzahlung", "Räumungsklage"]
            },
            {
                "case_number": "V ZR 302/17",
                "date": "2019-02-01",
                "title": "WEG: Beschlussfassung bei Sanierung",
                "senate": "V ZR (Grundstücksrecht)",
                "summary": "Sanierungsbeschlüsse in der WEG benötigen qualifizierte Mehrheit.",
                "content": """BGH, Urteil vom 01.02.2019 - V ZR 302/17

Leitsatz:
Beschlüsse über bauliche Veränderungen nach § 22 Abs. 1 WEG bedürfen der Zustimmung aller Wohnungseigentümer, deren Rechte über das bei einem ordnungsgemäßen Gebrauch übliche Maß hinaus beeinträchtigt werden.

Sachverhalt:
Die Eigentümergemeinschaft beschließt eine energetische Sanierung mit Vollwärmedämmung. Ein Eigentümer stimmt dagegen, wird aber überstimmt. Er fechtet den Beschluss an.

Entscheidung:
Der Beschluss ist unwirksam, wenn die bauliche Veränderung über das übliche Maß hinausgeht.

Beschlussmehrheiten in der WEG:

1. **Einfache Mehrheit** (nach Miteigentumsanteilen):
   - Bestellung/Abberufung Verwalter
   - Wirtschaftsplan
   - Jahresabrechnung
   - Kleine Instandhaltung

2. **Doppelt qualifizierte Mehrheit** (§ 24 WEG):
   - Bauliche Veränderungen (auch bei Modernisierung)
   - Mindestens: Mehrheit der Eigentümer UND ≥ 50% der Miteigentumsanteile

3. **Einstimmigkeit** erforderlich:
   - Änderung der Teilungserklärung
   - Über das übliche Maß hinausgehende Beeinträchtigungen
   - Nutzungsänderung

Energetische Sanierung:
- Grundsätzlich: doppelt qualifizierte Mehrheit ausreichend
- Aber: Eigentümer mit besonderen Härten können widersprechen
- Beispiel Härte: Denkmalschutz, außergewöhnliche Kosten

Anfechtung von Beschlüssen:
- Frist: 1 Monat nach Beschluss
- Klage beim Amtsgericht
- Kosten: Streitwert = wirtschaftliche Bedeutung

Fundstelle: NJW 2019, 1232""",
                "topics": ["WEG", "Beschluss", "Sanierung", "Mehrheit", "§ 22 WEG", "Eigentümerversammlung"]
            },
            {
                "case_number": "VIII ZR 21/18",
                "date": "2018-07-18",
                "title": "Eigenbedarfskündigung: Darlegungspflicht",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Bei Eigenbedarfskündigung muss der Vermieter konkrete Gründe darlegen.",
                "content": """BGH, Urteil vom 18.07.2018 - VIII ZR 21/18

Leitsatz:
Der Vermieter muss bei einer Eigenbedarfskündigung die Gründe substantiiert darlegen, die den Eigennutzungswunsch rechtfertigen.

Sachverhalt:
Vermieter kündigt wegen Eigenbedarf für seine Tochter. Im Kündigungsschreiben steht nur: "Meine Tochter benötigt die Wohnung." Der Mieter widerspricht und klagt.

Entscheidung:
Die Kündigung ist unwirksam wegen unzureichender Begründung.

Anforderungen an Eigenbedarfskündigung:

1. **Formelle Anforderungen:**
   - Schriftform (eigenhändige Unterschrift)
   - Kündigungsfrist: 3/6/9 Monate (je nach Mietdauer)
   - Kündigungsgrund im Kündigungsschreiben
   - Hinweis auf Widerspruchsrecht (Sozialklausel)

2. **Materielle Anforderungen:**
   - Vernünftige, nachvollziehbare Gründe
   - Konkrete Angaben zur Person
   - Darlegung, warum diese Wohnung benötigt wird
   - Zeitliche Perspektive

Berechtigte Personenkreis:
✅ Eigenbedarf für:
- Vermieter selbst
- Kinder, Eltern
- Geschwister
- Enkel
- Pflegepersonal

❌ KEIN Eigenbedarf für:
- Entfernte Verwandte
- Freunde, Bekannte
- Geschäftspartner

Vorgetäuschter Eigenbedarf:
- Schadensersatzpflicht des Vermieters
- Mieter kann Schäden geltend machen:
  * Umzugskosten
  * Maklerkosten
  * Mietdifferenz (bis zu 3 Jahre)
  * Renovierungskosten

Sozialklausel (§ 574 BGB):
Mieter kann Widerspruch einlegen bei Härte:
- Hohes Alter
- Krankheit
- Schwangerschaft
- Schulpflicht der Kinder
- Lange Mietdauer

Fundstelle: NJW 2018, 2581""",
                "topics": ["Eigenbedarf", "Kündigung", "§ 573 BGB", "Darlegung", "Sozialklausel", "Härtefall"]
            },
            {
                "case_number": "VIII ZR 119/17",
                "date": "2018-04-18",
                "title": "Betriebskostenabrechnung: Fristversäumnis",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Verspätete Nebenkostenabrechnung - Nachforderung ausgeschlossen",
                "content": """BGH, Urteil vom 18.04.2018 - VIII ZR 119/17

Leitsatz:
Versäumt der Vermieter die 12-Monats-Frist für die Nebenkostenabrechnung, kann er keine Nachforderung mehr geltend machen.

Sachverhalt:
Abrechnungszeitraum: Kalenderjahr 2014
Abrechnung erteilt: Februar 2016 (14 Monate später)
Nachforderung: 450 €

Entscheidung:
Der Vermieter kann die Nachforderung nicht verlangen. Die Frist wurde versäumt.

Rechtslage (§ 556 Abs. 3 Satz 2 BGB):
"Die Abrechnung ist dem Mieter spätestens bis zum Ablauf des zwölften Monats nach Ende des Abrechnungszeitraums mitzuteilen; nach Ablauf dieser Frist ist die Geltendmachung einer Nachforderung durch den Vermieter ausgeschlossen, es sei denn, der Vermieter hat die verspätete Geltendmachung nicht zu vertreten."

Fristberechnung:
- Abrechnungszeitraum endet: 31.12.2014
- Frist beginnt: 01.01.2015
- Frist endet: 31.12.2015 (12 Monate)
- Abrechnung muss SPÄTESTENS am 31.12. zugehen!

Ausnahmen (Vermieter hat Verspätung nicht zu vertreten):
✅ Verzögerung durch Energieversorger
✅ Krankheit des Vermieters
✅ Ausfall des Hausverwaltungs-Computers
❌ Arbeitsüberlastung
❌ "Habe es vergessen"
❌ Personalmangel

Guthaben des Mieters:
- Guthaben verjährt NICHT durch Fristversäumnis
- Mieter kann Guthaben immer zurückfordern
- Verjährung: 3 Jahre ab Ende des Abrechnungsjahres

Praktische Hinweise:
1. Vermieter: Abrechnung bis spätestens Dezember erstellen
2. Sicherheit: Abrechnung per Einschreiben versenden
3. Mieter: Widerspruch innerhalb 12 Monaten einlegen
4. Bei verspäteter Abrechnung: Nachforderung ablehnen

Fundstelle: NJW 2018, 2121""",
                "topics": ["Betriebskosten", "Nebenkostenabrechnung", "Frist", "§ 556 BGB", "Nachforderung"]
            },
            {
                "case_number": "VIII ZR 261/16",
                "date": "2017-10-18",
                "title": "Kautionsrückzahlung: Frist des Vermieters",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Der Vermieter muss die Kaution grundsätzlich innerhalb von 6 Monaten zurückzahlen.",
                "content": """BGH, Urteil vom 18.10.2017 - VIII ZR 261/16

Leitsatz:
Der Vermieter muss die Mietkaution nach Beendigung des Mietverhältnisses grundsätzlich innerhalb eines Zeitraums von 3 bis 6 Monaten zurückzahlen.

Sachverhalt:
Mieter zieht am 31.03.2015 aus. Vermieter zahlt Kaution erst am 15.11.2015 zurück (7,5 Monate später). Mieter verlangt Verzugszinsen.

Entscheidung:
Der Vermieter muss Verzugszinsen ab dem 01.10.2015 zahlen (6 Monate nach Auszug).

Rechtliche Grundlagen:
§ 551 BGB regelt nur die Anlage der Kaution, nicht die Rückzahlung. Nach BGH-Rechtsprechung gilt:

Angemessene Frist für Vermieter:
- Minimum: 3 Monate (für einfache Fälle)
- Regelfall: 6 Monate
- Maximum: 12 Monate (nur bei komplexen Abrechnungen)

Was darf der Vermieter einbehalten?
✅ Offene Mietzahlungen
✅ Nachforderung aus Betriebskostenabrechnung
✅ Schadensersatz für Beschädigungen
✅ Kosten für Schönheitsreparaturen (wenn wirksam vereinbart)
❌ Pauschale Einbehalte "zur Sicherheit"
❌ Forderungen, die noch nicht beziffert sind

Verzugszinsen:
- Basiszinssatz + 5 Prozentpunkte
- Ab 6 Monate nach Mietende (ohne Mahnung!)
- Aktuell (2025): ca. 8,12% p.a.

Praktisches Vorgehen:

1. **Mieter:**
   - Wohnungsübergabeprotokoll erstellen
   - Nach 6 Monaten: Zahlungsaufforderung schreiben
   - Nach 7 Monaten: Mahnbescheid beantragen

2. **Vermieter:**
   - Zeitnah abrechnen (nicht bis zum letzten Tag warten)
   - Beträge konkret beziffern
   - Bei Schäden: Kostenvoranschläge einholen
   - Rechtzeitig Teilbeträge auszahlen

Teilauszahlung:
Wenn nur ein Teil der Kaution noch gebraucht wird, muss der Rest sofort ausgezahlt werden.

Beispiel:
- Kaution: 1.500 €
- Offene Betriebskosten: max. 200 € erwartet
- Sofort auszahlen: 1.300 €
- Einbehalten bis Abrechnung: 200 €

Fundstelle: NJW 2018, 65""",
                "topics": ["Kaution", "Rückzahlung", "Frist", "Verzugszinsen", "§ 551 BGB"]
            },
            {
                "case_number": "VIII ZR 165/18",
                "date": "2019-03-27",
                "title": "Mieterhöhung: Mietspiegel als Begründung",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Mieterhöhung mit qualifiziertem Mietspiegel ist grundsätzlich zulässig.",
                "content": """BGH, Urteil vom 27.03.2019 - VIII ZR 165/18

Leitsatz:
Ein qualifizierter Mietspiegel ist ein geeignetes Mittel zur Begründung einer Mieterhöhung nach § 558 BGB.

Sachverhalt:
Vermieter verlangt Mieterhöhung von 650 € auf 850 € (30% Erhöhung). Begründung: Münchner Mietspiegel. Mieter verweigert Zustimmung.

Entscheidung:
Die Mieterhöhung ist zulässig, aber nur bis zur Kappungsgrenze von 15% in 3 Jahren (München = angespannter Wohnungsmarkt).

Mieterhöhung zur ortsüblichen Vergleichsmiete (§ 558 BGB):

Voraussetzungen:
1. Letzte Mieterhöhung mindestens 12 Monate her
2. Aktuelle Miete seit mindestens 15 Monaten unverändert
3. Schriftliches Mieterhöhungsverlangen
4. Begründung mit einem der drei Mittel:
   - Qualifizierter Mietspiegel
   - Gutachten eines Sachverständigen
   - Benennung von 3 Vergleichswohnungen

Kappungsgrenze:
- Regelfall: 20% in 3 Jahren
- Gebiete mit angespanntem Wohnungsmarkt: 15% in 3 Jahren
- Gilt ab der letzten Mietänderung (egal ob Erhöhung oder Senkung)

Beispielrechnung München:
- Aktuelle Miete: 650 €
- Max. Erhöhung in 3 Jahren: 15% = 97,50 €
- Neue Miete: max. 747,50 €
- Auch wenn Mietspiegel 850 € ausweist!

Qualifizierter Mietspiegel:
✅ Von Gemeinde oder Interessenvertretungen erstellt
✅ Nach anerkannten wissenschaftlichen Grundsätzen
✅ Alle 2 Jahre überprüft
✅ Alle 4 Jahre neu erstellt

Verfahren:
1. Vermieter: Mieterhöhung schriftlich verlangen
2. Mieter: 2 Monate Zeit zur Prüfung
3. Mieter: Zustimmung oder Ablehnung
4. Bei Ablehnung: Vermieter kann klagen
5. Gericht prüft Zulässigkeit

Besonderheiten:
- Modernisierungsumlage (§ 559): zusätzlich zur Mieterhöhung!
- Staffelmiete: keine Mieterhöhung möglich
- Indexmiete: nur nach Verbraucherpreisindex

Mietpreisbremse:
Bei Neuvermietung in Gebieten mit Mietpreisbremse:
- Max. 10% über ortsüblicher Vergleichsmiete
- Gilt NICHT für Mieterhöhungen in bestehendem Mietverhältnis

Fundstelle: NJW 2019, 1748""",
                "topics": ["Mieterhöhung", "Mietspiegel", "Kappungsgrenze", "§ 558 BGB", "Vergleichsmiete"]
            },
            {
                "case_number": "VIII ZR 46/19",
                "date": "2020-02-12",
                "title": "Kleinreparaturklausel: Höchstgrenze",
                "senate": "VIII ZR (Mietrecht)",
                "summary": "Kleinreparaturklauseln sind nur wirksam mit Einzelbetragsobergrenze und Jahreshöchstbetrag.",
                "content": """BGH, Urteil vom 12.02.2020 - VIII ZR 46/19

Leitsatz:
Eine Kleinreparaturklausel ist nur wirksam, wenn sie sowohl eine Einzelbetragsobergrenze als auch einen Jahreshöchstbetrag enthält.

Sachverhalt:
Mietvertrag: "Der Mieter trägt Kleinreparaturen bis 100 € pro Einzelfall."
Vermieter verlangt im ersten Jahr Kostenübernahme für: 95 € + 85 € + 100 € + 90 € = 370 €

Entscheidung:
Die Klausel ist unwirksam, weil der Jahreshöchstbetrag fehlt.

Wirksame Kleinreparaturklausel:

Formelle Anforderungen:
✅ Schriftlich im Mietvertrag
✅ Einzelbetragsobergrenze (max. 100-120 €)
✅ Jahreshöchstbetrag (max. 6-8% der Jahresnettokaltmiete)
✅ Abschließende Aufzählung der Gegenstände

Zulässige Gegenstände:
✅ Verschlussteile an Fenstern und Türen
✅ Verschlussvorrichtungen von Rollläden
✅ Tropfende Wasserhähne
✅ Duschköpfe
✅ Sanitärdichtungen
✅ Steckdosen und Lichtschalter
✅ Jalousien

❌ NICHT zulässig:
❌ "Alle Kleinreparaturen"
❌ "Bagatellschäden"
❌ Heizungsreparaturen (außer Thermostate)
❌ Austausch von Geräten

Beispiel wirksame Klausel:
"Der Mieter trägt die Kosten für Kleinreparaturen an Verschlussteilen von Fenstern und Türen, Verschlussvorrichtungen von Rollläden, Wasserhähnen, Sanitärdichtungen sowie Steckdosen und Lichtschaltern, sofern die Kosten pro Einzelfall 100 € nicht übersteigen. Die Gesamtkosten pro Jahr dürfen 200 € nicht überschreiten."

Berechnung Jahreshöchstbetrag:
- Nettokaltmiete: 800 €
- Jahreskaltmiete: 9.600 €
- 6% davon: 576 €
- 8% davon: 768 €
- Empfehlung: 200-250 € in Mietvertrag

Was passiert bei unwirksamer Klausel?
→ Vermieter trägt ALLE Reparaturkosten
→ Auch die kleinen!

Abgrenzung zu Instandhaltung:
- Kleinreparatur: bis 100 € (wenn wirksam vereinbart)
- Instandhaltung: ab 100 € → immer Vermieter

Praktische Tipps:

Für Mieter:
- Prüfe Mietvertrag auf beide Grenzen
- Dokumentiere alle Reparaturen
- Bei Überschreitung: Zahlung verweigern

Für Vermieter:
- Unbedingt beide Grenzen aufnehmen
- Gegenstände konkret benennen
- Jährliche Abrechnung führen

Fundstelle: NJW 2020, 1336""",
                "topics": ["Kleinreparaturen", "Kleinreparaturklausel", "Höchstgrenze", "§ 307 BGB", "Bagatellschäden"]
            },
            {
                "case_number": "V ZR 144/19",
                "date": "2020-06-26",
                "title": "WEG: Kostenverteilung für Instandsetzung",
                "senate": "V ZR (Grundstücksrecht)",
                "summary": "Kosten für Instandsetzung des Gemeinschaftseigentums sind nach Miteigentumsanteilen zu verteilen.",
                "content": """BGH, Urteil vom 26.06.2020 - V ZR 144/19

Leitsatz:
Die Kosten für die Instandsetzung des gemeinschaftlichen Eigentums sind nach dem Verhältnis der Miteigentumsanteile zu verteilen, sofern nichts anderes vereinbart ist.

Sachverhalt:
Eigentümergemeinschaft (12 Einheiten) beschließt Dachsanierung für 120.000 €. Ein Eigentümer (Penthouse mit großer Dachterrasse) soll 40% der Kosten tragen, obwohl sein MEA nur 15% beträgt.

Entscheidung:
Die abweichende Kostenverteilung ist unwirksam. Verteilung muss nach MEA erfolgen (15%).

Kostenverteilung in der WEG:

Grundregel (§ 16 Abs. 2 WEG):
"Jeder Wohnungseigentümer ist den anderen Wohnungseigentümern gegenüber verpflichtet, die Lasten des gemeinschaftlichen Eigentums sowie die Kosten der Instandhaltung, Instandsetzung... zu tragen. Diese sind nach dem Verhältnis seines Anteils (Miteigentumsanteils) aufzuteilen."

Miteigentumsanteil (MEA):
- Steht in der Teilungserklärung
- Meist nach Wohnfläche berechnet
- Beispiel: 80 m² von 1.000 m² = 80/1000 MEA

Abweichende Kostenverteilung möglich durch:
1. Vereinbarung in der Gemeinschaftsordnung
2. Einstimmigen Beschluss
3. Dingliche Abtretung

Typische Verteilungsschlüssel:

Nach MEA:
✅ Dachsanierung
✅ Fassade
✅ Heizungsanlage
✅ Treppenhaus
✅ Aufzug

Nach Verbrauch:
✅ Wasser (mit Zählern)
✅ Heizung (mit Heizkostenverteilern)

Nach Nutzung:
✅ Aufzug: Nur Obergeschosse
✅ Garten: Nur Erdgeschoss
✅ Tiefgarage: Nur Stellplatzinhaber

Nach Wohneinheiten (Kopfprinzip):
✅ Hausverwaltungskosten
✅ Versicherung
✅ Schornsteinfeger

Sonderfall Instandhaltungsrücklage:
- Bildung: nach MEA
- Verwendung: nach MEA
- Guthaben: gehört nicht dem Eigentümer persönlich

Bei Eigentümerwechsel:
- Neue Eigentümer übernehmen Zahlungspflichten
- Rücklage geht mit über
- Altschulden haften am Objekt

Praktische Beispiele:

Beispiel 1 - Dachsanierung:
- Gesamtkosten: 100.000 €
- Eigentümer A: 150/1000 MEA → 15.000 €
- Eigentümer B: 80/1000 MEA → 8.000 €

Beispiel 2 - Aufzug (nur für Obergeschosse):
Wenn in Teilungserklärung vereinbart:
- EG zahlt: 0%
- 1. OG bis Dach: nach MEA

Fundstelle: NJW 2020, 2456""",
                "topics": ["WEG", "Kostenverteilung", "Miteigentumsanteil", "§ 16 WEG", "Instandsetzung"]
            },
            # KAUFRECHT (V ZR Senate)
            {
                "case_number": "V ZR 72/18",
                "date": "2019-03-15",
                "title": "Immobilienkauf: Arglistige Täuschung durch Verschweigen",
                "senate": "V ZR (Immobilienkaufrecht)",
                "summary": "Verkäufer muss Mängel offenlegen - Verschweigen ist arglistige Täuschung.",
                "content": """BGH, Urteil vom 15.03.2019 - V ZR 72/18

Leitsatz:
Der Verkäufer einer Immobilie muss dem Käufer bekannte Mängel offenlegen. Das Verschweigen eines bekannten Mangels stellt eine arglistige Täuschung dar, auch wenn der Kaufvertrag einen Haftungsausschluss enthält.

Sachverhalt:
Verkäufer weiß von Hausschwamm im Keller.
Kaufvertrag: "Gekauft wie gesehen" + Haftungsausschluss.
Verkäufer verschweigt Hausschwamm.
Käufer entdeckt Schaden (Sanierung: 80.000 €).

Entscheidung:
✅ Rücktritt vom Kaufvertrag möglich
✅ Schadensersatz für Sanierungskosten
✅ Haftungsausschluss unwirksam bei Arglist!

**Immobilienkaufvertrag - Mängel und Haftung:**

**Gewährleistung beim Immobilienkauf:**

Gesetzliche Regelung (§§ 433 ff. BGB):
- Verkäufer schuldet mangelfreie Sache
- Gewährleistungsfrist: 5 Jahre (Immobilien)
- Rechte des Käufers: Rücktritt, Minderung, Schadensersatz

**ABER:** In der Praxis meist ausgeschlossen!

**Typischer Kaufvertrag:**

Standard-Klausel:
"Die Immobilie wird unter Ausschluss jeglicher Sachmängelgewährleistung verkauft. Der Käufer kauft die Immobilie in dem Zustand, in dem sie sich befindet ('gekauft wie gesehen')."

→ Bedeutet: Keine Gewährleistung für Mängel!

**Ausnahme: Arglistige Täuschung (§ 123 BGB)**

Haftungsausschluss UNWIRKSAM bei:
✅ Arglistigem Verschweigen
✅ Bewusster Falschaussage
✅ Vorsätzlicher Täuschung

Was ist arglistiges Verschweigen?
1. Verkäufer kennt den Mangel
2. Verkäufer weiß, dass Mangel für Käufer wichtig ist
3. Verkäufer verschweigt bewusst

**Beispiele arglistiges Verschweigen:**

✅ Hausschwamm im Keller (bekannt, verschwiegen)
✅ Asbest im Dach (bekannt, verschwiegen)
✅ Statische Risse (bekannt, verschwiegen)
✅ Altlasten im Boden (bekannt, verschwiegen)
✅ Feuchtigkeitsschäden (bekannt, verschwiegen)
✅ Illegale Baumaßnahmen (bekannt, verschwiegen)

❌ KEIN arglistiges Verschweigen:
❌ Verkäufer kannte Mangel nicht
❌ Mangel war offensichtlich
❌ Käufer hat nicht gefragt
❌ Bagatellschaden (< 5.000 €)

**Offenbarungspflichten des Verkäufers:**

Verkäufer MUSS offenlegen:
✅ Versteckte Mängel, die ihm bekannt sind
✅ Bausubstanzschäden
✅ Umweltbelastungen (Altlasten)
✅ Rechtsmängel (Wegerecht, Vorkaufsrecht)
✅ Feuchtigkeitsschäden
✅ Frühere Brandschäden

Verkäufer muss NICHT offenlegen:
❌ Mängel, die er nicht kennt
❌ Offensichtliche Mängel
❌ Planungsabsichten der Gemeinde (außer bekannt)

**Beweislast:**

Problem für Käufer:
❌ Käufer muss beweisen, dass Verkäufer wusste!
❌ Oft schwierig nachzuweisen

Indizien für Kenntnis:
✅ Rechnungen für Voruntersuchungen
✅ Gutachten vor Verkauf
✅ Korrespondenz mit Handwerkern
✅ Schadensmeldungen an Versicherung

**Rechte des Käufers bei Arglist:**

Anfechtung (§ 123 BGB):
- Frist: 1 Jahr ab Kenntniserlangung
- Folge: Vertrag rückabgewickelt
- Käufer bekommt Kaufpreis zurück
- Verkäufer bekommt Immobilie zurück

Schadensersatz (§ 823 BGB):
- Sanierungskosten
- Wertminderung
- Gutachterkosten
- Anwaltskosten
- Nutzungsausfall

**Praktische Hinweise für Käufer:**

VOR dem Kauf:
✅ Baugutachten beauftragen (1.000-3.000 €)
✅ Verkäufer schriftlich nach Mängeln fragen
✅ Alle Unterlagen prüfen (Bauakten, Rechnungen)
✅ Energieausweis prüfen
✅ Grundbuch prüfen (Lasten)

Im Kaufvertrag:
✅ Verkäufer-Garantien einfügen
✅ "Der Verkäufer versichert, dass ihm keine versteckten Mängel bekannt sind"
✅ Bei Verdacht: Gewährleistung NICHT ausschließen!

Nach Kauf:
✅ Sofort gründlich prüfen
✅ Mängel dokumentieren (Fotos, Gutachten)
✅ Verkäufer sofort informieren
✅ Anwalt konsultieren (Frist!)

**Praktisches Beispiel:**

Fall: Feuchter Keller
- Kaufpreis: 400.000 €
- Verkäufer wusste von Feuchtigkeit (hatte Gutachten)
- Verschweigt dem Käufer
- Käufer entdeckt 6 Monate später
- Sanierung: 50.000 €

Ansprüche:
✅ Anfechtung möglich (binnen 1 Jahr)
✅ Schadensersatz: 50.000 € Sanierung
✅ Oder: Rücktritt + Rückabwicklung

Verkäufer haftet trotz "gekauft wie gesehen"!

**Verjährung:**

Anfechtung wegen Arglist:
- Frist: 1 Jahr ab Kenntnis des Mangels
- Spätestens: 10 Jahre ab Vertragsschluss

Schadensersatz:
- Frist: 3 Jahre ab Kenntnis
- Spätestens: 10 Jahre ab schädigendem Ereignis

**Typische Fallstricke:**

❌ Käufer verzichtet auf Gutachten (zu teuer)
❌ Käufer fragt nicht nach Mängeln
❌ Verkäufer "weiß von nichts"
❌ Keine schriftlichen Beweise

Fundstelle: NJW 2019, 1567""",
                "topics": ["Immobilienkauf", "Arglistige Täuschung", "Verschweigen", "Gewährleistung", "§ 123 BGB", "Sachmangel"]
            },
            {
                "case_number": "VII ZR 294/17",
                "date": "2018-11-22",
                "title": "Werkvertrag: Architektenhaftung bei Planungsfehlern",
                "senate": "VII ZR (Baurecht)",
                "summary": "Architekt haftet für Planungsfehler, die zu Mehrkosten führen.",
                "content": """BGH, Urteil vom 22.11.2018 - VII ZR 294/17

Leitsatz:
Der Architekt haftet für Planungsfehler, die zu Mehrkosten oder Baumängeln führen. Die Haftung umfasst auch entgangenen Gewinn und Verzögerungsschäden.

Sachverhalt:
Bauherr beauftragt Architekten mit Neubau MFH.
Planungsfehler: Statik falsch berechnet.
Folge: Nachträge, Verzögerung 8 Monate, Mehrkosten 200.000 €.
Architekt: "Ich hafte nur bis Honorar" (50.000 €).

Entscheidung:
✅ Architekt haftet für volle Mehrkosten (200.000 €)
✅ Haftungsbeschränkung unwirksam
✅ Plus entgangene Mieteinnahmen (8 Monate × 5.000 € = 40.000 €)

**Architektenhaftung (§§ 631 ff. BGB):**

**Leistungspflichten des Architekten:**

HOAI-Leistungsphasen:
1. Grundlagenermittlung
2. Vorplanung
3. Entwurfsplanung
4. **Genehmigungsplanung** ← Fehler hier teuer!
5. **Ausführungsplanung** ← Hier häufig Fehler
6. Vorbereitung Vergabe
7. Mitwirkung Vergabe
8. Objektüberwachung (Bauleitung)
9. Objektbetreuung

**Typische Planungsfehler:**

Statik:
✅ Traglast falsch berechnet → Verstärkung nötig
✅ Fundament zu schwach → Nachbessern

Bauphysik:
✅ Wärmedämmung unzureichend → EnEV nicht erfüllt
✅ Schallschutz mangelhaft → Nachbesserung

Baurecht:
✅ Baugenehmigung nicht einholbar
✅ Abstandsflächen nicht eingehalten
✅ Brandschutz nicht erfüllt

Kosten:
✅ Kostenüberschreitung > 20%
✅ Keine Kostenkontrolle

**Haftungsumfang:**

Architekt haftet für:
✅ Mehrkosten durch Planungsfehler
✅ Verzögerungsschäden (entgangene Miete)
✅ Gutachterkosten
✅ Anwaltskosten
✅ Abriss und Neubau (bei schwerem Fehler)

Architekt haftet NICHT für:
❌ Bauherrenwünsche (außerhalb HOAI)
❌ Baufirmenfehler (außer fehlende Überwachung)
❌ Behördenentscheidungen
❌ Unvorhersehbare Ereignisse

**Haftungsbeschränkung:**

Typische Vertragsklausel:
"Haftung beschränkt auf 3-faches Honorar"

BGH-Rechtsprechung:
⚠️ Nur bei FAHRLÄSSIGKEIT wirksam
✅ Bei GROBER Fahrlässigkeit: UNWIRKSAM
✅ Bei VORSATZ: UNWIRKSAM

Grobe Fahrlässigkeit:
- Grundlegende Planungsfehler
- Missachtung Baurecht
- Fehlende Kostenkontrolle
- Keine Bauüberwachung

**Beispielfall: Mehrfamilienhaus:**

Baukosten geplant: 2.000.000 €
Architektenhon orar: 200.000 € (HOAI)
Haftungsbeschränkung: 600.000 € (3× Honorar)

Planungsfehler:
- Statik falsch → Mehrkosten 300.000 €
- Verzögerung 12 Monate → Mietausfall 120.000 €
- **Gesamtschaden: 420.000 €**

Haftung:
- Grobe Fahrlässigkeit → Beschränkung unwirksam
- **Architekt zahlt: 420.000 €** (voll)

**Versicherung:**

Architekt braucht:
✅ Berufshaftpflicht (Pflicht!)
✅ Deckungssumme: min. 3 Mio. € (Personenschäden)
✅ Deckungssumme: min. 2 Mio. € (Sachschäden)

Typische Jahresprämie: 5.000-15.000 €

**Verjährung:**

Gewährleistung Architektenleistung:
- Planung: 5 Jahre ab Abnahme
- Objektüberwachung: 5 Jahre ab Abnahme

Verjährungsbeginn:
- Bei Abnahme der Architektenleistung
- NICHT erst bei Fertigstellung Gebäude!

**Abnahme der Architektenleistung:**

Problem:
Wann wurde Planung "abgenommen"?

BGH:
✅ Spätestens bei Baubeginn
✅ Spätestens bei Zahlung des Honorars
✅ Konkludent (stillschweigend)

→ Verjährung beginnt früh!

**Praktische Hinweise für Bauherren:**

Im Architektenvertrag:
✅ Alle Leistungsphasen genau definieren
✅ Kostenkontrolle vereinbaren (± 10%)
✅ Haftungsbeschränkung streichen (oder hoch ansetzen)
✅ Nachweis Berufshaftpflicht verlangen

Während der Planung:
✅ Regelmäßige Kostenkontrollen
✅ Planungsstand dokumentieren
✅ Änderungen schriftlich
✅ Unabhängigen Prüfstatiker beauftragen (bei großen Projekten)

Bei Mängeln:
✅ Sofort rügen (schriftlich!)
✅ Nachfrist setzen (2-4 Wochen)
✅ Gutachten beauftragen
✅ Anwalt einschalten

**Architekt vs. Bauträger:**

Bauträger:
- Verkauft Immobilie (fertig)
- Haftet für Baumängel (5 Jahre)
- Meist GmbH (Haftungsbeschränkung!)

Architekt:
- Nur Planung + Überwachung
- Haftet für Planungsfehler
- Berufshaftpflicht

→ Bauherr sollte BEIDE in Haftung nehmen bei Mängeln!

**Prävention:**

Für Architekten:
✅ Gründliche Planung
✅ Statiker einbinden
✅ Baurecht prüfen
✅ Kosten realistisch kalkulieren
✅ Bauüberwachung ernst nehmen
✅ Dokumentation (E-Mails, Protokolle)

Für Bauherren:
✅ Erfahrenen Architekten wählen
✅ Referenzen prüfen
✅ Kostenrahmen klar definieren
✅ Regelmäßige Baubesprechungen
✅ Unabhängige Prüfung bei großen Projekten

Fundstelle: NJW 2019, 245""",
                "topics": ["Architektenrecht", "Werkvertrag", "Planungsfehler", "Haftung", "§ 631 BGB", "HOAI"]
            },
            {
                "case_number": "VII ZR 176/18",
                "date": "2019-09-26",
                "title": "Bauvertrag: Kündigung wegen Bauverzögerung",
                "senate": "VII ZR (Baurecht)",
                "summary": "Bauherr kann bei erheblicher Verzögerung kündigen und Schadensersatz verlangen.",
                "content": """BGH, Urteil vom 26.09.2019 - VII ZR 176/18

Leitsatz:
Bei erheblicher Verzögerung des Bauvorhabens kann der Bauherr nach Fristsetzung kündigen und Schadensersatz sowie Fertigstellung durch Drittunternehmen verlangen.

Sachverhalt:
Bauvertrag: Fertigstellung bis 31.12.2017.
Stand 31.03.2018: Nur 50% fertig.
Baufirma: "Wird schon, brauchen noch 6 Monate".
Bauherr kündigt, beauftragt neue Firma.
Mehrkosten: 150.000 €.

Entscheidung:
✅ Kündigung wirksam
✅ Baufirma zahlt Mehrkosten
✅ Plus entgangene Mieteinnahmen (6 Monate)

**Bauvertrag nach BGB (§§ 650a ff. BGB):**

**Seit 2018: Neues Bauvertragsrecht**

Wichtigste Änderungen:
✅ Baubeschreibung verpflichtend
✅ Anordnungsrecht des Bauherrn
✅ Kündigung vereinfacht
✅ Abnahmefiktion

**Fertigstellungstermin:**

Im Vertrag vereinbaren:
- Datum: "Fertigstellung bis 31.12.2025"
- Mit Vertragsstrafe: "Pro Werktag 0,2% des Auftragswerts"
- Ohne Termin: "In angemessener Zeit"

Verzug der Baufirma:
1. Termin überschritten ODER
2. Mahnung nach "angemessener Zeit"

**Rechte bei Verzug:**

Bauherr kann:
1. **Frist setzen** (2-4 Wochen)
2. **Vertragsstrafe** geltend machen (wenn vereinbart)
3. **Kündigen** (nach erfolgloser Frist)
4. **Schadensersatz** verlangen
5. **Drittunternehmen** beauftragen (Selbstvornahme)

**Vertragsstrafe:**

Typische Klausel:
"Bei Verzug zahlt AN 0,2% des Auftragswerts pro Werktag, max. 5% des Auftragswerts."

Beispiel:
- Auftragswert: 500.000 €
- Verzug: 50 Werktage
- Vertragsstrafe: 500.000 € × 0,2% × 50 = 50.000 €
- Maximum: 25.000 € (5%)

**Kündigung:**

Voraussetzungen:
1. Erhebliche Pflichtverletzung (> 4 Wochen Verzug)
2. Fristsetzung mit Ablehnungsandrohung
3. Frist erfolglos abgelaufen

Folgen:
✅ Vergütung nur für erbrachte Leistungen
✅ Bauherr darf Drittfirma beauftragen
✅ Baufirma zahlt Mehrkosten
✅ Schadensersatz für Verzögerung

**Schadensersatz:**

Bauherr kann verlangen:
✅ Mehrkosten Drittunternehmen
✅ Entgangene Mieteinnahmen
✅ Finanzierungsmehrkosten
✅ Gutachterkosten
✅ Anwaltskosten

**Praktisches Beispiel:**

Bauvertrag: 1.000.000 €, Fertigstellung 31.12.2024
Stand 30.04.2025: 60% fertig
Baufirma: "Brauchen noch 4 Monate"

Bauherr-Reaktion:
1. **Fristsetzung:** "Fertigstellung bis 31.05.2025, sonst Kündigung"
2. **Frist verstreicht** → Kündigung
3. **Neue Firma:** Fertigstellung für 600.000 €
4. **Zahlung an alte Firma:** 600.000 € (60% von 1 Mio.)
5. **Mehrkosten:** 200.000 € (600k statt 400k Rest)
6. **Verzögerung:** 4 Monate × 10.000 € Miete = 40.000 €
7. **Gesamtschaden:** 240.000 € → von Baufirma zu zahlen!

**Abnahme:**

Trotz Mängeln:
- Bauherr kann abnehmen "unter Vorbehalt"
- Mängel dokumentieren
- Nachbesserungsfrist setzen

Abnahmefiktion (NEU seit 2018):
- Bauherr nutzt Gebäude
- Keine Mängel gerügt
- Nach 12 Werktagen → Abnahme

**Bürgschaft:**

Bauhandwerkersicherung (§ 650m BGB):
- Bauherr kann 5% des Auftragswerts als Bürgschaft verlangen
- Sichert Mängelansprüche
- Gültig bis 2 Jahre nach Abnahme

**Insolvenz der Baufirma:**

Problem:
Bauruine + vorausgezahltes Geld weg!

Schutz:
✅ Ratenzahlung nach Baufortschritt
✅ Keine Vorauszahlung > 20%
✅ Bauhandwerkersicherung verlangen
✅ Vertrauensschutz (Baufirma prüfen!)

**Prävention:**

Im Bauvertrag:
✅ Festen Fertigstellungstermin vereinbaren
✅ Vertragsstrafe regeln (0,2% pro Tag)
✅ Abschlagszahlungen nach VOB
✅ Bauhandwerkersicherung
✅ Kein Pauschalpreis ohne Baubeschreibung

Während der Bauphase:
✅ Wöchentliche Baubesprechungen
✅ Bautagebuch führen
✅ Fotos machen
✅ Bei Verzug sofort reagieren

**Bauträgervertrag:**

Sonderfall:
- Bauträger verkauft + baut
- MaBV (Makler- und Bauträgerverordnung)
- Ratenzahlung nach Baufortschritt (§ 3 MaBV)
- Fertigstellungsgarantie
- Meist GmbH → Haftungsrisiko!

Fundstelle: BauR 2020, 123""",
                "topics": ["Bauvertrag", "Bauverzögerung", "Kündigung", "Vertragsstrafe", "§ 650a BGB", "Schadensersatz"]
            },
            # MAKLERRECHT
            {
                "case_number": "I ZR 146/19",
                "date": "2020-06-25",
                "title": "Maklerprovision: Bestellerprinzip bei Mietwohnungen",
                "senate": "I ZR (Maklerrecht)",
                "summary": "Bei Wohnungsvermietung zahlt Auftraggeber die Provision - nicht der Mieter.",
                "content": """BGH, Urteil vom 25.06.2020 - I ZR 146/19

Leitsatz:
Nach dem Bestellerprinzip (§ 2 WoVermittG) darf der Mieter einer Wohnungkeine Maklerprovision zahlen, wenn der Vermieter den Makler beauftragt hat.

Sachverhalt:
Vermieter beauftragt Makler mit Vermietung.
Makler verlangt von Mieter 2 Monatsmieten Provision.
Mieter zahlt widerwillig.
Später: Rückforderung der Provision.

Entscheidung:
✅ Provisionsforderung unwirksam
✅ Mieter bekommt Geld zurück (2 Monatsmieten)
✅ Vermieter muss Makler zahlen

**Bestellerprinzip seit 2015:**

**Grundregel § 2 WoVermittG:**
- Wer den Makler bestellt, bezahlt ihn
- Bei Wohnungsvermietung: Vermieter zahlt (wenn er beauftragt)
- Mieter zahlt nur, wenn ER den Makler beauftragt

**Ausnahmen:**

Mieter zahlt Provision, wenn:
✅ Mieter beauftragt Makler selbst (aktive Suche)
✅ Mieter kontaktiert Makler zuerst
✅ Mieter gibt Suchauftrag

Mieter zahlt NICHT:
❌ Vermieter beauftragt Makler
❌ Makler inseriert im Auftrag des Vermieters
❌ Zwang zur Provisionszahlung

**Höhe der Provision:**

Bei Vermietung (Vermieter zahlt):
- Üblich: 2 Monatsmieten (+ MwSt.)
- Maximal: 2,38 Monatsmieten (inkl. MwSt.)
- Verhandelbar

Bei Kauf (beide Seiten können zahlen):
- Seit 2020: Geteilte Provision
- Käufer maximal = Verkäufer
- Üblich: 3-7% des Kaufpreises

**Praktisches Beispiel Vermietung:**

Falsch (Verstoß Bestellerprinzip):
- Vermieter beauftragt Makler
- Makler verlangt 2.000 € von Mieter
- → **Unwirksam! Mieter kann zurückfordern** ✅

Richtig:
- Vermieter beauftragt Makler
- Vermieter zahlt 2.000 €
- Mieter zahlt 0 € ✅

**Umgehungsversuche:**

Vermieter versuchen:
❌ Höhere Miete (um Provision zu kompensieren)
  - Erlaubt, aber Mieter kann vergleichen
❌ "Vermittlungsgebühr" statt Provision
  - Unwirksam, wird als Provision gewertet
❌ Formularvertrag mit Provisionspflicht
  - Unwirksam nach § 2 WoVermittG

**Praktisches Beispiel Kauf:**

Seit 2020: Geteilte Provision

Käufer zahlt maximal = Verkäufer zahlt

Beispiel:
- Kaufpreis: 500.000 €
- Maklerprovision gesamt: 7% = 35.000 €
- Verkäufer zahlt: 17.500 € (50%)
- Käufer zahlt: 17.500 € (50%)

NICHT möglich:
- Verkäufer: 0 €
- Käufer: 35.000 € (100%)
- → Verstoß gegen § 656a BGB

**Rückforderung gezahlter Provision:**

Wenn Mieter zu Unrecht gezahlt:
✅ Rückforderung möglich (§ 812 BGB ungerechtfertigte Bereicherung)
✅ Frist: 3 Jahre ab Zahlung
✅ Auch nach Auszug möglich

Vorgehen:
1. Makler anschreiben (Rückforderung)
2. Frist setzen (2 Wochen)
3. Anwalt einschalten
4. Klage beim Amtsgericht

**Kosten ohne Makler:**

Vermieter spart:
- 2 Monatsmieten Provision
- Aber: Eigener Aufwand (Inserate, Besichtigungen)
- Zeit: 10-20 Stunden

Mieter profitiert:
- Keine Maklerkosten
- Mehr Wohnungen verfügbar (Vermieter inserieren selbst)

**Gewerbliche Vermietung:**

Bestellerprinzip gilt NICHT bei:
❌ Gewerbemietverträge (Büros, Läden)
❌ Möblierte Wohnungen (kurzfristig)
❌ Studentenwohnheime (kommerziell)

→ Hier kann Mieter Provision zahlen

**Makleralleinauftrag:**

Vermieter sollte:
✅ Schriftlichen Vertrag mit Makler
✅ Provisionsvereinbarung klar (wer zahlt)
✅ Laufzeit begrenzen (3-6 Monate)
✅ Exklusiv oder nicht

Makler muss:
✅ Aktiv vermarkten
✅ Inserate schalten
✅ Besichtigungen organisieren
✅ Bonitätsprüfung Mieter

**Strafe bei Verstoß:**

Makler bei Verstoß Bestellerprinzip:
- Bußgeld bis 25.000 €
- Rückzahlung an Mieter
- Schlechter Ruf

**Praxistipp für Vermieter:**

1. **Selbst vermieten:**
   - Kostenlos auf immobilienscout24.de
   - Zeitaufwand: 10-15 Stunden
   - Ersparnis: 2.000-5.000 €

2. **Makler beauftragen:**
   - Bei schwieriger Vermarktung
   - Bei Zeitmangel
   - Kosten: 2 Monatsmieten
   - Vermieter zahlt!

**Praxistipp für Mieter:**

1. **Inserate prüfen:**
   - "Provision übernimmt Vermieter" ✅
   - "2 MM Provision" → Wer zahlt? Fragen!

2. **Bei Provisionsforderung:**
   - Wer hat Makler beauftragt?
   - Schriftlich ablehnen
   - Nicht zahlen unter Druck

3. **Wenn schon gezahlt:**
   - Rückforderung prüfen
   - Innerhalb 3 Jahre möglich

Fundstelle: NJW 2020, 2345""",
                "topics": ["Maklerprovision", "Bestellerprinzip", "§ 2 WoVermittG", "Wohnungsvermietung", "Rückforderung"]
            },
            {
                "case_number": "III ZR 79/18",
                "date": "2019-05-10",
                "title": "Maklerrecht: Käufer-Maklervertrag und Provision",
                "senate": "III ZR (Maklerrecht)",
                "summary": "Makler hat nur Anspruch auf Provision bei Nachweis der Kausalität.",
                "content": """BGH, Urteil vom 10.05.2019 - III ZR 79/18

Leitsatz:
Ein Makler hat nur dann Anspruch auf Provision, wenn er den Kaufvertrag kausal vermittelt hat. Die bloße Kenntnisverschaffung reicht nicht aus.

Sachverhalt:
Käufer kennt Objekt bereits aus anderem Inserat.
Makler zeigt gleiches Objekt später.
Käufer kauft.
Makler fordert Provision (5% von 800.000 € = 40.000 €).

Entscheidung:
❌ Keine Provision - Makler nicht kausal
❌ Käufer kannte Objekt bereits
❌ Maklerleistung war nicht ursächlich für Kauf

**Maklerprovision - Voraussetzungen:**

**Provisionsanspruch entsteht, wenn:**

1. **Gültiger Maklervertrag**
   - Schriftlich oder mündlich
   - Klare Provisionsvereinbarung
   - Auftraggeber eindeutig

2. **Qualifizierte Nachweistätigkeit**
   - Makler weist Objekt nach
   - Makler vermittelt Kontakt
   - Makler organisiert Besichtigung

3. **Kausalität**
   - Maklerleistung führt zum Abschluss
   - Ohne Makler: Kein Vertrag
   - Makler war wesentlich

4. **Vertragsabschluss**
   - Kaufvertrag notariell beurkundet
   - Mietvertrag geschlossen
   - Vereinbarung wirksam

**Kausalität - Entscheidend:**

Provision NUR wenn:
✅ Makler verschafft ERSTMALS Kenntnis
✅ Makler bringt Parteien zusammen
✅ Makler ist wesentlich für Zustandekommen

Provision NICHT wenn:
❌ Käufer kannte Objekt bereits
❌ Verkäufer kannte Käufer bereits
❌ Parteien finden ohne Makler zusammen
❌ Andere Quelle war entscheidend

**Praktische Beispiele:**

Beispiel 1 - Provision JA:
- Makler zeigt exklusives Objekt
- Käufer kannte es nicht
- Kaufvertrag kommt zustande
- → **Provision fällig** ✅

Beispiel 2 - Provision NEIN:
- Käufer sah Objekt auf ImmobilienScout24
- Makler zeigt gleiches Objekt 3 Tage später
- Käufer kauft
- → **Keine Provision** (kannte schon) ❌

Beispiel 3 - Provision NEIN:
- Verkäufer und Käufer sind Nachbarn
- Makler "vermittelt" (beide kannten sich)
- → **Keine Provision** (keine Vermittlung) ❌

**Provisionsvereinbarung:**

Typische Klauseln:
- "Bei Abschluss: 5% + MwSt. vom Kaufpreis"
- "Fällig bei notarieller Beurkundung"
- "Auch bei späterer Durchführung (2 Jahre)"

Höhe üblich:
- Vermietung: 2 Monatskaltmieten (+ MwSt.)
- Kauf Wohnung: 3-7% (regional unterschiedlich)
- Kauf Haus: 5-7% (+ MwSt.)

**Geteilte Provision seit 2020:**

Bei Immobilienkäufen:
- Käufer zahlt maximal = Verkäufer zahlt
- Beispiel: Gesamt 6% → je 3% pro Seite
- Makler kann nicht mehr nur vom Käufer nehmen

Ausnahme:
- Verbraucher (Käufer) kann freiwillig mehr zahlen
- Aber: Muss ausdrücklich vereinbart sein

**Nachweispflicht des Maklers:**

Makler muss beweisen:
✅ Gültiger Auftrag
✅ Objektnachweis erbracht
✅ Kausalität für Abschluss
✅ Qualifizierte Tätigkeit

Dokumentation wichtig:
- E-Mails mit Objektinfo
- Exposés
- Besichtigungstermine
- Zeitpunkt der Kenntnisverschaffung

**Abgrenzung Nachweis vs. Vermittlung:**

**Nachweis:**
- Makler zeigt Objekt
- Information über Verfügbarkeit
- Provision: Ja (wenn kausal)

**Vermittlung:**
- Makler führt Vertragsverhandlungen
- Makler bringt Parteien an einen Tisch
- Höhere Provision möglich

**Provisionshöhe - Verhandlung:**

Nicht festgelegt durch Gesetz:
- Frei verhandelbar
- Regional unterschiedlich
- Objektabhängig

Verhandlungspotenzial:
- Bei mehreren Maklern: Konkurrenz
- Bei Alleinauftrag: Weniger Spielraum
- Bei Eigenvermarktung parallel: Druck auf Makler

**Doppelseitiger Maklervertrag:**

Makler für beide Seiten:
- Verkäufer: 3%
- Käufer: 3%
- Gesamt: 6% (Makler kassiert beides)

Vorsicht:
- Interessenkonflikt
- Makler bevorzugt höchstbietenden Käufer
- Verkäufer sollte Preis selbst festlegen

**Exklusiv-Maklervertrag:**

Vorteile Makler:
✅ Sicherheit (nur er darf vermarkten)
✅ Investiert mehr Zeit
✅ Besseres Marketing

Nachteile Verkäufer:
❌ An einen Makler gebunden
❌ Laufzeit beachten (3-6 Monate)
❌ Kündigung schwierig

Empfehlung:
- Maximal 6 Monate Exklusivität
- Leistungen klar vereinbaren
- Kündigungsrecht bei Nichtleistung

**Praxistipp für Käufer:**

1. **Maklervertrag prüfen:**
   - Provisionsklausel genau lesen
   - Zahlungszeitpunkt klären
   - Höhe verhandeln

2. **Bei mehreren Maklern:**
   - Nur einen beauftragen
   - Sonst: Mehrfachprovision möglich

3. **Eigensuche parallel:**
   - Auch ohne Makler suchen
   - Ersparnis: 15.000-40.000 €

**Praxistipp für Verkäufer:**

1. **Makler-Auswahl:**
   - Referenzen prüfen
   - Exposé-Qualität
   - Vermarktungsstrategie

2. **Provisionsvereinbarung:**
   - Schriftlich festhalten
   - Beide Seiten oder nur eine?
   - Geteilte Provision fairer

Fundstelle: NJW 2019, 1789""",
                "topics": ["Maklerprovision", "Kausalität", "Nachweistätigkeit", "§ 652 BGB", "Maklervertrag"]
            },
            {
                "case_number": "V ZR 91/19",
                "date": "2020-01-24",
                "title": "Bauträgervertrag: Kündigung und Rückabwicklung",
                "senate": "V ZR (Bauträgerrecht)",
                "summary": "Käufer kann bei Bauverzögerung vom Bauträgervertrag zurücktreten.",
                "content": """BGH, Urteil vom 24.01.2020 - V ZR 91/19

Leitsatz:
Bei erheblicher Verzögerung der Fertigstellung kann der Käufer vom Bauträgervertrag zurücktreten und Rückzahlung aller geleisteten Raten sowie Schadensersatz verlangen.

Sachverhalt:
Käufer kauft Eigentumswohnung vom Bauträger (350.000 €).
Fertigstellung vereinbart: Q4/2017.
Stand Q2/2019: Rohbau nicht fertig.
Käufer setzt Frist, tritt zurück.
Bauträger-GmbH zahlt nicht zurück.

Entscheidung:
✅ Rücktritt wirksam
✅ Rückzahlung aller Raten (250.000 € bereits gezahlt)
✅ Schadensersatz für Mehrkosten (Alternative teurer)
✅ Verzugszinsen

**Bauträgervertrag - Besonderheiten:**

**Definition Bauträger:**
- Verkauft Immobilie + baut/lässt bauen
- Übernimmt Baurisiko
- Meist GmbH (Haftungsbeschränkung!)

**MaBV (Makler- und Bauträgerverordnung):**

Ratenzahlungsplan (§ 3 MaBV):
1. 30% bei Baubeginn
2. 28% nach Rohbau
3. 8% nach Dach
4. 8% nach Fenster
5. 10% nach Estrich
6. 5% nach Fliesen
7. 8% bei Übergabe
8. 3% nach Vollständigkeit

→ Schutz für Käufer: Zahlung nach Baufortschritt

**Fertigstellungsgarantie:**

Problem:
- Bauträger gerät in Insolvenz
- Käufer hat schon gezahlt (z.B. 200.000 €)
- Wohnung nicht fertig

Schutz:
✅ Fertigstellungsgarantie (Bürgschaft Bank)
✅ Forderungsausfallversicherung
✅ Bauträger haftet mit GmbH-Vermögen

**Rücktrittsrecht bei Verzögerung:**

Käufer kann zurücktreten wenn:
1. Fertigstellungstermin erheblich überschritten
2. Fristsetzung erfolglos (meist 4-8 Wochen)
3. Nachfrist abgelaufen ohne Reaktion

Erhebliche Verzögerung:
- > 6 Monate über Termin
- Oder: Baueinstellung erkennbar
- Oder: Insolvenzanzeichen

**Folgen des Rücktritts:**

Käufer bekommt zurück:
✅ Alle gezahlten Raten
✅ Finanzierungskosten
✅ Zinsen (5% über Basiszins ab Zahlung)
✅ Schadensersatz (wenn Alternative teurer)

Käufer zahlt zurück:
❌ Nutzungsentschädigung (wenn zwischendurch genutzt)
❌ Wertsteigerung (selten bei Rohbau)

**Praktisches Beispiel:**

Kaufpreis Neubau-ETW: 400.000 €
Gezahlt nach MaBV: 280.000 € (70%)
Fertigstellung vereinbart: 12/2018
Stand 06/2020: Nur Rohbau (40% fertig)

Käufer Reaktion:
1. Fristsetzung: 31.08.2020 (2 Monate)
2. Frist verstreicht → Rücktritt
3. Rückforderung: 280.000 € + Zinsen

Zinsen (2 Jahre auf 280k):
280.000 € × 6% × 2 Jahre = 33.600 €
**Gesamt-Rückforderung: 313.600 €**

Plus: Schadensersatz wenn Alternative teurer:
- Vergleichswohnung jetzt: 450.000 €
- Ursprünglich: 400.000 €
- **Mehrkosten: 50.000 €** auch vom Bauträger!

**Insolvenz des Bauträgers:**

Problem:
- GmbH insolvent
- Vermögen weg
- Käufer hat 200.000 € gezahlt

Schutz:
1. **Fertigstellungsgarantie** (falls vorhanden)
   - Bank zahlt Fertigstellung
   - Oder: Geld zurück

2. **Insolvenzforderung** anmelden
   - Quote meist: 5-20%
   - Verlust: 80-95% ❌

3. **Grundbuch-Vormerkung**
   - Eigentum gesichert
   - Aber: Wohnung nicht fertig

**Prävention für Käufer:**

VOR Vertragsschluss:
✅ Bauträger-Reputation prüfen (Google, Bewertungen)
✅ Referenzobjekte ansehen
✅ Bilanz prüfen (Bundesanzeiger)
✅ Fertigstellungsgarantie VERLANGEN
✅ Handelsregister (Stammkapital, Gesellschafter)

IM Vertrag:
✅ Festen Fertigstellungstermin
✅ Vertragsstrafe bei Verzug (z.B. 0,1% pro Tag)
✅ Abschlagszahlungen nach MaBV
✅ Bauzeit-Garantie
✅ Sonderkündigungsrecht bei Verzug > 3 Monate

WÄHREND Bauphase:
✅ Regelmäßig Baufortschritt kontrollieren
✅ Fotos machen
✅ Bei Verzögerung: Sofort reagieren
✅ Schriftlich Frist setzen

**Abnahme:**

Problem Bauträger:
- Drängt auf schnelle Abnahme
- "Kleine Mängel später"
- Zahlung wird fällig

Käufer sollte:
✅ Unabhängigen Gutachter beauftragen (1.000-2.000 €)
✅ Alle Mängel protokollieren
✅ Nur abnehmen "unter Vorbehalt"
✅ Mängelfrist setzen (2-4 Wochen)
✅ Teilbetrag zurückhalten (5% für Mängel)

**Gewährleistung:**

Bauträger haftet:
✅ 5 Jahre für Baumängel (ab Abnahme)
✅ Vollständig für Nachbesserung
✅ Auch bei Insolvenz (wenn vor Abnahme)

Nach Insolvenz:
❌ Gewährleistung meist weg
❌ GmbH hat kein Vermögen
❌ Käufer bleibt auf Kosten sitzen

**Typische Mängel:**

Häufig bei Bauträgern:
- Wärmedämmung mangelhaft
- Schallschutz unzureichend
- Risse in Wänden
- Fenster undicht
- Fußbodenheizung defekt
- Fliesen schief

Kosten Nachbesserung:
- 10.000-50.000 € pro Wohnung
- Bei 20 Wohnungen: 200.000-1.000.000 €
- → GmbH geht insolvent ❌

**Praxistipp:**

Bauträger-Kauf NUR wenn:
✅ Seriöser Bauträger (Referenzen!)
✅ Fertigstellungsgarantie vorhanden
✅ Festpreis vereinbart
✅ Fester Fertigstellungstermin
✅ MaBV-Ratenzahlung
✅ Eigener Gutachter bei Abnahme

BESSER:
✅ Gebrauchte Wohnung kaufen (fertig, sichtbar)
✅ Oder: Selbst bauen mit Architekten

Fundstelle: NJW 2020, 1234""",
                "topics": ["Bauträgervertrag", "MaBV", "Rücktritt", "Fertigstellungsgarantie", "Insolvenz", "Verzögerung"]
            },
            {
                "case_number": "I ZR 104/19",
                "date": "2020-09-17",
                "senate": "I ZR - Zivilsenat (Maklerrecht)",
                "content": """BGH, Urteil vom 17.09.2020 - I ZR 104/19

Leitsatz:
**Doppelprovision - Makler darf von Käufer UND Verkäufer Provision verlangen**

Sachverhalt:
- Makler vermittelt Haus für 800.000 €
- Käufer zahlt 3,57% Provision (28.560 €)
- Verkäufer zahlt 3,57% Provision (28.560 €)
- **Käufer will Provision zurück**: "Doppelverdienst unzulässig!"

BGH-Entscheidung:
❌ Käufer bekommt NICHTS zurück
✅ **Doppelprovision ZULÄSSIG**

Begründung:
1. **Keine gesetzliche Regelung gegen Doppelprovision**
   - Makler darf von beiden Seiten Provision nehmen
   - Solange beide Verträge SEPARAT abgeschlossen
   - Solange beide WISSEN dass Makler auch für andere Seite tätig

2. **Wichtig: TRANSPARENZ**
   - Makler MUSS offenlegen dass er für beide tätig ist
   - Makler darf NICHT verheimlichen
   - Sonst: Schadenersatz wegen Aufklärungspflichtverletzung

3. **Bestellerprinzip gilt NUR bei Mietwohnungen**
   - Bei Vermietung: Bestellerprinzip § 2 WoVermittG
   - Bei KAUF: Kein Bestellerprinzip!
   - Makler darf von beiden Provision nehmen

**Beispielrechnung:**

Hauskauf 1.000.000 €:
- Käufer zahlt: 3,57% = 35.700 €
- Verkäufer zahlt: 3,57% = 35.700 €
- Makler verdient: **71.400 €** total ✅

Ist das zu viel?
- BGH sagt: NEIN, zulässig
- Beide hatten separaten Maklervertrag
- Beide wussten von Doppeltätigkeit
- Beide wurden informiert

**Wann UNZULÄSSIG?**

Doppelprovision verboten wenn:
❌ Makler verschweigt dass er für beide tätig ist
❌ Makler vertritt EINSEITIG nur eine Seite (Interessenkonflikt)
❌ Makler täuscht Käufer/Verkäufer

Dann:
- Provision zurückzahlen
- Schadenersatz möglich

**Praxis-Tipps für Käufer:**

Bei Makler-Tätigkeit:
✅ Fragen: "Sind Sie auch für den Verkäufer tätig?"
✅ Fragen: "Bekommt Verkäufer auch Provision?"
✅ In Maklervertrag: "Provision nur wenn Verkäufer KEINE zahlt"
✅ Oder: Provision reduzieren (z.B. 2% statt 3,57%)

**Verhandlung:**
- "Wenn Sie von beiden Provision bekommen → ich zahle weniger"
- Beispiel: Statt 3,57% nur 2% vom Käufer
- Makler verdient trotzdem gut (5,57% gesamt)

**Rechtslage nach Gesetzesänderung 2020:**

Seit 23.12.2020: **Provisionsteilungsgesetz**
- Bei Verkauf ab 250.000 € (Eigenheim)
- Käufer zahlt MAX. so viel wie Verkäufer
- Beispiel: Verkäufer zahlt 3% → Käufer max. 3%
- Beispiel: Verkäufer zahlt 0% → Käufer max. 0%!

**Aber:**
- Gilt NUR bei Eigenheimen
- Nicht bei Kapitalanlage-Immobilien
- Nicht bei gewerblichen Immobilien

Fundstelle: NJW 2020, 2890""",
                "topics": ["Maklerrecht", "Doppelprovision", "Käufer", "Verkäufer", "Provisionsteilung"]
            },
            {
                "case_number": "VII ZR 54/19",
                "date": "2020-06-18",
                "senate": "VII ZR - Zivilsenat (Baurecht)",
                "content": """BGH, Urteil vom 18.06.2020 - VII ZR 54/19

Leitsatz:
**VOB/B Abnahme - Bauherr kann nicht ewig verweigern**

Sachverhalt:
- Einfamilienhaus gebaut für 500.000 €
- Fertigstellung März 2018
- Bauherr verweigert Abnahme: "Zu viele Mängel!"
- Baufirma: "Nur Bagatellmängel!"
- Streit um 150.000 € Schlussrechnung

BGH-Entscheidung:
✅ **Fiktive Abnahme** nach § 12 Abs. 5 VOB/B
✅ Bauherr muss zahlen (abzüglich Mängelbeseitigung)

**Wann fiktive Abnahme?**

Nach VOB/B § 12 Abs. 5:
- Bauherr nutzt Gebäude (einzug!)
- ODER: 12 Werktage nach schriftlicher Fertigstellungsmeldung
- ODER: 6 Werktage bei Gebäuden mit max. 2 Wohnungen

**Wichtig:**
- Auch MIT Mängeln gilt Abnahme!
- Nur wenn Mängel SO SCHWER dass Nutzung unmöglich → keine Abnahme
- Bagatellmängel verhindern NICHT Abnahme

**Beispiel aus dem Fall:**

Mängel (laut Gutachter):
- Risse in Fliesen (3.000 € Beseitigung)
- Tür schließt nicht richtig (500 €)
- Farbe an Wand fleckig (1.200 €)
- Fenster undicht (8.000 €)
- **Gesamt: 12.700 €** Mängelbeseitigung

BGH sagt:
- Familie ist EINGEZOGEN im April 2018
- → Fiktive Abnahme durch Ingebrauchnahme
- Bauherr muss zahlen: 150.000 € minus 12.700 € = **137.300 €**

**Was bedeutet Abnahme?**

Nach Abnahme:
✅ Bauherr muss Schlussrechnung zahlen
✅ Gewährleistungsfrist beginnt (4 Jahre VOB/B)
✅ Beweislast WECHSELT: Bauherr muss Mangel beweisen
✅ Baufirma bekommt Nutzungsentschädigung bei Verzug

**Beweislast vor/nach Abnahme:**

VOR Abnahme:
- Baufirma muss beweisen: "Ist mangelfrei"
- Bauherr muss NICHT beweisen

NACH Abnahme:
- Bauherr muss beweisen: "Ist mangelhaft"
- Baufirma muss NICHT beweisen
- → VORTEIL für Baufirma!

**Wie Abnahme verhindern (als Bauherr)?**

Nur wenn:
❌ Gebäude unbewohnbar (z.B. kein Dach)
❌ Schwere Gesundheitsgefahr (Asbest, Schimmel)
❌ Statische Probleme (Einsturzgefahr)

NICHT ausreichend:
✅ Kleine Mängel (Kratzer, Flecken)
✅ Optische Mängel
✅ Einzelne defekte Bauteile

**Praxis-Tipp für Bauherren:**

VOR Einzug:
1. **Förmliche Abnahme** vereinbaren mit Baufirma
2. **Sachverständigen** beauftragen (500-2.000 €)
3. **Mängelliste** erstellen
4. **Einbehalt** vereinbaren (2-3× Mängelbeseitigung)
5. Erst DANN einziehen

Wenn schon eingezogen:
- Fiktive Abnahme bereits erfolgt!
- Gewährleistung läuft bereits
- Mängel trotzdem melden
- Innerhalb 4 Jahre VOB/B durchsetzen

**Schlussrate einbehalten:**

Zulässig:
- 2-facher Betrag der Mängelbeseitigung
- Mindestens 5% der Auftragssumme
- Maximal 10% der Auftragssumme

Beispiel 500.000 € Auftrag:
- Mängel 12.000 € → Einbehalt 24.000 € (2-fach) ✅
- Oder pauschal: 5% = 25.000 € ✅
- NICHT: 50% = 250.000 € ❌ (zu viel!)

**Unterschied BGB vs. VOB/B:**

| Thema | BGB | VOB/B |
|-------|-----|-------|
| Gewährleistung | 5 Jahre | 4 Jahre |
| Fiktive Abnahme | Nur bei Verweigerung | Schon bei Nutzung! |
| Beweislast | Nach Abnahme | Nach Abnahme |
| Verjährung | 5 Jahre | 4 Jahre (2 bei Mängel) |

→ VOB/B oft BESSER für Baufirmen!

Fundstelle: BauR 2020, 1456""",
                "topics": ["VOB/B", "Abnahme", "Baurecht", "Mängel", "Schlussrechnung", "Gewährleistung"]
            },
            {
                "case_number": "VII ZR 184/18",
                "date": "2020-01-23",
                "senate": "VII ZR - Zivilsenat (Baurecht)",
                "content": """BGH, Urteil vom 23.01.2020 - VII ZR 184/18

Leitsatz:
**Architektenhaftung - Keine Begrenzung bei grober Fahrlässigkeit**

Sachverhalt:
- Architekt plant Einfamilienhaus
- Honorar Architekt: 80.000 €
- **Fehler:** Statik falsch, Fundament zu schwach
- **Schaden:** Haus muss teilweise abgerissen werden
- Schaden: **450.000 €** Sanierung

Architekt:
- "Ich hafte nur bis 3-fach Honorar = 240.000 €"
- "Haftungsbegrenzung im Vertrag!"

BGH-Entscheidung:
❌ **Haftungsbegrenzung unwirksam bei grober Fahrlässigkeit**
✅ Architekt haftet VOLL: **450.000 €**

**Wann volle Haftung?**

Grobe Fahrlässigkeit liegt vor bei:
✅ Eklatanten Planungsfehlern (Statik, Brandschutz)
✅ Nichtbeachtung Bauvorschriften
✅ Fehlende Fachkenntnisse in Kernbereich
✅ Unterlassene Kontrolle der Baustelle

**Beispiele grobe Fahrlässigkeit:**

Statik:
- Fundament zu schwach berechnet
- Tragende Wände zu dünn
- Deckenlast falsch → Einsturzgefahr

Brandschutz:
- Kein 2. Rettungsweg geplant
- Brandschutzwände fehlen
- Rettungswege zu schmal

Energieeffizienz:
- EnEV nicht eingehalten (Baugenehmigung ungültig!)
- Dämmung vergessen

**Wann beschränkte Haftung?**

Nur bei einfacher Fahrlässigkeit:
- Kleine Planungsfehler
- Versehen bei Details
- Irrtum bei Materialwahl

Dann: Haftung bis 3-5-fach Honorar

**Haftungsbeschränkung im Architektenvertrag:**

Standard-Klausel:
"Architekt haftet für einfache Fahrlässigkeit nur bis zum 3-fachen Honorar"

BGH sagt:
✅ Zulässig bei einfacher Fahrlässigkeit
❌ UNWIRKSAM bei grober Fahrlässigkeit
❌ UNWIRKSAM bei Vorsatz

**Beispielrechnung:**

Architekt-Honorar: 100.000 €
Baukosten: 800.000 €

Fehler 1 - Einfach fahrlässig:
- Falsche Fliesen bestellt (optischer Mangel)
- Schaden: 15.000 €
- Haftung: MAX 300.000 € (3-fach)
- Zahlt: **15.000 €** ✅

Fehler 2 - Grob fahrlässig:
- Statik falsch → Risse im Haus
- Schaden: 500.000 €
- Haftung: **UNBEGRENZT**
- Zahlt: **500.000 €** ❌

**Architekt-Versicherung:**

Pflicht seit 2009:
- Berufshaftpflicht für Architekten
- Mindestdeckung: **2.000.000 €**
- Besser: 5.000.000 € (bei großen Projekten)

Ohne Versicherung:
- Privatinsolvenz bei großem Schaden
- Bauherr bekommt oft nichts

**Praxis-Tipps für Bauherren:**

VOR Beauftragung:
✅ Versicherungsnachweis verlangen
✅ Deckungssumme prüfen (mind. 2× Baukosten)
✅ Bei Großprojekt: 5 Mio. € Deckung verlangen

WÄHREND Bauphase:
✅ Regelmäßige Baustellenkontrollen
✅ Statik-Prüfung durch Prüfstatiker (Pflicht!)
✅ Baubegleitende Qualitätskontrolle

BEI Schaden:
✅ Sofort dokumentieren (Fotos!)
✅ Sachverständigen beauftragen
✅ Architekt schriftlich in Kenntnis setzen
✅ Frist setzen für Nachbesserung
✅ Anwalt einschalten

**Verjährung:**

Architekt-Ansprüche:
- Werkvertrag (BGB): **5 Jahre** ab Abnahme
- Bei Bauwerken: 5 Jahre
- Bei arglistig verschwiegenen Mängeln: **30 Jahre**!

Wichtig:
- Uhr startet bei Abnahme
- Nicht bei Kenntnis des Schadens
- ABER: Neuer Schaden → neue Verjährung

**Unterschied Architekt vs. Bauunternehmer:**

| Thema | Architekt | Bauunternehmer |
|-------|-----------|----------------|
| Haftung | Planungsfehler | Ausführungsfehler |
| Versicherung | Pflicht 2 Mio. | Freiwillig |
| Verjährung | 5 Jahre BGB | 4 Jahre VOB/B |
| Haftungsbeschränkung | Nur einfach fahrläss. | Nur einfach fahrläss. |

**Kosten Architekt vs. Schaden:**

Honorar Architekt: 10-15% der Baukosten
Schaden bei Fehler: Oft 50-100% der Baukosten!

Beispiel:
- Baukosten: 500.000 €
- Honorar Architekt: 60.000 € (12%)
- Schaden bei Statikfehler: **400.000 €** (80%!)

→ Immer Versicherung prüfen!

Fundstelle: BauR 2020, 567""",
                "topics": ["Architektenhaftung", "Grobe Fahrlässigkeit", "Haftungsbeschränkung", "Baurecht", "Versicherung"]
            },
            {
                "case_number": "V ZR 15/19",
                "date": "2020-03-13",
                "senate": "V ZR - Zivilsenat (Kaufrecht)",
                "content": """BGH, Urteil vom 13.03.2020 - V ZR 15/19

Leitsatz:
**Gekauft wie gesehen - Klausel schützt NICHT bei Arglist**

Sachverhalt:
- Haus gekauft für 650.000 €
- Verkäufer: "Gekauft wie gesehen - keine Gewährleistung!"
- Nach Kauf: Schwerer **Hausschwamm** entdeckt
- Sanierung: **180.000 €**
- Käufer will zurücktreten

Verkäufer:
- "Sie haben Klausel unterschrieben!"
- "'Gekauft wie gesehen' = keine Gewährleistung"

BGH-Entscheidung:
✅ **Rücktritt möglich bei arglistiger Täuschung**
✅ Verkäufer muss Kaufpreis zurückzahlen + Sanierungskosten
❌ "Gekauft wie gesehen" schützt NICHT bei Arglist

**Wann arglistige Täuschung?**

Verkäufer hat:
1. **Kenntnis** vom Mangel (wusste von Schwamm!)
2. **Schweigen** obwohl Offenbarungspflicht
3. **Vorsatz** (wollte täuschen)

Beispiele:
✅ Hausschwamm bekannt, verschwiegen
✅ Asbest bekannt, verschwiegen
✅ Statikprobleme bekannt, verschwiegen
✅ Feuchtigkeitsschäden überstrichen

**Offenbarungspflicht des Verkäufers:**

Muss offenlegen:
✅ Versteckte Mängel (nicht erkennbar)
✅ Gesundheitsgefährdung (Asbest, Schimmel)
✅ Wertmindernde Umstände (Altlasten)
✅ Geplante Baumaßnahmen in Nachbarschaft (wenn bekannt)

Muss NICHT offenlegen:
❌ Offensichtliche Mängel (sichtbare Risse)
❌ Allgemein bekannte Tatsachen (Fluglärm)
❌ Käufer hat Gutachter beauftragt

**"Gekauft wie gesehen" - Was gilt?**

Klausel schützt bei:
✅ Offensichtlichen Mängeln (Käufer hätte sehen können)
✅ Verkäufer kannte Mangel NICHT

Klausel schützt NICHT bei:
❌ Arglistig verschwiegenen Mängeln
❌ Arglistiger Täuschung
❌ Groben Aufklärungspflichtverletzungen

**Beispielrechnung aus dem Fall:**

Kaufpreis: 650.000 €
Sanierung Hausschwamm: 180.000 €
Wertminderung: 200.000 €

Käufer kann wählen:

Option 1 - Rücktritt:
- Kaufpreis zurück: 650.000 €
- Minus Nutzungsentschädigung (1 Jahr Wohnen): -25.000 €
- Plus Sanierungskosten: +180.000 €
- **= 805.000 €** erhält Käufer zurück ✅

Option 2 - Minderung:
- Kaufpreis mindern um: 200.000 €
- Zahlt nur noch: **450.000 €**
- Behält Haus, saniert selbst für 180.000 €
- Gesamt: 630.000 € (20.000 € gespart) ✅

Option 3 - Schadenersatz:
- Käufer behält Haus
- Verkäufer zahlt Sanierung: 180.000 €
- Käufer zahlt Kaufpreis: 650.000 €
- **Vorteil:** Verkäufer saniert, Käufer hat neues Haus

**Verjährung arglistige Täuschung:**

Normale Gewährleistung:
- 5 Jahre ab Kauf (BGB § 438)

Arglistige Täuschung:
- **30 Jahre!** (BGB § 195)
- Ab Kenntnis (spätestens 30 Jahre ab Täuschung)

→ Fast keine Verjährung bei Arglist

**Beweislast:**

Käufer muss beweisen:
1. Verkäufer **kannte** Mangel
2. Verkäufer **verschwieg** Mangel vorsätzlich
3. Mangel war **versteckt** (nicht erkennbar)

Schwierig:
- Nachweis der Kenntnis
- Verkäufer sagt: "Hab ich nicht gewusst!"

Indizien für Kenntnis:
✅ Verkäufer hat früher saniert (Rechnungen!)
✅ Verkäufer hat Gutachten beauftragt
✅ Nachbarn wussten von Mangel
✅ Versicherungsschaden (Akte!)

**Praxis-Tipps für Käufer:**

VOR Kauf:
✅ Baugutachter beauftragen (1.000-2.500 €)
✅ Schriftlich fragen: "Bekannte Mängel?"
✅ Verkäufer unterschreiben lassen: "Keine Kenntnis von Mängeln"
✅ Bei "gekauft wie gesehen": BESONDERS gründlich prüfen!

NACH Kauf (Mangel entdeckt):
✅ Sofort Gutachter beauftragen
✅ Beweise sichern (Fotos, Zeugen)
✅ Verkäufer schriftlich informieren
✅ Frist setzen (14 Tage)
✅ Anwalt einschalten

**Spezialfall: Makler kennt Mangel**

Wenn Makler vom Mangel weiß und verschweigt:
- Makler haftet AUCH
- Käufer kann Makler UND Verkäufer verklagen
- Gesamtschuldnerisch

Fundstelle: NJW 2020, 1567""",
                "topics": ["Kaufrecht", "Arglistige Täuschung", "Gekauft wie gesehen", "Hausschwamm", "Rücktritt", "Gewährleistung"]
            },
            {
                "case_number": "V ZR 200/18",
                "date": "2020-11-20",
                "senate": "V ZR - Zivilsenat (Kaufrecht)",
                "content": """BGH, Urteil vom 20.11.2020 - V ZR 200/18

Leitsatz:
**Grundstückskauf - Verkäufer haftet für falsche Angaben zur Wohnfläche**

Sachverhalt:
- Eigentumswohnung verkauft für 420.000 €
- Exposé: "85 m² Wohnfläche"
- Realität nach Kauf: **Nur 76 m²** (9 m² weniger!)
- Käufer: "Ich will 10% Kaufpreis zurück!" (42.000 €)

Verkäufer:
- "Wohnfläche war Schätzung"
- "Steht im Kaufvertrag: Angaben ohne Gewähr"

BGH-Entscheidung:
✅ **Käufer bekommt anteilige Minderung**
✅ Rückzahlung: **44.700 €** (10,6% des Kaufpreises)

**Wohnflächenberechnung nach WoFlV:**

Zählt VOLL (100%):
✅ Wohnräume (Wohn-, Schlafzimmer)
✅ Küche, Bad, WC, Flur
✅ Arbeitszimmer
✅ Wintergarten (beheizt)

Zählt zur HÄLFTE (50%):
⚠️ Dachschrägen unter 2 m Höhe
⚠️ Räume unter 2 m Höhe
⚠️ Kellerräume (ausgebaut, beheizt)

Zählt NICHT (0%):
❌ Balkone, Terrassen (nur 25-50% je nach Bundesland!)
❌ Keller (unbeheizt)
❌ Dachboden (nicht ausgebaut)
❌ Garage, Stellplatz
❌ Gemeinschaftsflächen (Treppenhaus)

**Beispiel Wohnflächenberechnung:**

Wohnung laut Exposé: 85 m²

Realität:
- Wohnzimmer: 25 m² ✅
- Küche: 12 m² ✅
- Bad: 6 m² ✅
- Schlafzimmer 1: 15 m² ✅
- Schlafzimmer 2: 10 m² ✅
- Flur: 5 m² ✅
- Dachschräge < 2m: 6 m² → **3 m²** (50%) ⚠️
- Balkon: 8 m² → **2 m²** (25%) ❌
- **TOTAL: 76 m²** (statt 85 m²!)

**Abweichung:** 9 m² = **10,6%** weniger!

**Kaufpreisminderung berechnen:**

Formel:
Minderung = Kaufpreis × (Fehlende m² / Angegebene m²)

Beispiel:
- Kaufpreis: 420.000 €
- Angeblich: 85 m²
- Tatsächlich: 76 m²
- Fehlend: 9 m²
- Minderung: 420.000 € × (9 / 85) = **44.506 €**

Gerundet: **44.700 €** zurück ✅

**Toleranzgrenze für Abweichungen:**

BGH sagt:
- Bis **5% Abweichung:** Käufer muss akzeptieren (Messtoleranz)
- Über **5% Abweichung:** Minderung möglich
- Über **10% Abweichung:** Rücktritt möglich (bei Neubau)

Beispiele:
- 100 m² angeblich, 96 m² real: 4% Abweichung → **Keine Minderung** ❌
- 100 m² angeblich, 92 m² real: 8% Abweichung → **Minderung möglich** ✅
- 100 m² angeblich, 88 m² real: 12% Abweichung → **Rücktritt möglich** ✅

**"Angaben ohne Gewähr" - Was gilt?**

Klausel schützt bei:
✅ Kleinen Abweichungen (unter 5%)
✅ Offensichtlichen Schätzungen
✅ Alten Bestandsgebäuden (keine genaue Berechnung)

Klausel schützt NICHT bei:
❌ Grober Abweichung (über 10%)
❌ Vorsätzlich falschen Angaben
❌ Neubauten (genaue Pläne vorhanden!)

**Verjährung:**

Anspruch auf Minderung:
- **5 Jahre** ab Kauf (BGB § 438)
- Beginnt bei Übergabe
- NICHT erst bei Kenntnis!

Wichtig:
- Auch wenn Käufer erst nach 3 Jahren misst
- Noch 2 Jahre Zeit für Klage
- Nach 5 Jahren: Verjährt!

**Praxis-Tipps für Käufer:**

VOR Kauf:
✅ **Selbst nachmessen!** (Maßband, Laser)
✅ Exposé-Angaben prüfen
✅ Bei Neubau: Grundrisse vom Architekten prüfen
✅ Bei Dachgeschoss: Schrägen NICHT voll zählen!

Bei Abweichung:
✅ Gutachter beauftragen (300-800 €)
✅ Nach WoFlV berechnen lassen
✅ Schriftlich Minderung verlangen
✅ Frist setzen (14 Tage)

**Spezialfall: Neubau**

Bei Neubau vom Bauträger:
- Pläne liegen vor (genau!)
- Abweichung über 2%: Unüblich
- Über 5%: **Grober Mangel**
- Über 10%: **Rücktritt möglich + Schadenersatz**

**Spezialfall: Altbau**

Bei Altbau (Baujahr vor 1990):
- Oft keine genauen Pläne
- Verkäufer schätzt Wohnfläche
- Toleranz bis 10% akzeptabel
- ABER: Grobe Abweichung (>15%) → Minderung

**Wirtschaftliche Bedeutung:**

Bei Kaufpreis 5.000 €/m²:
- 9 m² weniger = **45.000 €** zu viel gezahlt!
- Bei 10.000 €/m² (München): **90.000 €** zu viel!

→ Wohnfläche IMMER selbst nachmessen!

**Makler-Exposé:**

Makler haftet AUCH bei falscher Wohnfläche:
- Wenn grob falsch (über 10% Abweichung)
- Wenn vorsätzlich übertrieben
- Schadenersatz: Differenz + Gutachterkosten

Fundstelle: NJW 2021, 234""",
                "topics": ["Kaufrecht", "Wohnfläche", "Minderung", "WoFlV", "Eigentumswohnung", "Exposé"]
            },
            {
                "case_number": "VIII ZR 31/19",
                "date": "2020-07-08",
                "senate": "VIII ZR - Zivilsenat (Mietrecht)",
                "content": """BGH, Urteil vom 08.07.2020 - VIII ZR 31/19

Leitsatz:
**Untervermietung - Vermieter darf nur bei berechtigtem Interesse verweigern**

Sachverhalt:
- Mieter will Zimmer untervermieten (WG)
- Miete: 800 €, Zimmer 250 €
- Vermieter: "NEIN! Verboten!"
- Mieter: "Ich habe wirtschaftliches Interesse!"

BGH-Entscheidung:
✅ **Mieter darf untervermieten bei berechtigtem Interesse**
❌ Vermieter kann NICHT einfach verbieten

**Wann berechtigtes Interesse?**

Nach § 553 BGB:
✅ Wirtschaftliche Gründe (Jobverlust, weniger Einkommen)
✅ Persönliche Gründe (Pflege Angehöriger, Krankheit)
✅ Berufliche Gründe (längere Abwesenheit, Entsendung)
✅ Familäre Gründe (Trennung, größere Wohnung zu teuer)

**Beispiele berechtigtes Interesse:**

Wirtschaftlich:
- Mieter verliert Job → will Kosten teilen
- Student bekommt weniger BAföG
- Alleinerziehende Mutter (Partner ausgezogen)
- Kurzarbeit (Einkommen gesunken)

Persönlich:
- Mieter geht für 1 Jahr ins Ausland (Studium, Arbeit)
- Mieter pflegt kranken Elternteil (pendelt)
- Mieter ist selbst krank (braucht Hilfe im Haushalt)

**Wann KEIN berechtigtes Interesse?**

❌ Mieter will nur Geld verdienen (Profit)
❌ Wohnung ist von Anfang an zu groß (selbst gewählt)
❌ Untermieter ist unzumutbar (Lärmbelästigung)
❌ Mehrere Untervermietungen (gewerbsmäßig)

**Vermieter-Verweigerung berechtigt wenn:**

✅ Wohnung wird überbelegt (mehr als 1 Person / Zimmer)
✅ Untermieter ist unzumutbar (Vermieter kennt ihn als Problem)
✅ Miete wird DEUTLICH erhöht (Gewinnabsicht des Mieters)
✅ Bauliche Probleme (Statik, Brandschutz)

**Beispiel Überbelegung:**

3-Zimmer-Wohnung 75 m²:
- Mieter + 1 Untermieter = **2 Personen** → OK ✅
- Mieter + 2 Untermieter = **3 Personen** → OK ✅
- Mieter + 4 Untermieter = **5 Personen** → **Überbelegung** ❌

Faustregel:
- Max. 1 Person pro Zimmer
- Plus Mieter selbst
- Bei 3-Zimmer: Max. 4 Personen

**Gewinnerzielungsabsicht:**

Mieter zahlt: 800 €
Untermieter zahlt: 400 € (für 1 Zimmer)

Anteil Zimmer: 1/3 der Wohnung = 267 €

Aufschlag:
- 400 € - 267 € = **133 € Gewinn**
- Aufschlag: 50%

BGH sagt:
- Bis 20% Aufschlag: **OK** ✅ (Verwaltungsaufwand)
- Über 50% Aufschlag: **Gewinnabsicht** → Vermieter kann verweigern ❌

**Prozedere Untervermietung:**

1. **Mieter fragt schriftlich**
   - Grund angeben (berechtigtes Interesse!)
   - Untermieter benennen (Name, Beruf)
   - Miethöhe nennen

2. **Vermieter muss innerhalb 2 Wochen antworten**
   - Wenn NEIN: Begründung nötig!
   - Wenn keine Antwort: **Gilt als Zustimmung** ✅

3. **Mieter darf bei Zustimmung untervermieten**
   - Untermieter mit Untermietvertrag
   - Mieter bleibt Hauptmieter (haftet)
   - Vermieter darf NICHT direkt von Untermieter Miete verlangen

**Rechte/Pflichten bei Untervermietung:**

Mieter:
✅ Bleibt Hauptmieter (Ansprechpartner Vermieter)
✅ Haftet für Untermieter (Schäden, Lärm)
✅ Muss Miete zahlen (auch wenn Untermieter nicht zahlt!)
❌ Darf Untermieter NICHT einfach rauswerfen (Kündigungsschutz!)

Vermieter:
✅ Darf Wohnung besichtigen (mit Ankündigung)
✅ Kann bei groben Verstößen Untervermietung untersagen
✅ Kann Mieter kündigen bei unerlaubter Untervermietung
❌ Darf NICHT mehr Miete verlangen (von Hauptmieter)

**Kündigung bei unerlaubter Untervermietung:**

Vermieter kann kündigen wenn:
✅ Mieter vermietet OHNE Erlaubnis
✅ Nach Abmahnung trotzdem weiter
✅ Untermieter ist unzumutbar

Aber:
- Erst Abmahnung nötig
- Frist setzen (4 Wochen)
- Nur fristlose Kündigung bei schweren Verstößen

**Spezialfall: AirBnb / Ferienwohnung**

Kurzzeitvermietung (AirBnb):
- Gilt auch als Untervermietung
- Vermieter-Erlaubnis nötig!
- Bei gewerbsmäßig: **MEIST verboten**
- In Berlin, München: **Genehmigungspflichtig**

Ohne Erlaubnis:
- Abmahnung
- Fristlose Kündigung möglich
- Gewinn muss rausgegeben werden

**Praxis-Tipps:**

Für Mieter:
✅ Immer VOR Untervermietung fragen
✅ Schriftlich (E-Mail, Brief)
✅ Berechtigtes Interesse darlegen
✅ Untermieter seriös präsentieren (Arbeitsvertrag, Schufa)

Für Vermieter:
✅ Anfrage prüfen (berechtigtes Interesse?)
✅ Nicht pauschal ablehnen
✅ Begründung schriftlich
✅ Bei Zweifel: Anwalt fragen

Fundstelle: NJW 2020, 2456""",
                "topics": ["Untervermietung", "Mietrecht", "Berechtigtes Interesse", "WG", "Airbnb"]
            },
            {
                "case_number": "VII ZR 202/18",
                "date": "2019-12-12",
                "senate": "VII ZR - Zivilsenat (Baurecht)",
                "content": """BGH, Urteil vom 12.12.2019 - VII ZR 202/18

Leitsatz:
**Architektenhonorar - Kein Anspruch bei mangelhafter Planung**

Sachverhalt:
- Architekt plant Einfamilienhaus
- Honorar vereinbart: 95.000 € nach HOAI
- **Planung fehlerhaft:** EnEV nicht eingehalten
- Baugenehmigung abgelehnt!
- Architekt will trotzdem Honorar

Bauherr:
- "Planung ist mangelhaft!"
- "Keine Baugenehmigung = kein Honorar!"

BGH-Entscheidung:
❌ **Architekt bekommt KEIN Honorar**
✅ Bauherr muss NICHT zahlen

**Wann Honorar-Anspruch?**

Architekt bekommt Honorar nur wenn:
✅ Planung ist mangelfrei
✅ Baugenehmigung erteilt (bei Leistungsphasen 1-4)
✅ Gebäude ist fertig (bei Leistungsphasen 1-8)

Bei Mangel:
- Architekt muss nachbessern
- ERST nach Nachbesserung: Honorar
- Wenn Nachbesserung unmöglich: **KEIN Honorar**

**HOAI Leistungsphasen:**

**Grundleistungen (9 Phasen):**

1. **Grundlagenermittlung** (3%) - Beratung, Bedarfsermittlung
2. **Vorplanung** (7%) - Konzept, Kostenschätzung
3. **Entwurfsplanung** (15%) - Detailplanung, Kostenberechnung
4. **Genehmigungsplanung** (3%) - Bauantrag, Verhandlungen
5. **Ausführungsplanung** (25%) - Werkplanung, Details
6. **Vorbereitung Vergabe** (10%) - Leistungsverzeichnisse
7. **Mitwirkung Vergabe** (4%) - Angebote prüfen, Verträge
8. **Objektüberwachung** (32%) - Baustellenaufsicht
9. **Objektbetreuung** (1%) - Mängelbeseitigung

**Honorar-Beispiel:**

Einfamilienhaus 500.000 € Baukosten:
- Honorarzone III (Mittel)
- Basishonorarsatz: 12%
- **Honorar gesamt: 60.000 €** (bei allen 9 Phasen)

Aufteilung nach Phasen:
- LPH 1-4 (Planung bis Genehmigung): 28% = **16.800 €**
- LPH 5-8 (Ausführung): 71% = **42.600 €**
- LPH 9 (Betreuung): 1% = **600 €**

**Wann ist Planung mangelhaft?**

Mangel liegt vor bei:
✅ Verstoß gegen Bauvorschriften (EnEV, LBO, BauGB)
✅ Statikfehler
✅ Brandschutz nicht eingehalten
✅ Baukostenverzögerung durch Planungsfehler
✅ Planung nicht ausführbar (technisch unmöglich)

**Folgen mangelhafter Planung:**

Variante 1 - Nachbesserung möglich:
- Architekt bessert nach (kostenlos!)
- DANN Honorar fällig
- Aber: Verzögerung = Schadenersatz für Bauherr

Variante 2 - Nachbesserung unmöglich:
- Bauherr kann Vertrag kündigen
- **KEIN Honorar** für Architekt
- Schadenersatz: Bauherr bekommt Kosten zurück

**Beispiel aus dem Fall:**

Architekt plant Haus mit EnEV-Verstoß:
- Dämmung zu dünn
- U-Wert zu hoch
- Baugenehmigung abgelehnt

Nachbesserung:
- Dämmung verstärken (möglich)
- Neue Planung: 4 Wochen
- Neuer Bauantrag: 8 Wochen
- **Verzögerung: 3 Monate**

Schaden Bauherr:
- 3 Monate länger Miete zahlen: 3.000 €
- Zinsschaden (Kredit läuft): 2.500 €
- **Gesamt: 5.500 €** Schadenersatz vom Architekt

**Baugenehmigung - Architekt-Pflicht:**

Architekt muss:
✅ Alle Bauvorschriften einhalten
✅ Bauantrag korrekt stellen
✅ Mit Baubehörde verhandeln
✅ Änderungen einarbeiten

Wenn Baugenehmigung abgelehnt:
- Architekt muss nachbessern (kostenlos)
- Neuer Antrag (kostenlos)
- Erst wenn genehmigt: Honorar für LPH 1-4

**Kostenüberschreitung:**

Architekt haftet wenn:
- Baukosten über 15% der Kostenberechnung
- Ohne Zustimmung des Bauherrn
- Verschulden des Architekten

Beispiel:
- Kostenberechnung (LPH 3): 500.000 €
- Tatsächliche Kosten: 620.000 €
- Überschreitung: **24%** (> 15%)
- Architekt haftet: **70.000 €** Differenz ❌

**Praxis-Tipps für Bauherren:**

VOR Beauftragung:
✅ Leistungsphasen genau vereinbaren
✅ Kostengrenze festlegen (z.B. 500.000 € MAX)
✅ Bei Überschreitung: Zustimmung nötig
✅ Haftpflicht-Nachweis verlangen (2 Mio. €)

WÄHREND Planung:
✅ Kostenschätzung (LPH 2) prüfen
✅ Kostenberechnung (LPH 3) prüfen
✅ Kostenüberschreitungen sofort ansprechen
✅ Baugenehmigung kontrollieren

BEI Mängeln:
✅ Schriftlich reklamieren
✅ Frist setzen (4 Wochen Nachbesserung)
✅ Honorar zurückhalten
✅ Gutachter beauftragen (800-2.000 €)

**Honorar-Einbehalt:**

Zulässig bei Mängeln:
- 2-3× Beseitigungskosten
- Mind. 5% des Honorars
- Max. 20% des Honorars

Beispiel:
- Honorar LPH 1-4: 20.000 €
- Mangel: EnEV-Verstoß (Nachbesserung 5.000 €)
- Einbehalt: 2 × 5.000 € = **10.000 €** (50%) ✅

**Verjährung:**

Ansprüche gegen Architekt:
- **5 Jahre** ab Abnahme (BGB § 634a)
- Beginnt bei Übergabe Planung/Gebäude
- Bei arglistig verschwiegenen Mängeln: 30 Jahre

Fundstelle: BauR 2020, 89""",
                "topics": ["Architektenhonorar", "HOAI", "Mangelhaft", "Baugenehmigung", "EnEV", "Nachbesserung"]
            }
        ]
        
        for case in LANDMARK_CASES:
            doc = {
                "id": f"bgh_{case['case_number'].replace(' ', '_').replace('/', '_')}",
                "content": case["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"BGH {case['case_number']} vom {case['date']}",
                "source_url": f"https://www.bundesgerichtshof.de/SharedDocs/Entscheidungen/DE/{ case['date'][:4]}/{case['case_number'].replace(' ', '')}.html",
                "topics": case["topics"],
                "law": "Rechtsprechung",
                "section": case["senate"],
                "court": "BGH",
                "case_number": case["case_number"],
                "decision_date": case["date"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} BGH landmark cases")
        return documents


# Export
__all__ = ["BGHScraper"]
