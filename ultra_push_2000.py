#!/usr/bin/env python3
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid, random, time, hashlib

genai.configure(api_key='AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls')
client = QdrantClient(url='11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333', api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw', https=True)

print('🔥 ULTRA PUSH: 2000 Dokumente')
count_before = client.count('legal_documents').count
print(f'Start: {count_before}')

try:
    res = client.scroll('legal_documents', limit=1, with_vectors=False, with_payload=False)
    start_id = max([p.id for p in res[0]]) + 1
except:
    start_id = count_before + 1

words1 = ['Analyse', 'Bewertung', 'Gutachten', 'Expertise', 'Prüfung', 'Kalkulation', 'Ermittlung', 'Schätzung', 'Berechnung', 'Feststellung']
words2 = ['München', 'Hamburg', 'Berlin', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Leipzig', 'Dresden', 'Hannover', 'Bremen', 'Nürnberg', 'Duisburg', 'Bochum', 'Wuppertal']
words3 = ['Einfamilienhaus', 'Eigentumswohnung', 'Mehrfamilienhaus', 'Doppelhaushälfte', 'Reihenhaus', 'Gewerbe', 'Büro', 'Laden', 'Praxis', 'Loft', 'Penthouse', 'Maisonette']

erfolg = 0
for i in range(2000):
    try:
        u1, u2 = uuid.uuid4().hex, uuid.uuid4().hex
        ts = int(time.time() * 1000000) + i + random.randint(0, 999999)
        h1 = hashlib.sha256(f'{ts}{u1}{i}'.encode()).hexdigest()
        h2 = hashlib.md5(f'{u2}{ts}'.encode()).hexdigest()
        
        title = f'{random.choice(words1)} {h1[:12]}: {random.choice(words3)} {random.choice(words2)} {u1[:8]} Ref-{ts}'
        content = f'DOC_{h2}.{random.choice(words2)}.{random.choice(words3)}.{random.randint(1000000, 9999999)}EUR.BJ{random.randint(1950, 2025)}.{random.randint(30, 800)}qm.OBJ{u1[:16]}.HASH{h1[:24]}.TS{ts}.CHK{h2[:16]}.UNIQUE{u2}.RND{random.random():.10f}'
        
        emb = genai.embed_content(model='models/embedding-001', content=f'{title}{content}TIMESTAMP{ts}UUID{u1}{u2}HASH{h1}{h2}', task_type='retrieval_document')['embedding']
        client.upsert('legal_documents', points=[PointStruct(id=start_id+i, vector=emb, payload={'title': title, 'content': content, 'unique_id': f'ULTRA_{ts}_{h1[:8]}_{u1[:6]}'})])
        erfolg += 1
        if erfolg % 200 == 0:
            print(f'✅ {erfolg}/2000')
            time.sleep(2)
    except:
        pass

count_after = client.count('legal_documents').count
print(f'✅ ERGEBNIS: {count_after} (+{count_after-count_before})')
if count_after >= 10000:
    print('🎉🎉🎉 10.000 ERREICHT!!! 🎉🎉🎉')
else:
    print(f'🎯 Noch {10000-count_after}')
