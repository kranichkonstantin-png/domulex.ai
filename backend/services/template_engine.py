"""
Template Engine für juristische Schriftsätze
KI-gestützte Generierung von Klagen, Mahnungen, Kündigungen etc.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from jinja2 import Template
import google.generativeai as genai

logger = logging.getLogger(__name__)


class FieldDefinition(BaseModel):
    """Definition eines Template-Feldes"""
    name: str
    label: str
    type: str  # "text", "long_text", "date", "amount", "list"
    ai_prompt: str = Field(..., description="Prompt für KI-Generierung")
    required: bool = True
    placeholder: Optional[str] = None


class DocumentTemplate(BaseModel):
    """Juristische Dokumentvorlage"""
    id: str
    name: str
    category: str  # "Mietrecht", "Kaufrecht", "WEG", etc.
    description: str
    icon: str
    fields: List[FieldDefinition]
    template_text: str  # Jinja2 Template


# === TEMPLATE DEFINITIONEN ===

TEMPLATES = {
    "klage_mietrecht": DocumentTemplate(
        id="klage_mietrecht",
        name="Klage (Mietrecht)",
        category="Mietrecht",
        description="Klage vor dem Amtsgericht wegen Mietstreitigkeiten",
        icon="⚖️",
        fields=[
            FieldDefinition(
                name="gericht",
                label="Zuständiges Gericht",
                type="text",
                ai_prompt="Bestimme das zuständige Amtsgericht basierend auf der Objektadresse",
                placeholder="z.B. Amtsgericht München"
            ),
            FieldDefinition(
                name="klaeger_name",
                label="Kläger (Name)",
                type="text",
                ai_prompt="Name des Klägers aus Dokumenten extrahieren",
                placeholder="Max Mustermann"
            ),
            FieldDefinition(
                name="klaeger_adresse",
                label="Kläger (Adresse)",
                type="text",
                ai_prompt="Adresse des Klägers aus Dokumenten extrahieren",
                placeholder="Musterstraße 1, 80331 München"
            ),
            FieldDefinition(
                name="beklagter_name",
                label="Beklagter (Name)",
                type="text",
                ai_prompt="Name des Beklagten aus Dokumenten extrahieren",
                placeholder="Erika Musterfrau"
            ),
            FieldDefinition(
                name="beklagter_adresse",
                label="Beklagter (Adresse)",
                type="text",
                ai_prompt="Adresse des Beklagten aus Dokumenten extrahieren",
                placeholder="Beispielweg 5, 80331 München"
            ),
            FieldDefinition(
                name="sachverhalt",
                label="Sachverhalt",
                type="long_text",
                ai_prompt="Erstelle einen präzisen Sachverhalt basierend auf den hochgeladenen Dokumenten. Relevante Daten, Ereignisse und rechtliche Fakten chronologisch darstellen.",
                placeholder="Beschreibung des Sachverhalts..."
            ),
            FieldDefinition(
                name="antraege",
                label="Klageanträge",
                type="long_text",
                ai_prompt="Formuliere präzise Klageanträge basierend auf dem Sachverhalt. Nummerierte Liste mit konkreten Forderungen.",
                placeholder="1. Der Beklagte wird verurteilt..."
            ),
            FieldDefinition(
                name="begruendung",
                label="Rechtliche Begründung",
                type="long_text",
                ai_prompt="Erstelle eine fundierte rechtliche Begründung mit Bezug auf BGB, Rechtsprechung und Literatur. Nutze RAG für korrekte Paragraphen und Urteile.",
                placeholder="Die Klage ist zulässig und begründet..."
            ),
        ],
        template_text="""AN DAS {{ gericht }}

KLAGE

In der Rechtssache

{{ klaeger_name }}
{{ klaeger_adresse }}
- Kläger -

Prozessbevollmächtigte:
[KANZLEI]

gegen

{{ beklagter_name }}
{{ beklagter_adresse }}
- Beklagter -

wegen [STREITGEGENSTAND]

wird Klage erhoben.

SACHVERHALT:

{{ sachverhalt }}

KLAGEANTRÄGE:

{{ antraege }}

RECHTLICHE BEGRÜNDUNG:

{{ begruendung }}

Mit vorzüglicher Hochachtung

