#!/bin/bash
# Seed Mustervorlagen für Dokumentenmanagement
# Lädt verschiedene Vorlagen in die managed_documents Collection

PROJECT_ID="domulex-ai"
USER_ID="${1:-tfIrffaZl3WmJECzBiFFP9BNWpY2}"

ACCESS_TOKEN=$(gcloud auth application-default print-access-token 2>/dev/null)
if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ Nicht bei gcloud angemeldet!"
    exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

echo "📄 Erstelle Mustervorlagen für User: $USER_ID"
echo ""

# Funktion zum Erstellen eines Dokuments
create_document() {
    local NAME="$1"
    local CATEGORY="$2"
    local CONTENT="$3"
    local TAGS="$4"
    local AI_SUMMARY="$5"
    
    DOCUMENT_JSON=$(cat <<EOF
{
  "fields": {
    "name": { "stringValue": "$NAME" },
    "category": { "stringValue": "$CATEGORY" },
    "status": { "stringValue": "aktiv" },
    "content": { "stringValue": "$CONTENT" },
    "aiSummary": { "stringValue": "$AI_SUMMARY" },
    "sourceApp": { "stringValue": "import" },
    "createdAt": { "timestampValue": "$TIMESTAMP" },
    "updatedAt": { "timestampValue": "$TIMESTAMP" },
    "tags": {
      "arrayValue": {
        "values": [
$TAGS
        ]
      }
    },
    "deadlines": { "arrayValue": { "values": [] } }
  }
}
EOF
)

    RESPONSE=$(curl -s -X POST \
      "https://firestore.googleapis.com/v1/projects/$PROJECT_ID/databases/(default)/documents/users/$USER_ID/managed_documents" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$DOCUMENT_JSON")
    
    if echo "$RESPONSE" | grep -q '"name":'; then
        echo "  ✅ $NAME"
    else
        echo "  ❌ $NAME - Fehler"
    fi
}

echo "📋 Erstelle Mietrecht-Vorlagen..."

# 1. Mietvertrag Wohnung
create_document \
    "Mietvertrag Wohnung" \
    "mustervorlagen" \
    "MIETVERTRAG\\n\\nzwischen\\n\\n[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\n- nachfolgend Vermieter genannt -\\n\\nund\\n\\n[Mieter-Name]\\n[Mieter-Adresse]\\n\\n- nachfolgend Mieter genannt -\\n\\n§ 1 Mietgegenstand\\nDer Vermieter vermietet dem Mieter die Wohnung [Adresse], bestehend aus [Anzahl] Zimmern, Küche, Bad/WC, Flur, mit einer Wohnfläche von ca. [X] m².\\n\\n§ 2 Mietzeit\\nDas Mietverhältnis beginnt am [Datum] und wird auf unbestimmte Zeit geschlossen.\\n\\n§ 3 Miete\\nDie monatliche Kaltmiete beträgt [X] EUR.\\nDie monatlichen Betriebskostenvorauszahlungen betragen [X] EUR.\\nDie Gesamtmiete beträgt somit [X] EUR.\\n\\n§ 4 Kaution\\nDer Mieter zahlt eine Kaution in Höhe von [X] EUR (entspricht [X] Monatsmieten).\\n\\n§ 5 Schönheitsreparaturen\\nSchönheitsreparaturen sind vom Mieter fachgerecht auszuführen.\\n\\n[Ort], den [Datum]\\n\\n____________________          ____________________\\nVermieter                                    Mieter" \
    '{ "stringValue": "Mietvertrag" }, { "stringValue": "Wohnung" }, { "stringValue": "Vorlage" }' \
    "Standard-Mietvertrag für Wohnraum mit allen wichtigen Klauseln nach BGB §§ 535 ff."

# 2. Mieterhöhungsverlangen
create_document \
    "Mieterhöhungsverlangen" \
    "mustervorlagen" \
    "[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\nAn\\n[Mieter-Name]\\n[Mieter-Adresse]\\n\\n[Ort], den [Datum]\\n\\nMieterhöhungsverlangen gem. § 558 BGB\\n\\nSehr geehrte/r [Mieter-Name],\\n\\nhiermit verlange ich die Zustimmung zur Erhöhung der Nettokaltmiete für die von Ihnen gemietete Wohnung [Adresse].\\n\\nDie bisherige Nettokaltmiete beträgt: [X] EUR\\nDie neue Nettokaltmiete soll betragen: [Y] EUR\\n\\nDie Erhöhung entspricht [X]% und liegt innerhalb der ortsüblichen Vergleichsmiete gemäß dem aktuellen Mietspiegel [Stadt/Jahr].\\n\\nIch bitte Sie, mir Ihre Zustimmung bis zum [Datum + 2 Monate] schriftlich zu erteilen.\\n\\nMit freundlichen Grüßen\\n\\n____________________\\n[Vermieter-Name]" \
    '{ "stringValue": "Mieterhöhung" }, { "stringValue": "§558 BGB" }, { "stringValue": "Vorlage" }' \
    "Mieterhöhungsverlangen nach § 558 BGB mit Bezug auf Mietspiegel."

# 3. Kündigung Mietvertrag (Vermieter)
create_document \
    "Kündigung Mietvertrag (Vermieter)" \
    "mustervorlagen" \
    "[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\nEinschreiben mit Rückschein\\n\\nAn\\n[Mieter-Name]\\n[Mieter-Adresse]\\n\\n[Ort], den [Datum]\\n\\nOrdentliche Kündigung des Mietverhältnisses\\n\\nSehr geehrte/r [Mieter-Name],\\n\\nhiermit kündige ich das mit Ihnen bestehende Mietverhältnis über die Wohnung [Adresse] ordentlich zum [Kündigungsdatum] bzw. zum nächstmöglichen Termin.\\n\\nKündigungsgrund:\\n[Eigenbedarf / Hinderung wirtschaftlicher Verwertung / Pflichtverletzung]\\n\\n[Bei Eigenbedarf: Die Wohnung wird benötigt für: [Person], [Verhältnis zum Vermieter], [Grund des Bedarfs]]\\n\\nIch weise Sie auf Ihr Widerspruchsrecht gemäß § 574 BGB (Sozialklausel) hin.\\n\\nBitte bestätigen Sie den Erhalt dieser Kündigung.\\n\\nMit freundlichen Grüßen\\n\\n____________________\\n[Vermieter-Name]" \
    '{ "stringValue": "Kündigung" }, { "stringValue": "Vermieter" }, { "stringValue": "Eigenbedarf" }' \
    "Ordentliche Kündigung durch Vermieter mit Hinweis auf Widerspruchsrecht nach § 574 BGB."

# 4. Mängelanzeige
create_document \
    "Mängelanzeige" \
    "mustervorlagen" \
    "[Mieter-Name]\\n[Mieter-Adresse]\\n\\nAn\\n[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\n[Ort], den [Datum]\\n\\nMängelanzeige gem. § 536c BGB\\n\\nSehr geehrte/r [Vermieter-Name],\\n\\nhiermit zeige ich Ihnen folgenden Mangel in der von mir gemieteten Wohnung [Adresse] an:\\n\\nBeschreibung des Mangels:\\n[Detaillierte Beschreibung]\\n\\nFestgestellt am: [Datum]\\nOrt: [Zimmer/Bereich]\\n\\nIch fordere Sie auf, den Mangel bis zum [Frist: 14 Tage] zu beseitigen.\\n\\nBis zur Mängelbeseitigung behalte ich mir vor, die Miete gemäß § 536 BGB zu mindern.\\n\\nFotos des Mangels sind diesem Schreiben beigefügt.\\n\\nMit freundlichen Grüßen\\n\\n____________________\\n[Mieter-Name]\\n\\nAnlagen: [X] Fotos" \
    '{ "stringValue": "Mängelanzeige" }, { "stringValue": "§536c BGB" }, { "stringValue": "Mieter" }' \
    "Mängelanzeige mit Fristsetzung nach § 536c BGB, Vorbereitung für Mietminderung."

# 5. Nebenkostenabrechnung
create_document \
    "Nebenkostenabrechnung" \
    "mustervorlagen" \
    "NEBENKOSTENABRECHNUNG\\n\\nfür den Abrechnungszeitraum [01.01.XXXX] bis [31.12.XXXX]\\n\\nVermieter: [Vermieter-Name]\\nMieter: [Mieter-Name]\\nObjekt: [Adresse]\\nWohneinheit: [Einheit]\\nWohnfläche: [X] m²\\n\\nKostenart                    | Gesamtkosten | Ihr Anteil | Verteilerschlüssel\\n-----------------------------|--------------|------------|-------------------\\nGrundsteuer                  | [X] EUR      | [X] EUR    | nach Fläche\\nWasserversorgung             | [X] EUR      | [X] EUR    | nach Verbrauch\\nEntwässerung                 | [X] EUR      | [X] EUR    | nach Verbrauch\\nHeizkosten                   | [X] EUR      | [X] EUR    | 70% Verbrauch/30% Fläche\\nMüllabfuhr                   | [X] EUR      | [X] EUR    | nach Personen\\nGebäudeversicherung          | [X] EUR      | [X] EUR    | nach Fläche\\nHauswart                     | [X] EUR      | [X] EUR    | nach Fläche\\nAllgemeinstrom               | [X] EUR      | [X] EUR    | nach Einheiten\\n-----------------------------|--------------|------------|-------------------\\nGESAMTKOSTEN                 | [X] EUR      | [X] EUR    |\\n\\nIhre Vorauszahlungen: [X] EUR (12 × [X] EUR/Monat)\\n\\n[NACHZAHLUNG/GUTHABEN]: [X] EUR\\n\\nDer Betrag ist zahlbar bis zum [Datum] auf folgendes Konto:\\n[IBAN]\\n\\n[Ort], den [Datum]\\n\\n____________________\\n[Vermieter-Name]" \
    '{ "stringValue": "Nebenkostenabrechnung" }, { "stringValue": "BetrKV" }, { "stringValue": "Vorlage" }' \
    "Vollständige Nebenkostenabrechnung nach BetrKV mit allen umlagefähigen Kostenarten."

# 6. Mahnung Mietzahlung
create_document \
    "Mahnung Mietzahlung" \
    "mustervorlagen" \
    "[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\nAn\\n[Mieter-Name]\\n[Mieter-Adresse]\\n\\n[Ort], den [Datum]\\n\\n[1./2./3.] Mahnung - Rückstand Mietzahlung\\n\\nSehr geehrte/r [Mieter-Name],\\n\\nleider mussten wir feststellen, dass Sie mit der Zahlung der Miete im Rückstand sind.\\n\\nEs fehlen folgende Zahlungen:\\n- Miete [Monat/Jahr]: [X] EUR\\n- Miete [Monat/Jahr]: [X] EUR\\n\\nGesamtrückstand: [X] EUR\\n\\nIch fordere Sie auf, den ausstehenden Betrag bis zum [Frist] auf folgendes Konto zu überweisen:\\n[IBAN]\\n\\n[Bei 2./3. Mahnung: Sollte die Zahlung nicht fristgerecht erfolgen, behalte ich mir die fristlose Kündigung gem. § 543 Abs. 2 Nr. 3 BGB vor.]\\n\\nMit freundlichen Grüßen\\n\\n____________________\\n[Vermieter-Name]" \
    '{ "stringValue": "Mahnung" }, { "stringValue": "Mietrückstand" }, { "stringValue": "Vorlage" }' \
    "Mahnung bei Mietrückstand mit Eskalationsstufen bis zur fristlosen Kündigung."

echo ""
echo "📋 Erstelle Kaufrecht-Vorlagen..."

# 7. Kaufvertrag Immobilie (Entwurf)
create_document \
    "Kaufvertrag Immobilie (Entwurf)" \
    "mustervorlagen" \
    "KAUFVERTRAG\\n(Entwurf - Beurkundung durch Notar erforderlich)\\n\\nzwischen\\n\\n[Verkäufer-Name]\\n[Verkäufer-Adresse]\\n\\n- nachfolgend Verkäufer genannt -\\n\\nund\\n\\n[Käufer-Name]\\n[Käufer-Adresse]\\n\\n- nachfolgend Käufer genannt -\\n\\n§ 1 Kaufgegenstand\\nDer Verkäufer verkauft an den Käufer das im Grundbuch von [Ort], Blatt [X], Flur [X], Flurstück [X] eingetragene Grundstück mit der darauf befindlichen Immobilie [Adresse].\\n\\n§ 2 Kaufpreis\\nDer Kaufpreis beträgt [X] EUR (in Worten: [Betrag] Euro).\\n\\n§ 3 Fälligkeit und Zahlung\\nDer Kaufpreis ist fällig innerhalb von [X] Tagen nach Vorliegen aller Fälligkeitsvoraussetzungen.\\n\\n§ 4 Besitzübergang\\nDer Besitz geht am [Datum] auf den Käufer über.\\n\\n§ 5 Gewährleistung\\nDie Immobilie wird verkauft wie besichtigt unter Ausschluss der Gewährleistung, soweit gesetzlich zulässig.\\n\\n§ 6 Grundbucherklärungen\\nDer Verkäufer bewilligt und beantragt die Eintragung einer Auflassungsvormerkung zugunsten des Käufers.\\n\\n[Hinweis: Dieser Entwurf muss notariell beurkundet werden gem. § 311b BGB]" \
    '{ "stringValue": "Kaufvertrag" }, { "stringValue": "Immobilie" }, { "stringValue": "Notar" }' \
    "Entwurf eines Immobilienkaufvertrags, erfordert notarielle Beurkundung nach § 311b BGB."

# 8. Reservierungsvereinbarung
create_document \
    "Reservierungsvereinbarung Immobilie" \
    "mustervorlagen" \
    "RESERVIERUNGSVEREINBARUNG\\n\\nzwischen\\n\\n[Verkäufer/Makler-Name]\\n[Adresse]\\n\\n- nachfolgend Anbieter genannt -\\n\\nund\\n\\n[Interessent-Name]\\n[Adresse]\\n\\n- nachfolgend Interessent genannt -\\n\\nbetreffend die Immobilie [Adresse]\\n\\n§ 1 Reservierung\\nDer Anbieter reserviert die o.g. Immobilie bis zum [Datum] exklusiv für den Interessenten.\\n\\n§ 2 Reservierungsgebühr\\nDer Interessent zahlt eine Reservierungsgebühr von [X] EUR.\\nDiese wird bei Zustandekommen des Kaufvertrags auf den Kaufpreis angerechnet.\\nBei Nichtzustandekommen aus Gründen, die der Interessent zu vertreten hat, verfällt die Gebühr.\\n\\n§ 3 Kaufpreis\\nDer vorgesehene Kaufpreis beträgt [X] EUR.\\n\\n§ 4 Notartermin\\nDer Notartermin soll bis zum [Datum] stattfinden.\\n\\n[Ort], den [Datum]\\n\\n____________________          ____________________\\nAnbieter                                  Interessent" \
    '{ "stringValue": "Reservierung" }, { "stringValue": "Immobilienkauf" }, { "stringValue": "Vorlage" }' \
    "Reservierungsvereinbarung für Immobilien mit Regelung der Reservierungsgebühr."

echo ""
echo "📋 Erstelle WEG-Vorlagen..."

# 9. Einladung Eigentümerversammlung
create_document \
    "Einladung Eigentümerversammlung" \
    "mustervorlagen" \
    "[WEG-Verwaltung]\\n[Adresse]\\n\\nAn alle Wohnungseigentümer der WEG [Adresse]\\n\\n[Ort], den [Datum]\\n\\nEinladung zur ordentlichen Eigentümerversammlung\\n\\nSehr geehrte Eigentümer,\\n\\nhiermit lade ich Sie zur ordentlichen Eigentümerversammlung ein:\\n\\nDatum: [Datum]\\nUhrzeit: [Uhrzeit]\\nOrt: [Ort/Adresse]\\n\\nTagesordnung:\\n\\nTOP 1: Begrüßung und Feststellung der Beschlussfähigkeit\\nTOP 2: Genehmigung der Niederschrift der letzten Versammlung\\nTOP 3: Bericht des Verwalters\\nTOP 4: Jahresabrechnung [Jahr]\\nTOP 5: Entlastung des Verwalters\\nTOP 6: Wirtschaftsplan [Jahr]\\nTOP 7: Instandhaltungsrücklage\\nTOP 8: [Weitere Tagesordnungspunkte]\\nTOP 9: Verschiedenes\\n\\nBei Verhinderung können Sie sich durch Vollmacht vertreten lassen.\\n\\nMit freundlichen Grüßen\\n\\n____________________\\n[Verwalter-Name]\\n\\nAnlagen:\\n- Vollmachtsformular\\n- Jahresabrechnung\\n- Wirtschaftsplan" \
    '{ "stringValue": "WEG" }, { "stringValue": "Eigentümerversammlung" }, { "stringValue": "Einladung" }' \
    "Einladung zur WEG-Eigentümerversammlung mit Tagesordnung nach WEG-Reform 2020."

# 10. Beschlussprotokoll WEG
create_document \
    "Beschlussprotokoll Eigentümerversammlung" \
    "mustervorlagen" \
    "NIEDERSCHRIFT\\nder Eigentümerversammlung der WEG [Adresse]\\n\\nam [Datum] um [Uhrzeit] in [Ort]\\n\\nAnwesend/Vertreten: [X] von [Y] Miteigentumsanteilen = [X]%\\n\\nVersammlungsleiter: [Name]\\nProtokollführer: [Name]\\n\\nDie Versammlung ist beschlussfähig.\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nTOP 1: Genehmigung der Jahresabrechnung [Jahr]\\n\\nBeschluss:\\nDie Jahresabrechnung für das Jahr [Jahr] wird genehmigt.\\n\\nAbstimmungsergebnis: [Ja]-Stimmen, [Nein]-Stimmen, [Enthaltungen]\\nBeschluss: ☐ angenommen ☐ abgelehnt\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nTOP 2: Entlastung des Verwalters\\n\\nBeschluss:\\nDem Verwalter wird für das Jahr [Jahr] Entlastung erteilt.\\n\\nAbstimmungsergebnis: [Ja]-Stimmen, [Nein]-Stimmen, [Enthaltungen]\\nBeschluss: ☐ angenommen ☐ abgelehnt\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nDie Versammlung wurde um [Uhrzeit] geschlossen.\\n\\n____________________          ____________________\\nVersammlungsleiter                Protokollführer" \
    '{ "stringValue": "WEG" }, { "stringValue": "Protokoll" }, { "stringValue": "Beschluss" }' \
    "Beschlussprotokoll für WEG-Versammlung mit Abstimmungsergebnissen."

echo ""
echo "📋 Erstelle Schriftsätze..."

# 11. Klage auf Zahlung
create_document \
    "Klage auf Zahlung (Mietrückstand)" \
    "mustervorlagen" \
    "An das\\nAmtsgericht [Ort]\\n[Adresse]\\n\\nKLAGE\\n\\ndes/der [Kläger-Name], [Adresse]\\n\\n- Kläger/in -\\n\\nProzessbevollmächtigte/r: [Rechtsanwalt]\\n\\ngegen\\n\\n[Beklagter-Name], [Adresse]\\n\\n- Beklagte/r -\\n\\nwegen: Zahlung von Mietrückständen\\nStreitwert: [X] EUR\\n\\nNamens und in Vollmacht des Klägers erhebe ich Klage und beantrage:\\n\\n1. Der/Die Beklagte wird verurteilt, an den Kläger [X] EUR nebst Zinsen in Höhe von 5 Prozentpunkten über dem Basiszinssatz seit [Datum] zu zahlen.\\n\\n2. Der/Die Beklagte trägt die Kosten des Rechtsstreits.\\n\\n3. Das Urteil ist vorläufig vollstreckbar.\\n\\nBegründung:\\n\\nI.\\nDer Kläger ist Eigentümer und Vermieter der Wohnung [Adresse]. Der Beklagte ist aufgrund des Mietvertrags vom [Datum] Mieter dieser Wohnung.\\n\\nII.\\nDie monatliche Miete beträgt [X] EUR. Der Beklagte hat folgende Mietzahlungen nicht geleistet:\\n- [Monat/Jahr]: [X] EUR\\n- [Monat/Jahr]: [X] EUR\\n\\nIII.\\nTrotz Mahnung vom [Datum] erfolgte keine Zahlung.\\n\\nBeweis: Mietvertrag (Anlage K1)\\n        Mahnschreiben (Anlage K2)\\n\\n[Ort], den [Datum]\\n\\n____________________\\n[Rechtsanwalt]" \
    '{ "stringValue": "Klage" }, { "stringValue": "Mietrückstand" }, { "stringValue": "Schriftsatz" }' \
    "Klageschrift für Zahlungsklage wegen Mietrückständen am Amtsgericht."

# 12. Räumungsklage
create_document \
    "Räumungsklage" \
    "mustervorlagen" \
    "An das\\nAmtsgericht [Ort]\\n[Adresse]\\n\\nKLAGE\\n\\ndes/der [Kläger-Name], [Adresse]\\n\\n- Kläger/in -\\n\\nProzessbevollmächtigte/r: [Rechtsanwalt]\\n\\ngegen\\n\\n[Beklagter-Name], [Adresse]\\n\\n- Beklagte/r -\\n\\nwegen: Räumung und Herausgabe\\nStreitwert: [Jahreskaltmiete] EUR\\n\\nNamens und in Vollmacht des Klägers erhebe ich Klage und beantrage:\\n\\n1. Der/Die Beklagte wird verurteilt, die Wohnung [Adresse], bestehend aus [X] Zimmern, Küche, Bad, zu räumen und an den Kläger herauszugeben.\\n\\n2. Der/Die Beklagte wird verurteilt, an den Kläger [X] EUR (rückständige Mieten) nebst Zinsen zu zahlen.\\n\\n3. Der/Die Beklagte trägt die Kosten des Rechtsstreits.\\n\\nBegründung:\\n\\nI.\\nDer Kläger ist Vermieter, der Beklagte war Mieter der o.g. Wohnung. Das Mietverhältnis wurde wirksam gekündigt.\\n\\nII.\\nMit Schreiben vom [Datum] wurde das Mietverhältnis fristlos, hilfsweise ordentlich gekündigt wegen:\\n☐ Zahlungsverzug (§ 543 Abs. 2 Nr. 3 BGB)\\n☐ Vertragsverletzung (§ 543 Abs. 1 BGB)\\n☐ Eigenbedarf (§ 573 Abs. 2 Nr. 2 BGB)\\n\\nIII.\\nDer Beklagte hat die Wohnung trotz Aufforderung nicht geräumt.\\n\\n[Ort], den [Datum]\\n\\n____________________\\n[Rechtsanwalt]" \
    '{ "stringValue": "Räumungsklage" }, { "stringValue": "Zwangsräumung" }, { "stringValue": "Schriftsatz" }' \
    "Räumungsklage bei Mietvertragskündigung mit Zahlungsantrag."

# 13. Widerspruch Nebenkostenabrechnung
create_document \
    "Widerspruch Nebenkostenabrechnung" \
    "mustervorlagen" \
    "[Mieter-Name]\\n[Mieter-Adresse]\\n\\nAn\\n[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\n[Ort], den [Datum]\\n\\nWiderspruch gegen die Nebenkostenabrechnung [Jahr]\\n\\nSehr geehrte/r [Vermieter-Name],\\n\\ngegen Ihre Nebenkostenabrechnung vom [Datum] für den Abrechnungszeitraum [Jahr] erhebe ich fristgerecht Widerspruch.\\n\\nIch beanstande folgende Punkte:\\n\\n1. [Kostenart]:\\n   - Beanstandung: [z.B. nicht umlagefähig nach BetrKV]\\n   - Forderung: Streichung von [X] EUR\\n\\n2. [Kostenart]:\\n   - Beanstandung: [z.B. falscher Verteilerschlüssel]\\n   - Forderung: Neuberechnung\\n\\n3. [Kostenart]:\\n   - Beanstandung: [z.B. fehlende Belege]\\n   - Forderung: Vorlage der Originalrechnungen\\n\\nIch fordere Sie auf, die Abrechnung entsprechend zu korrigieren und mir eine berichtigte Abrechnung zuzusenden.\\n\\nGleichzeitig mache ich von meinem Belegeinsichtsrecht gemäß § 259 BGB Gebrauch und bitte um Terminvorschlag.\\n\\nMit freundlichen Grüßen\\n\\n____________________\\n[Mieter-Name]" \
    '{ "stringValue": "Widerspruch" }, { "stringValue": "Nebenkosten" }, { "stringValue": "Mieter" }' \
    "Widerspruch gegen Nebenkostenabrechnung mit Belegeinsicht nach § 259 BGB."

echo ""
echo "📋 Erstelle Makler-Vorlagen..."

# 14. Maklervertrag
create_document \
    "Maklervertrag (Alleinauftrag)" \
    "mustervorlagen" \
    "MAKLERVERTRAG\\n(Qualifizierter Alleinauftrag)\\n\\nzwischen\\n\\n[Auftraggeber-Name]\\n[Adresse]\\n\\n- nachfolgend Auftraggeber genannt -\\n\\nund\\n\\n[Makler-Firma]\\n[Adresse]\\nGewerbeerlaubnis nach § 34c GewO\\n\\n- nachfolgend Makler genannt -\\n\\n§ 1 Auftragsgegenstand\\nDer Auftraggeber beauftragt den Makler mit der Vermittlung/dem Nachweis\\n☐ des Verkaufs\\n☐ der Vermietung\\nder Immobilie [Adresse].\\n\\n§ 2 Laufzeit\\nDer Vertrag wird für [X] Monate geschlossen, beginnend am [Datum].\\n\\n§ 3 Alleinauftrag\\nDer Auftraggeber verpflichtet sich, während der Vertragslaufzeit keinen anderen Makler zu beauftragen.\\n\\n§ 4 Maklerprovision\\nBei erfolgreichem Abschluss beträgt die Provision:\\n☐ Verkauf: [X]% des Kaufpreises zzgl. MwSt.\\n☐ Vermietung: [X] Monatsmieten zzgl. MwSt.\\n\\nDie Provision ist hälftig vom Verkäufer und Käufer zu tragen (§ 656c BGB).\\n\\n§ 5 Widerrufsrecht\\nSie haben das Recht, binnen 14 Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen.\\n\\n[Ort], den [Datum]\\n\\n____________________          ____________________\\nAuftraggeber                              Makler" \
    '{ "stringValue": "Maklervertrag" }, { "stringValue": "Provision" }, { "stringValue": "§34c GewO" }' \
    "Qualifizierter Makler-Alleinauftrag mit Provisionsregelung nach § 656c BGB."

# 15. Exposé Vorlage
create_document \
    "Immobilien-Exposé" \
    "mustervorlagen" \
    "EXPOSÉ\\n\\n[OBJEKTTITEL]\\n[Adresse]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nECKDATEN\\n\\nObjektart:        [Eigentumswohnung/Haus/etc.]\\nWohnfläche:       [X] m²\\nGrundstück:       [X] m²\\nZimmer:           [X]\\nBaujahr:          [Jahr]\\nHeizung:          [Typ]\\nEnergieausweis:   [Typ], [kWh/m²a], Klasse [A-H]\\n\\nKaufpreis:        [X] EUR\\nProvision:        [X]% zzgl. MwSt.\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nOBJEKTBESCHREIBUNG\\n\\n[Ausführliche Beschreibung der Immobilie]\\n\\nAUSTATTUNG\\n\\n☑ [Ausstattungsmerkmal 1]\\n☑ [Ausstattungsmerkmal 2]\\n☑ [Ausstattungsmerkmal 3]\\n\\nLAGE\\n\\n[Beschreibung der Lage, Infrastruktur, Anbindung]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nKONTAKT\\n\\n[Makler-Name]\\n[Telefon]\\n[E-Mail]\\n\\nAlle Angaben basieren auf Informationen des Eigentümers. Irrtum und Zwischenverkauf vorbehalten." \
    '{ "stringValue": "Exposé" }, { "stringValue": "Vermarktung" }, { "stringValue": "Makler" }' \
    "Immobilien-Exposé Vorlage mit allen wichtigen Eckdaten und Energieausweis."

echo ""
echo "📋 Erstelle Vollmachten & Verträge..."

# 16. Vollmacht allgemein
create_document \
    "Vollmacht (Allgemein)" \
    "mustervorlagen" \
    "VOLLMACHT\\n\\nIch, [Vollmachtgeber-Name]\\n[Adresse]\\n[Geburtsdatum]\\n\\nerteile hiermit\\n\\n[Bevollmächtigter-Name]\\n[Adresse]\\n[Geburtsdatum]\\n\\nVollmacht, mich in folgenden Angelegenheiten zu vertreten:\\n\\n☐ Generalvollmacht (alle Rechtsgeschäfte)\\n☐ Immobilienangelegenheiten\\n☐ Mietangelegenheiten\\n☐ Behördenangelegenheiten\\n☐ Bankangelegenheiten\\n☐ [Sonstige: _____________]\\n\\nDie Vollmacht gilt:\\n☐ unbefristet\\n☐ bis zum [Datum]\\n☐ für den Einzelfall [Beschreibung]\\n\\nDer Bevollmächtigte ist berechtigt, Untervollmacht zu erteilen:\\n☐ Ja  ☐ Nein\\n\\n[Ort], den [Datum]\\n\\n____________________\\n[Vollmachtgeber]\\n\\nIdentitätsbestätigung (optional):\\nHiermit bestätige ich die Echtheit der Unterschrift.\\n\\n____________________\\n[Notar/Behörde]" \
    '{ "stringValue": "Vollmacht" }, { "stringValue": "Vertretung" }, { "stringValue": "Vorlage" }' \
    "Allgemeine Vollmacht mit Optionen für verschiedene Anwendungsbereiche."

# 17. Übergabeprotokoll
create_document \
    "Übergabeprotokoll Wohnung" \
    "mustervorlagen" \
    "ÜBERGABEPROTOKOLL\\n\\nObjekt: [Adresse]\\nDatum: [Datum]\\nUhrzeit: [Uhrzeit]\\n\\nAnwesend:\\nVermieter/Vertreter: [Name]\\nMieter (alt/neu): [Name]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nZÄHLERSTÄNDE\\n\\nStrom:       Zähler-Nr. [X]    Stand: [X] kWh\\nGas:         Zähler-Nr. [X]    Stand: [X] m³\\nWasser:      Zähler-Nr. [X]    Stand: [X] m³\\nHeizung:     Zähler-Nr. [X]    Stand: [X]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nSCHLÜSSEL\\n\\nHaustür:     [X] Stück\\nWohnung:     [X] Stück\\nKeller:      [X] Stück\\nBriefkasten: [X] Stück\\nGarage:      [X] Stück\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nZUSTAND DER RÄUME\\n\\nFlur:        ☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\nWohnzimmer:  ☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\nSchlafzimmer:☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\nKüche:       ☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\nBad:         ☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\nBalkon:      ☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\nKeller:      ☐ ohne Mängel  ☐ Mängel: [Beschreibung]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\nBEMERKUNGEN\\n\\n[Weitere Bemerkungen]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\n____________________          ____________________\\nVermieter                                    Mieter" \
    '{ "stringValue": "Übergabeprotokoll" }, { "stringValue": "Wohnung" }, { "stringValue": "Zählerstände" }' \
    "Wohnungsübergabeprotokoll mit Zählerständen, Schlüsseln und Zustandsdokumentation."

# 18. Mietschuldenfreiheitsbescheinigung
create_document \
    "Mietschuldenfreiheitsbescheinigung" \
    "mustervorlagen" \
    "[Vermieter-Name]\\n[Vermieter-Adresse]\\n\\n[Ort], den [Datum]\\n\\nMIETSCHULDENFREIHEITSBESCHEINIGUNG\\n\\nHiermit bestätige ich, dass\\n\\n[Mieter-Name]\\n[Geburtsdatum]\\n\\nvom [Einzugsdatum] bis zum [Auszugsdatum/heute]\\n\\nMieter/in der Wohnung [Adresse] war/ist.\\n\\nWährend des gesamten Mietverhältnisses wurden alle Mietzahlungen (Kaltmiete und Nebenkosten) pünktlich und vollständig geleistet.\\n\\nEs bestehen keine offenen Forderungen.\\n\\nDie monatliche Miete betrug zuletzt [X] EUR.\\n\\nDiese Bescheinigung wird auf Wunsch des Mieters für die Vorlage bei einem neuen Vermieter ausgestellt.\\n\\n____________________\\n[Vermieter-Name]\\n\\n[Optional: Stempel]" \
    '{ "stringValue": "Mietschuldenfreiheit" }, { "stringValue": "Bescheinigung" }, { "stringValue": "Vorlage" }' \
    "Bescheinigung über Mietschuldenfreiheit für Wohnungsbewerbungen."

# 19. SEPA-Lastschriftmandat
create_document \
    "SEPA-Lastschriftmandat Miete" \
    "mustervorlagen" \
    "SEPA-LASTSCHRIFTMANDAT\\n\\nGläubiger:\\n[Vermieter-Name]\\n[Adresse]\\nGläubiger-ID: [DE...]\\n\\nZahlungspflichtiger (Mieter):\\nName: [Mieter-Name]\\nAdresse: [Adresse]\\n\\nIch ermächtige den o.g. Zahlungsempfänger, Zahlungen von meinem Konto mittels Lastschrift einzuziehen. Zugleich weise ich mein Kreditinstitut an, die vom Zahlungsempfänger auf mein Konto gezogenen Lastschriften einzulösen.\\n\\nHinweis: Ich kann innerhalb von acht Wochen, beginnend mit dem Belastungsdatum, die Erstattung des belasteten Betrages verlangen.\\n\\nBankverbindung:\\nKreditinstitut: [Bank-Name]\\nIBAN: [DE...]\\nBIC: [...]\\n\\nMandatsreferenz: [wird vom Vermieter vergeben]\\n\\nArt der Zahlung: Wiederkehrende Zahlung\\nVerwendungszweck: Miete [Adresse]\\nBetrag: [X] EUR monatlich\\nErsteinzug: [Datum]\\n\\n[Ort], den [Datum]\\n\\n____________________\\n[Unterschrift Kontoinhaber]" \
    '{ "stringValue": "SEPA" }, { "stringValue": "Lastschrift" }, { "stringValue": "Miete" }' \
    "SEPA-Lastschriftmandat für wiederkehrende Mietzahlungen."

# 20. Hausordnung
create_document \
    "Hausordnung" \
    "mustervorlagen" \
    "HAUSORDNUNG\\n\\nfür das Gebäude [Adresse]\\n\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n\\n§ 1 ALLGEMEINES\\nDiese Hausordnung dient dem friedlichen Zusammenleben aller Bewohner und ist Bestandteil des Mietvertrags.\\n\\n§ 2 RUHEZEITEN\\nNachtruhe: 22:00 - 6:00 Uhr\\nMittagsruhe: 13:00 - 15:00 Uhr\\nSonn- und Feiertage: ganztägig\\n\\n§ 3 REINIGUNG\\nDie Reinigung des Treppenhauses erfolgt wöchentlich im Wechsel durch die Mieter gemäß Reinigungsplan / durch den Hausmeister.\\n\\n§ 4 MÜLLENTSORGUNG\\nDer Müll ist getrennt in den dafür vorgesehenen Behältern zu entsorgen. Sperrmüll ist vom Mieter selbst zu entsorgen.\\n\\n§ 5 GEMEINSCHAFTSFLÄCHEN\\nTreppenhaus, Flure und Keller sind freizuhalten. Kinderwagen und Fahrräder sind in den vorgesehenen Räumen abzustellen.\\n\\n§ 6 TIERHALTUNG\\nDie Haltung von Haustieren bedarf der vorherigen Zustimmung des Vermieters. Kleintiere sind genehmigungsfrei.\\n\\n§ 7 SCHLIESSDIENST\\nDie Haustür ist ab 20:00 Uhr geschlossen zu halten.\\n\\n§ 8 SICHERHEIT\\nDas Abstellen von feuergefährlichen Gegenständen in Fluren und Kellerräumen ist verboten.\\n\\nStand: [Datum]\\n\\n____________________\\nVermieter/Hausverwaltung" \
    '{ "stringValue": "Hausordnung" }, { "stringValue": "Mietvertrag" }, { "stringValue": "Ruhezeiten" }' \
    "Muster-Hausordnung für Mehrfamilienhäuser mit Ruhezeiten und Nutzungsregeln."

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Alle Vorlagen wurden erstellt!"
echo ""
echo "📊 Zusammenfassung:"
echo "   • Mietrecht: 6 Vorlagen"
echo "   • Kaufrecht: 2 Vorlagen"
echo "   • WEG: 2 Vorlagen"
echo "   • Schriftsätze: 3 Vorlagen"
echo "   • Makler: 2 Vorlagen"
echo "   • Vollmachten & Verträge: 5 Vorlagen"
echo "   ─────────────────────"
echo "   GESAMT: 20 Vorlagen"
echo ""
echo "🔗 Öffne https://domulex.ai/app/documents"
echo "   Wähle 'Meine Vorlagen' in der Sidebar"
