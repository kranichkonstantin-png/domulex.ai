#!/usr/bin/env python3
"""
Seed-Script: Erstellt ein Test-MFH mit 6 Mietparteien in Firestore
Benötigt: pip install firebase-admin

Vor der Ausführung:
1. Gehe zu Firebase Console > Project Settings > Service Accounts
2. Generiere einen neuen Private Key (JSON)
3. Speichere als 'service-account.json' im Projektroot
4. Führe aus: python scripts/seed_test_objekt.py <USER_ID>
"""

import sys
import json
from datetime import datetime, date

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("❌ firebase-admin nicht installiert!")
    print("   Installiere mit: pip install firebase-admin")
    sys.exit(1)

# Test-Objekt: Mehrfamilienhaus mit 6 Parteien
TEST_OBJEKT = {
    "adresse": "Musterstraße 42",
    "plz": "10115",
    "ort": "Berlin",
    "gesamtflaeche": 480,  # 6 Wohnungen à ca. 80m²
    "gesamteinheiten": 6,
    "baujahr": 1985,
    "heizungstyp": "gas",
    "energieausweis": "E",
    "typ": "mfh",
    "notizen": "Test-MFH für Nebenkostenabrechnung - Erstellt am " + datetime.now().strftime("%d.%m.%Y"),
    "mieter": [
        {
            "id": "mieter-1",
            "name": "Familie Müller",
            "einheit": "EG links",
            "flaeche": 75,
            "personenanzahl": 3,
            "einzugsdatum": "2020-04-01",
            "email": "mueller@example.com",
            "telefon": "030-12345671",
            "vorauszahlung": 250
        },
        {
            "id": "mieter-2",
            "name": "Herr Schmidt",
            "einheit": "EG rechts",
            "flaeche": 65,
            "personenanzahl": 1,
            "einzugsdatum": "2019-07-15",
            "email": "schmidt@example.com",
            "telefon": "030-12345672",
            "vorauszahlung": 180
        },
        {
            "id": "mieter-3",
            "name": "Frau Weber",
            "einheit": "1. OG links",
            "flaeche": 85,
            "personenanzahl": 2,
            "einzugsdatum": "2021-01-01",
            "email": "weber@example.com",
            "telefon": "030-12345673",
            "vorauszahlung": 280
        },
        {
            "id": "mieter-4",
            "name": "WG Hoffmann",
            "einheit": "1. OG rechts",
            "flaeche": 95,
            "personenanzahl": 4,
            "einzugsdatum": "2022-10-01",
            "email": "wg-hoffmann@example.com",
            "telefon": "030-12345674",
            "vorauszahlung": 320
        },
        {
            "id": "mieter-5",
            "name": "Familie Yilmaz",
            "einheit": "2. OG links",
            "flaeche": 80,
            "personenanzahl": 4,
            "einzugsdatum": "2018-03-01",
            "email": "yilmaz@example.com",
            "telefon": "030-12345675",
            "vorauszahlung": 270
        },
        {
            "id": "mieter-6",
            "name": "Dr. Braun",
            "einheit": "2. OG rechts",
            "flaeche": 80,
            "personenanzahl": 2,
            "einzugsdatum": "2023-06-01",
            "email": "braun@example.com",
            "telefon": "030-12345676",
            "vorauszahlung": 260
        }
    ],
    "createdAt": datetime.now()
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/seed_test_objekt.py <USER_ID>")
        print("")
        print("Die User-ID findest du:")
        print("1. Firebase Console > Authentication > Users")
        print("2. Klicke auf den Benutzer")
        print("3. Kopiere die 'User UID'")
        print("")
        print("Beispiel: python scripts/seed_test_objekt.py tfIrffaZl3WmJECzBiFFP9BNWpY2")
        sys.exit(1)
    
    user_id = sys.argv[1]
    
    # Firebase initialisieren
    try:
        cred = credentials.Certificate("service-account.json")
        firebase_admin.initialize_app(cred)
    except FileNotFoundError:
        print("❌ service-account.json nicht gefunden!")
        print("")
        print("Erstelle die Datei so:")
        print("1. Firebase Console > Project Settings > Service Accounts")
        print("2. 'Generate new private key' klicken")
        print("3. Die heruntergeladene JSON-Datei als 'service-account.json' speichern")
        sys.exit(1)
    except Exception as e:
        if "already exists" in str(e):
            pass  # App bereits initialisiert
        else:
            raise e
    
    db = firestore.client()
    
    print(f"🏢 Erstelle Test-MFH für User: {user_id}")
    print("")
    
    # Dokument erstellen
    doc_ref = db.collection("users").document(user_id).collection("objekte").add(TEST_OBJEKT)
    doc_id = doc_ref[1].id
    
    print(f"✅ Test-Objekt erstellt mit ID: {doc_id}")
    print("")
    print("📋 Objektdaten:")
    print(f"   Adresse: {TEST_OBJEKT['adresse']}, {TEST_OBJEKT['plz']} {TEST_OBJEKT['ort']}")
    print(f"   Typ: Mehrfamilienhaus")
    print(f"   Gesamtfläche: {TEST_OBJEKT['gesamtflaeche']} m²")
    print(f"   Einheiten: {TEST_OBJEKT['gesamteinheiten']}")
    print(f"   Heizung: Erdgas")
    print(f"   Baujahr: {TEST_OBJEKT['baujahr']}")
    print("")
    print("👥 Mieter:")
    for m in TEST_OBJEKT["mieter"]:
        print(f"   - {m['name']} ({m['einheit']}): {m['flaeche']}m², {m['personenanzahl']} Personen, {m['vorauszahlung']}€/Monat")
    
    print("")
    print("🎉 Fertig!")
    print("")
    print("Nächste Schritte:")
    print("1. Öffne https://domulex.ai/app/objekte")
    print("2. Melde dich mit dem Professional/Lawyer Account an")
    print("3. Du siehst das neue MFH 'Musterstraße 42'")
    print("4. Gehe zu https://domulex.ai/app/nebenkosten-abrechnung")
    print("5. Wähle das Objekt und erstelle eine Abrechnung")


if __name__ == "__main__":
    main()
