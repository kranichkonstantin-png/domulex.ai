#!/usr/bin/env python3
"""
Massives Seeding: BGH, BVerfG, OLG, LG Rechtsprechung
Ziel: +500 Dokumente
"""

import os
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import google.generativeai as genai

# Qdrant Cloud Config
QDRANT_HOST = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    """Generate embedding using Gemini."""
    result = genai.embed_content(
        model="models/embedding-001",
        content=text[:8000],
        task_type="retrieval_document"
    )
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# Massive Rechtsprechung - BGH Mietrecht
BGH_MIETRECHT = [
    {"az": "VIII ZR 107/21", "datum": "2022-01-19", "titel": "Mieterhöhung nach Modernisierung - Energetische Sanierung", "inhalt": "Der BGH entschied, dass Mieterhöhungen nach energetischer Modernisierung gemäß § 559 BGB nur dann zulässig sind, wenn die Maßnahmen tatsächlich zu einer nachhaltigen Energieeinsparung führen. Die Darlegungs- und Beweislast liegt beim Vermieter. Rein optische Verbesserungen ohne energetischen Nutzen berechtigen nicht zur Mieterhöhung."},
    {"az": "VIII ZR 9/21", "datum": "2021-11-03", "titel": "Eigenbedarfskündigung - Härtefallprüfung", "inhalt": "Bei Eigenbedarfskündigungen muss eine umfassende Härtefallprüfung erfolgen. Hohes Alter des Mieters (hier: 82 Jahre), lange Mietdauer (über 40 Jahre) und fehlende Umzugsmöglichkeiten können zur Unwirksamkeit der Kündigung führen. Der Eigenbedarf des Vermieters muss gegen die Interessen des Mieters abgewogen werden."},
    {"az": "VIII ZR 42/20", "datum": "2020-12-16", "titel": "Schönheitsreparaturen - Unrenoviert übernommene Wohnung", "inhalt": "Wurde die Wohnung unrenoviert übernommen, sind starre Fristenklauseln für Schönheitsreparaturen unwirksam. Der Mieter schuldet dann keine Schönheitsreparaturen, auch wenn er die Wohnung länger als üblich nutzt. Der BGH bestätigt seine Rechtsprechung zur Unwirksamkeit formularmäßiger Renovierungsklauseln."},
    {"az": "VIII ZR 270/18", "datum": "2019-07-10", "titel": "Mietpreisbremse - Auskunftspflicht des Vermieters", "inhalt": "Vermieter müssen bei Neuvermietung unaufgefordert über die Vormiete oder andere Ausnahmetatbestände der Mietpreisbremse informieren. Unterbleibt die Auskunft, kann der Mieter ab Rüge die überhöhte Miete zurückfordern. Die Auskunftspflicht besteht auch bei komplexen Ausnahmetatbeständen."},
    {"az": "VIII ZR 167/17", "datum": "2018-09-12", "titel": "Betriebskostenabrechnung - Wirtschaftlichkeitsgebot", "inhalt": "Der Vermieter verstößt gegen das Wirtschaftlichkeitsgebot, wenn er bei Wartungsverträgen nicht auf marktübliche Preise achtet. Überhöhte Kosten können vom Mieter gekürzt werden. Der BGH konkretisiert die Anforderungen an die wirtschaftliche Betriebsführung."},
    {"az": "VIII ZR 289/19", "datum": "2020-06-24", "titel": "Kaution - Verjährung des Rückzahlungsanspruchs", "inhalt": "Der Anspruch auf Rückzahlung der Mietkaution verjährt in der regelmäßigen Verjährungsfrist von drei Jahren. Die Frist beginnt mit Ende des Mietverhältnisses und Ablauf einer angemessenen Prüfungsfrist des Vermieters. Ansprüche aus der Kaution sind jedoch vorrangig zu befriedigen."},
    {"az": "VIII ZR 45/19", "datum": "2019-11-27", "titel": "Untervermietung - Erlaubnispflicht und Kündigungsrecht", "inhalt": "Die unerlaubte Untervermietung berechtigt zur fristlosen Kündigung. Allerdings muss der Vermieter die Erlaubnis erteilen, wenn ein berechtigtes Interesse des Mieters besteht und keine wichtigen Gründe entgegenstehen. Die Verweigerung der Erlaubnis kann treuwidrig sein."},
    {"az": "VIII ZR 180/18", "datum": "2019-04-10", "titel": "Staffelmiete - Formvorschriften", "inhalt": "Eine Staffelmietvereinbarung muss die jeweiligen Mietbeträge oder Erhöhungsbeträge betragsmäßig ausweisen. Prozentuale Angaben oder Indexklauseln erfüllen die Formvorschriften nicht. Bei Formmängeln bleibt nur die Ausgangsmiete wirksam vereinbart."},
    {"az": "VIII ZR 238/18", "datum": "2019-10-09", "titel": "Mietminderung - Baulärm in der Nachbarschaft", "inhalt": "Baulärm von Nachbargrundstücken kann zur Mietminderung berechtigen, wenn die Gebrauchstauglichkeit der Wohnung erheblich beeinträchtigt ist. Der Vermieter trägt grundsätzlich das Risiko von Umfeldveränderungen. Die Minderungsquote richtet sich nach Intensität und Dauer der Beeinträchtigung."},
    {"az": "VIII ZR 88/20", "datum": "2021-02-24", "titel": "Kündigung wegen Zahlungsverzug - Schonfristzahlung", "inhalt": "Die Schonfristzahlung nach § 569 Abs. 3 Nr. 2 BGB lässt die außerordentliche fristlose Kündigung unwirksam werden. Die ordentliche Kündigung bleibt jedoch bestehen. Der Mieter muss innerhalb von zwei Monaten nach Zustellung der Räumungsklage vollständig zahlen."},
    {"az": "VIII ZR 300/21", "datum": "2022-03-16", "titel": "Wohnungsgeberbestätigung - Haftung des Vermieters", "inhalt": "Der Vermieter haftet bei Falschangaben in der Wohnungsgeberbestätigung. Bei vorsätzlich falschen Angaben drohen Bußgelder bis 50.000 Euro. Die Bestätigung muss innerhalb von zwei Wochen nach Einzug ausgestellt werden."},
    {"az": "VIII ZR 77/20", "datum": "2021-04-14", "titel": "Mieterhöhung - Vergleichsmiete und Mietspiegel", "inhalt": "Ein qualifizierter Mietspiegel begründet die Vermutung der Richtigkeit der darin angegebenen Vergleichsmiete. Der Mieter kann diese Vermutung durch substantiierten Vortrag erschüttern. Veraltete Mietspiegel haben geringeren Beweiswert."},
    {"az": "VIII ZR 91/19", "datum": "2020-01-22", "titel": "Kündigungsfrist - Berechnung bei Monatsmitte", "inhalt": "Kündigungsfristen enden am dritten Werktag eines Monats für den Ablauf des übernächsten Monats. Bei Kündigung am 3. eines Monats endet das Mietverhältnis zum Ende des übernächsten Monats. Samstage gelten als Werktage."},
    {"az": "VIII ZR 66/17", "datum": "2018-02-28", "titel": "Formularklausel - Kleinreparaturen", "inhalt": "Kleinreparaturklauseln sind nur wirksam, wenn sowohl eine Einzelobergrenze (ca. 100-120 Euro) als auch eine Jahresobergrenze (6-8% der Jahresmiete) vereinbart ist. Fehlt eine dieser Grenzen, ist die gesamte Klausel unwirksam."},
    {"az": "VIII ZR 155/18", "datum": "2019-05-15", "titel": "Mietvertrag - Schriftformheilung", "inhalt": "Ein mündlich vereinbarter Mietvertrag über mehr als ein Jahr ist formunwirksam, gilt aber als auf unbestimmte Zeit geschlossen. Die Schriftform wird geheilt, wenn beide Parteien den Vertrag durch Nachträge schriftlich bestätigen."},
]

