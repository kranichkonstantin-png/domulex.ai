"""
Legal Document Scraper Factory
Strictly separates data sources per jurisdiction to prevent contamination.
"""

import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from models.legal import LegalDocument, Jurisdiction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseLegalScraper(ABC):
    """
    Abstract base class for jurisdiction-specific scrapers.
    
    CRITICAL: Each scraper MUST only return documents for its jurisdiction.
    Never mix German BGB with US Code in the same scraper.
    """
    
    def __init__(self, jurisdiction: Jurisdiction):
        self.jurisdiction = jurisdiction
        self.documents_fetched: List[LegalDocument] = []
    
    @abstractmethod
    async def fetch(self, max_documents: Optional[int] = None) -> List[LegalDocument]:
        """
        Fetch legal documents from official source.
        
        Args:
            max_documents: Limit for testing purposes
            
        Returns:
            List of LegalDocument with jurisdiction field set correctly
        """
        pass
    
    @abstractmethod
    async def validate_source(self) -> bool:
        """Validate that the data source is accessible and official."""
        pass
    
    def _create_document(
        self,
        title: str,
        content: str,
        source_url: str,
        publication_date: date,
        document_type: str,
        language: str,
        sub_jurisdiction: Optional[str] = None,
        keywords: Optional[List[str]] = None,
    ) -> LegalDocument:
        """Helper to create LegalDocument with jurisdiction locked."""
        return LegalDocument(
            jurisdiction=self.jurisdiction,  # LOCKED to scraper's jurisdiction
            sub_jurisdiction=sub_jurisdiction,
            title=title,
            content_original=content,
            source_url=source_url,
            publication_date=publication_date,
            document_type=document_type,
            language=language,
            keywords=keywords or [],
        )


