"""
Spanish Celery Tasks
Scheduled scraping tasks for Spanish legal sources
"""

import logging
from celery import Task
from qdrant_client import QdrantClient

from ingestion.celery_worker import celery_app
from ingestion.scrapers.spanish_boe_scraper import SpanishBOEScraper
from ingestion.processor import DocumentProcessor
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class QdrantTask(Task):
    """Base Task mit Qdrant Connection"""
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
    default_retry_delay=300
)
def scrape_boe_xml_feed(self):
    """
    BOE XML Feed - Official Spanish Gazette
    Scheduled: Daily 06:00 UTC
    """
    logger.info("🇪🇸 Starting BOE Scraper")
    
    try:
        scraper = SpanishBOEScraper()
        
        # Scrape last 7 days
        documents = scraper.scrape_recent_boe(
            days_back=7,
            max_docs=50
        )
        
        if not documents:
            logger.info("ℹ️  Keine neuen BOE Dokumente")
            return {"status": "success", "documents_found": 0}
        
        # Process & Upload
        processor = DocumentProcessor(qdrant_client=self.qdrant)
        
        stats = {
            "found": len(documents),
            "processed": 0,
            "duplicates": 0,
            "irrelevant": 0,
            "uploaded_chunks": 0
        }
        
        for doc in documents:
            try:
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
                logger.error(f"Fehler bei BOE Doc {doc.title[:50]}: {e}")
                continue
        
        logger.info(f"✅ BOE Scraper done: {stats}")
        return stats
        
    except Exception as exc:
        logger.error(f"❌ BOE Scraper failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@celery_app.task(base=QdrantTask, bind=True)
def scrape_cendoj_rulings(self):
    """CENDOJ Court Rulings - Weekly Wednesday 07:30"""
    logger.info("🇪🇸 CENDOJ Scraper - Not yet implemented")
    return {"status": "not_implemented"}
