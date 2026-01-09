"""
CRM Service for Lawyer Practice Management
Handles clients, mandates, documents with AI integration
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import google.generativeai as genai
from firebase_admin import firestore
import uuid

from models.crm import (
    Client, CreateClientRequest, UpdateClientRequest,
    Mandate, CreateMandateRequest, UpdateMandateRequest,
    Document, UploadDocumentRequest, SearchDocumentsRequest, DocumentSearchResult,
    AddDeadlineRequest, Deadline,
    GenerateInsightsRequest, MandateInsights,
    ChatWithDocumentsRequest, ChatWithDocumentsResponse,
    ClientStatus, MandateStatus, DocumentCategory
)

logger = logging.getLogger(__name__)


class CRMService:
    """Service for CRM and document management with AI."""
    
    def __init__(self, gemini_api_key: str):
        """Initialize CRM service with AI."""
        self.db = firestore.client()
        genai.configure(api_key=gemini_api_key)
        self.ai_model = genai.GenerativeModel('gemini-1.5-pro')
        self.ai_flash = genai.GenerativeModel('gemini-1.5-flash')
    
    # === CLIENT MANAGEMENT ===
    
    async def create_client(
        self, 
        lawyer_id: str, 
        request: CreateClientRequest
    ) -> Client:
        """Create a new client with AI-generated summary."""
        
        # Generate client ID
        client_id = str(uuid.uuid4())
        
        # Create client object
        client = Client(
            client_id=client_id,
            lawyer_id=lawyer_id,
            **request.dict()
        )
        
        # Generate AI summary if we have enough info
        if request.notes:
            try:
                summary_prompt = f"""
Erstelle eine professionelle Zusammenfassung für diesen Mandanten:

Name: {request.first_name} {request.last_name}
Firma: {request.company_name or 'Privatperson'}
Notizen: {request.notes}

