#!/bin/bash
# Seed Test-Objekt für Domulex
# Nutzt gcloud REST API zum Erstellen von Firestore-Dokumenten

# Konfiguration
PROJECT_ID="domulex-ai"
USER_ID="${1:-}"

if [ -z "$USER_ID" ]; then
    echo "❌ Bitte User-ID angeben!"
    echo ""
    echo "Usage: ./scripts/seed_test_objekt.sh <USER_ID>"
    echo ""
    echo "Die User-ID findest du:"
    echo "  Firebase Console > Authentication > Users"
    echo ""
    echo "Beispiel:"
    echo "  ./scripts/seed_test_objekt.sh tfIrffaZl3WmJECzBiFFP9BNWpY2"
    exit 1
fi

echo "🏢 Erstelle Test-MFH für User: $USER_ID"
echo ""

# Access Token holen
ACCESS_TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Nicht bei gcloud angemeldet!"
    echo "   Führe aus: gcloud auth application-default login"
    exit 1
fi

# Aktuelles Datum für createdAt
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

# Dokument-Daten als JSON
DOCUMENT_JSON=$(cat <<EOF
{
  "fields": {
    "adresse": { "stringValue": "Musterstraße 42" },
    "plz": { "stringValue": "10115" },
    "ort": { "stringValue": "Berlin" },
    "gesamtflaeche": { "integerValue": "480" },
    "gesamteinheiten": { "integerValue": "6" },
    "baujahr": { "integerValue": "1985" },
    "heizungstyp": { "stringValue": "gas" },
    "energieausweis": { "stringValue": "E" },
    "typ": { "stringValue": "mfh" },
    "notizen": { "stringValue": "Test-MFH für Nebenkostenabrechnung" },
    "createdAt": { "timestampValue": "$TIMESTAMP" },
    "mieter": {
      "arrayValue": {
        "values": [
          {
            "mapValue": {
              "fields": {
                "id": { "stringValue": "mieter-1" },
                "name": { "stringValue": "Familie Müller" },
                "einheit": { "stringValue": "EG links" },
                "flaeche": { "integerValue": "75" },
                "personenanzahl": { "integerValue": "3" },
                "einzugsdatum": { "stringValue": "2020-04-01" },
                "email": { "stringValue": "mueller@example.com" },
                "telefon": { "stringValue": "030-12345671" },
                "vorauszahlung": { "integerValue": "250" }
              }
            }
          },
          {
            "mapValue": {
              "fields": {
                "id": { "stringValue": "mieter-2" },
                "name": { "stringValue": "Herr Schmidt" },
                "einheit": { "stringValue": "EG rechts" },
                "flaeche": { "integerValue": "65" },
                "personenanzahl": { "integerValue": "1" },
                "einzugsdatum": { "stringValue": "2019-07-15" },
                "email": { "stringValue": "schmidt@example.com" },
                "telefon": { "stringValue": "030-12345672" },
                "vorauszahlung": { "integerValue": "180" }
              }
            }
          },
          {
            "mapValue": {
              "fields": {
                "id": { "stringValue": "mieter-3" },
                "name": { "stringValue": "Frau Weber" },
                "einheit": { "stringValue": "1. OG links" },
                "flaeche": { "integerValue": "85" },
                "personenanzahl": { "integerValue": "2" },
                "einzugsdatum": { "stringValue": "2021-01-01" },
                "email": { "stringValue": "weber@example.com" },
                "telefon": { "stringValue": "030-12345673" },
                "vorauszahlung": { "integerValue": "280" }
              }
            }
          },
          {
            "mapValue": {
              "fields": {
                "id": { "stringValue": "mieter-4" },
                "name": { "stringValue": "WG Hoffmann" },
                "einheit": { "stringValue": "1. OG rechts" },
                "flaeche": { "integerValue": "95" },
                "personenanzahl": { "integerValue": "4" },
                "einzugsdatum": { "stringValue": "2022-10-01" },
                "email": { "stringValue": "wg-hoffmann@example.com" },
                "telefon": { "stringValue": "030-12345674" },
                "vorauszahlung": { "integerValue": "320" }
              }
            }
          },
          {
            "mapValue": {
              "fields": {
                "id": { "stringValue": "mieter-5" },
                "name": { "stringValue": "Familie Yilmaz" },
                "einheit": { "stringValue": "2. OG links" },
                "flaeche": { "integerValue": "80" },
                "personenanzahl": { "integerValue": "4" },
                "einzugsdatum": { "stringValue": "2018-03-01" },
                "email": { "stringValue": "yilmaz@example.com" },
                "telefon": { "stringValue": "030-12345675" },
                "vorauszahlung": { "integerValue": "270" }
              }
            }
          },
          {
            "mapValue": {
              "fields": {
                "id": { "stringValue": "mieter-6" },
                "name": { "stringValue": "Dr. Braun" },
                "einheit": { "stringValue": "2. OG rechts" },
                "flaeche": { "integerValue": "80" },
                "personenanzahl": { "integerValue": "2" },
                "einzugsdatum": { "stringValue": "2023-06-01" },
                "email": { "stringValue": "braun@example.com" },
                "telefon": { "stringValue": "030-12345676" },
                "vorauszahlung": { "integerValue": "260" }
              }
            }
          }
        ]
      }
    }
  }
}
EOF
)

# API-Aufruf
RESPONSE=$(curl -s -X POST \
  "https://firestore.googleapis.com/v1/projects/$PROJECT_ID/databases/(default)/documents/users/$USER_ID/objekte" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$DOCUMENT_JSON")

# Prüfen ob erfolgreich
if echo "$RESPONSE" | grep -q '"name":'; then
    DOC_ID=$(echo "$RESPONSE" | grep -o '"name": "[^"]*"' | head -1 | sed 's/.*objekte\///' | sed 's/".*//')
    echo "✅ Test-Objekt erstellt mit ID: $DOC_ID"
    echo ""
    echo "📋 Objektdaten:"
    echo "   Adresse: Musterstraße 42, 10115 Berlin"
    echo "   Typ: Mehrfamilienhaus"
    echo "   Gesamtfläche: 480 m²"
    echo "   Einheiten: 6"
    echo "   Heizung: Erdgas"
    echo "   Baujahr: 1985"
    echo ""
    echo "👥 Mieter:"
    echo "   - Familie Müller (EG links): 75m², 3 Personen, 250€/Monat"
    echo "   - Herr Schmidt (EG rechts): 65m², 1 Person, 180€/Monat"
    echo "   - Frau Weber (1. OG links): 85m², 2 Personen, 280€/Monat"
    echo "   - WG Hoffmann (1. OG rechts): 95m², 4 Personen, 320€/Monat"
    echo "   - Familie Yilmaz (2. OG links): 80m², 4 Personen, 270€/Monat"
    echo "   - Dr. Braun (2. OG rechts): 80m², 2 Personen, 260€/Monat"
    echo ""
    echo "🎉 Fertig!"
    echo ""
    echo "Nächste Schritte:"
    echo "1. Öffne https://domulex.ai/app/objekte"
    echo "2. Du siehst das neue MFH 'Musterstraße 42'"
    echo "3. Gehe zu https://domulex.ai/app/nebenkosten-abrechnung"
    echo "4. Wähle das Objekt und erstelle eine Abrechnung"
else
    echo "❌ Fehler beim Erstellen:"
    echo "$RESPONSE" | head -20
    exit 1
fi