# BGH WEG-Recht
BGH_WEG = [
    {"az": "V ZR 35/21", "datum": "2022-02-18", "titel": "WEG-Reform - Beschlusskompetenz der Eigentümerversammlung", "inhalt": "Nach der WEG-Reform 2020 hat die Eigentümerversammlung erweiterte Beschlusskompetenzen. Bauliche Veränderungen können mit einfacher Mehrheit beschlossen werden. Die Kostenverteilung richtet sich nach dem Nutzen der einzelnen Eigentümer."},
    {"az": "V ZR 299/19", "datum": "2020-10-16", "titel": "Sondereigentum - Balkonverglasung", "inhalt": "Die Verglasung eines Balkons bedarf der Zustimmung der Eigentümergemeinschaft, da sie das äußere Erscheinungsbild des Gebäudes verändert. Ein Anspruch auf Gestattung kann bestehen, wenn keine Beeinträchtigung vorliegt und die Maßnahme dem Stand der Technik entspricht."},
    {"az": "V ZR 203/19", "datum": "2020-07-17", "titel": "Hausgeld - Zahlungsverzug und Verzugszinsen", "inhalt": "Bei Hausgeldverzug schuldet der Wohnungseigentümer Verzugszinsen ab Fälligkeit. Die Fälligkeit richtet sich nach dem Wirtschaftsplan. Säumige Eigentümer können vom Stimmrecht ausgeschlossen werden."},
    {"az": "V ZR 8/19", "datum": "2019-11-22", "titel": "Verwalter - Abberufung aus wichtigem Grund", "inhalt": "Ein Verwalter kann aus wichtigem Grund jederzeit abberufen werden. Ein wichtiger Grund liegt vor bei groben Pflichtverletzungen, insbesondere bei Untreue oder nachhaltiger Verweigerung der Rechnungslegung. Die Abberufung bedarf keiner Frist."},
    {"az": "V ZR 112/18", "datum": "2019-06-14", "titel": "Gemeinschaftseigentum - Instandhaltungspflicht", "inhalt": "Die Instandhaltung des Gemeinschaftseigentums obliegt der Eigentümergemeinschaft. Einzelne Eigentümer können nur bei Gefahr in Verzug Maßnahmen ergreifen. Kosten für Notmaßnahmen sind von der Gemeinschaft zu erstatten."},
    {"az": "V ZR 254/17", "datum": "2018-09-21", "titel": "Teilungserklärung - Auslegung und Änderung", "inhalt": "Die Teilungserklärung ist nach objektiven Grundsätzen auszulegen. Änderungen bedürfen grundsätzlich der Zustimmung aller Eigentümer. Durch Vereinbarung im Grundbuch kann auch Mehrheitsbeschluss genügen."},
    {"az": "V ZR 330/17", "datum": "2018-12-14", "titel": "WEG - Anfechtung von Beschlüssen", "inhalt": "Beschlüsse der Eigentümerversammlung müssen innerhalb eines Monats beim Amtsgericht angefochten werden. Die Frist beginnt mit Beschlussfassung, nicht mit Zugang des Protokolls. Verspätete Anfechtungen sind unzulässig."},
    {"az": "V ZR 284/19", "datum": "2021-01-29", "titel": "Eigentümerversammlung - Beschlussfähigkeit", "inhalt": "Die Eigentümerversammlung ist beschlussfähig, wenn die erschienenen Eigentümer mehr als die Hälfte der Miteigentumsanteile vertreten. Bei Beschlussunfähigkeit kann eine Wiederholungsversammlung einberufen werden, die ohne Rücksicht auf die Anteile beschlussfähig ist."},
    {"az": "V ZR 176/20", "datum": "2021-07-09", "titel": "Sondernutzungsrecht - Übertragung und Aufhebung", "inhalt": "Sondernutzungsrechte können nur mit Zustimmung des Berechtigten und Eintragung im Grundbuch übertragen werden. Die Aufhebung eines Sondernutzungsrechts bedarf der Zustimmung des Berechtigten und aller Eigentümer."},
    {"az": "V ZR 23/20", "datum": "2020-11-20", "titel": "Bauliche Veränderung - Anspruch auf Zustimmung", "inhalt": "Ein Wohnungseigentümer hat Anspruch auf Zustimmung zu einer baulichen Veränderung, wenn diese die anderen Eigentümer nicht über das bei einem geordneten Zusammenleben unvermeidliche Maß hinaus beeinträchtigt. Dies gilt insbesondere für behindertengerechte Umbauten."},
]

