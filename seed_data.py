"""
DOMULEX Data Seeding Script
Loads sample legal documents from /data/raw into Qdrant for testing.

This script demonstrates the CRITICAL jurisdiction filtering:
- German BGB → jurisdiction=DE
- US Florida Statutes → jurisdiction=US
- Spanish LAU → jurisdiction=ES
"""

import os
import sys
import uuid
from pathlib import Path
from typing import List, Dict, Tuple

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DocumentChunker:
    """Split documents into semantic chunks respecting sentence boundaries."""
    
    @staticmethod
    def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Split text into chunks of approximately max_chunk_size characters.
        Respects sentence boundaries (splits on '. ', '! ', '? ').
        
        Args:
            text: Input text to chunk
            max_chunk_size: Target chunk size in characters
            
        Returns:
            List of text chunks
        """
        # Split into sentences
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            if char in '.!?' and len(current_sentence) > 10:
                sentences.append(current_sentence.strip())
                current_sentence = ""
        
        if current_sentence:
            sentences.append(current_sentence.strip())
        
        # Group sentences into chunks
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks


class QdrantSeeder:
    """Seed Qdrant with sample legal documents."""
    
    def __init__(
        self,
        qdrant_url: str,
        collection_name: str,
        gemini_api_key: str,
    ):
        self.qdrant = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.embedding_model = "models/embedding-001"
        
        # Ensure collection exists
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            self.qdrant.get_collection(self.collection_name)
            print(f"✓ Collection '{self.collection_name}' exists")
        except Exception:
            print(f"⚠ Collection '{self.collection_name}' not found. Creating...")
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=768,  # Gemini embedding dimension
                    distance=Distance.COSINE,
                ),
            )
            print(f"✓ Collection '{self.collection_name}' created")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Gemini."""
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document",
        )
        return result["embedding"]
    
    def load_and_seed_file(
        self,
        file_path: Path,
        jurisdiction: str,
        language: str,
    ) -> int:
        """
        Load a file, chunk it, generate embeddings, and upload to Qdrant.
        
        Args:
            file_path: Path to the text file
            jurisdiction: DE, ES, or US
            language: de, es, or en
            
        Returns:
            Number of chunks uploaded
        """
        print(f"\n📄 Processing: {file_path.name}")
        print(f"   Jurisdiction: {jurisdiction}")
        print(f"   Language: {language}")
        
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"   File size: {len(content)} characters")
        
        # Chunk text
        chunker = DocumentChunker()
        chunks = chunker.chunk_text(content, max_chunk_size=1000)
        print(f"   Chunks created: {len(chunks)}")
        
        # Create points for Qdrant
        points = []
        
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = self.generate_embedding(chunk)
            
            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "jurisdiction": jurisdiction,
                    "language": language,
                    "source_file": file_path.name,
                    "chunk_index": i,
                    "content": chunk,
                },
            )
            points.append(point)
            
            print(f"   ✓ Chunk {i+1}/{len(chunks)} embedded")
        
        # Upload to Qdrant
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        
        print(f"   ✅ Uploaded {len(points)} chunks to Qdrant")
        return len(points)
    
    def seed_all(self, data_dir: Path) -> Dict[str, int]:
        """
        Seed all sample files from data directory.
        
        Expected files:
        - sample_de.txt (German BGB)
        - sample_us.txt (US Florida Statutes)
        - sample_es.txt (Spanish LAU)
        
        Returns:
            Dict of {filename: chunk_count}
        """
        # Define files and their metadata
        files_config = [
            ("sample_de.txt", "DE", "de"),
            ("sample_us.txt", "US", "en"),
            ("sample_es.txt", "ES", "es"),
        ]
        
        results = {}
        total_chunks = 0
        
        for filename, jurisdiction, language in files_config:
            file_path = data_dir / filename
            
            if not file_path.exists():
                print(f"⚠ Warning: {filename} not found in {data_dir}")
                continue
            
            count = self.load_and_seed_file(
                file_path=file_path,
                jurisdiction=jurisdiction,
                language=language,
            )
            results[filename] = count
            total_chunks += count
        
        return results, total_chunks


def main():
    """Main seeding function."""
    print("=" * 60)
    print("DOMULEX - Data Seeding Script")
    print("=" * 60)
    
    # Load configuration from environment
    gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "domulex_legal_docs")
    
    if not gemini_api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment")
        print("   Set it in .env file or export it:")
        print("   export GOOGLE_API_KEY='your_key_here'")
        sys.exit(1)
    
    print(f"\n⚙️  Configuration:")
    print(f"   Qdrant URL: {qdrant_url}")
    print(f"   Collection: {collection_name}")
    print(f"   Gemini API: {'✓ Configured' if gemini_api_key else '✗ Missing'}")
    
    # Define data directory
    data_dir = Path(__file__).parent / "data" / "raw"
    
    if not data_dir.exists():
        print(f"\n⚠ Warning: Data directory not found: {data_dir}")
        print(f"   Creating directory...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Directory created")
        print(f"\n❌ No sample files found. Please add:")
        print(f"   - {data_dir}/sample_de.txt (German BGB)")
        print(f"   - {data_dir}/sample_us.txt (US Florida Statutes)")
        print(f"   - {data_dir}/sample_es.txt (Spanish LAU)")
        sys.exit(1)
    
    print(f"\n📂 Data directory: {data_dir}")
    
    # Initialize seeder
    seeder = QdrantSeeder(
        qdrant_url=qdrant_url,
        collection_name=collection_name,
        gemini_api_key=gemini_api_key,
    )
    
    # Seed all files
    print("\n" + "=" * 60)
    print("Starting Data Ingestion")
    print("=" * 60)
    
    results, total_chunks = seeder.seed_all(data_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("Seeding Complete!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    for filename, count in results.items():
        print(f"   {filename}: {count} chunks")
    print(f"\n   Total: {total_chunks} chunks uploaded")
    
    # Verify collection stats
    collection_info = seeder.qdrant.get_collection(collection_name)
    print(f"\n✅ Qdrant Collection Stats:")
    print(f"   Total points: {collection_info.points_count}")
    print(f"   Vector size: {collection_info.config.params.vectors.size}")
    
    print("\n" + "=" * 60)
    print("🎉 Ready to test multi-jurisdiction queries!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the backend: cd backend && uvicorn main:app --reload")
    print("2. Test query: curl -X POST http://localhost:8000/query \\")
    print('   -H "Content-Type: application/json" \\')
    print("   -d '{\"query\": \"Mietvertrag\", \"target_jurisdiction\": \"DE\", \"user_role\": \"TENANT\", \"user_language\": \"de\"}'")


if __name__ == "__main__":
    main()
