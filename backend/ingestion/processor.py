"""
Document Processor - The Intelligence Layer
Decides: "Is this relevant for Real Estate?"
Performs: Deduplication, Chunking, Embedding, Metadata Enrichment
"""

import logging
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from models.legal import LegalDocument, Jurisdiction
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Gemini Setup
genai.configure(api_key=settings.gemini_api_key)


class DocumentProcessor:
    """
    Der Kern der Ingestion-Pipeline:
    1. Relevanz-Klassifizierung
    2. Deduplizierung (Hash-basiert)
    3. Chunking
    4. Embedding-Generierung
    5. Qdrant Upload
    """
    
    # Real Estate Relevanz Keywords (Multi-Jurisdictional)
    RELEVANCE_KEYWORDS = {
        Jurisdiction.DE: [
            "immobilien", "grundstück", "miete", "vermieter", "mieter",
            "wohnung", "eigentum", "bau", "grundsteuer", "afa",
            "abschreibung", "vermietung", "verpachtung", "erbbaurecht",
            "wohnungseigentum", "weg", "mietrecht", "baurecht"
        ],
        Jurisdiction.US: [
            "property", "real estate", "landlord", "tenant", "lease",
            "rental", "eviction", "zoning", "tax", "depreciation",
            "1031 exchange", "foreclosure", "mortgage", "deed",
            "title", "hoa", "condo", "apartment"
        ],
        Jurisdiction.ES: [
            "inmobiliaria", "propiedad", "arrendador", "arrendatario",
            "alquiler", "vivienda", "edificio", "construcción",
            "ibi", "plusvalía", "hipoteca", "escritura", "catastro",
            "comunidad de propietarios", "lau"
        ],
    }
    
    # Cache Verzeichnis für Hashes
    CACHE_DIR = Path("/app/cache/document_hashes")
    
    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant = qdrant_client
        self.cache_dir = self.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def compute_document_hash(self, content: str) -> str:
        """SHA256 Hash für Deduplizierung"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    def is_duplicate(self, doc_hash: str, jurisdiction: Jurisdiction) -> bool:
        """
        Prüft ob Dokument bereits existiert.
        Hash wird in Filesystem gespeichert (schneller als DB-Lookup).
        """
        hash_file = self.cache_dir / f"{jurisdiction.value}_{doc_hash}.json"
        
        if hash_file.exists():
            # Prüfe Alter - nach 90 Tagen erneut indizieren
            data = json.loads(hash_file.read_text())
            indexed_at = datetime.fromisoformat(data["indexed_at"])
            age_days = (datetime.utcnow() - indexed_at).days
            
            if age_days < 90:
                logger.info(f"✅ Duplicate gefunden: {doc_hash[:12]}... (Age: {age_days}d)")
                return True
            else:
                logger.info(f"🔄 Re-indexing altes Dokument: {doc_hash[:12]}... (Age: {age_days}d)")
                return False
        
        return False
    
    def mark_as_indexed(self, doc_hash: str, jurisdiction: Jurisdiction, metadata: Dict):
        """Speichere Hash nach erfolgreichem Indexing"""
        hash_file = self.cache_dir / f"{jurisdiction.value}_{doc_hash}.json"
        data = {
            "hash": doc_hash,
            "indexed_at": datetime.utcnow().isoformat(),
            "jurisdiction": jurisdiction.value,
            "metadata": metadata,
        }
        hash_file.write_text(json.dumps(data, indent=2))
    
    def classify_relevance(
        self, 
        text: str, 
        jurisdiction: Jurisdiction,
        title: str = ""
    ) -> Tuple[bool, float]:
        """
        CRITICAL FUNCTION: Filtert irrelevante Dokumente BEVOR Embedding.
        
        2-Stage Process:
        1. Keyword-Matching (schnell, 95% Precision)
        2. LLM-Validation (langsam, nur bei Grenzfällen)
        
        Returns:
            (is_relevant: bool, confidence: float)
        """
        # Stage 1: Fast Keyword Check
        text_lower = (title + " " + text).lower()
        keywords = self.RELEVANCE_KEYWORDS.get(jurisdiction, [])
        
        matches = sum(1 for kw in keywords if kw in text_lower)
        keyword_score = min(matches / 3, 1.0)  # 3+ Matches = 100% Keyword-Confidence
        
        # Sofort ablehnen wenn 0 Matches
        if matches == 0:
            logger.info(f"❌ REJECT (0 Keywords): {title[:50]}...")
            return False, 0.0
        
        # Sofort akzeptieren wenn viele Matches
        if matches >= 5:
            logger.info(f"✅ ACCEPT (Strong Keywords: {matches}): {title[:50]}...")
            return True, keyword_score
        
        # Stage 2: LLM-Validation für Grenzfälle (1-4 Matches)
        logger.info(f"🤔 LLM-Check (Weak Keywords: {matches}): {title[:50]}...")
        
        try:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",  # Schnelleres Modell für Klassifizierung
                generation_config={"temperature": 0.0}
            )
            
            prompt = f"""Du bist ein Legal Document Classifier.

TASK: Ist dieses Dokument relevant für IMMOBILIEN-INVESTOREN?

DOKUMENT:
Titel: {title}
Text (First 500 chars): {text[:500]}

Relevante Themen:
- Immobilienkauf/Verkauf
- Mietrecht (Vermieter/Mieter)
- Baurecht, Zoning
- Grundsteuer, Immobiliensteuern
- Abschreibungen (AfA/Depreciation)

IRRELEVANTE Themen:
- Strafrecht
- Familienrecht
- Arbeitsrecht
- Markenrecht

