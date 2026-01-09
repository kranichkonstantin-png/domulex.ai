#!/usr/bin/env python3
"""
Fill templates with sample data for demonstration purposes.
Maintains the rigid form structure but with filled-in examples.
"""

import re
from datetime import datetime, timedelta

# Sample data mappings
REPLACEMENTS = {
    # Personal data - Mieter
    r'\[Ihr Name\]': 'Max Mustermann',
    r'\[Ihre Adresse\]': 'Musterstraße 12',
    r'\[PLZ Ort\]': '12345 Berlin',
    
    # Personal data - Vermieter
    r'\[Name des Vermieters\]': 'Immobilien Schmidt GmbH',
    r'\[Adresse des Vermieters\]': 'Hausverwaltung Straße 5',
    r'\[Name Vermieter\]': 'Schmidt Immobilien GmbH',
    r'\[Adresse Vermieter\]': 'Verwaltungsweg 20, 10115 Berlin',
    
    # Personal data - General parties
    r'\[Name Mieter\]': 'Anna Müller',
    r'\[Adresse Mieter\]': 'Wohnstraße 7, 80331 München',
    r'\[Name Eigentümer\]': 'Thomas Wagner',
    r'\[Name/Firma Vermieter\]': 'Hausverwaltung Meyer GmbH',
    r'\[Firma/Name Vermieter\]': 'Gewerbeimmobilien Nord GmbH',
    
    # Lawyer/Professional data
    r'\[Kanzlei-Briefkopf\]': 'Rechtsanwaltskanzlei Dr. Schneider & Partner\nBahnhofstraße 45, 60329 Frankfurt\nTel: 069/12345678, Fax: 069/12345679\nmail@ra-schneider.de',
    r'\[Kanzleiname\]': 'Rechtsanwaltskanzlei Dr. Schneider & Partner',
    r'\[Name der Kanzlei\]': 'Rechtsanwaltskanzlei Weber & Kollegen',
    r'\[Name/Firma Auftraggeber\]': 'Bau-AG Mustermann',
    r'\[Name/Firma Auftragnehmer\]': 'Handwerksbetrieb Schmidt GmbH',
    
    # Addresses
    r'\[Mietadresse\]': 'Musterstraße 12, 12345 Berlin',
    r'\[Adresse\]': 'Hauptstraße 15, 50667 Köln',
    r'\[Objektbezeichnung\]': 'Wohnanlage Parkblick',
    
    # Dates
    r'\[Ort\], den \[Datum\]': f'Berlin, den {datetime.now().strftime("%d.%m.%Y")}',
    r'\[Datum\]': (datetime.now() + timedelta(days=30)).strftime('%d.%m.%Y'),
    r'\[Ort\]': 'Berlin',
    
    # Money amounts
    r'\[Betrag\] €': '850,00 €',
    r'\[___\] €': '1.200,00 €',
    r'\[Miethöhe\]': '950,00 €',
    
    # Numbers and quantities
    r'\[Anzahl\]': '2',
    r'\[___\]': '3',
    
    # Court/Legal
    r'\[Aktenzeichen\]': '12 C 345/24',
    r'\[Gericht\]': 'Amtsgericht Berlin-Mitte',
    
    # Property details
    r'\[Quadratmeter\]': '75',
    r'\[Stockwerk\]': '3. OG',
    r'\[Zimmer\]': '3',
    
    # Account details
    r'\[IBAN\]': 'DE89 3704 0044 0532 0130 00',
    r'\[Kontoinhaber\]': 'Schmidt Immobilien GmbH',
    
    # Specific descriptions
    r'\[Beschreibung des Mangels\]': 'Schimmelbildung im Badezimmer an der Decke (ca. 30x40 cm)',
    r'\[Beschreibung der Mängel\]': 'Heizung funktioniert nicht ordnungsgemäß, Raumtemperatur unter 18°C',
}

def fill_templates():
    file_path = "src/app/app/templates/page.tsx"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply all replacements
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Count changes
    changes = sum(1 for p in REPLACEMENTS if re.search(p, original))
    
    print(f"✅ Filled templates with sample data")
    print(f"   Applied {len(REPLACEMENTS)} replacement patterns")
    print(f"   Found and replaced {changes} different placeholder types")

if __name__ == "__main__":
    fill_templates()
