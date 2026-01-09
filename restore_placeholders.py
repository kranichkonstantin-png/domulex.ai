#!/usr/bin/env python3
"""
Restore placeholders in templates for AI-based dynamic filling.
"""

import re

# Reverse mappings - replace sample data back to placeholders
REVERSE_REPLACEMENTS = {
    # Personal data - Mieter
    r'Max Mustermann': '[Ihr Name]',
    r'Musterstraße 12': '[Ihre Adresse]',
    r'12345 Berlin': '[PLZ Ort]',
    
    # Personal data - Vermieter
    r'Immobilien Schmidt GmbH': '[Name des Vermieters]',
    r'Hausverwaltung Straße 5': '[Adresse des Vermieters]',
    r'Schmidt Immobilien GmbH': '[Name Vermieter]',
    r'Verwaltungsweg 20, 10115 Berlin': '[Adresse Vermieter]',
    
    # Personal data - General parties
    r'Anna Müller': '[Name Mieter]',
    r'Wohnstraße 7, 80331 München': '[Adresse Mieter]',
    r'Thomas Wagner': '[Name Eigentümer]',
    r'Hausverwaltung Meyer GmbH': '[Name/Firma Vermieter]',
    r'Gewerbeimmobilien Nord GmbH': '[Firma/Name Vermieter]',
    
    # Lawyer/Professional data
    r'Rechtsanwaltskanzlei Dr\. Schneider & Partner\nBahnhofstraße 45, 60329 Frankfurt\nTel: 069/12345678, Fax: 069/12345679\nmail@ra-schneider\.de': '[Kanzlei-Briefkopf]',
    r'Rechtsanwaltskanzlei Dr\. Schneider & Partner': '[Kanzleiname]',
    r'Rechtsanwaltskanzlei Weber & Kollegen': '[Name der Kanzlei]',
    r'Bau-AG Mustermann': '[Name/Firma Auftraggeber]',
    r'Handwerksbetrieb Schmidt GmbH': '[Name/Firma Auftragnehmer]',
    
    # Addresses
    r'Musterstraße 12, 12345 Berlin': '[Mietadresse]',
    r'Hauptstraße 15, 50667 Köln': '[Adresse]',
    r'Wohnanlage Parkblick': '[Objektbezeichnung]',
    
    # Dates - generic patterns
    r'Berlin, den \d{2}\.\d{2}\.\d{4}': '[Ort], den [Datum]',
    r'\d{2}\.\d{2}\.\d{4}': '[Datum]',
    r'Berlin(?!,)': '[Ort]',
    
    # Money amounts
    r'850,00 €': '[Betrag] €',
    r'1\.200,00 €': '[___] €',
    r'950,00 €': '[Miethöhe]',
    
    # Numbers and quantities
    r'(?<!\d)2(?!\d)': '[Anzahl]',
    r'(?<!\d)3(?!\d)': '[___]',
    
    # Court/Legal
    r'12 C 345/24': '[Aktenzeichen]',
    r'Amtsgericht Berlin-Mitte': '[Gericht]',
    
    # Property details
    r'(?<!\d)75(?!\d)': '[Quadratmeter]',
    r'3\. OG': '[Stockwerk]',
    
    # Account details
    r'DE89 3704 0044 0532 0130 00': '[IBAN]',
    
    # Specific descriptions
    r'Schimmelbildung im Badezimmer an der Decke \(ca\. 30x40 cm\)': '[Beschreibung des Mangels]',
    r'Heizung funktioniert nicht ordnungsgemäß, Raumtemperatur unter 18°C': '[Beschreibung der Mängel]',
}

def restore_placeholders():
    file_path = "src/app/app/templates/page.tsx"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all reverse replacements
    for pattern, placeholder in REVERSE_REPLACEMENTS.items():
        content = re.sub(pattern, placeholder, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Restored placeholders in templates")
    print(f"   Applied {len(REVERSE_REPLACEMENTS)} reverse replacements")
    print(f"   Templates ready for AI-based dynamic filling")

if __name__ == "__main__":
    restore_placeholders()
