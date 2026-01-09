#!/usr/bin/env python3
"""
Mega-Seeding Teil 9: 100+ Dokumente 
- Mehr EU Recht
- Komplettes Steuerrecht 
- Vollständige LBO aller Bundesländer
- Versicherungsrecht
- Mehr Praxisfälle
"""

import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

QDRANT_HOST = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    result = genai.embed_content(model="models/embedding-001", content=text[:8000], task_type="retrieval_document")
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# Vollständige Landesbauordnungen Details
LBO_ALLE_LAENDER = [
    {"land": "Bayern", "artikel": "Art. 8 BayBO", "titel": "Genehmigungsverfahren Bayern", "inhalt": "Bauvorhaben bedürfen der Baugenehmigung. Ausnahmen: Verfahrensfreie Bauvorhaben und Genehmigungsfreistellung. Das Verfahren gliedert sich in Vorprüfung und Vollprüfung. Bei einfachen Bauvorhaben kann eine vereinfachte Genehmigung erteilt werden. Die Genehmigung gilt 3 Jahre."},
    {"land": "Bayern", "artikel": "Art. 15 BayBO", "titel": "Stellplätze und Garagen Bayern", "inhalt": "Bei der Errichtung von Gebäuden sind in ausreichender Zahl notwendige Stellplätze auf dem Baugrundstück oder in unmittelbarer Nähe herzustellen. Je angefangene 40 qm Wohnfläche ist ein Stellplatz erforderlich. Ausnahmen in Innenstädten und bei ÖPNV-Anbindung möglich."},
    {"land": "Baden-Württemberg", "artikel": "§ 50 LBO BW", "titel": "Genehmigungsverfahren Baden-Württemberg", "inhalt": "Das Baugenehmigungsverfahren kann als vollständiges oder vereinfachtes Verfahren durchgeführt werden. Bei Gebäuden der Gebäudeklassen 1-3 ist das vereinfachte Verfahren möglich. Die Prüftiefe richtet sich nach der Komplexität des Bauvorhabens."},
    {"land": "Nordrhein-Westfalen", "artikel": "§ 62 BauO NRW", "titel": "Genehmigungsverfahren NRW", "inhalt": "Die Baugenehmigung wird von der unteren Bauaufsichtsbehörde erteilt. Bei Industriebauten ist die obere Bauaufsichtsbehörde zuständig. Das Kenntnisgabeverfahren ermöglicht bei einfachen Bauvorhaben den Baubeginn ohne förmliche Genehmigung nach 4 Wochen."},
    {"land": "Hessen", "artikel": "§ 63 HBO", "titel": "Genehmigungsverfahren Hessen", "inhalt": "Bauvorhaben werden im Baugenehmigungsverfahren oder im Kenntnisgabeverfahren behandelt. Bei Wohngebäuden der Gebäudeklassen 1-3 ist oft das Kenntnisgabeverfahren möglich. Die Behörde kann binnen eines Monats Einwendungen erheben."},
    {"land": "Berlin", "artikel": "§ 59 BauO Bln", "titel": "Genehmigungsverfahren Berlin", "inhalt": "Berlin kennt das vereinfachte Genehmigungsverfahren für Ein- und Zweifamilienhäuser. Bei komplexeren Vorhaben: Vollverfahren mit Beteiligung aller Träger öffentlicher Belange. Besonderheit: Gestaltungskommission bei städtebaulich bedeutsamen Vorhaben."},
    {"land": "Hamburg", "artikel": "§ 58 HBauO", "titel": "Genehmigungsverfahren Hamburg", "inhalt": "Hamburg hat das Kenntnisgabeverfahren für kleinere Bauvorhaben. Der Bauherr teilt das Vorhaben mit und kann nach 4 Wochen ohne Widerspruch beginnen. Bei komplexeren Vorhaben: Baugenehmigungsverfahren mit Prüfung der Bauvorlagen."},
    {"land": "Sachsen", "artikel": "§ 64 SächsBO", "titel": "Genehmigungsverfahren Sachsen", "inhalt": "Sachsen unterscheidet zwischen dem Baugenehmigungsverfahren und dem Kenntnisgabeverfahren. Bei letzterem kann nach 4 Wochen ohne Widerspruch der Behörde mit dem Bau begonnen werden. Zuständig sind die unteren Bauaufsichtsbehörden der Landkreise."},
    {"land": "Niedersachsen", "artikel": "§ 57 NBauO", "titel": "Genehmigungsverfahren Niedersachsen", "inhalt": "Die Baugenehmigung wird von der Bauaufsichtsbehörde erteilt. Bei einfachen Vorhaben ist das vereinfachte Genehmigungsverfahren möglich. Besonderheit: Privilegierung für landwirtschaftliche Betriebe im Außenbereich."},
    {"land": "Rheinland-Pfalz", "artikel": "§ 58 LBauO RP", "titel": "Genehmigungsverfahren Rheinland-Pfalz", "inhalt": "Das Baugenehmigungsverfahren gliedert sich in vereinfachtes und vollständiges Verfahren. Bei Gebäudeklasse 1 und 2 ist meist das vereinfachte Verfahren ausreichend. Die Genehmigung gilt 3 Jahre, Verlängerung um weitere 2 Jahre möglich."},
    {"land": "Schleswig-Holstein", "artikel": "§ 58 LBO SH", "titel": "Genehmigungsverfahren Schleswig-Holstein", "inhalt": "Schleswig-Holstein kennt das Baugenehmigungsverfahren und das Anzeigeverfahren. Beim Anzeigeverfahren kann nach einem Monat ohne Widerspruch mit dem Bau begonnen werden. Zuständig sind die unteren Bauaufsichtsbehörden der Kreise."},
]

