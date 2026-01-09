#!/usr/bin/env python3
"""
Moderne Rechtspraxis: 30+ neue Themen
- ESG-Kriterien in der Immobilienwirtschaft
- Klimaschutz und Recht
- Digitalisierung im Immobilienrecht
- Pandemie-Auswirkungen
"""

import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai
import time

QDRANT_HOST = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlem9zIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    result = genai.embed_content(model="models/embedding-001", content=text[:8000], task_type="retrieval_document")
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# ESG-Kriterien (Environmental, Social, Governance)
ESG_IMMOBILIEN = [
    {"thema": "Taxonomie-Verordnung Immobilien", "inhalt": "EU-Taxonomie definiert nachhaltige Immobilieninvestitionen. Kriterien: Energieeffizienz (PEB < 10% der lokalen Gebäude), Kreislaufwirtschaft, Biodiversitätsschutz. Do-no-significant-harm Prinzip. Offenlegungspflichten für institutionelle Investoren. Finanzierungsvorteile für taxonomie-konforme Gebäude."},
    
    {"thema": "ESG-Due-Diligence bei Immobilienkauf", "inhalt": "ESG-Prüfung umfasst Umwelt-, Sozial- und Governance-Aspekte. Umwelt: Energieausweis, CO2-Bilanz, Schadstoffe. Sozial: Mieterstruktur, Barrierefreiheit, Quartiersentwicklung. Governance: Compliance, Transparenz, Stakeholder-Management. ESG-Scores beeinflussen Finanzierungskonditionen."},
    
    {"thema": "Green Buildings Zertifizierung", "inhalt": "Zertifizierungssysteme: DGNB, BREEAM, LEED. Bewertungskriterien: Energieeffizienz, Materialien, Wasserverbrauch, Innenraumqualität. Lebenszyklus-Betrachtung von der Planung bis zum Abriss. Mehrwert durch niedrigere Betriebskosten und höhere Vermietbarkeit. Investoren bevorzugen zertifizierte Gebäude."},
    
    {"thema": "Social Impact Immobilien", "inhalt": "Soziale Nachhaltigkeit umfasst bezahlbaren Wohnraum, Quartiersentwicklung und soziale Infrastruktur. Impact Investing mit messbaren sozialen Zielen. Genossenschaftsmodelle und Community Land Trusts. Partizipative Stadtentwicklung mit Bürgerbeteiligung. ESG-Reporting zu sozialen KPIs."},
]

# Klimaschutz im Immobilienrecht
KLIMASCHUTZ_RECHT = [
    {"thema": "CO2-Bepreisung und Immobilien", "inhalt": "CO2-Preis seit 2021 für Heizöl und Gas. Aufteilung zwischen Mieter und Vermieter je nach Gebäudeeffizienz. Schlechte Effizienz = höherer Vermieteranteil. Anreiz für energetische Sanierung. Preisanstieg bis 2025 auf 55€/t CO2 geplant. Lenkungswirkung für Investitionen."},
    
    {"thema": "Heizungsverbot und GEG-Verschärfung", "inhalt": "Ab 2024 nur noch Heizungen mit 65% erneuerbaren Energien in Neubaugebieten. Bestandsgebäude: Übergangsfristen bis kommunale Wärmeplanung. Wärmepumpen, Fernwärme oder Hybridlösungen erforderlich. Förderung über BEG. Reparaturen alter Heizungen weiter möglich."},
    
    {"thema": "Klimaanpassung in der Stadtplanung", "inhalt": "Klimaanpassung wird planungsrechtlich relevant. Überflutungsvorsorge durch Retentionsflächen. Hitzevorsorge durch Grünflächen und Beschattung. Starkregenvorsorge in der Entwässerungsplanung. Versicherung gegen Elementarschäden. Bauleitplanung berücksichtigt Klimarisiken."},
    
    {"thema": "Klimaklagen und Immobilienrecht", "inhalt": "Klimaklagen können Planungsverfahren beeinflussen. Grundrechte auf Leben und Gesundheit vs. Eigentum. Klimaschutz als verfassungsrechtliches Staatsziel. Generationengerechtigkeit im Umweltrecht. Immobilienindustrie unter verschärftem Rechtfertigungsdruck für klimaschädliche Projekte."},
]

