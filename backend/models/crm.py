"""
CRM Models for Lawyer Practice Management
Client/Mandate/Document management with AI integration
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime, date
from enum import Enum


class ClientStatus(str, Enum):
    """Status of a client relationship."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"
    PROSPECT = "PROSPECT"


class MandateStatus(str, Enum):
    """Status of a legal mandate/case."""
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class MandateType(str, Enum):
    """Type of legal mandate."""
    MIETRECHT = "MIETRECHT"  # Tenant law
    KAUFRECHT = "KAUFRECHT"  # Purchase law
    WEG = "WEG"  # Condominium law
    BAURECHT = "BAURECHT"  # Construction law
    PROZESSFUEHRUNG = "PROZESSFUEHRUNG"  # Litigation
    BERATUNG = "BERATUNG"  # Consultation
    SONSTIGES = "SONSTIGES"  # Other


class DocumentCategory(str, Enum):
    """Category of legal document."""
    CONTRACT = "CONTRACT"  # Verträge
    CORRESPONDENCE = "CORRESPONDENCE"  # Schriftverkehr
    COURT_FILING = "COURT_FILING"  # Gerichtsakte
    EVIDENCE = "EVIDENCE"  # Beweismittel
    INVOICE = "INVOICE"  # Rechnungen
    NOTE = "NOTE"  # Notizen
    TEMPLATE = "TEMPLATE"  # Vorlagen
    OTHER = "OTHER"


class Priority(str, Enum):
    """Priority level."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


# === CLIENT MANAGEMENT ===

class Client(BaseModel):
    """Client/Mandant model."""
    client_id: str = Field(..., description="Unique client ID (Firestore doc ID)")
    lawyer_id: str = Field(..., description="Firebase UID of the lawyer")
    
    # Personal Information
    first_name: str
    last_name: str
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_zip: Optional[str] = None
    
    # Status
    status: ClientStatus = ClientStatus.ACTIVE
    client_since: datetime = Field(default_factory=datetime.now)
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    
    # AI-generated insights
    ai_summary: Optional[str] = Field(None, description="AI-generated client summary")
    risk_assessment: Optional[str] = Field(None, description="AI risk assessment")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CreateClientRequest(BaseModel):
    """Request to create a new client."""
    first_name: str
    last_name: str
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_zip: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class UpdateClientRequest(BaseModel):
    """Request to update client information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_zip: Optional[str] = None
    status: Optional[ClientStatus] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


# === MANDATE MANAGEMENT ===

class Deadline(BaseModel):
    """A legal deadline/Frist."""
    title: str
    due_date: date
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    notes: Optional[str] = None


class Mandate(BaseModel):
    """Legal mandate/case model."""
    mandate_id: str = Field(..., description="Unique mandate ID")
    lawyer_id: str = Field(..., description="Firebase UID of the lawyer")
    client_id: str = Field(..., description="Associated client ID")
    
    # Mandate Information
    title: str = Field(..., description="Mandate title/description")
    mandate_type: MandateType
    status: MandateStatus = MandateStatus.NEW
    
    # Case Details
    case_number: Optional[str] = Field(None, description="Court case number if applicable")
    opposing_party: Optional[str] = Field(None, description="Gegner/Opposing party")
    summary: str = Field(..., description="Case summary")
    
    # Deadlines & Dates
    start_date: date = Field(default_factory=date.today)
    expected_end_date: Optional[date] = None
    deadlines: List[Deadline] = Field(default_factory=list)
    
    # Financial
    hourly_rate: Optional[float] = Field(None, description="Stundensatz in EUR")
    estimated_hours: Optional[float] = None
    total_billed: float = Field(default=0.0)
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    priority: Priority = Priority.MEDIUM
    
    # AI Insights
    ai_strategy: Optional[str] = Field(None, description="AI-generated legal strategy")
    ai_risk_assessment: Optional[str] = Field(None, description="AI risk assessment")
    ai_similar_cases: List[str] = Field(default_factory=list, description="Similar case IDs")
    success_probability: Optional[float] = Field(None, description="AI-estimated success rate 0-1")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CreateMandateRequest(BaseModel):
    """Request to create a new mandate."""
    client_id: str
    title: str
    mandate_type: MandateType
    summary: str
    case_number: Optional[str] = None
    opposing_party: Optional[str] = None
    expected_end_date: Optional[date] = None
    hourly_rate: Optional[float] = None
    estimated_hours: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    priority: Priority = Priority.MEDIUM


