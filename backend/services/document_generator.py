"""
Legal Document Generator Service
Generates legal documents and templates for lawyers
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum
import google.generativeai as genai
from datetime import date


class DocumentType(str, Enum):
    """Types of legal documents to generate."""
    KLAGE = "KLAGE"  # Lawsuit
    MAHNUNG = "MAHNUNG"  # Dunning letter
    KUENDIGUNG = "KUENDIGUNG"  # Termination notice
    WIDERSPRUCH = "WIDERSPRUCH"  # Objection
    VOLLMACHT = "VOLLMACHT"  # Power of attorney
    FRISTSETZUNG = "FRISTSETZUNG"  # Deadline notice
    MAENGELANZEIGE = "MAENGELANZEIGE"  # Defect notice
    MIETMINDERUNG = "MIETMINDERUNG"  # Rent reduction notice
    EINSPRUCH = "EINSPRUCH"  # Appeal
    SCHRIFTSATZ = "SCHRIFTSATZ"  # Legal brief


class DocumentRequest(BaseModel):
    """Request to generate a legal document."""
    document_type: DocumentType
    case_summary: str = Field(..., description="Summary of the legal case/situation")
    party_plaintiff: str = Field(..., description="Name of plaintiff/sender")
    party_defendant: str = Field(..., description="Name of defendant/recipient")
    legal_basis: Optional[str] = Field(None, description="Legal basis (e.g., § 543 BGB)")
    deadline_days: Optional[int] = Field(None, description="Deadline in days")
    amount: Optional[float] = Field(None, description="Amount in EUR if applicable")
    additional_info: Optional[str] = Field(None, description="Any additional information")


class GeneratedDocument(BaseModel):
    """Generated legal document."""
    document_type: str
    title: str
    content: str
    legal_notes: str
    next_steps: Optional[str] = None


class DocumentGenerator:
    """Service to generate legal documents and templates."""
    
    def __init__(self, gemini_api_key: str):
        """Initialize with Gemini API key."""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_document(self, request: DocumentRequest) -> GeneratedDocument:
        """
        Generate a legal document based on the request.
        
        Uses Gemini to create a professionally formatted legal document
        following German legal standards.
        """
        
        prompt = self._build_generation_prompt(request)
        
        try:
            response = self.model.generate_content(prompt)
            generated_text = response.text
            
            # Parse response into sections
            title, content, legal_notes, next_steps = self._parse_generated_document(
                generated_text, 
                request.document_type
            )
            
            return GeneratedDocument(
                document_type=request.document_type.value,
                title=title,
                content=content,
                legal_notes=legal_notes,
                next_steps=next_steps
            )
            
        except Exception as e:
            raise Exception(f"Document generation failed: {str(e)}")
    
    def _build_generation_prompt(self, request: DocumentRequest) -> str:
        """Build the prompt for document generation."""
        
        document_specs = {
            DocumentType.KLAGE: {
                "name": "Klage",
                "structure": "1) Rubrum, 2) Sachverhalt, 3) Rechtliche Würdigung, 4) Antrag",
                "tone": "formal, präzise, juristisch"
            },
            DocumentType.MAHNUNG: {
                "name": "Mahnung",
                "structure": "1) Anrede, 2) Forderung, 3) Fristsetzung, 4) Androhung rechtlicher Schritte",
                "tone": "bestimmt aber höflich"
            },
            DocumentType.KUENDIGUNG: {
                "name": "Kündigung",
                "structure": "1) Kündigungserklärung, 2) Kündigungsgrund, 3) Kündigungsfrist, 4) Rückgabeverlangen",
                "tone": "formal, eindeutig"
            },
            DocumentType.WIDERSPRUCH: {
                "name": "Widerspruch",
                "structure": "1) Widerspruchserklärung, 2) Begründung, 3) Beweismittel, 4) Fristsetzung",
                "tone": "bestimmt, argumentativ"
            },
            DocumentType.MAENGELANZEIGE: {
                "name": "Mängelanzeige",
                "structure": "1) Beschreibung Mangel, 2) Fristsetzung Beseitigung, 3) Androhung Mietminderung/Selbstvornahme",
                "tone": "sachlich, präzise"
            },
            DocumentType.MIETMINDERUNG: {
                "name": "Mietminderungsanzeige",
                "structure": "1) Mangelbeschreibung, 2) Minderungsquote, 3) Rechtliche Grundlage, 4) Rückforderung",
                "tone": "sachlich, begründet"
            },
            DocumentType.SCHRIFTSATZ: {
                "name": "Schriftsatz",
                "structure": "1) Rubrum, 2) Sachvortrag, 3) Rechtliche Würdigung, 4) Antrag/Stellungnahme",
                "tone": "formal, juristisch präzise"
            }
        }
        
        spec = document_specs.get(request.document_type, document_specs[DocumentType.SCHRIFTSATZ])
        
        today = date.today().strftime("%d.%m.%Y")
        
        prompt = f"""Du bist ein erfahrener Fachanwalt für Miet- und Immobilienrecht in Deutschland.

Erstelle ein rechtssicheres {spec['name']} gemäß den folgenden Vorgaben:

**DOKUMENTTYP:** {spec['name']}
**STRUKTUR:** {spec['structure']}
**TONALITÄT:** {spec['tone']}

**FALL-DETAILS:**
- Absender/Mandant: {request.party_plaintiff}
- Empfänger/Gegner: {request.party_defendant}
- Sachverhalt: {request.case_summary}
"""

        if request.legal_basis:
            prompt += f"- Rechtsgrundlage: {request.legal_basis}\n"
        
        if request.amount:
            prompt += f"- Betrag: {request.amount:.2f} EUR\n"
        
        if request.deadline_days:
            prompt += f"- Frist: {request.deadline_days} Tage\n"
        
        if request.additional_info:
            prompt += f"- Zusätzliche Informationen: {request.additional_info}\n"
        
        prompt += f"""
**DATUM:** {today}

**ANFORDERUNGEN:**
1. Vollständiges, druckfertiges Dokument
2. Korrekte juristische Formulierungen
3. Konkrete Rechtsgrundlagen zitieren (z.B. § 543 BGB, § 535 BGB)
4. Fristen eindeutig benennen
5. Alle relevanten Beweismittel erwähnen
6. Professionelle Formatierung

**AUSGABEFORMAT:**
Gib das Dokument in folgendem Format aus:

===TITEL===
[Dokumententitel, z.B. "Kündigung des Mietverhältnisses"]

===DOKUMENT===
[Vollständiges Dokument mit allen Formalia]

===RECHTSHINWEISE===
[Wichtige rechtliche Hinweise für den Mandanten]

===NÄCHSTE SCHRITTE===
[Was sollte als nächstes getan werden]

Erstelle jetzt das {spec['name']}:
"""
        
        return prompt
    
    def _parse_generated_document(
        self, 
        text: str, 
        doc_type: DocumentType
    ) -> tuple[str, str, str, str]:
        """Parse the generated text into structured sections."""
        
        # Split by section markers
        sections = {}
        current_section = None
        current_content = []
        
        for line in text.split('\n'):
            if line.startswith('===') and line.endswith('==='):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.strip('=').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Add last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Extract sections
        title = sections.get('TITEL', f'{doc_type.value} - Entwurf')
        content = sections.get('DOKUMENT', text)  # Fallback to full text
        legal_notes = sections.get('RECHTSHINWEISE', 'Keine weiteren Hinweise.')
        next_steps = sections.get('NÄCHSTE SCHRITTE', None)
        
        return title, content, legal_notes, next_steps
