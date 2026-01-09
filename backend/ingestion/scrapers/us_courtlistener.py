"""
US CourtListener Scraper - The Firehose
Automated case law collection from Federal & State courts
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from models.legal import LegalDocument, Jurisdiction
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class USCourtListenerScraper:
    """
    CourtListener API Integration.
    
    Focus:
    - Florida, New York, California (Hotspot-States für Immobilien)
    - Federal Courts (Tax Court, Bankruptcy)
    - Nur letzten 24h (High-Frequency)
    """
    
    BASE_URL = "https://www.courtlistener.com/api/rest/v3"
    
    # Real Estate Keywords (Pre-Filter)
    RE_KEYWORDS = [
        "property", "real estate", "landlord", "tenant", "lease",
        "rental", "eviction", "foreclosure", "mortgage", "deed",
        "title", "zoning", "tax", "depreciation", "1031"
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.courtlistener_api_key
        
        if not self.api_key:
            logger.warning("⚠️  CourtListener API Key fehlt - Limit: 100 req/day")
        
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Token {self.api_key}"
            })
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=30)
    )
    def search_opinions(
        self,
        query: str,
        jurisdiction: str = "fl",
        date_filed_after: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Search CourtListener Opinions API.
        
        Args:
            query: Search query (Keywords)
            jurisdiction: State code (fl, ny, ca) oder "fed"
            date_filed_after: Nur Fälle nach diesem Datum
        """
        endpoint = f"{self.BASE_URL}/search/"
        
        params = {
            "q": query,
            "type": "o",  # Opinions
            "court": jurisdiction,
            "order_by": "dateFiled desc",
        }
        
        if date_filed_after:
            params["filed_after"] = date_filed_after.strftime("%Y-%m-%d")
        
        logger.info(f"🔍 Searching CourtListener: {query} in {jurisdiction}")
        
        response = self.session.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        results = data.get("results", [])
        
        logger.info(f"📊 Found {len(results)} cases")
        return results
    
    def is_relevant(self, case_data: Dict) -> bool:
        """
        Quick filter: Enthält der Case Real Estate Keywords?
        """
        text = (
            case_data.get("caseName", "") + " " +
            case_data.get("snippet", "")
        ).lower()
        
        matches = sum(1 for kw in self.RE_KEYWORDS if kw in text)
        
        if matches >= 2:  # Min. 2 Keywords
            logger.debug(f"✅ RELEVANT: {case_data.get('caseName', '')[:50]}")
            return True
        else:
            logger.debug(f"⏭️  SKIP: {case_data.get('caseName', '')[:50]}")
            return False
    
    def scrape_recent_florida_cases(
        self,
        hours_back: int = 24,
        max_docs: int = 50
    ) -> List[LegalDocument]:
        """
        Scrape Florida Real Estate Cases der letzten N Stunden.
        """
        logger.info(f"🇺🇸 Florida Scraper (last {hours_back}h)")
        
        documents = []
        cutoff = datetime.utcnow() - timedelta(hours=hours_back)
        
        try:
            # Search mit RE Keywords
            results = self.search_opinions(
                query=" OR ".join(self.RE_KEYWORDS[:5]),  # Top 5 Keywords
                jurisdiction="fl",
                date_filed_after=cutoff
            )
            
            for case in results:
                if len(documents) >= max_docs:
                    break
                
                # Relevance Filter
                if not self.is_relevant(case):
                    continue
                
                # Extract Data
                doc = LegalDocument(
                    id=str(case.get("id")),
                    jurisdiction=Jurisdiction.US,
                    sub_jurisdiction="Florida",
                    title=case.get("caseName", "Unknown Case"),
                    content_original=case.get("snippet", ""),
                    source_url=f"https://www.courtlistener.com{case.get('absolute_url', '')}",
                    publication_date=datetime.fromisoformat(case.get("dateFiled", datetime.utcnow().isoformat())),
                    document_type="Court Opinion",
                    language="en",
                    keywords=[kw for kw in self.RE_KEYWORDS if kw in case.get("snippet", "").lower()][:10]
                )
                
                documents.append(doc)
                logger.info(f"✅ [{len(documents)}] {doc.title[:60]}...")
            
            logger.info(f"🎉 Florida Scraping done: {len(documents)} docs")
            return documents
            
        except Exception as e:
            logger.error(f"CourtListener Scraper failed: {e}", exc_info=True)
            return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = USCourtListenerScraper()
    docs = scraper.scrape_recent_florida_cases(hours_back=168, max_docs=10)  # 7 days
    
    print(f"\n📊 Results: {len(docs)} documents")
    for doc in docs:
        print(f"  - {doc.title}")