Gib eine prägnante 2-3 Satz Zusammenfassung, die für einen Anwalt relevant ist.
"""
                response = self.ai_flash.generate_content(summary_prompt)
                client.ai_summary = response.text.strip()
            except Exception as e:
                logger.warning(f"Failed to generate AI summary: {e}")
        
        # Save to Firestore
        self.db.collection('clients').document(client_id).set(client.dict())
        
        logger.info(f"Created client {client_id} for lawyer {lawyer_id}")
        return client
    
    async def get_client(self, lawyer_id: str, client_id: str) -> Optional[Client]:
        """Get a client by ID."""
        doc = self.db.collection('clients').document(client_id).get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        
        # Security: verify lawyer owns this client
        if data.get('lawyer_id') != lawyer_id:
            return None
        
        return Client(**data)
    
    async def list_clients(
        self, 
        lawyer_id: str,
        status: Optional[ClientStatus] = None,
        limit: int = 100
    ) -> List[Client]:
        """List all clients for a lawyer."""
        query = self.db.collection('clients').where('lawyer_id', '==', lawyer_id)
        
        if status:
            query = query.where('status', '==', status.value)
        
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        
        docs = query.stream()
        
        clients = []
        for doc in docs:
            try:
                clients.append(Client(**doc.to_dict()))
            except Exception as e:
                logger.warning(f"Failed to parse client {doc.id}: {e}")
        
        return clients
    
    async def update_client(
        self,
        lawyer_id: str,
        client_id: str,
        request: UpdateClientRequest
    ) -> Optional[Client]:
        """Update client information."""
        
        # Verify ownership
        client = await self.get_client(lawyer_id, client_id)
        if not client:
            return None
        
        # Update fields
        update_data = {k: v for k, v in request.dict().items() if v is not None}
        update_data['updated_at'] = datetime.now()
        
        self.db.collection('clients').document(client_id).update(update_data)
        
        # Get updated client
        return await self.get_client(lawyer_id, client_id)
    
    async def delete_client(self, lawyer_id: str, client_id: str) -> bool:
        """Delete a client (archive)."""
        
        # Verify ownership
        client = await self.get_client(lawyer_id, client_id)
        if not client:
            return False
        
        # Archive instead of delete
        self.db.collection('clients').document(client_id).update({
            'status': ClientStatus.ARCHIVED.value,
            'updated_at': datetime.now()
        })
        
        return True
    
    # === MANDATE MANAGEMENT ===
    
    async def create_mandate(
        self,
        lawyer_id: str,
        request: CreateMandateRequest
    ) -> Mandate:
        """Create a new mandate/case."""
        
        # Verify client exists and belongs to lawyer
        client = await self.get_client(lawyer_id, request.client_id)
        if not client:
            raise ValueError("Client not found or not owned by lawyer")
        
        # Generate mandate ID
        mandate_id = str(uuid.uuid4())
        
        # Create mandate
        mandate = Mandate(
            mandate_id=mandate_id,
            lawyer_id=lawyer_id,
            **request.dict()
        )
        
        # Save to Firestore
        self.db.collection('mandates').document(mandate_id).set(mandate.dict())
        
        logger.info(f"Created mandate {mandate_id} for client {request.client_id}")
        return mandate
    
    async def get_mandate(self, lawyer_id: str, mandate_id: str) -> Optional[Mandate]:
        """Get a mandate by ID."""
        doc = self.db.collection('mandates').document(mandate_id).get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        
        # Security: verify lawyer owns this mandate
        if data.get('lawyer_id') != lawyer_id:
            return None
        
        return Mandate(**data)
    
    async def list_mandates(
        self,
        lawyer_id: str,
        client_id: Optional[str] = None,
        status: Optional[MandateStatus] = None,
        limit: int = 100
    ) -> List[Mandate]:
        """List mandates for a lawyer."""
        query = self.db.collection('mandates').where('lawyer_id', '==', lawyer_id)
        
        if client_id:
            query = query.where('client_id', '==', client_id)
        
        if status:
            query = query.where('status', '==', status.value)
        
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        
        docs = query.stream()
        
        mandates = []
        for doc in docs:
            try:
                mandates.append(Mandate(**doc.to_dict()))
            except Exception as e:
                logger.warning(f"Failed to parse mandate {doc.id}: {e}")
        
        return mandates
    
    async def update_mandate(
        self,
        lawyer_id: str,
        mandate_id: str,
        request: UpdateMandateRequest
    ) -> Optional[Mandate]:
        """Update mandate information."""
        
        # Verify ownership
        mandate = await self.get_mandate(lawyer_id, mandate_id)
        if not mandate:
            return None
        
        # Update fields
        update_data = {k: v for k, v in request.dict().items() if v is not None}
        update_data['updated_at'] = datetime.now()
        
        self.db.collection('mandates').document(mandate_id).update(update_data)
        
        return await self.get_mandate(lawyer_id, mandate_id)
    
    async def add_deadline(
        self,
        lawyer_id: str,
        request: AddDeadlineRequest
    ) -> Optional[Mandate]:
        """Add a deadline to a mandate."""
        
        mandate = await self.get_mandate(lawyer_id, request.mandate_id)
        if not mandate:
            return None
        
        # Create new deadline
        deadline = Deadline(
            title=request.title,
            due_date=request.due_date,
            priority=request.priority,
            notes=request.notes
        )
        
        # Add to mandate
        mandate.deadlines.append(deadline)
        
        # Update in Firestore
        self.db.collection('mandates').document(request.mandate_id).update({
            'deadlines': [d.dict() for d in mandate.deadlines],
            'updated_at': datetime.now()
        })
        
        return mandate
    
    async def get_upcoming_deadlines(
        self,
        lawyer_id: str,
        days_ahead: int = 30
    ) -> List[Dict[str, Any]]:
        """Get all upcoming deadlines across all mandates."""
        
        mandates = await self.list_mandates(lawyer_id, status=MandateStatus.IN_PROGRESS)
        
        from datetime import timedelta
        today = date.today()
        cutoff_date = today + timedelta(days=days_ahead)
        
        upcoming = []
        for mandate in mandates:
            for deadline in mandate.deadlines:
                if not deadline.completed and today <= deadline.due_date <= cutoff_date:
                    upcoming.append({
                        'mandate_id': mandate.mandate_id,
                        'mandate_title': mandate.title,
                        'client_id': mandate.client_id,
                        'deadline': deadline.dict(),
                        'days_until': (deadline.due_date - today).days
                    })
        
        # Sort by due date
        upcoming.sort(key=lambda x: x['deadline']['due_date'])
        
        return upcoming
    
    # === AI INSIGHTS ===
    
    async def generate_mandate_insights(
        self,
        lawyer_id: str,
        request: GenerateInsightsRequest
    ) -> MandateInsights:
        """Generate AI insights for a mandate."""
        
        mandate = await self.get_mandate(lawyer_id, request.mandate_id)
        if not mandate:
            raise ValueError("Mandate not found")
        
        client = await self.get_client(lawyer_id, mandate.client_id)
        
        # Get associated documents
        docs = await self.list_documents(lawyer_id, mandate_id=request.mandate_id)
        
        # Build context
        context = f"""