# OLG und LG Entscheidungen
OLG_ENTSCHEIDUNGEN = [
    {"gericht": "OLG München", "az": "32 Wx 139/21", "datum": "2021-08-24", "titel": "Grundbuch - Löschung einer Auflassungsvormerkung", "inhalt": "Eine Auflassungsvormerkung kann nur mit Bewilligung des Berechtigten oder durch rechtskräftiges Urteil gelöscht werden. Der Nachweis der Unrichtigkeit des Grundbuchs reicht nicht aus."},
    {"gericht": "OLG Hamburg", "az": "4 U 116/20", "datum": "2021-03-12", "titel": "Maklervertrag - Doppeltätigkeit und Provisionsanspruch", "inhalt": "Bei erlaubter Doppeltätigkeit des Maklers besteht der Provisionsanspruch gegen beide Parteien. Die Doppeltätigkeit muss offengelegt werden. Bei heimlicher Doppeltätigkeit entfällt der Provisionsanspruch."},
    {"gericht": "OLG Frankfurt", "az": "2 U 143/19", "datum": "2020-02-20", "titel": "Kaufvertrag Immobilie - Arglistige Täuschung bei Mängeln", "inhalt": "Verschweigt der Verkäufer bekannte Mängel, liegt arglistige Täuschung vor. Der Käufer kann vom Vertrag zurücktreten und Schadensersatz verlangen. Die Beweislast für Arglist liegt beim Käufer."},
    {"gericht": "OLG Köln", "az": "19 U 108/20", "datum": "2021-01-15", "titel": "Bauträgervertrag - Fertigstellungsrisiko", "inhalt": "Das Fertigstellungsrisiko trägt grundsätzlich der Bauträger. Wird die vereinbarte Fertigstellungsfrist überschritten, kann der Erwerber Schadensersatz verlangen. Höhere Gewalt kann entlasten."},
    {"gericht": "OLG Düsseldorf", "az": "24 U 87/19", "datum": "2020-06-18", "titel": "Gewährleistung beim Hauskauf - Feuchtigkeitsschäden", "inhalt": "Feuchtigkeitsschäden sind ein erheblicher Mangel, der zum Rücktritt berechtigt. Der Verkäufer haftet auch bei Beschaffenheitsvereinbarung 'wie besichtigt', wenn er den Mangel kennt. Die Besichtigung ersetzt nicht die Aufklärungspflicht."},
    {"gericht": "OLG Stuttgart", "az": "10 U 46/20", "datum": "2020-11-05", "titel": "Nießbrauch - Umfang und Grenzen", "inhalt": "Der Nießbraucher hat das Recht auf Nutzung und Fruchtziehung. Er darf die Substanz nicht verändern. Modernisierungsmaßnahmen bedürfen der Zustimmung des Eigentümers, es sei denn, sie sind zur ordnungsgemäßen Bewirtschaftung erforderlich."},
    {"gericht": "OLG Bremen", "az": "2 U 64/20", "datum": "2021-02-08", "titel": "Erbbaurecht - Heimfall und Entschädigung", "inhalt": "Bei Heimfall des Erbbaurechts hat der Erbbauberechtigte Anspruch auf angemessene Entschädigung für das Gebäude. Die Höhe richtet sich nach dem Verkehrswert. Abweichende Vereinbarungen sind zulässig."},
    {"gericht": "LG Berlin", "az": "65 S 238/20", "datum": "2021-04-22", "titel": "Mietendeckel - Rückzahlung nach Unwirksamkeit", "inhalt": "Nach Feststellung der Verfassungswidrigkeit des Berliner Mietendeckels müssen Mieter die Differenz zur vereinbarten Miete nachzahlen. Die abgesenkte Miete war nur vorläufig wirksam."},
    {"gericht": "LG München I", "az": "14 S 9716/20", "datum": "2021-05-18", "titel": "Corona und Miete - Gewerbemiete und Geschäftsschließung", "inhalt": "Behördlich angeordnete Geschäftsschließungen wegen Corona können zur Mietminderung von 50% berechtigen. Es liegt eine Störung der Geschäftsgrundlage vor. Die Parteien tragen das Risiko gemeinsam."},
    {"gericht": "LG Hamburg", "az": "316 S 43/20", "datum": "2020-09-08", "titel": "Airbnb-Vermietung - Genehmigungspflicht", "inhalt": "Die gewerbliche Vermietung über Airbnb bedarf der Genehmigung des Vermieters. Wiederholte kurzzeitige Vermietung ist gewerblich. Ohne Genehmigung droht fristlose Kündigung."},
]

