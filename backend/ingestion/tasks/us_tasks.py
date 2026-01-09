"""
US Celery Tasks
Scheduled scraping tasks for US legal sources
"""

import logging
from celery import Task
from qdrant_client import QdrantClient

from ingestion.celery_worker import celery_app
from ingestion.scrapers.us_courtlistener import USCourtListenerScraper
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
    default_retry_delay=600
)
def scrape_courtlistener_recent(self):
    """
    CourtListener Firehose - Recent Cases
    Scheduled: Hourly at :15
    """
    logger.info("🇺🇸 Starting CourtListener Scraper")
    
    try:
        scraper = USCourtListenerScraper()
        
        # Scrape last 2 hours (overlap für Sicherheit)
        documents = scraper.scrape_recent_florida_cases(
            hours_back=2,
            max_docs=100
        )
        
        if not documents:
            logger.info("ℹ️  Keine neuen CourtListener Cases")
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
                logger.error(f"Fehler bei Case {doc.title[:50]}: {e}")
                continue
        
        logger.info(f"✅ CourtListener done: {stats}")
        return stats
        
    except Exception as exc:
        logger.error(f"❌ CourtListener failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@celery_app.task(base=QdrantTask, bind=True)
def scrape_irs_revenue_rulings(self):
    """IRS Revenue Rulings - Daily 04:00"""
    logger.info("🇺🇸 IRS Scraper - Not yet implemented")
    return {"status": "not_implemented"}


@celery_app.task(base=QdrantTask, bind=True)
def scrape_florida_statutes(self):
    """Florida Statutes - Weekly Tuesday 05:00"""
    logger.info("🇺🇸 Florida Statutes Scraper - Not yet implemented")
    return {"status": "not_implemented"}
