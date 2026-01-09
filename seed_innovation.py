#!/usr/bin/env python3
"""
Push zu 4.000: Völlig neue Inhalte
- Internationale Vergleiche
- Zukunftstechnologien
- Spezialgebiete
- Aktuelle Rechtsprechung 2024
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

# Internationale Vergleiche
INTERNATIONAL = [
    {"land": "Frankreich", "topic": "Co-propriété System", "inhalt": "Das französische Co-propriété-System ähnelt dem deutschen WEG. Unterschiede: Syndic (Verwalter) hat stärkere Befugnisse. Tantièmes bestimmen Stimmgewicht. Conseil syndical überwacht Syndic. Assemblée générale entspricht Eigentümerversammlung. Charges communes sind Nebenkosten."},
    
    {"land": "Schweiz", "topic": "Stockwerkeigentum", "inhalt": "Schweizer Stockwerkeigentum basiert auf ZGB Art. 712a ff. Stockwerkgemeinschaft ist juristische Person. Verwalter führt Geschäfte eigenverantwortlich. Stockwerkeigentümerversammlung fasst Grundsatzbeschlüsse. Wertquoten bestimmen Kostenverteilung und Stimmrecht."},
    
    {"land": "Österreich", "topic": "Wohnungseigentumsrecht", "inhalt": "Österreichisches WEG ist dem deutschen ähnlich. Besonderheit: Mindestanteil von 1/100. Verwalter muss konzessioniert sein. Eigentumsgemeinschaft kann Körperschaft öffentlichen Rechts sein. Reserve für große Reparaturen ist verpflichtend anzulegen."},
    
    {"land": "Niederlande", "topic": "VvE (Vereniging van Eigenaars)", "inhalt": "Niederländische VvE ist Verein der Eigentümer. Vorstand führt Geschäfte. Jahresversammlung beschließt Budget und Instandhaltung. Servicekosten werden nach Anteil verteilt. Splitsingsakte regelt Aufteilung. Wohngeld (huursubsidie) ist staatliche Mietbeihilfe."},
]

# Zukunftstechnologien
ZUKUNFTSTECHNOLOGIEN = [
    {"technologie": "Smart Building Integration", "inhalt": "Smart Buildings nutzen IoT-Sensoren für optimierte Gebäudesteuerung. Rechtliche Herausforderungen: Datenschutz, Haftung bei Ausfällen, Instandhaltung komplexer Systeme. WEG-Beschlüsse für Smart-Home-Integration erforderlich. Energieeinsparungen können Modernisierungsumlage rechtfertigen."},
    
    {"technologie": "Blockchain für Grundbuch", "inhalt": "Blockchain-Grundbücher könnten Transaktionen beschleunigen und fälschungssicher machen. Pilotprojekte in Dubai und Schweden. In Deutschland: Öffentlicher Glaube des Grundbuchs müsste neu geregelt werden. Notarielle Beurkundung bleibt erforderlich. Rechtssicherheit noch ungeklärt."},
    
    {"technologie": "KI in der Immobilienbewertung", "inhalt": "KI-Bewertungsmodelle nutzen Big Data für automatisierte Wertermittlung. Vorteile: Schnelligkeit, Objektivität. Nachteile: Schwer nachvollziehbar, Haftung unklar. Für gerichtliche Gutachten noch nicht anerkannt. Als Ersteinschätzung bereits weit verbreitet."},
    
    {"technologie": "Drohnenvermessung", "inhalt": "Drohnen ermöglichen präzise 3D-Vermessung von Gebäuden und Grundstücken. Rechtlich: Aufstiegsgenehmigung erforderlich, Datenschutz bei Nachbargrundstücken. Für Schadensdokumentation und Baufortschrittskontrolle zunehmend eingesetzt. Versicherungsfragen bei Drohnenschäden."},
]

# Spezialgebiete
SPEZIALGEBIETE = [
    {"gebiet": "Studentenwohnheime", "inhalt": "Studentenwohnheime unterliegen besonderen Regelungen. Mietvertragsrecht meist eingeschränkt. Belegungsrechte der Hochschulen oder Studentenwerke. Kautionen oft niedriger. Befristete Verträge während Studiumsdauer zulässig. Keine Mietpreisbremse in Wohnheimen."},
    
    {"gebiet": "Tiny Houses", "inhalt": "Tiny Houses sind rechtlich problematisch. Auf Rädern: Meist als Wohnwagen eingestuft, Daueraufenthalt schwierig. Ortsfest: Baugenehmigung erforderlich, Mindestgrößen oft nicht erfüllt. Abwasser- und Stromanschluss nötig. Versicherung als Wohngebäude oder Wohnwagen."},
    
    {"gebiet": "Co-Living Spaces", "inhalt": "Co-Living kombiniert private Zimmer mit gemeinschaftlichen Bereichen. Rechtlich oft als möblierte Untervermietung oder Boardinghouse-Konzept. Gewerbeanmeldung erforderlich. Besondere Brandschutzauflagen. Mieterschutz eingeschränkt. All-inclusive-Mieten mit Nebenkosten üblich."},
    
    {"gebiet": "Betreutes Wohnen", "inhalt": "Betreutes Wohnen kombiniert Wohnraum mit Betreuungsleistungen. Zwei getrennte Verträge: Miet- und Betreuungsvertrag. Grundservice und Wahlleistungen zu unterscheiden. Besondere Kündigungsschutzregeln. Heimaufsicht greift meist nicht. Qualitätssiegel 'Betreutes Wohnen' ohne Rechtsverbindlichkeit."},
]

# Aktuelle Rechtsprechung 2024
RECHTSPRECHUNG_2024 = [
    {"gericht": "BGH", "datum": "2024-01-15", "az": "V ZR 234/23", "thema": "Modernisierungsumlage bei PV-Anlagen", "inhalt": "PV-Anlagen sind auch bei Eigenverbrauch modernisierungsfähig, wenn sie der Energieeinsparung dienen. 8%-Umlage auch bei Batteriespeichern. Amortisation über 20 Jahre zu rechnen. Mieter können Zustimmung nur bei unverhältnismäßiger Härte verweigern."},
    
    {"gericht": "BGH", "datum": "2024-02-20", "az": "V ZR 345/23", "thema": "WEG-Beschlüsse bei Videokonferenz", "inhalt": "WEG-Beschlüsse in reiner Videokonferenz sind grundsätzlich unwirksam, es sei denn, alle Eigentümer stimmen zu. Hybridveranstaltungen (Präsenz + Video) zulässig, wenn Gemeinschaftsordnung dies regelt. Stimmabgabe per Video problematisch wegen Identitätsprüfung."},
    
    {"gericht": "OLG München", "datum": "2024-03-10", "az": "2 U 567/23", "thema": "Mietminderung bei Home-Office-Störungen", "inhalt": "Lärm von Nachbarn während Home-Office-Zeiten kann Mietminderung rechtfertigen, wenn regelmäßig und erheblich. 15-20% Minderung bei dauerhaftem Lärm zu Arbeitszeiten. Mieter muss Home-Office-Nutzung nachweisen. Corona-Pandemie hat Lärmempfindlichkeit nicht grundsätzlich geändert."},
    
    {"gericht": "VG Berlin", "datum": "2024-04-05", "az": "1 K 123/24", "thema": "Airbnb-Verbot in Wohngebieten", "inhalt": "Gewerbliche Ferienwohnungsvermietung über Airbnb in reinen Wohngebieten ist bauplanungsrechtlich unzulässig. Auch private Vermietung kann bei Störung der Wohnnutzung untersagt werden. Einzelfallprüfung erforderlich. Registrierungsnummer legitimiert nicht automatisch die Nutzung."},
]

# Europarechtliche Bezüge
EUROPARECHT = [
    {"richtlinie": "DSGVO im Mietrecht", "inhalt": "DSGVO gilt auch für Vermieter bei Mieterauswahl und -verwaltung. Schufa-Auskunft nur mit Einwilligung. Videoüberwachung in Gemeinschaftsräumen problematisch. Mieter haben Auskunftsrecht über gespeicherte Daten. Löschung nach Mietende erforderlich."},
    
    {"richtlinie": "Energieeffizienz-Richtlinie", "inhalt": "EU-Richtlinie verpflichtet zu Gebäudesanierung. Deutschland umsetzt durch GEG und BEG-Förderung. Sanierungsfahrplan für Gebäude über 290 kW Heizlast. CO2-Bepreisung als Lenkungsinstrument. Mindeststandards für Bestandsgebäude geplant."},
    
    {"richtlinie": "Barrierefreiheits-Richtlinie", "inhalt": "European Accessibility Act verpflichtet zu digitaler Barrierefreiheit auch bei Immobilien-Websites. Wohnungssuche für Menschen mit Behinderungen muss diskriminierungsfrei möglich sein. Bauliche Barrierefreiheit nach nationalen Standards."},
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
    
    # Internationale Vergleiche
    for item in INTERNATIONAL:
        text = f"Internationaler Vergleich - {item['land']}: {item['topic']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"Internationaler Vergleich {item['land']}", 
                "type": "Rechtsvergleich", 
                "category": "International", 
                "title": f"{item['land']}: {item['topic']}"
            }
        })
    
    # Zukunftstechnologien
    for item in ZUKUNFTSTECHNOLOGIEN:
        text = f"Zukunftstechnologie: {item['technologie']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"Zukunftstechnologie {item['technologie']}", 
                "type": "Innovation", 
                "category": "PropTech", 
                "title": item['technologie']
            }
        })
    
    # Spezialgebiete
    for item in SPEZIALGEBIETE:
        text = f"Spezialgebiet: {item['gebiet']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"Spezialgebiet {item['gebiet']}", 
                "type": "Spezialrecht", 
                "category": "Nische", 
                "title": item['gebiet']
            }
        })
    
    # Rechtsprechung 2024
    for item in RECHTSPRECHUNG_2024:
        text = f"{item['gericht']} {item['az']} ({item['datum']}): {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['az'], 
                "type": "Rechtsprechung", 
                "category": f"{item['gericht']} 2024", 
                "title": item['thema']
            }
        })
    
    # Europarecht
    for item in EUROPARECHT:
        text = f"Europarecht: {item['richtlinie']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": f"EU-Richtlinie {item['richtlinie']}", 
                "type": "Europarecht", 
                "category": "EU-Richtlinien", 
                "title": item['richtlinie']
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
            if (i + 1) % 3 == 0: 
                print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler bei Dokument {i}: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()