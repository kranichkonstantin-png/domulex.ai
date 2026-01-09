#!/usr/bin/env python3
"""
MASSIVE SEEDING - Lädt ALLE verfügbaren Dokumente aus allen Scrapern
Ziel: 10.000+ Dokumente in Qdrant Cloud
"""

import sys
import os
import asyncio
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

# Import all scrapers
# Import only working scrapers (no external dependencies)
try:
    from ingestion.scrapers.literatur_scraper import LiteraturScraper
    HAS_LITERATUR = True
except:
    HAS_LITERATUR = False

try:
    from ingestion.scrapers.bgh_scraper import BGHScraper
    HAS_BGH = True
except:
    HAS_BGH = False

try:
    from ingestion.scrapers.bfh_scraper import BFHScraper
    HAS_BFH = True
except:
    HAS_BFH = False

try:
    from ingestion.scrapers.urteile_immobilien_scraper import UrteileImmobilienScraper
    HAS_URTEILE = True
except:
    HAS_URTEILE = False

try:
    from ingestion.scrapers.bmf_scraper import BMFScraper
    HAS_BMF = True
except:
    HAS_BMF = False

try:
    from ingestion.scrapers.lbo_scraper import LBOScraper
    HAS_LBO = True
except:
    HAS_LBO = False

try:
    from ingestion.scrapers.gesetze_scraper import GesetzeScraper
    HAS_GESETZE = True
except:
    HAS_GESETZE = False

try:
    from ingestion.scrapers.bgb_sachenrecht_scraper import BGBSachenrechtScraper
    HAS_BGB = True
except:
    HAS_BGB = False

try:
    from ingestion.scrapers.complete_expansion_scraper import CompleteExpansionScraper
    HAS_EXPANSION = True
except:
    HAS_EXPANSION = False

try:
    from ingestion.scrapers.immobilien_komplett_scraper import ImmobilienKomplettScraper
    HAS_IMMOBILIEN = True
except:
    HAS_IMMOBILIEN = False

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

def upload_documents(client, documents, batch_size=50):
    """Upload documents to Qdrant in batches"""
    print(f"\n📤 Uploading {len(documents)} documents...")
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        points = []
        
        for doc in batch:
            # Create embedding
            text = f"{doc.get('title', '')} {doc.get('content', '')}"
            embedding = get_embedding(text)
            
            # Create point
            point = PointStruct(
                id=doc.get('id', str(hash(text))),
                vector=embedding,
                payload=doc
            )
            points.append(point)
        
        # Upload batch
        client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
        print(f"   ✅ Batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size} uploaded")
        time.sleep(2)  # Rate limit