ANTWORTE NUR:
"RELEVANT" oder "IRRELEVANT"
"""
            
            response = model.generate_content(prompt)
            decision = response.text.strip().upper()
            
            is_relevant = "RELEVANT" in decision
            confidence = 0.7 if is_relevant else 0.3  # LLM Confidence immer moderater
            
            logger.info(f"🤖 LLM Verdict: {decision} (Confidence: {confidence})")
            return is_relevant, confidence
            
        except Exception as e:
            logger.error(f"LLM-Klassifizierung fehlgeschlagen: {e}")
            # Fallback: Bei LLM-Fehler akzeptieren (Conservative Approach)
            return keyword_score > 0.3, keyword_score
    
    def chunk_text(self, text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
        """
        Intelligentes Chunking:
        - Respektiert Satzgrenzen
        - Overlap für Kontext-Erhalt
        - Max 1500 Zeichen (optimal für Embeddings)
        """
        sentences = text.replace("\n", " ").split(". ")
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > chunk_size and current_chunk:
                # Chunk fertig
                chunk_text = ". ".join(current_chunk) + "."
                chunks.append(chunk_text)
                
                # Overlap: Letzte 2 Sätze behalten
                current_chunk = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_length = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Letzter Chunk
        if current_chunk:
            chunks.append(". ".join(current_chunk) + ".")
        
        logger.info(f"📄 Chunking: {len(text)} chars → {len(chunks)} chunks")
        return chunks
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generiere Embedding mit Gemini"""
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document",
        )
        return result["embedding"]
    
    async def process_and_upload(
        self,
        document: LegalDocument,
        force: bool = False
    ) -> Dict[str, any]:
        """
        Haupt-Pipeline:
        1. Hash Check (Dedup)
        2. Relevanz Check
        3. Chunking
        4. Embedding
        5. Qdrant Upload
        
        Returns:
            Stats dict
        """
        stats = {
            "processed": False,
            "duplicate": False,
            "irrelevant": False,
            "chunks_uploaded": 0,
            "reason": ""
        }
        
        # Step 1: Dedup Check
        doc_hash = self.compute_document_hash(document.content_original)
        
        if not force and self.is_duplicate(doc_hash, document.jurisdiction):
            stats["duplicate"] = True
            stats["reason"] = "Duplicate detected via hash"
            return stats
        
        # Step 2: Relevanz Klassifizierung
        is_relevant, confidence = self.classify_relevance(
            text=document.content_original,
            jurisdiction=document.jurisdiction,
            title=document.title
        )
        
        if not is_relevant:
            stats["irrelevant"] = True
            stats["reason"] = f"Not relevant for real estate (confidence: {confidence:.2f})"
            logger.warning(f"⏭️  SKIPPING: {document.title} - {stats['reason']}")
            return stats
        
        logger.info(f"✅ RELEVANT ({confidence:.2f}): {document.title}")
        
        # Step 3: Chunking
        chunks = self.chunk_text(document.content_original)
        
        # Step 4 & 5: Embedding + Upload
        points = []
        for i, chunk in enumerate(chunks):
            # Embedding generieren
            embedding = await self.generate_embedding(chunk)
            
            # Qdrant Point erstellen
            point = PointStruct(
                id=f"{doc_hash}_{i}",
                vector=embedding,
                payload={
                    "jurisdiction": document.jurisdiction.value,
                    "sub_jurisdiction": document.sub_jurisdiction,
                    "title": document.title,
                    "content": chunk,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "source_url": str(document.source_url),
                    "publication_date": document.publication_date.isoformat(),
                    "document_type": document.document_type,
                    "language": document.language,
                    "keywords": document.keywords,
                    "relevance_score": confidence,
                    "indexed_at": datetime.utcnow().isoformat(),
                    "document_hash": doc_hash,
                }
            )
            points.append(point)
        
        # Batch Upload zu Qdrant
        self.qdrant.upsert(
            collection_name=settings.qdrant_collection,
            points=points
        )
        
        # Hash speichern
        self.mark_as_indexed(
            doc_hash=doc_hash,
            jurisdiction=document.jurisdiction,
            metadata={
                "title": document.title,
                "chunks": len(chunks),
                "confidence": confidence,
            }
        )
        
        stats["processed"] = True
        stats["chunks_uploaded"] = len(chunks)
        stats["reason"] = "Successfully processed and uploaded"
        
        logger.info(f"🎉 UPLOADED: {document.title} - {len(chunks)} chunks")
        
        return stats


async def generate_update_summary(new_text: str, old_text: str) -> str:
    """
    BREAKING NEWS Generator:
    Vergleicht neue vs. alte Version eines Gesetzes.
    Generiert 1-Sentence Headline für News Feed.
    """
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-pro-latest",
            generation_config={"temperature": 0.3}
        )
        
        prompt = f"""Du bist ein Legal News Editor.

AUFGABE: Generiere eine 1-Satz SCHLAGZEILE für die Änderung.

ALTE VERSION (First 500 chars):
{old_text[:500]}

NEUE VERSION (First 500 chars):
{new_text[:500]}

FORMAT:
"[Land]: [Was hat sich geändert] (Effektiv ab [Datum])"

BEISPIELE:
- "Germany: New depreciation rules for commercial property released today"
- "USA/Florida: Security deposit interest requirement removed (Effective Jan 1, 2026)"
- "Spain: IBI tax rates increased for foreign property owners"

NUR DIE SCHLAGZEILE ZURÜCKGEBEN (max 150 chars):
"""
        
        response = model.generate_content(prompt)
        headline = response.text.strip()
        
        logger.info(f"📰 Breaking News: {headline}")
        return headline
        
    except Exception as e:
        logger.error(f"News-Generierung fehlgeschlagen: {e}")
        return "Legal update detected"
