#!/usr/bin/env python3
"""
Seed Urteile - Fügt Rechtsprechung zum Immobilienrecht zur Datenbank hinzu
============================================================================

Lädt Urteile aller Gerichtsebenen:
- BGH (5 Urteile)
- OLG (4 Urteile)
- LG (3 Urteile)
- AG (3 Urteile)

Gesamt: 15 hochwertige Urteile zum Immobilienrecht
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

from urteile_immobilien_scraper import UrteileImmobilienScraper

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
    print("⚖️  RECHTSPRECHUNG IMMOBILIENRECHT - Seeding Script")
    print("="*60 + "\n")
    
    # Initialize
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    scraper = UrteileImmobilienScraper()
    
    # Check current count
    collection_info = client.get_collection(COLLECTION_NAME)
    start_count = collection_info.points_count
    print(f"📊 Aktuell in Qdrant: {start_count} Dokumente\n")
    
    # Load all urteile
    print("⚖️  Lade Urteile...")
    all_urteile = scraper.scrape_all()
    print(f"   ✅ {len(all_urteile)} Urteile geladen\n")
    
    # Show gerichtsebene
    gerichtsebenen = {}
    for urteil in all_urteile:
        ebene = urteil.get('gerichtsebene', 'Sonstige')
        gerichtsebenen[ebene] = gerichtsebenen.get(ebene, 0) + 1
    
    print("📋 Gerichtsebenen:")
    for ebene, count in sorted(gerichtsebenen.items()):
        print(f"   - {ebene}: {count}")
    print()
    
    # Show rechtsgebiete
    rechtsgebiete = {}
    for urteil in all_urteile:
        gebiet = urteil.get('rechtsgebiet', 'Sonstige')
        rechtsgebiete[gebiet] = rechtsgebiete.get(gebiet, 0) + 1
    
    print("📋 Rechtsgebiete:")
    for gebiet, count in sorted(rechtsgebiete.items()):
        print(f"   - {gebiet}: {count}")
    print()
    
    print("="*60)
    
    # Generate embeddings and upload
    points = []
    total = len(all_urteile)
    
    for i, urteil in enumerate(all_urteile, 1):
        try:
            # Rate limiting
            if i > 1:
                time.sleep(3)  # 3 Sekunden zwischen Anfragen
            
            print(f"[{i}/{total}] Embedding: {urteil['title'][:60]}...")
            
            # Create text for embedding
            embedding_text = f"{urteil['title']}\n\n{urteil['content']}"
            embedding = get_embedding(embedding_text)
            
            # Create payload
            payload = {
                "title": urteil['title'],
                "content": urteil['content'],
                "jurisdiction": urteil.get('jurisdiction', 'DE'),
                "doc_type": urteil.get('doc_type', 'URTEIL'),
                "gericht": urteil.get('gericht', ''),
                "gerichtsebene": urteil.get('gerichtsebene', ''),
                "aktenzeichen": urteil.get('aktenzeichen', ''),
                "datum": urteil.get('datum', ''),
                "senat": urteil.get('senat', ''),
                "rechtsgebiet": urteil.get('rechtsgebiet', ''),
                "thema": urteil.get('thema', ''),
                "keywords": urteil.get('keywords', []),
                "citation": urteil.get('citation', ''),
                "indexed_at": datetime.utcnow().isoformat(),
            }
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload
            )
            points.append(point)
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            continue
    
    # Upload to Qdrant
    if points:
        print(f"\n⬆️  Uploading {len(points)} Urteile zu Qdrant...")
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("   ✅ Upload erfolgreich!")
    
    # Final count
    collection_info = client.get_collection(COLLECTION_NAME)
    end_count = collection_info.points_count
    added = end_count - start_count
    
    print("\n" + "="*60)
    print(f"✅ FERTIG!")
    print(f"📊 Vorher: {start_count} | Nachher: {end_count} | Hinzugefügt: {added}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
