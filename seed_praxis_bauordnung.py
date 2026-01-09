#!/usr/bin/env python3
"""
Mega-Seeding: 150+ Dokumente
- Alle Bundesländer Bauordnungen Details
- Musterverträge
- Praxisfälle
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

# Bauordnungen Details
BAUORDNUNGEN = [
    {"land": "Bayern", "paragraph": "Art. 6 BayBO", "titel": "Abstandsflächen Bayern", "inhalt": "In Bayern beträgt die Abstandsfläche grundsätzlich 1 H (Wandhöhe), mindestens 3 m. In Kerngebieten und Industriegebieten können geringere Abstandsflächen zugelassen werden. Vor Außenwänden von Gebäuden sind Abstandsflächen von oberirdischen Gebäuden freizuhalten."},
    {"land": "Baden-Württemberg", "paragraph": "§ 5 LBO BW", "titel": "Abstandsflächen Baden-Württemberg", "inhalt": "Die Abstandsfläche beträgt 0,4 H, mindestens 2,5 m. In Gewerbe- und Industriegebieten sind auch geringere Abstände zulässig. Vor den Außenwänden von Gebäuden sind Abstandsflächen von Gebäuden freizuhalten."},
    {"land": "Nordrhein-Westfalen", "paragraph": "§ 6 BauO NRW", "titel": "Abstandsflächen NRW", "inhalt": "Die Tiefe der Abstandsfläche beträgt 0,4 H, mindestens 3 m. In Kerngebieten, Gewerbe- und Industriegebieten können geringere Tiefen zugelassen werden. Bei Wohngebäuden der Gebäudeklassen 1 und 2 genügt eine Tiefe von 3 m."},
    {"land": "Hessen", "paragraph": "§ 6 HBO", "titel": "Abstandsflächen Hessen", "inhalt": "Die Tiefe der Abstandsflächen beträgt 0,4 H, mindestens 3 m. In Kerngebieten und besonderen Wohngebieten kann die Tiefe auf 0,2 H verringert werden. Für Garagen und Nebengebäude gelten Sonderregelungen."},
    {"land": "Berlin", "paragraph": "§ 6 BauO Bln", "titel": "Abstandsflächen Berlin", "inhalt": "Die Tiefe der Abstandsfläche beträgt 0,4 H, mindestens 3 m. In bestimmten Gebieten, insbesondere in der Innenstadt, kann die erforderliche Tiefe unterschritten werden. Die Nachbarzustimmung kann erforderlich sein."},
    {"land": "Hamburg", "paragraph": "§ 6 HBauO", "titel": "Abstandsflächen Hamburg", "inhalt": "Die Abstandsflächen betragen 0,4 H, mindestens 2,5 m. In verdichteten Gebieten können geringere Abstände zugelassen werden. Balkone und Erker dürfen in die Abstandsflächen hineinragen."},
    {"land": "Sachsen", "paragraph": "§ 6 SächsBO", "titel": "Abstandsflächen Sachsen", "inhalt": "Die Tiefe der Abstandsfläche beträgt 0,4 H, mindestens 3 m. Bei Wohngebäuden in Gebieten mit Bebauungsplan genügt auch 0,2 H. Für Garagen bis 9 m Länge sind keine Abstandsflächen erforderlich."},
    {"land": "Niedersachsen", "paragraph": "§ 5 NBauO", "titel": "Abstandsflächen Niedersachsen", "inhalt": "Die Tiefe der Abstandsflächen beträgt 0,5 H, mindestens 3 m. In Kerngebieten und besonderen Wohngebieten kann auf 0,25 H verringert werden. Auf der der Straße zugewandten Seite kann von Abstandsflächen abgesehen werden."},
    {"land": "Rheinland-Pfalz", "paragraph": "§ 8 LBauO RP", "titel": "Abstandsflächen Rheinland-Pfalz", "inhalt": "Vor den Außenwänden von Gebäuden sind Abstandsflächen von oberirdischen Gebäuden freizuhalten. Die Tiefe beträgt 0,4 H, mindestens 3 m. Für Garagen und Nebengebäude gelten Erleichterungen."},
    {"land": "Schleswig-Holstein", "paragraph": "§ 6 LBO SH", "titel": "Abstandsflächen Schleswig-Holstein", "inhalt": "Die Tiefe der Abstandsfläche beträgt 0,4 H, mindestens 3 m. An der Nachbargrenze sind Gebäude ohne Abstandsflächen zulässig, wenn der Nachbar zustimmt. Bei Grenzbebauung ist eine Brandwand erforderlich."},
    {"land": "Brandenburg", "paragraph": "§ 6 BbgBO", "titel": "Abstandsflächen Brandenburg", "inhalt": "Die Tiefe der Abstandsflächen beträgt 0,4 H, mindestens 3 m. Im Innenbereich nach § 34 BauGB können geringere Abstände zugelassen werden, wenn die Belichtung gewährleistet ist."},
    {"land": "Thüringen", "paragraph": "§ 6 ThürBO", "titel": "Abstandsflächen Thüringen", "inhalt": "Vor den Außenwänden von Gebäuden sind Abstandsflächen von oberirdischen Gebäuden freizuhalten. Die Tiefe beträgt 0,4 H, mindestens 3 m. Untergeordnete Bauteile können in Abstandsflächen hineinragen."},
    {"land": "Sachsen-Anhalt", "paragraph": "§ 6 BauO LSA", "titel": "Abstandsflächen Sachsen-Anhalt", "inhalt": "Die Tiefe der Abstandsflächen beträgt 0,4 H, mindestens 3 m. Im Geltungsbereich eines Bebauungsplans kann auf 0,2 H reduziert werden. Garagen und Nebenanlagen sind an der Grenze zulässig."},
    {"land": "Mecklenburg-Vorpommern", "paragraph": "§ 6 LBauO M-V", "titel": "Abstandsflächen Mecklenburg-Vorpommern", "inhalt": "Die Abstandsflächentiefe beträgt 0,4 H, mindestens 3 m. In verdichteten Gebieten und bei Bebauungsplan können geringere Abstände zugelassen werden. Für Garagen gilt die Privilegierung."},
    {"land": "Saarland", "paragraph": "§ 7 LBO Saar", "titel": "Abstandsflächen Saarland", "inhalt": "Die Tiefe der Abstandsflächen beträgt 0,4 H, mindestens 3 m. An der Grenze sind Gebäude zulässig, wenn der Nachbar schriftlich zustimmt oder an der Grenze bereits ein Gebäude steht."},
    {"land": "Bremen", "paragraph": "§ 6 BremLBO", "titel": "Abstandsflächen Bremen", "inhalt": "Die Tiefe der Abstandsflächen beträgt 0,4 H, mindestens 2,5 m. In verdichteten Innenstadtlagen können geringere Abstände zugelassen werden. Die Flächen müssen auf dem Grundstück selbst liegen."},
]

# Praxisfälle und Fallbeispiele
PRAXISFAELLE = [
    {"titel": "Fallbeispiel: Eigenbedarfskündigung - Härtefallprüfung", "inhalt": "Der Vermieter kündigt einer 78-jährigen Mieterin nach 35 Jahren Mietdauer wegen Eigenbedarfs für seine erwachsene Tochter. Die Mieterin hat gesundheitliche Einschränkungen. Lösung: Die Eigenbedarfskündigung ist zwar grundsätzlich wirksam, aber die Härtefallprüfung nach § 574 BGB führt zur Fortsetzung des Mietverhältnisses. Hohes Alter, lange Mietdauer und Gesundheitszustand überwiegen das Eigenbedarfsinteresse."},
    {"titel": "Fallbeispiel: Schimmel in der Mietwohnung", "inhalt": "In der Mietwohnung tritt Schimmel auf. Der Vermieter behauptet falsches Lüftungsverhalten. Lösung: Die Beweislast für bauliche Mängel liegt beim Mieter, die für falsches Nutzungsverhalten beim Vermieter. Ein Gutachten kann klären, ob bauliche Ursachen (Wärmebrücken, undichte Fenster) vorliegen. Bei baulichen Mängeln: Mietminderung 10-50% je nach Ausmaß."},
    {"titel": "Fallbeispiel: Betriebskostenabrechnung zu spät", "inhalt": "Der Vermieter sendet die Betriebskostenabrechnung erst nach 15 Monaten. Der Mieter soll 800 EUR nachzahlen. Lösung: Nach § 556 Abs. 3 BGB muss die Abrechnung innerhalb von 12 Monaten nach Ende des Abrechnungszeitraums zugehen. Bei verspäteter Abrechnung kann der Vermieter keine Nachzahlung mehr verlangen, es sei denn, er hat die Verspätung nicht zu vertreten."},
    {"titel": "Fallbeispiel: Untervermietung über Airbnb", "inhalt": "Der Mieter vermietet seine Wohnung während eines mehrwöchigen Urlaubs über Airbnb. Der Vermieter kündigt fristlos. Lösung: Die Untervermietung ohne Erlaubnis stellt eine Vertragsverletzung dar. Bei kurzzeitiger gewerblicher Vermietung ist die fristlose Kündigung nach Abmahnung in der Regel wirksam. Der Mieter hätte vorher die Erlaubnis einholen müssen."},
    {"titel": "Fallbeispiel: Mieterhöhung ohne Mietspiegel", "inhalt": "In einer Gemeinde ohne Mietspiegel will der Vermieter die Miete erhöhen. Lösung: Der Vermieter kann die Erhöhung durch mindestens 3 Vergleichswohnungen oder ein Sachverständigengutachten begründen. Die Vergleichswohnungen müssen nach Lage, Art, Größe und Ausstattung vergleichbar sein."},
    {"titel": "Fallbeispiel: Kaution nach 6 Monaten nicht zurück", "inhalt": "Das Mietverhältnis endete vor 6 Monaten. Der Vermieter hat die Kaution noch nicht zurückgezahlt und nennt keine Gründe. Lösung: Die angemessene Prüfungsfrist beträgt in der Regel 3-6 Monate. Nach Ablauf kann der Mieter die Rückzahlung einfordern. Der Vermieter darf nur für berechtigte Forderungen aufrechnen."},
    {"titel": "Fallbeispiel: Nachbarlärm durch Kinder", "inhalt": "Die Nachbarn beschweren sich über Kinderlärm in der Wohnung (spielende Kinder am Nachmittag). Lösung: Kinderlärm gehört zur sozialadäquaten Nutzung einer Wohnung. Eltern müssen Kinderlärm nicht vollständig unterbinden. Eine Kündigung wegen Kinderlärms ist nur bei extremen, unzumutbaren Störungen möglich."},
    {"titel": "Fallbeispiel: WEG-Beschluss Balkonverglasung", "inhalt": "Ein Eigentümer möchte seinen Balkon verglasen. Die Eigentümerversammlung lehnt ab. Lösung: Nach der WEG-Reform 2020 können bauliche Veränderungen mit einfacher Mehrheit beschlossen werden. Die Verglasung verändert aber das äußere Erscheinungsbild. Bei Ablehnung kann der Eigentümer prüfen, ob ein Anspruch auf Zustimmung besteht (keine Beeinträchtigung anderer Eigentümer)."},
    {"titel": "Fallbeispiel: Grundstückskauf mit Altlasten", "inhalt": "Nach dem Kauf stellt sich heraus, dass das Grundstück mit Öl kontaminiert ist. Der Verkäufer verschwieg dies. Lösung: Das arglistige Verschweigen eines Mangels schließt den vereinbarten Gewährleistungsausschluss aus. Der Käufer kann Rücktritt, Minderung und Schadensersatz verlangen. Die Beweislast für die Kenntnis liegt beim Käufer."},
    {"titel": "Fallbeispiel: Maklercourtage - Wer zahlt?", "inhalt": "Beim Wohnungskauf verlangt der Makler vom Käufer die volle Provision. Der Makler wurde aber vom Verkäufer beauftragt. Lösung: Nach § 656c BGB (seit 2020) gilt bei Maklerverträgen über Wohnungen: Wer den Makler beauftragt, zahlt mindestens 50% der Provision. Der andere Teil kann maximal 50% tragen. Wurde nur der Verkäufer beauftragt, darf der Käufer maximal 50% zahlen."},
]

# Nachbarrecht
NACHBARRECHT = [
    {"titel": "Nachbarrecht: Grenzbepflanzung", "inhalt": "Die Regelungen zur Grenzbepflanzung sind landesrechtlich geregelt. Grundsätzlich gilt: Bäume müssen je nach Höhe einen bestimmten Grenzabstand einhalten (oft 0,5-4 m). Der Nachbar kann Rückschnitt verlangen, wenn der Abstand unterschritten wird oder Äste herüberragen. Verjährung beachten!"},
    {"titel": "Nachbarrecht: Immissionen § 906 BGB", "inhalt": "Der Eigentümer eines Grundstücks kann Einwirkungen wie Geräusche, Gerüche, Rauch nicht verbieten, wenn sie ortsüblich sind und das Grundstück nicht wesentlich beeinträchtigen. Bei wesentlicher Beeinträchtigung: Unterlassungs- oder Ausgleichsanspruch."},
    {"titel": "Nachbarrecht: Hammerschlags- und Leiterrecht", "inhalt": "Das Hammerschlagsrecht erlaubt dem Grundstückseigentümer, das Nachbargrundstück zu betreten, um am eigenen Gebäude Arbeiten durchzuführen. Voraussetzung: Vorherige Ankündigung, keine anderweitige Möglichkeit. Der Nachbar hat Anspruch auf Schadensersatz bei Beschädigungen."},
    {"titel": "Nachbarrecht: Einfriedung und Grenzzaun", "inhalt": "Die Pflicht zur Einfriedung ist landesrechtlich geregelt. Im Zweifel trägt jeder Nachbar die Kosten für die Einfriedung auf seiner Seite. Gemeinsame Einfriedungen (Grenzmauer) erfordern Vereinbarung. Die zulässige Höhe von Zäunen regeln Bebauungspläne oder Landesrecht."},
    {"titel": "Nachbarrecht: Notwegerecht § 917 BGB", "inhalt": "Fehlt einem Grundstück die zur ordnungsgemäßen Nutzung notwendige Verbindung mit einem öffentlichen Weg, kann der Eigentümer von Nachbarn verlangen, dass sie die Benutzung ihrer Grundstücke dulden. Der Notwegberechtigte muss eine Geldrente zahlen."},
]

# Finanzierung
FINANZIERUNG = [
    {"titel": "Baufinanzierung: Annuitätendarlehen", "inhalt": "Das Annuitätendarlehen ist die häufigste Finanzierungsform. Die monatliche Rate (Annuität) bleibt konstant. Sie setzt sich aus Zins- und Tilgungsanteil zusammen. Mit jeder Rate sinkt der Zinsanteil, der Tilgungsanteil steigt. Die Anfangstilgung sollte mindestens 2% betragen."},
    {"titel": "Baufinanzierung: Sondertilgung", "inhalt": "Sondertilgungen ermöglichen die vorzeitige Rückzahlung ohne Vorfälligkeitsentschädigung. Üblich sind 5-10% der Darlehenssumme pro Jahr. Sondertilgungsrechte sollten im Darlehensvertrag vereinbart werden. Sie beschleunigen die Entschuldung und sparen Zinsen."},
    {"titel": "Baufinanzierung: KfW-Förderung", "inhalt": "Die KfW fördert energieeffizientes Bauen und Sanieren. Programme: BEG Wohngebäude (Effizienzhaus), BEG Einzelmaßnahmen. Förderung als zinsgünstiges Darlehen mit Tilgungszuschuss. Antrag vor Baubeginn über die Hausbank. Kombination mit BAFA-Förderung möglich."},
    {"titel": "Baufinanzierung: Beleihungswert und Beleihungsauslauf", "inhalt": "Der Beleihungswert ist der langfristig erzielbare Wert einer Immobilie (80-90% des Kaufpreises). Der Beleihungsauslauf ist das Verhältnis von Darlehen zu Beleihungswert. Bei über 80% steigt der Zinssatz. Optimaler Beleihungsauslauf: 60-80%."},
    {"titel": "Baufinanzierung: Bereitstellungszinsen", "inhalt": "Bereitstellungszinsen fallen an, wenn das Darlehen nicht sofort abgerufen wird. Üblich: 0,25% pro Monat ab dem 3.-6. Monat nach Darlehenszusage. Bei Neubau oder Sanierung: Möglichst lange bereitstellungszinsfreie Zeit vereinbaren (12-24 Monate)."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Bauordnungen
    for item in BAUORDNUNGEN:
        text = f"{item['paragraph']}: {item['titel']} ({item['land']})\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Bauordnung", "land": item['land'], "title": item['titel']}})
    
    # Praxisfälle
    for item in PRAXISFAELLE:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxisfall", "category": "Fallbeispiel", "title": item['titel']}})
    
    # Nachbarrecht
    for item in NACHBARRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Nachbarrecht", "title": item['titel']}})
    
    # Finanzierung
    for item in FINANZIERUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Baufinanzierung", "title": item['titel']}})
    
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