MANDAT: {mandate.title}
TYP: {mandate.mandate_type.value}
STATUS: {mandate.status.value}
ZUSAMMENFASSUNG: {mandate.summary}
GEGNER: {mandate.opposing_party or 'N/A'}
AKTENZEICHEN: {mandate.case_number or 'N/A'}

MANDANT: {client.first_name} {client.last_name}
"""
        
        if docs:
            context += f"\nVERBUNDENE DOKUMENTE: {len(docs)}\n"
            for doc in docs[:5]:  # Top 5
                if doc.ai_summary:
                    context += f"- {doc.filename}: {doc.ai_summary[:200]}\n"
        
        insights = MandateInsights(mandate_id=request.mandate_id)
        
        # Generate strategy
        if request.include_strategy:
            try:
                strategy_prompt = f"""
Du bist ein erfahrener Fachanwalt für Immobilienrecht.

{context}

Erstelle eine prägnante Verfahrensstrategie (max. 300 Wörter):
1. Rechtliche Einordnung
2. Empfohlenes Vorgehen
3. Wichtige zu berücksichtigende Punkte
"""
                response = self.ai_model.generate_content(strategy_prompt)
                insights.strategy = response.text.strip()
            except Exception as e:
                logger.error(f"Failed to generate strategy: {e}")
        
        # Risk assessment
        if request.include_risk_assessment:
            try:
                risk_prompt = f"""
{context}

Erstelle eine Risikoanalyse (max. 200 Wörter):
1. Hauptrisiken
2. Mögliche Probleme
3. Empfehlungen zur Risikominimierung
"""
                response = self.ai_model.generate_content(risk_prompt)
                insights.risk_assessment = response.text.strip()
            except Exception as e:
                logger.error(f"Failed to generate risk assessment: {e}")
        
        # Success probability
        if request.include_success_probability:
            try:
                prob_prompt = f"""
{context}

Schätze die Erfolgswahrscheinlichkeit dieses Mandats ein (0.0 bis 1.0).
Antworte NUR mit einer Zahl zwischen 0 und 1, z.B. "0.75"
"""
                response = self.ai_flash.generate_content(prob_prompt)
                try:
                    prob = float(response.text.strip())
                    insights.success_probability = max(0.0, min(1.0, prob))
                except ValueError:
                    pass
            except Exception as e:
                logger.error(f"Failed to estimate success probability: {e}")
        
        # Save insights to mandate
        self.db.collection('mandates').document(request.mandate_id).update({
            'ai_strategy': insights.strategy,
            'ai_risk_assessment': insights.risk_assessment,
            'success_probability': insights.success_probability,
            'updated_at': datetime.now()
        })
        
        return insights
    
    # === DOCUMENT MANAGEMENT ===
    
    async def list_documents(
        self,
        lawyer_id: str,
        client_id: Optional[str] = None,
        mandate_id: Optional[str] = None,
        category: Optional[DocumentCategory] = None,
        limit: int = 100
    ) -> List[Document]:
        """List documents for a lawyer."""
        query = self.db.collection('documents').where('lawyer_id', '==', lawyer_id)
        
        if client_id:
            query = query.where('client_id', '==', client_id)
        
        if mandate_id:
            query = query.where('mandate_id', '==', mandate_id)
        
        if category:
            query = query.where('category', '==', category.value)
        
        query = query.order_by('uploaded_at', direction=firestore.Query.DESCENDING).limit(limit)
        
        docs = query.stream()
        
        documents = []
        for doc in docs:
            try:
                documents.append(Document(**doc.to_dict()))
            except Exception as e:
                logger.warning(f"Failed to parse document {doc.id}: {e}")
        
        return documents
    
    async def get_document(self, lawyer_id: str, document_id: str) -> Optional[Document]:
        """Get a document by ID."""
        doc = self.db.collection('documents').document(document_id).get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        
        # Security check
        if data.get('lawyer_id') != lawyer_id:
            return None
        
        return Document(**data)
    
    async def search_documents_ai(
        self,
        lawyer_id: str,
        request: SearchDocumentsRequest
    ) -> List[DocumentSearchResult]:
        """Search documents using AI semantic search."""
        
        # Get candidate documents
        documents = await self.list_documents(
            lawyer_id=lawyer_id,
            client_id=request.client_id,
            mandate_id=request.mandate_id,
            category=request.category
        )
        
        if not documents:
            return []
        
        # Use AI to rank by relevance
        results = []
        
        for doc in documents:
            # Build document context
            doc_context = f"""
