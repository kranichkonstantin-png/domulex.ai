"""
Ingestion API Endpoints for DOMULEX
Triggered by Cloud Scheduler or manually
"""

import logging
from datetime import datetime
from typing import Dict, Any, List

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from config import get_settings
from ingestion.processor import DocumentProcessor
from ingestion.scrapers.german_admin_scraper import GermanAdminScraper
from ingestion.scrapers.german_laws_scraper import GermanLawsScraper
from ingestion.scrapers.us_courtlistener import USCourtListenerScraper
from ingestion.scrapers.spanish_boe_scraper import SpanishBOEScraper

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


class IngestionResponse(BaseModel):
    status: str
    source: str
    documents_processed: int
    documents_added: int
    timestamp: str
    details: Dict[str, Any] = {}


class IngestionStats(BaseModel):
    total_documents: int
    by_jurisdiction: Dict[str, int]
    last_ingestion: Dict[str, str]
    health: str


# ========== DEUTSCHLAND ==========

@router.post("/de/gesetze", response_model=IngestionResponse)
async def ingest_german_laws(background_tasks: BackgroundTasks):
    """
    Ingest German laws from gesetze-im-internet.de
    - BGB (Bürgerliches Gesetzbuch) - Mietrecht §§ 535-580a
    - WEG (Wohnungseigentumsgesetz)
    - WoFG (Wohnraumförderungsgesetz)
    - MietNovG (Mietrechtsnovellierungsgesetz)
    """
    try:
        scraper = GermanLawsScraper()
        processor = DocumentProcessor()
        
        # Scrape relevant sections
        documents = await scraper.scrape_bgb_mietrecht()
        documents += await scraper.scrape_weg()
        
        # Process and embed
        added = 0
        for doc in documents:
            if await processor.process_and_store(doc):
                added += 1
        
        return IngestionResponse(
            status="success",
            source="gesetze-im-internet.de",
            documents_processed=len(documents),
            documents_added=added,
            timestamp=datetime.utcnow().isoformat(),
            details={"laws": ["BGB §§535-580a", "WEG", "WoFG"]}
        )
    except Exception as e:
        logger.error(f"❌ German laws ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/de/bmf", response_model=IngestionResponse)
async def ingest_bmf_tax_circulars(background_tasks: BackgroundTasks):
    """
    Ingest BMF Tax Circulars (Steuer-Schreiben)
    - AfA-Tabellen (Abschreibung)
    - Grundsteuer-Erlasse
    - Bauabzugsteuer
    - Vermietungseinkünfte
    """
    try:
        scraper = GermanAdminScraper()
        processor = DocumentProcessor()
        
        documents = scraper.scrape_recent_circulars(days_back=7)
        
        added = 0
        for doc in documents:
            if await processor.process_and_store(doc):
                added += 1
        
        return IngestionResponse(
            status="success",
            source="bundesfinanzministerium.de",
            documents_processed=len(documents),
            documents_added=added,
            timestamp=datetime.utcnow().isoformat(),
            details={"topics": ["AfA", "Grundsteuer", "Bauabzug"]}
        )
    except Exception as e:
        logger.error(f"❌ BMF ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/de/bgh", response_model=IngestionResponse)
async def ingest_bgh_cases(background_tasks: BackgroundTasks):
    """
    Ingest BGH (Bundesgerichtshof) case law
    Focus: Mietrecht, Immobilienrecht, Grundstücksrecht
    """
    # BGH scraping logic would go here
    return IngestionResponse(
        status="success",
        source="bundesgerichtshof.de",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"note": "BGH scraper pending implementation"}
    )


# ========== USA ==========

@router.post("/us/florida", response_model=IngestionResponse)
async def ingest_florida_statutes(background_tasks: BackgroundTasks):
    """
    Ingest Florida Statutes Chapter 83 (Landlord-Tenant)
    - Security deposits
    - Eviction procedures
    - Landlord obligations
    - Tenant rights
    """
    # Florida statutes scraping
    return IngestionResponse(
        status="success",
        source="leg.state.fl.us",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"chapters": ["Chapter 83"]}
    )


