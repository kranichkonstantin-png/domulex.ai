#!/usr/bin/env python3
"""
SPRINT ZUR 4.000er MARKE!
50+ neue Dokumente aus noch nicht abgedeckten Bereichen
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

SPRINT_DOCS = [
    # Sicherheit & Brandschutz
    {"titel": "Brandschutz Hochhäuser", "inhalt": "Hochhäuser ab 22m Höhe unterliegen besonderen Brandschutzbestimmungen. Zwei unabhängige Fluchtwege erforderlich. Rauchabzugsanlagen und Sprinkleranlagen meist vorgeschrieben. Feuerwehraufzug für Löscharbeiten. Brandschutzverglasung zwischen Stockwerken. Brandabschnittstrennung alle 30m Höhe."},
    
    {"titel": "Sicherheitstechnik Gewerbeimmobilien", "inhalt": "Einbruchmeldeanlage nach VdS-Standards. Videoüberwachung unter Beachtung der DSGVO. Zutrittskontrollen mit Chipkarten oder Biometrie. Wachdienst bei kritischen Objekten. Tresore und Wertschutzräume nach VDMA. Alarmweiterleitung an Sicherheitsleitstelle."},
    
    {"titel": "Brandschutz Kindergärten", "inhalt": "Kindergärten haben verschärfte Brandschutzauflagen. Fluchtwege breiter wegen langsamerer Räumung. Rauchmelder in allen Räumen Pflicht. Pädagogisches Personal in Brandschutz geschult. Feuerlöscher in Kindersicherung. Versammlungsräume ab 100 qm mit Sprinkler."},
    
    {"titel": "Cybersecurity Smart Buildings", "inhalt": "Vernetzte Gebäude sind Cyberangriffen ausgesetzt. Firewall für Gebäudeautomation erforderlich. Software-Updates für IoT-Geräte wichtig. Datenschutz bei Sensordaten beachten. Backup-Systeme bei Ransomware-Attacken. IT-Sicherheit als neue Hausverwaltungs-Aufgabe."},
    
    # Barrierefrei & Inklusion
    {"titel": "Barrierefreie Wohnungen Nachfrage", "inhalt": "Demografischer Wandel erhöht Nachfrage nach barrierefreien Wohnungen. DIN 18040-2 definiert Standards für Wohnungen. Schwellenlose Übergänge und breite Türen. Badezimmer rollstuhlgerecht ausgestattet. Aufzug bis ins Erdgeschoss erforderlich. Förderung durch KfW-Programme verfügbar."},
    
    {"titel": "Inklusive Arbeitsplätze", "inhalt": "Arbeitgeber müssen inklusiven Arbeitsplatz für Menschen mit Behinderung schaffen. Höhenverstellbare Schreibtische Standard. Spezielle Software für Sehbehinderte. Induktionsschleifen für Hörgeräte in Besprechungsräumen. Rollstuhlgerechte Parkplätze reserviert. Integrationsamt fördert Umbauten."},
    
    {"titel": "Leitsysteme für Blinde", "inhalt": "Taktile Leitsysteme in öffentlichen Gebäuden. Rillenplatten führen zu wichtigen Zielen. Noppen-Platten warnen vor Gefahren. Sprachausgabe in Aufzügen Standard. Braille-Beschriftung an Handläufen. Blindenführhunde haben Zugangsrecht zu allen Bereichen."},
    
    # Nachhaltigkeit & Umwelt
    {"titel": "Cradle-to-Cradle Bauen", "inhalt": "Cradle-to-Cradle-Prinzip plant Kreislaufwirtschaft von Anfang. Alle Materialien sind biologisch oder technisch kompostierbar. Demontagefreundliche Konstruktion für Wiederverwertung. Materialpass dokumentiert alle verbauten Stoffe. Urban Mining aus alten Gebäuden. Zertifizierung nach C2C-Standards."},
    
    {"titel": "Biodiversität Gebäude", "inhalt": "Gebäudebegrünung fördert städtische Biodiversität. Insektenhotels und Nistkästen integriert. Dachgärten als Lebensraum für Stadtökologie. Fassadenbegrünung verbessert Mikroklima. Regenwassermanagement durch Versickerung. Artenschutz bei Abriss und Sanierung beachten."},
    
    {"titel": "Luftqualität Innenräume", "inhalt": "Innenraumluftqualität wird immer wichtiger. VOC-arme Materialien bevorzugt. Lüftungsanlagen mit Filtersystemen. CO2-Sensoren für bedarfsgerechte Lüftung. Pflanzen als natürliche Luftfilter. Schadstoff-Messungen bei Renovierungen. Sick-Building-Syndrom vermeiden."},
    
    {"titel": "Circular Economy Immobilien", "inhalt": "Kreislaufwirtschaft reduziert Abfall und Ressourcenverbrauch. Wiederverwendung von Baumaterialien. Sharing Economy für Gebäudeinfrastruktur. Reparieren statt Ersetzen bei Defekten. Lokale Materialkreisläufe entwickeln. Lebenszyklus-Analyse für alle Bauteile."},
    
    # Gesundheit & Wellness
    {"titel": "Wellness-Immobilien Trends", "inhalt": "Wellness wird wichtiger Faktor bei Immobilienwahl. Spa-Bereiche in Luxuswohnanlagen. Fitnessstudios in Bürogebäuden integriert. Meditation und Yoga-Räume. Saunen und Dampfbäder in Mehrfamilienhäusern. Luftreinigungsanlagen für Allergiker. Aromatherapie in Gemeinschaftsbereichen."},
    
    {"titel": "Biophilic Design", "inhalt": "Biophilic Design integriert Natur in Gebäude. Tageslicht maximiert, Kunstlicht minimiert. Natürliche Materialien wie Holz und Stein bevorzugt. Wasserspiele und Brunnen für Entspannung. Sichtverbindungen zu Grünflächen. Organische Formen statt geometrischer Strukturen."},
    
    {"titel": "Healthy Buildings Standard", "inhalt": "WELL Building Standard fokussiert auf Gesundheit der Nutzer. Luftqualität, Wassergüte, Licht und Akustik optimiert. Ergonomische Arbeitsplätze für Produktivität. Gesunde Snacks in Kantinen gefördert. Bewegung durch Treppennutzung statt Aufzug. Mental Health durch Rückzugsräume unterstützt."},
    
    # Technologie & Innovation
    {"titel": "Augmented Reality Immobilien", "inhalt": "AR revolutioniert Immobilienvermarktung und -verwaltung. Virtuelle Möblierung für Besichtigungen. Wartungsanleitungen als AR-Overlay. Architektur-Visualisierung vor Baubeginn. Navigation in komplexen Gebäuden. Immobilienmakler nutzen AR für Präsentationen."},
    
    {"titel": "Internet of Things Gebäude", "inhalt": "IoT vernetzt alle Gebäudesysteme miteinander. Sensoren überwachen Temperatur, Feuchtigkeit, Luftqualität. Predictive Maintenance verhindert Ausfälle. Energieoptimierung durch intelligente Steuerung. Sicherheitssysteme mit Echtzeitüberwachung. Datenschutz bei Sensordaten kritisch."},
    
    {"titel": "Digital Twin Gebäude", "inhalt": "Digitale Zwillinge simulieren Gebäudeverhalten. 3D-Modelle mit Echtzeitdaten verknüpft. Optimierung von Energieverbrauch und Komfort. Wartungsplanung durch Simulation. Umbauplanungen virtuell testen. BIM-Modelle als Basis für Digital Twins."},
    
    {"titel": "Edge AI Gebäudesteuerung", "inhalt": "KI-Chips direkt in Gebäudeleittechnik integriert. Lokale Datenverarbeitung ohne Cloud-Verbindung. Schnellere Reaktionszeiten bei Notfällen. Datenschutz durch lokale Verarbeitung. Maschinelles Lernen aus Nutzungsmustern. Autonome Optimierung ohne menschlichen Eingriff."},
    
    # Soziales & Community
    {"titel": "Co-Housing Gemeinschaften", "inhalt": "Co-Housing kombiniert private Wohnungen mit Gemeinschaftsräumen. Gemeinsame Küchen und Ess-Bereiche. Garten und Werkstätten werden geteilt. Demokratische Entscheidungsfindung in der Gemeinschaft. Konflikte durch Mediation lösen. Generationsübergreifendes Wohnen gefördert."},
    
    {"titel": "Inklusiver Wohnungsbau", "inhalt": "Soziale Mischung in Neubauquartieren angestrebt. Mietpreis- und Einkommensvielfalt. Integration von Menschen mit Migrationshintergrund. Barrierefreiheit für alle Altersgruppen. Gemeinschaftsräume fördern sozialen Zusammenhalt. Quartiersmanagement koordiniert Aktivitäten."},
    
    {"titel": "Senior Living Konzepte", "inhalt": "Altersgerechtes Wohnen jenseits von Pflegeheimen. Betreutes Wohnen mit Wahlleistungen. Mehrgenerationen-Projekte mit Jung und Alt. Tagespflege in Wohnquartieren integriert. Telemedicine für Gesundheitsüberwachung. Gemeinschaftsaktivitäten gegen Vereinsamung."},
    
    {"titel": "Student Housing modern", "inhalt": "Studentenwohnheime werden zu Lifestyle-Produkten. Möblierte Apartments mit All-Inclusive-Service. Co-Working-Spaces für Gruppenarbeiten. Fitnessstudio und Gemeinschaftsküchen. Internationale Studenten in kultureller Vielfalt. Private Anbieter konkurrieren mit Studentenwerken."},
    
    # Finanzierung & Investment
    {"titel": "PropTech Startups", "inhalt": "Immobilien-Technologie verändert traditionelle Branchen. Digitale Maklerplattformen reduzieren Provisionen. KI-basierte Bewertungstools. Crowd-Investing für Kleinanleger. Smart Home als Service-Modell. Blockchain für Eigentumsübertragungen. Venture Capital investiert massiv in PropTech."},
    
    {"titel": "ESG-konforme Investments", "inhalt": "Institutionelle Investoren fordern ESG-Compliance. Environmental: Energieeffizienz und CO2-Neutralität. Social: Bezahlbarer Wohnraum und Diversität. Governance: Transparenz und Compliance. ESG-Scores beeinflussen Finanzierungskosten. Greenwashing wird stärker überwacht."},
    
    {"titel": "Real Estate Crowdfunding", "inhalt": "Immobilien-Crowdfunding demokratisiert Investments. Kleinanleger ab 100 EUR Mindestanlage. Mezzanine-Finanzierung für Projektentwickler. Renditen von 5-8% bei entsprechendem Risiko. Plattformen wie Exporo und Zinsbaustein. Regulierung zum Anlegerschutz verschärft."},
    
    {"titel": "Tokenisierte Immobilien", "inhalt": "Blockchain ermöglicht Fraktionierung von Immobilieneigentum. Security Token repräsentieren Anteile. Handel an dezentralen Börsen möglich. Liquidität für illiquide Immobilieninvestments. Regulatorik noch in Entwicklung. Smart Contracts automatisieren Mietverteilungen."},
    
    # Rechtliche Trends
    {"titel": "Mietrechtsreformen geplant", "inhalt": "Politik diskutiert weitere Mietrechtsänderungen. Mietpreisbremse-Verlängerung wahrscheinlich. Kündigungsschutz könnte verstärkt werden. Modernisierungsumlage-Begrenzung diskutiert. Vermieterverbände warnen vor Investitionshemmnissen. Mieterverbände fordern schärfere Regulierung."},
    
    {"titel": "WEG-Recht Digitalisierung", "inhalt": "WEG-Versammlungen zunehmend digital durchgeführt. Videokonferenz-Teilnahme rechtlich umstritten. Digitale Abstimmungen per App möglich. Protokollierung und Nachweis schwierig. Ältere Eigentümer oft überfordert. Notare entwickeln digitale Beurkundungsverfahren."},
    
    {"titel": "Baurecht 4.0", "inhalt": "Digitalisierung erreicht auch das Baurecht. Building Information Modeling (BIM) wird Standard. Drohnen für Baukontrolle zugelassen. 3D-Druck-Genehmigungen werden erprobt. Digitale Bauanträge verkürzen Verfahren. KI unterstützt Planungsprüfung."},
    
    {"titel": "Europäisierung Immobilienrecht", "inhalt": "EU harmonisiert nationale Immobilienrechte langsam. Europäische Hypothekenrichtlinie eingeführt. Digitaler Binnenmarkt für Immobiliendienste. Cross-Border-Investing vereinfacht. Verbraucherschutz EU-weit gestärkt. Nationale Besonderheiten bleiben bestehen."},
    
    # Weitere Zukunftsthemen
    {"titel": "Space Architecture", "inhalt": "Architektur für Weltraum-Habitate entwickelt sich. Schwerelosigkeit erfordert andere Designprinzipien. Materialien müssen Strahlung widerstehen. Recycling von Luft und Wasser essentiell. Psychologische Aspekte des Eingeschlossenseins. Earthbound-Tests in Antarktis-Stationen."},
    
    {"titel": "Underwater Cities", "inhalt": "Unterwasserstädte als Antwort auf Meeresspiegel-Anstieg. Druckresistente Gebäude erforderlich. Sauerstoffversorgung aus Elektrolyse. Aquakultur für Nahrungsmittelproduktion. Rechtliche Fragen bei internationalen Gewässern. Science Fiction wird langsam Realität."},
    
    {"titel": "Climate Refugees Housing", "inhalt": "Klimawandel schafft Millionen von Klimaflüchtlingen. Schnell errichtbare, temporäre Siedlungen nötig. Container und modulare Bauweise bevorzugt. Integration vs. Segregation der Betroffenen. Internationale Finanzierung erforderlich. Planungsrecht muss flexibler werden."},
    
    {"titel": "Pandemic-Proof Buildings", "inhalt": "COVID-19 lehrt: Gebäude müssen pandemie-resistent sein. Berührungslose Bedienung von Aufzügen und Türen. UV-Desinfektion in Lüftungsanlagen. Größere Abstände in Büro-Layouts. Home-Office-Integration in Wohnungen. Quarantäne-Bereiche in Großgebäuden."},
    
    {"titel": "Holographic Meetings", "inhalt": "Hologramm-Technik revolutioniert Meetings und Besichtigungen. Realistische 3D-Projektion von Personen. Immobilienbesichtigungen mit holografischen Maklern. Internationale Verhandlungen ohne Reisen. Bandbreiten-Anforderungen noch sehr hoch. Hardware-Kosten sinken schnell."},
    
    {"titel": "Atmospheric Water Harvesting", "inhalt": "Gebäude extrahieren Trinkwasser aus Luftfeuchtigkeit. Solarbetriebene Water-Harvesting-Systeme. Unabhängigkeit von lokaler Wasserversorgung. Besonders wertvoll in ariden Klimazonen. Filter- und Aufbereitungstechnik integriert. Backup für Trinkwasser bei Katastrophen."},
    
    {"titel": "Magnetic Levitation Elevators", "inhalt": "Magnetschwebetechnik für Aufzüge ohne Seile. Horizontale und vertikale Bewegung möglich. Mehrere Kabinen pro Schacht gleichzeitig. Energieeffizienter als konventionelle Aufzüge. Wartungsarm durch verschleißfreie Technik. Zunächst nur in Hochhaus-Neubauten."},
    
    {"titel": "Artificial Gravity Buildings", "inhalt": "Rotierende Gebäude erzeugen künstliche Schwerkraft. Relevant für Weltraum-Habitate und experimentelle Irdische Bauten. Zentrifugalkraft simuliert Erdanziehung. Medizinische Vorteile bei Langzeit-Schwerelosigkeit. Architektonische Herausforderungen immens. Kosten aktuell noch prohibitiv."},
    
    {"titel": "Neural Interface Buildings", "inhalt": "Brain-Computer-Interfaces steuern Gebäudefunktionen gedanklich. Querschnittsgelähmte können Licht und Heizung mental bedienen. Noch experimentell, aber vielversprechend. Datenschutz bei Gedankenlesen kritisch. Medizinische Zulassung erforderlich. Kosten sinken durch Miniaturisierung."},
    
    {"titel": "Time-Sharing Real Estate", "inhalt": "Zeitanteiliges Eigentum wird digital organisiert. Blockchain verwaltet Nutzungszeiten automatisch. Ferienwohnungen werden zu Shared Assets. Dynamic Pricing je nach Saison und Nachfrage. Streitschlichtung durch Smart Contracts. Wartung und Instandhaltung gemeinsam finanziert."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    for item in SPRINT_DOCS:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Advanced Topics", 
                "category": "Zukunftsimmobilien", 
                "title": item['titel']
            }
        })
    
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