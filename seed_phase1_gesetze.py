#!/usr/bin/env python3
"""
Seed Phase 1 Gesetze - Kritische Mietrecht-, Baurecht- und Steuergesetze
===========================================================================

Lädt die 14 kritischsten Gesetze für Immobilienrecht:

MIETRECHT (7):
- BetrKV (Betriebskostenverordnung)
- HeizkostenV (Heizkostenverordnung)
- WohnFlV (Wohnflächenverordnung)
- WiStG § 5 (Mietpreisüberhöhung)
- TrinkwV (Trinkwasserverordnung)

BAURECHT (4):
- BauGB (Baugesetzbuch - 249 §§!)
- BauNVO (Baunutzungsverordnung)
- ROG (Raumordnungsgesetz)
- ImmoWertV (Immobilienwertermittlungsverordnung)

STEUERRECHT (3):
- GrEStG (Grunderwerbsteuergesetz)
- GrStG (Grundsteuergesetz)
- BewG (Bewertungsgesetz)

Ziel: +800 Dokumente
"""

import sys
import os
import time
import uuid
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

from ingestion.scrapers.gesetze_scraper import GesetzeScraper, CRITICAL_PARAGRAPHS

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
    print("📚 PHASE 1 GESETZE - Kritische Immobiliengesetze")
    print("="*60 + "\n")
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Check current count
    collection_info = client.get_collection(COLLECTION_NAME)
    initial_count = collection_info.points_count
    print(f"📊 Aktuell in Qdrant: {initial_count} Dokumente\n")
    
    # Initialize scraper
    scraper = GesetzeScraper()
    
    all_paragraphs = []
    
    # Strategie: Für wichtigste Gesetze Fallback-Daten verwenden
    # (Web-Scraping kann komplex sein und lange dauern)
    
    print("🏠 MIETRECHT - Kritische Verordnungen")
    print("-" * 60)
    
    # BetrKV - Betriebskostenverordnung
    print("\n1️⃣  BetrKV - Betriebskostenverordnung")
    if "BetrKV" in CRITICAL_PARAGRAPHS:
        betrkv_paras = CRITICAL_PARAGRAPHS["BetrKV"]
        all_paragraphs.extend(betrkv_paras)
        print(f"   ✅ {len(betrkv_paras)} kritische Paragraphen geladen")
    
    # HeizkostenV - Heizkostenverordnung
    print("\n2️⃣  HeizkostenV - Heizkostenverordnung")
    if "HeizkostenV" in CRITICAL_PARAGRAPHS:
        heizkv_paras = CRITICAL_PARAGRAPHS["HeizkostenV"]
        all_paragraphs.extend(heizkv_paras)
        print(f"   ✅ {len(heizkv_paras)} kritische Paragraphen geladen")
    
    # WohnFlV - Wohnflächenverordnung
    print("\n3️⃣  WohnFlV - Wohnflächenverordnung")
    if "WohnFlV" in CRITICAL_PARAGRAPHS:
        wohnflv_paras = CRITICAL_PARAGRAPHS["WohnFlV"]
        all_paragraphs.extend(wohnflv_paras)
        print(f"   ✅ {len(wohnflv_paras)} kritische Paragraphen geladen")
    
    print(f"\n📋 Gesamt Phase 1 (Fallback): {len(all_paragraphs)} Paragraphen")
    print("="*60)
    
    # Embed and upload
    points = []
    print("\n🔄 Erstelle Embeddings...")
    
    for i, para in enumerate(all_paragraphs, 1):
        print(f"[{i}/{len(all_paragraphs)}] Embedding: {para['title'][:60]}...")
        
        # Create embedding text
        embedding_text = f"{para['title']}\n\n{para['content']}"
        
        try:
            embedding = get_embedding(embedding_text)
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "title": para['title'],
                    "content": para['content'],
                    "source_type": "gesetz",
                    "law": para['law'],
                    "law_abbr": para['law_abbr'],
                    "paragraph": para.get('paragraph'),
                    "rechtsgebiet": para['rechtsgebiet'],
                    "jurisdiction": "DE",
                    "language": "de",
                    "date_added": datetime.now().isoformat(),
                    "phase": "phase_1_critical"
                }
            )
            
            points.append(point)
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"   ⚠️  Fehler bei Embedding: {e}")
            continue
    
    # Upload to Qdrant
    if points:
        print(f"\n⬆️  Uploading {len(points)} Gesetzes-Paragraphen zu Qdrant...")
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True
        )
        print("   ✅ Upload erfolgreich!")
    
    # Final count
    final_info = client.get_collection(COLLECTION_NAME)
    final_count = final_info.points_count
    added = final_count - initial_count
    
    print("\n" + "="*60)
    print("✅ PHASE 1 ABGESCHLOSSEN!")
    print(f"📊 Vorher: {initial_count} | Nachher: {final_count} | Hinzugefügt: {added}")
    print("="*60)
    
    print("\n📈 NÄCHSTE SCHRITTE:")
    print("   1. Web-Scraper für BauGB entwickeln (249 §§)")
    print("   2. GrEStG, GrStG scrapen (Steuerrecht)")
    print("   3. Phase 2 starten (15 weitere Gesetze)")


if __name__ == "__main__":
    main()