# Digitalisierung
DIGITALISIERUNG = [
    {"thema": "Digitale Hausverwaltung", "inhalt": "PropTech-Lösungen digitalisieren Hausverwaltung. Digitale Nebenkostenabrechnung mit Fotodokumentation. Online-Mieterportale für Beschwerden und Services. Smart-Meter für automatische Verbrauchsablesung. Datenschutz nach DSGVO beachten. Effizienzsteigerung bei Personalkosten."},
    
    {"thema": "Virtuelle Besichtigungen", "inhalt": "VR-Besichtigungen reduzieren Präsenztermine. 360°-Rundgänge und 3D-Modelle. Rechtlich: Fernabsatzrecht bei Online-Vermietung nicht anwendbar. Besichtigungsrecht bleibt bestehen. Virtuelle Besichtigung ersetzt nicht physische Übergabe. Haftung bei irreführender Darstellung."},
    
    {"thema": "KI in der Mieterauswahl", "inhalt": "KI-Tools bewerten Mieterqualität anhand von Daten. Rechtsprobleme: Diskriminierungsverbot, DSGVO-Konformität, Transparenz der Algorithmen. Entscheidungslogik muss nachvollziehbar sein. Bias in Algorithmen vermeiden. Menschliche Letztentscheidung empfohlen."},
    
    {"thema": "Blockchain Mietverträge", "inhalt": "Smart Contracts automatisieren Mietverträge. Automatische Mietauszahlung bei Bedingungserfüllung. Rechtsprobleme: AGB-Recht, Widerrufsrechte, Gerichtsstand. Deutsche Rechtsprechung zu Smart Contracts noch unklar. Notarielle Beurkundung bei Grundstücken weiter erforderlich."},
]

# Pandemie-Auswirkungen
PANDEMIE_RECHT = [
    {"thema": "Home-Office und Mietrecht", "inhalt": "Verstärkte Home-Office-Nutzung verändert Wohnansprüche. Arbeitszimmer-Bedarf steigt. Lärmproblematik bei Online-Meetings. Energiekosten-Anstieg durch Ganztags-Nutzung. Vermieter kann Home-Office nicht untersagen. Gewerbliche Nutzung bei reinem Home-Office meist unproblematisch."},
    
    {"thema": "Mietstundungen Corona", "inhalt": "Zeitweilige Stundungsmöglichkeiten während Lockdowns. Keine Kündigung wegen Corona-bedingter Mietschulden möglich gewesen. Nachzahlungspflicht bis Juni 2022. Härtefallregelungen für besonders Betroffene. Vermieter konnten staatliche Hilfen beantragen."},
    
    {"thema": "Hygieneschutz in Gemeinschaftsräumen", "inhalt": "Pandemie erforderte Anpassung der Hausordnung. Lüftungskonzepte in geschlossenen Räumen. Reinigungsintervalle erhöht. Nutzungsbeschränkungen in Gemeinschaftsräumen. Kosten als Betriebskosten umlegbar. Mieter können angemessene Schutzmaßnahmen verlangen."},
    
    {"thema": "Immobilienmarkt Post-Corona", "inhalt": "Stadtflucht und Nachfrage nach Umland-Immobilien. Büroflächenbedarf reduziert durch Home-Office. Einzelhandelsimmobilien unter Druck. Logistikimmobilien profitieren von E-Commerce-Boom. Wohnungsmarkt regional stark unterschiedlich entwickelt."},
]