class UpdateMandateRequest(BaseModel):
    """Request to update mandate information."""
    title: Optional[str] = None
    status: Optional[MandateStatus] = None
    summary: Optional[str] = None
    case_number: Optional[str] = None
    opposing_party: Optional[str] = None
    expected_end_date: Optional[date] = None
    hourly_rate: Optional[float] = None
    estimated_hours: Optional[float] = None
    total_billed: Optional[float] = None
    tags: Optional[List[str]] = None
    priority: Optional[Priority] = None


class AddDeadlineRequest(BaseModel):
    """Request to add a deadline to a mandate."""
    mandate_id: str
    title: str
    due_date: date
    priority: Priority = Priority.MEDIUM
    notes: Optional[str] = None


# === DOCUMENT MANAGEMENT ===

class Document(BaseModel):
    """Legal document model."""
    document_id: str = Field(..., description="Unique document ID")
    lawyer_id: str = Field(..., description="Firebase UID of the lawyer")
    
    # Associations
    client_id: Optional[str] = Field(None, description="Associated client")
    mandate_id: Optional[str] = Field(None, description="Associated mandate")
    
    # Document Information
    filename: str
    original_filename: str
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str
    storage_path: str = Field(..., description="Path in Firebase Storage")
    
    # Categorization
    category: DocumentCategory = DocumentCategory.OTHER
    tags: List[str] = Field(default_factory=list)
    title: Optional[str] = None
    description: Optional[str] = None
    
    # AI Analysis
    ai_summary: Optional[str] = Field(None, description="AI-generated summary")
    ai_key_points: List[str] = Field(default_factory=list, description="AI-extracted key points")
    ai_legal_issues: List[str] = Field(default_factory=list, description="AI-identified legal issues")
    ai_risks: List[str] = Field(default_factory=list, description="AI-identified risks")
    extracted_text: Optional[str] = Field(None, description="Extracted text content")
    
    # Versioning
    version: int = Field(default=1)
    is_latest: bool = Field(default=True)
    previous_version_id: Optional[str] = None
    
    # Timestamps
    uploaded_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UploadDocumentRequest(BaseModel):
    """Request to upload a document."""
    client_id: Optional[str] = None
    mandate_id: Optional[str] = None
    category: DocumentCategory = DocumentCategory.OTHER
    tags: List[str] = Field(default_factory=list)
    title: Optional[str] = None
    description: Optional[str] = None


class SearchDocumentsRequest(BaseModel):
    """Request to search documents with AI."""
    query: str = Field(..., description="Natural language search query")
    client_id: Optional[str] = None
    mandate_id: Optional[str] = None
    category: Optional[DocumentCategory] = None
    tags: Optional[List[str]] = None
    limit: int = Field(default=10, ge=1, le=100)


class DocumentSearchResult(BaseModel):
    """Search result for a document."""
    document: Document
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    matching_excerpt: Optional[str] = None
    ai_explanation: Optional[str] = Field(None, description="Why this document matches")


# === AI INSIGHTS ===

class GenerateInsightsRequest(BaseModel):
    """Request to generate AI insights for a mandate."""
    mandate_id: str
    include_strategy: bool = True
    include_risk_assessment: bool = True
    include_similar_cases: bool = True
    include_success_probability: bool = True


class MandateInsights(BaseModel):
    """AI-generated insights for a mandate."""
    mandate_id: str
    strategy: Optional[str] = None
    risk_assessment: Optional[str] = None
    similar_case_ids: List[str] = Field(default_factory=list)
    success_probability: Optional[float] = None
    key_considerations: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.now)


class ChatWithDocumentsRequest(BaseModel):
    """Request to chat with context from specific documents/mandates."""
    query: str = Field(..., description="User's question")
    mandate_id: Optional[str] = Field(None, description="Context from this mandate")
    document_ids: List[str] = Field(default_factory=list, description="Context from these documents")
    client_id: Optional[str] = Field(None, description="Context from this client")


class ChatWithDocumentsResponse(BaseModel):
    """Response from document-aware chat."""
    answer: str
    sources_used: List[str] = Field(default_factory=list, description="Document IDs used as context")
    confidence: float = Field(..., ge=0.0, le=1.0)
    follow_up_questions: List[str] = Field(default_factory=list)
