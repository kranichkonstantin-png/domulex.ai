"""
German Celery Tasks
Scheduled scraping tasks for German legal sources
"""

import logging
from celery import Task
from qdrant_client import QdrantClient

from ingestion.celery_worker import celery_app
from ingestion.scrapers.german_admin_scraper import GermanAdminScraper
from ingestion.processor import DocumentProcessor
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class QdrantTask(Task):
    """Base Task mit Qdrant Connection Pooling"""
    _qdrant = None
    
    @property
    def qdrant(self):
        if self._qdrant is None:
            self._qdrant = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port
            )
        return self._qdrant


@celery_app.task(
    base=QdrantTask,
    bind=True,
    max_retries=3,
    default_retry_delay=300  # 5 Minuten
)
def scrape_bmf_tax_circulars(self):
    """
    BMF Tax Circulars - The Investor Gold Mine
    Scheduled: Daily 02:30 UTC
    """
    logger.info("🇩🇪 Starting BMF Tax Circular Scraper")
    
    try:
        # Scraper initialisieren
        scraper = GermanAdminScraper()
        
        # Scrape letzte 30 Tage
        documents = scraper.scrape_recent_bmf_circulars(
            days_back=30,
            max_documents=50
        )
        
        if not documents:
            logger.warning("⚠️  Keine neuen BMF Dokumente gefunden")
            return {
                "status": "success",
                "documents_found": 0,
                "documents_processed": 0
            }
        
        # Processor für Upload
        processor = DocumentProcessor(qdrant_client=self.qdrant)
        
        stats = {
            "found": len(documents),
            "processed": 0,
            "duplicates": 0,
            "irrelevant": 0,
            "uploaded_chunks": 0
        }
        
        # Verarbeite jedes Dokument
        for doc in documents:
            try:
                # Process & Upload (async wrapper)
                import asyncio
                result = asyncio.run(processor.process_and_upload(doc))
                
                if result["processed"]:
                    stats["processed"] += 1
                    stats["uploaded_chunks"] += result["chunks_uploaded"]
                elif result["duplicate"]:
                    stats["duplicates"] += 1
                elif result["irrelevant"]:
                    stats["irrelevant"] += 1
                
            except Exception as e:
                logger.error(f"Fehler bei Dokument {doc.title[:50]}: {e}")
                continue
        
        logger.info(f"✅ BMF Scraper abgeschlossen: {stats}")
        return stats
        
    except Exception as exc:
        logger.error(f"❌ BMF Scraper fehlgeschlagen: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@celery_app.task(
    base=QdrantTask,
    bind=True,
    max_retries=2
)
def scrape_bgh_cases(self):
    """
    BGH (Bundesgerichtshof) Cases
    Scheduled: Every 4 hours
    """
    logger.info("🇩🇪 BGH Scraper - Not yet implemented")
    # TODO: Implement BGH scraper (rechtsprechung-im-internet.de)
    return {"status": "not_implemented"}


@celery_app.task(
    base=QdrantTask,
    bind=True
)
def scrape_bfh_tax_rulings(self):
    """
    BFH (Bundesfinanzhof) Tax Rulings
    Scheduled: Weekly Monday 03:00
    """
    logger.info("🇩🇪 BFH Scraper - Not yet implemented")
    # TODO: Implement BFH scraper
    return {"status": "not_implemented"}