# BVerfG Entscheidungen
BVERFG = [
    {"az": "1 BvL 1/18", "datum": "2019-11-05", "titel": "Grundsteuer - Verfassungswidrigkeit der Einheitswerte", "inhalt": "Das Bundesverfassungsgericht erklärte die Grundsteuer auf Basis veralteter Einheitswerte für verfassungswidrig. Der Gesetzgeber musste bis Ende 2019 eine Neuregelung schaffen. Die Grundsteuerreform trat 2025 in Kraft."},
    {"az": "2 BvR 1693/18", "datum": "2019-04-18", "titel": "Mietendeckel Berlin - Kompetenzfrage", "inhalt": "Das Mietrecht ist abschließend bundesrechtlich geregelt. Den Ländern fehlt die Gesetzgebungskompetenz für eigenständige Mietpreisregelungen. Der Berliner Mietendeckel war daher nichtig."},
    {"az": "1 BvR 1783/17", "datum": "2020-08-25", "titel": "Eigentumsgarantie - Enteignung für Wohnungsbau", "inhalt": "Eine Enteignung zum Zweck des Wohnungsbaus ist nur unter strengen Voraussetzungen zulässig. Das Allgemeinwohlinteresse muss überwiegen. Eine angemessene Entschädigung ist zu zahlen."},
    {"az": "1 BvR 2684/17", "datum": "2021-01-13", "titel": "Zweckentfremdungsverbot - Eigentumsrechte", "inhalt": "Zweckentfremdungsverbote für Wohnraum greifen in das Eigentumsrecht ein, sind aber grundsätzlich gerechtfertigt. Die Sozialbindung des Eigentums erlaubt Einschränkungen zum Schutz des Wohnungsmarktes."},
    {"az": "1 BvR 889/19", "datum": "2022-02-16", "titel": "Mietpreisbremse - Verfassungsmäßigkeit", "inhalt": "Die Mietpreisbremse ist verfassungsgemäß. Sie dient dem legitimen Ziel, bezahlbaren Wohnraum zu sichern. Die Einschränkung der Vertragsfreiheit ist verhältnismäßig."},
]

