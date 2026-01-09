#!/usr/bin/env python3
"""
Mega-Seeding Teil 6: Sozialwohnungen, Kommunalrecht, mehr Paragraphen
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

# Sozialwohnungen und Wohnraumförderung
SOZIALWOHNUNGEN = [
    {"titel": "Sozialwohnung: Wohnberechtigungsschein (WBS)", "inhalt": "Der Wohnberechtigungsschein berechtigt zum Bezug einer Sozialwohnung. Voraussetzung: Einkommen unter der Einkommensgrenze. Die Grenzen variieren je nach Bundesland und Haushaltsgröße. Der WBS wird bei der Gemeinde beantragt und gilt meist 1-2 Jahre."},
    {"titel": "Sozialwohnung: Einkommensgrenzen", "inhalt": "Die Einkommensgrenzen für den WBS richten sich nach dem Wohnraumförderungsgesetz und Landesrecht. Grundsatz: Einkommen von 12.000 EUR pro Jahr für Alleinstehende plus Zuschläge für weitere Haushaltsmitglieder. In teuren Städten höhere Grenzen (WBS mit erhöhtem Einkommen)."},
    {"titel": "Sozialwohnung: Mietpreisbindung", "inhalt": "Sozialwohnungen unterliegen einer Mietpreisbindung. Die Miete darf die Kostenmiete nicht überschreiten. Nach Ablauf der Bindungsfrist (oft 15-30 Jahre) fällt die Bindung weg. Der Vermieter kann dann die Miete auf das ortsübliche Niveau erhöhen."},
    {"titel": "Sozialwohnung: Fehlbelegungsabgabe", "inhalt": "Wer in einer Sozialwohnung lebt und die Einkommensgrenze übersteigt, muss ggf. eine Fehlbelegungsabgabe zahlen. Diese ist in einigen Bundesländern abgeschafft. Wo sie gilt: Zusätzliche Zahlung von bis zu 2,50 EUR/qm."},
    {"titel": "Wohnraumförderung: Wohneigentumsprogramme", "inhalt": "Bund und Länder fördern die Bildung von Wohneigentum. Fördermittel: Zinsgünstige Darlehen, Zuschüsse, Wohn-Riester. Zielgruppe: Familien mit Kindern, Menschen mit Behinderung. Voraussetzung meist: Einkommensgrenze und Selbstnutzung."},
]

# Mietendeckel und Mietpreisbremse Details
MIETPREISREGULIERUNG = [
    {"titel": "Mietpreisbremse: Voraussetzungen und Anwendungsbereich", "inhalt": "Die Mietpreisbremse gilt in Gebieten mit angespanntem Wohnungsmarkt, die durch Landesverordnung bestimmt werden. Sie gilt nicht für: Neubauten (Erstbezug nach 01.10.2014), umfassend modernisierte Wohnungen, bereits überhöhte Vormieten (Bestandsschutz)."},
    {"titel": "Mietpreisbremse: Rügepflicht und Rückforderung", "inhalt": "Der Mieter muss die Überschreitung der zulässigen Miete schriftlich rügen. Erst ab Zugang der Rüge kann er die zu viel gezahlte Miete zurückfordern. Eine rückwirkende Rückforderung ist seit 2020 für 30 Monate vor der Rüge möglich."},
    {"titel": "Mietpreisbremse: Auskunftspflicht des Vermieters", "inhalt": "Der Vermieter muss dem Mieter auf Verlangen Auskunft geben, warum die Miete die ortsübliche Vergleichsmiete plus 10% übersteigt (Vormiete, Modernisierung, Neubau). Die Auskunft muss vor Vertragsschluss oder auf Anfrage erteilt werden."},
    {"titel": "Kappungsgrenze: Mieterhöhung auf Vergleichsmiete", "inhalt": "Die Kappungsgrenze begrenzt Mieterhöhungen innerhalb von 3 Jahren auf 20% (in angespannten Märkten: 15%). Ausgangspunkt ist die Miete vor 3 Jahren. Die Kappungsgrenze gilt zusätzlich zur Grenze der ortsüblichen Vergleichsmiete."},
]

# Zweckentfremdung
ZWECKENTFREMDUNG = [
    {"titel": "Zweckentfremdung: Verbote und Genehmigungspflicht", "inhalt": "In Gebieten mit Wohnraummangel ist die Zweckentfremdung von Wohnraum verboten oder genehmigungspflichtig. Als Zweckentfremdung gilt: Gewerbliche Nutzung, Abriss, Leerstand über 6 Monate, Ferienwohnungsvermietung ohne Genehmigung."},
    {"titel": "Zweckentfremdung: Ferienwohnungen und Airbnb", "inhalt": "Die Vermietung von Wohnungen als Ferienwohnung ist in vielen Städten genehmigungspflichtig. Berlin: Registrierungsnummer erforderlich, Höchstdauer ohne Hauptwohnsitz. München: Genehmigung erforderlich. Verstöße werden mit hohen Bußgeldern geahndet."},
    {"titel": "Zweckentfremdung: Leerstand und Instandsetzungspflicht", "inhalt": "Längerer Leerstand von Wohnungen kann als Zweckentfremdung gelten. Die Behörde kann den Eigentümer zur Vermietung auffordern. Bei Vernachlässigung: Modernisierungsgebot oder Instandsetzungsanordnung. Im Extremfall: Treuhänder oder Enteignung."},
]

# Mehr BGB - Schuldrecht Kauf
BGB_KAUFRECHT = [
    {"paragraph": "§ 433 BGB", "titel": "Vertragstypische Pflichten beim Kaufvertrag", "inhalt": "Durch den Kaufvertrag wird der Verkäufer einer Sache verpflichtet, dem Käufer die Sache zu übergeben und das Eigentum an der Sache zu verschaffen. Der Verkäufer hat dem Käufer die Sache frei von Sach- und Rechtsmängeln zu verschaffen. Der Käufer ist verpflichtet, dem Verkäufer den vereinbarten Kaufpreis zu zahlen und die gekaufte Sache abzunehmen."},
    {"paragraph": "§ 434 BGB", "titel": "Sachmangel", "inhalt": "Die Sache ist frei von Sachmängeln, wenn sie bei Gefahrübergang die vereinbarte Beschaffenheit hat. Soweit die Beschaffenheit nicht vereinbart ist, ist die Sache frei von Sachmängeln, wenn sie sich für die nach dem Vertrag vorausgesetzte Verwendung eignet, ansonsten wenn sie sich für die gewöhnliche Verwendung eignet und eine Beschaffenheit aufweist, die bei Sachen der gleichen Art üblich ist."},
    {"paragraph": "§ 437 BGB", "titel": "Rechte des Käufers bei Mängeln", "inhalt": "Ist die Sache mangelhaft, kann der Käufer, wenn die Voraussetzungen der folgenden Vorschriften vorliegen und soweit nicht ein anderes bestimmt ist: nach § 439 Nacherfüllung verlangen, nach §§ 440, 323 und 326 von dem Vertrag zurücktreten oder nach § 441 den Kaufpreis mindern und nach §§ 440, 280, 281, 283 und 311a Schadensersatz verlangen."},
    {"paragraph": "§ 438 BGB", "titel": "Verjährung der Mängelansprüche", "inhalt": "Die Ansprüche wegen Mängeln verjähren bei einem Bauwerk in 5 Jahren, bei einer Sache, die entsprechend ihrer üblichen Verwendungsweise für ein Bauwerk verwendet worden ist, in 5 Jahren, im Übrigen in 2 Jahren. Die Verjährung beginnt bei Grundstücken mit der Übergabe, im Übrigen mit der Ablieferung der Sache."},
    {"paragraph": "§ 439 BGB", "titel": "Nacherfüllung", "inhalt": "Der Käufer kann als Nacherfüllung nach seiner Wahl die Beseitigung des Mangels oder die Lieferung einer mangelfreien Sache verlangen. Der Verkäufer hat die zum Zwecke der Nacherfüllung erforderlichen Aufwendungen zu tragen. Der Verkäufer kann die vom Käufer gewählte Art der Nacherfüllung verweigern, wenn sie nur mit unverhältnismäßigen Kosten möglich ist."},
    {"paragraph": "§ 440 BGB", "titel": "Besondere Voraussetzungen für Schadensersatz und Rücktritt", "inhalt": "Außer in den Fällen des § 281 Absatz 2 und des § 323 Absatz 2 bedarf es der Fristsetzung auch dann nicht, wenn der Verkäufer beide Arten der Nacherfüllung verweigert oder wenn die dem Käufer zustehende Art der Nacherfüllung fehlgeschlagen oder ihm unzumutbar ist. Eine Nachbesserung gilt nach dem erfolglosen zweiten Versuch als fehlgeschlagen."},
    {"paragraph": "§ 441 BGB", "titel": "Minderung", "inhalt": "Statt zurückzutreten, kann der Käufer den Kaufpreis durch Erklärung gegenüber dem Verkäufer mindern. Die Minderung erfolgt durch Herabsetzung des Kaufpreises in dem Verhältnis, in welchem zur Zeit des Vertragsschlusses der Wert der Sache in mangelfreiem Zustand zu dem wirklichen Wert gestanden haben würde."},
    {"paragraph": "§ 444 BGB", "titel": "Haftungsausschluss", "inhalt": "Auf eine Vereinbarung, durch welche die Rechte des Käufers wegen eines Mangels ausgeschlossen oder beschränkt werden, kann sich der Verkäufer nicht berufen, soweit er den Mangel arglistig verschwiegen oder eine Garantie für die Beschaffenheit der Sache übernommen hat."},
]

# Mehr Mietminderungstabelle
MIETMINDERUNG_TABELLE = [
    {"mangel": "Heizungsausfall im Winter", "minderung": "70-100%", "inhalt": "Bei Totalausfall der Heizung im Winter ist eine Mietminderung von 70-100% angemessen. Voraussetzung: Der Mieter hat den Mangel angezeigt. Die Höhe hängt von der Außentemperatur und der Dauer des Ausfalls ab."},
    {"mangel": "Warmwasserausfall", "minderung": "10-20%", "inhalt": "Fehlt warmes Wasser komplett, ist eine Minderung von etwa 10-20% gerechtfertigt. Bei nur zeitweisem Ausfall entsprechend weniger. Der Vermieter muss unverzüglich für Reparatur sorgen."},
    {"mangel": "Schimmel in Wohnräumen", "minderung": "10-50%", "inhalt": "Je nach Ausmaß und betroffenen Räumen: 10% bei geringem Befall in Nebenräumen bis 50% bei starkem Befall in Wohn- oder Schlafräumen. Gesundheitsgefährdung erhöht den Minderungssatz."},
    {"mangel": "Lärmbelästigung durch Bauarbeiten", "minderung": "10-30%", "inhalt": "Bei erheblichem Baulärm in unmittelbarer Nähe: 10-30% Minderung möglich. Maßgeblich: Dauer, Intensität und Tageszeit. Üblicher innerstädtischer Baulärm wird eher hingenommen."},
    {"mangel": "Aufzug defekt", "minderung": "5-20%", "inhalt": "Bei dauerhaftem Aufzugsausfall: 5-20% je nach Etage und körperlicher Beeinträchtigung des Mieters. In der Regel 3% pro Etage als Richtwert. Für Gehbehinderte höher."},
    {"mangel": "Fenster undicht", "minderung": "5-15%", "inhalt": "Undichte Fenster, die zu Zugluft und erhöhtem Energieverbrauch führen: 5-15% Minderung. Bei Wassereinbruch bei Regen höhere Minderung. Auch erhöhte Heizkosten sind ersatzfähig."},
    {"mangel": "Küche nicht nutzbar", "minderung": "20-30%", "inhalt": "Bei kompletter Unbenutzbarkeit der Küche (z.B. Wasserschaden, defekter Herd bei vermieteter Einbauküche): 20-30% Minderung. Nur zeitweise Einschränkungen entsprechend weniger."},
    {"mangel": "Bad nicht nutzbar", "minderung": "30-50%", "inhalt": "Kompletter Ausfall des Badezimmers (kein Wasser, keine Toilette): 30-50% Minderung. Bei teilweiser Einschränkung (nur Dusche defekt) entsprechend weniger: 10-20%."},
    {"mangel": "Ungeziefer (Kakerlaken, Ratten)", "minderung": "20-100%", "inhalt": "Bei Ungezieferbefall: Je nach Art und Ausmaß 20-100%. Kakerlaken: 15-30%, Ratten: 30-80%, bei Gesundheitsgefährdung bis 100%. Der Vermieter muss sofort handeln."},
    {"mangel": "Wohnungsgröße weicht ab", "minderung": "Prozentual zur Abweichung", "inhalt": "Weicht die tatsächliche Wohnfläche um mehr als 10% von der vereinbarten Fläche ab, kann die Miete proportional gemindert werden. Beispiel: 15% zu klein = 15% Mietminderung."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Sozialwohnungen
    for item in SOZIALWOHNUNGEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Sozialwohnungen", "title": item['titel']}})
    
    # Mietpreisregulierung
    for item in MIETPREISREGULIERUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Mietpreisbremse", "title": item['titel']}})
    
    # Zweckentfremdung
    for item in ZWECKENTFREMDUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Zweckentfremdung", "title": item['titel']}})
    
    # BGB Kaufrecht
    for item in BGB_KAUFRECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Kaufrecht", "title": item['titel']}})
    
    # Mietminderungstabelle
    for item in MIETMINDERUNG_TABELLE:
        text = f"Mietminderung bei: {item['mangel']} - {item['minderung']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"Mietminderung: {item['mangel']}", "type": "Praxiswissen", "category": "Mietminderung", "title": item['mangel']}})
    
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
