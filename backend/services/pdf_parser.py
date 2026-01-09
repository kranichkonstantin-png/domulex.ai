"""
PDF Contract Parser & Analyzer
Extracts text from PDF contracts and analyzes clauses against legal standards.
Supports OCR for scanned documents.
"""

import io
import logging
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

import fitz  # PyMuPDF
from pydantic import BaseModel, Field
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

from models import Jurisdiction, UserRole


logger = logging.getLogger(__name__)


class RiskLevel(str, Enum):
    """Risk assessment for contract clauses."""
    GREEN = "GREEN"  # Complies with law / favorable
    YELLOW = "YELLOW"  # Potentially problematic
    RED = "RED"  # Likely illegal / highly unfavorable


class ClauseAnalysis(BaseModel):
    """Analysis of a single contract clause."""
    clause_type: str = Field(..., description="Type of clause (e.g., 'Deposit', 'Termination')")
    clause_text: str = Field(..., description="Exact text from PDF")
    risk_level: RiskLevel
    legal_standard: str = Field(..., description="What the law says")
    comparison: str = Field(..., description="How the clause compares to law")
    recommendation: Optional[str] = Field(None, description="Action to take")
    
    # Sources
    source_title: Optional[str] = None
    source_url: Optional[str] = None


class ContractAnalysis(BaseModel):
    """Complete contract analysis result."""
    contract_name: str
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)
    jurisdiction: Jurisdiction
    user_role: UserRole
    
    # Results
    clauses: List[ClauseAnalysis] = Field(default_factory=list)
    overall_risk: RiskLevel = RiskLevel.YELLOW
    summary: str = Field(..., description="Executive summary of findings")
    
    # Metadata
    total_clauses_analyzed: int = 0
    red_flags: int = 0
    yellow_flags: int = 0
    green_flags: int = 0


class PDFParser:
    """
    Extracts text from PDF contracts using PyMuPDF (fitz).
    Falls back to OCR (Tesseract) for scanned documents.
    """
    
    @staticmethod
    def extract_text_with_ocr(pdf_bytes: bytes) -> str:
        """
        Extract text from scanned PDF using OCR (Tesseract).
        
        Args:
            pdf_bytes: Raw PDF file bytes
            
        Returns:
            Extracted text as string
        """
        logger.info("🔍 Using OCR to extract text from scanned PDF...")
        
        try:
            # Convert PDF pages to images
            images = convert_from_bytes(pdf_bytes, dpi=300)
            logger.info(f"📄 Converted PDF to {len(images)} images")
            
            full_text = []
            
            for i, image in enumerate(images):
                # Run OCR on each page (German + English)
                text = pytesseract.image_to_string(image, lang='deu+eng')
                if text.strip():
                    full_text.append(text)
                logger.debug(f"📝 OCR page {i+1}: {len(text)} characters")
            
            extracted = "\n\n".join(full_text).strip()
            logger.info(f"✅ OCR extracted {len(extracted)} characters from {len(images)} pages")
            
            return extracted
            
        except Exception as e:
            logger.error(f"❌ OCR extraction failed: {e}")
            raise ValueError(f"OCR extraction failed: {str(e)}")
    
    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes.
        Falls back to OCR for scanned documents.
        
        Args:
            pdf_bytes: Raw PDF file bytes
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If PDF is corrupted or cannot be read
        """
        try:
            # Open PDF from bytes
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            page_count = pdf_document.page_count
            
            full_text = []
            
            # Extract text from each page
            for page_num in range(page_count):
                page = pdf_document[page_num]
                text = page.get_text("text")
                full_text.append(text)
            
            pdf_document.close()
            
            extracted = "\n\n".join(full_text).strip()
            
            # If no text extracted, try OCR
            if not extracted or len(extracted) < 100:
                logger.info("📄 PDF has little/no extractable text, trying OCR...")
                extracted = PDFParser.extract_text_with_ocr(pdf_bytes)
                
                if not extracted:
                    raise ValueError("Konnte keinen Text aus dem PDF extrahieren (auch nicht mit OCR)")
            
            logger.info(f"✅ Extracted {len(extracted)} characters from PDF ({page_count} pages)")
            
            return extracted
        
        except Exception as e:
            logger.error(f"❌ PDF extraction failed: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def identify_key_clauses(contract_text: str, gemini_model) -> List[Dict[str, str]]:
        """
        Use Gemini to identify key clauses in the contract.
        
        Args:
            contract_text: Full contract text
            gemini_model: Initialized Gemini model
            
        Returns:
            List of identified clauses with type and text
        """
        prompt = f"""
Du bist ein erfahrener Rechtsexperte für Immobilienrecht. Analysiere diesen Vertrag und identifiziere die WICHTIGSTEN KLAUSELN.

Für jede Klausel extrahiere:
1. **type**: Art der Klausel auf Deutsch (z.B. "Kaufpreis", "Übergabetermin", "Gewährleistung", "Kaution", "Kündigungsfrist")
2. **text**: Der exakte Text aus dem Vertrag (mindestens 20-50 Wörter, nicht abkürzen!)

