"""
Legal Domain Models for DOMULEX
Strict schemas to prevent cross-jurisdictional hallucinations.
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class Jurisdiction(str, Enum):
    """Primary jurisdiction filter - CRITICAL for preventing legal hallucinations."""
    DE = "DE"  # Germany - Civil Law
    EU = "EU"  # European Union - Supranational Law
    ES = "ES"  # Spain - Civil Law
    US = "US"  # USA - Common Law
    AE = "AE"  # UAE/Dubai - Islamic/Civil Law Hybrid


class UserRole(str, Enum):
    """User role determines context and prompt engineering."""
    # English roles
    INVESTOR = "INVESTOR"
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    MEDIATOR = "MEDIATOR"  # For conflict resolution mode
    LAWYER = "LAWYER"  # Professional legal workbench mode
    # German roles (aliases)
    MIETER = "MIETER"  # = TENANT
    VERMIETER = "VERMIETER"  # = LANDLORD
    EIGENTUEMER = "EIGENTUEMER"  # = OWNER
    VERWALTER = "VERWALTER"  # = MANAGER
    ANWALT = "ANWALT"  # = LAWYER


class LegalDocument(BaseModel):
    """
    Core legal document model.
    Stored in Qdrant with jurisdiction-based filtering.
    """
    id: UUID = Field(default_factory=uuid4)
    jurisdiction: Jurisdiction = Field(
        ..., 
        description="PRIMARY FILTER - Never mix jurisdictions in retrieval"
    )
    sub_jurisdiction: Optional[str] = Field(
        None, 
        description="State/Region: e.g., 'Bayern', 'Florida', 'Mallorca'"
    )
    title: str = Field(..., description="Document title or case name")
    content_original: str = Field(..., description="Full legal text in original language")
    source_url: Optional[str] = Field(None, description="Official source URL (optional)")
    publication_date: date = Field(..., description="Recency matters for legal validity")
    document_type: str = Field(
        ..., 
        description="e.g., 'statute', 'case_law', 'regulation'"
    )
    language: str = Field(..., description="ISO 639-1 code: 'de', 'es', 'en'")
    
    # Metadata for retrieval
    keywords: list[str] = Field(default_factory=list)
    embedding_vector: Optional[list[float]] = Field(None, description="Qdrant vector")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "jurisdiction": "DE",
                "sub_jurisdiction": "Bayern",
                "title": "BGB § 535 - Inhalt und Hauptpflichten des Mietvertrags",
                "content_original": "Durch den Mietvertrag wird der Vermieter verpflichtet...",
                "source_url": "https://www.gesetze-im-internet.de/bgb/__535.html",
                "publication_date": "2002-01-02",
                "document_type": "statute",
                "language": "de",
                "keywords": ["Mietvertrag", "Vermieter", "Mieter"]
            }
        }


class UploadedDocumentRef(BaseModel):
    """Reference to an uploaded document for query context."""
    document_id: str = Field(..., description="Document ID from upload")
    text: str = Field(..., description="Extracted text from document")


class QueryRequest(BaseModel):
    """User query request model."""
    query: str = Field(..., min_length=10, description="User's legal question")
    target_jurisdiction: Jurisdiction = Field(..., description="Which country's law to query")
    user_role: UserRole = Field(default=UserRole.INVESTOR)
    user_language: str = Field(default="de", description="ISO 639-1: de, es, en")
    sub_jurisdiction: Optional[str] = Field(None, description="Specific state/region if needed")
    user_id: Optional[str] = Field(None, description="Firebase user ID for quota tracking")
    user_tier: Optional[str] = Field(default="free", description="User subscription tier: free, mieter_plus, professional, lawyer")
    source_filter: Optional[list[str]] = Field(None, description="Filter by doc_type (e.g., ['GESETZ', 'URTEIL', 'LITERATUR'])")
    gerichtsebene_filter: Optional[list[str]] = Field(None, description="Filter by gerichtsebene (e.g., ['BGH', 'OLG', 'LG', 'AG'])")
    use_public_sources: Optional[bool] = Field(default=False, description="🔑 Use public sources (BGB, BGH, literature) for enhanced answers")
    uploaded_documents: Optional[list[UploadedDocumentRef]] = Field(default=None, description="📎 Uploaded documents to include in context")


class QueryResponse(BaseModel):
    """Response with legal answer and sources."""
    answer: str = Field(..., description="AI-generated legal explanation")
    sources: list[LegalDocument] = Field(default_factory=list)
    jurisdiction_warning: Optional[str] = Field(
        None, 
        description="Warning if query spans multiple jurisdictions"
    )
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class IngestionRequest(BaseModel):
    """Request to trigger data ingestion."""
    jurisdiction: Jurisdiction
    force_refresh: bool = Field(default=False)
    max_documents: Optional[int] = Field(None, description="Limit for testing")


class IngestionResponse(BaseModel):
    """Response from ingestion process."""
    status: str
    documents_processed: int
    errors: list[str] = Field(default_factory=list)


class ConflictRequest(BaseModel):
    """Request for conflict resolution analysis."""
    party_a_statement: str = Field(
        ..., 
        min_length=20, 
        description="Party A's perspective (e.g., Landlord's view)"
    )
    party_b_statement: str = Field(
        ..., 
        min_length=20, 
        description="Party B's perspective (e.g., Tenant's view)"
    )
    jurisdiction: Jurisdiction = Field(
        ..., 
        description="Jurisdiction for legal precedent search"
    )
    sub_jurisdiction: Optional[str] = Field(
        None, 
        description="Specific state/region if applicable"
    )
    user_language: str = Field(
        default="en", 
        description="Response language (de, es, en)"
    )
    party_a_label: str = Field(
        default="Party A",
        description="Label for first party (e.g., 'Landlord', 'Seller')"
    )
    party_b_label: str = Field(
        default="Party B",
        description="Label for second party (e.g., 'Tenant', 'Buyer')"
    )


class ConflictAnalysis(BaseModel):
    """Individual party's legal analysis."""
    party_label: str
    legal_arguments: str = Field(
        ..., 
        description="Legal basis supporting this party"
    )
    supporting_sources: list[LegalDocument] = Field(default_factory=list)
    strength_assessment: str = Field(
        ..., 
        description="Weak/Moderate/Strong with reasoning"
    )


class ConflictResponse(BaseModel):
    """Response from conflict resolution analysis."""
    dispute_summary: str = Field(
        ..., 
        description="Brief summary of the dispute"
    )
    party_a_analysis: ConflictAnalysis
    party_b_analysis: ConflictAnalysis
    neutral_assessment: str = Field(
        ..., 
        description="Neutral legal analysis of the situation"
    )
    success_probability_a: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Party A's litigation success probability (0-100%)"
    )
    success_probability_b: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Party B's litigation success probability (0-100%)"
    )
    settlement_likelihood: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Probability parties should settle (0-100%)"
    )
    recommendation: str = Field(
        ..., 
        description="Mediator's recommendation with reasoning"
    )
    jurisdiction: Jurisdiction
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    duration_seconds: float
