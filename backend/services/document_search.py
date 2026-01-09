"""
Document Search Service - Semantic search for generated documents
"""

import logging
from typing import List, Optional
from datetime import datetime

import google.generativeai as genai
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GeneratedDocumentSearchRequest(BaseModel):
    """Request for searching generated documents."""
    query: str
    user_id: str
    max_results: int = 10


class GeneratedDocumentSearchResult(BaseModel):
    """Search result for a generated document."""
    document_id: str
    template_name: str
    client_name: Optional[str] = None
    case_number: Optional[str] = None
    created_at: datetime
    relevance_score: float
    summary: str  # AI-generated summary
    matching_excerpt: Optional[str] = None


class DocumentSearchService:
    """Service for semantic document search using Gemini AI."""
    
    def __init__(self, gemini_api_key: str):
        """Initialize the document search service."""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def generate_document_summary(self, content: str, template_name: str) -> str:
        """Generate AI summary for a document."""
        try:
            prompt = f"""Erstelle eine kurze Zusammenfassung (max. 2-3 Sätze) für folgendes juristisches Dokument:

Dokumenttyp: {template_name}

Inhalt:
{content[:2000]}  # Erste 2000 Zeichen

Zusammenfassung:"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return f"Dokument: {template_name}"
    
    async def search_documents(
        self,
        documents: List[dict],
        query: str,
        max_results: int = 10
    ) -> List[GeneratedDocumentSearchResult]:
        """
        Search documents using semantic AI search.
        
        Args:
            documents: List of document dicts with keys: id, templateName, content, clientName, etc.
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results ranked by relevance
        """
        if not documents:
            return []
        
        results = []
        
        for doc in documents:
            try:
                # Build document context
                doc_context = f"""
Dokumenttyp: {doc.get('templateName', 'Unbekannt')}
Mandant: {doc.get('clientName', 'N/A')}
Aktenzeichen: {doc.get('caseNumber', 'N/A')}
Erstellt: {doc.get('createdAt', 'N/A')}

Inhalt (Auszug):
{doc.get('content', '')[:1000]}
"""
                
                # Ask AI to rate relevance
                relevance_prompt = f"""Bewerte die Relevanz dieses Dokuments für die Suchanfrage.

Suchanfrage: "{query}"

Dokument:
{doc_context}

Antworte NUR mit einer Zahl zwischen 0.0 (nicht relevant) und 1.0 (sehr relevant).
Keine Erklärung, nur die Zahl."""

                response = self.model.generate_content(relevance_prompt)
                
                # Parse relevance score
                try:
                    relevance = float(response.text.strip())
                    relevance = max(0.0, min(1.0, relevance))  # Clamp to [0, 1]
                except ValueError:
                    relevance = 0.0
                
                # Skip if not relevant
                if relevance < 0.1:
                    continue
                
                # Generate summary
                summary = await self.generate_document_summary(
                    doc.get('content', ''),
                    doc.get('templateName', 'Dokument')
                )
                
                # Find matching excerpt (simple approach - first 200 chars)
                excerpt = None
                content = doc.get('content', '')
                if len(content) > 200:
                    excerpt = content[:200] + "..."
                else:
                    excerpt = content
                
                results.append(GeneratedDocumentSearchResult(
                    document_id=doc['id'],
                    template_name=doc.get('templateName', 'Unbekannt'),
                    client_name=doc.get('clientName'),
                    case_number=doc.get('caseNumber'),
                    created_at=doc.get('createdAt', datetime.now()),
                    relevance_score=relevance,
                    summary=summary,
                    matching_excerpt=excerpt
                ))
            
            except Exception as e:
                logger.error(f"Error processing document {doc.get('id')}: {e}")
                continue
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Limit results
        return results[:max_results]