Wichtige Klauseltypen für KAUFVERTRÄGE:
- Kaufpreis und Zahlungsmodalitäten
- Übergabetermin und Besitzübergang
- Gewährleistung und Haftungsausschlüsse
- Grundbucheintragung
- Finanzierungsvorbehalte
- Rücktrittsrechte
- Erschließungskosten
- Instandhaltungsrücklagen (bei WEG)

Wichtige Klauseltypen für MIETVERTRÄGE:
- Miethöhe und Nebenkosten
- Kaution
- Kündigungsfristen
- Schönheitsreparaturen
- Mieterhöhungsklauseln
- Untervermietung

**Vertragstext:**
{contract_text[:8000]}

**Antworte NUR mit validem JSON (kein Markdown, kein zusätzlicher Text):**
[
  {{"type": "Kaufpreis", "text": "Der Kaufpreis für das Vertragsobjekt beträgt EUR 450.000,00 (in Worten: vierhundertfünfzigtausend Euro). Der Kaufpreis ist fällig am Tag der Eigentumsumschreibung im Grundbuch."}},
  {{"type": "Gewährleistung", "text": "Der Verkäufer schließt jegliche Gewährleistung für Sachmängel aus, soweit dies gesetzlich zulässig ist. Der Käufer hat das Objekt besichtigt und kauft es im gegenwärtigen Zustand."}}
]
"""
        
        try:
            response = gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            import json
            clauses = json.loads(response_text)
            
            # Filter out empty clauses
            valid_clauses = [c for c in clauses if c.get("text") and len(c.get("text", "")) > 10]
            
            logger.info(f"✅ Identified {len(valid_clauses)} key clauses")
            return valid_clauses
        
        except Exception as e:
            logger.error(f"❌ Clause identification failed: {e}")
            # Fallback: return empty list
            return []
    
    @staticmethod
    def compare_clause_with_law(
        clause_type: str,
        clause_text: str,
        legal_context: str,
        user_role: UserRole,
        jurisdiction: Jurisdiction,
        gemini_model
    ) -> Dict[str, str]:
        """
        Compare a contract clause against legal standards.
        
        Args:
            clause_type: Type of clause
            clause_text: Exact clause text from contract
            legal_context: Relevant law from Qdrant
            user_role: User's role (TENANT, LANDLORD, etc.)
            jurisdiction: Legal jurisdiction
            gemini_model: Initialized Gemini model
            
        Returns:
            Dict with risk_level, comparison, recommendation
        """
        role_context = {
            UserRole.TENANT: "den Mieter/Käufer",
            UserRole.LANDLORD: "den Vermieter/Verkäufer",
            UserRole.OWNER: "den Eigentümer",
            UserRole.INVESTOR: "den Immobilieninvestor",
            UserRole.MANAGER: "den Verwalter",
        }
        
        prompt = f"""
Du bist ein erfahrener Rechtsanwalt für deutsches Immobilienrecht.

**Aufgabe:** Bewerte diese Vertragsklausel und prüfe sie auf Risiken für {role_context.get(user_role, "den Nutzer")}.

**Klauseltyp:** {clause_type}
**Vertragsklausel:** 
"{clause_text}"

**Relevante Rechtsgrundlage ({jurisdiction.value}):**
{legal_context}

**Analyse-Anweisungen:**
1. **Risikobewertung:** Bewerte als GREEN (rechtskonform/vorteilhaft), YELLOW (potenziell problematisch), oder RED (rechtlich bedenklich/nachteilig)
2. **Vergleich:** Erkläre auf Deutsch, wie die Klausel sich zum geltenden Recht verhält
3. **Empfehlung:** Was sollte der Nutzer tun? (z.B. "Klausel akzeptabel", "Nachverhandeln empfohlen", "Anwaltliche Prüfung ratsam")

**Antworte NUR mit validem JSON:**
{{
  "risk_level": "YELLOW",
  "comparison": "Die Klausel schließt die Gewährleistung vollständig aus. Nach § 444 BGB ist ein Haftungsausschluss für arglistig verschwiegene Mängel jedoch unwirksam.",
  "recommendation": "Lassen Sie vor Unterzeichnung prüfen, ob der Ausschluss alle gesetzlichen Anforderungen erfüllt. Bei älteren Objekten ist ein Gewährleistungsausschluss üblich."
}}
"""
        
        try:
            response = gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            import json
            analysis = json.loads(response_text)
            
            return analysis
        
        except Exception as e:
            logger.error(f"❌ Clause comparison failed: {e}")
            # Fallback
            return {
                "risk_level": "YELLOW",
                "comparison": "Automatische Analyse nicht möglich.",
                "recommendation": "Bitte lassen Sie diese Klausel von einem Rechtsanwalt prüfen."
            }