async def main():
    print("=" * 80)
    print("🚀 MASSIVE SEEDING - ALLE SCRAPER")
    print("=" * 80)
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Check current count
    collection_info = client.get_collection(COLLECTION_NAME)
    initial_count = collection_info.points_count
    print(f"\n📊 Start: {initial_count} Dokumente\n")
    
    all_documents = []
    
    # 1. LITERATUR SCRAPER (größter!)
    if HAS_LITERATUR:
        print("\n1️⃣  LITERATUR - Kommentare")
        print("-" * 80)
        lit_scraper = LiteraturScraper()
        try:
            lit_docs = await lit_scraper.scrape_all_kommentare()
            print(f"   ✅ {len(lit_docs)} Kommentar-Dokumente")
            all_documents.extend(lit_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 2. BGH SCRAPER
    if HAS_BGH:
        print("\n2️⃣  BGH - Bundesgerichtshof")
        print("-" * 80)
        bgh_scraper = BGHScraper()
        try:
            bgh_docs = await bgh_scraper.scrape_all_senate()
            print(f"   ✅ {len(bgh_docs)} BGH-Urteile")
            all_documents.extend(bgh_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 3. BFH SCRAPER
    if HAS_BFH:
        print("\n3️⃣  BFH - Bundesfinanzhof")
        print("-" * 80)
        bfh_scraper = BFHScraper()
        try:
            bfh_docs = await bfh_scraper.scrape_all_immobilien()
            print(f"   ✅ {len(bfh_docs)} BFH-Urteile")
            all_documents.extend(bfh_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 4. URTEILE IMMOBILIEN
    if HAS_URTEILE:
        print("\n4️⃣  URTEILE - Immobilienrecht")
        print("-" * 80)
        urt_scraper = UrteileImmobilienScraper()
        try:
            urt_docs = await urt_scraper.scrape_all_gerichte()
            print(f"   ✅ {len(urt_docs)} Immobilien-Urteile")
            all_documents.extend(urt_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 5. BMF SCRAPER
    if HAS_BMF:
        print("\n5️⃣  BMF - Bundesministerium der Finanzen")
        print("-" * 80)
        bmf_scraper = BMFScraper()
        try:
            bmf_docs = await bmf_scraper.scrape_all_schreiben()
            print(f"   ✅ {len(bmf_docs)} BMF-Schreiben")
            all_documents.extend(bmf_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 6. LANDESBAUORDNUNGEN
    if HAS_LBO:
        print("\n6️⃣  LBOs - Landesbauordnungen")
        print("-" * 80)
        lbo_scraper = LBOScraper()
        try:
            lbo_docs = await lbo_scraper.scrape_all_bundeslaender()
            print(f"   ✅ {len(lbo_docs)} LBO-Dokumente")
            all_documents.extend(lbo_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 7. GESETZE SCRAPER
    if HAS_GESETZE:
        print("\n7️⃣  GESETZE - Alle Immobiliengesetze")
        print("-" * 80)
        ges_scraper = GesetzeScraper()
        try:
            ges_docs = await ges_scraper.scrape_all_gesetze()
            print(f"   ✅ {len(ges_docs)} Gesetzes-Paragraphen")
            all_documents.extend(ges_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 8. BGB SACHENRECHT
    if HAS_BGB:
        print("\n8️⃣  BGB - Sachenrecht komplett")
        print("-" * 80)
        bgb_scraper = BGBSachenrechtScraper()
        try:
            bgb_docs = await bgb_scraper.scrape_all_sachenrecht()
            print(f"   ✅ {len(bgb_docs)} BGB Sachenrecht")
            all_documents.extend(bgb_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 9. COMPLETE EXPANSION
    if HAS_EXPANSION:
        print("\n9️⃣  EXPANSION - Alle fehlenden Dokumente")
        print("-" * 80)
        exp_scraper = CompleteExpansionScraper()
        try:
            exp_docs = await exp_scraper.scrape_all_expansion_documents()
            print(f"   ✅ {len(exp_docs)} Expansion-Dokumente")
            all_documents.extend(exp_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # 10. IMMOBILIEN KOMPLETT
    if HAS_IMMOBILIEN:
        print("\n🔟 IMMOBILIEN KOMPLETT")
        print("-" * 80)
        immo_scraper = ImmobilienKomplettScraper()
        try:
            immo_docs = await immo_scraper.scrape_all()
            print(f"   ✅ {len(immo_docs)} Immobilien-Dokumente")
            all_documents.extend(immo_docs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    
    # Upload all
    if all_documents:
        upload_documents(client, all_documents)
    
    # Final count
    collection_info = client.get_collection(COLLECTION_NAME)
    final_count = collection_info.points_count
    
    print("\n" + "=" * 80)
    print("✅ MASSIVE SEEDING ABGESCHLOSSEN!")
    print("=" * 80)
    print(f"\n📊 Start:       {initial_count:,} Dokumente")
    print(f"📊 Ende:        {final_count:,} Dokumente")
    print(f"📊 Hinzugefügt: {final_count - initial_count:,} Dokumente")
    print("\n🎉 Qdrant Cloud ist bereit für Produktion!")

if __name__ == "__main__":
    asyncio.run(main())
