#!/usr/bin/env python3
"""
Expansion zu 4.000+ Dokumenten
Neue Rechtsbereiche: Verkehr, Medizin, Arbeit, Insolvenz
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

NEUE_DOCS = [
    # Verkehrsrecht
    {"titel": "E-Scooter Stellplätze", "inhalt": "E-Scooter-Sharing erfordert Abstellflächen. Kommunen können Stellplätze ausweisen. Private Grundstücke: Hausrecht der Eigentümer. Ordnungswidriges Abstellen führt zu Bußgeldern. Konflikte mit Fußgängern und Rollstuhlfahrern. Lösungen durch Abstellsäulen oder markierte Flächen."},
    
    {"titel": "Autonomous Vehicle Parking", "inhalt": "Autonome Fahrzeuge verändern Parkraumbedarf fundamental. Fahrzeuge können sich selbst parken, entfernte Parkplätze anfahren. Stellplatzbedarf sinkt drastisch. Rechtlich: Haftung bei autonomem Parken, Verkehrsrecht für fahrerlose Autos. Deutschland testet autonome Parkdienste."},
    
    {"titel": "Drohnen-Landeplätze Gebäude", "inhalt": "Kommerzielle Drohnen benötigen Landeplätze auf Gebäuden. Rechtlich: Luftverkehrsrecht, Genehmigung durch Luftfahrtbehörde. Sicherheitsabstände zu bewohnten Bereichen. Versicherung gegen Abstürze. Paketdrohnen für Hochhäuser in Erprobung."},
    
    # Medizinrecht  
    {"titel": "Telemedizin-Praxen", "inhalt": "Telemedizin reduziert Bedarf an klassischen Praxisräumen. Rechtlich: Ärztliche Sorgfaltspflicht auch bei Fernbehandlung. Datenschutz bei Video-Sprechstunden kritisch. Praxisräume werden kleiner, aber hochtechnisiert. Hybridmodelle aus Präsenz und Telemedizin."},
    
    {"titel": "Pflegeimmobilien Investment", "inhalt": "Demografischer Wandel macht Pflegeimmobilien attraktiv. Sale-and-lease-back bei Pflegeheimen üblich. Renditen 4-6% bei 20+ Jahren Pachtverträgen. Risiko: Insolvenz der Betreiber, Regulierung. Qualitätsstandards beeinflussen Investitionssicherheit."},
    
    {"titel": "Quarantäne-Einrichtungen", "inhalt": "Corona schuf Bedarf für Quarantäne-Hotels. Rechtlich: Infektionsschutzgesetz ermöglicht Zwangseinweisung. Hotels können für Quarantäne requiriert werden. Hygieneschleusen, getrennte Lüftung erforderlich. Geschäftsmodell für Hotel-Immobilien in Pandemiezeiten."},
    
    # Arbeitsrecht
    {"titel": "Co-Working Rechtsfragen", "inhalt": "Co-Working-Spaces haben komplexe Rechtsfragen. Gewerbliche vs. private Nutzung abgrenzen. Arbeitsschutz für Freelancer ungeklärt. Haftung bei Diebstählen zwischen Nutzern. Datenschutz bei geteilten Arbeitsplätzen. Versicherungsschutz für temporäre Nutzer."},
    
    {"titel": "Remote Work Steuerrecht", "inhalt": "Home-Office verändert Steuerrecht fundamental. Betriebsstätte entsteht bei dauerhaftem Home-Office. Internationale Besteuerung bei grenzüberschreitendem Remote Work. Arbeitszimmer-Abzug erweitert. Reisekosten zwischen Home-Office und Büro problematisch."},
    
    {"titel": "Gig Economy Immobilien", "inhalt": "Gig Worker (Uber, Lieferando) nutzen Immobilien anders. Kurzzeitige Nutzungen, flexible Arbeitsplätze. Dark Kitchens nur für Lieferservice ohne Gästebereich. Micro-Hubs für Paketverteilung in Wohngebieten. Rechtlich zwischen Gewerbe und Privatnutzung."},
    
    # Insolvenzrecht
    {"titel": "Zombie-Immobilien", "inhalt": "Verlassene Immobilien nach Eigentümer-Insolvenz. Verwahrlosung schädigt Nachbarschaft. Kommunen können Verkehrssicherung anordnen. Kosten gehen zu Lasten der Allgemeinheit. Vorkaufsrechte der Gemeinde als Lösung. Urban Mining aus verlassenen Gebäuden."},
    
    {"titel": "REITs Insolvenzschutz", "inhalt": "Real Estate Investment Trusts (REITs) bieten Insolvenzschutz durch Diversifikation. Immobilien im Sondervermögen geschützt. Bei REIT-Insolvenz: Abwicklung, kein Totalverlust. Deutschland hat REITs eingeschränkt zugelassen. Internationale REITs für deutsche Investoren verfügbar."},
    
    # Spezialgebiete
    {"titel": "Friedwald Bestattungsimmobilien", "inhalt": "Bestattungswälder als neue Immobiliennutzung. Forst wird zu Friedhof umgewidmet. Kommunale Genehmigung erforderlich. Rechtlich: Bestattungsgesetz, Forstreecht, Naturschutz. Nachfrage steigt durch veränderte Bestattungskultur. Alternative zu überfüllten Friedhöfen."},
    
    {"titel": "Escape Room Sicherheitsrecht", "inhalt": "Escape Rooms sind rechtlich komplex. Einschluss von Personen vs. Fluchtwegegebot. Brandschutz kritisch bei verriegelten Räumen. Personenüberwachung durch Kameras/Mikrofone. Versicherung gegen Panikattacken. Notfall-Öffnungsmechanismen vorgeschrieben."},
    
    {"titel": "Indoor-Farming Rechtsfragen", "inhalt": "Vertikale Landwirtschaft in Gebäuden rechtlich hybrid. Landwirtschaft vs. Gewerbe vs. Industrie. Energieverbrauch durch LED-Beleuchtung extrem hoch. Wassermanagement und Abwasser. Pestizideinsatz in geschlossenen Systemen. Lebensmittelhygiene-Verordnung anzuwenden."},
    
    {"titel": "Krypto-Mining Immobiliennutzung", "inhalt": "Bitcoin-Mining in Immobilien energieintensiv. Stromverbrauch wie Industriebetrieb. Lärm durch Kühlsysteme problematisch. Brandgefahr durch Überhitzung. Gewerbeanmeldung meist erforderlich. Mining-Farmen in ehemaligen Industriegebäuden. Regulierung durch Energiewende gefährdet."},
    
    {"titel": "Streamdeck Broadcast Studios", "inhalt": "Content Creator benötigen spezialisierte Studios. Schallschutz für Streaming und Podcast-Aufnahmen. Professionelle Beleuchtung und Technik. Rechtlich meist Gewerbe, nicht freie Berufe. Urheberrecht bei Musik im Stream. Steuerliche Behandlung als Influencer ungeklärt."},
    
    {"titel": "VR-Arcade Immobiliennutzung", "inhalt": "Virtual Reality Arcades als neue Vergnügungsstätten. Große, leere Räume für VR-Bewegung erforderlich. Haftung bei VR-bedingten Stürzen/Verletzungen. Jugendschutz bei VR-Inhalten. Motion Sickness und Gesundheitsrisiken. Technologie-Updates erfordern hohe Investitionen."},
    
    {"titel": "Repair Cafés Gemeinschaftsräume", "inhalt": "Repair Cafés in Wohnquartieren fördern Nachhaltigkeit. Rechtlich: Gewerbeanmeldung bei regelmäßigen Events. Haftung bei Reparaturschäden. Werkzeug-Versicherung wichtig. Lärmschutz bei handwerklichen Arbeiten. Abfallentsorgung von Elektroschrott."},
    
    {"titel": "Darknet-Server Hosting illegal", "inhalt": "Illegales Server-Hosting in Immobilien. Rechtlich: Beihilfe zu Straftaten, Geldwäsche. Stromverbrauch-Anomalien als Indiz. Hausdurchsuchungen und Beschlagnahmen. Vermieter haften bei Wissentlichkeit. Immobilie kann eingezogen werden bei schweren Straftaten."},
    
    {"titel": "Influencer-Häuser rechtlich", "inhalt": "Content Creator WGs für gemeinsame Produktion. Rechtlich: Wohnung vs. Gewerbe vs. Filmstudio. Lärmbelastung durch ständige Aufnahmen. Steuerliche Abgrenzung privat/beruflich. Influencer als Gewerbetreibende. Urheberrecht bei gemeinsamen Inhalten."},
    
    {"titel": "Airsoft Gaming Immobilien", "inhalt": "Airsoft-Arenen benötigen spezielle Sicherheitsvorkehrungen. Waffenrecht bei Softair-Waffen beachten. Schutzausrüstung vorgeschrieben. Versicherung gegen Verletzungen. Lärmschutz bei Simulator-Geräuschen. Jugendschutz bei kriegsähnlichen Spielen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    for item in NEUE_DOCS:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Spezialrecht", 
                "category": "Moderne Nutzungen", 
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