Dateiname: {doc.filename}
Kategorie: {doc.category.value}
Zusammenfassung: {doc.ai_summary or 'N/A'}
Schlüsselpunkte: {', '.join(doc.ai_key_points) if doc.ai_key_points else 'N/A'}
"""
            
            try:
                # Ask AI to rate relevance
                relevance_prompt = f"""
Suchanfrage: {request.query}

Dokument:
{doc_context}

Wie relevant ist dieses Dokument für die Suchanfrage?
Antworte NUR mit einer Zahl zwischen 0.0 (nicht relevant) und 1.0 (sehr relevant).
"""
                response = self.ai_flash.generate_content(relevance_prompt)
                try:
                    score = float(response.text.strip())
                    score = max(0.0, min(1.0, score))
                except ValueError:
                    score = 0.0
                
                if score > 0.3:  # Threshold
                    results.append(DocumentSearchResult(
                        document=doc,
                        relevance_score=score,
                        matching_excerpt=doc.ai_summary[:200] if doc.ai_summary else None
                    ))
            
            except Exception as e:
                logger.warning(f"Failed to score document {doc.document_id}: {e}")
        
        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:request.limit]
    
    async def chat_with_documents(
        self,
        lawyer_id: str,
        request: ChatWithDocumentsRequest
    ) -> ChatWithDocumentsResponse:
        """Chat with AI using document context."""
        
        # Gather context
        context_parts = []
        sources_used = []
        
        # Get mandate context
        if request.mandate_id:
            mandate = await self.get_mandate(lawyer_id, request.mandate_id)
            if mandate:
                context_parts.append(f"""
MANDAT: {mandate.title}
ZUSAMMENFASSUNG: {mandate.summary}
TYP: {mandate.mandate_type.value}
STATUS: {mandate.status.value}
""")
                sources_used.append(f"Mandat: {mandate.title}")
        
        # Get document context
        if request.document_ids:
            for doc_id in request.document_ids[:5]:  # Max 5 documents
                doc = await self.get_document(lawyer_id, doc_id)
                if doc:
                    context_parts.append(f"""
DOKUMENT: {doc.filename}
ZUSAMMENFASSUNG: {doc.ai_summary or 'N/A'}
SCHLÜSSELPUNKTE: {', '.join(doc.ai_key_points) if doc.ai_key_points else 'N/A'}
""")
                    sources_used.append(doc.filename)
        
        # Get client context
        if request.client_id:
            client = await self.get_client(lawyer_id, request.client_id)
            if client:
                context_parts.append(f"""
MANDANT: {client.first_name} {client.last_name}
ZUSAMMENFASSUNG: {client.ai_summary or 'N/A'}
""")
                sources_used.append(f"Mandant: {client.first_name} {client.last_name}")
        
        # Build prompt
        full_context = "\n\n---\n\n".join(context_parts)
        
        prompt = f"""
Du bist ein Assistent für einen Fachanwalt für Immobilienrecht.

KONTEXT:
{full_context}

FRAGE: {request.query}

Beantworte die Frage präzise und professionell unter Berücksichtigung des Kontexts.
"""
        
        # Generate response
        response = self.ai_model.generate_content(prompt)
        answer = response.text.strip()
        
        return ChatWithDocumentsResponse(
            answer=answer,
            sources_used=sources_used,
            confidence=0.85,  # Could be estimated with another AI call
            follow_up_questions=[
                "Welche rechtlichen Schritte sind als nächstes zu empfehlen?",
                "Gibt es ähnliche Präzedenzfälle?",
                "Welche Fristen sind zu beachten?"
            ]
        )
