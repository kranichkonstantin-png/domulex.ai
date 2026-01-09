#!/usr/bin/env python3
"""
COMPLETE SEEDING - Lädt ALLE Dokumente aus allen Scrapern mit korrekten Methoden
"""

import sys
import os
import time
import uuid
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

# Configuration
QDRANT_URL = "https://11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text[:8000],  # Limit
        task_type="retrieval_document"
    )
    return result['embedding']

def upload_docs(client, documents, name):
    """Upload documents to Qdrant"""
    if not documents:
        return 0
    
    print(f"   📤 Uploading {len(documents)} {name}...")
    batch_size = 50
    uploaded = 0
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        points = []
        
        for doc in batch:
            try:
                text = f"{doc.get('title', '')} {doc.get('content', '')}"
                embedding = get_embedding(text)
                
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=doc
                )
                points.append(point)
            except Exception as e:
                print(f"      ⚠️  Skip: {e}")
                continue
        
        if points:
            client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
            uploaded += len(points)
            print(f"      ✅ Batch {i//batch_size + 1}: {len(points)} docs")
            time.sleep(1)
    
    return uploaded

def main():
    print("=" * 80)
    print("🚀 COMPLETE SEEDING - Alle Scraper")
    print("=" * 80)
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    collection_info = client.get_collection(COLLECTION_NAME)
    initial_count = collection_info.points_count
    print(f"\n📊 Start: {initial_count:,} Dokumente\n")
    
    total_uploaded = 0
    
    # 1. BMF Scraper
    print("\n1️⃣  BMF-SCHREIBEN")
    print("-" * 60)
    try:
        from ingestion.scrapers.bmf_scraper import BMFScraper
        scraper = BMFScraper()
        docs = scraper.scrape_bmf_rulings()
        print(f"   📚 {len(docs)} BMF-Dokumente gefunden")
        total_uploaded += upload_docs(client, docs, "BMF")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 2. LBO Scraper
    print("\n2️⃣  LANDESBAUORDNUNGEN")
    print("-" * 60)
    try:
        from ingestion.scrapers.lbo_scraper import LBOScraper
        scraper = LBOScraper()
        docs = scraper.scrape_building_codes()
        print(f"   📚 {len(docs)} LBO-Dokumente gefunden")
        total_uploaded += upload_docs(client, docs, "LBO")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 3. Gesetze Scraper - Phase 1, 2, 3
    print("\n3️⃣  GESETZE (Phase 1-3)")
    print("-" * 60)
    try:
        from ingestion.scrapers.gesetze_scraper import GesetzeScraper
        scraper = GesetzeScraper()
        
        # Phase 1
        docs1 = scraper.scrape_phase_1()
        print(f"   Phase 1: {len(docs1)} Dokumente")
        total_uploaded += upload_docs(client, docs1, "Gesetze Phase 1")
        
        # Phase 2
        docs2 = scraper.scrape_phase_2()
        print(f"   Phase 2: {len(docs2)} Dokumente")
        total_uploaded += upload_docs(client, docs2, "Gesetze Phase 2")
        
        # Phase 3
        docs3 = scraper.scrape_phase_3()
        print(f"   Phase 3: {len(docs3)} Dokumente")
        total_uploaded += upload_docs(client, docs3, "Gesetze Phase 3")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 4. BGB Sachenrecht
    print("\n4️⃣  BGB SACHENRECHT")
    print("-" * 60)
    try:
        from ingestion.scrapers.bgb_sachenrecht_scraper import BGBSachenrechtScraper
        scraper = BGBSachenrechtScraper()
        # Check methods
        methods = [m for m in dir(scraper) if m.startswith('scrape')]
        for method in methods:
            try:
                func = getattr(scraper, method)
                docs = func()
                if docs:
                    print(f"   {method}: {len(docs)} Dokumente")
                    total_uploaded += upload_docs(client, docs, f"BGB {method}")
            except:
                pass
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 5. Complete Expansion (async)
    print("\n5️⃣  COMPLETE EXPANSION")
    print("-" * 60)
    try:
        from ingestion.scrapers.complete_expansion_scraper import CompleteExpansionScraper
        scraper = CompleteExpansionScraper()
        docs = asyncio.run(scraper.scrape_all_expansion_documents())
        print(f"   📚 {len(docs)} Expansion-Dokumente gefunden")
        total_uploaded += upload_docs(client, docs, "Expansion")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 6. Immobilien Komplett
    print("\n6️⃣  IMMOBILIEN KOMPLETT")
    print("-" * 60)
    try:
        from ingestion.scrapers.immobilien_komplett_scraper import ImmobilienKomplettScraper
        scraper = ImmobilienKomplettScraper()
        methods = [m for m in dir(scraper) if m.startswith('scrape')]
        for method in methods:
            try:
                func = getattr(scraper, method)
                docs = func()
                if docs:
                    print(f"   {method}: {len(docs)} Dokumente")
                    total_uploaded += upload_docs(client, docs, f"Immobilien {method}")
            except:
                pass
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 7. EU Law
    print("\n7️⃣  EU LAW")
    print("-" * 60)
    try:
        from ingestion.scrapers.eu_law_scraper import EULawScraper
        scraper = EULawScraper()
        methods = [m for m in dir(scraper) if m.startswith('scrape')]
        for method in methods:
            try:
                func = getattr(scraper, method)
                docs = func()
                if docs:
                    print(f"   {method}: {len(docs)} Dokumente")
                    total_uploaded += upload_docs(client, docs, f"EU {method}")
            except:
                pass
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # 8. Additional Laws
    print("\n8️⃣  ADDITIONAL LAWS")
    print("-" * 60)
    try:
        from ingestion.scrapers.additional_laws_scraper import AdditionalLawsScraper
        scraper = AdditionalLawsScraper()
        methods = [m for m in dir(scraper) if m.startswith('scrape')]
        for method in methods:
            try:
                func = getattr(scraper, method)
                docs = func()
                if docs:
                    print(f"   {method}: {len(docs)} Dokumente")
                    total_uploaded += upload_docs(client, docs, f"Add {method}")
            except:
                pass
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # Final
    collection_info = client.get_collection(COLLECTION_NAME)
    final_count = collection_info.points_count
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE SEEDING FERTIG!")
    print("=" * 80)
    print(f"\n📊 Start:       {initial_count:,} Dokumente")
    print(f"📊 Ende:        {final_count:,} Dokumente")
    print(f"📊 Hochgeladen: {total_uploaded:,} Dokumente")
    print(f"📊 Neu:         {final_count - initial_count:,} Dokumente")

if __name__ == "__main__":
    main()
