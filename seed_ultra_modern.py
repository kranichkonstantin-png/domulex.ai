#!/usr/bin/env python3
"""
Push zu 4.000!
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

DOKUMENTE = [
    {"titel": "Künstliche Intelligenz in der Immobilienverwaltung", "inhalt": "KI-Systeme übernehmen Routineaufgaben in der Hausverwaltung: Automatische Nebenkostenabrechnung, Instandhaltungsplanung, Mieterbetreuung. Rechtliche Herausforderungen: Haftung bei KI-Fehlern, Datenschutz, Transparenz von Algorithmen. Mieter haben Recht auf menschliche Überprüfung automatisierter Entscheidungen."},
    
    {"titel": "3D-Druck von Gebäuden", "inhalt": "3D-Betondruck revolutioniert das Bauwesen. Rechtliche Aspekte: Bauaufsichtliche Zulassung neuer Bauverfahren, Haftung bei Konstruktionsfehlern, Gewährleistung bei innovativen Baumethoden. Deutschland hinkt international hinterher, Niederlande genehmigen bereits 3D-gedruckte Wohnhäuser."},
    
    {"titel": "Immobilien-Crowdinvesting", "inhalt": "Crowdinvesting ermöglicht Kleinanlegern Immobilieninvestments. Rechtlicher Rahmen: Vermögensanlagen-Verkaufsprospektverordnung, Kleinanlegerschutzgesetz. Plattformen benötigen Erlaubnis nach KWG oder WpIG. Anleger tragen Totalverlustrisiko. Prospektpflicht ab 2,5 Mio. EUR Emission."},
    
    {"titel": "Modulares Bauen rechtlich", "inhalt": "Modulbauweise ermöglicht schnelle, kostengünstige Errichtung. Rechtlich: Zulassung von Modulen nach Bauregelliste, Gewährleistung bei Systembauweise, Rückbaubarkeit als Vorteil. Modulhersteller haften für Konstruktion, Bauherr für Gesamtgebäude. Brandschutz bei mehrgeschossigen Modulbauten besonders kritisch."},
    
    {"titel": "Smart City Integration Immobilien", "inhalt": "Immobilien werden Teil vernetzter Smart Cities. Datenaustausch zwischen Gebäuden und städtischer Infrastruktur. Rechtliche Fragen: Datenschutz, IT-Sicherheit, Interoperabilität. Kommunen können Smart-City-Standards in Bebauungsplänen festschreiben. Eigentümer müssen Vernetzung meist dulden."},
    
    {"titel": "Algen-Fassaden zur Energiegewinnung", "inhalt": "Bio-Reaktor-Fassaden nutzen Algen zur Energiegewinnung und Dämmung. In Deutschland: BIQ-Haus Hamburg als Pilotprojekt. Rechtlich: Bauordnungsrechtliche Zulassung innovativer Fassadensysteme, Brandschutz, Wartungsaufwand. Algensysteme gelten als regenerative Energiequelle nach EEG."},
    
    {"titel": "Hyperloop-Immobilienentwicklung", "inhalt": "Hyperloop-Verkehrssysteme verändern Immobilienmärkte fundamental. Entfernungen werden irrelevant, ländliche Gebiete attraktiver. Rechtlich: Planfeststellungsverfahren für Hyperloop-Strecken, Lärmschutz, Enteignungsrecht. Immobilienpreise entlang geplanter Strecken bereits volatil."},
    
    {"titel": "Genossenschaften 4.0", "inhalt": "Digitale Plattformen modernisieren Wohnungsgenossenschaften. Online-Partizipation bei Mitgliederversammlungen, digitale Abstimmungen, transparente Kostenstrukturen. Rechtlich: Genossenschaftsgesetz vs. digitale Teilhabe, Satzungsänderungen für Online-Verfahren. Jüngere Mitglieder bevorzugen digitale Beteiligung."},
    
    {"titel": "Klimaanpassung Bestandsgebäude", "inhalt": "Klimawandel erfordert Anpassung bestehender Gebäude: Hitze-, Starkregen- und Sturmschutz. Rechtlich: Verkehrssicherungspflicht der Eigentümer, Versicherungsschutz bei Elementarschäden. Nachrüstpflichten für Klimaanpassung diskutiert. Förderung durch KfW-Programme verfügbar."},
    
    {"titel": "Quantencomputing Gebäudesimulation", "inhalt": "Quantencomputer revolutionieren Gebäudesimulation: Exakte Berechnungen komplexer Systeme. Anwendung: Energieoptimierung, Materialverhalten, Statik. Deutschland investiert in Quantentechnologie-Forschung. Praktische Anwendung noch 10-15 Jahre entfernt. Rechtliche Frameworks fehlen noch völlig."},
    
    {"titel": "Biobasierte Baustoffe rechtlich", "inhalt": "Stroh, Hanf, Pilzmyzel als nachhaltige Baumaterialien. Bauordnungsrechtliche Zulassung oft schwierig. Brandschutznachweis bei organischen Materialien problematisch. EU fördert Forschung zu biobasierten Baustoffen. Kreislaufwirtschaft macht Naturmaterialien attraktiver."},
    
    {"titel": "Drohnen-Gebäudeinspektion", "inhalt": "Drohnen inspizieren schwer zugängliche Gebäudeteile. Vorteile: Kostengünstig, detaillierte Bilder, Sicherheit. Rechtlich: Luftverkehrsrecht, Versicherung, Datenschutz bei Nachbargrundstücken. Thermografie-Drohnen entdecken Energielecks. Wartungsunternehmen setzen Drohnen zunehmend ein."},
    
    {"titel": "Robotic Process Automation Verwaltung", "inhalt": "Software-Roboter automatisieren Verwaltungsabläufe: Mietverträge erstellen, Nebenkostenabrechnung, Mahnwesen. Effizienzsteigerung bis 80% möglich. Rechtlich: Datenschutz, Fehlerhaftung, Arbeitsplätze. Verwalter müssen in Digitalisierung investieren oder Marktanteile verlieren."},
    
    {"titel": "Immobilien-Tokenisierung", "inhalt": "Blockchain ermöglicht Tokenisierung von Immobilienbesitz. Bruchteile von Gebäuden als handelbare Token. Rechtlich: Grundbuchrecht vs. Blockchain, Prospektpflicht, Geldwäscherecht. International bereits erste Projekte. Deutschland prüft rechtliche Rahmenbedingungen für digitale Wertpapiere."},
    
    {"titel": "Vertikale Gärten rechtlich", "inhalt": "Gebäudebegrünung verbessert Mikroklima und Energieeffizienz. Rechtlich: Statische Mehrbelastung, Wasserschäden-Risiko, Wartungspflichten. Förderung durch Kommunen üblich. Brandschutz bei extensiver Begrünung meist unproblematisch. Insektenschutz als positiver Nebeneffekt."},
    
    {"titel": "Mikrowohnen rechtlich", "inhalt": "Wohnungsknappheit führt zu Mikro-Apartments unter 25 qm. Rechtlich: Mindestgrößen nach Landesbauordnung, Funktionalität vs. Fläche. Sanitärausstattung muss vollwertig sein. Möblierung oft Standard. Zielgruppe: Singles, Studenten, Stadtpendler."},
    
    {"titel": "Predictive Maintenance Gebäude", "inhalt": "KI sagt Wartungsbedarf vor Ausfällen vorher. Sensoren überwachen Heizung, Lüftung, Aufzüge kontinuierlich. Kosteneinsparungen durch geplante statt Notfall-Reparaturen. Rechtlich: Datenschutz, Haftung bei Sensor-Ausfällen. Wartungsverträge müssen angepasst werden."},
    
    {"titel": "Sharing Economy Immobilien", "inhalt": "Geteilte Nutzung von Immobilien: Co-Working, Car-Sharing-Plätze, Gemeinschaftsküchen. Rechtlich: Gewerbeordnung vs. private Nutzung, Versicherungsschutz, Betriebskostenabgrenzung. Millennials bevorzugen 'Access over Ownership'. Neue Geschäftsmodelle für Immobilienwirtschaft."},
    
    {"titel": "Wassermanagement Gebäude", "inhalt": "Wassersparen und -recycling in Gebäuden. Grauwasser-Recycling, Regenwassernutzung, wassersparende Armaturen. Rechtlich: Trinkwasserverordnung bei Recycling, Abwassergebühren. Trockenheit macht Wassermanagement wichtiger. Förderung durch Kommunen möglich."},
    
    {"titel": "5G Campusnetze Immobilien", "inhalt": "Private 5G-Netze für Gewerbeimmobilien. Lokale Datenverarbeitung, geringe Latenz für IoT. Rechtlich: Frequenzzuteilung durch BNetzA, Strahlenschutz. Anwendung: Smart Factory, Logistik, Bürokommunikation. Deutschland vergibt lokale 5G-Lizenzen für Unternehmen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    try:
        client = QdrantClient(
            host=QDRANT_HOST, 
            port=QDRANT_PORT, 
            api_key=QDRANT_API_KEY, 
            https=True
        )
        
        info = client.get_collection(COLLECTION_NAME)
        print(f"Dokumente vorher: {info.points_count}")
    except Exception as e:
        print(f"Verbindung fehlgeschlagen: {e}")
        return
    
    all_docs = []
    
    for item in DOKUMENTE:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"{item['titel']}", 
                "type": "Zukunftstechnologie", 
                "category": "Innovation", 
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
                payload={"text": doc["text"], **doc["metadata"]}
            ))
            if (i + 1) % 5 == 0: 
                print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler bei {i}: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()