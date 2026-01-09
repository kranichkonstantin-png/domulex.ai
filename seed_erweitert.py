#!/usr/bin/env python3
"""
Erweitertes Gesetze-Seeding - Phase 1 & Phase 2
================================================

PHASE 1 - Mietrecht, Baurecht, Steuerrecht:
- BetrKV, HeizkostenV, WohnFlV (Mietrecht)
- GrEStG, GrStG, BewG (Steuerrecht)
- BauGB (Baurecht)

PHASE 2 - Baurecht erweitert:
- HOAI (Architektenhonorar)
- GEG (Heizungsgesetz 2024)
- MaBV (Bauträger)

Ziel: 36+ Paragraphen aus 10 Gesetzen
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai
import uuid

# Load environment
load_dotenv()

# Import CRITICAL_PARAGRAPHS directly
from ingestion.scrapers.gesetze_scraper import CRITICAL_PARAGRAPHS

# Configure Qdrant Cloud (Production)
QDRANT_URL = "https://11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"

# Configure Gemini
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"
genai.configure(api_key=GEMINI_API_KEY)

def create_embedding(text: str) -> list:
    """Create embedding using Gemini"""
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return None

def main():
    print("=" * 70)
    print("🏛️  GESETZE-SEEDING ERWEITERT - PHASE 1 & 2")
    print("=" * 70)
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Get current count
    collection_info = client.get_collection(COLLECTION_NAME)
    count_before = collection_info.points_count
    print(f"\n📊 Aktuell in Qdrant: {count_before} Dokumente\n")
    
    # Prepare all paragraphs
    all_paragraphs = []
    
    # Count paragraphs per law
    law_counts = {}
    for law_abbr, paragraphs in CRITICAL_PARAGRAPHS.items():
        law_counts[law_abbr] = len(paragraphs)
        all_paragraphs.extend(paragraphs)
    
    # Display overview with emojis
    print("=" * 70)
    print("📋 GESETZE-ÜBERSICHT")
    print("=" * 70)
    
    print("\n🏠 MIETRECHT (Phase 1):")
    for law in ["BetrKV", "HeizkostenV", "WohnFlV"]:
        if law in law_counts:
            print(f"   ✅ {law:15} {law_counts[law]:2} Paragraphen")
    
    print("\n💰 STEUERRECHT (Phase 1):")
    for law in ["GrEStG", "GrStG", "BewG"]:
        if law in law_counts:
            print(f"   ✅ {law:15} {law_counts[law]:2} Paragraphen")
    
    print("\n🏗️  BAURECHT (Phase 1 & 2):")
    for law in ["BauGB", "HOAI", "GEG", "MaBV"]:
        if law in law_counts:
            phase = "Phase 1" if law == "BauGB" else "Phase 2"
            print(f"   ✅ {law:15} {law_counts[law]:2} Paragraphen ({phase})")
    
    total_paragraphs = len(all_paragraphs)
    print("\n" + "=" * 70)
    print(f"📋 GESAMT: {total_paragraphs} Paragraphen aus {len(law_counts)} Gesetzen")
    print("=" * 70)
    
    # Create embeddings
    print(f"\n🔄 Erstelle Embeddings...\n")
    points = []
    
    for idx, para in enumerate(all_paragraphs, 1):
        # Create text for embedding
        text_for_embedding = f"{para['title']}\n\n{para['content']}"
        
        # Progress indicator
        law_display = f"{para['law_abbr']:10}"
        para_display = f"§ {para['paragraph']:3}"
        print(f"[{idx:2}/{total_paragraphs}] {law_display} {para_display}...", end=" ")
        
        # Create embedding
        embedding = create_embedding(text_for_embedding)
        
        if embedding:
            # Determine phase
            phase = "1" if para["law_abbr"] in ["BetrKV", "HeizkostenV", "WohnFlV", 
                                                  "GrEStG", "GrStG", "BewG", "BauGB"] else "2"
            
            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "title": para["title"],
                    "content": para["content"],
                    "law": para["law"],
                    "law_abbr": para["law_abbr"],
                    "paragraph": para["paragraph"],
                    "rechtsgebiet": para["rechtsgebiet"],
                    "doc_type": "Gesetz",
                    "jurisdiction": "Deutschland",
                    "phase": phase,
                    "source": "gesetze-im-internet.de (curated)",
                    "year": "2024"
                }
            )
            points.append(point)
            print("✅")
        else:
            print("❌")
    
    # Upload to Qdrant
    if points:
        print(f"\n⬆️  Uploading {len(points)} Paragraphen zu Qdrant...")
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print("   ✅ Upload erfolgreich!")
    
    # Get updated count
    collection_info = client.get_collection(COLLECTION_NAME)
    count_after = collection_info.points_count
    added = count_after - count_before
    
    print("\n" + "=" * 70)
    print("✅ SEEDING ABGESCHLOSSEN!")
    print("=" * 70)
    print(f"📊 Vorher:      {count_before:5} Dokumente")
    print(f"📊 Nachher:     {count_after:5} Dokumente")
    print(f"📊 Hinzugefügt: {added:5} Dokumente")
    print("=" * 70)
    
    # Breakdown by Rechtsgebiet
    print("\n📊 BREAKDOWN:")
    rechtsgebiete = {}
    for para in all_paragraphs:
        rg = para['rechtsgebiet']
        rechtsgebiete[rg] = rechtsgebiete.get(rg, 0) + 1
    
    for rg, count in sorted(rechtsgebiete.items()):
        print(f"   {rg:25} {count:2} Paragraphen")
    
    print("\n" + "=" * 70)
    print("🎯 NÄCHSTE SCHRITTE:")
    print("=" * 70)
    print("1. ⚖️  Rechtsprechung erweitern:")
    print("   - BGH +176 Urteile (VIII ZR Mietrecht, V ZR Kaufrecht)")
    print("   - BFH +131 Urteile (IX R Grunderwerbsteuer)")
    print("   - EuGH +90 Urteile (Kapitalverkehr, Dienstleistungsfreiheit)")
    print("\n2. 📚 Literatur komplett:")
    print("   - Palandt BGB komplett (alle §§ mit Kommentierung)")
    print("   - MüKo Mietrecht/Sachenrecht")
    print("   - Schmidt Steuerrecht")
    print("\n3. 📋 Weitere Gesetze (Phase 2):")
    print("   - UStG (Umsatzsteuergesetz)")
    print("   - ErbStG (Erbschaftsteuergesetz)")
    print("   - AO (Abgabenordnung)")
    print("=" * 70)

if __name__ == "__main__":
    main()
