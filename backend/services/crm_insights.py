"""
CRM AI Insights Service - Generate AI-powered insights for clients and cases
"""

import logging
from typing import List, Optional
from datetime import datetime

import google.generativeai as genai

logger = logging.getLogger(__name__)


class CRMInsightsService:
    """Generate AI insights for CRM data."""
    
    def __init__(self, gemini_api_key: str):
        """Initialize the insights service."""
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    async def generate_client_summary(
        self,
        client_name: str,
        case_type: Optional[str],
        notes: Optional[str],
        case_notes: List[str]
    ) -> str:
        """Generate AI summary for a client."""
        try:
            context = f"""Mandant: {client_name}
Fallart: {case_type or 'Nicht angegeben'}

Notizen:
{notes or 'Keine Notizen'}

Aktennotizen:
{chr(10).join(f'- {note}' for note in case_notes[:10]) if case_notes else 'Keine Aktennotizen'}
"""
            
            prompt = f"""Erstelle eine prägnante, professionelle Zusammenfassung (max. 3-4 Sätze) für diesen Mandanten:

{context}

Die Zusammenfassung soll die wichtigsten Aspekte des Falls hervorheben und für einen Anwalt schnell erfassbar sein."""

            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            logger.error(f"Failed to generate client summary: {e}")
            return f"Mandant: {client_name} - {case_type or 'Allgemein'}"
    
    async def generate_case_analysis(
        self,
        client_name: str,
        case_type: str,
        case_description: str,
        case_notes: List[str]
    ) -> dict:
        """
        Generate comprehensive case analysis with strategic recommendations.
        
        Returns:
            dict with keys: analysis, strengths, weaknesses, recommendations, next_steps
        """
        try:
            context = f"""FALLANALYSE FÜR: {client_name}

FALLART: {case_type}

FALLBESCHREIBUNG:
{case_description}

AKTENNOTIZEN:
{chr(10).join(f'{i+1}. {note}' for i, note in enumerate(case_notes))}
"""
            
            prompt = f"""{context}

Als spezialisierter Rechtsanwalt für Immobilienrecht, analysiere diesen Fall umfassend:

1. FALLANALYSE (2-3 Sätze): Kernproblem und rechtliche Einordnung

2. STÄRKEN (3-5 Punkte): Was spricht für unseren Mandanten?

3. SCHWÄCHEN/RISIKEN (3-5 Punkte): Welche Risiken gibt es?

4. STRATEGIEEMPFEHLUNG (3-5 Punkte): Konkrete Handlungsempfehlungen

5. NÄCHSTE SCHRITTE (3-5 Punkte): Sofortige Maßnahmen

Antworte in professioneller, präziser Form."""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Parse response into sections
            sections = {
                'analysis': '',
                'strengths': [],
                'weaknesses': [],
                'recommendations': [],
                'next_steps': []
            }
            
            current_section = None
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                if 'FALLANALYSE' in line.upper():
                    current_section = 'analysis'
                    continue
                elif 'STÄRKEN' in line.upper():
                    current_section = 'strengths'
                    continue
                elif 'SCHWÄCHEN' in line.upper() or 'RISIKEN' in line.upper():
                    current_section = 'weaknesses'
                    continue
                elif 'STRATEGIE' in line.upper():
                    current_section = 'recommendations'
                    continue
                elif 'NÄCHSTE SCHRITTE' in line.upper() or 'MASSNAHMEN' in line.upper():
                    current_section = 'next_steps'
                    continue
                
                # Add content to current section
                if current_section == 'analysis':
                    sections['analysis'] += line + ' '
                elif current_section in ['strengths', 'weaknesses', 'recommendations', 'next_steps']:
                    # Remove bullet points and numbering
                    cleaned = line.lstrip('-•*123456789. ')
                    if cleaned:
                        sections[current_section].append(cleaned)
            
            # Clean up analysis
            sections['analysis'] = sections['analysis'].strip()
            
            return sections
        
        except Exception as e:
            logger.error(f"Failed to generate case analysis: {e}")
            return {
                'analysis': 'Fehler bei der Analyse. Bitte versuchen Sie es erneut.',
                'strengths': [],
                'weaknesses': [],
                'recommendations': [],
                'next_steps': []
            }
    
    async def generate_risk_assessment(
        self,
        client_name: str,
        case_type: str,
        case_description: str
    ) -> str:
        """Generate risk assessment for a client/case."""
        try:
            prompt = f"""Bewerte das Risiko dieses Falls auf einer Skala von 1-10:

Mandant: {client_name}
Fallart: {case_type}
Beschreibung: {case_description}

Gib eine kurze Risikobewertung (1-2 Sätze) mit Risiko-Score (1=sehr niedrig, 10=sehr hoch):
Format: "RISIKO: [Score]/10 - [Begründung]"
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            logger.error(f"Failed to generate risk assessment: {e}")
            return "RISIKO: Nicht bewertet"
    
    async def suggest_next_steps(
        self,
        case_type: str,
        current_status: str,
        case_notes: List[str]
    ) -> List[str]:
        """Suggest next steps for a case based on current state."""
        try:
            context = f"""Fallart: {case_type}
Status: {current_status}

Letzte Entwicklungen:
{chr(10).join(f'- {note}' for note in case_notes[-5:])}
"""
            
            prompt = f"""{context}

Schlage 3-5 konkrete nächste Schritte vor, die ein Anwalt in diesem Fall unternehmen sollte.
Antworte nur mit den Schritten, jeweils auf einer neuen Zeile mit "- " am Anfang."""

            response = self.model.generate_content(prompt)
            
            # Parse steps
            steps = []
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    cleaned = line.lstrip('-•*123456789. ')
                    if cleaned:
                        steps.append(cleaned)
            
            return steps[:5]  # Max 5 steps
        
        except Exception as e:
            logger.error(f"Failed to suggest next steps: {e}")
            return ["Fehler bei der Generierung von Vorschlägen"]
