#!/usr/bin/env python3
"""
SIMPLE MASSIVE SEEDING - Lädt alle in-memory Dokumente aus Scrapern
Ziel: Maximale Datenmenge in Qdrant Cloud
"""

import sys
import os
import time
import uuid
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

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
    print("=" * 80)
    print("🚀 SIMPLE MASSIVE SEEDING")
    print("=" * 80)
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Check current count
    collection_info = client.get_collection(COLLECTION_NAME)
    initial_count = collection_info.points_count
    print(f"\n📊 Start: {initial_count:,} Dokumente\n")
    
    all_documents = []
    
    # 1. LITERATUR SCRAPER
    print("\n1️⃣  LITERATUR")
    print("-" * 80)
    try:
        from ingestion.scrapers.literatur_scraper import LiteraturScraper
        scraper = LiteraturScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} Literatur-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 2. BGBSachenrecht
    print("\n2️⃣  BGB SACHENRECHT")
    print("-" * 80)
    try:
        from ingestion.scrapers.bgb_sachenrecht_scraper import BGBSachenrechtScraper
        scraper = BGBSachenrechtScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} BGB-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 3. LBO
    print("\n3️⃣  LANDESBAUORDNUNGEN")
    print("-" * 80)
    try:
        from ingestion.scrapers.lbo_scraper import LBOScraper
        scraper = LBOScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} LBO-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 4. BMF
    print("\n4️⃣  BMF-SCHREIBEN")
    print("-" * 80)
    try:
        from ingestion.scrapers.bmf_scraper import BMFScraper
        scraper = BMFScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} BMF-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 5. Immobilien Komplett
    print("\n5️⃣  IMMOBILIEN KOMPLETT")
    print("-" * 80)
    try:
        from ingestion.scrapers.immobilien_komplett_scraper import ImmobilienKomplettScraper
        scraper = ImmobilienKomplettScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} Immobilien-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 6. Complete Expansion
    print("\n6️⃣  COMPLETE EXPANSION")
    print("-" * 80)
    try:
        from ingestion.scrapers.complete_expansion_scraper import CompleteExpansionScraper
        scraper = CompleteExpansionScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} Expansion-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 7. Additional Laws
    print("\n7️⃣  ADDITIONAL LAWS")
    print("-" * 80)
    try:
        from ingestion.scrapers.additional_laws_scraper import AdditionalLawsScraper
        scraper = AdditionalLawsScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} Additional-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 8. EU Law
    print("\n8️⃣  EU LAW")
    print("-" * 80)
    try:
        from ingestion.scrapers.eu_law_scraper import EULawScraper
        scraper = EULawScraper()
        docs = scraper.scrape_all()
        print(f"   ✅ {len(docs)} EU-Dokumente")
        all_documents.extend(docs)
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    print(f"\n📦 GESAMT GELADEN: {len(all_documents)} Dokumente")
    
    # Upload in batches
    if all_documents:
        print("\n📤 Uploading zu Qdrant Cloud...")
        batch_size = 50
        total_batches = (len(all_documents) + batch_size - 1) // batch_size
        
        for i in range(0, len(all_documents), batch_size):
            batch = all_documents[i:i + batch_size]
            points = []
            
            for doc in batch:
                # Create embedding
                text = f"{doc.get('title', '')} {doc.get('content', '')}"
                try:
                    embedding = get_embedding(text)
                    
                    # Create point
                    point = PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload=doc
                    )
                    points.append(point)
                except Exception as e:
                    print(f"   ⚠️  Embedding error: {e}")
                    continue
            
            # Upload batch
            if points:
                client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
                print(f"   ✅ Batch {i//batch_size + 1}/{total_batches} ({len(points)} docs)")
                time.sleep(2)  # Rate limit
    
    # Final count
    collection_info = client.get_collection(COLLECTION_NAME)
    final_count = collection_info.points_count
    
    print("\n" + "=" * 80)
    print("✅ SEEDING ABGESCHLOSSEN!")
    print("=" * 80)
    print(f"\n📊 Start:       {initial_count:,} Dokumente")
    print(f"📊 Ende:        {final_count:,} Dokumente")
    print(f"📊 Hinzugefügt: {final_count - initial_count:,} Dokumente")
    print("\n🎉 Qdrant Cloud bereit!")

if __name__ == "__main__":
    main()
