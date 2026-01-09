"""
Spanish BOE Scraper - Official Government Gazette
Target: boe.es XML Feed für Housing & Tax Updates
"""

import logging
from typing import List, Dict
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from models.legal import LegalDocument, Jurisdiction
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class SpanishBOEScraper:
    """
    BOE.es (Boletín Oficial del Estado) XML Feed Scraper.
    
    Focus:
    - Ministerio de Transportes (Housing)
    - Ministerio de Hacienda (Tax)
    - IBI, Plusvalía, LAU Updates
    """
    
    BASE_URL = "https://www.boe.es"
    XML_FEED_URL = "https://www.boe.es/diario_boe/xml.php"
    
    # Relevante Ministerien
    RELEVANT_DEPARTMENTS = [
        "Ministerio de Transportes, Movilidad y Agenda Urbana",
        "Ministerio de Hacienda",
        "Ministerio de Justicia"
    ]
    
    # Keywords
    RE_KEYWORDS = [
        "vivienda", "alquiler", "arrendamiento", "inmobiliaria",
        "ibi", "plusvalía", "lau", "propiedad", "hipoteca",
        "catastro", "comunidad de propietarios"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (DOMULEX Legal Bot)"
        })
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def fetch_daily_xml(self, date: datetime) -> str:
        """
        Download BOE XML für bestimmtes Datum.
        
        Format: https://www.boe.es/diario_boe/xml.php?id=BOE-S-2025-247
        """
        # Datum zu BOE-ID konvertieren
        day_of_year = date.timetuple().tm_yday
        boe_id = f"BOE-S-{date.year}-{day_of_year}"
        
        url = f"{self.XML_FEED_URL}?id={boe_id}"
        logger.info(f"📥 Fetching BOE XML: {url}")
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        return response.text
    
    def parse_xml(self, xml_content: str) -> List[Dict]:
        """
        Parse BOE XML und extrahiere relevante Dokumente.
        
        Returns:
            [{"title": "...", "department": "...", "url": "..."}]
        """
        try:
            root = ET.fromstring(xml_content)
            documents = []
            
            # BOE XML Struktur: <sumario><diario><seccion><item>
            for item in root.findall(".//item"):
                title_elem = item.find("titulo")
                dept_elem = item.find("departamento")
                url_elem = item.find("url")
                
                if title_elem is None or url_elem is None:
                    continue
                
                title = title_elem.text or ""
                department = dept_elem.text if dept_elem is not None else ""
                url = url_elem.text or ""
                
                # Filter: Nur relevante Ministerien
                if department not in self.RELEVANT_DEPARTMENTS:
                    continue
                
                documents.append({
                    "title": title,
                    "department": department,
                    "url": self.BASE_URL + url if not url.startswith("http") else url
                })
            
            logger.info(f"📄 Parsed {len(documents)} relevant BOE documents")
            return documents
            
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return []
    
    def is_relevant(self, title: str, department: str) -> bool:
        """Keyword-basierte Relevanz-Prüfung"""
        text = (title + " " + department).lower()
        
        matches = sum(1 for kw in self.RE_KEYWORDS if kw in text)
        
        if matches > 0:
            logger.debug(f"✅ RELEVANT: {title[:50]}")
            return True
        else:
            logger.debug(f"⏭️  SKIP: {title[:50]}")
            return False
    
    def scrape_recent_boe(
        self,
        days_back: int = 7,
        max_docs: int = 30
    ) -> List[LegalDocument]:
        """
        Scrape BOE der letzten N Tage.
        """
        logger.info(f"🇪🇸 BOE Scraper (last {days_back} days)")
        
        documents = []
        
        try:
            # Iteriere über letzte N Tage
            for i in range(days_back):
                if len(documents) >= max_docs:
                    break
                
                target_date = datetime.utcnow() - timedelta(days=i)
                
                try:
                    # XML fetchen
                    xml_content = self.fetch_daily_xml(target_date)
                    boe_docs = self.parse_xml(xml_content)
                    
                    # Filtern und konvertieren
                    for boe_doc in boe_docs:
                        if len(documents) >= max_docs:
                            break
                        
                        # Relevance Check
                        if not self.is_relevant(boe_doc["title"], boe_doc["department"]):
                            continue
                        
                        # LegalDocument erstellen
                        doc = LegalDocument(
                            id=boe_doc["url"].split("/")[-1],
                            jurisdiction=Jurisdiction.ES,
                            sub_jurisdiction="Nacional",
                            title=boe_doc["title"],
                            content_original=f"Departamento: {boe_doc['department']}\n\nTítulo: {boe_doc['title']}",
                            source_url=boe_doc["url"],
                            publication_date=target_date,
                            document_type="BOE Official Gazette",
                            language="es",
                            keywords=[kw for kw in self.RE_KEYWORDS if kw in boe_doc["title"].lower()][:10]
                        )
                        
                        documents.append(doc)
                        logger.info(f"✅ [{len(documents)}] {doc.title[:60]}...")
                
                except Exception as e:
                    logger.warning(f"Fehler bei Datum {target_date.date()}: {e}")
                    continue
            
            logger.info(f"🎉 BOE Scraping done: {len(documents)} docs")
            return documents
            
        except Exception as e:
            logger.error(f"BOE Scraper failed: {e}", exc_info=True)
            return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = SpanishBOEScraper()
    docs = scraper.scrape_recent_boe(days_back=7, max_docs=10)
    
    print(f"\n📊 Results: {len(docs)} documents")
    for doc in docs:
        print(f"  - {doc.title[:80]}")
        print(f"    Keywords: {', '.join(doc.keywords[:3])}\n")