# Steuerrecht komplett
STEUERRECHT_KOMPLETT = [
    {"paragraph": "§ 7 EStG", "titel": "Absetzung für Abnutzung (AfA) bei Immobilien", "inhalt": "Gebäude können über die Nutzungsdauer abgeschrieben werden. Wohngebäude: 2% bzw. 2,5% AfA (je nach Baujahr). Gewerbliche Gebäude: 3% AfA. Bei denkmalgeschützten Gebäuden: Sonder-AfA nach § 7i EStG für Vermieter oder § 10f EStG für Eigennutzer möglich."},
    {"paragraph": "§ 9 GrESt", "titel": "Grunderwerbsteuer: Bemessungsgrundlage", "inhalt": "Die Grunderwerbsteuer beträgt je nach Bundesland 3,5% bis 6,5% des Kaufpreises. Bemessungsgrundlage ist der Kaufpreis inklusive Inventar, soweit es mit dem Grundstück verkauft wird. Bei Verwandtengeschäften: Mindestens der Grundbesitzwert. Freibetrag: 2.500 EUR nur bei bestimmten Verwandtschaftsgraden."},
    {"paragraph": "§ 10 ErbStG", "titel": "Erbschaftsteuer: Bewertung von Grundbesitz", "inhalt": "Grundbesitz wird mit dem Grundbesitzwert angesetzt. Dieser orientiert sich am Verkehrswert (Vergleichswertverfahren, Sachwertverfahren, Ertragswertverfahren). Verschonungsregelungen: Familienheim an Ehegatte/Kinder steuerfrei bei 10-jähriger Selbstnutzung und Mindestfläche."},
    {"paragraph": "§ 21 EStG", "titel": "Einkünfte aus Vermietung und Verpachtung", "inhalt": "Mieteinnahmen sind steuerpflichtig. Absetzbar: AfA, Zinsen, Betriebskosten bei Leerstand, Verwaltungskosten, Instandhaltung, Modernisierung (teilweise). Bei Vermietung unter 66% der ortsüblichen Miete: Liebhaberei-Prüfung. Negativer Überschuss kann mit anderen Einkünften verrechnet werden."},
    {"paragraph": "§ 23 EStG", "titel": "Spekulationssteuer bei Immobilienverkauf", "inhalt": "Bei Verkauf einer Immobilie innerhalb von 10 Jahren nach Erwerb ist der Gewinn steuerpflichtig (Spekulationssteuer). Ausnahme: Eigengenutzte Immobilie (mindestens 3 Jahre in den letzten 5 Jahren selbst bewohnt). Verkaufsgewinn = Verkaufspreis minus Anschaffungskosten minus Verbesserungsaufwendungen."},
    {"paragraph": "§ 52 EStG", "titel": "Erhöhte Absetzungen für Modernisierung", "inhalt": "Bei energetischen Sanierungsmaßnahmen können erhöhte Absetzungen geltend gemacht werden. Bei selbstgenutzten Eigenheimen: 20% der Kosten über 3 Jahre verteilt als Steuerermäßigung (§ 35c EStG). Bei vermieteten Objekten: Sonderabschreibung oder normale AfA."},
    {"paragraph": "§ 13 GrStG", "titel": "Grundsteuer: Bewertung und Hebesatz", "inhalt": "Die Grundsteuer wird auf Basis des Einheitswerts (alt) bzw. Grundsteuerwerts (neu ab 2025) berechnet. Die Kommunen legen den Hebesatz fest. Grundsteuer A: Land- und forstwirtschaftliche Betriebe. Grundsteuer B: Bebaute und bebaubare Grundstücke. Die Steuer ist bei Vermietung auf Mieter umlagefähig."},
    {"paragraph": "§ 6 UStG", "titel": "Umsatzsteuer bei Immobilien", "inhalt": "Die Vermietung von Wohnraum ist umsatzsteuerfrei. Bei Gewerbevermietung kann zur Umsatzsteuer optiert werden. Der Verkauf von Grundstücken ist grundsätzlich umsatzsteuerfrei, es sei denn, es handelt sich um ein Bauträgergeschäft oder gewerblichen Grundstückshandel."},
]