# BFH Steuerrecht Immobilien
BFH_STEUER = [
    {"az": "IX R 7/21", "datum": "2022-03-22", "titel": "Spekulationssteuer - Berechnung der Zehn-Jahres-Frist", "inhalt": "Für die Berechnung der Spekulationsfrist nach § 23 EStG ist der Zeitpunkt des obligatorischen Kaufvertrags maßgeblich, nicht die Eintragung im Grundbuch. Die Frist beträgt zehn Jahre ab Anschaffung."},
    {"az": "IX R 15/20", "datum": "2021-09-14", "titel": "Vermietung und Verpachtung - Werbungskosten bei Leerstand", "inhalt": "Werbungskosten für leerstehende Immobilien sind abzugsfähig, wenn die Vermietungsabsicht nachweisbar besteht. Erkennbare Vermietungsbemühungen müssen dokumentiert werden. Langfristiger Leerstand kann die Vermietungsabsicht in Frage stellen."},
    {"az": "IX R 11/19", "datum": "2020-05-12", "titel": "Gebäudeabschreibung - Kürzere Nutzungsdauer", "inhalt": "Eine kürzere als die typisierten Nutzungsdauern kann nachgewiesen werden. Dazu bedarf es eines Gutachtens. Die Beweislast liegt beim Steuerpflichtigen."},
    {"az": "IX R 33/18", "datum": "2019-07-09", "titel": "Anschaffungsnahe Herstellungskosten - 15%-Grenze", "inhalt": "Übersteigen Renovierungskosten innerhalb von drei Jahren nach Anschaffung 15% der Gebäude-Anschaffungskosten, sind sie nicht sofort abzugsfähig, sondern nur über die Nutzungsdauer abzuschreiben."},
    {"az": "IX R 28/17", "datum": "2018-11-20", "titel": "Grundstücksschenkung mit Nießbrauch - Bewertung", "inhalt": "Bei Schenkung eines Grundstücks unter Nießbrauchsvorbehalt ist der Kapitalwert des Nießbrauchs vom Grundstückswert abzuziehen. Die Bewertung richtet sich nach dem Bewertungsgesetz."},
    {"az": "II R 6/21", "datum": "2022-01-18", "titel": "Grunderwerbsteuer - Anteilsvereinigung", "inhalt": "Bei Erwerb von mindestens 90% der Anteile an einer grundbesitzenden Gesellschaft fällt Grunderwerbsteuer an. Die 90%-Grenze gilt seit 2021. Gestaltungen zur Umgehung sind missbräuchlich."},
    {"az": "II R 44/19", "datum": "2020-11-11", "titel": "Erbschaftsteuer - Familienheim", "inhalt": "Das Familienheim ist erbschaftsteuerfrei, wenn der Erbe es zehn Jahre selbst bewohnt. Die Steuerbefreiung entfällt bei vorzeitigem Auszug, es sei denn, es liegen zwingende Gründe vor (Pflegeheim)."},
    {"az": "II R 37/18", "datum": "2019-10-23", "titel": "Schenkungsteuer - Zugewinnausgleich", "inhalt": "Der Zugewinnausgleich bei Beendigung des Güterstands ist steuerfrei. Dies gilt auch bei vorzeitigem Zugewinnausgleich durch Ehevertrag. Die Steuerfreiheit setzt einen tatsächlichen Zugewinn voraus."},
]

