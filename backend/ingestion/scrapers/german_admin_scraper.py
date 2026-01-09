"""
German Administrative Scraper - The Investor Value Add
Target: Bundesfinanzministerium (BMF) Tax Circulars

CRITICAL für Investoren:
- AfA-Regeln (Abschreibung)
- Grundsteuer-Updates
- Bauabzug-Vorschriften
- Vermietungs-Besteuerung
"""

import logging
import hashlib
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path
import io

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
import PyMuPDF  # fitz

from models.legal import LegalDocument, Jurisdiction
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GermanAdminScraper:
    """
    Scraper für BMF-Schreiben (Tax Circulars).
    
    Workflow:
    1. Scrape BMF-Website für neue PDFs
    2. Keyword-Filtering (nur Real Estate relevante)
    3. PDF → Text Extraktion
    4. Dedup via Hash
    5. Return LegalDocument objects
    """
    
    BASE_URL = "https://www.bundesfinanzministerium.de"
    SEARCH_ENDPOINT = "/Content/DE/Standardartikel/Themen/Steuern/steuerschreiben-a-z.html"
    
    # Investor-relevante Keywords
    REAL_ESTATE_KEYWORDS = [
        "immobilien",
        "grundsteuer",
        "grundstück",
        "afa",  # Absetzung für Abnutzung
        "abschreibung",
        "gebäude",
        "vermietung",
        "verpachtung",
        "bauabzug",
        "bauträger",
        "wohnung",
        "eigentum",
        "invest"
    ]
    
    def __init__(self, cache_dir: Path = Path("/app/cache/bmf_pdfs")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (DOMULEX Legal Intelligence Bot)"
        })
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def fetch_page(self, url: str) -> str:
        """HTTP GET mit Retry-Logic"""
        logger.info(f"🌐 Fetching: {url}")
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def fetch_pdf(self, url: str) -> bytes:
        """Download PDF mit Retry-Logic"""
        logger.info(f"📄 Downloading PDF: {url}")
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        return response.content
    
    def extract_pdf_links(self, html: str) -> List[Dict[str, str]]:
        """
        Parse HTML für PDF-Links.
        
        Returns:
            [{"url": "...", "title": "...", "date": "..."}]
        """
        soup = BeautifulSoup(html, "lxml")
        pdf_links = []
        
        # BMF-Website Struktur: Links in <a> Tags mit .pdf Extension
        for link in soup.find_all("a", href=True):
            href = link["href"]
            
            if not href.endswith(".pdf"):
                continue
            
            # Relative URLs zu Absolute konvertieren
            if not href.startswith("http"):
                href = self.BASE_URL + href
            
            # Titel extrahieren
            title = link.get_text(strip=True)
            
            # Datum extrahieren (falls vorhanden)
            date_str = None
            date_elem = link.find_parent("div", class_="date")
            if date_elem:
                date_str = date_elem.get_text(strip=True)
            
            pdf_links.append({
                "url": href,
                "title": title,
                "date": date_str
            })
        
        logger.info(f"🔗 Found {len(pdf_links)} PDF links")
        return pdf_links
    
    def is_relevant(self, title: str, text: str = "") -> bool:
        """
        Quick Keyword-Check BEVOR PDF-Download.
        Spart Bandbreite und Zeit.
        """
        content = (title + " " + text).lower()
        
        matches = sum(1 for kw in self.REAL_ESTATE_KEYWORDS if kw in content)
        
        if matches > 0:
            logger.info(f"✅ RELEVANT ({matches} keywords): {title[:60]}...")
            return True
        else:
            logger.debug(f"⏭️  SKIP (irrelevant): {title[:60]}...")
            return False
    
    def pdf_to_text(self, pdf_bytes: bytes) -> str:
        """
        PDF → Text Extraktion mit PyMuPDF.
        Robuster als pypdf2 für deutsche Umlaute.
        """
        try:
            # PDF in Memory öffnen
            pdf_stream = io.BytesIO(pdf_bytes)
            doc = PyMuPDF.open(stream=pdf_stream, filetype="pdf")
            
            text_parts = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_parts.append(text)
            
            doc.close()
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"📖 Extracted {len(full_text)} characters from PDF")
            
            return full_text
            
        except Exception as e:
            logger.error(f"PDF-Extraktion fehlgeschlagen: {e}")
            return ""
    
    def compute_pdf_hash(self, pdf_bytes: bytes) -> str:
        """SHA256 Hash für Dedup"""
        return hashlib.sha256(pdf_bytes).hexdigest()
    
    def is_cached(self, pdf_hash: str) -> bool:
        """Prüft ob PDF bereits verarbeitet wurde"""
        cache_file = self.cache_dir / f"{pdf_hash}.txt"
        return cache_file.exists()
    
    def cache_pdf_text(self, pdf_hash: str, text: str):
        """Speichere extrahierten Text"""
        cache_file = self.cache_dir / f"{pdf_hash}.txt"
        cache_file.write_text(text, encoding="utf-8")
    
    def get_cached_text(self, pdf_hash: str) -> Optional[str]:
        """Lade gecacheten Text"""
        cache_file = self.cache_dir / f"{pdf_hash}.txt"
        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")
        return None
    
    def scrape_recent_bmf_circulars(
        self,
        days_back: int = 30,
        max_documents: int = 50
    ) -> List[LegalDocument]:
        """
        Hauptfunktion: Scrape BMF-Schreiben der letzten N Tage.
        
        Args:
            days_back: Wie weit zurück suchen
            max_documents: Max. Anzahl Dokumente
            
        Returns:
            List von LegalDocument Objekten
        """
        logger.info(f"🇩🇪 Starting BMF Scraper (last {days_back} days, max {max_documents} docs)")
        
        documents = []
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        try:
            # Step 1: Website scrapen
            html = self.fetch_page(self.BASE_URL + self.SEARCH_ENDPOINT)
            pdf_links = self.extract_pdf_links(html)
            
            # Step 2: PDFs verarbeiten
            for i, pdf_info in enumerate(pdf_links):
                if len(documents) >= max_documents:
                    logger.info(f"📊 Limit erreicht: {max_documents} Dokumente")
                    break
                
                # Quick Relevance Check BEVOR Download
                if not self.is_relevant(pdf_info["title"]):
                    continue
                
                try:
                    # Download PDF
                    pdf_bytes = self.fetch_pdf(pdf_info["url"])
                    pdf_hash = self.compute_pdf_hash(pdf_bytes)
                    
                    # Dedup Check
                    if self.is_cached(pdf_hash):
                        logger.info(f"✅ CACHED: {pdf_info['title'][:50]}...")
                        text = self.get_cached_text(pdf_hash)
                    else:
                        # Extrahiere Text
                        text = self.pdf_to_text(pdf_bytes)
                        
                        if not text or len(text) < 100:
                            logger.warning(f"⚠️  PDF leer oder zu kurz: {pdf_info['title']}")
                            continue
                        
                        # Cache speichern
                        self.cache_pdf_text(pdf_hash, text)
                    
                    # Final Relevance Check (jetzt mit vollem Text)
                    if not self.is_relevant(pdf_info["title"], text):
                        continue
                    
                    # Extract Keywords aus Text
                    keywords = [
                        kw for kw in self.REAL_ESTATE_KEYWORDS
                        if kw in text.lower()
                    ]
                    
                    # Datum parsen
                    pub_date = datetime.utcnow()  # Fallback
                    if pdf_info["date"]:
                        try:
                            # Format: "15.12.2025"
                            pub_date = datetime.strptime(pdf_info["date"], "%d.%m.%Y")
                        except ValueError:
                            pass
                    
                    # LegalDocument erstellen
                    doc = LegalDocument(
                        id=pdf_hash,
                        jurisdiction=Jurisdiction.DE,
                        sub_jurisdiction="Bundesebene",
                        title=pdf_info["title"],
                        content_original=text,
                        source_url=pdf_info["url"],
                        publication_date=pub_date,
                        document_type="BMF Tax Circular",
                        language="de",
                        keywords=keywords[:10],  # Top 10
                    )
                    
                    documents.append(doc)
                    logger.info(f"✅ [{len(documents)}/{max_documents}] {doc.title[:60]}...")
                    
                except Exception as e:
                    logger.error(f"Fehler bei PDF {pdf_info['url']}: {e}")
                    continue
            
            logger.info(f"🎉 BMF Scraping abgeschlossen: {len(documents)} relevante Dokumente")
            return documents
            
        except Exception as e:
            logger.error(f"BMF Scraper fehlgeschlagen: {e}", exc_info=True)
            return []


# Standalone Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    scraper = GermanAdminScraper()
    docs = scraper.scrape_recent_bmf_circulars(days_back=90, max_documents=10)
    
    print(f"\n📊 Results: {len(docs)} documents")
    for doc in docs:
        print(f"  - {doc.title}")
        print(f"    Keywords: {', '.join(doc.keywords[:5])}")
        print(f"    Length: {len(doc.content_original)} chars\n")
