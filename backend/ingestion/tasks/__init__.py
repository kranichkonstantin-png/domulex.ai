"""Task package initialization"""

from .german_tasks import (
    scrape_bmf_tax_circulars,
    scrape_bgh_cases,
    scrape_bfh_tax_rulings,
)
from .us_tasks import (
    scrape_courtlistener_recent,
    scrape_irs_revenue_rulings,
    scrape_florida_statutes,
)
from .spanish_tasks import (
    scrape_boe_xml_feed,
    scrape_cendoj_rulings,
)
from .maintenance import (
    cleanup_old_embeddings,
    generate_intelligence_summary,
)

__all__ = [
    # German
    "scrape_bmf_tax_circulars",
    "scrape_bgh_cases",
    "scrape_bfh_tax_rulings",
    # US
    "scrape_courtlistener_recent",
    "scrape_irs_revenue_rulings",
    "scrape_florida_statutes",
    # Spanish
    "scrape_boe_xml_feed",
    "scrape_cendoj_rulings",
    # Maintenance
    "cleanup_old_embeddings",
    "generate_intelligence_summary",
]