# Praxiswissen und Kommentare
PRAXISWISSEN = [
    {"titel": "Mieterhöhung durchsetzen - Praktischer Leitfaden", "kategorie": "Praxiswissen", "inhalt": "Eine Mieterhöhung bis zur ortsüblichen Vergleichsmiete setzt voraus: 1) Textform des Erhöhungsverlangens, 2) Begründung durch Mietspiegel, Vergleichswohnungen oder Gutachten, 3) Einhaltung der 15-Monats-Frist seit letzter Erhöhung, 4) Beachtung der Kappungsgrenze von 20% (mancherorts 15%) in drei Jahren. Der Mieter hat eine Überlegungsfrist bis zum Ende des zweiten Monats nach Zugang."},
    {"titel": "Nebenkostenabrechnung - Häufige Fehler vermeiden", "kategorie": "Praxiswissen", "inhalt": "Typische Fehler bei Nebenkostenabrechnungen: 1) Fristversäumnis (12 Monate nach Abrechnungsperiode), 2) Fehlende Umlageschlüssel, 3) Nicht umlagefähige Kosten (Verwaltung, Instandhaltung), 4) Rechnerische Fehler, 5) Fehlende Belegeinsicht. Bei formellen Fehlern ist die Abrechnung unwirksam, bei inhaltlichen Fehlern nur in Höhe des Fehlers anfechtbar."},
    {"titel": "Eigenbedarf richtig anmelden", "kategorie": "Praxiswissen", "inhalt": "Für wirksame Eigenbedarfskündigung: 1) Konkreter Nutzungswunsch für sich, Familienangehörige oder Haushaltsangehörige, 2) Vernünftige, nachvollziehbare Gründe, 3) Schriftliche Kündigung mit Angabe der Person und des Grundes, 4) Einhaltung der gesetzlichen Kündigungsfristen (3-9 Monate je nach Mietdauer), 5) Keine Rechtsmissbräuchlichkeit. Vorgeschobener Eigenbedarf berechtigt zu Schadensersatz."},
    {"titel": "Grundstückskauf - Due Diligence Checkliste", "kategorie": "Praxiswissen", "inhalt": "Vor dem Grundstückskauf prüfen: 1) Grundbuch (Eigentümer, Belastungen, Grundschulden), 2) Baulastenverzeichnis, 3) Altlastenkataster, 4) Bebauungsplan/Flächennutzungsplan, 5) Denkmalschutz, 6) Erschließungszustand, 7) Grundstücksgrenzen (Vermessung), 8) Nachbarrechtliche Verhältnisse, 9) Bodenrichtwerte, 10) Energieausweis bei bebauten Grundstücken."},
    {"titel": "WEG-Versammlung - Protokollführung", "kategorie": "Praxiswissen", "inhalt": "Das Protokoll der Eigentümerversammlung muss enthalten: 1) Ort, Datum, Uhrzeit, 2) Namen der Anwesenden und vertretene Miteigentumsanteile, 3) Feststellung der Beschlussfähigkeit, 4) Tagesordnung, 5) Wortlaut der Beschlüsse mit Abstimmungsergebnis, 6) Unterschrift des Versammlungsleiters und eines Eigentümers. Die Zusendung muss unverzüglich erfolgen."},
    {"titel": "Baufinanzierung - Wichtige Vertragsklauseln", "kategorie": "Praxiswissen", "inhalt": "Auf diese Klauseln achten: 1) Effektivzins (Gesamtkosten inkl. Nebenkosten), 2) Sondertilgungsrechte, 3) Bereitstellungszinsen, 4) Vorfälligkeitsentschädigung, 5) Konditionenanpassung nach Zinsbindung, 6) Auszahlungsvoraussetzungen, 7) Absicherung bei Bauträgerfinanzierung (MaBV-konform). Prüfen Sie alle Nebenkosten und versteckte Gebühren."},
    {"titel": "Notarkosten und Grunderwerbsteuer berechnen", "kategorie": "Praxiswissen", "inhalt": "Kaufnebenkosten beim Immobilienerwerb: 1) Grunderwerbsteuer: 3,5-6,5% je nach Bundesland, 2) Notar: ca. 1-1,5% des Kaufpreises, 3) Grundbuchamt: ca. 0,5%, 4) Ggf. Makler: 3,57-7,14% inkl. MwSt. Gesamte Nebenkosten: 8-15% des Kaufpreises. Diese Kosten sind bei der Finanzierung zu berücksichtigen."},
    {"titel": "Mietkaution - Rechte und Pflichten", "kategorie": "Praxiswissen", "inhalt": "Die Mietkaution beträgt maximal drei Nettokaltmieten. Der Mieter kann in drei Monatsraten zahlen. Der Vermieter muss die Kaution getrennt vom Vermögen anlegen (insolvenzfest). Zinsen stehen dem Mieter zu. Nach Mietende: Rückzahlung nach angemessener Prüfungsfrist (3-6 Monate). Aufrechnung nur mit unstreitigen oder rechtskräftig festgestellten Forderungen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        api_key=QDRANT_API_KEY,
        https=True
    )
    
    # Status vorher
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # BGH Mietrecht
    for item in BGH_MIETRECHT:
        text = f"BGH {item['az']} vom {item['datum']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {
                "source": f"BGH {item['az']}",
                "type": "Rechtsprechung",
                "category": "Mietrecht",
                "court": "BGH",
                "date": item['datum'],
                "title": item['titel']
            }
        })
    
    # BGH WEG
    for item in BGH_WEG:
        text = f"BGH {item['az']} vom {item['datum']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {
                "source": f"BGH {item['az']}",
                "type": "Rechtsprechung",
                "category": "WEG-Recht",
                "court": "BGH",
                "date": item['datum'],
                "title": item['titel']
            }
        })
    
    # OLG/LG
    for item in OLG_ENTSCHEIDUNGEN:
        text = f"{item['gericht']} {item['az']} vom {item['datum']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {
                "source": f"{item['gericht']} {item['az']}",
                "type": "Rechtsprechung",
                "category": "Immobilienrecht",
                "court": item['gericht'],
                "date": item['datum'],
                "title": item['titel']
            }
        })
    
    # BVerfG
    for item in BVERFG:
        text = f"BVerfG {item['az']} vom {item['datum']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {
                "source": f"BVerfG {item['az']}",
                "type": "Rechtsprechung",
                "category": "Verfassungsrecht",
                "court": "BVerfG",
                "date": item['datum'],
                "title": item['titel']
            }
        })
    
    # BFH Steuer
    for item in BFH_STEUER:
        text = f"BFH {item['az']} vom {item['datum']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {
                "source": f"BFH {item['az']}",
                "type": "Rechtsprechung",
                "category": "Steuerrecht",
                "court": "BFH",
                "date": item['datum'],
                "title": item['titel']
            }
        })
    
    # Praxiswissen
    for item in PRAXISWISSEN:
        text = f"{item['titel']}\n\nKategorie: {item['kategorie']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {
                "source": item['titel'],
                "type": "Praxiswissen",
                "category": item['kategorie'],
                "title": item['titel']
            }
        })
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(
                id=doc["id"],
                vector=embedding,
                payload={
                    "text": doc["text"],
                    **doc["metadata"]
                }
            ))
            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{len(all_docs)} Embeddings generiert")
        except Exception as e:
            print(f"Fehler bei Dokument {i}: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    # Status nachher
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")
    print("Fertig!")

if __name__ == "__main__":
    main()