# Weitere Spezialthemen
WEITERE_THEMEN = [
    {"thema": "Micro-Apartments und Wohnungsnot", "inhalt": "Micro-Apartments als Antwort auf Wohnungsknappheit. Mindestgrößen nach Landesbauordnung beachten. Funktionalität wichtiger als Größe. Rechtlich wie normale Mietwohnungen behandelt. Möblierung oft Standard. Zielgruppe: Singles, Studenten, Pendler."},
    
    {"thema": "Quartiersmanagement rechtlich", "inhalt": "Quartiersmanagement koordiniert Stadtentwicklung. Rechtlicher Rahmen durch Städtebauförderung. Partizipation der Bewohner rechtlich gewährleistet. Sanierungsrecht und Soziale Stadt Programme. Aufwertung vs. Verdrängung (Gentrifizierung). Mitwirkungspflichten der Eigentümer."},
    
    {"thema": "Serviced Apartments rechtlich", "inhalt": "Serviced Apartments zwischen Hotel und Wohnung. Rechtlich meist als gewerbliche Vermietung einzuordnen. Gewerbesteuer und Umsatzsteuer relevant. Mietrecht nur eingeschränkt anwendbar. All-inclusive-Preise üblich. Brandschutz wie bei Hotels. Konzessionspflicht möglich."},
    
    {"thema": "Urban Mining Immobilien", "inhalt": "Urban Mining nutzt Gebäude als Rohstofflager. Kreislaufwirtschaft im Bauwesen. Rückbaubarkeit in der Planung berücksichtigen. Materialpass dokumentiert verbaute Stoffe. Rechtlich: Abfallrecht vs. Produktrecht. Recycling-Quote im Baurecht steigend. Ressourcenpass für Gebäude geplant."},
    
    {"thema": "Wohnungstausch und Sharing Economy", "inhalt": "Wohnungstausch-Plattformen vermitteln temporäre Wechsel. Rechtlich kompliziert bei regulären Mietverträgen. Vermieter-Zustimmung meist erforderlich. Haftung bei Schäden ungeklärt. Steuerliche Behandlung bei entgeltlichem Tausch. Versicherungsschutz prüfen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(
        host=QDRANT_HOST, 
        port=QDRANT_PORT, 
        api_key=QDRANT_API_KEY, 
        https=True,
        timeout=60.0
    )
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # ESG-Kriterien
    for item in ESG_IMMOBILIEN:
        text = f"ESG-Kriterien Immobilien: {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"ESG {item['thema']}", 
                "type": "Nachhaltigkeit", 
                "category": "ESG", 
                "title": item['thema']
            }
        })
    
    # Klimaschutz
    for item in KLIMASCHUTZ_RECHT:
        text = f"Klimaschutz im Immobilienrecht: {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"Klimaschutz {item['thema']}", 
                "type": "Umweltrecht", 
                "category": "Klimaschutz", 
                "title": item['thema']
            }
        })
    
    # Digitalisierung
    for item in DIGITALISIERUNG:
        text = f"Digitalisierung Immobilienrecht: {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"Digital {item['thema']}", 
                "type": "PropTech", 
                "category": "Digitalisierung", 
                "title": item['thema']
            }
        })
    
    # Pandemie
    for item in PANDEMIE_RECHT:
        text = f"Pandemie-Auswirkungen: {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"COVID-19 {item['thema']}", 
                "type": "Sonderrecht", 
                "category": "Pandemie", 
                "title": item['thema']
            }
        })
    
    # Weitere Themen
    for item in WEITERE_THEMEN:
        text = f"Modernes Immobilienrecht: {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"Modern {item['thema']}", 
                "type": "Moderne Trends", 
                "category": "Zukunft", 
                "title": item['thema']
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
                payload={"text": doc["text"], **doc["metadata"]}
            ))
            if (i + 1) % 4 == 0: 
                print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler bei Dokument {i}: {e}")
            time.sleep(1)  # Rate limiting
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()