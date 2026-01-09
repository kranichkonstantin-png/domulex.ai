#!/usr/bin/env python3
"""
Seed Immobilienrecht KOMPLETT - Lädt alle 5 Häppchen
Fügt ~195 neue Dokumente hinzu (55 + 35 + 35 + 35 + 35)
"""

import asyncio
import sys
import os
import time
import uuid
from datetime import datetime

# Add scrapers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'ingestion', 'scrapers'))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

# Import directly
from immobilien_komplett_scraper import ImmobilienKomplettScraper

# Configuration
QDRANT_URL = "https://11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"


def get_embedding(text: str) -> list:
    """Get embedding from Gemini"""
    genai.configure(api_key=GEMINI_API_KEY)
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']


def main():
    print("\n" + "="*60)
    print("🏠 IMMOBILIENRECHT KOMPLETT - Seeding Script")
    print("="*60 + "\n")
    
    # Initialize
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    scraper = ImmobilienKomplettScraper()
    
    # Check current count
    collection_info = client.get_collection(COLLECTION_NAME)
    start_count = collection_info.points_count
    print(f"📊 Aktuell in Qdrant: {start_count} Dokumente\n")
    
    all_docs = []
    
    # Häppchen 1: Maklerrecht + Mietpreisbremse + ZVG (55 docs)
    print("📦 Häppchen 1: Maklerrecht + Mietpreisbremse + ZVG...")
    docs1 = scraper.scrape_haeppchen_1()
    all_docs.extend(docs1)
    print(f"   ✅ {len(docs1)} Dokumente geladen\n")
    
    # Häppchen 2: HOAI + Erbbaurecht + Notarrecht (35 docs)
    print("📦 Häppchen 2: HOAI + Erbbaurecht + Notarrecht...")
    docs2 = scraper.scrape_haeppchen_2()
    all_docs.extend(docs2)
    print(f"   ✅ {len(docs2)} Dokumente geladen\n")
    
    # Häppchen 3: BGB Kaufrecht + Werkvertragsrecht (35 docs)
    print("📦 Häppchen 3: BGB Kaufrecht + Werkvertragsrecht...")
    docs3 = scraper.scrape_haeppchen_3()
    all_docs.extend(docs3)
    print(f"   ✅ {len(docs3)} Dokumente geladen\n")
    
    # Häppchen 4: BauGB + VOB/B (35 docs)
    print("📦 Häppchen 4: BauGB + VOB/B...")
    docs4 = scraper.scrape_haeppchen_4()
    all_docs.extend(docs4)
    print(f"   ✅ {len(docs4)} Dokumente geladen\n")
    
    # Häppchen 5: WEG + GEG (35 docs)
    print("📦 Häppchen 5: WEG + GEG...")
    docs5 = scraper.scrape_haeppchen_5()
    all_docs.extend(docs5)
    print(f"   ✅ {len(docs5)} Dokumente geladen\n")
    
    print(f"📋 Gesamt: {len(all_docs)} neue Dokumente zu verarbeiten\n")
    print("="*60)
    
    # Generate embeddings and upload
    points = []
    total = len(all_docs)
    
    for i, doc in enumerate(all_docs, 1):
        try:
            # Rate limiting
            if i > 1:
                time.sleep(3)  # 3 Sekunden zwischen Anfragen
            
            # Generate embedding
            embedding = get_embedding(doc['content'])
            
            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "content": doc['content'],
                    "jurisdiction": doc.get('jurisdiction', 'DE'),
                    "language": doc.get('language', 'de'),
                    "source": doc.get('source', ''),
                    "source_url": doc.get('source_url', ''),
                    "topics": doc.get('topics', []),
                    "law": doc.get('law', ''),
                    "section": doc.get('section', ''),
                    "last_updated": doc.get('last_updated', datetime.utcnow().isoformat())
                }
            )
            points.append(point)
            
            # Progress
            if i % 10 == 0 or i == total:
                print(f"   [{i}/{total}] Embeddings generiert...")
            
            # Upload in batches of 50
            if len(points) >= 50:
                client.upsert(collection_name=COLLECTION_NAME, points=points)
                print(f"   📤 {len(points)} Punkte hochgeladen")
                points = []
                
        except Exception as e:
            print(f"   ⚠️ Fehler bei Dokument {i}: {e}")
            time.sleep(5)  # Längere Pause bei Fehler
            continue
    
    # Upload remaining points
    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"   📤 {len(points)} verbleibende Punkte hochgeladen")
    
    # Final count
    collection_info = client.get_collection(COLLECTION_NAME)
    end_count = collection_info.points_count
    
    print("\n" + "="*60)
    print("📊 ERGEBNIS")
    print("="*60)
    print(f"   Vorher:  {start_count} Dokumente")
    print(f"   Nachher: {end_count} Dokumente")
    print(f"   NEU:     +{end_count - start_count} Dokumente")
    print("="*60)
    print("✅ FERTIG! Immobilienrecht KOMPLETT geladen!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