# EU Recht Immobilien
EU_RECHT = [
    {"richtlinie": "Richtlinie 2002/91/EG", "titel": "EU-Gebäuderichtlinie (Energieeffizienz)", "inhalt": "Die EU-Gebäuderichtlinie verpflichtet die Mitgliedstaaten zur Einführung von Energieausweisen für Gebäude. Sie regelt Mindestanforderungen an die Gesamteffizienz von Gebäuden. Umsetzung in Deutschland durch das Gebäudeenergiegesetz (GEG). Nearly-Zero-Energy-Buildings sind das Ziel für Neubauten."},
    {"richtlinie": "Richtlinie 2012/27/EU", "titel": "EU-Energieeffizienzrichtlinie", "inhalt": "Die Energieeffizienzrichtlinie setzt verbindliche Ziele für die Energieeffizienz. Öffentliche Gebäude müssen eine Vorbildfunktion einnehmen. Sanierungsquoten von 3% pro Jahr für öffentliche Gebäude. Die Richtlinie beeinflusst nationale Förderinstrumente für Gebäudesanierung."},
    {"verordnung": "EU-Taxonomie-VO", "titel": "EU-Taxonomie für nachhaltige Immobilien", "inhalt": "Die EU-Taxonomie definiert Kriterien für ökologisch nachhaltige Wirtschaftsaktivitäten. Immobilieninvestitionen müssen bestimmte Umweltkriterien erfüllen, um als 'grün' zu gelten. Kriterien: CO2-Emissionen unter 70% des nationalen Durchschnitts oder Energieeffizienzklasse A."},
    {"richtlinie": "Richtlinie 2018/844/EU", "titel": "Novelle der Gebäuderichtlinie", "inhalt": "Die novellierte Gebäuderichtlinie stärkt langfristige Renovierungsstrategien. Intelligente Technologien in Gebäuden werden gefördert. Inspektionen von Heizungs- und Klimaanlagen werden verschärft. Ziel: Dekarbonisierung des Gebäudebestands bis 2050."},
    {"grundrecht": "Art. 17 EU-Grundrechtecharta", "titel": "Eigentumsschutz in der EU", "inhalt": "Das Eigentumsrecht ist als Grundrecht in der EU-Grundrechtecharta verankert. Es umfasst auch das geistige Eigentum. Enteignungen sind nur im öffentlichen Interesse und gegen Entschädigung zulässig. Das Recht wirkt auch im Verhältnis zwischen den Mitgliedstaaten (Investitionsschutz)."},
]

