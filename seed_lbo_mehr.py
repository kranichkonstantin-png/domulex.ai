#!/usr/bin/env python3
"""Landesbauordnungen aller Bundesländer"""

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import uuid

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
client = QdrantClient(host=os.environ['QDRANT_HOST'], port=6333, api_key=os.environ['QDRANT_API_KEY'], https=True)

def embed(text):
    return genai.embed_content(model='models/text-embedding-004', content=text[:8000])['embedding']

print('🚀 LBO BUNDESLÄNDER SEEDING')

lbo_docs = [
    # Bayern
    {'title': 'BayBO Art. 6 - Abstandsflächen Bayern', 'content': 'Die Abstandsfläche beträgt in Bayern 0,4 H, mindestens 3 m. H ist die Wandhöhe. In Kern-, Gewerbe- und Industriegebieten kann die Tiefe auf 0,25 H, mindestens 2,50 m, verringert werden. Garagen bis 9 m Länge und 3 m Höhe sind in der Abstandsfläche zulässig. Außenwände von untergeordneter Bedeutung (max. 1/5 der Außenwand, max. 5 m) bleiben bei der Bemessung unberücksichtigt.', 'source': 'BayBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bayern'},
    {'title': 'BayBO Art. 57 - Verfahrensfreie Bauvorhaben Bayern', 'content': 'Verfahrensfrei sind in Bayern: Gebäude ohne Aufenthaltsräume bis 75 m³, Garagen und Carports bis 50 m² Grundfläche, Terrassenüberdachungen bis 30 m², Gartenhäuser bis 75 m³, Gewächshäuser bis 30 m². Auch Einfriedungen, Mauern, Stützmauern bis 2 m Höhe, Schwimmbecken bis 100 m³, Wärmepumpen und Solaranlagen sind verfahrensfrei.', 'source': 'BayBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bayern'},
    
    # Baden-Württemberg
    {'title': 'LBO BW § 5 - Abstandsflächen Baden-Württemberg', 'content': 'In Baden-Württemberg beträgt die Tiefe der Abstandsflächen 0,4 der Wandhöhe, mindestens 2,5 m. In Wohngebieten beträgt die Mindesttiefe 2,0 m. In Gewerbe- und Industriegebieten kann die Tiefe auf 0,2 H reduziert werden. Garagen, Carports und Nebenanlagen bis 3 m Höhe und insgesamt 15 m Länge sind an der Grenze zulässig.', 'source': 'LBO BW', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Baden-Württemberg'},
    {'title': 'LBO BW § 50 - Verfahrensfreie Vorhaben BW', 'content': 'Verfahrensfrei in Baden-Württemberg: Gebäude bis 40 m³, Garagen bis 30 m², Carports bis 40 m², Terrassenüberdachungen bis 30 m², Gartenhäuser bis 25 m³, Wintergärten bis 20 m². Solaranlagen auf Dächern und an Fassaden sind generell verfahrensfrei. Auch Wärmepumpen, Satellitenempfangsanlagen und temporäre Bauten sind verfahrensfrei.', 'source': 'LBO BW', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Baden-Württemberg'},
    
    # Nordrhein-Westfalen
    {'title': 'BauO NRW § 6 - Abstandsflächen NRW', 'content': 'In NRW beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In Gewerbe- und Industriegebieten genügt 0,2 H, mindestens 3 m. Garagen und Carports bis 3 m Höhe und 9 m Länge sind ohne Abstand zur Grenze zulässig. Bei Grenzbebauung ist die Zustimmung des Nachbarn nicht erforderlich, wenn die Bauordnung es erlaubt.', 'source': 'BauO NRW', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Nordrhein-Westfalen'},
    {'title': 'BauO NRW § 62 - Verfahrensfreie Vorhaben NRW', 'content': 'Verfahrensfrei in NRW: Gebäude bis 75 m³, Garagen bis 100 m² Brutto-Grundfläche, Carports bis 100 m², Terrassenüberdachungen bis 30 m², Gewächshäuser bis 50 m². Auch Schwimmbecken bis 100 m³, Solaranlagen auf Dächern und Wärmepumpen sind verfahrensfrei. Die Einhaltung der Abstandsflächen ist trotzdem erforderlich.', 'source': 'BauO NRW', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Nordrhein-Westfalen'},
    
    # Berlin
    {'title': 'BauO Bln § 6 - Abstandsflächen Berlin', 'content': 'In Berlin beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In Kern- und Gewerbegebieten kann sie auf 0,2 H reduziert werden. Untergeordnete Bauteile bis 1,5 m Tiefe und nicht mehr als 1/5 der Wandlänge bleiben bei der Berechnung unberücksichtigt. Garagen bis 3 m Höhe und 9 m Länge sind grenznah zulässig.', 'source': 'BauO Bln', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Berlin'},
    
    # Hamburg
    {'title': 'HBauO § 6 - Abstandsflächen Hamburg', 'content': 'In Hamburg beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 2,5 m. In den Innenstadtbereichen können geringere Abstände festgesetzt werden. Garagen und Carports bis 3 m Höhe sind an der Grenze zulässig. Die Hamburger Bauordnung ermöglicht flexible Regelungen durch die Bezirksämter.', 'source': 'HBauO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Hamburg'},
    
    # Hessen
    {'title': 'HBO § 6 - Abstandsflächen Hessen', 'content': 'In Hessen beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. Bei Wohngebäuden der Gebäudeklasse 1 und 2 beträgt der Mindestabstand 2 m. Garagen bis 3 m Höhe und 9 m Länge sind an der Grenze zulässig. Die Abstandsflächen müssen auf dem eigenen Grundstück liegen, können aber auf öffentlichen Verkehrsflächen enden.', 'source': 'HBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Hessen'},
    {'title': 'HBO § 63 - Verfahrensfreie Vorhaben Hessen', 'content': 'Verfahrensfrei in Hessen: Gebäude bis 30 m³ im Innenbereich, bis 50 m³ im Außenbereich, Garagen bis 50 m², Carports bis 50 m², Terrassenüberdachungen bis 30 m², Gartenhäuser bis 30 m³. Solaranlagen auf Dächern und an Fassaden, Wärmepumpen und Ladestationen für E-Fahrzeuge sind ebenfalls verfahrensfrei.', 'source': 'HBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Hessen'},
    
    # Niedersachsen
    {'title': 'NBauO § 5 - Abstandsflächen Niedersachsen', 'content': 'In Niedersachsen beträgt die Tiefe der Abstandsflächen 0,5 H, mindestens 3 m. In Gewerbe- und Industriegebieten kann die Tiefe auf 0,25 H reduziert werden. Garagen und Carports bis 3 m Höhe und 9 m Länge sind an der Grenze zulässig. Bei geschlossener Bauweise entfällt der seitliche Grenzabstand.', 'source': 'NBauO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Niedersachsen'},
    
    # Sachsen
    {'title': 'SächsBO § 6 - Abstandsflächen Sachsen', 'content': 'In Sachsen beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In Kern- und Gewerbegebieten ist eine Reduzierung auf 0,2 H möglich. Garagen bis 3 m Höhe und 9 m Länge können ohne Abstand zur Grenze errichtet werden. Die Grunderwerbsteuer in Sachsen beträgt 3,5%.', 'source': 'SächsBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Sachsen'},
    
    # Schleswig-Holstein
    {'title': 'LBO SH § 6 - Abstandsflächen Schleswig-Holstein', 'content': 'In Schleswig-Holstein beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. Vor Außenwänden mit Fenstern beträgt die Tiefe 0,4 H, sonst 0,2 H. Garagen bis 3 m Höhe und 9 m Länge sind an der Grenze zulässig. Die Grunderwerbsteuer in Schleswig-Holstein beträgt 6,5%.', 'source': 'LBO SH', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Schleswig-Holstein'},
    
    # Brandenburg
    {'title': 'BbgBO § 6 - Abstandsflächen Brandenburg', 'content': 'In Brandenburg beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In Gewerbe- und Industriegebieten genügt 0,2 H. Garagen und Carports bis 3 m Höhe und 9 m Länge sind grenznah zulässig. Die Grunderwerbsteuer in Brandenburg beträgt 6,5%, die höchste in Deutschland.', 'source': 'BbgBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Brandenburg'},
    
    # Rheinland-Pfalz
    {'title': 'LBauO RLP § 8 - Abstandsflächen Rheinland-Pfalz', 'content': 'In Rheinland-Pfalz beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In reinen Wohngebieten kann die Mindesttiefe auf 2 m reduziert werden. Garagen bis 3 m Höhe und 9 m Länge sind an der Grenze zulässig. Bei Dachneigung über 70 Grad ist die volle Dachhöhe anzurechnen.', 'source': 'LBauO RLP', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Rheinland-Pfalz'},
    
    # Thüringen
    {'title': 'ThürBO § 6 - Abstandsflächen Thüringen', 'content': 'In Thüringen beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In Gewerbe- und Industriegebieten genügt 0,2 H, mindestens 3 m. Garagen, Carports und Gewächshäuser bis 3 m Höhe und 9 m Länge sind grenznah zulässig. Die Grunderwerbsteuer in Thüringen beträgt 6,5%.', 'source': 'ThürBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Thüringen'},
    
    # Sachsen-Anhalt
    {'title': 'BauO LSA § 6 - Abstandsflächen Sachsen-Anhalt', 'content': 'In Sachsen-Anhalt beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. Vor Außenwänden von Wohngebäuden mit nicht mehr als zwei Wohnungen kann die Tiefe auf 0,25 H reduziert werden. Garagen bis 3 m Höhe sind grenznah zulässig.', 'source': 'BauO LSA', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Sachsen-Anhalt'},
    
    # Mecklenburg-Vorpommern
    {'title': 'LBauO M-V § 6 - Abstandsflächen Mecklenburg-Vorpommern', 'content': 'In Mecklenburg-Vorpommern beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In Kern- und Gewerbegebieten ist eine Reduzierung auf 0,2 H möglich. Garagen bis 3 m Höhe und 9 m Länge sind ohne Grenzabstand zulässig.', 'source': 'LBauO M-V', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Mecklenburg-Vorpommern'},
    
    # Saarland
    {'title': 'LBO SL § 7 - Abstandsflächen Saarland', 'content': 'Im Saarland beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. In allgemeinen und reinen Wohngebieten beträgt die Mindesttiefe 2,5 m. Garagen bis 3 m Höhe und 9 m Länge sind grenznah zulässig. Die Grunderwerbsteuer im Saarland beträgt 6,5%.', 'source': 'LBO SL', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Saarland'},
    
    # Bremen
    {'title': 'BremLBO § 6 - Abstandsflächen Bremen', 'content': 'In Bremen beträgt die Tiefe der Abstandsflächen 0,4 H, mindestens 3 m. Im Kerngebiet und in Gewerbegebieten genügt 0,2 H. Garagen bis 3 m Höhe und 9 m Länge sind ohne Grenzabstand zulässig. Bremen und Bremerhaven haben unterschiedliche Regelungen für Innenstadtbereiche.', 'source': 'BremLBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bremen'},
    
    # Allgemein
    {'title': 'Gebäudeklassen nach Musterbauordnung', 'content': 'Die Musterbauordnung definiert fünf Gebäudeklassen: GK 1: Freistehende Gebäude bis 7 m Höhe mit max. 2 Nutzungseinheiten bis je 400 m². GK 2: Wie GK 1, aber nicht freistehend. GK 3: Sonstige Gebäude bis 7 m Höhe. GK 4: Gebäude bis 13 m Höhe, max. 400 m² Nutzungseinheit. GK 5: Sonstige Gebäude einschließlich unterirdischer Gebäude. Die Gebäudeklasse bestimmt die Anforderungen an Brandschutz, Fluchtwege und Baustoffe.', 'source': 'MBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bund'},
    {'title': 'Brandschutz nach Landesbauordnungen', 'content': 'Brandschutzanforderungen nach Gebäudeklasse: GK 1-2: Tragende Wände und Decken feuerhemmend (F30). GK 3: Tragende Wände und Decken feuerhemmend, Treppenraumwände feuerbeständig. GK 4-5: Tragende Wände, Decken und Stützen feuerbeständig (F90). Rettungswege: Erster Rettungsweg über Treppe, zweiter über Leitern der Feuerwehr oder baulichen Rettungsweg. Notwendige Treppen müssen rauchsicher sein ab GK 4.', 'source': 'LBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bund'},
    {'title': 'Stellplatzpflicht nach Landesbauordnungen', 'content': 'Die Stellplatzpflicht variiert je nach Bundesland und Gemeinde. Richtwerte: Wohnungen: 1-2 Stellplätze je Wohnung. Bürogebäude: 1 Stellplatz je 30-40 m² Nutzfläche. Einzelhandel: 1 Stellplatz je 20-30 m² Verkaufsfläche. Bei Nichtherstellung: Ablöse zwischen 5.000-25.000 Euro je Stellplatz. Fahrradabstellplätze: 2-4 je Wohnung, vermehrt als Pflicht eingeführt. Elektroladestationen sind bei Neubauten teilweise vorgeschrieben.', 'source': 'LBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bund'},
    {'title': 'Barrierefreiheit nach Landesbauordnungen', 'content': 'Barrierefreiheit bei Wohngebäuden: Ab GK 3 (mehr als 2 Wohnungen): Erdgeschosswohnungen barrierefrei zugänglich. In Gebäuden mit mehr als 4 Wohnungen: Eine Wohnung je angefangene 8 Wohnungen barrierefrei und rollstuhlgerecht. Aufzugpflicht ab 4 Vollgeschosse oder 13 m Höhe in den meisten Bundesländern. Öffentlich zugängliche Gebäude müssen grundsätzlich barrierefrei sein.', 'source': 'LBO', 'category': 'Baurecht', 'doc_type': 'Gesetz', 'bundesland': 'Bund'},
]

print(f'📤 Uploading {len(lbo_docs)} Dokumente...')
points = []
for i, doc in enumerate(lbo_docs):
    vector = embed(doc['content'])
    points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=doc))
    if (i+1) % 10 == 0:
        print(f'  📝 {i+1}/{len(lbo_docs)} embedded...')

for i in range(0, len(points), 25):
    batch = points[i:i+25]
    client.upsert(collection_name='legal_documents', points=batch)
    print(f'  ✅ Batch {i//25+1}: {len(batch)} docs')

info = client.get_collection('legal_documents')
print(f'📊 Gesamt: {info.points_count} Dokumente')