class GermanScraper(BaseLegalScraper):
    """
    Scraper for German legal documents.
    
    Sources:
    - rechtsprechung-im-internet.de (XML API)
    - gesetze-im-internet.de (BGB, HGB, etc.)
    - bundesfinanzhof.de (BFH tax cases)
    """
    
    def __init__(self):
        super().__init__(Jurisdiction.DE)
        self.base_urls = {
            "statutes": "https://www.gesetze-im-internet.de",
            "case_law": "https://www.rechtsprechung-im-internet.de",
        }
        # RSS feed for recent decisions
        self.rss_feed_url = "https://www.rechtsprechung-im-internet.de/jportal/portal/page/bsjrsprod.psml?feed=bsjrsfeed"
        self.min_date = date(2024, 1, 1)  # Only fetch recent documents
    
    async def fetch(self, max_documents: Optional[int] = None) -> List[LegalDocument]:
        """
        Fetch German legal documents from rechtsprechung-im-internet.de.
        
        Workflow:
        1. Fetch RSS/XML feed
        2. Parse XML for recent decisions
        3. Extract relevant fields (Gericht, Datum, Leitsatz, Tenor)
        4. Filter by date (> 2024-01-01)
        5. Create LegalDocument objects
        """
        documents = []
        
        try:
            logger.info("🇩🇪 Fetching German legal documents from rechtsprechung-im-internet.de")
            
            # Fetch RSS feed
            response = requests.get(
                self.rss_feed_url,
                timeout=30,
                headers={'User-Agent': 'DOMULEX Legal Research Bot/1.0'}
            )
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Find all items in the RSS feed
            items = root.findall('.//item')
            logger.info(f"Found {len(items)} items in RSS feed")
            
            for item in items:
                try:
                    # Extract fields from XML
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    description_elem = item.find('description')
                    pub_date_elem = item.find('pubDate')
                    
                    if not all([title_elem, link_elem]):
                        continue
                    
                    title = title_elem.text or "Untitled Decision"
                    link = link_elem.text
                    description = description_elem.text if description_elem is not None else ""
                    
                    # Parse publication date
                    pub_date = None
                    if pub_date_elem is not None and pub_date_elem.text:
                        try:
                            # RSS date format: "Tue, 15 Jan 2024 10:00:00 +0100"
                            pub_date = datetime.strptime(
                                pub_date_elem.text[:16], 
                                "%a, %d %b %Y"
                            ).date()
                        except Exception as e:
                            logger.warning(f"Could not parse date: {pub_date_elem.text} - {e}")
                            pub_date = date.today()
                    else:
                        pub_date = date.today()
                    
                    # Filter by date
                    if pub_date < self.min_date:
                        logger.debug(f"Skipping old document: {title} ({pub_date})")
                        continue
                    
                    # Extract court name from title (format: "Court - Case Number - Topic")
                    court_name = "Unbekanntes Gericht"
                    if " - " in title:
                        parts = title.split(" - ")
                        court_name = parts[0].strip()
                    
                    # Determine sub-jurisdiction from court name
                    sub_jurisdiction = None
                    if "BGH" in court_name:
                        sub_jurisdiction = "Bundesgerichtshof"
                    elif "BFH" in court_name:
                        sub_jurisdiction = "Bundesfinanzhof"
                    elif "OLG München" in court_name or "Bayern" in court_name:
                        sub_jurisdiction = "Bayern"
                    elif "OLG Köln" in court_name or "NRW" in court_name:
                        sub_jurisdiction = "NRW"
                    
                    # Create document
                    doc = self._create_document(
                        title=title,
                        content=description or title,  # Use description as content
                        source_url=link,
                        publication_date=pub_date,
                        document_type="case_law",
                        language="de",
                        sub_jurisdiction=sub_jurisdiction,
                        keywords=self._extract_keywords_de(title, description),
                    )
                    
                    documents.append(doc)
                    logger.debug(f"✓ Extracted: {title}")
                    
                    # Check max_documents limit
                    if max_documents and len(documents) >= max_documents:
                        break
                
                except Exception as e:
                    logger.error(f"Error parsing German document item: {e}")
                    continue
            
            logger.info(f"✅ Successfully fetched {len(documents)} German documents")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error fetching German documents: {e}")
        except ET.ParseError as e:
            logger.error(f"❌ XML parsing error: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error in GermanScraper: {e}")
        
        self.documents_fetched = documents
        return documents
    
    def _extract_keywords_de(self, title: str, description: str) -> List[str]:
        """Extract German legal keywords from title and description."""
        keywords = []
        text = f"{title} {description}".lower()
        
        # Common German legal terms
        terms = [
            "mietvertrag", "mieter", "vermieter", "kaution", "kündigung",
            "eigenbedarf", "mietminderung", "schadensersatz", "räumung",
            "nebenkosten", "betriebskosten", "wohnungseigentumsgesetz",
            "bgb", "bfh", "bgh", "grundbuch", "auflassung"
        ]
        
        for term in terms:
            if term in text:
                keywords.append(term)
        
        return keywords
    
    async def validate_source(self) -> bool:
        """Verify gesetze-im-internet.de is reachable."""
        try:
            response = requests.head(
                self.base_urls["statutes"],
                timeout=5,
                headers={'User-Agent': 'DOMULEX Legal Research Bot/1.0'}
            )
            is_valid = response.status_code == 200
            if is_valid:
                logger.info("✓ German source validated")
            else:
                logger.warning(f"⚠ German source returned status {response.status_code}")
            return is_valid
        except Exception as e:
            logger.error(f"❌ Cannot reach German source: {e}")
            return False


