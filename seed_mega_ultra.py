#!/usr/bin/env python3
"""
ULTRA MEGA PUSH ZU 4.000!
30 neue Bereiche: Sport, Bildung, Kultur, Industrie 4.0, Logistik, Energie
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

ALLE_NEUEN_DOCS = [
    # Sportimmobilien
    {"titel": "Fußballstadien als Mehrzweckarenen", "inhalt": "Moderne Stadien funktionieren als Event-Locations. Außerhalb der Saison: Konzerte, Messen, Firmenevents. Rechtlich: Versammlungsstättenverordnung für verschiedene Nutzungen. Lärmschutz bei Konzerten vs. Fußball unterschiedlich. Parken und Verkehr bei unterschiedlichen Veranstaltungsarten. Naming Rights und Sponsoring-Verträge."},
    
    {"titel": "Fitnessstudio-Ketten Expansion", "inhalt": "McFit, FitX etc. suchen standardisierte Standorte. Mindestfläche 800-1200 qm, hohe Decken für Geräte. 24/7-Öffnung erfordert Sicherheitstechnik. Schallschutz für Cardio-Bereich und Kurse. Duschen/Umkleiden mit Hygienestandards. Franchising-Modelle mit einheitlichen Standards."},
    
    {"titel": "E-Sports-Arenas als Zukunftsimmobilien", "inhalt": "E-Sports wächst rasant, spezialisierte Venues entstehen. Hochleistungs-Internet und Gaming-PCs. Klimatisierung wegen Hardware-Abwärme. Streaming-Technik für Live-Übertragungen. Jugendschutz bei Gewalt-Spielen. Sponsoring durch Gaming-Industrie. Gastronomie für Gaming-Sessions."},
    
    {"titel": "Kletterhallen Indoor-Boom", "inhalt": "Bouldern und Sportklettern sehr beliebt. Höhe mindestens 4,5m für Bouldering, 15m+ für Klettern. Spezielle Fallschutz-Matten erforderlich. Versicherung gegen Kletter-Unfälle kritisch. Kindergeburtstage und Firmen-Events als Zusatzgeschäft. Aufstieg in städtischen Gebieten statt Natur."},
    
    # Bildungsimmobilien
    {"titel": "Internationale Schulen Deutschland", "inhalt": "Wachsende Expat-Community benötigt internationale Schulen. Unterricht in englischer oder anderen Sprachen. Anerkennung von Abschlüssen komplex. Schulgeld 10.000-30.000 EUR pro Jahr. Campus-ähnliche Anlagen mit Sport und Kultur. Lehrpersonal oft aus Herkunftsländern."},
    
    {"titel": "Volkshochschulen als Immobilienprojekte", "inhalt": "VHS modernisieren ihre Standorte. Erwachsenenbildung in flexiblen Räumen. Integration von Digitalem Lernen erforderlich. Barrierefreiheit für ältere Lernende wichtig. Abendkurse erfordern sichere Parkplätze. Kooperationen mit anderen Bildungsträgern."},
    
    {"titel": "Musikschulen schalltechnisch", "inhalt": "Private Musikschulen wachsen stark. Schallschutz zwischen Übungsräumen essentiell. Flügel erfordern stabile Böden und Klimatisierung. Bands und Schlagzeug besonders lärmintensiv. Nachbarn oft gestört, Standortwahl kritisch. GEMA-Gebühren bei Aufführungen und Konzerten."},
    
    {"titel": "Sprachschulen für Business English", "inhalt": "Firmentrainings in modernen Schulungsräumen. Zentrale Lage für Berufstätige wichtig. Flexible Kurszeiten auch abends/weekends. Digitale Ausstattung für Online-Kurse. Berlitz, Wall Street English als Franchise-Systeme. Integration mit Video-Konferenz-Technik."},
    
    # Kulturimmobilien
    {"titel": "Pop-Up Galerien in Leerständen", "inhalt": "Leerstehende Geschäfte werden temporär zu Galerien. Zwischennutzung belebt Innenstädte. Kunstszene nutzt günstige Mieten für Ausstellungen. Sicherheitstechnik für wertvolle Kunstwerke. Versicherung bei temporären Standorten kompliziert. Stadtmarketing unterstützt Kulturnutzung."},
    
    {"titel": "Konzertsäle akustisch perfekt", "inhalt": "Akustik ist bei Konzertsälen alles entscheidend. Nachträgliche Korrekturen extrem teuer. Elbphilharmonie als Referenzprojekt. Lärmschutz zur Umgebung bei Rock/Pop-Konzerten. Variable Akustik für verschiedene Musikstile. Parken bei ausverkauften Konzerten problematisch."},
    
    {"titel": "Museen mit Erlebnischarakter", "inhalt": "Moderne Museen setzen auf Interaktivität. Virtual Reality und digitale Installationen. Klimatisierung für empfindliche Exponate. Sicherheitstechnik gegen Kunstdiebstahl. Shop und Gastronomie als Zusatzeinkommen. Barrierefreiheit für alle Besuchergruppen."},
    
    {"titel": "Bibliotheken als Community Centers", "inhalt": "Bibliotheken wandeln sich zu sozialen Treffpunkten. Co-Working-Spaces mit WLAN und Strom. Veranstaltungsräume für Lesungen und Vorträge. Café-Integration für längere Aufenthalte. Kinderbereich mit Spielecken. Digitalisierung reduziert physische Buchbestände."},
    
    # Industrie 4.0
    {"titel": "Smart Factory Vernetzung", "inhalt": "Industrie 4.0 vernetzt alle Produktionselemente. 5G-Campusnetze für Echtzeit-Kommunikation. Predictive Maintenance reduziert Ausfallzeiten. Cybersecurity wird kritischer Faktor. Flexible Produktionslinien für Mass Customization. Mitarbeiter arbeiten mit Robotern kollaborativ zusammen."},
    
    {"titel": "Automatisierte Hochregallager", "inhalt": "Vollautomatische Lager ohne menschliche Mitarbeiter. Roboter kommissionieren 24/7. Höhere Lagerkapazität durch optimale Raumnutzung. Brandschutz bei engen Gängen herausfordernd. Software steuert komplette Logistik. Schnellere Auftragsabwicklung für E-Commerce."},
    
    {"titel": "Rechenzentren Edge Computing", "inhalt": "Dezentrale Mini-Rechenzentren näher beim Nutzer. Latenzzeiten unter 10ms für Autonome Autos. 5G-Integration für Mobile Edge Computing. Abwärme-Nutzung für Gebäude-Heizung. Glasfaser-Anbindung mit hoher Redundanz. Sicherheit gegen physische und Cyber-Angriffe."},
    
    {"titel": "3D-Druck Produktionshallen", "inhalt": "Additive Manufacturing revolutioniert Produktion. Große 3D-Drucker für Bauteile und Prototyping. Metall-Pulver erfordert Explosion-Schutz. Nachbearbeitung der gedruckten Teile. Design-to-Print verkürzt Entwicklungszeiten. On-Demand-Produktion reduziert Lagerhaltung."},
    
    # Logistik & E-Commerce
    {"titel": "Last-Mile-Hubs in Städten", "inhalt": "Innenstädtische Mini-Verteilzentren für schnelle Lieferung. E-Bike und E-Transporter für emissionsfreie Zustellung. Mikro-Fulfillment in Kellern und Parkgaragen. Same-Day-Delivery als Kundenerwartung. Konflikt mit Anwohnern wegen Lieferverkehr. Kooperationen zwischen verschiedenen Paketdiensten."},
    
    {"titel": "Amazon Fresh Lebensmittel-Logistik", "inhalt": "Gekühlte Lagerung und Transport von Lebensmitteln. Temperaturen konstant unter 4°C für Frische. Schnelle Rotation bei kurzen Haltbarkeiten. Hygiene-Standards wie bei Lebensmittelproduzenten. 2-Stunden-Lieferung erfordert lokale Lager. Verpackung ohne Plastik zunehmend gefordert."},
    
    {"titel": "Paketstation-Netzwerk", "inhalt": "DHL Packstationen und Amazon Lockers überall. 24/7-Verfügbarkeit für berufstätige Kunden. Integration in Supermärkte, Tankstellen, Bahnhöfe. Vandalismus-schutz und Diebstahl-Prävention. Größere Pakete erfordern größere Fächer. Smartphone-App für Paket-Management."},
    
    {"titel": "Drohnen-Lieferung rechtlich", "inhalt": "Zukunft der Paket-Zustellung per Drohne. Luftverkehrsrecht noch nicht angepasst. Landeplätze auf Hausdächern geplant. Kollision-Gefahr mit bemannter Luftfahrt. Wetterabhängigkeit begrenzt Einsatztage. Batterie-Reichweite für maximal 20km. Lärmbelastung durch Rotoren problematisch."},
    
    # Energieimmobilien  
    {"titel": "Solarpanels auf Gewerbeimmobilien", "inhalt": "Große Dachflächen optimal für Photovoltaik. Eigenverbrauch senkt Stromkosten erheblich. Überschussstrom ins Netz gegen Vergütung. Statik prüfen vor Installation erforderlich. 20-25 Jahre Lebensdauer der Module. Wartung und Reinigung für optimalen Ertrag."},
    
    {"titel": "Windkraft-Anlagen Offshore", "inhalt": "Offshore-Windparks in Nord- und Ostsee. Höhere und konstantere Windgeschwindigkeiten. Seekabel für Strom-Transport ans Festland. Wartung bei rauher See schwierig. Umweltauswirkungen auf Meeresökosystem. Akzeptanz höher als bei Onshore-Anlagen."},
    
    {"titel": "Batteriespeicher-Farmen", "inhalt": "Großbatterien stabilisieren schwankende Erneuerbaren-Energie. Lithium-Ionen oder neue Technologien. Brandschutz wegen thermischer Probleme kritisch. Integration in bestehende Umspannwerke. Regelenergie-Vermarktung als Geschäftsmodell. Recycling nach 10-15 Jahren Nutzung."},
    
    {"titel": "Wasserstoff-Elektrolyse-Anlagen", "inhalt": "Power-to-Gas wandelt überschüssigen Strom in Wasserstoff. Hochdruck-Speicherung oder Verflüssigung. Transport per Pipeline oder Trailer. Sicherheitsvorschriften strenger als bei Erdgas. Industrielle Abnehmer für chemische Prozesse. Tankstellen für Wasserstoff-Fahrzeuge."},
    
    {"titel": "Geothermie-Kraftwerke", "inhalt": "Tiefengeothermie nutzt Erdwärme für Strom und Heizung. Bohrungen bis 5000m Tiefe erforderlich. Seismische Risiken bei tiefen Eingriffen. Fernwärmenetze für Wärmeverteilung. Lange Vorlaufzeiten und hohe Investitionen. Akzeptanz nach Erdbeben-Problemen gesunken."},
    
    # Weitere innovative Bereiche
    {"titel": "Urban Farming Vertical", "inhalt": "Vertikale Landwirtschaft in Gebäuden wächst. LED-Beleuchtung ersetzt Sonnenlicht. Hydro- oder Aeroponik statt Boden. Ganzjährige Ernte unabhängig von Wetter. Pestizide unnötig in geschlossenen Systemen. Sehr hoher Energieverbrauch durch Kunstlicht."},
    
    {"titel": "Dark Kitchens Delivery Only", "inhalt": "Ghost Kitchens nur für Lieferdienste ohne Gäste. Niedrigere Mieten in B-Lagen möglich. Mehrere Marken aus einer Küche (Virtual Brands). Hygiene-Standards wie bei normalen Restaurants. Delivery-Apps als einziger Vertriebskanal. Packaging für Transport optimiert."},
    
    {"titel": "Data Centers Edge Computing", "inhalt": "Kleine Rechenzentren in Mobilfunkmasten. 5G erfordert lokale Datenverarbeitung. Autonome Fahrzeuge benötigen Echtzeit-Response. Content Delivery näher beim Endnutzer. Weniger Energie als zentrale Mega-Rechenzentren. Integration in bestehende Infrastruktur."},
    
    {"titel": "Micro-Fulfillment Supermärkte", "inhalt": "Online-Bestellung mit Abholung im Laden. Automatisierte Kommissionierung im Keller. Click & Collect reduziert Kundenzeit im Laden. Personal konzentriert sich auf Service statt Regale. Parken direkt vor dem Geschäft wichtig. Hybridmodell Online/Offline erfolgreich."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    for item in ALLE_NEUEN_DOCS:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Moderne Immobilienwirtschaft", 
                "category": "Zukunftstrends", 
                "title": item['titel']
            }
        })
    
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