#!/usr/bin/env python3
"""
Massives Seeding: MaBV, HOAI, Bauvertragsrecht, Maklerrecht
+ Praktische Vertragsmuster und Checklisten
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

# MaBV - Makler- und Bauträgerverordnung
MABV = [
    {"paragraph": "§ 1 MaBV", "titel": "Anwendungsbereich", "inhalt": "Diese Verordnung gilt für Gewerbetreibende, die gewerbsmäßig als Makler oder Bauträger tätig sind. Als Bauträger gilt, wer im eigenen Namen und auf eigene Rechnung ein Gebäude errichtet oder errichten lässt und vor oder während der Bauphase Verträge über die Übertragung des Eigentums abschließt."},
    {"paragraph": "§ 2 MaBV", "titel": "Buchführungspflichten", "inhalt": "Der Gewerbetreibende hat über alle Geschäftsvorgänge Aufzeichnungen zu führen. Die Aufzeichnungen müssen insbesondere die Vereinnahmung und Verausgabung von Vermögenswerten des Auftraggebers erkennen lassen. Die Belege sind geordnet aufzubewahren."},
    {"paragraph": "§ 3 MaBV", "titel": "Sicherheitsleistung (Bauträger)", "inhalt": "Der Bauträger darf Vermögenswerte des Auftraggebers zur Ausführung des Auftrages erst entgegennehmen oder sich zu deren Verwendung ermächtigen lassen, wenn er eine Sicherheit in Höhe der entgegenzunehmenden Vermögenswerte geleistet hat. Die Sicherheit kann durch Bürgschaft einer Bank oder Versicherung erbracht werden."},
    {"paragraph": "§ 4 MaBV", "titel": "Zahlungsplan für Bauträger", "inhalt": "Der Bauträger darf Zahlungen des Erwerbers nur entsprechend dem Baufortschritt entgegennehmen. Die Raten richten sich nach dem Baufortschritt: 1) Beginn der Erdarbeiten: 30%, 2) Rohbaufertigstellung inkl. Dach: 28%, 3) Herstellung der Rohinstallation: 5,6% usw. Die Schlussrate von 3,5% wird nach vollständiger Fertigstellung fällig."},
    {"paragraph": "§ 7 MaBV", "titel": "Abwicklung über Notaranderkonto", "inhalt": "Vermögenswerte des Auftraggebers sind unverzüglich einem Notaranderkonto zuzuführen, wenn der Auftraggeber dies verlangt. Die Anlage hat bei einem Kreditinstitut zu erfolgen. Der Notar verwaltet das Konto treuhänderisch und zahlt nur nach den vereinbarten Bedingungen aus."},
    {"paragraph": "§ 10 MaBV", "titel": "Haftpflichtversicherung", "inhalt": "Der Gewerbetreibende hat eine Berufshaftpflichtversicherung abzuschließen und aufrechtzuerhalten. Die Mindestversicherungssumme beträgt 500.000 Euro für jeden Versicherungsfall und 1.000.000 Euro für alle Versicherungsfälle eines Jahres."},
]

# Bauvertragsrecht BGB
BAUVERTRAGSRECHT = [
    {"paragraph": "§ 650a BGB", "titel": "Bauvertrag", "inhalt": "Ein Bauvertrag ist ein Vertrag über die Herstellung, die Wiederherstellung, die Beseitigung oder den Umbau eines Bauwerks, einer Außenanlage oder eines Teils davon. Für den Bauvertrag gelten ergänzend die Vorschriften des Werkvertragsrechts."},
    {"paragraph": "§ 650b BGB", "titel": "Änderungen des Vertrags; Anordnungsrecht des Bestellers", "inhalt": "Begehrt der Besteller eine Änderung des vereinbarten Werkerfolgs oder eine Änderung, die zur Erreichung des vereinbarten Werkerfolgs notwendig ist, ist der Unternehmer verpflichtet, ein Angebot über die Mehr- oder Minderkosten zu erstellen. Der Besteller kann die Änderung anordnen."},
    {"paragraph": "§ 650c BGB", "titel": "Vergütungsanpassung bei Anordnungen", "inhalt": "Die Höhe des Vergütungsanspruchs für den infolge einer Anordnung vermehrten oder verminderten Aufwand ist nach den tatsächlich erforderlichen Kosten mit angemessenen Zuschlägen für allgemeine Geschäftskosten, Wagnis und Gewinn zu ermitteln."},
    {"paragraph": "§ 650d BGB", "titel": "Einstweilige Verfügung", "inhalt": "Das Gericht hat auf Antrag des Unternehmers eine einstweilige Verfügung zu erlassen, in der dem Besteller aufgegeben wird, einen Abschlag auf die Vergütung für den vermehrten Aufwand zu leisten, wenn der Unternehmer glaubhaft macht, dass er den vereinbarten Werkerfolg ohne die Leistung gefährden würde."},
    {"paragraph": "§ 650f BGB", "titel": "Bauhandwerkersicherung", "inhalt": "Der Unternehmer eines Bauwerks kann vom Besteller Sicherheit für die Vergütung verlangen. Die Sicherheit kann durch eine Garantie oder ein Zahlungsversprechen eines Kreditinstituts erbracht werden. Die Sicherheit ist in Höhe des voraussichtlichen Vergütungsanspruchs zu leisten."},
    {"paragraph": "§ 650g BGB", "titel": "Zustandsfeststellung bei Verweigerung der Abnahme", "inhalt": "Verweigert der Besteller die Abnahme unter Angabe von Mängeln, hat er auf Verlangen des Unternehmers an einer gemeinsamen Feststellung des Zustands des Werks mitzuwirken. Die gemeinsame Zustandsfeststellung soll die erkennbaren Mängel enthalten."},
    {"paragraph": "§ 650h BGB", "titel": "Schriftform der Kündigung", "inhalt": "Die Kündigung des Bauvertrags bedarf der Schriftform. Die elektronische Form ist ausgeschlossen. Eine formunwirksame Kündigung entfaltet keine Wirkung."},
    {"paragraph": "§ 650i BGB", "titel": "Verbraucherbauvertrag", "inhalt": "Verbraucherbauverträge sind Verträge, durch die der Unternehmer von einem Verbraucher zum Bau eines neuen Gebäudes oder zu erheblichen Umbaumaßnahmen an einem bestehenden Gebäude verpflichtet wird."},
    {"paragraph": "§ 650j BGB", "titel": "Baubeschreibung", "inhalt": "Der Unternehmer hat dem Verbraucher rechtzeitig vor Abgabe seiner Vertragserklärung eine Baubeschreibung zur Verfügung zu stellen. Die Baubeschreibung muss die wesentlichen Eigenschaften des Werks in klarer Weise darstellen."},
    {"paragraph": "§ 650l BGB", "titel": "Widerrufsrecht", "inhalt": "Dem Verbraucher steht bei einem Verbraucherbauvertrag ein Widerrufsrecht zu. Der Widerruf ist innerhalb von 14 Tagen ohne Angabe von Gründen zu erklären. Die Widerrufsfrist beginnt mit Vertragsschluss."},
]

# Maklerrecht BGB
MAKLERRECHT = [
    {"paragraph": "§ 652 BGB", "titel": "Entstehung des Maklerlohns", "inhalt": "Wer für den Nachweis der Gelegenheit zum Abschluss eines Vertrags oder für die Vermittlung eines Vertrags einen Mäklerlohn verspricht, ist zur Entrichtung des Lohnes nur verpflichtet, wenn der Vertrag infolge des Nachweises oder der Vermittlung des Mäklers zustande kommt."},
    {"paragraph": "§ 653 BGB", "titel": "Mäklerlohn bei Tarifpflicht", "inhalt": "Ist für den Mäklerlohn ein Tarif oder eine Taxe behördlich festgesetzt, so ist dieser im Zweifel als vereinbart anzusehen. Ist die Höhe des Mäklerlohns nicht bestimmt, so ist der übliche Lohn als vereinbart anzusehen."},
    {"paragraph": "§ 654 BGB", "titel": "Verwirkung des Mäklerlohns", "inhalt": "Der Anspruch auf den Mäklerlohn und den Ersatz von Aufwendungen ist ausgeschlossen, wenn der Mäkler dem Inhalt des Vertrags zuwider auch für den anderen Teil tätig gewesen ist (verbotene Doppeltätigkeit)."},
    {"paragraph": "§ 656a BGB", "titel": "Textform beim Maklervertrag über Wohnungen", "inhalt": "Ein Maklervertrag, der zum Nachweis der Gelegenheit zum Abschluss eines Kaufvertrags über eine Wohnung oder ein Einfamilienhaus oder zur Vermittlung eines solchen Vertrags verpflichtet, bedarf der Textform."},
    {"paragraph": "§ 656c BGB", "titel": "Lohnanspruch bei Tätigkeit für beide Parteien", "inhalt": "Lässt sich der Makler von beiden Parteien des Kaufvertrags über eine Wohnung oder ein Einfamilienhaus einen Maklerlohn versprechen, so kann er den Lohn nur von beiden Parteien verlangen, und zwar nur in gleicher Höhe."},
    {"paragraph": "§ 656d BGB", "titel": "Vereinbarungen über die Maklerprovision", "inhalt": "Hat nur eine Partei des Kaufvertrags über eine Wohnung oder ein Einfamilienhaus einen Maklervertrag abgeschlossen, ist eine Vereinbarung, die die andere Partei zur Zahlung oder Erstattung von Maklerlohn verpflichtet, nur wirksam, wenn die andere Partei höchstens 50% der Gesamtprovision trägt."},
]

# Vertragsmuster und Checklisten
VERTRAGSMUSTER = [
    {"titel": "Checkliste: Mietvertrag für Wohnraum", "kategorie": "Vertragsmuster", "inhalt": "Wesentliche Bestandteile eines Wohnraummietvertrags: 1) Vertragsparteien (Vermieter, Mieter), 2) Mietobjekt (Adresse, Größe, Zimmer, Zubehör), 3) Mietdauer (befristet/unbefristet), 4) Miethöhe (Kaltmiete, Betriebskostenvorauszahlung), 5) Kaution (max. 3 Monatsmieten), 6) Übergabetermin, 7) Zustand bei Übergabe, 8) Schönheitsreparaturen, 9) Tierhaltung, 10) Untervermietung, 11) Kündigungsfristen, 12) Hausordnung."},
    {"titel": "Checkliste: Kaufvertrag Immobilie", "kategorie": "Vertragsmuster", "inhalt": "Wesentliche Inhalte eines Immobilienkaufvertrags: 1) Vertragsparteien mit vollständiger Anschrift, 2) Genaue Objektbezeichnung (Grundbuch, Flurstück), 3) Kaufpreis und Zahlungsmodalitäten, 4) Übergabetermin und Gefahrübergang, 5) Gewährleistungsregelungen, 6) Lasten und Beschränkungen, 7) Auflassungsvormerkung, 8) Finanzierungsvollmacht, 9) Besitzübergang, 10) Kosten und Steuern, 11) Erschließungskosten."},
    {"titel": "Muster: Eigenbedarfskündigung", "kategorie": "Vertragsmuster", "inhalt": "Sehr geehrte(r) [Mieter], hiermit kündige ich das Mietverhältnis über die Wohnung [Adresse] ordentlich wegen Eigenbedarfs gemäß § 573 Abs. 2 Nr. 2 BGB zum [Datum]. Ich benötige die Wohnung für [Person/Beziehung], weil [Begründung]. Die gesetzliche Kündigungsfrist von [X] Monaten gemäß § 573c BGB ist eingehalten. Mit freundlichen Grüßen, [Vermieter]. Hinweis: Die Kündigung muss schriftlich erfolgen und die Kündigungsgründe konkret benennen."},
    {"titel": "Muster: Mietminderungsanzeige", "kategorie": "Vertragsmuster", "inhalt": "Sehr geehrte(r) [Vermieter], in meiner Wohnung [Adresse] besteht seit dem [Datum] folgender Mangel: [genaue Beschreibung]. Dieser Mangel beeinträchtigt die Gebrauchstauglichkeit der Wohnung erheblich. Ich fordere Sie auf, den Mangel bis zum [Frist] zu beseitigen. Bis zur Mängelbeseitigung mindere ich die Miete um [X]% gemäß § 536 BGB. Mit freundlichen Grüßen, [Mieter]."},
    {"titel": "Muster: Betriebskostenabrechnung Widerspruch", "kategorie": "Vertragsmuster", "inhalt": "Sehr geehrte(r) [Vermieter], gegen die Betriebskostenabrechnung für das Jahr [Jahr] erhebe ich Widerspruch. Folgende Punkte sind zu beanstanden: 1) [Konkreter Einwand]. 2) [Weiterer Einwand]. Bitte legen Sie mir die Belege zur Einsicht vor. Eine Nachzahlung werde ich erst leisten, wenn die Abrechnung korrigiert wurde. Mit freundlichen Grüßen, [Mieter]."},
    {"titel": "Muster: Mieterhöhungsverlangen", "kategorie": "Vertragsmuster", "inhalt": "Sehr geehrte(r) [Mieter], ich erhöhe die Nettokaltmiete für die Wohnung [Adresse] von bisher [X] EUR auf [Y] EUR monatlich gemäß § 558 BGB. Die neue Miete entspricht der ortsüblichen Vergleichsmiete, wie der beigefügte Mietspiegel [Stadt] belegt. Die Kappungsgrenze von [15/20]% ist eingehalten. Ich bitte um Ihre Zustimmung bis zum Ende des übernächsten Monats."},
    {"titel": "Checkliste: WEG-Eigentümerversammlung", "kategorie": "Vertragsmuster", "inhalt": "Vorbereitung Eigentümerversammlung: 1) Einladung 3 Wochen vorher in Textform, 2) Tagesordnung mit allen Beschlussgegenständen, 3) Teilnehmerliste mit Miteigentumsanteilen, 4) Feststellung der Beschlussfähigkeit, 5) Wahl des Versammlungsleiters, 6) Abstimmung über jeden TOP, 7) Protokoll mit Wortlaut der Beschlüsse, 8) Unterschrift von Versammlungsleiter und einem Eigentümer, 9) Versand des Protokolls an alle Eigentümer."},
    {"titel": "Muster: Kautionsrückforderung", "kategorie": "Vertragsmuster", "inhalt": "Sehr geehrte(r) [Vermieter], das Mietverhältnis über die Wohnung [Adresse] endete am [Datum]. Ich habe die Wohnung ordnungsgemäß übergeben. Die Kaution in Höhe von [Betrag] EUR nebst aufgelaufenen Zinsen ist zur Rückzahlung fällig. Bitte überweisen Sie den Betrag bis zum [Frist] auf mein Konto [IBAN]. Mit freundlichen Grüßen, [Mieter]."},
]

# Energierecht für Immobilien
ENERGIERECHT = [
    {"paragraph": "§ 80 GEG", "titel": "Energieausweis für Gebäude", "inhalt": "Für Gebäude ist ein Energieausweis auszustellen. Der Energieausweis ist bei Verkauf, Vermietung oder Verpachtung dem Käufer oder Mieter vorzulegen. Bei Nichtvorlage drohen Bußgelder bis 15.000 Euro. Der Ausweis ist 10 Jahre gültig."},
    {"paragraph": "§ 85 GEG", "titel": "Energieausweis bei Verkauf und Vermietung", "inhalt": "Wird ein Gebäude, eine Wohnung oder eine sonstige selbständige Nutzungseinheit verkauft oder vermietet, hat der Verkäufer oder Vermieter dem Kaufinteressenten oder Mietinteressenten spätestens bei der Besichtigung einen Energieausweis vorzulegen."},
    {"paragraph": "§ 87 GEG", "titel": "Pflichtangaben in Immobilienanzeigen", "inhalt": "Wird in einer Immobilienanzeige ein Gebäude oder eine Wohnung zum Verkauf oder zur Vermietung angeboten, sind folgende Pflichtangaben zu machen: Art des Energieausweises, Energieeffizienzklasse, wesentlicher Energieträger, Baujahr des Gebäudes."},
    {"paragraph": "§ 71 GEG", "titel": "Heizungsgesetz 2024", "inhalt": "Ab 2024 dürfen in Neubaugebieten nur noch Heizungen eingebaut werden, die zu mindestens 65% mit erneuerbaren Energien betrieben werden. Für Bestandsgebäude gilt die kommunale Wärmeplanung. Übergangsfristen bis 2028/2045 je nach Kommune."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    for item in MABV:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Verordnung", "category": "MaBV", "title": item['titel']}})
    
    for item in BAUVERTRAGSRECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Bauvertragsrecht", "title": item['titel']}})
    
    for item in MAKLERRECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Maklerrecht", "title": item['titel']}})
    
    for item in VERTRAGSMUSTER:
        text = f"{item['titel']}\n\nKategorie: {item['kategorie']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Vertragsmuster", "category": item['kategorie'], "title": item['titel']}})
    
    for item in ENERGIERECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Energierecht", "title": item['titel']}})
    
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