class SpanishScraper(BaseLegalScraper):
    """
    Scraper for Spanish legal documents.
    
    Sources:
    - BOE.es (Boletín Oficial del Estado) - Official Gazette
    - Código Civil - Civil Code
    - Ley de Arrendamientos Urbanos - Rental Law
    """
    
    def __init__(self):
        super().__init__(Jurisdiction.ES)
        self.boe_api_base = "https://www.boe.es/datosabiertos/api"
        self.boe_search_base = "https://www.boe.es/buscar"
    
    async def fetch(self, max_documents: Optional[int] = None) -> List[LegalDocument]:
        """
        Fetch Spanish legal documents.
        
        Focus areas:
        - Property law (Ley de Propiedad Horizontal)
        - Rental law (LAU - Ley de Arrendamientos Urbanos)
        - Tax law for foreigners (NIE, non-resident tax)
        """
        documents = []
        
        try:
            logger.info("🇪🇸 Fetching Spanish legal documents")
            
            # For MVP, use fallback with known important laws
            # BOE API requires complex authentication and query structure
            documents = self._fetch_spanish_fallback(max_documents or 20)
            
            logger.info(f"✅ Successfully fetched {len(documents)} Spanish documents")
        
        except Exception as e:
            logger.error(f"❌ Error in SpanishScraper: {e}")
        
        self.documents_fetched = documents
        return documents
    
    def _fetch_spanish_fallback(self, limit: int = 20) -> List[LegalDocument]:
        """
        Fallback method using key Spanish laws.
        Used for MVP demonstration.
        """
        logger.info("Using fallback: Fetching key Spanish laws")
        documents = []
        
        # Key Spanish real estate laws
        spanish_laws = [
            {
                "title": "Ley 29/1994 - Ley de Arrendamientos Urbanos (LAU)",
                "article": "Artículo 5",
                "content": "Fianza: A la celebración del contrato, el arrendatario está obligado a entregar al arrendador, en concepto de fianza, una mensualidad de renta en metálico.",
                "url": "https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003",
            },
            {
                "title": "Ley 29/1994 - Ley de Arrendamientos Urbanos (LAU)",
                "article": "Artículo 9",
                "content": "Duración del contrato: La duración del arrendamiento será libremente pactada por las partes. Si fuera inferior a cinco años, el contrato se prorrogará obligatoriamente.",
                "url": "https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003",
            },
            {
                "title": "Ley 29/1994 - Ley de Arrendamientos Urbanos (LAU)",
                "article": "Artículo 10",
                "content": "Desistimiento del arrendatario: El arrendatario puede desistir del contrato, una vez que hayan transcurrido al menos seis meses, con preaviso de treinta días.",
                "url": "https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003",
            },
            {
                "title": "Ley 49/1960 - Ley de Propiedad Horizontal",
                "article": "Artículo 7",
                "content": "Obligaciones de los propietarios: Los propietarios deberán contribuir a los gastos generales para el adecuado sostenimiento del inmueble.",
                "url": "https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906",
            },
            {
                "title": "Real Decreto Legislativo 2/2004 - Texto Refundido de la Ley de Haciendas Locales",
                "article": "IBI (Impuesto sobre Bienes Inmuebles)",
                "content": "El Impuesto sobre Bienes Inmuebles es un tributo directo de carácter real que grava el valor de los bienes inmuebles.",
                "url": "https://www.boe.es/buscar/act.php?id=BOE-A-2004-4214",
            },
            {
                "title": "Código Civil Español",
                "article": "Artículo 1545",
                "content": "El arrendamiento puede ser de cosas, o de obras o servicios. En el arrendamiento de cosas, una de las partes se obliga a dar a la otra el goce o uso de una cosa por tiempo determinado y precio cierto.",
                "url": "https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763",
            },
        ]
        
        for law in spanish_laws[:limit]:
            doc = self._create_document(
                title=f"{law['title']} - {law['article']}",
                content=law['content'],
                source_url=law['url'],
                publication_date=date(2024, 1, 1),  # Generic date
                document_type="statute",
                language="es",
                sub_jurisdiction=None,
                keywords=self._extract_keywords_es(law['title'], law['content']),
            )
            documents.append(doc)
        
        logger.info(f"✓ Loaded {len(documents)} Spanish laws as fallback")
        return documents
    
    def _extract_keywords_es(self, title: str, content: str) -> List[str]:
        """Extract Spanish legal keywords from title and content."""
        keywords = []
        text = f"{title} {content}".lower()
        
        # Common Spanish real estate legal terms
        terms = [
            "arrendador", "arrendatario", "fianza", "lau", "nie",
            "comunidad de propietarios", "propiedad horizontal",
            "desahucio", "ibi", "plusvalía", "escritura",
            "notario", "registro de la propiedad", "hipoteca"
        ]
        
        for term in terms:
            if term in text:
                keywords.append(term.replace(" ", "_"))
        
        return keywords
    
    async def validate_source(self) -> bool:
        """Verify BOE website is accessible."""
        try:
            response = requests.head(
                "https://www.boe.es",
                timeout=5,
                headers={'User-Agent': 'DOMULEX Legal Research Bot/1.0'}
            )
            is_valid = response.status_code == 200
            if is_valid:
                logger.info("✓ Spanish source (BOE) validated")
            else:
                logger.warning(f"⚠ BOE returned status {response.status_code}")
            return is_valid
        except Exception as e:
            logger.error(f"❌ Cannot reach BOE: {e}")
            return False


