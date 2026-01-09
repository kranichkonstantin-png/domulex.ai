"""
Tests for PDF Parser
"""

import pytest
from services.pdf_parser import PDFParser, RiskLevel, ClauseAnalysis


def test_risk_level_enum():
    """Test RiskLevel enum."""
    assert RiskLevel.GREEN == "GREEN"
    assert RiskLevel.YELLOW == "YELLOW"
    assert RiskLevel.RED == "RED"


def test_extract_keywords_de():
    """Test German keyword extraction."""
    title = "Mietvertrag und Kaution"
    content = "Der Mieter zahlt eine Kaution von 2000 Euro"
    
    from backend.ingestion.scraper_factory import GermanScraper
    scraper = GermanScraper()
    keywords = scraper._extract_keywords_de(title, content)
    
    assert "kaution" in keywords or "mieter" in keywords


def test_extract_keywords_us():
    """Test US keyword extraction."""
    title = "Security Deposit Law"
    content = "Landlord must return security deposit within 15 days"
    
    from backend.ingestion.scraper_factory import USScraper
    scraper = USScraper()
    keywords = scraper._extract_keywords_us(title, content)
    
    assert "security_deposit" in keywords or "landlord" in keywords


def test_extract_keywords_es():
    """Test Spanish keyword extraction."""
    title = "Ley de Arrendamientos Urbanos"
    content = "El arrendador debe cobrar una fianza"
    
    from backend.ingestion.scraper_factory import SpanishScraper
    scraper = SpanishScraper()
    keywords = scraper._extract_keywords_es(title, content)
    
    assert "fianza" in keywords or "arrendador" in keywords


@pytest.mark.asyncio
async def test_pdf_extraction_invalid():
    """Test PDF extraction with invalid bytes."""
    with pytest.raises(ValueError):
        PDFParser.extract_text_from_pdf(b"invalid pdf data")