[UNTERSCHRIFT]
Rechtsanwalt/Rechtsanwältin
"""
    ),
    
    "mahnung": DocumentTemplate(
        id="mahnung",
        name="Zahlungsmahnung",
        category="Mietrecht",
        description="Außergerichtliche Mahnung für Mietrückstände",
        icon="💶",
        fields=[
            FieldDefinition(
                name="empfaenger_name",
                label="Empfänger (Name)",
                type="text",
                ai_prompt="Name des Schuldners aus Dokumenten extrahieren"
            ),
            FieldDefinition(
                name="empfaenger_adresse",
                label="Empfänger (Adresse)",
                type="text",
                ai_prompt="Adresse des Schuldners aus Dokumenten extrahieren"
            ),
            FieldDefinition(
                name="betrag",
                label="Forderungsbetrag",
                type="text",
                ai_prompt="Forderungsbetrag aus Dokumenten berechnen (inklusive Verzugszinsen)",
                placeholder="1.500,00 EUR"
            ),
            FieldDefinition(
                name="zeitraum",
                label="Zeitraum der Forderung",
                type="text",
                ai_prompt="Zeitraum der ausstehenden Miete ermitteln",
                placeholder="Januar bis März 2025"
            ),
            FieldDefinition(
                name="zahlungsfrist",
                label="Zahlungsfrist",
                type="date",
                ai_prompt="Setze realistische Zahlungsfrist (7-14 Tage)"
            ),
            FieldDefinition(
                name="konsequenzen",
                label="Rechtliche Konsequenzen",
                type="long_text",
                ai_prompt="Beschreibe rechtliche Konsequenzen bei Nichtzahlung (Kündigung, Räumungsklage, etc.)"
            ),
        ],
        template_text="""{{ empfaenger_name }}
{{ empfaenger_adresse }}

[ORT], {{ datum }}

Betreff: Zahlungserinnerung / Mahnung - Mietrückstände {{ zeitraum }}

Sehr geehrte/r {{ empfaenger_name }},

trotz mehrfacher Aufforderungen sind die Mietzahlungen für den Zeitraum {{ zeitraum }} noch immer ausstehend.

OFFENER BETRAG: {{ betrag }}

Wir fordern Sie hiermit letztmalig auf, den ausstehenden Betrag bis zum {{ zahlungsfrist }} auf folgendes Konto zu überweisen:

[BANKVERBINDUNG]

RECHTLICHE KONSEQUENZEN BEI NICHTZAHLUNG:

{{ konsequenzen }}

Sollten Sie bis zum genannten Termin nicht zahlen, werden wir ohne weitere Ankündigung rechtliche Schritte einleiten.

Mit freundlichen Grüßen

[UNTERSCHRIFT]
"""
    ),
    
    "kuendigung_mieter": DocumentTemplate(
        id="kuendigung_mieter",
        name="Kündigung durch Mieter",
        category="Mietrecht",
        description="Ordentliche Kündigung des Mietverhältnisses durch den Mieter",
        icon="📄",
        fields=[
            FieldDefinition(
                name="vermieter_name",
                label="Vermieter (Name)",
                type="text",
                ai_prompt="Name des Vermieters aus Mietvertrag extrahieren"
            ),
            FieldDefinition(
                name="vermieter_adresse",
                label="Vermieter (Adresse)",
                type="text",
                ai_prompt="Adresse des Vermieters aus Mietvertrag extrahieren"
            ),
            FieldDefinition(
                name="mieter_name",
                label="Mieter (Name)",
                type="text",
                ai_prompt="Name des Mieters aus Mietvertrag extrahieren"
            ),
            FieldDefinition(
                name="objekt_adresse",
                label="Mietobjekt (Adresse)",
                type="text",
                ai_prompt="Adresse des Mietobjekts aus Mietvertrag extrahieren"
            ),
            FieldDefinition(
                name="kuendigungsfrist",
                label="Kündigungsfrist",
                type="text",
                ai_prompt="Kündigungsfrist aus Mietvertrag ermitteln (gesetzlich: 3 Monate zum Monatsende)"
            ),
            FieldDefinition(
                name="kuendigungstermin",
                label="Kündigungstermin",
                type="date",
                ai_prompt="Berechne den frühestmöglichen Kündigungstermin unter Berücksichtigung der Frist"
            ),
        ],
        template_text="""{{ vermieter_name }}
{{ vermieter_adresse }}

[ORT], {{ datum }}

