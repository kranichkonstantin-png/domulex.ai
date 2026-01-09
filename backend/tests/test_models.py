"""
Tests for Models
"""

import pytest
from datetime import date
from pydantic import ValidationError

from models.legal import (
    Jurisdiction,
    UserRole,
    LegalDocument,
    QueryRequest,
    ConflictRequest,
)


def test_jurisdiction_enum():
    """Test Jurisdiction enum."""
    assert Jurisdiction.DE == "DE"
    assert Jurisdiction.ES == "ES"
    assert Jurisdiction.US == "US"


def test_user_role_enum():
    """Test UserRole enum."""
    assert UserRole.TENANT == "TENANT"
    assert UserRole.LANDLORD == "LANDLORD"
    assert UserRole.INVESTOR == "INVESTOR"
    assert UserRole.MEDIATOR == "MEDIATOR"


def test_legal_document_creation():
    """Test LegalDocument model."""
    doc = LegalDocument(
        jurisdiction=Jurisdiction.DE,
        title="BGB § 535",
        content_original="Mietvertrag...",
        source_url="https://example.com",
        publication_date=date(2024, 1, 1),
        document_type="statute",
        language="de"
    )
    assert doc.jurisdiction == Jurisdiction.DE
    assert doc.title == "BGB § 535"
    assert doc.language == "de"


def test_legal_document_missing_required():
    """Test LegalDocument with missing required fields."""
    with pytest.raises(ValidationError):
        LegalDocument(
            jurisdiction=Jurisdiction.DE,
            # Missing required fields
        )


def test_query_request_validation():
    """Test QueryRequest validation."""
    # Valid request
    request = QueryRequest(
        query="Was sind meine Rechte?",
        target_jurisdiction=Jurisdiction.DE,
        user_role=UserRole.TENANT,
        user_language="de"
    )
    assert request.query == "Was sind meine Rechte?"
    
    # Invalid - query too short
    with pytest.raises(ValidationError):
        QueryRequest(
            query="Test",  # < 10 chars
            target_jurisdiction=Jurisdiction.DE,
            user_role=UserRole.TENANT,
            user_language="de"
        )


def test_conflict_request_validation():
    """Test ConflictRequest validation."""
    # Valid request
    request = ConflictRequest(
        party_a_statement="Vermieter sagt: Miete nicht bezahlt",
        party_b_statement="Mieter sagt: Heizung kaputt",
        jurisdiction=Jurisdiction.DE
    )
    assert request.party_a_label == "Party A"  # Default
    assert request.party_b_label == "Party B"  # Default
    
    # With custom labels
    request = ConflictRequest(
        party_a_statement="Vermieter sagt: Miete nicht bezahlt",
        party_b_statement="Mieter sagt: Heizung kaputt",
        jurisdiction=Jurisdiction.DE,
        party_a_label="Vermieter",
        party_b_label="Mieter"
    )
    assert request.party_a_label == "Vermieter"
    assert request.party_b_label == "Mieter"
