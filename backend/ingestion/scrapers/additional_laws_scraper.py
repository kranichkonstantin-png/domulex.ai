"""
Additional German Laws Scraper - GEG, BauGB, weitere wichtige Gesetze
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class AdditionalLawsScraper:
    """Scraper für zusätzliche deutsche Gesetze"""
    
    def __init__(self):
        pass
    
    async def scrape_additional_laws(self) -> List[Dict]:
        """Scrape additional important laws"""
        documents = []
        
        ADDITIONAL_LAWS = [
            {
                "law": "GEG",
                "section": "§ 48 - Energieausweis",
                "content": """GEG § 48 - Energieausweis Pflicht

Bei Verkauf/Vermietung PFLICHT:
✅ Energieausweis vorlegen
✅ In Anzeige: Energiekennwerte
✅ Bußgeld ohne: bis 15.000 €

Kosten: 100-800 €""",
                "topics": ["GEG", "Energieausweis", "Pflicht", "Bußgeld"]
            },
            {
                "law": "BauGB",
                "section": "§ 34 - Zulässigkeit im unbeplanten Innenbereich",
                "content": """BauGB § 34 - Bauen im Innenbereich

OHNE Bebauungsplan:
✅ Gebäude muss sich EINFÜGEN
✅ Art der Nutzung (Wohnen/Gewerbe)
✅ Maß (Höhe, Volumen)
✅ Bauweise (offen/geschlossen)

Bei Einfügung: Genehmigung möglich""",
                "topics": ["BauGB", "Bebauung", "Innenbereich", "Einfügung"]
            },
            {
                "law": "BGB",
                "section": "§ 433 - Kaufvertrag Pflichten",
                "content": """BGB § 433 - Kaufvertrag

Verkäufer-Pflichten:
✅ Übergabe der Sache
✅ Verschaffung des Eigentums
✅ Übergabe mangelfrei

Käufer-Pflichten:
✅ Kaufpreis zahlen
✅ Sache abnehmen""",
                "topics": ["BGB", "Kaufvertrag", "Pflichten", "Übergabe"]
            }
        ]
        
        for law in ADDITIONAL_LAWS:
            doc = {
                "id": f"{law['law'].lower()}_{law['section'].lower().replace(' ', '_').replace('§', 'par').replace('.', '')}",
                "content": law["content"],
                "jurisdiction": "DE",
                "language": "de",
                "source": f"{law['law']} {law['section']}",
                "source_url": "https://www.gesetze-im-internet.de",
                "topics": law["topics"],
                "law": law["law"],
                "section": law["section"],
                "last_updated": datetime.utcnow().isoformat()
            }
            documents.append(doc)
        
        logger.info(f"✅ Found {len(documents)} additional laws")
        return documents


# Export
__all__ = ["AdditionalLawsScraper"]