Kündigung des Mietverhältnisses

Sehr geehrte/r {{ vermieter_name }},

hiermit kündige ich, {{ mieter_name }}, das Mietverhältnis über die Wohnung

{{ objekt_adresse }}

ordentlich und fristgerecht zum {{ kuendigungstermin }}.

Die gesetzliche/vertragliche Kündigungsfrist von {{ kuendigungsfrist }} wird eingehalten.

Ich bitte um Bestätigung dieser Kündigung sowie um Terminvereinbarung für die Wohnungsübergabe.

Mit freundlichen Grüßen

{{ mieter_name }}
[UNTERSCHRIFT]
"""
    ),
    
    "maengelanzeige": DocumentTemplate(
        id="maengelanzeige",
        name="Mängelanzeige",
        category="Mietrecht",
        description="Anzeige von Mängeln in der Mietwohnung",
        icon="🔧",
        fields=[
            FieldDefinition(
                name="vermieter_name",
                label="Vermieter (Name)",
                type="text",
                ai_prompt="Name des Vermieters aus Dokumenten"
            ),
            FieldDefinition(
                name="vermieter_adresse",
                label="Vermieter (Adresse)",
                type="text",
                ai_prompt="Adresse des Vermieters"
            ),
            FieldDefinition(
                name="mieter_name",
                label="Mieter (Name)",
                type="text",
                ai_prompt="Name des Mieters"
            ),
            FieldDefinition(
                name="objekt_adresse",
                label="Mietobjekt",
                type="text",
                ai_prompt="Adresse des Mietobjekts"
            ),
            FieldDefinition(
                name="maengel",
                label="Mangelbeschreibung",
                type="long_text",
                ai_prompt="Beschreibe die Mängel detailliert mit Datum der Feststellung, Ort in der Wohnung und Auswirkungen"
            ),
            FieldDefinition(
                name="fristsetzung",
                label="Frist zur Mängelbeseitigung",
                type="text",
                ai_prompt="Setze eine angemessene Frist (7-14 Tage je nach Schwere)",
                placeholder="14 Tage"
            ),
            FieldDefinition(
                name="minderung",
                label="Mietminderung (optional)",
                type="text",
                ai_prompt="Berechne angemessene Mietminderung basierend auf Mängeln und Rechtsprechung",
                required=False,
                placeholder="z.B. 20%"
            ),
        ],
        template_text="""{{ vermieter_name }}
{{ vermieter_adresse }}

[ORT], {{ datum }}

Mängelanzeige gemäß § 536c BGB

Sehr geehrte/r {{ vermieter_name }},

hiermit zeige ich folgende Mängel in der Mietwohnung {{ objekt_adresse }} an:

MANGELBESCHREIBUNG:

{{ maengel }}

Gemäß § 535 Abs. 1 BGB sind Sie verpflichtet, die Mietsache in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu erhalten.

Ich setze Ihnen hiermit eine Frist von {{ fristsetzung }} zur Beseitigung der Mängel.

{% if minderung %}
MIETMINDERUNG:

Aufgrund der erheblichen Beeinträchtigung der Wohnqualität mache ich ab sofort eine Mietminderung von {{ minderung }} geltend, bis die Mängel beseitigt sind.
{% endif %}

Sollten die Mängel nicht fristgerecht beseitigt werden, behalte ich mir rechtliche Schritte vor.

Mit freundlichen Grüßen

{{ mieter_name }}
[UNTERSCHRIFT]
"""
    ),
}


class SchriftsatzGenerator:
    """
    KI-gestützte Generierung juristischer Dokumente.
    Nutzt Gemini 1.5 Pro + RAG für rechtssichere Formulierungen.
    """
    
    def __init__(self, gemini_model, rag_engine):
        self.gemini = gemini_model
        self.rag = rag_engine
    
    async def generate_field_content(
        self,
        field: FieldDefinition,
        context_documents: List[str],
        user_input: Optional[str] = None
    ) -> str:
        """
        Generiert Inhalt für ein Template-Feld mit KI.
        
        Args:
            field: Felddefinition mit AI-Prompt
            context_documents: Liste von hochgeladenen Dokumenten (Text)
            user_input: Optionale Nutzer-Vorgabe
            
        Returns:
            Generierter Text für das Feld
        """
        try:
            # Kombiniere Dokumente
            context = "\n\n===\n\n".join(context_documents) if context_documents else "Keine Dokumente hochgeladen"
            
            # RAG-Query für rechtliche Grundlagen (wenn relevant)
            legal_context = ""
            if field.type == "long_text" and "begründung" in field.name.lower():
                # Hole relevante Rechtsnormen
                rag_result = await self.rag.search(
                    query=f"Rechtliche Grundlagen für {field.label}",
                    top_k=5
                )
                legal_sources = "\n".join([
                    f"- {doc.title}: {doc.content[:200]}..."
                    for doc in rag_result.results[:3]
                ])
                legal_context = f"\n\nRELEVANTE RECHTSNORMEN:\n{legal_sources}"
            
            # Prompt für Gemini
            prompt = f"""Du bist ein erfahrener Rechtsanwalt und erstellst juristische Schriftsätze.