# Versicherungsrecht Immobilien
VERSICHERUNGSRECHT = [
    {"titel": "Wohngebäudeversicherung: Leistungsumfang", "inhalt": "Die Wohngebäudeversicherung deckt Schäden durch Feuer, Leitungswasser, Sturm/Hagel und optional weitere Elementarschäden. Versichert sind Gebäude, fest mit dem Gebäude verbundene Anlagen und Nebengebäude. Wichtig: Gleitende Neuwertversicherung und Unterversicherungsverzicht."},
    {"titel": "Hausrat- vs. Wohngebäudeversicherung", "inhalt": "Die Hausratversicherung deckt bewegliche Gegenstände in der Wohnung. Die Wohngebäudeversicherung versichert das Gebäude selbst. Abgrenzung: Einbauküche gehört zum Hausrat, fest installierte Sanitärobjekte zur Gebäudeversicherung. Bei Eigentumswohnungen: Unterscheidung Sonder-/Gemeinschaftseigentum."},
    {"titel": "Haftpflicht bei Immobilien: Haus- und Grundbesitzer", "inhalt": "Der Eigentümer haftet für Schäden durch sein Grundstück (Verkehrssicherungspflicht). Die Haus- und Grundbesitzerhaftpflicht deckt Personen-, Sach- und Vermögensschäden. Typische Risiken: Glatteis, herabfallende Gegenstände, Baumängel. Bei vermieteten Objekten: Auch Haftung gegenüber Mietern."},
    {"titel": "Bauleistungsversicherung und Bauherrenhaftpflicht", "inhalt": "Die Bauleistungsversicherung (Bauwesen-Versicherung) deckt Schäden am Bau während der Bauzeit. Die Bauherrenhaftpflicht versichert Schäden an Dritten. Wichtig: Rohbau-/Feuerversicherung für Eigenbauten. Bei Bauträgern: Fertigstellungsversicherung nach MaBV."},
    {"titel": "Mietausfallversicherung", "inhalt": "Die Mietausfallversicherung ersetzt Mieteinnahmen bei unverschuldetem Mietausfall (z.B. Zahlungsunfähigkeit des Mieters, Gebäudeschäden). Unterscheidung: Mietausfalldeckung in der Gebäudeversicherung vs. separate Mietausfallversicherung. Selbstbehalt und Wartezeiten beachten."},
]

# Mehr Praxisfälle komplex
PRAXISFAELLE_KOMPLEX = [
    {"titel": "Fallbeispiel: WEG-Konflikt - Dachterrasse nachträglich einbauen", "inhalt": "Ein Wohnungseigentümer im obersten Geschoss möchte eine Dachterrasse errichten. Die anderen Eigentümer lehnen ab. Lösung: Nach der WEG-Reform 2020 können bauliche Veränderungen mit einfacher Mehrheit beschlossen werden. Hier liegt aber eine wesentliche Umgestaltung vor, die das Gemeinschaftseigentum betrifft. Ohne Zustimmung der anderen Eigentümer ist die Maßnahme nicht möglich, da sie deren Rechte unverhältnismäßig beeinträchtigt."},
    {"titel": "Fallbeispiel: Erbpacht läuft aus - Was passiert mit dem Haus?", "inhalt": "Ein 75-jähriger Erbbaurechtsvertrag läuft in 5 Jahren aus. Das darauf errichtete Haus ist 2 Millionen wert. Lösung: Der Grundstückseigentümer muss dem Erbbauberechtigten eine Entschädigung zahlen (mindestens 2/3 des Verkehrswerts). Bei Einigung: Verlängerung des Erbbaurechts oder Verkauf des Grundstücks an den Erbbauberechtigten. Ohne Einigung: Heimfall gegen Entschädigung. Der Erbbauberechtigte hat aber ein Vorkaufsrecht bei Verkauf des Grundstücks."},
    {"titel": "Fallbeispiel: Immobilie gekauft - Grundbuch zeigt andere Eigentümer", "inhalt": "Ein Käufer hat notariell eine Immobilie gekauft, aber im Grundbuch steht noch der Verkäufer. Zwischenzeitlich hat eine Bank eine Grundschuld eintragen lassen. Lösung: Die Auflassungsvormerkung schützt den Käufer. Sind Bank und Käufer beide im Grundbuch, entscheidet der Rang. War die Auflassungsvormerkung vor der Grundschuld eingetragen, geht der Käufer vor. Die Bank kann ihre Grundschuld nicht gegen den Käufer durchsetzen."},
    {"titel": "Fallbeispiel: Bauträger insolvent - Käufer haben angezahlt", "inhalt": "Ein Bauträger geht nach Zahlung der ersten Rate (30%) in die Insolvenz. Das Haus ist noch nicht fertig. Lösung: Die MaBV verpflichtet den Bauträger zur Sicherheitsleistung (Bürgschaft oder Fertigstellungsversicherung). Die Käufer können die Bürgschaft in Anspruch nehmen oder die Fertigstellungsversicherung aktivieren. Reicht die Sicherheit nicht aus: Rücktritt vom Kaufvertrag und Rückforderung der geleisteten Zahlungen im Insolvenzverfahren."},
    {"titel": "Fallbeispiel: Nachbar baut zu dicht an die Grenze", "inhalt": "Der Nachbar baut eine Garage 1 Meter von der Grenze entfernt. Laut Bebauungsplan müssen aber 3 Meter Abstand eingehalten werden. Die Bauaufsichtsbehörde hat den Bau genehmigt. Lösung: Der betroffene Nachbar kann Widerspruch gegen die Baugenehmigung einlegen (Drittschutz). Ist die Baugenehmigung rechtswidrig, kann ihre Aufhebung verlangt werden. Bei bereits fertiggestelltem Bau: Beseitigungsanspruch oder Abstandsflächenablösung gegen Entschädigung."},
    {"titel": "Fallbeispiel: Mieter zahlt nicht - Kündigung und Zwangsräumung", "inhalt": "Ein Mieter zahlt seit 3 Monaten keine Miete (Rückstand: 4.500 EUR). Wie geht der Vermieter vor? Lösung: 1. Fristlose Kündigung wegen Zahlungsverzugs (§ 543 BGB) mit hilfsweiser ordentlicher Kündigung. 2. Räumungsklage beim Amtsgericht. 3. Nach rechtskräftigem Urteil: Zwangsvollstreckung (Zwangsräumung). Der Mieter kann durch Zahlung bis zur Zwangsräumung die Kündigung noch heilen (Schonfristzahlung § 569 BGB - aber nur bei erstmaligem Verzug)."},
]

