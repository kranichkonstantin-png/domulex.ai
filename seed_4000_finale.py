#!/usr/bin/env python3
"""
FINALER ULTRA PUSH ZU 4.000!
Branchen die noch fehlen: Tourismus, Gastronomie, Einzelhandel, Automotive, Pharma, Gaming
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

FINALE_DOCS = [
    # Tourismus-Immobilien
    {"titel": "Ferienimmobilien Rechtsfragen", "inhalt": "Ferienwohnungen boomen, aber rechtlich komplex. Zweckentfremdungsverbote in Großstädten. Gewerbliche vs. private Vermietung abgrenzen. Airbnb-Regulation durch Kommunen. Möblierung und Ausstattungsstandards. Haftung bei Gästeschäden. Reinigungsservice als Betriebskosten."},
    
    {"titel": "Hotel-Immobilien als Investment", "inhalt": "Hotels als Asset-Klasse für Investoren attraktiv. Sale-and-lease-back Modelle üblich. Pachtverträge oft 15-25 Jahre mit Hotelbetreibern. Brandschutz und Sicherheit nach Hotelverordnung. Gastronomie-Integration für Zusatzerlöse. Tagungsräume als wichtiges Standbein."},
    
    {"titel": "Campingplätze modernisieren", "inhalt": "Camping erlebt Renaissance, besonders nach Corona. Sanitärgebäude müssen modernisiert werden. Glamping (Luxus-Camping) als Upgrade-Trend. Dauercamper vs. Touristen rechtlich unterscheiden. Umweltauflagen bei Gewässernähe. Mobilheime als semi-permanente Bauten."},
    
    {"titel": "Kreuzfahrt-Terminals", "inhalt": "Kreuzfahrt-Boom erfordert spezielle Terminals. Handling tausender Passagiere gleichzeitig. Sicherheitskontrollen wie am Flughafen. Gepäcklogistik hochkomplex. Shopping und Gastronomie im Terminal. Umweltauflagen für Schiffsabgase verschärft."},
    
    {"titel": "Freizeitparks und Erlebnisparks", "inhalt": "Phantasialand, Europa-Park als Immobilien-Giganten. Achterbahnen erfordern spezielle Statik-Gutachten. TÜV-Prüfungen für Fahrgeschäfte obligatorisch. Versicherung gegen Unfälle kritischer Faktor. Saisonalität vs. ganzjährige Nutzung. Hotels und Gastronomie integriert."},
    
    # Gastronomie-Immobilien
    {"titel": "Restaurant-Immobilien Post-Corona", "inhalt": "Gastronomie-Immobilien durch Pandemie stark betroffen. Outdoor-Dining wird wichtiger, Terrassen gefragt. Lieferservice erfordert andere Küchenkonzepte. Ghost Kitchens ohne Gästebereich boomen. Hygieneschutz-Maßnahmen dauerhaft implementiert. Mietnachlässe für Gastronomen üblich geworden."},
    
    {"titel": "Fast-Food-Ketten Expansion", "inhalt": "McDonald's, Burger King suchen standardisierte Standorte. Drive-Through erfordert spezielle Grundstücksform. Franchise-System mit einheitlichen Baustandards. Parken und Verkehrsführung kritisch. 24/7-Betrieb bei Autobahn-Standorten. Lärmschutz bei Wohngebietsnähe."},
    
    {"titel": "Craft-Beer-Brauereien", "inhalt": "Lokale Brauereien mit Ausschank kombiniert. Produktionsstätte und Gastronomie unter einem Dach. Hygienevorschriften wie Lebensmittelbetrieb. Abwasserbehandlung bei Brauprozess. Lärmschutz durch Anlagen und Gäste. Tourismus-Attraktion für Bier-Liebhaber."},
    
    {"titel": "Food Courts Einkaufszentren", "inhalt": "Food Courts als Magnet für Shopping-Center. Verschiedene Anbieter unter einem Dach. Gemeinschaftsbereich mit zentraler Reinigung. Dunstabzug und Geruchsfilterung zentral. Flexibler Umbau der Gastro-Stände. Internationale Küchen als Differenzierung."},
    
    # Einzelhandel-Immobilien
    {"titel": "Pop-Up-Stores temporär", "inhalt": "Pop-Up-Stores beleben leerstehende Ladenlokale. Kurze Mietverträge von wenigen Wochen bis Monaten. Flexibler Ladenbau für schnellen Auf-/Abbau. Startup-Brands testen neue Märkte. Vermieter aktivieren Leerstände kostengünstig. Zwischennutzung bis Vollvermietung."},
    
    {"titel": "Outlet-Center am Stadtrand", "inhalt": "Outlet-Malls für Marken-Restposten. Größere Flächen zu günstigeren Mieten außerhalb. Parken kostenlos im Gegensatz zur Innenstadt. Busreisen und Tourismus als Zielgruppe. Factory Stores der Hersteller direkt. Gastronomie und Entertainment integriert."},
    
    {"titel": "Concept Stores Experience", "inhalt": "Einzelhandel wird zu Experience-Centern. Kombinationen aus Shopping, Café, Events. Instagram-taugliche Einrichtung für Social Media. Personal als Brand-Botschafter statt Verkäufer. Workshops und Events statt nur Verkauf. Mieten steigen durch Aufwertung der Standorte."},
    
    {"titel": "Click-and-Collect Hybrid", "inhalt": "Online bestellen, im Laden abholen wird Standard. Drive-Through auch für Non-Food-Einzelhandel. Lager-Integration in Verkaufsräume. Personal für Kommissionierung zusätzlich. Parken direkt vor dem Geschäft wichtig. Returns/Umtausch vor Ort möglich."},
    
    # Automotive-Immobilien
    {"titel": "E-Auto-Ladeparks", "inhalt": "Schnelllade-Hubs an Autobahnen und Stadträdern. Tesla Supercharger als Referenz. 150-350kW Schnellladung in 15-30 Minuten. Gastronomie und Shopping während Ladezeit. Photovoltaik-Überdachung für grünen Strom. Batterie-Pufferspeicher für Lastspitzen."},
    
    {"titel": "Autowerkstätten E-Mobilität", "inhalt": "KFZ-Betriebe rüsten für E-Auto-Service um. Hochvolt-Schulungen für Mechaniker obligatorisch. Spezialwerkzeug und Hebebühnen für Batterien. Brandschutz bei Lithium-Ionen-Problemen. Batterietest und -tausch als neues Geschäftsfeld. Software-Updates over-the-air."},
    
    {"titel": "Carsharing-Stationen urban", "inhalt": "Car2Go, DriveNow etc. brauchen urbane Standorte. Feste Stationen vs. Free-Floating-Modelle. E-Auto-Carsharing mit Ladestationen. App-gesteuerte Fahrzeugfreigabe. Vandalismus und Diebstahl als Risiken. Integration in ÖPNV-Knotenpunkte sinnvoll."},
    
    {"titel": "Autonome Fahrzeuge Parken", "inhalt": "Selbstfahrende Autos ändern Parkraumbedarf fundamental. Autos parken sich selbst in entfernteren Gebieten. Valet-Parking durch Roboter. Effizienzsteigerung durch optimierte Parkraumnutzung. Weniger Stellplätze in Innenstädten nötig. Rechtsfragen bei Unfällen beim autonomen Parken."},
    
    # Pharma-Immobilien
    {"titel": "Apotheken 2.0 digital", "inhalt": "Digitalisierung verändert Apotheken grundlegend. E-Rezept und Online-Bestellung Standard. Pharma-Automaten für 24/7-Verfügbarkeit. Beratung per Video-Chat möglich. Lagerautomatisierung reduziert Personalbedarf. Versandapotheken als Konkurrenz zu lokalen Apotheken."},
    
    {"titel": "Cannabis-Dispensaries legal", "inhalt": "Cannabis-Legalisierung schafft neue Einzelhandels-Kategorie. Sicherheitsauflagen wie bei Juwelieren oder Banken. Jugendschutz durch Standort-Beschränkungen. Geruchsfilterung und Lüftung wichtig. Banking und Zahlungssysteme noch problematisch. Marketing-Beschränkungen wie bei Tabak."},
    
    {"titel": "Pharma-Logistik temperiert", "inhalt": "Medikamenten-Transport unter kontrollierten Bedingungen. Kühlkette von 2-8°C für viele Präparate. Sicherheitstransport für Betäubungsmittel und teure Therapien. Track-and-Trace für jeden Einzelpack. Apotheken-Belieferung mehrmals täglich. Notfall-Lieferungen außerhalb Geschäftszeiten."},
    
    {"titel": "Impfzentren temporär", "inhalt": "Corona schuf Bedarf für große Impf-Locations. Messe- und Sporthallen umfunktioniert. Separate Ein- und Ausgänge für Personenfluss. Kühllogistik für verschiedene Impfstoffe. Warteräume mit Abstandsregeln. Personal-Schulung und Notfall-Ausrüstung. Umbau zu normaler Nutzung nach Pandemie."},
    
    # Gaming & Entertainment
    {"titel": "VR-Arcades Entertainment", "inhalt": "Virtual Reality Spielhallen als neue Entertainment-Form. Große leere Räume für VR-Bewegung erforderlich. Motion-Tracking-Systeme an Decke und Wänden. Haftung bei VR-bedingten Stürzen kritisch. Hygieneschutz bei geteilten VR-Brillen. Jugendschutz bei Gewalt-VR-Spielen."},
    
    {"titel": "Streaming-Studios Content", "inhalt": "YouTube, Twitch Creator brauchen professionelle Studios. Schallschutz für Audio-Aufnahmen essentiell. Professionelle Beleuchtung und Green-Screens. Glasfaser-Internet für Upload-Bandbreite. Steuerliche Abschreibung der Studio-Ausstattung. Urheberrecht bei Hintergrundmusik in Streams."},
    
    {"titel": "Retro-Gaming-Cafés", "inhalt": "Nostalgie-Gaming mit alten Konsolen und Arcade-Automaten. Kombination aus Gaming und Gastronomie. Sammler-Community als loyale Kundschaft. Wartung alter Hardware zunehmend schwierig. Lizenzgebühren für klassische Spiele. Kindergeburtstage und Events als Zusatzgeschäft."},
    
    {"titel": "E-Sports-Training-Facilities", "inhalt": "Professionelle E-Sports-Teams benötigen Trainingsräume. Gaming-PCs mit High-End-Hardware. Ergonomische Gaming-Stühle und -Tische. Coach-Bereiche für Taktik-Besprechungen. Streaming-Equipment für Content-Erstellung. Physiotherapie-Räume für Handgelenke und Rücken. Gaming-House-Konzepte mit Wohnräumen."},
    
    # Weitere Zukunftsfelder
    {"titel": "Krypto-Mining-Farmen", "inhalt": "Bitcoin-Mining erfordert massive Rechenleistung und Energie. Kühlung der Mining-Rigs kritisch für Effizienz. Stromkosten dominieren Wirtschaftlichkeit. Lärm durch Lüfter belastet Nachbarschaft. Regulierung durch Klimaschutz-Auflagen. Alternative Kryptowährungen mit geringerem Energiebedarf."},
    
    {"titel": "Vertical Farming Indoor", "inhalt": "Landwirtschaft in mehrstöckigen Gebäuden. LED-Beleuchtung ersetzt Sonnenlicht komplett. Hydroponik oder Aeroponik ohne Erdboden. Ganzjährige Ernte unabhängig von Wetter. Pestizide unnötig in kontrollierten Bedingungen. Extrem hoher Energieverbrauch durch Kunstlicht. Lokale Produktion reduziert Transportwege."},
    
    {"titel": "Drohnen-Delivery-Hubs", "inhalt": "Verteilzentren für autonome Drohnen-Lieferung. Automatische Be- und Entladung der Drohnen. Wartung und Batteriewechsel vollautomatisch. Flugrouten-Optimierung durch KI. Wetter-Monitoring für sicheren Flugbetrieb. Integration mit Luftverkehrskontrolle. Notlandeplätze bei technischen Problemen."},
    
    {"titel": "Micro-Mobility Sharing", "inhalt": "E-Scooter, E-Bikes und andere Kleinstfahrzeuge. Abstellflächen in öffentlichen und privaten Räumen. Aufladung der Fahrzeug-Batterien organisieren. Wartung und Reparatur-Service. Umverteilung zwischen beliebten und weniger frequentierten Standorten. Vandalismus und Diebstahl als Dauerproblem. Integration in ÖPNV-Apps."},
    
    {"titel": "Shared Office Spaces", "inhalt": "Geteilte Büroräume für Freelancer und Startups. Flexible Mitgliedschaften von Tages- bis Jahrestarifen. Meeting-Räume stundenweise buchbar. Gemeinschaftsküche und Lounge-Bereiche. High-Speed-Internet und Drucker/Scanner. Community-Events für Networking. Expansion in kleinere Städte jenseits der Metropolen."},
    
    {"titel": "Dark Stores Supermarkt", "inhalt": "Supermarkt nur für Online-Bestellung ohne Kunden vor Ort. Optimierte Lager-Layouts für Kommissionierung. Personal arbeitet nur für Picking und Packing. Delivery-Integration für schnelle Lieferung. Kosteneinsparung durch B-Lagen ohne Laufkundschaft. Fresh-Food-Handling für verderbliche Waren. Konkurrenz zu traditionellen Supermärkten."},
    
    {"titel": "Maker Spaces Community", "inhalt": "Gemeinschaftswerkstätten für DIY-Projekte. 3D-Drucker, Lasercutter und traditionelle Werkzeuge. Mitgliedschaft für Zugang zu teuren Geräten. Kurse und Workshops für Fertigkeiten-Vermittlung. Startup-Inkubation für Hardware-Projekte. Versicherung für Werkstatt-Unfälle wichtig. Lärmschutz bei handwerklichen Arbeiten."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    for item in FINALE_DOCS:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Branchenimmobilien", 
                "category": "Spezialnutzungen", 
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