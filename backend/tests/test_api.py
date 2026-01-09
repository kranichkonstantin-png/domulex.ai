"""
Tests for API Endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "qdrant" in data
    assert "gemini" in data


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "DOMULEX Backend"
    assert "supported_jurisdictions" in data


def test_get_jurisdictions(client: TestClient):
    """Test jurisdictions endpoint."""
    response = client.get("/jurisdictions")
    assert response.status_code == 200
    data = response.json()
    assert "jurisdictions" in data
    assert len(data["jurisdictions"]) == 3  # DE, ES, US


def test_get_stats(client: TestClient):
    """Test stats endpoint."""
    response = client.get("/stats")
    assert response.status_code == 200
    # May have error if Qdrant not running
    # Just check response format
    data = response.json()
    assert "total_documents" in data


@pytest.mark.asyncio
async def test_query_missing_fields(client: TestClient):
    """Test query with missing fields."""
    response = client.post("/query", json={
        "query": "Test question"
        # Missing required fields
    })
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_query_invalid_jurisdiction(client: TestClient):
    """Test query with invalid jurisdiction."""
    response = client.post("/query", json={
        "query": "Test question",
        "target_jurisdiction": "INVALID",
        "user_role": "TENANT",
        "user_language": "de"
    })
    assert response.status_code == 422


def test_conflict_resolution_missing_fields(client: TestClient):
    """Test conflict resolution with missing fields."""
    response = client.post("/resolve_conflict", json={
        "party_a_statement": "Statement A"
        # Missing party_b_statement
    })
    assert response.status_code == 422


def test_analyze_contract_no_file(client: TestClient):
    """Test contract analysis without file."""
    response = client.post("/analyze_contract", data={
        "jurisdiction": "DE",
        "user_role": "TENANT"
    })
    assert response.status_code == 422  # Missing file


def test_analyze_contract_invalid_jurisdiction(client: TestClient):
    """Test contract analysis with invalid jurisdiction."""
    # Create dummy PDF file
    files = {"file": ("test.pdf", b"PDF content", "application/pdf")}
    data = {
        "jurisdiction": "INVALID",
        "user_role": "TENANT"
    }
    response = client.post("/analyze_contract", files=files, data=data)
    assert response.status_code == 400  # Bad request
