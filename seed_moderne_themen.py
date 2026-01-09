#!/usr/bin/env python3
"""
Schneller Batch: 40 hochwertige Dokumente
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

# Schnelle wichtige Ergänzungen
WICHTIGE_ERGAENZUNGEN = [
    {"titel": "VOB/B: Grundlagen Bauvertragsrecht", "inhalt": "Die VOB/B (Vergabe- und Vertragsordnung für Bauleistungen Teil B) regelt die Durchführung von Bauverträgen. Sie gilt nur bei ausdrücklicher Vereinbarung. Vorteile: Präzise Regelungen für Bauleistungen, verkürzte Gewährleistungsfristen (4 statt 5 Jahre). Nachteile: Verschärfte Kündigungsregeln, eingeschränkte Minderungsrechte."},
    {"titel": "HOAI: Honorarordnung für Architekten", "inhalt": "Die HOAI regelt die Vergütung von Architekten und Ingenieuren. Seit 2019 sind die Mindest- und Höchstsätze nicht mehr verbindlich (EuGH-Urteil). Die 9 Leistungsphasen bleiben maßgeblich. Vergütung richtet sich nach anrechenbaren Kosten, Honorarzone und Schwierigkeitsgrad."},
    {"titel": "Schwarzarbeit am Bau: Rechtliche Folgen", "inhalt": "Schwarzarbeit ist strafbar und führt zu Nachzahlungen bei Sozialversicherung und Steuern. Der Auftraggeber hafft für nicht abgeführte Sozialversicherungsbeiträge (§ 28e SGB IV). Gewährleistungsansprüche können entfallen. Die Zahlung kann zurückgefordert werden (§ 817 S. 2 BGB)."},
    {"titel": "Bauabnahme: Rechtliche Bedeutung", "inhalt": "Die Abnahme ist die Billigung der Bauleistung als im Wesentlichen vertragsgemäß. Mit der Abnahme geht die Beweislast für Mängel auf den Auftraggeber über, die Gewährleistung beginnt, der Werklohnanspruch wird fällig. Verweigerung nur bei wesentlichen Mängeln zulässig."},
    {"titel": "Bauhandwerkersicherungshypothek § 648 BGB", "inhalt": "Bauhandwerker haben ein gesetzliches Pfandrecht an dem errichteten Bauwerk. Die Sicherungshypothek muss im Grundbuch eingetragen werden. Sie sichert Werklohnansprüche ab. Rang: Meist nachrangig zu Bankfinanzierungen. Löschung nach vollständiger Bezahlung."},
    {"titel": "EnEV vs. GEG: Was änderte sich?", "inhalt": "Das Gebäudeenergiegesetz (GEG) löste 2020 die Energieeinsparverordnung (EnEV) ab. Es führt EnEV, EEWärmeG und Teile des EEG zusammen. Änderungen: Vereinfachte Bestimmungen, Innovations­klausel für neue Technologien, Berücksichtigung erneuerbarer Energien bei der Bilanzierung."},
    {"titel": "KfW-Förderung: BEG vs. alte Programme", "inhalt": "Die Bundesförderung für effiziente Gebäude (BEG) ersetzt seit 2021 die KfW-Programme. BEG WG für Wohngebäude, BEG NWG für Nichtwohngebäude, BEG EM für Einzelmaßnahmen. Förderung als Kredit oder Zuschuss. Kombinierbar mit steuerlicher Förderung bei selbstgenutzten Immobilien."},
    {"titel": "Grundsteuerreform 2025: Was ändert sich?", "inhalt": "Ab 2025 wird die Grundsteuer auf Basis neuer Bewertungen erhoben. Statt Einheitswerte: Grundsteuerwerte nach Bundesmodell oder Ländermodellen. Die meisten Länder übernehmen das Bundesmodell mit Bodenwert, Nettokaltmiete/Gebäudewert und statistischem Kostenfaktor."},
    {"titel": "Barrierefreies Bauen: DIN 18040", "inhalt": "Die DIN 18040 regelt barrierefreies Planen und Bauen. Teil 1: Öffentliche Gebäude, Teil 2: Wohnungen, Teil 3: Verkehrsanlagen. Anforderungen: Schwellenlose Zugänge, ausreichende Bewegungsflächen, unterfahrbare Einrichtungen. In den Landesbauordnungen teilweise verbindlich."},
    {"titel": "Elektromobilität: GEIG und Ladeinfrastruktur", "inhalt": "Das Gebäude-Elektromobilitätsinfrastruktur-Gesetz (GEIG) verpflichtet zur Vorrüstung für Ladepunkte. Neubauten ab 5 Stellplätzen: Leitungsinfrastruktur für jeden Stellplatz. Bestand ab 20 Stellplätzen: Mindestens ein Ladepunkt bis 2025. Wohngebäude: Jeder 5. Stellplatz vorrüsten."},
    {"titel": "Sharing Economy: Rechtliche Einordnung", "inhalt": "Car-Sharing, Bike-Sharing und Co-Working verändern Immobiliennutzung. Mietrechtlich: Ist Sharing Untervermietung? Planungsrechtlich: Sind neue Nutzungsarten zulässig? Steuerrechtlich: Wann liegt gewerbliche Tätigkeit vor? Besonders relevant bei privaten Sharing-Angeboten in Wohngebieten."},
    {"titel": "Smart Home: Rechtliche Aspekte", "inhalt": "Smart Home-Systeme werfen rechtliche Fragen auf: Datenschutz bei vernetzten Geräten, Haftung bei Fehlfunktionen, Gewährleistung bei Software-Updates. Bei Mietverhältnissen: Wer darf Smart Home-Systeme einbauen? Müssen sie bei Auszug entfernt werden? Betriebskosten bei Smart Metering."},
    {"titel": "Airbnb und Zweckentfremdung", "inhalt": "Kurzzeitvermietung über Plattformen wie Airbnb unterliegt oft Zweckentfremdungsverboten. Viele Städte verlangen Registrierung oder Genehmigung. Hamburg: Max. 8 Wochen ohne Genehmigung. Berlin: Registriernummer erforderlich. München: Genehmigungspflicht. Verstöße: Bußgelder bis 500.000 EUR."},
    {"titel": "Digitale Baugenehmigung: eGovernment", "inhalt": "Die Digitalisierung erreicht die Bauämter. Einige Bundesländer bieten bereits digitale Antragsverfahren. Vorteile: Beschleunigung, Transparenz, Wegfall von Medienbrüchen. Herausforderungen: Technische Standards, Rechtssicherheit digitaler Signaturen, Schulung der Mitarbeiter."},
    {"titel": "Photovoltaik auf dem Dach: Rechtsfragen", "inhalt": "PV-Anlagen können als Mieterstrommodell oder Eigenversorgung betrieben werden. Rechtsfragen: Genehmigungspflicht, Denkmalschutz, Nachbarrechte (Blendung), Brandschutz. Bei Eigentumswohnungen: Beschluss der WEG erforderlich. Steuerlich: EEG-Vergütung vs. Eigenverbrauch."},
    {"titel": "Klimawandel und Immobilien", "inhalt": "Der Klimawandel beeinflusst Immobilienwerte durch Extremwetter-Risiken. Juristische Folgen: Versicherbarkeit, Offenbarungspflichten beim Verkauf, verschärfte Umweltauflagen. EU-Taxonomie und ESG-Kriterien beeinflussen Finanzierung. Klimaanpassung wird zu einem neuen Rechtsgebiet."},
    {"titel": "Blockchain und Immobilien", "inhalt": "Blockchain-Technologie könnte Grundbuchwesen revolutionieren. Smart Contracts für automatisierte Abwicklung von Immobilientransaktionen. Tokenisierung von Immobilien für Teilinvestments. Rechtliche Herausforderungen: Rechtssicherheit, Urkundenqualität, Notarpflicht bei Grundstücken."},
    {"titel": "ESG-Kriterien bei Immobilieninvestments", "inhalt": "Environmental, Social, Governance-Kriterien beeinflussen Immobilienfinanzierung. EU-Taxonomie definiert 'grüne' Immobilien. Banken berücksichtigen ESG-Scores bei Finanzierungskonditionen. Berichtspflichten für große Immobilienunternehmen. Stranded Assets bei ineffizienten Gebäuden."},
    {"titel": "Quartiersplanung und Mobilitätswende", "inhalt": "Neue Mobilitätskonzepte erfordern andere Stellplatzkonzepte. Autofreie Quartiere, Mobility Hubs, geteilte Mobilität. Rechtliche Anpassungen: Stellplatzverordnungen, Mobilitätskonzepte als Ersatz für Stellplätze. Herausforderung: Balance zwischen Flexibilität und Verbindlichkeit."},
    {"titel": "Büroimmobilien nach Corona", "inhalt": "Die Pandemie verändert Büronutzung dauerhaft. Homeoffice reduziert Flächenbedarf. Hybride Arbeitsmodelle erfordern flexible Bürokonzepte. Rechtliche Folgen: Mietvertragsanpassungen, Indexmieten bei sinkenden Marktmieten, Umnutzung von Büros zu Wohnraum."},
    {"titel": "PropTech: Technologie in der Immobilienwirtschaft", "inhalt": "Property Technology revolutioniert die Immobilienbranche. Digitale Maklerdienste, automatisierte Bewertungen, virtuelle Besichtigungen. Rechtsfragen: Haftung bei automatisierten Bewertungen, Datenschutz bei digitalen Besichtigungen, Qualifikation von Online-Maklern."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    for item in WICHTIGE_ERGAENZUNGEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Moderne Themen", "title": item['titel']}})
    
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