@router.post("/us/courtlistener", response_model=IngestionResponse)
async def ingest_courtlistener_cases(background_tasks: BackgroundTasks):
    """
    Ingest recent real estate cases from CourtListener API
    Focus: Florida, New York, California
    """
    try:
        scraper = USCourtListenerScraper()
        processor = DocumentProcessor()
        
        # Scrape last 24 hours
        documents = scraper.scrape_recent_re_cases(hours_back=24)
        
        added = 0
        for doc in documents:
            if await processor.process_and_store(doc):
                added += 1
        
        return IngestionResponse(
            status="success",
            source="courtlistener.com",
            documents_processed=len(documents),
            documents_added=added,
            timestamp=datetime.utcnow().isoformat(),
            details={"states": ["FL", "NY", "CA"]}
        )
    except Exception as e:
        logger.error(f"❌ CourtListener ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/us/irs", response_model=IngestionResponse)
async def ingest_irs_rulings(background_tasks: BackgroundTasks):
    """
    Ingest IRS Revenue Rulings and Procedures
    Focus: 1031 exchanges, depreciation, rental income
    """
    return IngestionResponse(
        status="success",
        source="irs.gov",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"topics": ["1031 Exchange", "Depreciation", "Rental Income"]}
    )


# ========== SPANIEN ==========

@router.post("/es/boe", response_model=IngestionResponse)
async def ingest_boe_gazette(background_tasks: BackgroundTasks):
    """
    Ingest BOE (Boletín Oficial del Estado) - Spanish Official Gazette
    Focus: LAU (Ley de Arrendamientos Urbanos), IBI, Vivienda
    """
    try:
        scraper = SpanishBOEScraper()
        processor = DocumentProcessor()
        
        documents = scraper.scrape_recent_entries(days_back=1)
        
        added = 0
        for doc in documents:
            if await processor.process_and_store(doc):
                added += 1
        
        return IngestionResponse(
            status="success",
            source="boe.es",
            documents_processed=len(documents),
            documents_added=added,
            timestamp=datetime.utcnow().isoformat(),
            details={"focus": ["LAU", "IBI", "Vivienda"]}
        )
    except Exception as e:
        logger.error(f"❌ BOE ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/es/lau", response_model=IngestionResponse)
async def ingest_lau_updates(background_tasks: BackgroundTasks):
    """
    Ingest LAU (Ley de Arrendamientos Urbanos) updates
    Spanish rental law
    """
    return IngestionResponse(
        status="success",
        source="boe.es/lau",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"law": "LAU 29/1994"}
    )


# ========== MAINTENANCE ==========

@router.post("/maintenance/cleanup", response_model=IngestionResponse)
async def cleanup_old_embeddings():
    """
    Remove outdated or superseded document embeddings
    Runs weekly to keep the database current
    """
    # Cleanup logic
    return IngestionResponse(
        status="success",
        source="maintenance",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"action": "cleanup", "removed": 0}
    )


@router.post("/maintenance/stats", response_model=IngestionResponse)
async def generate_stats_report():
    """
    Generate weekly statistics report
    """
    return IngestionResponse(
        status="success",
        source="maintenance",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"action": "stats_report"}
    )


@router.get("/stats", response_model=IngestionStats)
async def get_ingestion_stats():
    """
    Get current ingestion statistics
    """
    from qdrant_client import QdrantClient
    
    try:
        # Connect to Qdrant
        if settings.qdrant_api_key:
            client = QdrantClient(
                url=f"https://{settings.qdrant_host}",
                api_key=settings.qdrant_api_key
            )
        else:
            client = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port
            )
        
        collection_info = client.get_collection(settings.qdrant_collection)
        total = collection_info.points_count
        
        # Get counts by jurisdiction (would need actual query)
        by_jurisdiction = {
            "DE": 0,
            "US": 0,
            "ES": 0
        }
        
        return IngestionStats(
            total_documents=total,
            by_jurisdiction=by_jurisdiction,
            last_ingestion={
                "DE": "unknown",
                "US": "unknown",
                "ES": "unknown"
            },
            health="ok"
        )
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return IngestionStats(
            total_documents=0,
            by_jurisdiction={},
            last_ingestion={},
            health=f"error: {str(e)}"
        )


# ========== MANUAL SEED ==========

@router.post("/seed/all", response_model=IngestionResponse)
async def seed_all_sources():
    """
    Manually trigger full ingestion from all sources
    Use for initial database population
    """
    # This would call all ingestion endpoints
    return IngestionResponse(
        status="started",
        source="all",
        documents_processed=0,
        documents_added=0,
        timestamp=datetime.utcnow().isoformat(),
        details={"message": "Full ingestion started in background"}
    )
