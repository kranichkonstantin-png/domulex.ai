"""
RAG Engine for DOMULEX
Retrieval-Augmented Generation with strict jurisdiction filtering.
"""

import asyncio
import logging
from typing import List, Optional

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny,
)

from models.legal import LegalDocument, Jurisdiction, UserRole, QueryResponse
from rag.prompts import (
    get_system_instruction,
    detect_jurisdiction_from_query,
    get_jurisdiction_warning,
    JURISDICTION_KEYWORDS,
)

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Retrieval-Augmented Generation engine with jurisdiction-aware filtering.
    
    Architecture:
    1. Embed user query with Gemini
    2. Search Qdrant with STRICT jurisdiction filter (if available)
    3. Synthesize answer with Cultural Bridge prompts
    
    Graceful Degradation:
    - If Qdrant is not available, runs in Gemini-only mode
    - Answers are generated without document retrieval
    """
    
    def __init__(
        self,
        qdrant_client: Optional[QdrantClient],
        gemini_api_key: str,
        collection_name: str = "legal_documents",
        vector_size: int = 768,  # Gemini embedding dimension
    ):
        self.qdrant = qdrant_client
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.qdrant_available = qdrant_client is not None
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        # Use same embedding model as seed_qdrant_cloud.py (768 dimensions)
        self.embedding_model = "models/text-embedding-004"
        # Strict mode: temperature=0.0 eliminates randomness for legal accuracy
        self.generation_model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config={"temperature": 0.0}
        )
        
        # Collection will be ensured lazily on first use
        self._collection_ensured = False
    
    def _ensure_collection(self):
        """Create Qdrant collection if it doesn't exist. Called lazily."""
        if self._collection_ensured or not self.qdrant_available:
            return
        try:
            self.qdrant.get_collection(self.collection_name)
            self._collection_ensured = True
        except Exception:
            # Create collection with cosine similarity
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            self._collection_ensured = True
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding using Gemini."""
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_query",  # Optimized for search
        )
        return result["embedding"]
    
    async def index_documents(self, documents: List[LegalDocument]) -> int:
        """
        Index legal documents into Qdrant.
        
        Args:
            documents: List of LegalDocument objects
            
        Returns:
            Number of documents successfully indexed
        """
        points = []
        
        for doc in documents:
            # Generate embedding if not already present
            if not doc.embedding_vector:
                # Combine title + content for better semantic search
                text_to_embed = f"{doc.title}\n\n{doc.content_original[:2000]}"  # Limit to 2k chars
                doc.embedding_vector = await self.embed_text(text_to_embed)
            
            # Create Qdrant point
            point = PointStruct(
                id=str(doc.id),
                vector=doc.embedding_vector,
                payload={
                    "jurisdiction": doc.jurisdiction.value,
                    "sub_jurisdiction": doc.sub_jurisdiction,
                    "title": doc.title,
                    "content": doc.content_original,
                    "source_url": str(doc.source_url),
                    "publication_date": doc.publication_date.isoformat(),
                    "document_type": doc.document_type,
                    "language": doc.language,
                    "keywords": doc.keywords,
                },
            )
            points.append(point)
        
        # Batch upload
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        
        return len(points)
    
    async def search(
        self,
        query: str,
        target_jurisdiction: Jurisdiction,
        sub_jurisdiction: Optional[str] = None,
        limit: int = 5,
        source_filter: Optional[List[str]] = None,
        gerichtsebene_filter: Optional[List[str]] = None,
    ) -> List[LegalDocument]:
        """
        Search for relevant legal documents with STRICT jurisdiction filtering.
        
        This is the CRITICAL function that prevents legal hallucinations:
        - A US query will NEVER retrieve German BGB
        - A Spanish query will NEVER retrieve US Code
        
        Args:
            query: User's question
            target_jurisdiction: MUST match - no cross-contamination
            sub_jurisdiction: Optional state/region filter
            limit: Max number of results
            source_filter: Optional list of doc_types to include (e.g., ["GESETZ", "URTEIL", "LITERATUR"])
                          If None, all types are included
            gerichtsebene_filter: Optional list of court levels (e.g., ["BGH", "OLG", "LG", "AG"])
                                 Only applies when URTEIL is in source_filter
            
        Returns:
            List of relevant LegalDocument objects (empty if Qdrant unavailable)
        """
        # If Qdrant not available, return empty list
        if not self.qdrant_available:
            return []
        
        # Ensure collection exists (lazy initialization)
        self._ensure_collection()
        
        # Embed the query
        query_vector = await self.embed_text(query)
        
        # Build filter - JURISDICTION IS MANDATORY for legal accuracy
        filter_conditions = [
            FieldCondition(
                key="jurisdiction",
                match=MatchValue(value=target_jurisdiction.value),
            )
        ]
        
        # Add sub-jurisdiction filter if specified
        if sub_jurisdiction:
            filter_conditions.append(
                FieldCondition(
                    key="sub_jurisdiction",
                    match=MatchValue(value=sub_jurisdiction),
                )
            )
        
        # Add source filter if specified (for lawyer source selection)
        if source_filter:
            filter_conditions.append(
                FieldCondition(
                    key="doc_type",
                    match=MatchAny(any=source_filter),
                )
            )
        
        # Add gerichtsebene filter if specified (only for URTEIL)
        if gerichtsebene_filter and source_filter and "URTEIL" in source_filter:
            filter_conditions.append(
                FieldCondition(
                    key="gerichtsebene",
                    match=MatchAny(any=gerichtsebene_filter),
                )
            )
        
        # Search Qdrant - catch errors and return empty list for Gemini fallback
        try:
            search_results = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=Filter(must=filter_conditions),
                limit=limit,
            )
        except Exception as e:
            logger.warning(f"Qdrant search failed, using Gemini-only mode: {e}")
            return []
        
        # Convert to LegalDocument objects
        # Payload schema: doc_id, content, jurisdiction, language, source, source_url, topics, law, section, last_updated
        documents = []
        for result in search_results:
            payload = result.payload
            # Handle publication_date - check multiple possible date fields
            pub_date_raw = payload.get("last_updated") or payload.get("datum") or payload.get("date") or "2025-01-01"
            if isinstance(pub_date_raw, str) and "T" in pub_date_raw:
                pub_date = pub_date_raw.split("T")[0]  # Extract date part only
            else:
                pub_date = pub_date_raw if pub_date_raw else "2025-01-01"
            
            # Use title field first, then fallback to other fields
            title = payload.get("title") or payload.get("source") or payload.get("doc_id") or "Unbekannt"
            
            doc = LegalDocument(
                id=result.id,
                jurisdiction=Jurisdiction(payload.get("jurisdiction", "DE")),
                sub_jurisdiction=payload.get("sub_jurisdiction"),
                title=title,
                content_original=payload.get("content", ""),
                source_url=payload.get("source_url", ""),
                publication_date=pub_date,
                document_type=payload.get("law") or payload.get("type") or payload.get("doc_type") or "Gesetz",
                language=payload.get("language", "de"),
                keywords=payload.get("topics") or payload.get("keywords") or [],
                embedding_vector=None,  # Don't return vectors in response
            )
            documents.append(doc)
        
        return documents
        gerichtsebene_filter: Optional[List[str]] = None,
    
    async def query(
        self,
        user_query: str,
        target_jurisdiction: Jurisdiction,
        user_role: UserRole,
        user_language: str = "de",
        sub_jurisdiction: Optional[str] = None,
        source_filter: Optional[List[str]] = None,
        gerichtsebene_filter: Optional[List[str]] = None,
        use_public_sources: Optional[bool] = False,
        uploaded_documents: Optional[List[dict]] = None,
    ) -> QueryResponse:
        """
        Main RAG query function with Cultural Bridge.
        
        Workflow:
        1. Detect if query contains foreign jurisdiction terms → warn
        2. Search Qdrant with strict filtering
        3. Generate answer using Gemini with culturally-aware prompts
        
        Args:
            user_query: User's legal question
            target_jurisdiction: Which country's law to query
            user_role: INVESTOR, LANDLORD, etc.
            user_language: de, es, en
            sub_jurisdiction: Optional state/region
            source_filter: Optional list of doc_types (e.g., ["GESETZ", "URTEIL", "LITERATUR"])
            gerichtsebene_filter: Optional list of court levels (e.g., ["BGH", "OLG"])
            use_public_sources: 🔑 Use public sources for enhanced answers
            
        Returns:
            QueryResponse with answer, sources, and warnings
        """
        # Step 1: Detect jurisdiction mismatch
        detected_jurisdictions = detect_jurisdiction_from_query(user_query)
        foreign_terms = []
        
        for jurisdiction, count in detected_jurisdictions.items():
            if jurisdiction != target_jurisdiction and count > 0:
                # Found terms from a different jurisdiction
                foreign_terms.extend([
                    kw for kw in JURISDICTION_KEYWORDS[jurisdiction]
                    if kw.lower() in user_query.lower()
                ])
        
        jurisdiction_warning = None
        if foreign_terms:
            jurisdiction_warning = get_jurisdiction_warning(
                target_jurisdiction,
                foreign_terms[:3],  # Limit to first 3 matches
            )
        
        # Step 2: Retrieve relevant documents (empty if Qdrant unavailable)
        # Lawyers get more sources (15) than regular users (5)
        search_limit = 15 if user_role == UserRole.LAWYER else 5
        
        relevant_docs = await self.search(
            query=user_query,
            target_jurisdiction=target_jurisdiction,
            sub_jurisdiction=sub_jurisdiction,
            gerichtsebene_filter=gerichtsebene_filter,
            limit=search_limit,
            source_filter=source_filter,
        )
        
        # Sort by recency - newest documents first (for most current legal state)
        relevant_docs.sort(key=lambda d: d.publication_date, reverse=True)
        
        # Step 3: Handle Gemini-only mode (no Qdrant)
        # Build user document context if available
        user_doc_context = ""
        if uploaded_documents:
            user_doc_parts = []
            for doc in uploaded_documents:
                doc_text = doc.get('text', '')
                if doc_text:
                    user_doc_parts.append(f"📎 HOCHGELADENES DOKUMENT:\n{doc_text[:10000]}")  # Max 10k chars per doc
            if user_doc_parts:
                user_doc_context = "\n\n---\n\n".join(user_doc_parts) + "\n\n---\n\n"
        
        if not relevant_docs:
            # Generate answer directly with Gemini (no document grounding)
            gemini_only_prompt = f"""You are a legal expert assistant for {target_jurisdiction.value} real estate law.
            
