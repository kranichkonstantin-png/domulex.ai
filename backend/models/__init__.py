"""Models package initialization."""

from .legal import (
    Jurisdiction,
    UserRole,
    LegalDocument,
    UploadedDocumentRef,
    QueryRequest,
    QueryResponse,
    IngestionRequest,
    IngestionResponse,
    ConflictRequest,
    ConflictResponse,
    ConflictAnalysis,
)

__all__ = [
    "Jurisdiction",
    "UserRole",
    "LegalDocument",
    "UploadedDocumentRef",
    "QueryRequest",
    "QueryResponse",
    "IngestionRequest",
    "IngestionResponse",
    "ConflictRequest",
    "ConflictResponse",
    "ConflictAnalysis",
]
