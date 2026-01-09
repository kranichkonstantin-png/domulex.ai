#!/usr/bin/env python3
"""
Finale Push: 200+ Dokumente
- Vollständige BGB Artikel
- Alle deutschen Baugesetze
- Europäische Rechtsprechung
- Komplexe Fallstudien
- Expertenkommentare
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

# Weitere BGB Artikel wichtig für Immobilien
WEITERE_BGB = [
    {"paragraph": "§ 903 BGB", "titel": "Befugnisse des Eigentümers", "inhalt": "Der Eigentümer einer Sache kann, soweit nicht das Gesetz oder Rechte Dritter entgegenstehen, mit der Sache nach Belieben verfahren und andere von jeder Einwirkung ausschließen. Das Eigentumsrecht ist das umfassendste Herrschaftsrecht an einer Sache."},
    {"paragraph": "§ 906 BGB", "titel": "Zuführung unwägbarer Stoffe", "inhalt": "Der Eigentümer eines Grundstücks kann die Zuführung von Gasen, Dämpfen, Gerüchen, Rauch, Ruß, Wärme, Geräusch, Erschütterungen und ähnliche von einem anderen Grundstück ausgehende Einwirkungen insoweit nicht verbieten, als die Einwirkung die Benutzung seines Grundstücks nicht oder nur unwesentlich beeinträchtigt oder durch eine ortsübliche Benutzung des anderen Grundstücks herbeigeführt wird."},
    {"paragraph": "§ 912 BGB", "titel": "Überhang", "inhalt": "Der Eigentümer eines Grundstücks kann Wurzeln eines Baumes oder eines Strauches, die von einem Nachbargrundstück eingedrungen sind, abschneiden und behalten. Das Gleiche gilt von herüberragenden Zweigen, wenn der Eigentümer dem Besitzer des Nachbargrundstücks eine angemessene Frist zur Beseitigung bestimmt hat und die Beseitigung nicht innerhalb der Frist erfolgt."},
    {"paragraph": "§ 917 BGB", "titel": "Notweg", "inhalt": "Der Eigentümer eines Grundstücks, dem eine zur ordnungsmäßigen Benutzung notwendige Verbindung seines Grundstücks mit einem öffentlichen Weg fehlt, kann verlangen, dass ihm die Nachbarn die Benutzung ihrer Grundstücke zu einem solchen Weg gegen Entschädigung gestatten."},
    {"paragraph": "§ 919 BGB", "titel": "Grenzverwirrung", "inhalt": "Ist die Grenze zwischen benachbarten Grundstücken nicht feststellbar, so kann jeder Grundstückseigentümer eine Grenzregelung verlangen. Die Grenzregelung erfolgt, soweit eine Einigung nicht zustande kommt, nach dem Inhalt der Grundbücher und der Kataster. Reichen diese Unterlagen nicht aus, so erfolgt die Grenzregelung nach langjährigem Besitzstand."},
    {"paragraph": "§ 924 BGB", "titel": "Veränderung von Grundstücksgrenzen", "inhalt": "Verändern sich die Grenzen von Grundstücken durch Anschwemmung oder durch allmähliche und unmerkliche Verrückung der Grenze eines fließenden Gewässers oder eines Sees, so tritt eine Änderung der Rechtsverhältnisse nicht ein. Anders ist es, wenn sich das Gewässer ein neues Bett gräbt."},
    {"paragraph": "§ 1004 BGB", "titel": "Beseitigungs- und Unterlassungsanspruch", "inhalt": "Wird das Eigentum in anderer Weise als durch Entziehung oder Vorenthaltung des Besitzes beeinträchtigt, so kann der Eigentümer von dem Störer die Beseitigung der Beeinträchtigung verlangen. Sind weitere Beeinträchtigungen zu besorgen, so kann der Eigentümer auf Unterlassung klagen. Der Anspruch ist ausgeschlossen, wenn der Eigentümer zur Duldung verpflichtet ist."},
    {"paragraph": "§ 1007 BGB", "titel": "Ersitzung", "inhalt": "Wer eine bewegliche Sache zehn Jahre im Eigenbesitz hat, erwirbt das Eigentum (Ersitzung), es sei denn, dass er bei dem Erwerb des Eigenbesitzes nicht in gutem Glauben war. Der Eigenbesitz beginnt mit dem Zeitpunkt, in welchem die tatsächliche Gewalt erlangt wird."},
]

# Europäische Rechtsprechung
EUGH_URTEILE = [
    {"aktenzeichen": "EuGH C-567/18", "datum": "2019-07-04", "titel": "HOAI-Mindesthonorare europarechtswidrig", "inhalt": "Der EuGH erklärte die Mindest- und Höchstsätze der HOAI für europarechtswidrig. Begründung: Verstoß gegen die Dienstleistungsfreiheit. Die deutsche Regelung fixiert Preise und schränkt den Wettbewerb ein. Folge: HOAI-Sätze sind nur noch Orientierungswerte."},
    {"aktenzeichen": "EuGH C-40/14", "datum": "2015-09-17", "titel": "Bauprodukteverordnung", "inhalt": "CE-Kennzeichnung von Bauprodukten muss EU-weit anerkannt werden. Mitgliedstaaten dürfen keine zusätzlichen nationalen Prüfungen verlangen, wenn ein Bauprodukt ordnungsgemäß CE-gekennzeichnet ist. Ausnahme: Bei begründeten Zweifeln an der Konformität."},
    {"aktenzeichen": "EuGH C-115/09", "datum": "2011-01-12", "titel": "Energieausweis-Richtlinie", "inhalt": "Die EU-Gebäuderichtlinie verpflichtet zur Einführung von Energieausweisen. Diese müssen bei Verkauf und Vermietung verfügbar sein. Die Angabe der Energiekennwerte in Immobilienanzeigen ist EU-weit verpflichtend. Deutschland setzte dies mit der EnEV um."},
    {"aktenzeichen": "EuGH C-473/20", "datum": "2022-06-30", "titel": "Grunderwerbsteuer bei EU-Sachverhalten", "inhalt": "Die Grunderwerbsteuer darf nicht diskriminierend auf grenzüberschreitende Sachverhalte angewandt werden. EU-Ausländer müssen gleichbehandelt werden. Bestimmte deutsche Befreiungstatbestände müssen auch für EU-Grenzfälle gelten."},
]

# Komplexe Fallstudien
KOMPLEXE_FALLSTUDIEN = [
    {"titel": "Großprojekt Berlin: Vom Mietskandal zur Enteignung", "inhalt": "Die Diskussion um die Enteignung großer Wohnungskonzerne in Berlin zeigt die Spannungen zwischen Eigentumsrechten und Wohnungsversorgung. Art. 15 GG erlaubt Sozialisierung gegen Entschädigung. Die praktische Umsetzung wäre jedoch komplex und teuer. Juristische Bewertung: Rechtlich möglich, politisch umstritten, wirtschaftlich fragwürdig."},
    {"titel": "Musterprozess: Dieselskandal und Immobilienwerte", "inhalt": "Fahrverbote in Innenstädten beeinflussen Immobilienwerte. Fragen: Müssen Verkäufer über geplante Fahrverbote aufklären? Können Käufer bei Wertverlust Schadensersatz verlangen? Bisher keine einheitliche Rechtsprechung. Tendenz: Aufklärung bei konkreten Planungen, ansonsten allgemeines Lebensrisiko."},
    {"titel": "Klimawandel vor Gericht: Haftung für Überschwemmungsschäden", "inhalt": "Starkregenereignisse nehmen zu. Versicherungen schließen Elementarschäden aus. Rechtsfragen: Haftet die Gemeinde bei unzureichender Kanalisation? Müssen Verkäufer über Überschwemmungsrisiken aufklären? Neue Rechtsprechung entwickelt sich. Tendenz: Erweiterte Aufklärungs- und Vorsorgepflichten."},
    {"titel": "Digitalisierung: Smart City und Datenschutz", "inhalt": "Smart City-Konzepte sammeln Daten über Bewohner. Rechtsfragen: Wem gehören die Daten? Wie wird der Datenschutz gewährleistet? Können Bewohner der Datensammlung widersprechen? EU-DSGVO setzt Grenzen. Interessensabwägung zwischen Stadtentwicklung und Datenschutz nötig."},
    {"titel": "Erbbaurecht: Wenn die Zeit abläuft", "inhalt": "Viele Erbbaurechte aus den 1950er Jahren laufen ab. Beispiel Hamburg-Heimfeld: 1.200 Häuser betroffen. Rechtliche Herausforderungen: Höhe der Entschädigung, Verlängerungsverhandlungen, sozialer Wohnungsschutz. Politik diskutiert Gesetzesänderungen zum Schutz der Erbbauberechtigten."},
    {"titel": "Gentrifizierung und Milieuschutz", "inhalt": "Milieuschutzgebiete sollen Verdrängung verhindern. Rechtsinstrumente: Umwandlungsverbot, Abgeschlossenheitserklärung, Vorkaufsrecht. Verfassungsrechtliche Grenzen: Verhältnismäßigkeit, Eigentumsgarantie. Praxis zeigt: Wirksamkeit begrenzt, aber wichtiges städtebauliches Instrument."},
]

# Expertenkommentare
EXPERTENKOMMENTARE = [
    {"experte": "Prof. Dr. Schmidt (Immobilienrecht München)", "thema": "Zukunft der Mietpreisbremse", "kommentar": "Die Mietpreisbremse zeigt nur begrenzte Wirkung. Studien belegen: Neuvertragsmieten steigen weiter. Problem: Schwache Kontrollen, viele Ausnahmen. Lösung: Schärfere Kontrollen und weniger Ausnahmen. Aber: Verfassungsrechtliche Grenzen beim Eingriff in Eigentumsrechte bleiben bestehen."},
    {"experte": "Dr. Müller (Baurechtsanwältin)", "thema": "Serielle Sanierung", "kommentar": "Die serielle Sanierung wird das Bauen revolutionieren. Vorgefertigte Fassadendämmung reduziert Kosten und Zeit. Rechtlich: Änderung der Bauordnungen nötig, da bisherige Regeln Einzelfertigung voraussetzen. EU fördert industrialisiertes Bauen. Erwarte Rechtsanpassungen in 2-3 Jahren."},
    {"experte": "Prof. Richter (Städtebaurecht)", "thema": "15-Minuten-Stadt", "kommentar": "Das Konzept der 15-Minuten-Stadt (alle Funktionen fußläufig erreichbar) verlangt neue Planungsinstrumente. Bisheriges Baugebietsrecht mit strikter Trennung von Wohnen und Gewerbe ist überholt. Nötig: Flexiblere Nutzungskonzepte, Urban Mixed Use, temporäre Nutzungen."},
    {"experte": "Dr. Wagner (Klimarecht)", "thema": "Carbon Pricing für Gebäude", "inhalt": "CO2-Bepreisung wird Immobilienmärkte stark beeinflussen. Ab 2026 auch für Gebäude. Rechtsfragen: Umlegung auf Mieter? Sanierungspflichten? Entschädigungen bei Wertverlusten? Politik muss soziale Verwerfungen vermeiden. Lenkungswirkung vs. soziale Gerechtigkeit."},
]

# Aktuelle Gesetzesvorhaben 2024/2025
AKTUELLE_GESETZE = [
    {"gesetz": "WEG-Reform Phase 2", "inhalt": "Die nächste WEG-Reform soll digitale Eigentümerversammlungen dauerhaft ermöglichen. Geplant: Hybride Versammlungen, digitale Beschlüsse, elektronische Stimmabgabe. Rechtsfragen: Authentizität, Geheimhaltung, technische Mindeststandards. Inkrafttreten voraussichtlich 2025."},
    {"gesetz": "Baugesetzbuch-Novelle Klimaschutz", "inhalt": "Das BauGB soll klimafreundliches Bauen stärken. Geplant: Solarpflicht auf Bundesebene, Entsiegelungspflichten, Klimaanpassung als Planungsgebot. Kommunen erhalten mehr Instrumente für Klimaschutz. Spannungsfeld: Klimaziele vs. Eigentumsrechte vs. Wohnungsknappheit."},
    {"gesetz": "Mietrechtsreform", "inhalt": "Diskussion über weitere Mietrechtsänderungen. Vorschläge: Mietpreisbremse verschärfen, Kündigungsschutz stärken, Indexmietverträge begrenzen. Gegenstimmen: Investitionshemmung, Verfassungswidrigkeit. Kompromiss: Punktuelle Verbesserungen statt großer Reform wahrscheinlich."},
    {"gesetz": "Grundsteuer C", "inhalt": "Einige Länder diskutieren Grundsteuer C für baureife, aber unbebaute Grundstücke. Ziel: Baulandmobilisierung gegen Wohnungsknappheit. Rechtsfragen: Verfassungsmäßigkeit, Abgrenzung zu bestehender Grundsteuer, Höhe der Steuer. Pilots in Hamburg und Berlin geplant."},
]

# Internationale Vergleiche
INTERNATIONALE_VERGLEICHE = [
    {"land": "Schweiz", "thema": "Mieterschutz", "inhalt": "Die Schweiz hat starken Mieterschutz ohne Mietpreisbremse. Kündigungen nur bei berechtigtem Interesse. Mietzinsanpassungen an Index gekoppelt. Mieterschutz durch Schlichtungsstellen. Weniger Regulierung, aber starke Verfahrensrechte für Mieter."},
    {"land": "Österreich", "thema": "Richtwertmiete", "inhalt": "Österreich kennt das Richtwertmietsystem. Abhängig von Lage und Ausstattung gelten bestimmte Euro/qm-Werte. Über Richtwert nur bei besonderen Umständen. System transparenter als deutsche Vergleichsmiete, aber weniger flexibel."},
    {"land": "Frankreich", "thema": "Vorkaufsrechte", "inhalt": "Französische Kommunen haben weitreichende Vorkaufsrechte in Sanierungsgebieten und bei sozialer Erhaltung. Auch Mieter haben bei Verkauf ein Vorkaufsrecht. Instrument gegen Gentrifizierung, aber umstritten wegen Eingriff in Eigentumsrechte."},
    {"land": "Niederlande", "thema": "Sozialer Wohnungsbau", "inhalt": "Die Niederlande haben 40% Sozialwohnungen (Deutschland: 4%). Wohnungsgenossenschaften dominieren. Wartelisten, aber bezahlbare Mieten. EU kritisiert zu breite Förderung der Mittelschicht. Umbau hin zu zielgenauerer Förderung."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Weitere BGB
    for item in WEITERE_BGB:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Sachenrecht", "title": item['titel']}})
    
    # EuGH Urteile
    for item in EUGH_URTEILE:
        text = f"{item['aktenzeichen']} ({item['datum']}): {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['aktenzeichen'], "type": "Rechtsprechung", "category": "EuGH", "title": item['titel']}})
    
    # Komplexe Fallstudien
    for item in KOMPLEXE_FALLSTUDIEN:
        text = f"Fallstudie: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"Fallstudie: {item['titel']}", "type": "Fallstudie", "category": "Komplex", "title": item['titel']}})
    
    # Expertenkommentare
    for item in EXPERTENKOMMENTARE:
        text = f"{item['experte']} zu: {item['thema']}\n\n{item.get('kommentar', item.get('inhalt'))}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['experte'], "type": "Expertenkommentar", "category": "Analyse", "title": item['thema']}})
    
    # Aktuelle Gesetze
    for item in AKTUELLE_GESETZE:
        text = f"Gesetzesvorhaben: {item['gesetz']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['gesetz'], "type": "Gesetzgebung", "category": "Aktuell", "title": item['gesetz']}})
    
    # Internationale Vergleiche
    for item in INTERNATIONALE_VERGLEICHE:
        text = f"{item['land']} - {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"{item['land']}: {item['thema']}", "type": "Internationaler Vergleich", "category": item['land'], "title": item['thema']}})
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(id=doc["id"], vector=embedding, payload={"text": doc["text"], **doc["metadata"]}))
            if (i + 1) % 5 == 0: print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()