**User Role:** {user_role.value}
**Target Jurisdiction:** {target_jurisdiction.value}
**Sub-Jurisdiction:** {sub_jurisdiction or "Not specified"}
**Language:** {user_language}

{user_doc_context}**User Question:**
{user_query}

**Instructions:**
1. Provide specific, actionable legal information with concrete paragraphs and court decisions
2. Give DIRECT answers - no hedging, no "general information", no "consult a professional"
3. FORBIDDEN phrases (NEVER use these):
   - "keine Rechtsberatung" / "not legal advice"
   - "konsultieren Sie einen Anwalt/Steuerberater" / "consult a lawyer/tax advisor"
   - "allgemeine Informationen" / "general information"  
   - "fundierte Grundlage" / "solid foundation"
   - "individuelle Beratung empfohlen" / "individual advice recommended"
4. If a document was uploaded, analyze it thoroughly and reference specific clauses/paragraphs
5. Respond confidently in {user_language} - you ARE the expert
"""
            try:
                response = await asyncio.to_thread(
                    self.generation_model.generate_content,
                    gemini_only_prompt,
                    generation_config={
                        "temperature": 0.1,  # Slightly higher for general knowledge
                        "max_output_tokens": 8192,
                    },
                )
                answer = response.text
                
                # No disclaimer needed - the answer stands on its own
                
            except Exception as e:
                answer = f"Error generating answer: {str(e)}"
            
            return QueryResponse(
                answer=answer,
                sources=[],
                jurisdiction_warning=jurisdiction_warning,
            )
        
        # Step 3: Build context from retrieved documents + user documents
        context_parts = []
        
        # Add user-uploaded documents first (if any)
        if user_doc_context:
            context_parts.append(user_doc_context)
        
        # Add database sources
        for doc in relevant_docs:
            context_parts.append(
                f"**Source:** {doc.title}\n"
                f"**Date:** {doc.publication_date}\n"
                f"**URL:** {doc.source_url}\n\n"
                f"{doc.content_original[:1500]}..."  # Limit context per doc
            )
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Step 4: Get strict legal analyst prompt (anti-hallucination)
        from rag.prompts import get_strict_legal_prompt
        
        strict_prompt = get_strict_legal_prompt(
            context_chunks=context,
            query=user_query,
            jurisdiction=target_jurisdiction,
            role=user_role,
            user_language=user_language,
            use_public_sources=use_public_sources,  # 🔑 Öffentliche Quellen
        )
        
        # Step 5: Generate answer with strict grounding (temperature=0.0)
        try:
            response = await asyncio.to_thread(
                self.generation_model.generate_content,
                strict_prompt,
                generation_config={
                    "temperature": 0.0,  # STRICT: No randomness
                    "top_p": 1.0,
                    "max_output_tokens": 8192,
                },
            )
            
            answer = response.text
            
            # 🔑 Halluzinations-Warnung bei allgemeinem KI-Wissen (ohne Datenbank)
            if use_public_sources:
                if user_language == "de":
                    answer += "\n\n⚠️ **WARNUNG - KEINE DATENBANKNUTZUNG:** Diese Antwort basiert auf **allgemeinem KI-Chatbot-Wissen** ohne Zugriff auf die verlässliche Datenbank. Die KI nutzt nur ihr Trainingswissen mit **erhöhtem Risiko für Halluzinationen und Fehler**. Prüfen Sie ALLE Paragraphen, Urteile und rechtlichen Angaben eigenständig nach!"
                elif user_language == "en":
                    answer += "\n\n⚠️ **WARNING - NO DATABASE ACCESS:** This answer is based on general AI chatbot knowledge without access to the reliable database. Higher risk of hallucinations and errors. Verify all legal details independently!"
                elif user_language == "es":
                    answer += "\n\n⚠️ **ADVERTENCIA - SIN ACCESO A BASE DE DATOS:** Esta respuesta se basa en conocimiento general del chatbot de IA sin acceso a la base de datos confiable. Mayor riesgo de alucinaciones y errores. ¡Verifique todos los detalles legales de forma independiente!"
            
            
            # Step 6: Self-Critique Verification Loop (anti-hallucination guard)
            critique_prompt = f"""You are a fact-checker. Review the following answer against the provided context.

**CONTEXT:**
{context}

**ANSWER TO VERIFY:**
{answer}

**TASK:**
Does the answer contain ANY claims NOT directly supported by the context?
If YES, output: "HALLUCINATION DETECTED: [specific claim]"
If NO, output: "VERIFIED"
"""
            
            critique_response = await asyncio.to_thread(
                self.generation_model.generate_content,
                critique_prompt,
                generation_config={"temperature": 0.0},
            )
            
            critique_result = critique_response.text.strip()
            
            # If hallucination detected, append warning
            if "HALLUCINATION DETECTED" in critique_result.upper():
                answer += f"\n\n⚠️ **SYSTEM WARNING:** {critique_result}"
            
        except Exception as e:
            answer = f"Error generating answer: {str(e)}"
        
        # Step 7: Return response with sources
        return QueryResponse(
            answer=answer,
            sources=relevant_docs,
            jurisdiction_warning=jurisdiction_warning,
        )
