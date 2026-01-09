"""
Pytest Configuration
"""

import pytest
from fastapi.testclient import TestClient
from qdrant_client import QdrantClient

from main import app
from config import get_settings


@pytest.fixture
def client():
    """FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def settings():
    """Get settings."""
    return get_settings()


@pytest.fixture
def sample_query_request():
    """Sample query request."""
    return {
        "query": "Was sind meine Rechte als Mieter?",
        "target_jurisdiction": "DE",
        "user_role": "TENANT",
        "user_language": "de"
    }


@pytest.fixture
def sample_conflict_request():
    """Sample conflict resolution request."""
    return {
        "party_a_statement": "Mieter zahlt seit 2 Monaten keine Miete",
        "party_b_statement": "Heizung ist kaputt und wird nicht repariert",
        "jurisdiction": "DE",
        "party_a_label": "Vermieter",
        "party_b_label": "Mieter",
        "user_language": "de"
    }