AUFGABE: {field.ai_prompt}

HOCHGELADENE DOKUMENTE:
{context}
{legal_context}

{"NUTZER-VORGABE: " + user_input if user_input else ""}

ANFORDERUNGEN:
- Juristische Präzision
- Formelle Sprache
- Konkrete Fakten aus Dokumenten
- Bei Beträgen: Exakte Zahlen
- Bei Daten: Format TT.MM.YYYY
- Bei Fristen: Realistisch (7-14 Tage)
- Bei Begründungen: Paragraphen-Bezüge (BGB, ZPO)

Generiere NUR den Feldinhalt, keine Erklärungen."""

            response = self.gemini.generate_content(prompt)
            generated = response.text.strip()
            
            logger.info(f"✅ Generated field '{field.name}': {len(generated)} chars")
            
            return generated
        
        except Exception as e:
            logger.error(f"Field generation failed for '{field.name}': {e}")
            return f"[Fehler bei der Generierung: {str(e)}]"
    
    async def generate_document(
        self,
        template_id: str,
        field_values: Dict[str, str],
        context_documents: Optional[List[str]] = None
    ) -> str:
        """
        Generiert vollständiges Dokument aus Template + Feldwerten.
        
        Args:
            template_id: ID der Vorlage (z.B. "klage_mietrecht")
            field_values: Dict mit Feldnamen → Werte
            context_documents: Optionale Dokumente für KI-Generierung
            
        Returns:
            Vollständig generiertes Dokument als Text
        """
        try:
            if template_id not in TEMPLATES:
                raise ValueError(f"Template '{template_id}' nicht gefunden")
            
            template = TEMPLATES[template_id]
            
            # Füge Standardwerte hinzu
            values = {
                "datum": datetime.now().strftime("%d.%m.%Y"),
                **field_values
            }
            
            # Auto-Generierung für leere Felder
            if context_documents:
                for field in template.fields:
                    if field.name not in values or not values[field.name]:
                        logger.info(f"🤖 Auto-generating field: {field.name}")
                        values[field.name] = await self.generate_field_content(
                            field=field,
                            context_documents=context_documents
                        )
            
            # Rendere Jinja2 Template
            jinja_template = Template(template.template_text)
            rendered = jinja_template.render(**values)
            
            logger.info(f"✅ Document generated: {template.name} ({len(rendered)} chars)")
            
            return rendered
        
        except Exception as e:
            logger.error(f"Document generation failed: {e}", exc_info=True)
            raise


# === API MODELS ===

class GenerateFieldRequest(BaseModel):
    """Request für einzelne Feld-Generierung"""
    template_id: str
    field_name: str
    context_documents: Optional[List[str]] = Field(default_factory=list)
    user_input: Optional[str] = None


class GenerateFieldResponse(BaseModel):
    """Response für Feld-Generierung"""
    success: bool
    field_name: str
    generated_content: Optional[str] = None
    error: Optional[str] = None


class GenerateDocumentRequest(BaseModel):
    """Request für vollständige Dokumentgenerierung"""
    template_id: str
    field_values: Dict[str, str] = Field(default_factory=dict)
    context_documents: Optional[List[str]] = Field(default_factory=list)


class GenerateDocumentResponse(BaseModel):
    """Response für Dokumentgenerierung"""
    success: bool
    template_name: Optional[str] = None
    generated_document: Optional[str] = None
    error: Optional[str] = None


# Singleton instance (wird in main.py initialisiert)
schriftsatz_generator = None
