"""
Celery Worker für DOMULEX Ingestion Engine
24/7 Automated Legal Intelligence Collection
"""

import logging
from celery import Celery
from celery.schedules import crontab
from kombu import Queue

from config import get_settings

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Celery App Konfiguration
celery_app = Celery(
    "domulex_ingestion",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "ingestion.tasks.german_tasks",
        "ingestion.tasks.us_tasks",
        "ingestion.tasks.spanish_tasks",
    ],
)

# Celery Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 Stunde max pro Task
    task_soft_time_limit=3000,  # 50 Minuten Soft-Limit
    worker_prefetch_multiplier=1,  # Verhindert Worker-Overload
    worker_max_tasks_per_child=50,  # Restart Worker nach 50 Tasks (Memory Leak Prevention)
    result_expires=86400,  # Results nach 24h löschen
    task_acks_late=True,  # Nur ACK wenn Task erfolgreich
    task_reject_on_worker_lost=True,
    # Queues
    task_default_queue="default",
    task_queues=(
        Queue("default", routing_key="task.#"),
        Queue("scraping", routing_key="scraping.#"),
        Queue("processing", routing_key="processing.#"),
        Queue("priority", routing_key="priority.#"),
    ),
)

# Beat Schedule - The Heart of Data Supremacy
celery_app.conf.beat_schedule = {
    # ========== DEUTSCHLAND (Hochfrequent) ==========
    "scrape-de-bgh-every-4h": {
        "task": "ingestion.tasks.german_tasks.scrape_bgh_cases",
        "schedule": crontab(minute=0, hour="*/4"),  # Alle 4 Stunden
        "options": {"queue": "scraping"},
    },
    "scrape-de-bmf-daily": {
        "task": "ingestion.tasks.german_tasks.scrape_bmf_tax_circulars",
        "schedule": crontab(minute=30, hour=2),  # 02:30 UTC täglich
        "options": {"queue": "scraping"},
    },
    "scrape-de-bfh-weekly": {
        "task": "ingestion.tasks.german_tasks.scrape_bfh_tax_rulings",
        "schedule": crontab(minute=0, hour=3, day_of_week=1),  # Montags 03:00
        "options": {"queue": "scraping"},
    },
    
    # ========== USA (CourtListener Firehose) ==========
    "scrape-us-courtlistener-hourly": {
        "task": "ingestion.tasks.us_tasks.scrape_courtlistener_recent",
        "schedule": crontab(minute=15),  # Jede Stunde bei Minute 15
        "options": {"queue": "scraping"},
    },
    "scrape-us-irs-rulings-daily": {
        "task": "ingestion.tasks.us_tasks.scrape_irs_revenue_rulings",
        "schedule": crontab(minute=0, hour=4),  # 04:00 UTC täglich
        "options": {"queue": "scraping"},
    },
    "scrape-us-florida-statutes-weekly": {
        "task": "ingestion.tasks.us_tasks.scrape_florida_statutes",
        "schedule": crontab(minute=0, hour=5, day_of_week=2),  # Dienstags 05:00
        "options": {"queue": "scraping"},
    },
    
    # ========== SPANIEN (BOE Official Feed) ==========
    "scrape-es-boe-daily": {
        "task": "ingestion.tasks.spanish_tasks.scrape_boe_xml_feed",
        "schedule": crontab(minute=0, hour=6),  # 06:00 UTC täglich
        "options": {"queue": "scraping"},
    },
    "scrape-es-cendoj-weekly": {
        "task": "ingestion.tasks.spanish_tasks.scrape_cendoj_rulings",
        "schedule": crontab(minute=30, hour=7, day_of_week=3),  # Mittwochs 07:30
        "options": {"queue": "scraping"},
    },
    
    # ========== MAINTENANCE & CLEANUP ==========
    "cleanup-old-embeddings-weekly": {
        "task": "ingestion.tasks.maintenance.cleanup_old_embeddings",
        "schedule": crontab(minute=0, hour=1, day_of_week=0),  # Sonntags 01:00
        "options": {"queue": "processing"},
    },
    "generate-weekly-intelligence-report": {
        "task": "ingestion.tasks.maintenance.generate_intelligence_summary",
        "schedule": crontab(minute=0, hour=8, day_of_week=5),  # Freitags 08:00
        "options": {"queue": "priority"},
    },
}

# Celery Signals für Monitoring
@celery_app.task(bind=True)
def debug_task(self):
    """Debug Task für Health Checks"""
    logger.info(f"Request: {self.request!r}")
    return {"status": "healthy", "worker": "online"}


# Worker Startup Hook
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Wird ausgeführt wenn Worker startet"""
    logger.info("🚀 DOMULEX Celery Worker gestartet")
    logger.info(f"📊 Configured Beat Schedule: {len(celery_app.conf.beat_schedule)} tasks")


# Task Failure Hook
@celery_app.task(bind=True, max_retries=3)
def on_task_failure(self, exc, task_id, args, kwargs, einfo):
    """Global Error Handler"""
    logger.error(f"❌ Task {task_id} fehlgeschlagen: {exc}")
    logger.error(f"Args: {args}, Kwargs: {kwargs}")
    logger.error(f"Exception Info: {einfo}")
    
    # Sentry Integration (optional)
    if settings.sentry_dsn:
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
        except ImportError:
            pass


if __name__ == "__main__":
    celery_app.start()
