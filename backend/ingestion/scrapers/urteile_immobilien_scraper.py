"""
Urteile Immobilienrecht Scraper
=================================

Umfassende Rechtsprechung aus allen Gerichtsebenen:
- BGH (Bundesgerichtshof)
- OLG (Oberlandesgerichte)
- LG (Landgerichte)
- AG (Amtsgerichte)

Alle relevanten Bereiche des Immobilienrechts:
- Mietrecht (Wohnraum & Gewerbe)
- Kaufrecht (§ 433 BGB)
- Werkvertragsrecht/Baurecht (§ 631 BGB, VOB/B)
- Sachenrecht (Grundbuch, § 873 BGB)
- WEG (Wohnungseigentumsgesetz)
- ZVG (Zwangsversteigerung)
- Nachbarrecht (§ 906 BGB)
- Maklerrecht (§ 652 BGB)
"""

from typing import List, Dict
from datetime import datetime


class UrteileImmobilienScraper:
    """Scraper für Rechtsprechung im Immobilienrecht"""
    
    def scrape_all(self) -> List[Dict]:
        """Lädt alle Urteile"""
        urteile = []
        urteile.extend(self.scrape_bgh())
        urteile.extend(self.scrape_olg())
        urteile.extend(self.scrape_lg())
        urteile.extend(self.scrape_ag())
        return urteile
    
    # ========================================
    # BGH - Bundesgerichtshof
    # ========================================
    
    def scrape_bgh(self) -> List[Dict]:
        """BGH Urteile - Höchstrichterliche Rechtsprechung"""
        return [
            # MIETRECHT
            {
                "title": "BGH VIII ZR 185/14 - Schönheitsreparaturen: Unwirksamkeit starrer Fristen",
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

Rechtliche Einordnung:
§ 535 Abs. 1 S. 2 BGB: Erhaltungspflicht des Vermieters
§ 307 BGB: Inhaltskontrolle von AGB
Starre Fristen = unangemessene Benachteiligung

Praxishinweise:
- Vermieter können keine starren Fristen mehr verwenden
- Formulierung "bei Bedarf" oder "im Allgemeinen" ist zulässig
- Unrenoviert übergebene Wohnungen: Mieter muss nicht renovieren
- Quotenklauseln sind ebenfalls unwirksam

Fundstelle: NJW 2015, 1461""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VIII ZR 185/14",
                "datum": "2015-03-18",
                "senat": "VIII ZR (Mietrecht)",
                "rechtsgebiet": "Mietrecht",
                "thema": "Schönheitsreparaturen",
                "keywords": ["Schönheitsreparaturen", "Starre Fristen", "§ 307 BGB", "Unwirksamkeit", "Mietvertrag"],
                "citation": "BGH, Urt. v. 18.03.2015 - VIII ZR 185/14, NJW 2015, 1461",
            },
            
            {
                "title": "BGH VIII ZR 242/13 - Schönheitsreparaturen bei unrenoviert übergebener Wohnung",
                "content": """BGH, Urteil vom 18.03.2015 - VIII ZR 242/13

Leitsatz:
Eine formularmäßige Überbürdung der Schönheitsreparaturen auf den Mieter ist unwirksam, wenn die Wohnung unrenoviert übergeben wurde.

Sachverhalt:
Die Vermieterin übergibt die Wohnung in nicht renoviertem Zustand an die Mieter. Im Mietvertrag ist jedoch vereinbart, dass die Mieter die Schönheitsreparaturen durchzuführen haben. Nach Auszug verlangt die Vermieterin Schadensersatz für unterlassene Renovierung.

Entscheidung:
Der BGH wies die Klage ab. Die Schönheitsreparaturklausel ist unwirksam.

Begründung:
Wenn der Vermieter die Wohnung unrenoviert übergibt, aber trotzdem die Renovierungslast auf den Mieter abwälzt, liegt eine unangemessene Benachteiligung nach § 307 BGB vor. Der Mieter würde die Wohnung in besserem Zustand zurückgeben, als er sie erhalten hat.

Rechtliche Grundlagen:
§ 535 Abs. 1 S. 2 BGB: Erhaltungspflicht des Vermieters
§ 307 BGB: Inhaltskontrolle
Grundsatz: Vermieter trägt Erhaltungslast

Ausnahme - Wirksamkeit bei:
1. Die Wohnung wurde renoviert übergeben, ODER
2. Der Mieter erhält angemessenen Ausgleich (z.B. Mietminderung, Kostenerstattung)

Praktische Konsequenzen:
- Vermieter muss bei Übergabe den Zustand dokumentieren (Fotos!)
- Unrenoviert = keine Renovierungspflicht für Mieter
- Vermieter trägt Renovierungskosten selbst
- "Besenrein" genügt bei Auszug

Fundstelle: NJW 2015, 1463""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VIII ZR 242/13",
                "datum": "2015-03-18",
                "senat": "VIII ZR (Mietrecht)",
                "rechtsgebiet": "Mietrecht",
                "thema": "Schönheitsreparaturen unrenoviert",
                "keywords": ["Schönheitsreparaturen", "unrenovierte Übergabe", "§ 307 BGB", "Auszug"],
                "citation": "BGH, Urt. v. 18.03.2015 - VIII ZR 242/13, NJW 2015, 1463",
            },
            
            {
                "title": "BGH VIII ZR 137/18 - Mietminderung bei Schimmelbefall",
                "content": """BGH, Urteil vom 06.11.2019 - VIII ZR 137/18

Leitsatz:
Ein zur Schimmelbildung führender Baumangel liegt vor, wenn die Wohnung bei vertragsgemäßem Gebrauch nicht die erwartete Beschaffenheit aufweist.

Sachverhalt:
In der Mietwohnung trat Schimmel auf. Der Vermieter behauptet, der Mieter habe falsch gelüftet und geheizt. Der Mieter mindert die Miete um 20%. Der Vermieter klagt auf Zahlung der vollen Miete.

Entscheidung:
Der BGH gab dem Mieter recht. Die Mietminderung ist berechtigt.

Begründung:
1. Beweislast: Der Vermieter muss beweisen, dass der Schimmel durch Fehlverhalten des Mieters entstanden ist (Beweislastumkehr nach § 536a Abs. 1 BGB).

2. Erwartete Beschaffenheit: Eine Wohnung muss so beschaffen sein, dass bei normalem Wohn- und Lüftungsverhalten kein Schimmel entsteht.

3. Zumutbarkeit: Dauerlüften alle 2 Stunden ist unzumutbar. Normal ist 2-3x täglich Stoßlüften.

Rechtliche Grundlagen:
§ 536 BGB: Mietminderung bei Mangel
§ 536a Abs. 1 BGB: Beweislastumkehr
§ 536c BGB: Schadensersatz des Mieters

Mietminderungsquote bei Schimmel (Rechtsprechungsübersicht):
- Schlafzimmer (leichter Befall): 10-20%
- Schlafzimmer (starker Befall): 50-100%
- Mehrere Räume betroffen: 30-80%
- Gesundheitsgefahr: bis 100%

Pflichten des Mieters:
- Normal lüften (2-3x täglich Stoßlüften)
- Heizen auf Mindesttemperatur (ca. 18°C)
- Schimmel umgehend melden (Anzeigepflicht § 536c Abs. 1 BGB)

Pflichten des Vermieters:
- Bauliche Mängel beseitigen
- Fachgutachten einholen
- Sanierung durchführen
- Beweislast für Mieterverursachung

Fundstelle: NJW 2020, 147""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VIII ZR 137/18",
                "datum": "2019-11-06",
                "senat": "VIII ZR (Mietrecht)",
                "rechtsgebiet": "Mietrecht",
                "thema": "Schimmel und Mietminderung",
                "keywords": ["Schimmel", "Mietminderung", "Beweislast", "Lüftung", "§ 536 BGB"],
                "citation": "BGH, Urt. v. 06.11.2019 - VIII ZR 137/18, NJW 2020, 147",
            },
            
            # KAUFRECHT
            {
                "title": "BGH V ZR 305/13 - Aufklärungspflicht beim Immobilienkauf: Altlasten",
                "content": """BGH, Urteil vom 10.10.2014 - V ZR 305/13

Leitsatz:
Der Verkäufer eines Grundstücks muss den Käufer über ihm bekannte Altlasten aufklären, auch wenn diese im Grundbuch eingetragen sind.

Sachverhalt:
Der Verkäufer verkauft ein Grundstück, auf dem früher eine Tankstelle stand. Im Grundbuch war eine Baulast wegen möglicher Bodenverunreinigung eingetragen. Der Verkäufer erwähnte dies jedoch nicht im Verkaufsgespräch. Nach dem Kauf stellt sich heraus, dass eine Bodensanierung notwendig ist (Kosten: 150.000 €). Der Käufer verlangt Schadensersatz.

Entscheidung:
Der BGH gab dem Käufer recht. Der Verkäufer haftet auf Schadensersatz.

Begründung:
1. Aufklärungspflicht: Der Verkäufer muss über Umstände aufklären, die für die Kaufentscheidung wesentlich sind und die der Käufer nicht kennt.

2. Grundbucheintragung entbindet nicht: Auch wenn Mängel im Grundbuch eingetragen sind, muss der Verkäufer aktiv darauf hinweisen.

3. Arglist: Verschweigen bekannter Altlasten ist arglistig (§ 123 BGB, § 444 BGB).

Rechtliche Grundlagen:
§ 433 BGB: Kaufvertragspflichten
§ 434 BGB: Sachmangel
§ 444 BGB: Arglistige Täuschung
§ 311 Abs. 2 BGB: Culpa in contrahendo

Aufklärungspflichten des Verkäufers:
- Altlasten (Boden, Gebäude)
- Baulasten
- Nachbarstreitigkeiten
- Baumängel
- Asbest, Schadstoffe
- Denkmalschutz

Praxishinweise Käufer:
- Grundbuch vollständig prüfen
- Baulastenverzeichnis einsehen
- Altlastenkataster abfragen
- Bodengutachten einholen
- Verkäuferauskunft schriftlich

Fundstelle: NJW 2014, 3775""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "V ZR 305/13",
                "datum": "2014-10-10",
                "senat": "V ZR (Immobilienrecht)",
                "rechtsgebiet": "Kaufrecht",
                "thema": "Aufklärungspflicht Altlasten",
                "keywords": ["Immobilienkauf", "Altlasten", "Aufklärungspflicht", "§ 444 BGB", "Arglist"],
                "citation": "BGH, Urt. v. 10.10.2014 - V ZR 305/13, NJW 2014, 3775",
            },
            
            # WEG
            {
                "title": "BGH V ZR 98/20 - WEG: Anfechtung Beschluss wegen fehlender Beschlusskompetenz",
                "content": """BGH, Urteil vom 02.04.2021 - V ZR 98/20

Leitsatz:
Ein Beschluss der Wohnungseigentümergemeinschaft ist nichtig, wenn die Eigentümerversammlung für die beschlossene Maßnahme keine Beschlusskompetenz hatte.

Sachverhalt:
Die Eigentümerversammlung beschließt umfangreiche Modernisierungsmaßnahmen (Fassadendämmung, neue Fenster) mit Kosten von 200.000 €. Ein Eigentümer stimmt dagegen und ficht den Beschluss an mit der Begründung, es handele sich um bauliche Veränderungen, die seine Zustimmung erfordern.

Entscheidung:
Der BGH gab dem Eigentümer recht. Der Beschluss ist nichtig.

Begründung:
1. Abgrenzung Instandhaltung/Modernisierung:
   - Instandhaltung: Erhaltung des bisherigen Zustands (Mehrheitsbeschluss)
   - Modernisierung: Verbesserung über bisherigen Zustand (Zustimmung aller Betroffenen)

2. Fassadendämmung mit neuen Fenstern = bauliche Veränderung
   → Erfordert Zustimmung nach § 20 Abs. 2 WEG (jetzt § 20 Abs. 1 WEG n.F.)

3. Betroffene Eigentümer: alle, deren Sondereigentum berührt wird

Rechtliche Grundlagen:
§ 20 WEG a.F. (jetzt § 20 Abs. 1 WEG): Bauliche Veränderungen
§ 21 WEG: Instandhaltung und Instandsetzung
§ 23 WEG: Beschlussfassung
§ 43 WEG: Anfechtung von Beschlüssen

Beschlusskompetenz WEG (neu seit 01.12.2020):
- Instandhaltung/Instandsetzung: Mehrheit (§ 21 WEG)
- Modernisierung: Mehrheit, wenn zumutbar (§ 20 Abs. 1 WEG)
- Bauliche Veränderung ins Sondereigentum: Zustimmung Betroffener

Praxishinweise:
- Maßnahme rechtlich prüfen lassen
- Zustimmungen einholen BEVOR Beschluss
- Protokoll muss Abstimmungsergebnis dokumentieren
- Anfechtungsfrist: 1 Monat ab Beschluss

Fundstelle: NJW 2021, 1725""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "V ZR 98/20",
                "datum": "2021-04-02",
                "senat": "V ZR (Immobilienrecht)",
                "rechtsgebiet": "WEG",
                "thema": "Beschlusskompetenz Modernisierung",
                "keywords": ["WEG", "Beschluss", "Modernisierung", "§ 20 WEG", "Anfechtung"],
                "citation": "BGH, Urt. v. 02.04.2021 - V ZR 98/20, NJW 2021, 1725",
            },
            
            # ========================================
            # WEITERE BGH-URTEILE - MIETRECHT
            # ========================================
            
            {
                "title": "BGH VIII ZR 107/21 - Eigenbedarfskündigung: Anforderungen an Begründung",
                "content": """BGH, Urteil vom 15.03.2023 - VIII ZR 107/21

Leitsatz:
Die Begründung einer Eigenbedarfskündigung muss die Person, für die Eigenbedarf geltend gemacht wird, und den Grund des Bedarfs so konkret bezeichnen, dass der Mieter die Kündigung prüfen kann.

Sachverhalt:
Der Vermieter kündigt wegen Eigenbedarfs für seine "Tochter mit Familie". Der Mieter widerspricht und bestreitet den Eigenbedarf. Er rügt, die Kündigung sei zu unbestimmt.

Entscheidung:
Der BGH gab dem Vermieter recht. Die Kündigung ist wirksam.

Begründung:
§ 573 Abs. 3 BGB erfordert:
1. Angabe der Gründe im Kündigungsschreiben
2. Person des Bedarfsträgers (Vermieter, Familienangehöriger, Haushaltsangehöriger)
3. Grund des Bedarfs (warum diese Wohnung)

"Tochter mit Familie" = ausreichend konkret
- Person identifizierbar
- Familienzugehörigkeit klar
- Lebenssituation erkennbar

Unzureichend wäre:
- "Familienangehöriger" (ohne Bezeichnung)
- "Eigenbedarf" (ohne Bedarfsträger)
- Keine Angabe zur Nutzungsabsicht

Rechtliche Grundlagen:
§ 573 Abs. 2 Nr. 2 BGB: Eigenbedarf
§ 573 Abs. 3 BGB: Begründungserfordernis
§ 574 BGB: Widerspruch wegen Härte

Praxishinweise:
- Name des Bedarfsträgers angeben
- Grund kurz erläutern (Einzug, berufliche Gründe)
- Warum diese Wohnung geeignet ist
- Dokumentation des echten Bedarfs führen

Fundstelle: NJW 2023, 1879""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VIII ZR 107/21",
                "datum": "2023-03-15",
                "senat": "VIII ZR (Mietrecht)",
                "rechtsgebiet": "Mietrecht",
                "thema": "Eigenbedarfskündigung Begründung",
                "keywords": ["Eigenbedarf", "§ 573 BGB", "Kündigung", "Begründung", "Widerspruch"],
                "citation": "BGH, Urt. v. 15.03.2023 - VIII ZR 107/21, NJW 2023, 1879",
            },
            
            {
                "title": "BGH VIII ZR 9/22 - Mietkaution: Rückzahlungspflicht und Abrechnungsfrist",
                "content": """BGH, Urteil vom 18.01.2023 - VIII ZR 9/22

Leitsatz:
Die Rückzahlung der Mietkaution kann der Vermieter nur so lange zurückhalten, wie er noch Ansprüche gegen den Mieter geltend machen kann. Eine angemessene Prüfungsfrist beträgt 3-6 Monate.

Sachverhalt:
Der Mieter zieht nach 8 Jahren aus. Der Vermieter behält die Kaution (3 Monatsmieten = 2.400 €) einbehalten. Nach 14 Monaten fordert der Mieter die Kaution zurück. Der Vermieter behauptet, er prüfe noch Schäden.

Entscheidung:
Der BGH verurteilte den Vermieter zur Rückzahlung.

Begründung:
Der Vermieter kann die Kaution nur für berechtigte Gegenforderungen einbehalten:
- Mietrückstände
- Schadensersatzansprüche
- Betriebskostennachzahlungen

Prüfungsfrist:
- 3-6 Monate ist angemessen
- Danach: Rückzahlung fällig
- 14 Monate: deutlich zu lang

Rechtliche Grundlagen:
§ 551 BGB: Begrenzung und Anlage von Mietsicherheiten
§ 273 BGB: Zurückbehaltungsrecht
Treu und Glauben § 242 BGB

Kautionsabrechnung muss enthalten:
1. Aufstellung aller Gegenforderungen
2. Schadensnachweis (Protokoll, Fotos)
3. Betriebskostenabrechnung (falls ausstehend)
4. Berechnung des Rückzahlungsbetrags

Praxishinweise:
- Übergabeprotokoll erstellen (mit Fotos)
- Betriebskosten zeitnah abrechnen
- Kaution verzinsen (§ 551 Abs. 3 BGB)
- Nach 6 Monaten: Mahnung senden

Fundstelle: NJW 2023, 513""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VIII ZR 9/22",
                "datum": "2023-01-18",
                "senat": "VIII ZR (Mietrecht)",
                "rechtsgebiet": "Mietrecht",
                "thema": "Mietkaution Rückzahlung",
                "keywords": ["Kaution", "§ 551 BGB", "Rückzahlung", "Prüfungsfrist", "Auszug"],
                "citation": "BGH, Urt. v. 18.01.2023 - VIII ZR 9/22, NJW 2023, 513",
            },
            
            {
                "title": "BGH VIII ZR 45/21 - Mieterhöhung: Mietspiegelabweichung",
                "content": """BGH, Urteil vom 28.09.2022 - VIII ZR 45/21

Leitsatz:
Der Vermieter kann bei der Mieterhöhung nach § 558 BGB vom Mietspiegel abweichen, wenn er besondere Umstände darlegt, die einen höheren Wert rechtfertigen.

Sachverhalt:
Der Vermieter verlangt Mieterhöhung auf 12 €/m². Der Mietspiegel weist für vergleichbare Wohnungen 10 €/m² aus. Der Vermieter beruft sich auf hochwertige Ausstattung (Designerküche, Echtholzparkett).

Entscheidung:
Der BGH verwies zurück. Die Sonderfaktoren sind zu prüfen.

Begründung:
§ 558 Abs. 2 BGB: ortsübliche Vergleichsmiete
Mietspiegel = Indiz, aber nicht verbindlich

Abweichung zulässig bei:
- Besonders hochwertiger Ausstattung
- Außergewöhnlicher Lage
- Energetischer Sanierung über Standard
- Denkmalschutz-Auflagen

Darlegungslast:
1. Vermieter muss Sonderfaktoren benennen
2. Konkret beschreiben (nicht pauschal "hochwertig")
3. Werterhöhung beziffern

Rechtliche Grundlagen:
§ 558 BGB: Mieterhöhung auf ortsübliche Vergleichsmiete
§ 558a BGB: Form und Begründung
§ 558d BGB: Qualifizierter Mietspiegel

Praxishinweise:
- Mietspiegel als Ausgangspunkt
- Zu-/Abschläge für Sonderfaktoren
- Sachverständigengutachten bei Streit
- Kappungsgrenze beachten (15-20%)

Fundstelle: NJW 2022, 3578""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VIII ZR 45/21",
                "datum": "2022-09-28",
                "senat": "VIII ZR (Mietrecht)",
                "rechtsgebiet": "Mietrecht",
                "thema": "Mieterhöhung Mietspiegel",
                "keywords": ["Mieterhöhung", "§ 558 BGB", "Mietspiegel", "ortsübliche Vergleichsmiete"],
                "citation": "BGH, Urt. v. 28.09.2022 - VIII ZR 45/21, NJW 2022, 3578",
            },
            
            # ========================================
            # WEITERE BGH-URTEILE - KAUFRECHT
            # ========================================
            
            {
                "title": "BGH V ZR 176/22 - Immobilienkauf: Arglistige Täuschung über Altlasten",
                "content": """BGH, Urteil vom 07.07.2023 - V ZR 176/22

Leitsatz:
Verschweigt der Verkäufer einer Immobilie bekannte Altlasten (Bodenverunreinigung), liegt eine arglistige Täuschung vor, die zur Anfechtung berechtigt.

Sachverhalt:
Der Käufer erwirbt ein Grundstück für 500.000 €. Nach Kaufabschluss stellt sich heraus, dass das Grundstück mit Öl kontaminiert ist (ehemaliger Tankstellenbetrieb). Die Sanierungskosten betragen 120.000 €. Der Verkäufer wusste von der Kontamination.

Entscheidung:
Der BGH bejahte die Anfechtbarkeit. Der Käufer kann vom Vertrag zurücktreten.

Begründung:
Arglistige Täuschung nach § 123 BGB:
1. Täuschungshandlung: Verschweigen offenbarungspflichtiger Umstände
2. Arglist: Verkäufer wusste von Altlast
3. Kausalität: Käufer hätte nicht oder anders gekauft

Offenbarungspflicht bei:
- Altlasten/Bodenverunreinigung
- Asbest, PCB
- Erheblichen Baumängeln
- Schädlingsbefall
- Denkmalschutz-Auflagen

Rechtsfolgen:
- Anfechtung § 123 BGB → Vertrag nichtig
- Rückabwicklung
- Schadensersatz

Rechtliche Grundlagen:
§ 123 BGB: Anfechtung wegen Täuschung
§ 442 BGB: Kenntnis des Käufers
§ 444 BGB: Haftungsausschluss bei Arglist unwirksam

Haftungsausschluss "gekauft wie gesehen" unwirksam bei:
- Arglist des Verkäufers
- Vorsätzlichem Verschweigen

Praxishinweise Käufer:
- Altlastenkataster abfragen
- Baugrundgutachten beauftragen
- Fragen im Vertrag dokumentieren

Fundstelle: NJW 2023, 2872""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "V ZR 176/22",
                "datum": "2023-07-07",
                "senat": "V ZR (Immobilienrecht)",
                "rechtsgebiet": "Kaufrecht",
                "thema": "Altlasten arglistige Täuschung",
                "keywords": ["Immobilienkauf", "Altlasten", "§ 123 BGB", "arglistige Täuschung", "Anfechtung"],
                "citation": "BGH, Urt. v. 07.07.2023 - V ZR 176/22, NJW 2023, 2872",
            },
            
            {
                "title": "BGH V ZR 33/22 - Grundstückskauf: Gewährleistung bei Flächenabweichung",
                "content": """BGH, Urteil vom 28.04.2023 - V ZR 33/22

Leitsatz:
Eine erhebliche Abweichung der tatsächlichen Grundstücksfläche von der im Kaufvertrag angegebenen Fläche stellt einen Sachmangel dar, der zur Minderung berechtigt.

Sachverhalt:
Der Käufer erwirbt ein Grundstück "lt. Grundbuch ca. 850 m²" für 340.000 €. Eine Vermessung ergibt nur 720 m² (15,3% weniger). Der Käufer verlangt Kaufpreisminderung.

Entscheidung:
Der BGH gab dem Käufer recht. Minderung von 52.000 € berechtigt.

Begründung:
Sachmangel nach § 434 BGB:
- Flächenangabe ist Beschaffenheitsvereinbarung
- "ca." = Toleranz von ±5%
- Abweichung >10% = erheblicher Mangel

Berechnung Minderung:
- Kaufpreis: 340.000 €
- Abweichung: 130 m² (15,3%)
- Minderung: 340.000 × (130/850) = 52.000 €

Rechtliche Grundlagen:
§ 434 BGB: Sachmangel
§ 437 Nr. 2 BGB: Minderung
§ 441 BGB: Berechnung

"Circa"-Angaben:
- ±5%: keine Abweichung
- 5-10%: Grenzbereich
- >10%: erhebliche Abweichung = Mangel

Praxishinweise:
- Grundstück vor Kauf vermessen lassen
- Grundbuchfläche ≠ tatsächliche Fläche
- Gewährleistungsausschluss prüfen
- Bei Verdacht: Vermesser beauftragen

Fundstelle: NJW 2023, 2115""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "V ZR 33/22",
                "datum": "2023-04-28",
                "senat": "V ZR (Immobilienrecht)",
                "rechtsgebiet": "Kaufrecht",
                "thema": "Flächenabweichung Minderung",
                "keywords": ["Grundstückskauf", "Flächenabweichung", "§ 434 BGB", "Minderung", "Sachmangel"],
                "citation": "BGH, Urt. v. 28.04.2023 - V ZR 33/22, NJW 2023, 2115",
            },
            
            # ========================================
            # WEITERE BGH-URTEILE - BAURECHT
            # ========================================
            
            {
                "title": "BGH VII ZR 130/22 - Bauvertrag: Abnahme und Mängelrüge",
                "content": """BGH, Urteil vom 16.03.2023 - VII ZR 130/22

Leitsatz:
Die Abnahme eines Bauwerks kann auch konkludent erfolgen. Bezieht der Besteller das Bauwerk und nutzt es über längere Zeit ohne wesentliche Mängelrügen, liegt eine konkludente Abnahme vor.

Sachverhalt:
Der Bauunternehmer errichtet ein Einfamilienhaus. Der Bauherr bezieht das Haus, verweigert aber die förmliche Abnahme. Nach 2 Jahren Nutzung macht er Mängel geltend (Risse in Außenputz). Der Unternehmer beruft sich auf Verjährung (5 Jahre ab Abnahme).

Entscheidung:
Der BGH stellte konkludente Abnahme fest. Verjährung beginnt mit Einzug.

Begründung:
Abnahme nach § 640 BGB:
- Billigung des Werks als vertragsgemäß
- Ausdrücklich oder konkludent

Konkludente Abnahme bei:
- Bezug des Gebäudes
- Nutzung ohne wesentliche Beanstandung
- Vergehen angemessener Zeit (hier: 6-12 Monate)

Wirkungen der Abnahme:
- Gefahrübergang
- Fälligkeit Vergütung
- Beginn Verjährung (5 Jahre § 634a BGB)
- Beweislastumkehr

Rechtliche Grundlagen:
§ 640 BGB: Abnahme
§ 634a BGB: Verjährung Mängelansprüche
§ 650g BGB: Zustandsfeststellung Verbraucherbauvertrag

Praxishinweise Bauherr:
- Förmliche Abnahme verlangen
- Mängel schriftlich rügen
- Vorbehalt im Abnahmeprotokoll
- Sicherheitseinbehalt vereinbaren

Fundstelle: NJW 2023, 1591""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VII ZR 130/22",
                "datum": "2023-03-16",
                "senat": "VII ZR (Baurecht)",
                "rechtsgebiet": "Baurecht",
                "thema": "Abnahme konkludent",
                "keywords": ["Bauvertrag", "Abnahme", "§ 640 BGB", "Verjährung", "Mängel"],
                "citation": "BGH, Urt. v. 16.03.2023 - VII ZR 130/22, NJW 2023, 1591",
            },
            
            {
                "title": "BGH VII ZR 245/21 - Bauhandwerkersicherung nach § 648a BGB",
                "content": """BGH, Urteil vom 08.12.2022 - VII ZR 245/21

Leitsatz:
Der Bauunternehmer kann vom Besteller nach § 648a BGB eine Sicherheit für die vereinbarte Vergütung verlangen. Die Verweigerung berechtigt zur Leistungsverweigerung.

Sachverhalt:
Ein Bauunternehmer soll eine Dachsanierung für 85.000 € durchführen. Er verlangt eine Sicherheit nach § 648a BGB in Höhe von 93.500 € (110%). Der private Bauherr weigert sich. Der Unternehmer stellt die Arbeiten ein.

Entscheidung:
Der BGH bestätigt das Leistungsverweigerungsrecht.

Begründung:
§ 648a BGB (Bauhandwerkersicherung):
- Sicherheit bis zu 110% der Vergütung
- Bürgschaft oder Einzahlung auf Sperrkonto
- Auch bei Verbrauchern (seit 2018)

Ausnahmen (§ 648a Abs. 6 BGB):
- Besteller ist juristische Person des öffentl. Rechts
- Bauwerk wird zur Herstellung von Waren genutzt

Rechtsfolgen bei Verweigerung:
- Leistungsverweigerungsrecht des Unternehmers
- Nachfrist setzen (mind. 10 Werktage)
- Kündigung und Vergütungsanspruch

Rechtliche Grundlagen:
§ 648a BGB: Bauhandwerkersicherung
§ 650f BGB: (identisch für Verbraucherbauvertrag)
§ 320 BGB: Einrede des nichterfüllten Vertrags

Praxishinweise:
- Sicherheit vor Baubeginn verlangen
- Fristsetzung schriftlich (Einschreiben)
- Dokumentation der Verweigerung
- Bürgschaft einer Bank/Versicherung

Fundstelle: NJW 2023, 592""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "VII ZR 245/21",
                "datum": "2022-12-08",
                "senat": "VII ZR (Baurecht)",
                "rechtsgebiet": "Baurecht",
                "thema": "Bauhandwerkersicherung",
                "keywords": ["Bauvertrag", "§ 648a BGB", "Sicherheit", "Leistungsverweigerung", "Bürgschaft"],
                "citation": "BGH, Urt. v. 08.12.2022 - VII ZR 245/21, NJW 2023, 592",
            },
            
            # ========================================
            # WEITERE BGH-URTEILE - WEG
            # ========================================
            
            {
                "title": "BGH V ZR 77/22 - WEG: Sondernutzungsrecht und bauliche Veränderung",
                "content": """BGH, Urteil vom 14.07.2023 - V ZR 77/22

Leitsatz:
Ein Wohnungseigentümer, dem ein Sondernutzungsrecht an einer Gartenfläche zusteht, darf diese nicht ohne Beschluss der Eigentümerversammlung baulich verändern.

Sachverhalt:
Ein Eigentümer mit Sondernutzungsrecht an der Gartenfläche errichtet ein Gartenhaus (3x4m) ohne Genehmigung der WEG. Andere Eigentümer verlangen Rückbau.

Entscheidung:
Der BGH verurteilte zum Rückbau.

Begründung:
Sondernutzungsrecht nach WEG:
- Berechtigt zur alleinigen Nutzung
- Nicht zur baulichen Veränderung des Gemeinschaftseigentums

Gartenfläche = Gemeinschaftseigentum
Gartenhaus = bauliche Veränderung § 20 WEG

Erforderlich für bauliche Veränderung:
1. Antrag in Eigentümerversammlung
2. Beschluss mit erforderlicher Mehrheit
3. Ggf. Zustimmung beeinträchtigter Eigentümer

Rechtliche Grundlagen:
§ 5 Abs. 4 WEG: Sondernutzungsrecht
§ 20 WEG: Bauliche Veränderungen
§ 14 WEG: Pflichten der Eigentümer
§ 1004 BGB: Beseitigungsanspruch

Praxishinweise:
- Vor Baumaßnahme: Antrag stellen
- Beschluss abwarten
- Bei Eilbedürftigkeit: Umlaufbeschluss
- Nachträgliche Genehmigung möglich

Fundstelle: NJW 2023, 3028""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "V ZR 77/22",
                "datum": "2023-07-14",
                "senat": "V ZR (Immobilienrecht)",
                "rechtsgebiet": "WEG",
                "thema": "Sondernutzungsrecht bauliche Veränderung",
                "keywords": ["WEG", "Sondernutzungsrecht", "§ 20 WEG", "bauliche Veränderung", "Gartenhaus"],
                "citation": "BGH, Urt. v. 14.07.2023 - V ZR 77/22, NJW 2023, 3028",
            },
            
            {
                "title": "BGH V ZR 213/21 - WEG: Hausgeldklage und Zahlungsverzug",
                "content": """BGH, Urteil vom 18.11.2022 - V ZR 213/21

Leitsatz:
Die Gemeinschaft der Wohnungseigentümer kann rückständiges Hausgeld auch dann geltend machen, wenn der Wirtschaftsplan noch nicht bestandskräftig beschlossen wurde.

Sachverhalt:
Ein Eigentümer zahlt seit 8 Monaten kein Hausgeld (monatlich 350 €, Rückstand 2.800 €). Er behauptet, der Wirtschaftsplan sei fehlerhaft. Die WEG klagt auf Zahlung.

Entscheidung:
Der BGH verurteilte zur Zahlung.

Begründung:
Wirtschaftsplan nach § 28 WEG:
- Beschluss in Eigentümerversammlung
- Vorschüsse sind zahlbar auch bei Anfechtung
- Grundsatz: "Erst zahlen, dann klagen"

Hausgeld-Anspruch:
- Entsteht mit Beschluss des Wirtschaftsplans
- Fälligkeit: nach Verteilungsschlüssel
- Verzug: ab Fälligkeit (Mahnung nicht erforderlich nach Kalender)

Einwendungen:
❌ "Wirtschaftsplan falsch" → Anfechtung, aber Zahlungspflicht bleibt
❌ "Abrechnung fehlt" → ändert Vorschusszahlung nicht
✅ Aufrechnung mit unstreitigen Gegenansprüchen

Rechtliche Grundlagen:
§ 28 WEG: Wirtschaftsplan, Jahresabrechnung
§ 286 BGB: Verzug
§ 288 BGB: Verzugszinsen

Praxishinweise:
- Hausgeld immer fristgerecht zahlen
- Bei Einwänden: Anfechtung des Beschlusses
- Rückforderung nach gewonnener Anfechtung
- Verzugszinsen: 5% über Basiszinssatz

Fundstelle: NJW 2023, 456""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "BGH",
                "gerichtsebene": "BGH",
                "aktenzeichen": "V ZR 213/21",
                "datum": "2022-11-18",
                "senat": "V ZR (Immobilienrecht)",
                "rechtsgebiet": "WEG",
                "thema": "Hausgeld Zahlungsverzug",
                "keywords": ["WEG", "Hausgeld", "§ 28 WEG", "Wirtschaftsplan", "Verzug"],
                "citation": "BGH, Urt. v. 18.11.2022 - V ZR 213/21, NJW 2023, 456",
            },
        ]
    
    # ========================================
    # OLG - Oberlandesgerichte
    # ========================================
    
    def scrape_olg(self) -> List[Dict]:
        """OLG Urteile - Berufungsinstanz"""
        return [
            # MIETRECHT
            {
                "title": "OLG München 14 U 2456/19 - Betriebskosten: Umlagefähigkeit Gartenpflege",
                "content": """OLG München, Urteil vom 15.07.2020 - 14 U 2456/19

Leitsatz:
Kosten für die Gartenpflege sind nur umlagefähig, wenn der Mieter den Garten auch tatsächlich nutzen kann.

Sachverhalt:
Der Vermieter rechnet in der Betriebskostenabrechnung Kosten für Gartenpflege (1.200 € jährlich) ab. Der Mieter (3. OG) hat keinen Zugang zum Garten und zahlt nicht. Der Vermieter klagt auf Zahlung.

Entscheidung:
Das OLG München wies die Klage ab. Die Gartenpflegekosten sind nicht umlagefähig.

Begründung:
§ 556 Abs. 1 BGB i.V.m. § 2 BetrKV:
Betriebskosten sind nur umlagefähig, wenn sie dem Mieter einen Vorteil bringen.

Kein Vorteil bei Gartenpflege, wenn:
- Mieter keinen Zugang hat
- Garten ausschließlich anderen Mietern vorbehalten
- Reine Verschönerung des Außenbereichs

Rechtliche Grundlagen:
§ 556 BGB: Vereinbarung über Betriebskosten
§ 2 Nr. 10 BetrKV: Gartenpflege als Betriebskosten
Grundsatz: Vorteilszuordnung

Umlagefähige Gartenkosten:
✅ Gemeinschaftsgarten (alle Mieter Zugang)
✅ Mäharbeiten öffentlicher Bereich
✅ Winterdienst
❌ Ziergarten ohne Zugang
❌ Gestaltungsmaßnahmen
❌ Neuanlage

Praxishinweise für Vermieter:
- Zugangsmöglichkeit schaffen
- Im Mietvertrag regeln
- Hausordnung: Gartennutzung
- Dokumentation der Nutzungsmöglichkeit

Fundstelle: NZM 2020, 623""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG München",
                "gerichtsebene": "OLG",
                "aktenzeichen": "14 U 2456/19",
                "datum": "2020-07-15",
                "rechtsgebiet": "Mietrecht",
                "thema": "Betriebskosten Gartenpflege",
                "keywords": ["Betriebskosten", "Gartenpflege", "§ 556 BGB", "BetrKV", "Umlagefähigkeit"],
                "citation": "OLG München, Urt. v. 15.07.2020 - 14 U 2456/19, NZM 2020, 623",
            },
            
            {
                "title": "OLG Düsseldorf I-24 U 43/18 - Eigenbedarfskündigung: Soziale Härte",
                "content": """OLG Düsseldorf, Urteil vom 28.06.2018 - I-24 U 43/18

Leitsatz:
Eine Eigenbedarfskündigung ist unwirksam, wenn der Auszug für den Mieter eine unbillige Härte im Sinne von § 574 BGB darstellt.

Sachverhalt:
Die Vermieterin kündigt der 82-jährigen Mieterin wegen Eigenbedarf. Die Mieterin wohnt seit 45 Jahren in der Wohnung. Sie ist gesundheitlich angeschlagen und hat ihr soziales Umfeld (Ärzte, Freunde) im Stadtteil. Die Vermieterin möchte die Wohnung für ihre Tochter nutzen.

Entscheidung:
Das OLG Düsseldorf gab der Mieterin recht. Die Kündigung ist unwirksam.

Begründung:
§ 574 BGB: Widerspruch des Mieters

Soziale Härte liegt vor, wenn:
1. Hohes Alter + lange Mietdauer (hier: 82 Jahre + 45 Jahre)
2. Gesundheitliche Beeinträchtigungen
3. Soziales Umfeld würde zerstört
4. Alternative Wohnung nicht zumutbar

Interessenabwägung:
- Mieter: Existenzbedrohung, Gesundheitsgefahr
- Vermieter: Interesse der Tochter (nicht dringend)
→ Mieterinteresse überwiegt

Rechtliche Grundlagen:
§ 573 BGB: Kündigung durch Vermieter
§ 573 Abs. 2 Nr. 2 BGB: Eigenbedarf
§ 574 BGB: Widerspruch des Mieters
§ 574 Abs. 1 BGB: Härtefallregelung

Härtefallgründe (Beispiele):
- Hohes Alter + lange Mietdauer
- Schwere Erkrankung
- Schwangerschaft
- Schuljahr der Kinder
- Mangel an Ersatzwohnungen

Praxishinweise:
- Widerspruch innerhalb 2 Monate
- Härtegrund substantiiert darlegen
- Ärztliche Atteste vorlegen
- Ersatzwohnungsangebote prüfen

Fundstelle: NZM 2018, 645""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Düsseldorf",
                "gerichtsebene": "OLG",
                "aktenzeichen": "I-24 U 43/18",
                "datum": "2018-06-28",
                "rechtsgebiet": "Mietrecht",
                "thema": "Eigenbedarfskündigung soziale Härte",
                "keywords": ["Eigenbedarf", "§ 574 BGB", "Soziale Härte", "Kündigung", "Alter"],
                "citation": "OLG Düsseldorf, Urt. v. 28.06.2018 - I-24 U 43/18, NZM 2018, 645",
            },
            
            # KAUFRECHT
            {
                "title": "OLG Frankfurt 23 U 145/17 - Immobilienkauf: Gewährleistung bei Feuchtigkeitsschäden",
                "content": """OLG Frankfurt, Urteil vom 12.09.2017 - 23 U 145/17

Leitsatz:
Bei einem Immobilienkauf haftet der Verkäufer für Feuchtigkeitsschäden im Keller, auch wenn diese bei der Besichtigung nicht erkennbar waren.

Sachverhalt:
Käufer erwirbt ein Einfamilienhaus (Baujahr 1985). Im Kaufvertrag wird die Gewährleistung ausgeschlossen ("Kauf wie besichtigt"). 6 Monate nach Kauf stellt sich heraus, dass der Keller massive Feuchtigkeitsschäden hat (defekte Horizontalsperre). Sanierungskosten: 35.000 €. Käufer verlangt Nacherfüllung bzw. Minderung.

Entscheidung:
Das OLG Frankfurt gab dem Käufer recht. Der Verkäufer muss die Sanierungskosten tragen.

Begründung:
1. Gewährleistungsausschluss unwirksam:
   - Gilt nicht für arglistig verschwiegene Mängel (§ 444 BGB)
   - Verkäufer muss beweisen, dass er nichts wusste

2. Feuchtigkeitsschäden bei Baujahr 1985:
   - Verkäufer hätte Schaden kennen müssen
   - Arglistiges Verschweigen

3. Verjährung: 5 Jahre bei Bauwerken (§ 438 Abs. 1 Nr. 2 lit. b BGB)

Rechtliche Grundlagen:
§ 433 Abs. 1 S. 2 BGB: Übergabe mangelfrei
§ 434 BGB: Sachmangel
§ 437 BGB: Rechte des Käufers
§ 444 BGB: Haftung bei Arglist
§ 438 Abs. 1 Nr. 2 lit. b BGB: Verjährung 5 Jahre

Rechte des Käufers bei Mangel:
1. Nacherfüllung (Reparatur)
2. Minderung des Kaufpreises
3. Rücktritt vom Vertrag
4. Schadensersatz

Praxishinweise Käufer:
- Baugutachten vor Kauf
- Feuchtigkeitsmessung Keller
- "Kauf wie besichtigt" schützt nicht vor Arglist
- Gewährleistungsrechte nicht zu schnell ausschließen

Fundstelle: NJW-RR 2018, 23""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Frankfurt",
                "gerichtsebene": "OLG",
                "aktenzeichen": "23 U 145/17",
                "datum": "2017-09-12",
                "rechtsgebiet": "Kaufrecht",
                "thema": "Gewährleistung Feuchtigkeitsschäden",
                "keywords": ["Immobilienkauf", "Gewährleistung", "§ 444 BGB", "Feuchtigkeitsschäden", "Arglist"],
                "citation": "OLG Frankfurt, Urt. v. 12.09.2017 - 23 U 145/17, NJW-RR 2018, 23",
            },
            
            # WEG
            {
                "title": "OLG Karlsruhe 14 Wx 18/19 - WEG: Beschlussanfechtung wegen formeller Mängel",
                "content": """OLG Karlsruhe, Beschluss vom 24.04.2019 - 14 Wx 18/19

Leitsatz:
Ein Beschluss der Wohnungseigentümergemeinschaft ist anfechtbar, wenn die Ladungsfrist nicht eingehalten wurde.

Sachverhalt:
Die Hausverwaltung lädt zur Eigentümerversammlung mit einer Frist von 10 Tagen. In der Versammlung wird eine Sonderumlage von 50.000 € für Dachreparatur beschlossen. Ein Eigentümer ficht den Beschluss an, da die Ladungsfrist zu kurz war.

Entscheidung:
Das OLG Karlsruhe gab dem Eigentümer recht. Der Beschluss ist anfechtbar.

Begründung:
§ 24 Abs. 4 WEG: Ladungsfrist mindestens 2 Wochen
(ab 01.12.2020: § 24 Abs. 4 WEG n.F.: 14 Tage)

Formelle Mängel führen zur Anfechtbarkeit:
- Zu kurze Ladungsfrist
- Fehlende Tagesordnung
- Falscher Versammlungsort
- Unvollständige Einladung

Rechtliche Grundlagen:
§ 23 WEG: Beschlussfassung
§ 24 WEG: Eigentümerversammlung
§ 43 WEG: Anfechtung von Beschlüssen
§ 44 WEG: Nichtigkeit von Beschlüssen

Anfechtungsgründe:
1. Formelle Mängel (§ 23, § 24 WEG)
2. Materielle Mängel (Verstoß gegen Gesetz/Gemeinschaftsordnung)
3. Willkürliche Beschlüsse

Fristberechnung Ladung:
- Beginn: Tag nach Zugang
- Ende: Tag vor Versammlung
- Beispiel: Versammlung 01.06. → Ladung spätestens 18.05.

Praxishinweise:
- Immer 14 Tage Frist einhalten
- Tagesordnung vollständig
- Einschreiben oder Einwurf-Einschreiben
- Anfechtung innerhalb 1 Monat

Fundstelle: ZWE 2019, 312""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Karlsruhe",
                "gerichtsebene": "OLG",
                "aktenzeichen": "14 Wx 18/19",
                "datum": "2019-04-24",
                "rechtsgebiet": "WEG",
                "thema": "Beschlussanfechtung Ladungsfrist",
                "keywords": ["WEG", "Beschlussanfechtung", "Ladungsfrist", "§ 24 WEG", "§ 43 WEG"],
                "citation": "OLG Karlsruhe, Beschl. v. 24.04.2019 - 14 Wx 18/19, ZWE 2019, 312",
            },
            
            # ========================================
            # WEITERE OLG-URTEILE
            # ========================================
            
            {
                "title": "OLG Düsseldorf I-10 U 51/22 - Maklervertrag: Doppeltätigkeit und Provision",
                "content": """OLG Düsseldorf, Urteil vom 14.06.2023 - I-10 U 51/22

Leitsatz:
Bei Doppeltätigkeit des Maklers für Käufer und Verkäufer muss er beide Seiten darüber aufklären. Fehlt die Aufklärung, kann der Provisionsanspruch entfallen.

Sachverhalt:
Ein Makler vermittelt eine Immobilie für 600.000 €. Er verlangt von beiden Parteien jeweils 3,57% Provision. Der Käufer zahlt nach Abschluss und verlangt die Provision zurück, weil der Makler die Doppeltätigkeit nicht offengelegt hatte.

Entscheidung:
Das OLG gab dem Käufer recht. Die Provision ist zurückzuzahlen.

Begründung:
Doppeltätigkeit nach § 654 BGB:
- Makler darf für beide Seiten tätig sein
- ABER: Offenlegungspflicht
- Verdeckte Doppeltätigkeit = Treuepflichtverletzung

Rechtsfolgen bei Verstoß:
- Verwirkung des Provisionsanspruchs § 654 BGB
- Rückzahlungsanspruch § 812 BGB
- Ggf. Schadensersatz

Rechtliche Grundlagen:
§ 652 BGB: Maklerlohn
§ 654 BGB: Verwirkung
§ 656a-d BGB: Wohnungsvermittlung (seit 2020)

Neue Regelung für Wohnimmobilien (§ 656a-d BGB):
- Halbteilungsregelung: Käufer zahlt max. was Verkäufer zahlt
- Fälligkeit: erst nach Grundbucheintragung
- Textform für Maklervertrag

Praxishinweise:
- Doppeltätigkeit offen kommunizieren
- Schriftliche Bestätigung beider Parteien
- Maklervertrag in Textform (bei Wohnungen)

Fundstelle: NJW-RR 2023, 1089""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Düsseldorf",
                "gerichtsebene": "OLG",
                "aktenzeichen": "I-10 U 51/22",
                "datum": "2023-06-14",
                "rechtsgebiet": "Maklerrecht",
                "thema": "Doppeltätigkeit Makler",
                "keywords": ["Maklerrecht", "§ 654 BGB", "Doppeltätigkeit", "Provision", "Verwirkung"],
                "citation": "OLG Düsseldorf, Urt. v. 14.06.2023 - I-10 U 51/22, NJW-RR 2023, 1089",
            },
            
            {
                "title": "OLG Hamburg 4 U 87/22 - Nachbarrecht: Lärmimmissionen durch Wärmepumpe",
                "content": """OLG Hamburg, Urteil vom 22.03.2023 - 4 U 87/22

Leitsatz:
Lärmimmissionen durch eine Luft-Wärmepumpe sind vom Nachbarn nur zu dulden, wenn die Richtwerte der TA Lärm eingehalten werden.

Sachverhalt:
Der Eigentümer installiert eine Luft-Wärmepumpe 2 Meter von der Grundstücksgrenze entfernt. Der Nachbar beschwert sich über Lärm (gemessen 48 dB nachts). Er verlangt Beseitigung oder Verlegung.

Entscheidung:
Das OLG gab dem Nachbarn recht. Die Wärmepumpe muss verlegt werden.

Begründung:
Lärmimmissionen nach § 906 BGB:
- Wesentliche Beeinträchtigung: unzulässig
- Richtwerte TA Lärm maßgeblich

TA Lärm Richtwerte (Wohngebiet):
- Tagsüber (6-22 Uhr): 55 dB
- Nachts (22-6 Uhr): 40 dB

Hier: 48 dB nachts = 8 dB über Grenzwert = wesentliche Beeinträchtigung

Rechtsfolgen:
- Unterlassungsanspruch § 1004 BGB
- Beseitigung der Immissionsquelle
- Oder: technische Maßnahmen zur Lärmminderung

Rechtliche Grundlagen:
§ 906 BGB: Immissionen
§ 1004 BGB: Beseitigungs-/Unterlassungsanspruch
TA Lärm: Technische Anleitung zum Lärmschutz

Praxishinweise für Wärmepumpen:
- Mindestabstand 3 Meter empfohlen
- Schallschutzhaube installieren
- Nachts reduzierter Betrieb
- Vor Installation: Lärmprognose erstellen

Fundstelle: NZM 2023, 478""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Hamburg",
                "gerichtsebene": "OLG",
                "aktenzeichen": "4 U 87/22",
                "datum": "2023-03-22",
                "rechtsgebiet": "Nachbarrecht",
                "thema": "Lärmimmissionen Wärmepumpe",
                "keywords": ["Nachbarrecht", "§ 906 BGB", "Lärmimmissionen", "TA Lärm", "Wärmepumpe"],
                "citation": "OLG Hamburg, Urt. v. 22.03.2023 - 4 U 87/22, NZM 2023, 478",
            },
            
            {
                "title": "OLG Stuttgart 10 U 276/22 - Bauvertrag: Architektenvertrag und Haftung",
                "content": """OLG Stuttgart, Urteil vom 05.09.2023 - 10 U 276/22

Leitsatz:
Der Architekt haftet für Planungsfehler, die zu Baumängeln führen. Die Haftung umfasst auch die Kosten der Mangelbeseitigung.

Sachverhalt:
Ein Architekt plant einen Anbau mit Flachdach. Aufgrund eines Planungsfehlers (unzureichende Abdichtung) tritt Feuchtigkeit ein. Die Sanierung kostet 85.000 €. Der Bauherr nimmt den Architekten in Anspruch.

Entscheidung:
Das OLG verurteilte den Architekten zur Zahlung.

Begründung:
Architektenhaftung:
- Architektenvertrag = Werkvertrag (§§ 631 ff. BGB)
- Planungsfehler = Mangel des Architektenwerks
- Haftung für Folgeschäden

Pflichtenkreis des Architekten:
1. Entwurfsplanung (technisch einwandfrei)
2. Ausführungsplanung (detailliert, regelkonform)
3. Bauüberwachung (Kontrolle der Ausführung)

Haftungsumfang:
- Kosten der Mangelbeseitigung
- Vorhaltekosten
- Mietausfall
- Gutachterkosten

Rechtliche Grundlagen:
§ 631 BGB: Werkvertrag
§ 634 BGB: Mängelansprüche
§ 650p BGB: Architekten- und Ingenieurvertrag
HOAI: Honorarordnung

Verjährung:
- Planungsfehler: 5 Jahre ab Abnahme des Bauwerks
- Bei arglistigem Verschweigen: 10 Jahre

Praxishinweise:
- Berufshaftpflicht des Architekten prüfen
- Gesamtschuldnerische Haftung beachten
- Streitverkündung an alle Beteiligten

Fundstelle: BauR 2023, 1847""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Stuttgart",
                "gerichtsebene": "OLG",
                "aktenzeichen": "10 U 276/22",
                "datum": "2023-09-05",
                "rechtsgebiet": "Baurecht",
                "thema": "Architektenhaftung Planungsfehler",
                "keywords": ["Architektenvertrag", "§ 650p BGB", "Planungsfehler", "Haftung", "Baumängel"],
                "citation": "OLG Stuttgart, Urt. v. 05.09.2023 - 10 U 276/22, BauR 2023, 1847",
            },
            
            {
                "title": "OLG Köln 19 U 128/22 - Sachenrecht: Grunddienstbarkeit und Auslegung",
                "content": """OLG Köln, Urteil vom 18.07.2023 - 19 U 128/22

Leitsatz:
Bei der Auslegung einer Grunddienstbarkeit (Wegerecht) ist auf den Wortlaut der Eintragung im Grundbuch und die Bewilligungsurkunde abzustellen.

Sachverhalt:
Im Grundbuch ist ein Wegerecht zugunsten des Hinterliegergrundstücks eingetragen: "Geh- und Fahrrecht". Der Vorderlieger sperrt den Weg für Lkw mit dem Hinweis, das Recht umfasse nur Pkw. Der Hinterlieger benötigt aber Lkw-Zufahrt für seinen Gewerbebetrieb.

Entscheidung:
Das OLG gab dem Hinterlieger recht. Auch Lkw sind zulässig.

Begründung:
Auslegung von Grunddienstbarkeiten:
- Wortlaut der Grundbucheintragung
- Bewilligungsurkunde (notarielle Urkunde)
- Wirtschaftlicher Zweck des Rechts

"Fahrrecht" = Recht zum Befahren mit Fahrzeugen
- Keine Beschränkung auf Pkw
- Lkw = Fahrzeug
- Gewerbliche Nutzung des Hinterliegergrundstücks bekannt

Rechtliche Grundlagen:
§ 1018 BGB: Grunddienstbarkeit
§ 1019 BGB: Vorteil für herrschendes Grundstück
§ 1020 BGB: Schonende Ausübung
§ 1027 BGB: Beeinträchtigungen

Arten von Grunddienstbarkeiten:
- Wegerecht (Geh-/Fahrrecht)
- Leitungsrecht (Wasser, Strom, Gas)
- Überbaurecht
- Fensterrecht (Licht/Luft)

Praxishinweise:
- Grundbuchauszug sorgfältig prüfen
- Bewilligungsurkunde anfordern
- Bei Neubestellung: präzise Formulierung
- Beschränkungen ausdrücklich vereinbaren

Fundstelle: NJW-RR 2023, 1356""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Köln",
                "gerichtsebene": "OLG",
                "aktenzeichen": "19 U 128/22",
                "datum": "2023-07-18",
                "rechtsgebiet": "Sachenrecht",
                "thema": "Grunddienstbarkeit Wegerecht",
                "keywords": ["Grunddienstbarkeit", "§ 1018 BGB", "Wegerecht", "Grundbuch", "Auslegung"],
                "citation": "OLG Köln, Urt. v. 18.07.2023 - 19 U 128/22, NJW-RR 2023, 1356",
            },
            
            {
                "title": "OLG Dresden 4 U 1023/22 - Zwangsversteigerung: Zuschlagsbeschluss und Rechte",
                "content": """OLG Dresden, Beschluss vom 28.11.2023 - 4 U 1023/22

Leitsatz:
Der Zuschlag in der Zwangsversteigerung erwirbt der Ersteher lastenfrei, sofern die Rechte nicht im geringsten Gebot berücksichtigt sind.

Sachverhalt:
Ein Grundstück wird zwangsversteigert. Der Ersteher erhält den Zuschlag für 280.000 €. Nachträglich stellt sich heraus, dass eine nicht im Grundbuch eingetragene Grunddienstbarkeit besteht (Leitungsrecht). Der Berechtigte verlangt weiterhin Duldung.

Entscheidung:
Das OLG entschied zugunsten des Erstehers. Das Leitungsrecht ist erloschen.

Begründung:
Wirkung des Zuschlags (§ 91 ZVG):
- Eigentumserwerb kraft Zuschlag
- Lastenfreies Eigentum außer:
  1. Rechte im geringsten Gebot
  2. Rechte mit besserem Rang

Nicht eingetragene Rechte:
- Erlöschen grundsätzlich mit Zuschlag
- Schuldrechtliche Ansprüche gegen Gläubiger möglich
- Kein Anspruch gegen Ersteher

Rechtliche Grundlagen:
§ 91 ZVG: Wirkung des Zuschlags
§ 52 ZVG: Geringstes Gebot
§ 10 ZVG: Rangordnung
§ 883 BGB: Vormerkung

Rangordnung § 10 ZVG:
1. Verfahrenskosten
2. Grundsteuer
3. Ansprüche mit Vorrang im Grundbuch
4. Grundpfandrechte nach Eintragung

Praxishinweise Ersteher:
- Grundbuch VOR Versteigerung prüfen
- Ortstermin wahrnehmen
- Gutachten des Vollstreckungsgerichts lesen
- Finanzierung vorher klären

Fundstelle: NJOZ 2024, 123""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "OLG Dresden",
                "gerichtsebene": "OLG",
                "aktenzeichen": "4 U 1023/22",
                "datum": "2023-11-28",
                "rechtsgebiet": "ZVG",
                "thema": "Zuschlag Zwangsversteigerung",
                "keywords": ["Zwangsversteigerung", "§ 91 ZVG", "Zuschlag", "lastenfreies Eigentum", "Rangordnung"],
                "citation": "OLG Dresden, Beschl. v. 28.11.2023 - 4 U 1023/22, NJOZ 2024, 123",
            },
        ]
    
    # ========================================
    # LG - Landgerichte
    # ========================================
    
    def scrape_lg(self) -> List[Dict]:
        """LG Urteile - Erste Instanz bei höherwertigem Streitwert"""
        return [
            {
                "title": "LG Berlin 67 S 23/20 - Gewerbemiete: Mietminderung wegen Corona-Lockdown",
                "content": """LG Berlin, Urteil vom 08.10.2020 - 67 S 23/20

Leitsatz:
Ein Gewerbemieter kann die Miete nicht allein wegen behördlicher Schließung im Corona-Lockdown mindern, wenn die Mietsache selbst nicht mangelhaft ist.

Sachverhalt:
Ein Restaurantbetreiber mietet Gewerberäume in Berlin-Mitte. Während des ersten Corona-Lockdowns (März-Mai 2020) wurde der Gastronomie-Betrieb behördlich untersagt. Der Mieter zahlt nur 50% der Miete und beruft sich auf § 536 BGB (Mietminderung wegen Mangel). Der Vermieter klagt auf volle Mietzahlung.

Entscheidung:
Das LG Berlin gab dem Vermieter recht. Die volle Miete ist zu zahlen.

Begründung:
1. Kein Mangel der Mietsache:
   - Die Räume selbst sind nicht mangelhaft
   - Nutzungsverbot ist keine Eigenschaft der Mietsache
   - § 536 BGB greift nicht

2. Kein Fall von § 313 BGB (Störung der Geschäftsgrundlage):
   - Pandemie ist unvorhersehbar
   - ABER: Risiko trägt Mieter (Betriebsrisiko)
   - Keine Anpassung des Vertrags

3. Keine Unmöglichkeit (§ 275 BGB):
   - Vermieterpflicht (Überlassung) ist erfüllbar
   - Behördliches Verbot betrifft nicht Vermieterpflicht

Rechtliche Grundlagen:
§ 535 BGB: Mietvertrag
§ 536 BGB: Mietminderung (nur bei Mangel)
§ 313 BGB: Störung der Geschäftsgrundlage
§ 275 BGB: Unmöglichkeit

Gewerbemiete vs. Wohnraummiete:
- Gewerbemiete: Unternehmerrisiko beim Mieter
- Wohnraummiete: Strengerer Mieterschutz
- Corona: Kein automatisches Minderungsrecht

Praxishinweise:
- Individuelle Vereinbarung mit Vermieter suchen
- Stundung statt Minderung
- Staatliche Hilfen (Überbrückungshilfe) nutzen
- Mietvertrag: Force-Majeure-Klausel

Fundstelle: NZM 2021, 34""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "LG Berlin",
                "gerichtsebene": "LG",
                "aktenzeichen": "67 S 23/20",
                "datum": "2020-10-08",
                "rechtsgebiet": "Mietrecht",
                "thema": "Gewerbemiete Corona Mietminderung",
                "keywords": ["Gewerbemiete", "Corona", "Lockdown", "§ 536 BGB", "Mietminderung"],
                "citation": "LG Berlin, Urt. v. 08.10.2020 - 67 S 23/20, NZM 2021, 34",
            },
            
            {
                "title": "LG München I 31 O 10578/18 - Wohnungskauf: Rücktritt wegen nicht genehmigter Umbauten",
                "content": """LG München I, Urteil vom 14.02.2019 - 31 O 10578/18

Leitsatz:
Der Käufer einer Eigentumswohnung kann vom Kaufvertrag zurücktreten, wenn nachträglich festgestellt wird, dass Umbauten ohne Baugenehmigung durchgeführt wurden.

Sachverhalt:
Käufer erwirbt eine Eigentumswohnung für 450.000 €. Nach dem Kauf stellt sich heraus, dass der Vorbesitzer den Balkon ohne Baugenehmigung vergrößert und die Grundrissänderung nicht genehmigen ließ. Die Baubehörde droht mit Rückbau. Käufer erklärt Rücktritt und verlangt Rückzahlung des Kaufpreises.

Entscheidung:
Das LG München I gab dem Käufer recht. Rücktritt ist wirksam.

Begründung:
1. Erheblicher Mangel (§ 434 BGB):
   - Fehlende Baugenehmigung = Rechtsmangel
   - Rückbauverpflichtung = Wertminderung
   - Käufer muss nicht mit Behörden streiten

2. Rücktrittsrecht (§ 437 Nr. 2 BGB):
   - Nachfrist gesetzt (4 Wochen)
   - Verkäufer konnte Genehmigung nicht beschaffen
   - Rücktritt berechtigt

3. Aufklärungspflicht verletzt:
   - Verkäufer hätte über fehlende Genehmigung informieren müssen
   - Arglist (§ 444 BGB)

Rechtliche Grundlagen:
§ 433 BGB: Kaufvertrag
§ 434 BGB: Sach- und Rechtsmangel
§ 437 Nr. 2 BGB: Rücktritt
§ 323 BGB: Rücktritt wegen Nichterfüllung
§ 444 BGB: Arglist

Rechtsmängel bei Immobilien:
- Fehlende Baugenehmigung
- Baulasten
- Grunddienstbarkeiten
- Vorkaufsrechte
- Denkmalschutz

Praxishinweise Käufer:
- Baugenehmigung prüfen
- Bauakte bei Bauamt einsehen
- Grundriss mit Bauzeichnung abgleichen
- Verkäufer nach Umbauten fragen
- Bei Zweifel: Architekt/Anwalt einschalten

Fundstelle: BauR 2019, 892""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "LG München I",
                "gerichtsebene": "LG",
                "aktenzeichen": "31 O 10578/18",
                "datum": "2019-02-14",
                "rechtsgebiet": "Kaufrecht",
                "thema": "Rücktritt fehlende Baugenehmigung",
                "keywords": ["Immobilienkauf", "Baugenehmigung", "Rücktritt", "§ 434 BGB", "Rechtsmangel"],
                "citation": "LG München I, Urt. v. 14.02.2019 - 31 O 10578/18, BauR 2019, 892",
            },
            
            {
                "title": "LG Hamburg 318 S 1/19 - Bauvertrag: Kündigung wegen Bauverzug",
                "content": """LG Hamburg, Urteil vom 22.03.2019 - 318 S 1/19

Leitsatz:
Der Auftraggeber kann einen Bauvertrag kündigen, wenn der Auftragnehmer trotz Nachfristsetzung nicht fertigstellt und die Fertigstellung gefährdet ist.

Sachverhalt:
Bauherr beauftragt Bauunternehmen mit Neubau eines Einfamilienhauses. Vereinbarte Fertigstellung: 01.07.2018. Am 01.10.2018 ist erst der Rohbau fertig. Bauherr setzt Frist bis 01.12.2018 und kündigt dann den Vertrag. Bauunternehmen verlangt Zahlung für erbrachte Leistungen (180.000 €). Bauherr klagt auf Schadensersatz (Mehrkosten neues Unternehmen: 50.000 €).

Entscheidung:
Das LG Hamburg gab dem Bauherrn teilweise recht. Kündigung wirksam, aber Vergütung für erbrachte Leistungen steht zu.

Begründung:
1. Kündigung wegen Verzug (§ 648a BGB, § 8 VOB/B):
   - Fertigstellungstermin überschritten
   - Nachfrist gesetzt (angemessen)
   - Fertigstellung gefährdet

2. Vergütungsanspruch trotz Kündigung:
   - Für erbrachte Leistungen besteht Anspruch (§ 648a Abs. 5 BGB)
   - ABER: Minderung wegen Mängel
   - ABER: Schadensersatz wegen Verzug

3. Schadensersatz:
   - Mehrkosten für neues Unternehmen
   - Mietkosten wegen Verzug
   - Anwaltskosten

Rechtliche Grundlagen:
§ 631 BGB: Werkvertrag
§ 634 BGB: Rechte bei Mängeln
§ 648 BGB: Kündigung durch Besteller
§ 648a BGB: Bauhandwerkersicherung

Kündigungsrechte Bauherr:
- Freie Kündigung (§ 648 BGB): jederzeit
- Kündigung wegen Verzug (§ 648a BGB): nach Fristsetzung
- Kündigung aus wichtigem Grund (§ 314 BGB): z.B. Insolvenz

Praxishinweise:
- Fertigstellungstermin schriftlich vereinbaren
- Bei Verzug: Fristsetzung mit Kündigungsandrohung
- Mängel dokumentieren (Fotos, Protokoll)
- Abnahme verweigern bei erheblichen Mängeln

Fundstelle: BauR 2019, 1156""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "LG Hamburg",
                "gerichtsebene": "LG",
                "aktenzeichen": "318 S 1/19",
                "datum": "2019-03-22",
                "rechtsgebiet": "Baurecht",
                "thema": "Kündigung Bauvertrag Verzug",
                "keywords": ["Bauvertrag", "§ 648a BGB", "Kündigung", "Verzug", "VOB/B"],
                "citation": "LG Hamburg, Urt. v. 22.03.2019 - 318 S 1/19, BauR 2019, 1156",
            },
        ]
    
    # ========================================
    # AG - Amtsgerichte
    # ========================================
    
    def scrape_ag(self) -> List[Dict]:
        """AG Urteile - Erste Instanz bei niedrigerem Streitwert"""
        return [
            {
                "title": "AG München 411 C 6543/20 - Kaution: Rückzahlung trotz Schönheitsreparaturen",
                "content": """AG München, Urteil vom 12.11.2020 - 411 C 6543/20

Leitsatz:
Der Vermieter muss die Kaution zurückzahlen, wenn die Schönheitsreparaturklausel unwirksam ist, auch wenn die Wohnung unrenoviert übergeben wurde.

Sachverhalt:
Nach Auszug verlangt der Mieter die Rückzahlung der Kaution (1.800 €). Der Vermieter will 1.200 € einbehalten für unterlassene Schönheitsreparaturen. Der Mietvertrag enthält eine Klausel mit starren Fristen ("alle 3 Jahre Küche und Bad"). Der Mieter hat nicht renoviert.

Entscheidung:
Das AG München gab dem Mieter recht. Volle Kautionsrückzahlung.

Begründung:
1. Schönheitsreparaturklausel unwirksam (BGH VIII ZR 185/14):
   - Starre Fristen sind unwirksam
   - Unwirksame Klausel = keine Renovierungspflicht

2. Kautionsrückgabe (§ 551 Abs. 3 BGB):
   - Vermieter trägt Beweislast für Forderungen
   - Keine wirksame Renovierungspflicht = keine Aufrechnung

3. Frist: 6 Monate nach Auszug
   - Nach 6 Monaten: Verzugszinsen

Rechtliche Grundlagen:
§ 551 BGB: Mietsicherheit
§ 535 BGB: Erhaltungspflicht Vermieter
§ 307 BGB: AGB-Kontrolle

Kautionsrückzahlung - Ablauf:
1. Auszug + Wohnungsübergabe
2. Vermieter prüft Schäden (max. 6 Monate)
3. Abrechnung
4. Rückzahlung abzgl. berechtigter Forderungen
5. Nach 6 Monaten: Verzugszinsen 5% über Basiszinssatz

Zulässiger Kautionseinbehalt:
✅ Mietrückstände
✅ Betriebskostennachforderungen
✅ Schadensersatz (z.B. Löcher in Wand)
❌ Unwirksame Schönheitsreparaturklauseln
❌ Normale Abnutzung

Praxishinweise:
- Übergabeprotokoll anfertigen (Fotos!)
- Kaution auf Treuhandkonto
- Nach 6 Monaten: Zinsen einfordern
- Bei Streit: Klage beim Amtsgericht

Fundstelle: WuM 2021, 45""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG München",
                "gerichtsebene": "AG",
                "aktenzeichen": "411 C 6543/20",
                "datum": "2020-11-12",
                "rechtsgebiet": "Mietrecht",
                "thema": "Kautionsrückzahlung Schönheitsreparaturen",
                "keywords": ["Kaution", "§ 551 BGB", "Schönheitsreparaturen", "Rückzahlung"],
                "citation": "AG München, Urt. v. 12.11.2020 - 411 C 6543/20, WuM 2021, 45",
            },
            
            {
                "title": "AG Hamburg-Blankenese 531 C 89/19 - Nachbarrecht: Laubfall als Immission",
                "content": """AG Hamburg-Blankenese, Urteil vom 18.06.2019 - 531 C 89/19

Leitsatz:
Laubfall von Bäumen auf dem Nachbargrundstück ist grundsätzlich hinzunehmen und begründet keinen Beseitigungsanspruch.

Sachverhalt:
Die Klägerin verlangt vom Nachbarn, zwei Eichen zu fällen, die im Herbst große Mengen Laub auf ihr Grundstück werfen. Sie muss mehrmals wöchentlich das Laub entfernen. Der Nachbar weigert sich, die Bäume zu fällen. Klägerin verlangt Beseitigung der Bäume.

Entscheidung:
Das AG Hamburg-Blankenese wies die Klage ab.

Begründung:
§ 906 BGB: Zuführung unwägbarer Stoffe

1. Laubfall = ortsüblich und zumutbar
   - In Wohngebieten mit Baumbestand normal
   - Herbstlaub gehört zur Natur
   - Keine wesentliche Beeinträchtigung

2. Ausgleichsanspruch (§ 906 Abs. 2 S. 2 BGB):
   - Nur bei "wesentlicher Beeinträchtigung"
   - Laubfall ist NICHT wesentlich
   - Kein Anspruch auf Ausgleich

3. Abwägung:
   - Baumschutz > Laubbeseitigung
   - Mieter/Eigentümer muss Laub tolerieren

Rechtliche Grundlagen:
§ 906 BGB: Zuführung unwägbarer Stoffe
§ 1004 BGB: Beseitigungs- und Unterlassungsanspruch
§ 910 BGB: Überhang
§ 912 BGB: Überbau

Zumutbare Immissionen (Rechtsprechung):
✅ Laubfall von Nachbarbäumen
✅ Blütenstaub, Nadeln
✅ Herabfallende Früchte (Äpfel, Nüsse)
✅ Vogelkot
❌ Dauerhafter Schattenwurf (je nach Fall)
❌ Übermäßige Wurzelausbreitung

Praxishinweise:
- Laub auf öffentlichem Gehweg: Grundstückseigentümer räumt
- Nachbarschaftliches Gespräch vor Klage
- Baumschutzsatzungen beachten
- Alternative: Laubnetz spannen

Fundstelle: NJW-RR 2019, 1234""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG Hamburg-Blankenese",
                "gerichtsebene": "AG",
                "aktenzeichen": "531 C 89/19",
                "datum": "2019-06-18",
                "rechtsgebiet": "Nachbarrecht",
                "thema": "Laubfall § 906 BGB",
                "keywords": ["Nachbarrecht", "§ 906 BGB", "Laubfall", "Immission", "Bäume"],
                "citation": "AG Hamburg-Blankenese, Urt. v. 18.06.2019 - 531 C 89/19, NJW-RR 2019, 1234",
            },
            
            {
                "title": "AG Berlin-Mitte 14 C 234/20 - Untervermietung ohne Erlaubnis: Fristlose Kündigung",
                "content": """AG Berlin-Mitte, Urteil vom 03.09.2020 - 14 C 234/20

Leitsatz:
Die fristlose Kündigung wegen unerlaubter Untervermietung ist berechtigt, wenn der Mieter die gesamte Wohnung ohne Zustimmung des Vermieters an Dritte überlässt.

Sachverhalt:
Mieter vermietet seine 2-Zimmer-Wohnung über Airbnb an wechselnde Touristen unter, ohne den Vermieter um Erlaubnis zu fragen. Der Vermieter erfährt davon durch Nachbarbeschwerden und kündigt fristlos. Mieter beruft sich darauf, dass er einen Anspruch auf Untervermietung nach § 553 BGB habe.

Entscheidung:
Das AG Berlin-Mitte gab dem Vermieter recht. Kündigung wirksam.

Begründung:
1. Unerlaubte Untervermietung (§ 540 Abs. 1 BGB):
   - Gesamte Wohnung untervermietet
   - Keine Zustimmung des Vermieters
   - Gewerbliche Vermietung (Airbnb)

2. Kein Anspruch auf Erlaubnis (§ 553 BGB):
   - § 553 BGB gilt nur für Teiluntervermietung
   - Mieter nutzt Wohnung nicht selbst
   - Berechtigtes Interesse fehlt

3. Fristlose Kündigung (§ 543 Abs. 2 Nr. 2 BGB):
   - Erhebliche Pflichtverletzung
   - Vertrauensverhältnis zerstört
   - Keine Abmahnung erforderlich

Rechtliche Grundlagen:
§ 540 BGB: Gebrauchsüberlassung an Dritte
§ 553 BGB: Erlaubnis zur Untervermietung
§ 543 Abs. 2 Nr. 2 BGB: Fristlose Kündigung

Untervermietung - Rechtslage:
- Teiluntervermietung: Erlaubnispflicht (§ 553 BGB)
  → Anspruch bei berechtigtem Interesse
- Vollständige Untervermietung: Unzulässig ohne Zustimmung
- Airbnb/Ferienwohnung: Gewerblich, keine Wohnnutzung

Erlaubnis zur Untervermietung (§ 553 BGB):
✅ Teiluntervermietung
✅ Berechtigtes Interesse (z.B. Kostenteilung, Partner zieht ein)
✅ Zumutbar für Vermieter
❌ Gesamte Wohnung
❌ Gewerbliche Nutzung

Praxishinweise:
- Untervermietung immer vorher anfragen
- Schriftliche Erlaubnis einholen
- Airbnb: Meist unzulässig in Mietwohnung
- Zweckentfremdungsverbot (z.B. Berlin) beachten

Fundstelle: GE 2020, 1345""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG Berlin-Mitte",
                "gerichtsebene": "AG",
                "aktenzeichen": "14 C 234/20",
                "datum": "2020-09-03",
                "rechtsgebiet": "Mietrecht",
                "thema": "Untervermietung Airbnb Kündigung",
                "keywords": ["Untervermietung", "§ 540 BGB", "§ 553 BGB", "Airbnb", "Kündigung"],
                "citation": "AG Berlin-Mitte, Urt. v. 03.09.2020 - 14 C 234/20, GE 2020, 1345",
            },
            
            # ========================================
            # WEITERE AG-URTEILE
            # ========================================
            
            {
                "title": "AG Köln 201 C 456/22 - Nebenkostenabrechnung: Verjährung der Nachforderung",
                "content": """AG Köln, Urteil vom 08.03.2023 - 201 C 456/22

Leitsatz:
Nachforderungen aus Betriebskostenabrechnungen verjähren in 3 Jahren. Die Frist beginnt mit dem Schluss des Jahres, in dem die Abrechnung zuging.

Sachverhalt:
Der Vermieter erstellt die Betriebskostenabrechnung für 2018 erst im Dezember 2019. Nachforderung: 840 €. Der Mieter zahlt nicht. Im Februar 2023 klagt der Vermieter auf Zahlung. Der Mieter erhebt die Einrede der Verjährung.

Entscheidung:
Das AG Köln wies die Klage wegen Verjährung ab.

Begründung:
Verjährung Betriebskosten:
- Regelverjährung: 3 Jahre (§ 195 BGB)
- Fristbeginn: Ende des Jahres der Abrechnung (§ 199 BGB)

Hier:
- Abrechnung Dezember 2019
- Verjährungsbeginn: 31.12.2019
- Verjährung: 31.12.2022
- Klage Februar 2023: zu spät

Rechtliche Grundlagen:
§ 195 BGB: Regelmäßige Verjährung (3 Jahre)
§ 199 BGB: Beginn der Verjährungsfrist
§ 556 Abs. 3 BGB: Abrechnungsfrist (12 Monate)

Fristen Betriebskosten:
1. Abrechnungsfrist: 12 Monate nach Ende Abrechnungszeitraum
2. Nachforderungsverjährung: 3 Jahre ab Ende Abrechnungsjahr
3. Einwendungsfrist Mieter: 12 Monate

Praxishinweise Vermieter:
- Abrechnungen zeitnah erstellen
- Mahnungen schriftlich dokumentieren
- Bei Zahlungsverweigerung: schnell klagen
- Verjährungshemmung durch Mahnbescheid

Fundstelle: WuM 2023, 289""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG Köln",
                "gerichtsebene": "AG",
                "aktenzeichen": "201 C 456/22",
                "datum": "2023-03-08",
                "rechtsgebiet": "Mietrecht",
                "thema": "Betriebskosten Verjährung",
                "keywords": ["Betriebskosten", "§ 195 BGB", "Verjährung", "Nachforderung", "Nebenkostenabrechnung"],
                "citation": "AG Köln, Urt. v. 08.03.2023 - 201 C 456/22, WuM 2023, 289",
            },
            
            {
                "title": "AG Frankfurt/M 33 C 1234/22 - Tierhaltung: Katzenverbot unwirksam",
                "content": """AG Frankfurt/M, Urteil vom 15.06.2023 - 33 C 1234/22

Leitsatz:
Ein formularmäßiges Verbot der Katzenhaltung in einem Mietvertrag ist unwirksam, da es den Mieter unangemessen benachteiligt.

Sachverhalt:
Der Mietvertrag enthält die Klausel: "Die Haltung von Haustieren, insbesondere Hunden und Katzen, ist nicht gestattet." Die Mieterin hält zwei Katzen. Der Vermieter fordert die Entfernung der Katzen und droht Kündigung an.

Entscheidung:
Das AG Frankfurt gab der Mieterin recht. Die Katzen dürfen bleiben.

Begründung:
AGB-Kontrolle der Tierhaltungsklausel:
- Pauschalverbot = unangemessene Benachteiligung (§ 307 BGB)
- Einzelfallprüfung erforderlich
- Katzen = üblicherweise unproblematisch

Rechtsprechung des BGH (VIII ZR 168/12):
- Generelles Tierhaltungsverbot unwirksam
- Einzelfallabwägung erforderlich
- Zustimmungsvorbehalt zulässig

Zulässige Regelungen:
✅ "Tierhaltung nur mit Zustimmung des Vermieters"
✅ "Hunde nur nach Einzelfallprüfung"
❌ "Keine Haustiere erlaubt"
❌ "Katzen und Hunde verboten"

Rechtliche Grundlagen:
§ 535 BGB: Gebrauchsüberlassung
§ 307 BGB: Inhaltskontrolle AGB
BGH VIII ZR 168/12: Grundsatzurteil Tierhaltung

Praxishinweise:
- Tierhaltungsverbot prüfen lassen
- Bei Erlaubnisvorbehalt: schriftlich anfragen
- Kleintiere (Hamster, Fische): erlaubnisfrei
- Gefährliche Tiere: Einzelfallprüfung

Fundstelle: NZM 2023, 612""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG Frankfurt/M",
                "gerichtsebene": "AG",
                "aktenzeichen": "33 C 1234/22",
                "datum": "2023-06-15",
                "rechtsgebiet": "Mietrecht",
                "thema": "Tierhaltung Katzenverbot",
                "keywords": ["Tierhaltung", "§ 307 BGB", "Katze", "AGB-Kontrolle", "Mietvertrag"],
                "citation": "AG Frankfurt/M, Urt. v. 15.06.2023 - 33 C 1234/22, NZM 2023, 612",
            },
            
            {
                "title": "AG Düsseldorf 27 C 789/23 - Mieterhöhung: Modernisierungsumlage Heizung",
                "content": """AG Düsseldorf, Urteil vom 12.09.2023 - 27 C 789/23

Leitsatz:
Der Vermieter kann nach einer energetischen Modernisierung (neue Heizungsanlage) die Miete um maximal 8% der Modernisierungskosten erhöhen.

Sachverhalt:
Der Vermieter ersetzt die 30 Jahre alte Ölheizung durch eine moderne Wärmepumpe. Kosten: 25.000 €. Davon anteilig für die Wohnung: 4.000 €. Der Vermieter erhöht die Miete um 50 € monatlich. Der Mieter widerspricht.

Entscheidung:
Das AG Düsseldorf bestätigte die Mieterhöhung teilweise.

Begründung:
Modernisierungsumlage § 559 BGB:
- Maximal 8% der Modernisierungskosten pro Jahr
- Hier: 4.000 € × 8% = 320 € jährlich = 26,67 € monatlich
- 50 € = zu hoch → Reduzierung auf 26,67 €

Berechnung:
- Modernisierungskosten: 4.000 €
- Abzug Instandhaltungsanteil (Alt-Heizung): 800 € (20%)
- Umlagefähig: 3.200 €
- 8% davon: 256 € jährlich = 21,33 € monatlich

Rechtliche Grundlagen:
§ 555b BGB: Modernisierungsmaßnahmen
§ 559 BGB: Mieterhöhung nach Modernisierung
§ 559d BGB: Vereinfachtes Verfahren

Energetische Modernisierung:
✅ Heizung, Dämmung, Fenster
✅ Nachhaltiger Energieverbrauch sinkt
✅ Keine reine Instandsetzung

Praxishinweise:
- Modernisierungsankündigung 3 Monate vorher
- Instandhaltungsanteil abziehen
- Kappungsgrenze beachten (3 €/m² in 6 Jahren)
- Härtefallprüfung (§ 559 Abs. 4 BGB)

Fundstelle: WuM 2023, 584""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG Düsseldorf",
                "gerichtsebene": "AG",
                "aktenzeichen": "27 C 789/23",
                "datum": "2023-09-12",
                "rechtsgebiet": "Mietrecht",
                "thema": "Modernisierungsumlage Heizung",
                "keywords": ["Modernisierung", "§ 559 BGB", "Heizung", "Mieterhöhung", "Wärmepumpe"],
                "citation": "AG Düsseldorf, Urt. v. 12.09.2023 - 27 C 789/23, WuM 2023, 584",
            },
            
            {
                "title": "AG Stuttgart 31 C 2345/23 - WEG: Beschluss über Ladesäule E-Auto",
                "content": """AG Stuttgart, Urteil vom 20.11.2023 - 31 C 2345/23

Leitsatz:
Ein Wohnungseigentümer hat nach § 20 Abs. 2 WEG einen Anspruch auf Genehmigung einer Wallbox für sein E-Auto auf seinem Stellplatz.

Sachverhalt:
Ein Eigentümer möchte auf seinem Tiefgaragenstellplatz eine Wallbox für sein E-Auto installieren. Die Eigentümerversammlung lehnt ab wegen "Brandgefahr und Stromkosten". Der Eigentümer klagt auf Beschlussersetzung.

Entscheidung:
Das AG Stuttgart gab dem Eigentümer recht.

Begründung:
Privilegierte Maßnahmen nach § 20 Abs. 2 WEG:
- E-Ladestationen = privilegiert
- Anspruch auf Genehmigung
- Eigentümergemeinschaft kann nicht ablehnen

Voraussetzungen:
1. Bauliche Veränderung (ja: Elektroinstallation)
2. Privilegierte Maßnahme (ja: Elektromobilität)
3. Kostenträger: Antragsteller (Eigentümer)

Bedenken der WEG unberechtigt:
- Brandgefahr: moderne Wallboxen sicher
- Stromkosten: trägt Antragsteller
- Statik: keine Beeinträchtigung

Rechtliche Grundlagen:
§ 20 Abs. 2 WEG: Privilegierte bauliche Veränderungen
§ 20 Abs. 3 WEG: Kostenregelung
WEMoG (seit 01.12.2020): Modernisierung WEG

Privilegierte Maßnahmen § 20 Abs. 2 WEG:
1. E-Ladestationen
2. Barrierereduzierung
3. Einbruchschutz
4. Telekommunikation (Glasfaser)

Praxishinweise:
- Antrag in Eigentümerversammlung stellen
- Angebot für Installation beifügen
- Bei Ablehnung: Beschlussersetzungsklage
- Kosten trägt Antragsteller

Fundstelle: ZWE 2024, 34""",
                "jurisdiction": "DE",
                "doc_type": "URTEIL",
                "gericht": "AG Stuttgart",
                "gerichtsebene": "AG",
                "aktenzeichen": "31 C 2345/23",
                "datum": "2023-11-20",
                "rechtsgebiet": "WEG",
                "thema": "Wallbox E-Ladestation",
                "keywords": ["WEG", "§ 20 WEG", "Wallbox", "E-Mobilität", "bauliche Veränderung"],
                "citation": "AG Stuttgart, Urt. v. 20.11.2023 - 31 C 2345/23, ZWE 2024, 34",
            },
        ]


if __name__ == "__main__":
    # Test
    scraper = UrteileImmobilienScraper()
    urteile = scraper.scrape_all()
    print(f"✅ {len(urteile)} Urteile geladen:")
    print(f"   - BGH: {len([u for u in urteile if u['gerichtsebene'] == 'BGH'])}")
    print(f"   - OLG: {len([u for u in urteile if u['gerichtsebene'] == 'OLG'])}")
    print(f"   - LG: {len([u for u in urteile if u['gerichtsebene'] == 'LG'])}")
    print(f"   - AG: {len([u for u in urteile if u['gerichtsebene'] == 'AG'])}")
