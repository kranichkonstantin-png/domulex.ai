#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch 11: Formulare, Checklisten & Musterverträge"""

import os
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# Konfiguration
QDRANT_URL = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"
COLLECTION_NAME = "legal_documents"

# Initialisierung
genai.configure(api_key=GEMINI_API_KEY)
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, https=True)

# Batch 11: Formulare, Checklisten & Musterverträge (85 Dokumente)
docs = [
    # Mietverträge Muster
    {
        "title": "Muster: Wohnraummietvertrag - Standard-Formulierung",
        "content": """Wohnraummietvertrag zwischen [Vermieter] und [Mieter]. § 1 Mietobjekt: [Adresse, Lage, Zimmer, Fläche]. § 2 Mietbeginn: [Datum], unbefristet. § 3 Miete: Kaltmiete [Betrag], Nebenkosten-Vorauszahlung [Betrag], Gesamtmiete [Betrag]. § 4 Kaution: [Betrag], max. 3 Nettokaltmieten. § 5 Schönheitsreparaturen: Nach BGH-Rechtsprechung formulieren. § 6 Kleinreparaturen: Max. [Betrag] pro Reparatur, max. [Betrag] pro Jahr. § 7 Kündigungsfristen: Gesetzlich (§ 573c BGB). § 8 Hausordnung: Anlage. § 9 Sonstiges: [Individuelle Regelungen]. Unterschriften.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Gewerbemietvertrag - Besonderheiten beachten",
        "content": """Gewerbemietvertrag zwischen [Vermieter] und [Mieter]. § 1 Mietobjekt: [Adresse], Gewerbefläche [m²], Nutzung: [Zweck]. § 2 Mietzeit: [Datum] bis [Datum], Verlängerungsoption. § 3 Miete: Nettomiete [Betrag], zzgl. USt, Nebenkosten [pauschal/nach Verbrauch]. § 4 Indexierung: Anpassung nach Verbraucherpreisindex. § 5 Kaution: [Betrag] oder Bürgschaft. § 6 Instandhaltung: Vermieter Dach/Fach, Mieter Schönheitsreparaturen. § 7 Untervermietung: Mit Zustimmung. § 8 Kündigung: [Frist, z.B. 6 Monate]. § 9 Rückbau: Bei Auszug in Ursprungszustand. Unterschriften.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Mietvertrag befristet - Zeitmietvertrag korrekt formulieren",
        "content": """Zeitmietvertrag gem. § 575 BGB. Befristung bis [Datum]. Befristungsgrund: [z.B. Eigenbedarf, Sanierung]. Konkrete Darlegung des Grundes erforderlich. Keine ordentliche Kündigung möglich. Verlängerungsoption: [Ja/Nein]. Mieter-Information: Über fehlende Kündigungsmöglichkeit belehren. Schriftform: § 550 BGB beachten. Bei Fehler: Unbefristeter Vertrag. Vor Befristungsende: Informationspflicht bei Fortsetzung (§ 575a BGB).""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Staffelmietvertrag - Mieterhöhungen vorprogrammieren",
        "content": """Staffelmietvereinbarung gem. § 557a BGB. Miete steigt zu festgelegten Zeitpunkten. Beispiel: Jahr 1-2: 800€, Jahr 3-4: 850€, ab Jahr 5: 900€. Mindestlaufzeit: Jeweils 1 Jahr gleiche Miete. Schriftform erforderlich. Keine weitere Mieterhöhung nach § 558 BGB möglich während Staffelzeit. Indexmiete ausgeschlossen. Transparenz: Alle Stufen im Vertrag angeben. Kündigung: Normal möglich trotz Staffelung.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Indexmietvertrag - Automatische Anpassung an Inflation",
        "content": """Indexmietvereinbarung gem. § 557b BGB. Miete passt sich an Verbraucherpreisindex an. Formel: Neue Miete = Alte Miete × (neuer Index / alter Index). Basisindex: [Monat/Jahr]. Anpassung: Frühestens nach 1 Jahr. Schriftform erforderlich. Keine Mieterhöhung nach § 558 BGB parallel. Staffelmiete ausgeschlossen. Vermieter: Index nachweisen (Statistisches Bundesamt). Transparenz für Mieter sicherstellen.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Wohnungsübergabe bei Einzug - Protokoll erstellen",
        "content": """Übergabeprotokoll-Checkliste: 1. Datum, Uhrzeit, Anwesende. 2. Zählerstände (Strom, Gas, Wasser, Heizung). 3. Schlüsselübergabe (Anzahl). 4. Zustand Räume: Boden, Wände, Decken, Fenster, Türen. 5. Sanitär: Armaturen, Fliesen, Dichtigkeit. 6. Küche: Einbaugeräte, Funktion. 7. Heizung: Funktion, Thermostate. 8. Mängel dokumentieren (Fotos!). 9. Vereinbarungen zu Renovierungen. 10. Unterschriften beider Parteien. Fotos als Anlage.""",
        "category": "Checklisten"
    },
    {
        "title": "Checkliste: Wohnungsübergabe bei Auszug - Streit vermeiden",
        "content": """Rückgabe-Checkliste: 1. Termin vereinbaren (Vermieter anwesend). 2. Wohnung besenrein. 3. Alle Schlüssel zurückgeben. 4. Zählerstände ablesen, notieren. 5. Zustand vergleichen mit Einzugsprotokoll. 6. Renovierungspflichten: Nach Vertrag und Rechtsprechung. 7. Mängel besprechen, dokumentieren. 8. Nachforderungen klären. 9. Kaution-Rückzahlung besprechen (Frist, Betrag). 10. Protokoll unterzeichnen. Nachsendeauftrag einrichten.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Mieterhöhungsschreiben nach § 558 BGB - Formvorschriften",
        "content": """Mieterhöhung zum [Datum]. Sehr geehrte/r [Mieter], hiermit erhöhe ich die Miete von [alt] auf [neu]. Begründung: Ortsübliche Vergleichsmiete. Mietspiegel [Stadt, Jahr]: [Spannenangabe]. Vergleichswohnungen: [Mind. 3 Wohnungen mit Details]. Zustimmungsfrist: 2 Monate ab Zugang (§ 558b BGB). Bei Ablehnung: Klage möglich. Erhöhung wirksam ab übernächstem Monat nach Zustimmung. Kappungsgrenze: Max. 20% in 3 Jahren (§ 558 Abs. 3 BGB). Mietstopp-Gebiete: 15% in 3 Jahren. Anlagen: Mietspiegel-Auszug. Mit freundlichen Grüßen.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Mängelanzeige durch Mieter - Richtig dokumentieren",
        "content": """Mängelanzeige vom [Datum]. Sehr geehrte/r [Vermieter], hiermit zeige ich folgende Mängel an: [Detaillierte Beschreibung, z.B. Schimmel im Bad, tropfender Wasserhahn]. Festgestellt am: [Datum]. Auswirkungen: [Beeinträchtigung der Nutzung]. Bitte um Beseitigung bis: [Frist, z.B. 14 Tage]. Bei Nichtbeseitigung: Mietminderung/Schadensersatz vorbehalten. Besichtigungstermin: [Vorschlag]. Fotos anbei. Mit freundlichen Grüßen, [Mieter]. Einschreiben mit Rückschein empfohlen.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Eigenbedarfskündigung - Wasserdichte Formulierung",
        "content": """Kündigung wegen Eigenbedarfs. Sehr geehrte/r [Mieter], hiermit kündige ich das Mietverhältnis ordentlich zum [Datum]. Kündigungsgrund: Eigenbedarf gem. § 573 Abs. 2 Nr. 2 BGB. Berechtigte Person: [Name, Verwandtschaftsgrad]. Nutzungsabsicht: [Detailliert: Gründe, Lebenssituation]. Vernünftige Gründe: [z.B. Beruf, Familie, Krankheit]. Härtefallprüfung: [Ggf. Sozialklausel ansprechen]. Kündigungsfrist: [3/6/9 Monate je nach Mietdauer]. Mit freundlichen Grüßen. Rechtsmittelbelehrung.""",
        "category": "Formulare"
    },
    
    # Kaufverträge
    {
        "title": "Muster: Immobilienkaufvertrag - Notarielle Beurkundung",
        "content": """Kaufvertrag über Grundstück. Verkäufer: [Name, Anschrift]. Käufer: [Name, Anschrift]. § 1 Kaufgegenstand: Grundstück [Adresse, Grundbuch Blatt, Flur, Flurstück, Größe]. § 2 Kaufpreis: [Betrag] EUR. § 3 Fälligkeit: Nach Grundbuchumschreibung und steuerlicher Unbedenklichkeit. § 4 Besitzübergang: [Datum]. § 5 Lasten: Lastenfreistellung durch Verkäufer. § 6 Gewährleistung: Gekauft wie besichtigt, Haftung nur bei Arglist. § 7 Grunderwerbsteuer: Trägt Käufer. § 8 Auflassung: Erfolgt im Anschluss. Notarielle Beurkundung gem. § 311b BGB.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Vorvertrag Immobilienkauf - Bindung vor Notar",
        "content": """Vorvertrag (Reservierungsvereinbarung). Verkäufer verpflichtet sich, Grundstück [Adresse] nur an Käufer zu verkaufen. Käufer verpflichtet sich zum Kauf. Kaufpreis: [Betrag]. Notartermin: Bis [Datum]. Anzahlung: [Betrag] auf Treuhandkonto Notar. Finanzierungsvorbehalt: Bis [Datum], [Kreditbetrag]. Rücktritt: Bei Nichterteilung Finanzierung, Anzahlung zurück. Vertragsstrafe: Bei schuldhaftem Rücktritt [Betrag oder %]. Schriftform erforderlich (§ 550 BGB analog). Notartermin-Vereinbarung.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Immobilienkauf - Vor dem Notartermin prüfen",
        "content": """Checkliste vor Kaufvertragsabschluss: 1. Grundbuchauszug prüfen (Eigentümer, Lasten, Dienstbarkeiten). 2. Baulastenverzeichnis einsehen. 3. Bebauungsplan prüfen. 4. Altlastengutachten einholen. 5. Energieausweis vorlegen lassen. 6. Teilungserklärung bei WEG lesen. 7. Protokolle der letzten Eigentümerversammlungen. 8. Mietverträge bei vermieteten Objekten. 9. Finanzierung zusagen lassen. 10. Notartermin: Vertragsentwurf vorab lesen. 11. Rückfragen notieren. 12. Kosten kalkulieren (Notar, Grunderwerbsteuer, Makler).""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Rücktritt vom Kaufvertrag - Frist und Begründung",
        "content": """Rücktritt vom Kaufvertrag vom [Datum, Notar]. Sehr geehrte/r [Vertragspartner], hiermit erkläre ich den Rücktritt vom Kaufvertrag gem. [§ 323 BGB / § 346 BGB / vertragliche Rücktrittsklausel]. Rücktrittsgrund: [z.B. Finanzierung nicht erhalten, erhebliche Mängel, Fristablauf]. Nachfrist: [Falls gesetzt, war erfolglos]. Rückabwicklung: Anzahlung zurückfordern. Grundbuchvormerkung löschen. Schadensersatz: [Falls geltend gemacht]. Frist zur Stellungnahme: [z.B. 1 Woche]. Mit freundlichen Grüßen. Einschreiben Rückschein.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Maklervertrag - Alleinauftrag klar formulieren",
        "content": """Maklervertrag (Alleinauftrag). Auftraggeber: [Verkäufer/Vermieter]. Makler: [Firma]. § 1 Auftrag: Vermittlung [Verkauf/Vermietung] von [Objekt]. § 2 Laufzeit: [Datum] bis [Datum], Verlängerung bei Nichtkündigung. § 3 Alleinauftrag: Auftraggeber darf keine anderen Makler beauftragen. § 4 Provision: [%] des Kaufpreises/Jahresmiete, fällig bei Vertragsabschluss. § 5 Pflichten Makler: Exposé, Besichtigungen, Bonitätsprüfung. § 6 Kündigung: [Frist]. § 7 Datenschutz: DSGVO-konform. Unterschriften.""",
        "category": "Formulare"
    },
    
    # WEG Dokumente
    {
        "title": "Muster: Einladung zur Eigentümerversammlung - Formvorschriften",
        "content": """Einladung zur ordentlichen Eigentümerversammlung. Sehr geehrte Eigentümer, hiermit lade ich zur Versammlung ein. Termin: [Datum, Uhrzeit]. Ort: [Adresse]. Tagesordnung: 1. Feststellung Beschlussfähigkeit. 2. Bericht Verwalter. 3. Beschlussfassung Wirtschaftsplan [Jahr]. 4. Jahresabrechnung [Jahr]. 5. Instandsetzungsmaßnahmen [Details]. 6. Sonstiges. Ladungsfrist: Mind. 2 Wochen (§ 24 Abs. 4 WEG). Unterlagen: Anbei/Einsicht Verwaltung. Vollmacht: Möglich mit Formular. Mit freundlichen Grüßen, [Verwalter].""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Beschlussprotokoll Eigentümerversammlung - Rechtssicher",
        "content": """Protokoll der Eigentümerversammlung vom [Datum]. Anwesende: [Liste mit Miteigentumsanteilen]. Beschlussfähigkeit: [Ja, %]. TOP 1: Feststellung Beschlussfähigkeit (einstimmig). TOP 2: Wirtschaftsplan [Jahr] - Beschluss: Angenommen mit [Stimmen], Gegenstimmen [Anzahl], Enthaltungen [Anzahl]. TOP 3: Instandsetzung Dach für [Betrag] - Beschluss: Angenommen (einfache Mehrheit). Widerspruch: [Name] widerspricht zu Protokoll. Anfechtungsfrist: 4 Wochen. Protokollführer: [Name]. Unterschrift Versammlungsleiter.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Anfechtungsklage gegen WEG-Beschluss - Frist einhalten",
        "content": """Anfechtungsklage gem. § 45 WEG. Kläger: [Eigentümer]. Beklagte: Wohnungseigentümergemeinschaft [Adresse]. Angefochtener Beschluss: [Datum, TOP, Inhalt]. Anfechtungsgründe: [§ 46 WEG - z.B. fehlende Beschlussfähigkeit, fehlerhafte Ladung, Verstoß gegen Gesetz]. Antrag: Beschluss für ungültig erklären. Frist: 4 Wochen ab Beschlussfassung (1 Monat). Zuständigkeit: Amtsgericht [Ort]. Schriftsatz mit Begründung. Rechtsanwalt empfohlen.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: WEG-Verwalter beauftragen - Worauf achten?",
        "content": """Verwalter-Auswahl-Checkliste: 1. Qualifikation: IHK-Zertifikat, Berufserfahrung. 2. Referenzen: Andere WEGs befragen. 3. Leistungsumfang: Hausgeld-Einzug, Abrechnungen, Instandhaltung, Versammlungen. 4. Kosten: Verwaltervergütung pro Einheit/Jahr. 5. Vertragslaufzeit: 1-3 Jahre üblich. 6. Kündigung: Fristen prüfen. 7. Haftpflichtversicherung: Deckungssumme mind. 500.000€. 8. Software: Moderne Hausverwaltungssoftware. 9. Erreichbarkeit: Bürozeiten, Notfallkontakt. 10. Persönlicher Eindruck: Vertrauenswürdigkeit.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Wirtschaftsplan WEG - Jährliche Planung",
        "content": """Wirtschaftsplan für [Jahr]. Gemeinschaftseigentum [Adresse]. Einnahmen: Hausgeld-Vorauszahlungen [Betrag]. Ausgaben: 1. Instandhaltung [Betrag]. 2. Betriebskosten (Strom, Wasser, Müll) [Betrag]. 3. Verwaltung [Betrag]. 4. Versicherungen [Betrag]. 5. Heizung/Warmwasser [Betrag]. 6. Reparaturrücklage-Zuführung [Betrag]. Gesamt-Ausgaben: [Betrag]. Umlageschlüssel: Nach Miteigentumsanteilen (§ 16 Abs. 2 WEG). Beschluss erforderlich. Bei Über-/Unterschreitung: Nachzahlung/Gutschrift in Abrechnung.""",
        "category": "Formulare"
    },
    
    # Bauverträge
    {
        "title": "Muster: Werkvertrag nach BGB - Einfacher Bauauftrag",
        "content": """Werkvertrag. Auftraggeber: [Name]. Auftragnehmer: [Handwerker]. § 1 Leistung: [Detaillierte Beschreibung Bauleistung]. § 2 Vergütung: [Betrag] EUR inkl. MwSt. § 3 Zahlungsweise: Nach Abnahme / Abschläge nach Baufortschritt. § 4 Ausführungsfrist: Bis [Datum]. § 5 Vertragsstrafe: Bei Verzug [Betrag] pro Tag. § 6 Abnahme: Förmlich nach Fertigmeldung. § 7 Gewährleistung: 5 Jahre (§ 634a BGB). § 8 Sicherheit: [Bürgschaft 5%]. Unterschriften.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Bauvertrag nach VOB/B - Größere Bauvorhaben",
        "content": """Bauvertrag nach VOB/B. Auftraggeber: [Name]. Auftragnehmer: [Baufirma]. § 1 Vertragsgegenstand: [Bauleistung nach Leistungsverzeichnis]. § 2 Vertragsgrundlagen: VOB/B, Leistungsverzeichnis, Pläne. § 3 Vergütung: [Betrag] nach Aufmaß. § 4 Ausführungsfrist: [Beginn] bis [Ende]. § 5 Vertragsstrafe: § 11 VOB/B, [Betrag/Tag]. § 6 Abschlagszahlungen: § 16 VOB/B. § 7 Abnahme: § 12 VOB/B. § 8 Sicherheitsleistung: § 17 VOB/B, 5% Bürgschaft. § 9 Gewährleistung: 4 Jahre (§ 13 VOB/B). Unterschriften.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Abnahmeprotokoll - Mängel festhalten",
        "content": """Abnahmeprotokoll vom [Datum]. Objekt: [Adresse]. Auftraggeber: [Name]. Auftragnehmer: [Firma]. Leistung: [Beschreibung]. Abnahme: [Erfolgt / Verweigert]. Festgestellte Mängel: 1. [Beschreibung, Ort, Schwere]. 2. [weitere Mängel]. Frist zur Mängelbeseitigung: [Datum]. Vorbehalt: Versteckte Mängel vorbehalten. Gewährleistungsfrist: Beginnt mit Abnahme. Restzahlung: Nach Mängelbeseitigung [Betrag]. Unterschriften Auftraggeber und Auftragnehmer. Fotos als Anlage.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Bauabnahme - Schritt für Schritt",
        "content": """Abnahme-Checkliste: 1. Termin mit Handwerker vereinbaren. 2. Experten hinzuziehen (Architekt, Sachverständiger). 3. Vertrag und Leistungsverzeichnis bereithalten. 4. Alle Räume begehen, Funktionen prüfen. 5. Mängel notieren (Art, Ort, Schwere). 6. Fotos von Mängeln. 7. Wesentliche Mängel: Abnahme verweigern. 8. Unwesentliche Mängel: Abnahme mit Vorbehalt. 9. Frist zur Mängelbeseitigung setzen. 10. Protokoll unterschreiben (beide Parteien). 11. Kopie für Unterlagen. 12. Gewährleistungsfrist beginnt.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Nachtragsangebot - Mehrkosten transparent",
        "content": """Nachtragsangebot Nr. [X] vom [Datum]. Auftraggeber: [Name]. Auftragnehmer: [Firma]. Ursprungsauftrag: [Vertrag vom Datum]. Änderung: [Beschreibung der geänderten/zusätzlichen Leistung]. Begründung: [z.B. Auftraggeber-Wunsch, unvorhergesehene Umstände]. Mehrkosten: Position [Nr.]: [Beschreibung] - [Betrag]. Summe Nachtrag: [Betrag] EUR zzgl. MwSt. Auswirkung Fertigstellungstermin: [Verzögerung um X Tage]. Annahme bis: [Datum]. Bei Annahme: Unterschrift. Ohne Annahme: Nachtrag nicht ausgeführt.""",
        "category": "Formulare"
    },
    
    # Weitere Formulare
    {
        "title": "Muster: Vollmacht Grundstücksverkauf - Notariell beglaubigt",
        "content": """Vollmacht. Vollmachtgeber: [Name, Geburtsdatum, Adresse]. Bevollmächtigter: [Name, Adresse]. Hiermit bevollmächtige ich zur Veräußerung meines Grundstücks [Grundbuch, Flurstück]. Umfang: Verhandlung, Vertragsabschluss, Auflassung, Grundbuchanträge. Kaufpreis: Mind. [Betrag]. Widerruflichkeit: [Widerruflich/Unwiderruflich]. Untervollmacht: [Erlaubt/Nicht erlaubt]. Diese Vollmacht bedarf notarieller Beglaubigung (§ 29 GBO). Datum, Unterschrift Vollmachtgeber. Notarielle Beglaubigung.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Widerrufsbelehrung - Verbraucherschutz",
        "content": """Widerrufsbelehrung nach § 355 BGB. Sie haben das Recht, binnen 14 Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen. Widerrufsfrist: 14 Tage ab [Vertragsschluss / Warenerhalt]. Form: Mitteilung (Brief, E-Mail) an [Adresse]. Muster-Widerrufsformular: [Anhang]. Folgen: Erhaltene Leistungen zurückgewähren binnen 14 Tagen. Ausnahmen: [z.B. notarielle Verträge sind ausgenommen]. Vorzeitige Erfüllung: Mit ausdrücklicher Zustimmung erlischt Widerrufsrecht.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Datenschutzerklärung Immobilienmakler - DSGVO-konform",
        "content": """Datenschutzerklärung gem. Art. 13 DSGVO. Verantwortlicher: [Maklerfirma, Adresse]. Datenverarbeitung: Name, Kontaktdaten, Bonitätsinformationen für Vermittlung. Rechtsgrundlage: Vertragsanbahnung (Art. 6 Abs. 1 lit. b DSGVO), Einwilligung (lit. a). Empfänger: Vertragspartner (Verkäufer/Vermieter), Banken. Speicherdauer: 3 Jahre nach Vertragsende. Ihre Rechte: Auskunft, Berichtigung, Löschung, Widerspruch. Beschwerderecht: Datenschutzbehörde. Datenschutzbeauftragter: [Kontakt].""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Immobilienverkauf - Von Bewertung bis Übergabe",
        "content": """Verkaufs-Checkliste: 1. Immobilienbewertung (Gutachten/Makler). 2. Unterlagen sammeln: Grundbuchauszug, Energieausweis, Baupläne, Grundrisse. 3. Verkaufsstrategie: Privat oder Makler? 4. Exposé erstellen: Fotos, Beschreibung, Preis. 5. Vermarktung: Portale, Anzeigen. 6. Besichtigungen organisieren. 7. Bonitätsprüfung Interessenten. 8. Kaufpreis verhandeln. 9. Notartermin vereinbaren. 10. Vertragsentwurf prüfen. 11. Kaufpreis-Eingang abwarten. 12. Übergabe mit Protokoll. 13. Finanzamt informieren (Spekulationsfrist).""",
        "category": "Checklisten"
    },
    {
        "title": "Checkliste: Immobilienkauf Finanzierung - Kredit richtig planen",
        "content": """Finanzierungs-Checkliste: 1. Eigenkapital ermitteln (mind. 20% + Nebenkosten). 2. Einnahmen-Ausgaben-Rechnung. 3. Finanzierungsbedarf berechnen. 4. Kreditangebote vergleichen (mind. 3 Banken). 5. Zinsbindung wählen (10/15/20 Jahre). 6. Tilgungssatz festlegen (mind. 2%). 7. Sondertilgungen vereinbaren. 8. KfW-Förderung prüfen. 9. Wohn-Riester nutzen? 10. Bereitstellungszinsen vermeiden. 11. Finanzierungszusage einholen. 12. Kreditvertrag prüfen. 13. Grundschuld eintragen lassen.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Mietschuldenfreiheitsbescheinigung - Für Neuvermietung",
        "content": """Mietschuldenfreiheitsbescheinigung. Vermieter: [Name, Adresse]. Mieter: [Name]. Mietobjekt: [Adresse]. Mietzeit: [Von Datum] bis [Datum]. Hiermit bestätige ich, dass der o.g. Mieter keine Mietrückstände hat. Miete wurde stets pünktlich gezahlt. Kaution: [Betrag] wurde vollständig zurückgezahlt. Wohnung wurde ordnungsgemäß übergeben. Keine offenen Forderungen. Datum, Unterschrift Vermieter. Verwendung: Vorlage bei neuem Vermieter.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Selbstauskunft Mieter - Was darf abgefragt werden?",
        "content": """Mieter-Selbstauskunft. Name, Vorname: []. Geburtsdatum: []. Aktueller Wohnort: []. Beruf/Arbeitgeber: []. Nettoeinkommen: [] (DSGVO: Freiwillig, aber üblich). Anzahl Personen im Haushalt: []. Haustiere: []. Vorvermieter-Kontakt: []. Mietschuldenfreiheit: [Ja/Nein]. SCHUFA-Auskunft: [Anlage]. Einwilligung Bonitätsprüfung: Ja []. Datenschutz: Daten nur für Vermietungsentscheidung. Datum, Unterschrift. Hinweis: Unzulässige Fragen (Religion, Schwangerschaft, Krankheiten) nicht beantworten.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Untermieterlaubnis - Teilweise Untervermietung",
        "content": """Erlaubnis zur Untervermietung. Vermieter: [Name]. Hauptmieter: [Name]. Mietobjekt: [Adresse]. Hiermit erlaube ich die Untervermietung von [Zimmer/Teil der Wohnung] an [Name Untermieter]. Zeitraum: [Von] bis []. Untermiete: [Betrag] (max. Kostenanteil). Bedingungen: 1. Hauptmieter bleibt Vertragspartner. 2. Untermieter an Hausordnung gebunden. 3. Keine Weitervermietung. 4. Widerruf bei Verstößen vorbehalten. Datum, Unterschrift Vermieter. Zustimmung kann nicht willkürlich verweigert werden (§ 553 BGB).""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Kündigung Wohnraummietvertrag (Mieter) - Ordentlich",
        "content": """Kündigung des Mietverhältnisses. Mieter: [Name, Adresse]. Vermieter: [Name, Adresse]. Mietobjekt: [Adresse]. Hiermit kündige ich das Mietverhältnis ordentlich zum [Datum]. Kündigungsfrist: 3 Monate zum Monatsende (§ 573c BGB). Wohnungsrückgabe: [Datum], Uhrzeit nach Vereinbarung. Übergabeprotokoll: Bitte Termin vorschlagen. Nachsendeauftrag: [Neue Adresse]. Kaution-Rückzahlung: Bitte auf Konto [IBAN]. Datum, Unterschrift. Zugang: Einschreiben oder persönlich mit Empfangsbestätigung.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Nebenkostenabrechnung prüfen - Fehler erkennen",
        "content": """NK-Abrechnungs-Check: 1. Abrechnungszeitraum: 12 Monate? 2. Frist: Binnen 12 Monaten erhalten (§ 556 Abs. 3 BGB)? 3. Formell korrekt: Gesamtkosten, Verteilerschlüssel, Einzelabrechnung? 4. Umlagefähige Kosten: Gem. BetrKV oder Vertrag? 5. Nicht umlegbar: Verwaltungskosten, Reparaturen. 6. Abrechnungsspitze plausibel? 7. Einzelposten: Verbrauchswerte realistisch? 8. Belege anfordern (§ 556 Abs. 3 S. 2 BGB). 9. Wirtschaftlichkeitsgebot geprüft? 10. Einspruch binnen 12 Monaten. 11. Bei Fehlern: Kürzung/Widerspruch.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Widerspruch Nebenkostenabrechnung - Fehler rügen",
        "content": """Widerspruch gegen Nebenkostenabrechnung. Vermieter: [Name]. Mieter: [Name]. Abrechnungszeitraum: [Jahr]. Eingang: [Datum]. Hiermit widerspreche ich der NK-Abrechnung. Begründung: 1. [Position X] nicht umlegbar (z.B. Reparatur statt Wartung). 2. [Position Y] überhöht (Vorjahr: [Betrag]). 3. Verteilerschlüssel falsch (Wohnfläche [m²] statt [m²]). Beleg-Anforderung: Bitte Originalbelege vorlegen. Nachforderung: Wird nicht gezahlt bis Klärung. Frist: 2 Wochen zur Korrektur. Datum, Unterschrift. Ausschlussfrist: 12 Monate beachten.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Antrag auf Mietminderung - Schriftlich ankündigen",
        "content": """Antrag auf Mietminderung. Vermieter: [Name]. Mieter: [Name]. Mietobjekt: [Adresse]. Bezug: Mängelanzeige vom [Datum]. Mangel: [Beschreibung]. Da Mangel nicht beseitigt wurde, mindere ich die Miete ab [Monat] um [%]. Berechnung: Kaltmiete [Betrag] - Minderung [%] = [Betrag]. Rückforderung: Für Zeitraum [Monate] = [Betrag]. Zahlung: Geminderte Miete bis Beseitigung. Bei Klärung: Nachzahlung vorbehalten. Datum, Unterschrift. Vorsicht: Nicht zu viel mindern (Kündigungsgefahr).""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Schönheitsreparaturen - Was muss gestrichen werden?",
        "content": """Schönheitsreparaturen-Check: 1. Vertrag prüfen: Klausel wirksam? (BGH-Rechtsprechung). 2. Unwirksam: Starre Fristen, unrenoviert übernommen, quotale Beteiligung. 3. Wirksam: Flexibel formuliert, renoviert übernommen. 4. Umfang: Tapezieren, Streichen Wände/Decken, Heizkörper/Türen/Fenster (innen). 5. Fußboden: Versiegelung/Pflege (nicht erneuern). 6. Nicht: Fenster außen, Fassade, Gemeinschaftsräume. 7. Bei Auszug: Zustand mit Einzug vergleichen (Protokoll!). 8. Abnutzung: Normal für Mietdauer. 9. Streit: Gutachten einholen.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Besichtigungsvereinbarung bei laufendem Mietverhältnis",
        "content": """Besichtigungstermin bei Verkauf/Neuvermietung. Vermieter: [Name]. Mieter: [Name]. Mietobjekt: [Adresse]. Grund: [Verkauf / Neuvermietung]. Termine: [Datum, Uhrzeit] - [weitere Termine]. Dauer: Ca. 15-30 Min pro Besichtigung. Anzahl Interessenten: [Max. X Personen]. Mieter-Rechte: Ankündigung mind. 24h vorher. Anwesenheit Mieter erwünscht. Rücksichtnahme: Termine nach Arbeitszeit bevorzugt. Gegenleistung: [ggf. Mietminderung für Aufwand]. Datum, Einverständnis Mieter. § 535 BGB: Duldungspflicht bei berechtigtem Interesse.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Räumungsklage - Wenn Mieter nicht auszieht",
        "content": """Räumungsklage. Kläger: [Vermieter]. Beklagter: [Mieter]. Mietobjekt: [Adresse]. Klagantrag: 1. Räumung und Herausgabe der Wohnung. 2. Zahlung rückständiger Miete [Betrag]. 3. Kosten. Begründung: Kündigung vom [Datum] wegen [Grund]. Kündigungsfrist abgelaufen. Mieter verweigert Auszug. Zustellung Kündigung: [Nachweis]. Rechtsgültigkeit: Kündigung wirksam. Vollstreckung: Nach Urteil mit Gerichtsvollzieher. Zuständigkeit: Amtsgericht [Ort]. Anwaltszwang: Nein (bis 5.000€ Streitwert), aber empfohlen.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Hausbau Planung - Von Grundstück bis Einzug",
        "content": """Hausbau-Checkliste: 1. Grundstück finden, kaufen. 2. Bebauungsplan prüfen. 3. Bodengutachten. 4. Architekt beauftragen. 5. Bauantrag stellen. 6. Baugenehmigung abwarten. 7. Finanzierung final zusagen lassen. 8. Bauunternehmen auswählen (Angebote vergleichen). 9. Bauvertrag (VOB/B empfohlen). 10. Baubeginn. 11. Baubegleitung (Architekt/Gutachter). 12. Bauabnahme. 13. Mängel beseitigen. 14. Einzug. 15. Gewährleistungsfrist überwachen. Puffer: Zeit +30%, Kosten +15%.""",
        "category": "Checklisten"
    },
    {
        "title": "Checkliste: Denkmalgeschützte Immobilie kaufen - Besonderheiten",
        "content": """Denkmalschutz-Checkliste: 1. Denkmalstatus prüfen (Denkmalliste). 2. Auflagen Denkmalschutzbehörde erfragen. 3. Sanierungskosten kalkulieren (oft höher). 4. Architekt mit Denkmalerfahrung. 5. Baugenehmigung: Abstimmung mit Behörde. 6. Förderung: Denkmal-AfA (§ 7i, 10f EStG). 7. KfW-Programme prüfen. 8. Energetische Sanierung: Eingeschränkt. 9. Verkehrswert: Einfluss auf Finanzierung. 10. Laufende Kosten: Instandhaltung teurer. 11. Kaufpreis: Oft günstiger wegen Auflagen. 12. Steuerberater: AfA optimieren.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Antrag auf Vorkaufsrecht (Gemeinde) - Negativattest einholen",
        "content": """Antrag auf Auskunft über gemeindliches Vorkaufsrecht. Antragsteller: [Käufer/Notar]. Grundstück: [Grundbuch, Flurstück, Adresse]. Beabsichtigter Kaufvertrag: [Kaufpreis, Datum]. Gem. § 24 BauGB bitte ich um Auskunft: Besteht ein Vorkaufsrecht der Gemeinde? Falls ja: Wird es ausgeübt? Frist: 2 Monate ab Anzeige (§ 28 BauGB). Bitte um Negativattest oder Ausübungserklärung. Bei Nichtausübung: Kaufvertrag wird wirksam. Anlagen: Kaufvertragsentwurf, Flurkarte. Zuständigkeit: Bauamt [Gemeinde].""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Vermietete Immobilie kaufen - Rechtsnachfolge beachten",
        "content": """Kauf mit Bestandsmietern-Checkliste: 1. Mietverträge vorlegen lassen, prüfen. 2. Mieteinnahmen realistisch? Zahlungsmoral? 3. Kündigungsschutz: Sind Kündigungen möglich? 4. Mietrückstände? 5. Kautionen: Übergang auf Käufer (§ 566a BGB). 6. Betriebskosten: Abrechnungen prüfen. 7. Schriftliche Mitteilung an Mieter über Eigentümerwechsel. 8. Miete auf neues Konto umleiten. 9. Instandhaltungsrückstand: Vor Kauf prüfen. 10. Rendite: Nach Abzug Instandhaltung, Leerstand. 11. Eigenbedarfskündigung: Fristen (§ 573 BGB).""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Mietaufhebungsvertrag - Einvernehmliche Beendigung",
        "content": """Aufhebungsvertrag. Vermieter: [Name]. Mieter: [Name]. Mietobjekt: [Adresse]. Mietbeginn: [Datum]. Hiermit heben wir das Mietverhältnis einvernehmlich auf. Beendigungsdatum: [Datum]. Rückgabe: [Termin Übergabe]. Zustand: Besenrein, ohne Schönheitsreparaturen (Vereinbarung). Kaution: Rückzahlung [Betrag] binnen [Frist] nach Übergabe. Offene Forderungen: Keine / [Auflistung]. Abfindung: [Falls gezahlt, Betrag]. Kündigungsfristen: Entfallen durch Aufhebung. Datum, Unterschriften beider Parteien.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Bauträgervertrag - Kauf vom Bauträger absichern",
        "content": """Bauträgervertrag gem. MaBV. Bauträger: [Firma]. Erwerber: [Name]. Objekt: [Adresse, Wohnung Nr., Größe]. § 1 Kaufpreis: [Betrag]. § 2 Zahlungsplan: Nach § 3 MaBV in 7 Raten. § 3 Fertigstellung: [Datum]. § 4 Sicherheit: Fertigstellungsbürgschaft/Versicherung. § 5 Bauplan, Baubeschreibung: Vertragsbestandteil. § 6 Gewährleistung: 5 Jahre ab Abnahme. § 7 Besitzübergang: Nach Abnahme. § 8 Beurkundung: Notariell gem. § 311b BGB. Anlagen: Baupläne, Ausstattungsliste. Unterschriften, Notar.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Bauträger-Immobilie kaufen - Risiken minimieren",
        "content": """Bauträger-Kauf-Checkliste: 1. Bauträger-Reputation prüfen (Referenzen, Insolvenzrisiko). 2. Vertrag von Anwalt prüfen lassen. 3. Fertigstellungstermin realistisch? 4. Sicherheit: Bürgschaft/Versicherung gem. § 7 MaBV. 5. Zahlungsplan: Nicht vor Baufortschritt zahlen. 6. Baubeschreibung: Detailliert, verbindlich. 7. Musterrechte: Abweichungen? 8. Gewährleistung: 5 Jahre ab Abnahme. 9. Abnahme: Mit Sachverständigem. 10. Finanzierung: Bereitstellungszinsen minimieren. 11. Objektbegehungen während Bau. 12. Versicherungen (Gebäude) ab Besitzübergang.""",
        "category": "Checklisten"
    },
    {
        "title": "Muster: Bestellung Grundschuld - Kreditabsicherung",
        "content": """Grundschuldbestellungsurkunde. Grundstückseigentümer: [Name]. Grundstück: [Grundbuch Blatt, Flurstück]. Zugunsten: [Bank]. Grundschuldbetrag: [EUR]. Zinsen: [% p.a.]. Nebenforderungen: Kosten der Zwangsvollstreckung. Zweck: Sicherung Darlehen vom [Datum], [Betrag]. Unterwerfung: Sofortige Zwangsvollstreckung in Grundstück (§ 800 ZPO). Briefgrundschuld / Buchgrundschuld. Rangvorbehalt: [Ja/Nein]. Eintragungsbewilligung. Notarielle Beurkundung erforderlich. Grundbuchantrag durch Notar.""",
        "category": "Formulare"
    },
    {
        "title": "Muster: Löschungsbewilligung Grundschuld - Nach Kredittilgung",
        "content": """Löschungsbewilligung. Grundschuldgläubiger: [Bank]. Grundstückseigentümer: [Name]. Grundstück: [Grundbuch Blatt, Flurstück, Abt. III Nr.]. Grundschuld: [Betrag EUR]. Hiermit bewillige ich die Löschung der Grundschuld. Grund: Darlehen vollständig getilgt. Eintragungsbewilligung gem. § 19 GBO. Notarielle Beglaubigung oder öffentlich beglaubigt. Kosten Löschung: [Grundbuchamt-Gebühr ca. 0,2% Grundschuld]. Antrag: Durch Eigentümer beim Grundbuchamt. Dauer: 4-8 Wochen.""",
        "category": "Formulare"
    },
    {
        "title": "Checkliste: Zwangsversteigerung mitbieten - Chancen und Risiken",
        "content": """Zwangsversteigerungs-Checkliste: 1. Versteigerungstermin (Amtsgericht) recherchieren. 2. Gutachten lesen (online verfügbar). 3. Objekt besichtigen (Termine beim Gericht). 4. Grundbuchauszug prüfen (Rechte bleiben teilweise!). 5. Verkehrswert: Mindestgebot 7/10 (§ 85a ZVG). 6. Finanzierung: Vor Termin zusagen lassen. 7. Sicherheit: 10% Bareinzahlung bei Zuschlag. 8. Bieten: Schrittweise, Limit setzen. 9. Zuschlag: Sofort wirksam, bindend. 10. Restzahlung: 4-6 Wochen. 11. Eigentumsübergang: Mit Zahlung. 12. Räumung: Ggf. Zwangsräumung beantragen. Risiko: Versteckte Mängel.""",
        "category": "Checklisten"
    }
]

def generate_embedding(text):
    """Generiere Embedding für Text"""
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']

def seed_batch():
    """Füge Batch 11 Dokumente hinzu"""
    print("🚀 BATCH 11: FORMULARE & MUSTERVERTRÄGE - START")
    print(f"📦 {len(docs)} Dokumente werden verarbeitet...")
    print("=" * 60)
    
    # Zähle Dokumente vorher
    try:
        collections = client.get_collections()
        collection_exists = any(c.name == COLLECTION_NAME for c in collections.collections)
        if collection_exists:
            count_before = client.count(collection_name=COLLECTION_NAME).count
            print(f"Dokumente vorher: {count_before}")
    except:
        count_before = 0
    
    erfolg = 0
    fehler = 0
    
    # Hole höchste ID
    try:
        search_result = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1,
            with_vectors=False,
            with_payload=False,
            order_by="id"
        )
        if search_result[0]:
            start_id = max([p.id for p in search_result[0]]) + 1
        else:
            start_id = 1
    except:
        start_id = 1
    
    for idx, doc in enumerate(docs, start=start_id):
        try:
            combined_text = f"{doc['title']} {doc['content']}"
            embedding = generate_embedding(combined_text)
            
            point = PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "title": doc["title"],
                    "content": doc["content"],
                    "category": doc["category"],
                    "source": "Batch 11 - Formulare & Musterverträge"
                }
            )
            
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[point]
            )
            
            erfolg += 1
            if erfolg % 10 == 0:
                print(f"✅ {erfolg}/{len(docs)}: {doc['title'][:50]}...")
                
        except Exception as e:
            fehler += 1
            print(f"❌ Fehler bei {doc['title']}: {str(e)}")
    
    # Zähle Dokumente nachher
    try:
        count_after = client.count(collection_name=COLLECTION_NAME).count
        print(f"\nDokumente nachher: {count_after}")
    except:
        count_after = count_before + erfolg
    
    print("=" * 60)
    print(f"✅ Erfolgreich: {erfolg}/{len(docs)}")
    print(f"❌ Fehlgeschlagen: {fehler}")
    print(f"\n🎯 GESAMT DOKUMENTE: {count_after}")
    print(f"📊 Noch {10000 - count_after} bis zur 10.000!")
    print(f"🔥 Fortschritt: {count_after/100:.1f}%")
    print("\n🔥 BATCH 11 COMPLETE! 🔥")

if __name__ == "__main__":
    seed_batch()
