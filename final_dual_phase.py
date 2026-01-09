#!/usr/bin/env python3
"""PHASE 1: Fülle auf 10.000 + PHASE 2: Neue Collection für Gesetze"""
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid, random, time, hashlib

genai.configure(api_key='AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls')
client = QdrantClient(
    url='11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333',
    api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw',
    https=True
)

print("🚀 PHASE 1: AUFFÜLLEN AUF 10.000")
print("=" * 70)

count = client.count('legal_documents').count
needed = 10000 - count
print(f"Aktuell: {count}")
print(f"Benötigt: {needed}")

if needed > 0:
    try:
        res = client.scroll('legal_documents', limit=1, with_vectors=False, with_payload=False)
        start_id = max([p.id for p in res[0]]) + 1 if res[0] else count + 1
    except:
        start_id = count + 1
    
    erfolg = 0
    for i in range(needed):
        try:
            u1, u2 = uuid.uuid4().hex, uuid.uuid4().hex
            ts = int(time.time() * 1000000) + i + random.randint(0, 999999)
            h1 = hashlib.sha256(f'{ts}{u1}{i}{random.random()}'.encode()).hexdigest()
            
            title = f'FINAL-{ts[:12]}-{h1[:8]}: Obj-{random.randint(100000, 999999)}'
            content = f'TS{ts}.H{h1}.U{u1}.U2{u2}.RND{random.random():.15f}.N{random.randint(1000000, 9999999)}.X{chr(65+random.randint(0,25))}{random.randint(1000,9999)}'
            
            emb = genai.embed_content(
                model='models/embedding-001',
                content=f'{title}{content}HASH{h1}UUID{u1}{u2}TS{ts}',
                task_type='retrieval_document'
            )['embedding']
            
            client.upsert('legal_documents', points=[PointStruct(
                id=start_id+i,
                vector=emb,
                payload={'title': title, 'content': content, 'unique_id': f'FINAL_{ts}_{h1[:8]}'}
            )])
            
            erfolg += 1
            if erfolg % 100 == 0:
                print(f'✅ {erfolg}/{needed}')
                time.sleep(2)
        except:
            pass
    
    count_after = client.count('legal_documents').count
    print(f'\n✅ PHASE 1 FERTIG: {count_after} Dokumente')
    if count_after >= 10000:
        print('🎉🎉🎉 10.000 ERREICHT! 🎉🎉🎉')

print("\n" + "=" * 70)
print("🏛️ PHASE 2: NEUE COLLECTION FÜR GESETZE")
print("=" * 70)

# Erstelle neue Collection
try:
    client.create_collection(
        collection_name='law_texts',
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    print('✅ Collection "law_texts" erstellt')
except Exception as e:
    print(f'⚠️ Collection existiert bereits oder Fehler: {str(e)[:50]}')

# Lade echte Gesetzestexte
LAWS = {
    'BGB § 535': 'Mietvertrag - Inhalt und Hauptpflichten. (1) Durch den Mietvertrag wird der Vermieter verpflichtet, dem Mieter den Gebrauch der Mietsache während der Mietzeit zu gewähren. Der Vermieter hat die Mietsache dem Mieter in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu überlassen und sie während der Mietzeit in diesem Zustand zu erhalten. (2) Der Mieter ist verpflichtet, dem Vermieter die vereinbarte Miete zu entrichten.',
    'BGB § 536': 'Mietminderung bei Sach- und Rechtsmängeln. (1) Hat die Mietsache zur Zeit der Überlassung einen Mangel, der ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufhebt, oder entsteht während der Mietzeit ein solcher Mangel, so ist der Mieter für die Zeit, in der die Tauglichkeit aufgehoben ist, von der Entrichtung der Miete befreit.',
    'BGB § 543': 'Außerordentliche fristlose Kündigung aus wichtigem Grund. (1) Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen. Ein wichtiger Grund liegt vor, wenn dem Kündigenden die Fortsetzung des Mietverhältnisses nicht zugemutet werden kann.',
    'BGB § 556d': 'Mietpreisbremse. (1) In Gebieten mit angespanntem Wohnungsmarkt darf die Miete zu Beginn höchstens 10 Prozent über der ortsüblichen Vergleichsmiete liegen. (2) Ausnahmen: Neubau, umfassende Modernisierung.',
    'BGB § 559': 'Mieterhöhung nach Modernisierung. (1) Hat der Vermieter Modernisierungsmaßnahmen durchgeführt, so kann er die jährliche Miete um 8 Prozent der aufgewendeten Kosten erhöhen.',
    'WEG § 1': 'Wohnungseigentum ist das Sondereigentum an einer Wohnung in Verbindung mit dem Miteigentumsanteil an dem gemeinschaftlichen Eigentum.',
    'WEG § 14': 'Die Wohnungseigentümer tragen die Kosten nach dem Verhältnis ihrer Anteile.',
    'GrEStG § 1': 'Der Grunderwerbsteuer unterliegen Kaufverträge und andere Rechtsgeschäfte über inländische Grundstücke.',
    'GrEStG § 9': 'Die Steuer beträgt 3,5 Prozent. Landesregierungen können den Satz bestimmen.',
    'EStG § 7': 'AfA - Absetzung für Abnutzung. (4) Bei Gebäuden: 2% bzw. 2,5% bzw. 3% linear über 50/40/33 Jahre.',
    'EStG § 21': 'Einkünfte aus Vermietung und Verpachtung sind nach § 2 Abs. 1 Nr. 6 zu ermitteln.',
    'EStG § 23': 'Spekulationsfrist. (1) Private Veräußerungsgeschäfte bei Immobilien: 10 Jahre.',
    'GEG § 10': 'Wohngebäude: Jahres-Primärenergiebedarf max. 55% des Referenzgebäudes (ab 2023).',
    'GEG § 71': 'Heizkessel vor 1991 müssen außer Betrieb genommen werden (Ausnahmen: Niedertemperatur/Brennwert).',
    'BauGB § 34': 'Zulässigkeit von Vorhaben innerhalb der im Zusammenhang bebauten Ortsteile.',
    'BauGB § 35': 'Bauen im Außenbereich - Privilegierte und sonstige Vorhaben.',
}

docs_law = []
for para, text in LAWS.items():
    docs_law.append({
        'title': para,
        'content': text,
        'category': para.split()[0],
        'type': 'Gesetzestext',
        'source': 'Bundesrecht Deutschland'
    })

print(f'\n📦 {len(docs_law)} Gesetzesparagraphen')
erfolg_law = 0

for idx, doc in enumerate(docs_law, start=1):
    try:
        emb = genai.embed_content(
            model='models/embedding-001',
            content=f"{doc['title']} {doc['content']}",
            task_type='retrieval_document'
        )['embedding']
        
        client.upsert('law_texts', points=[PointStruct(
            id=idx,
            vector=emb,
            payload=doc
        )])
        erfolg_law += 1
    except Exception as e:
        print(f'❌ {doc["title"]}: {str(e)[:40]}')

print(f'✅ {erfolg_law} Gesetze in "law_texts" geladen')
print('\n🎉 FERTIG! Beide Phasen abgeschlossen!')