class USScraper(BaseLegalScraper):
    """
    Scraper for US legal documents.
    
    Sources:
    - CourtListener.com (Federal + State cases)
    - congress.gov (Federal statutes)
    - State-specific sources (Florida Statutes, NY Real Property Law, CA Civil Code)
    """
    
    def __init__(self):
        super().__init__(Jurisdiction.US)
        self.courtlistener_api = "https://www.courtlistener.com/api/rest/v3"
        self.target_states = ["FL", "NY", "CA"]  # MVP focus
        # CourtListener requires API token for higher rate limits
        # For demo, we use public endpoints with lower limits
    
    async def fetch(self, max_documents: Optional[int] = None) -> List[LegalDocument]:
        """
        Fetch US legal documents from CourtListener.
        
        Workflow:
        1. Query CourtListener API for recent opinions
        2. Filter by jurisdiction (Florida, New York, California)
        3. Search for real estate-related keywords
        4. Handle pagination (fetch last 50 rulings)
        5. Map JSON to LegalDocument
        """
        documents = []
        
        try:
            logger.info("🇺🇸 Fetching US legal documents from CourtListener")
            
            # Focus on Florida for MVP (can expand to NY, CA later)
            florida_docs = await self._fetch_opinions_florida(max_documents or 50)
            documents.extend(florida_docs)
            
            logger.info(f"✅ Successfully fetched {len(documents)} US documents")
        
        except Exception as e:
            logger.error(f"❌ Error in USScraper: {e}")
        
        self.documents_fetched = documents
        return documents
    
    async def _fetch_opinions_florida(self, limit: int = 50) -> List[LegalDocument]:
        """
        Fetch Florida court opinions from CourtListener.
        
        Args:
            limit: Maximum number of opinions to fetch
            
        Returns:
            List of LegalDocument objects
        """
        documents = []
        
        try:
            # CourtListener search endpoint
            # Searching for landlord-tenant related cases in Florida
            search_url = f"{self.courtlistener_api}/search/"
            
            params = {
                "type": "o",  # Opinions
                "q": "landlord tenant OR lease OR eviction OR security deposit",
                "court": "fla fladistctapp flaapp flactapp",  # Florida courts
                "order_by": "dateFiled desc",
                "format": "json",
            }
            
            headers = {
                'User-Agent': 'DOMULEX Legal Research Bot/1.0',
                'Accept': 'application/json',
            }
            
            logger.info(f"Querying CourtListener for Florida opinions...")
            
            response = requests.get(
                search_url,
                params=params,
                headers=headers,
                timeout=30,
            )
            
            if response.status_code == 403:
                logger.warning("⚠ CourtListener API requires authentication for search. Using fallback method.")
                return self._fetch_florida_fallback(limit)
            
            response.raise_for_status()
            data = response.json()
            
            results = data.get('results', [])
            logger.info(f"Found {len(results)} results from CourtListener")
            
            for i, result in enumerate(results[:limit]):
                try:
                    # Extract fields from CourtListener JSON
                    case_name = result.get('caseName', 'Untitled Case')
                    court = result.get('court', 'Unknown Court')
                    date_filed = result.get('dateFiled')
                    snippet = result.get('snippet', '')
                    url = result.get('absolute_url', '')
                    
                    # Parse date
                    pub_date = date.today()
                    if date_filed:
                        try:
                            pub_date = datetime.strptime(date_filed, "%Y-%m-%d").date()
                        except Exception as e:
                            logger.warning(f"Could not parse date: {date_filed}")
                    
                    # Construct full URL
                    if url and not url.startswith('http'):
                        url = f"https://www.courtlistener.com{url}"
                    
                    # Create document
                    doc = self._create_document(
                        title=case_name,
                        content=snippet or case_name,
                        source_url=url or "https://www.courtlistener.com",
                        publication_date=pub_date,
                        document_type="case_law",
                        language="en",
                        sub_jurisdiction="Florida",
                        keywords=self._extract_keywords_us(case_name, snippet),
                    )
                    
                    documents.append(doc)
                    logger.debug(f"✓ Extracted: {case_name}")
                
                except Exception as e:
                    logger.error(f"Error parsing CourtListener result: {e}")
                    continue
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error fetching from CourtListener: {e}")
            # Try fallback method
            return self._fetch_florida_fallback(limit)
        except Exception as e:
            logger.error(f"❌ Unexpected error fetching Florida opinions: {e}")
        
        return documents
    
    def _fetch_florida_fallback(self, limit: int = 50) -> List[LegalDocument]:
        """
        Fallback method using static Florida Statutes.
        Used when CourtListener API is unavailable.
        """
        logger.info("Using fallback: Fetching Florida Statutes from public sources")
        documents = []
        
        # Florida Statutes Chapter 83 (Landlord-Tenant)
        florida_statutes = [
            {
                "section": "83.43",
                "title": "Landlord's obligation to maintain premises",
                "url": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0083/Sections/0083.43.html",
            },
            {
                "section": "83.49",
                "title": "Deposit money or advance rent; duty of landlord and tenant",
                "url": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0083/Sections/0083.49.html",
            },
            {
                "section": "83.56",
                "title": "Termination of rental agreement",
                "url": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0083/Sections/0083.56.html",
            },
            {
                "section": "83.60",
                "title": "Defenses to action for rent or possession; procedure",
                "url": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0083/Sections/0083.60.html",
            },
            {
                "section": "83.63",
                "title": "Casualty damage",
                "url": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0083/Sections/0083.63.html",
            },
        ]
        
        for statute in florida_statutes[:limit]:
            doc = self._create_document(
                title=f"Florida Statutes § {statute['section']} - {statute['title']}",
                content=f"Florida Statutes Chapter 83: Landlord and Tenant. Section {statute['section']}: {statute['title']}",
                source_url=statute['url'],
                publication_date=date(2024, 1, 1),  # Generic date for statutes
                document_type="statute",
                language="en",
                sub_jurisdiction="Florida",
                keywords=["florida", "landlord", "tenant", "lease", statute['section']],
            )
            documents.append(doc)
        
        logger.info(f"✓ Loaded {len(documents)} Florida Statutes as fallback")
        return documents
    
    def _extract_keywords_us(self, title: str, content: str) -> List[str]:
        """Extract US legal keywords from title and content."""
        keywords = []
        text = f"{title} {content}".lower()
        
        # Common US real estate legal terms
        terms = [
            "landlord", "tenant", "lease", "eviction", "security deposit",
            "notice to vacate", "fair housing act", "habitability",
            "rent control", "unlawful detainer", "foreclosure",
            "title insurance", "closing", "escrow", "hoa",
            "florida statutes", "real property law"
        ]
        
        for term in terms:
            if term in text:
                keywords.append(term.replace(" ", "_"))
        
        return keywords
    
    async def validate_source(self) -> bool:
        """Verify CourtListener API is accessible."""
        try:
            response = requests.get(
                f"{self.courtlistener_api}/",
                timeout=5,
                headers={'User-Agent': 'DOMULEX Legal Research Bot/1.0'}
            )
            is_valid = response.status_code in [200, 403]  # 403 means API exists but needs auth
            if is_valid:
                logger.info("✓ US source (CourtListener) validated")
            else:
                logger.warning(f"⚠ CourtListener returned status {response.status_code}")
            return is_valid
        except Exception as e:
            logger.error(f"❌ Cannot reach CourtListener: {e}")
            return False


class ScraperFactory:
    """Factory to get the correct scraper for a jurisdiction."""
    
    _scrapers = {
        Jurisdiction.DE: GermanScraper,
        Jurisdiction.ES: SpanishScraper,
        Jurisdiction.US: USScraper,
    }
    
    @classmethod
    def get_scraper(cls, jurisdiction: Jurisdiction) -> BaseLegalScraper:
        """
        Get scraper instance for jurisdiction.
        
        Raises:
            ValueError: If jurisdiction is not supported
        """
        scraper_class = cls._scrapers.get(jurisdiction)
        if not scraper_class:
            raise ValueError(f"No scraper available for jurisdiction: {jurisdiction}")
        
        return scraper_class()
    
    @classmethod
    def get_all_scrapers(cls) -> List[BaseLegalScraper]:
        """Get all available scrapers."""
        return [scraper_class() for scraper_class in cls._scrapers.values()]
