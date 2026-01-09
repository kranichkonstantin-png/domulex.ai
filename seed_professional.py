"""
Professional Qdrant Seeding Script
Seeds comprehensive legal database with German, US, and Spanish laws
"""

import os
import sys
import time
import asyncio
import uuid
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import google.generativeai as genai

# Configuration
QDRANT_URL = "https://11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"
COLLECTION_NAME = "legal_documents"

# Initialize
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)


def generate_embedding(text: str) -> list:
    """Generate embedding using Gemini text-embedding-004"""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]


async def seed_database():
    """Seed Qdrant with comprehensive legal documents"""
    
    print("🚀 DOMULEX Professional Database Seeding")
    print("=" * 60)
    
    # Check/Create collection
    try:
        qdrant.get_collection(COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' exists")
    except:
        print(f"📦 Creating collection '{COLLECTION_NAME}'...")
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"✅ Collection created")
    
    # Import scraper directly
    sys.path.insert(0, str(Path(__file__).parent / "backend" / "ingestion" / "scrapers"))
    from german_laws_scraper import GermanLawsScraper
    from bgh_scraper import BGHScraper
    from bfh_scraper import BFHScraper
    from lbo_scraper import LBOScraper
    from eu_law_scraper import EULawScraper
    from additional_laws_scraper import AdditionalLawsScraper
    from bmf_scraper import BMFScraper
    from complete_expansion_scraper import CompleteExpansionScraper
    
    print("=" * 60)
    
    scraper = GermanLawsScraper()
    
    # Get BGB Mietrecht
    print("\n🇩🇪 Scraping BGB Mietrecht (§§ 535-580a)...")
    bgb_docs = await scraper.scrape_bgb_mietrecht()
    print(f"   Found {len(bgb_docs)} paragraphs")
    
    # Get WEG
    print("\n🇩🇪 Scraping WEG (Wohnungseigentumsgesetz)...")
    weg_docs = await scraper.scrape_weg()
    print(f"   Found {len(weg_docs)} paragraphs")
    
    print("\n" + "=" * 60)
    print("⚖️  PHASE 2: BGH Case Law (Landmark Cases)")
    print("=" * 60)
    
    bgh_scraper = BGHScraper()
    
    # Get BGH landmark cases
    print("\n⚖️  Scraping BGH landmark cases...")
    bgh_docs = await bgh_scraper.scrape_recent_decisions()
    print(f"   Found {len(bgh_docs)} landmark cases")
    
    print("\n" + "=" * 60)
    print("💼 PHASE 3: BFH Tax Cases (Real Estate Tax Law)")
    print("=" * 60)
    
    bfh_scraper = BFHScraper()
    
    # Get BFH tax cases
    print("\n💼 Scraping BFH tax cases...")
    bfh_docs = await bfh_scraper.scrape_recent_rulings()
    print(f"   Found {len(bfh_docs)} tax cases")
    
    print("\n" + "=" * 60)
    print("🏛️  PHASE 4: Landesbauordnungen (Building Codes)")
    print("=" * 60)
    
    lbo_scraper = LBOScraper()
    
    # Get LBO regulations
    print("\n🏛️  Scraping Landesbauordnungen (16 Bundesländer)...")
    lbo_docs = await lbo_scraper.scrape_building_codes()
    print(f"   Found {len(lbo_docs)} building regulations")
    
    print("\n" + "=" * 60)
    print("🇪🇺 PHASE 5: EU-Recht (DSGVO, Verbraucherschutz)")
    print("=" * 60)
    
    eu_scraper = EULawScraper()
    
    # Get EU regulations
    print("\n🇪🇺 Scraping EU-Recht (DSGVO, Energy, Consumer)...")
    eu_docs = await eu_scraper.scrape_eu_regulations()
    print(f"   Found {len(eu_docs)} EU regulations")
    
    print("\n" + "=" * 60)
    print("📜 PHASE 6: Zusätzliche Gesetze (GEG, BauGB, BGB Kaufrecht)")
    print("=" * 60)
    
    additional_scraper = AdditionalLawsScraper()
    
    # Get additional laws
    print("\n📜 Scraping zusätzliche Gesetze...")
    additional_docs = await additional_scraper.scrape_additional_laws()
    print(f"   Found {len(additional_docs)} additional laws")
    
    print("\n" + "=" * 60)
    print("💼 PHASE 7: BMF-Schreiben (Steuerliche Verwaltungsanweisungen)")
    print("=" * 60)
    
    bmf_scraper = BMFScraper()
    
    # Get BMF rulings
    print("\n💼 Scraping BMF-Schreiben...")
    bmf_docs = await bmf_scraper.scrape_bmf_rulings()
    print(f"   Found {len(bmf_docs)} BMF rulings")
    
    print("\n" + "=" * 60)
    print("🚀 PHASE 8: VOLLSTÄNDIGKEITS-EXPANSION (90+ neue Dokumente)")
    print("=" * 60)
    
    expansion_scraper = CompleteExpansionScraper()
    
    # Get expansion documents
    print("\n🚀 Scraping BGB Sachenrecht (35) + GBO (25) + BGB Kaufrecht Start...")
    expansion_docs = await expansion_scraper.scrape_all_expansion_documents()
    print(f"   Found {len(expansion_docs)} expansion documents")
    
    all_docs = bgb_docs + weg_docs + bgh_docs + bfh_docs + lbo_docs + eu_docs + additional_docs + bmf_docs + expansion_docs
    
    print(f"\n📊 Total documents to process: {len(all_docs)}")
    print("=" * 60)
    
    # Process and upload
    points = []
    
    for i, doc in enumerate(all_docs, 1):
        print(f"\n[{i}/{len(all_docs)}] Processing: {doc['source']}")
        
        try:
            # Generate embedding
            embedding = generate_embedding(doc["content"])
            
            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),  # Use UUID instead of string ID
                vector=embedding,
                payload={
                    "doc_id": doc["id"],  # Store original ID in payload
                    "content": doc["content"],
                    "jurisdiction": doc["jurisdiction"],
                    "language": doc["language"],
                    "source": doc["source"],
                    "source_url": doc.get("source_url", ""),
                    "topics": doc["topics"],
                    "law": doc["law"],
                    "section": doc["section"],
                    "last_updated": doc["last_updated"]
                }
            )
            points.append(point)
            print(f"   ✅ Embedded successfully ({len(embedding)} dimensions)")
            
            # Wait to avoid rate limits
            if i < len(all_docs):
                print(f"   ⏳ Waiting 5 seconds...")
                time.sleep(5)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    # Upload to Qdrant
    print("\n" + "=" * 60)
    print(f"📤 Uploading {len(points)} documents to Qdrant Cloud...")
    print("=" * 60)
    
    try:
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )
        print(f"✅ Upload successful!")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return
    
    # Verify
    collection_info = qdrant.get_collection(COLLECTION_NAME)
    print("\n" + "=" * 60)
    print("📊 FINAL STATISTICS")
    print("=" * 60)
    print(f"Total documents in Qdrant: {collection_info.points_count}")
    print(f"BGB Mietrecht: {len(bgb_docs)} paragraphs")
    print(f"WEG: {len(weg_docs)} paragraphs")
    print(f"BGH Case Law: {len(bgh_docs)} landmark cases")
    print(f"BFH Tax Cases: {len(bfh_docs)} cases")
    print(f"Landesbauordnungen: {len(lbo_docs)} building regulations")
    print(f"EU-Recht: {len(eu_docs)} regulations")
    print(f"Zusätzliche Gesetze: {len(additional_docs)} laws")
    print(f"BMF-Schreiben: {len(bmf_docs)} rulings")
    print(f"Vollständigkeits-Expansion: {len(expansion_docs)} documents")
    print(f"\n⭐ NEUE GESAMT-DOKUMENTE: {len(bgb_docs) + len(weg_docs) + len(bgh_docs) + len(bfh_docs) + len(lbo_docs) + len(eu_docs) + len(additional_docs) + len(bmf_docs) + len(expansion_docs)}")
    print("\n✅ Professional database seeding completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed_database())
