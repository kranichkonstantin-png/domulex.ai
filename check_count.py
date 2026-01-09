#!/usr/bin/env python3
from qdrant_client import QdrantClient
c = QdrantClient(
    url='11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333',
    api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw',
    https=True
)
n1 = c.count('legal_documents').count
n2 = c.count('law_texts').count
print(f'\n📊 legal_documents: {n1} ({n1/100:.1f}%)')
print(f'📊 law_texts: {n2} Gesetzestexte')
print(f'📊 GESAMT: {n1+n2} Dokumente')
print(f'🎯 Noch {50000-n2} law_texts bis 50.000\n')
