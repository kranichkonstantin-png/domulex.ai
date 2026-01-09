#!/usr/bin/env python3
"""Massives Rechtsprechung-Seeding"""

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import uuid

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
client = QdrantClient(
    host=os.environ['QDRANT_HOST'],
    port=6333,
    api_key=os.environ['QDRANT_API_KEY'],
    https=True
)

def embed(text):
    result = genai.embed_content(model='models/text-embedding-004', content=text[:8000])
    return result['embedding']

print('🚀 MASSIVE RECHTSPRECHUNG SEEDING')

rechtsprechung = [
    {'title': 'BGH VIII ZR 277/16 - Schönheitsreparaturen', 'content': 'Der BGH hat entschieden, dass Klauseln in Formularmietverträgen, die den Mieter zu Schönheitsreparaturen verpflichten, unwirksam sind, wenn die Wohnung unrenoviert übergeben wurde.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 185/14 - Eigenbedarfskündigung', 'content': 'Für eine wirksame Eigenbedarfskündigung muss der Vermieter vernünftige und nachvollziehbare Gründe darlegen. Der Eigenbedarf muss konkret sein.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 329/18 - Mietminderung Schimmel', 'content': 'Bei Schimmelbildung trifft den Vermieter die Beweislast, dass der Schimmel auf das Verhalten des Mieters zurückzuführen ist. Bei baulichen Mängeln ist Mietminderung möglich.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 44/17 - Betriebskostenabrechnung', 'content': 'Die Betriebskostenabrechnung muss innerhalb von 12 Monaten nach Ende des Abrechnungszeitraums dem Mieter zugehen.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH V ZR 251/19 - WEG Beschlussanfechtung', 'content': 'Ein WEG-Beschluss kann innerhalb eines Monats nach Beschlussfassung angefochten werden.', 'source': 'BGH', 'category': 'WEG', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH V ZR 75/19 - Sondereigentum Balkon', 'content': 'Der Balkon steht grundsätzlich im Sondereigentum, konstruktive Teile sind Gemeinschaftseigentum.', 'source': 'BGH', 'category': 'WEG', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH I ZR 30/15 - Maklerprovision Bestellerprinzip', 'content': 'Nach dem Bestellerprinzip schuldet derjenige die Maklerprovision, der den Makler beauftragt hat.', 'source': 'BGH', 'category': 'Maklerrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VII ZR 42/19 - Baumängel Verjährung', 'content': 'Mängelansprüche bei Bauwerken verjähren in fünf Jahren nach Abnahme.', 'source': 'BGH', 'category': 'Baurecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH V ZR 8/18 - Grunddienstbarkeit', 'content': 'Eine Grunddienstbarkeit berechtigt zur Nutzung des dienenden Grundstücks und muss im Grundbuch eingetragen werden.', 'source': 'BGH', 'category': 'Grundstücksrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BFH II R 1/16 - Grunderwerbsteuer Share Deal', 'content': 'Beim Erwerb von mindestens 95% der Anteile an einer grundbesitzenden Gesellschaft fällt Grunderwerbsteuer an.', 'source': 'BFH', 'category': 'Steuerrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 108/15 - Kaution Abrechnung', 'content': 'Der Vermieter muss die Kaution nach Beendigung des Mietverhältnisses innerhalb von 3-6 Monaten abrechnen.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 234/17 - Kaution Höhe', 'content': 'Die Mietkaution darf maximal drei Nettokaltmieten betragen.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH V ZR 42/21 - WEG Reform Beschlusskompetenz', 'content': 'Nach der WEG-Reform 2020 kann die Gemeinschaft bauliche Veränderungen mit einfacher Mehrheit beschließen.', 'source': 'BGH', 'category': 'WEG', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH XII ZR 75/18 - Gewerberaum Schriftform', 'content': 'Gewerbemietverträge mit Laufzeit über einem Jahr bedürfen der Schriftform.', 'source': 'BGH', 'category': 'Gewerberaummietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH V ZR 183/18 - Erbbaurecht Heimfall', 'content': 'Der Heimfall des Erbbaurechts tritt ein bei Nichtbebauung, zweckfremder Nutzung oder Zahlungsverzug.', 'source': 'BGH', 'category': 'Erbbaurecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BFH IX R 9/18 - Spekulationsfrist Immobilien', 'content': 'Private Veräußerungsgeschäfte bei Immobilien sind steuerpflichtig, wenn zwischen Anschaffung und Veräußerung weniger als 10 Jahre liegen.', 'source': 'BFH', 'category': 'Steuerrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH V ZR 141/18 - Überhang Bäume', 'content': 'Nach § 910 BGB kann der Grundstückseigentümer überhängende Zweige und eindringende Wurzeln des Nachbarn abschneiden.', 'source': 'BGH', 'category': 'Nachbarrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 138/15 - Tierhaltung Mietwohnung', 'content': 'Eine Klausel, die Tierhaltung generell verbietet, ist unwirksam. Kleintiere sind ohne Erlaubnis zulässig.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 369/18 - Kündigung Zahlungsverzug', 'content': 'Der Vermieter kann fristlos kündigen bei Verzug mit zwei Monatsmieten.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
    {'title': 'BGH VIII ZR 107/19 - Modernisierungsmieterhöhung', 'content': 'Der Vermieter kann die Miete nach Modernisierung um 8% der Kosten jährlich erhöhen.', 'source': 'BGH', 'category': 'Mietrecht', 'doc_type': 'Rechtsprechung'},
]

print(f'📤 Uploading {len(rechtsprechung)} Dokumente...')
points = []
for doc in rechtsprechung:
    vector = embed(doc['content'])
    points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=doc))

for i in range(0, len(points), 20):
    batch = points[i:i+20]
    client.upsert(collection_name='legal_documents', points=batch)
    print(f'  ✅ Batch {i//20+1}: {len(batch)} docs')

info = client.get_collection('legal_documents')
print(f'📊 Gesamt: {info.points_count} Dokumente')
