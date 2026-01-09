"""
Document Upload Models
Pydantic models for document upload and storage
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UploadedDocumentType(str, Enum):
    """Types of uploaded documents"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    IMAGE = "image"


class UploadedDocument(BaseModel):
    """Metadata for an uploaded user document"""
    id: str = Field(..., description="Unique document ID")
    user_id: str = Field(..., description="Firebase UID of uploader")
    filename: str = Field(..., description="Original filename")
    doc_type: UploadedDocumentType
    storage_url: str = Field(..., description="Cloud Storage URL")
    char_count: int
    word_count: int
    ocr_applied: bool = False
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = Field(None, description="Chat session ID")


class DocumentUploadResponse(BaseModel):
    """Response from document upload endpoint"""
    success: bool
    document: Optional[UploadedDocument] = None
    extracted_text_preview: Optional[str] = Field(None, description="First 500 chars for display")
    extracted_text_full: Optional[str] = Field(None, description="Full text for analysis (max 50k chars)")
    error: Optional[str] = None