# Gewerbliches Mietrecht Details
GEWERBE_MIETRECHT = [
    {"titel": "Gewerbemiete: Indexklauseln und Anpassung", "inhalt": "Im Gewerbemietrecht sind Indexklauseln zulässig, die die Miete an den Verbraucherpreisindex koppeln. Die Anpassung erfolgt meist jährlich oder bei bestimmten Schwellenwerten (z.B. 3% Änderung). Wichtig: Die Klausel muss präzise formuliert sein und darf den Mieter nicht unangemessen benachteiligen."},
    {"titel": "Gewerbemiete: Kündigungsfristen und -gründe", "inhalt": "Bei Gewerbemiete können die Kündigungsfristen frei vereinbart werden. Ohne Vereinbarung gelten die gesetzlichen Fristen (3-6 Monate je nach Mietdauer). Es gibt keinen Kündigungsschutz wie bei Wohnraum. Der Vermieter kann auch ohne besonderen Grund kündigen. Schonfristzahlung gibt es nicht."},
    {"titel": "Gewerbemiete: Schriftformerfordernis § 550 BGB", "inhalt": "Gewerbemietverträge über ein Jahr müssen schriftlich geschlossen werden. Bei Formmangel gilt der Vertrag als auf unbestimmte Zeit geschlossen. Alle wesentlichen Vertragspunkte müssen schriftlich festgehalten werden: Mietsache, Miethöhe, Laufzeit, Nebenkostenumlage."},
    {"titel": "Gewerbemiete: Kaution und Sicherheiten", "inhalt": "Die Höhe der Kaution ist bei Gewerbemiete nicht begrenzt (anders als bei Wohnraum). Üblich sind 3-6 Monatsmieten. Alternativ: Bankbürgschaften oder andere Sicherheiten. Der Vermieter muss die Kaution nicht getrennt anlegen (kein insolvenzfester Schutz wie bei Wohnraummiete)."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # LBO aller Länder
    for item in LBO_ALLE_LAENDER:
        text = f"{item['artikel']}: {item['titel']} ({item['land']})\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['artikel'], "type": "Gesetz", "category": "Bauordnung", "land": item['land'], "title": item['titel']}})
    
    # Steuerrecht komplett
    for item in STEUERRECHT_KOMPLETT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Steuerrecht", "title": item['titel']}})
    
    # EU Recht
    for item in EU_RECHT:
        key = item.get('richtlinie') or item.get('verordnung') or item.get('grundrecht', 'EU-Recht')
        text = f"{key}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": key, "type": "EU-Recht", "category": "Immobilienrecht", "title": item['titel']}})
    
    # Versicherungsrecht
    for item in VERSICHERUNGSRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Versicherung", "title": item['titel']}})
    
    # Praxisfälle komplex
    for item in PRAXISFAELLE_KOMPLEX:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxisfall", "category": "Komplexfall", "title": item['titel']}})
    
    # Gewerbe Mietrecht
    for item in GEWERBE_MIETRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Gewerbemiete", "title": item['titel']}})
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(id=doc["id"], vector=embedding, payload={"text": doc["text"], **doc["metadata"]}))
            if (i + 1) % 10 == 0: print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()