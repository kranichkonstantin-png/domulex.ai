#!/usr/bin/env python3
"""Batch 1: Vertragsrecht Details - 50 Dokumente"""

import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai
import uuid

# Qdrant Cloud Setup
QDRANT_URL = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)
client = QdrantClient(url=f"https://{QDRANT_URL}", api_key=QDRANT_API_KEY, timeout=60)

documents = [
    {
        "title": "Mietvertrag: Schönheitsreparaturen im Detail",
        "content": """Schönheitsreparaturen sind renovierungsarbeiten, die durch normale Abnutzung entstehen. Tapezieren, Streichen von Wänden/Decken/Heizkörpern/Türen/Fenstern. Unwirksame Klauseln: Pauschalabgeltung bei Auszug, Quotenabgeltung, starre Fristenregelung. Wirksame Formulierung: 'Der Mieter ist verpflichtet, Schönheitsreparaturen fachgerecht ausführen zu lassen.' BGH: Renovierung nur bei tatsächlicher Notwendigkeit. Farbwahl: Mieter darf neutrale Farbtöne wählen. Vermieter muss unrenoviert übergeben haben.""",
        "category": "Mietrecht",
        "subcategory": "Schönheitsreparaturen"
    },
    {
        "title": "Mietvertrag: Nebenkostenabrechnung Fristen",
        "content": """Abrechnungsfrist: Spätestens 12 Monate nach Abrechnungszeitraum (§ 556 Abs. 3 BGB). Verspätete Abrechnung: Nachforderung ausgeschlossen. Mieter-Einwendungsfrist: 12 Monate nach Zugang. Abrechnungszeitraum: i.d.R. Kalenderjahr. Formelle Anforderungen: Zusammenstellung der Gesamtkosten, Verteilerschlüssel, Einzelberechnung pro Wohnung. Belegpflicht: Mieter kann Belegeinsicht verlangen. Schätzung nur bei fehlendem Zähler.""",
        "category": "Mietrecht",
        "subcategory": "Nebenkostenabrechnung"
    },
    {
        "title": "Kaufvertrag: Gewährleistungsausschluss bei Altbau",
        "content": """Gewährleistungsausschluss bei Gebrauchtimmobilien grundsätzlich zulässig. 'Gekauft wie gesehen' = wirksam bei Privatverkäufer. Arglistig verschwiegene Mängel: Ausschluss unwirksam (§ 444 BGB). Unternehmer-Verkauf: Ausschluss nur eingeschränkt möglich. Verjährung: 5 Jahre bei Bauwerken, 2 Jahre bei beweglichen Sachen. Beweislastumkehr ersten 6 Monate. Wichtig: Baubeschreibung überprüfen, Gutachten einholen.""",
        "category": "Kaufrecht",
        "subcategory": "Gewährleistung"
    },
    {
        "title": "Maklervertrag: Provisionshöhe und Fälligkeit",
        "content": """Provisionshöhe frei verhandelbar, üblich 3,57% inkl. MwSt. (je Partei bei Wohnimmobilien nach Bestellerprinzip). Fälligkeit: Mit Wirksamwerden des Hauptvertrags (notarielle Beurkundung + Kaufpreiszahlung). Nachweismakler: Nur bei Nachweis ohne Vermittlung, niedrigere Provision. Alleinauftrag: Höhere Erfolgschance, oft niedrigere Provision. Staffelprovision: Nach Verkaufspreis gestaffelt möglich.""",
        "category": "Maklerrecht",
        "subcategory": "Provision"
    },
    {
        "title": "Kaufvertrag: Rücktrittsrechte des Käufers",
        "content": """Rücktritt bei wesentlicher Pflichtverletzung (§ 323 BGB). Finanzierungsvorbehalt: Muss konkret formuliert sein, Frist setzen. Genehmigungsvorbehalt: Bei Vorkaufsrecht, Denkmalschutz. Mängel: Fristsetzung zur Nacherfüllung, dann Rücktritt. Rückabwicklung: Rückübertragung gegen Kaufpreisrückzahlung. Schadensersatz zusätzlich möglich. Notar-Kosten: Trägt i.d.R. zurücktretende Partei.""",
        "category": "Kaufrecht",
        "subcategory": "Rücktritt"
    },
    {
        "title": "Mietvertrag: Betriebskostenvorauszahlung Anpassung",
        "content": """Anpassung nach § 560 BGB analog oder vertraglicher Regelung. Erhöhung: Nur bei nachweislich gestiegenen Kosten. Senkung: Bei deutlich niedrigeren Kosten Anspruch des Mieters. Formerfordernis: Textform ausreichend. Berechnungsgrundlage: Letzte Abrechnung oder begründete Prognose. Änderung jederzeit möglich. Empfehlung: Nach jeder Abrechnung prüfen und anpassen.""",
        "category": "Mietrecht",
        "subcategory": "Betriebskosten"
    },
    {
        "title": "Kaufvertrag: Kaufpreisfälligkeit und Verzug",
        "content": """Fälligkeit: Nach Kaufvertrag, meist Zug-um-Zug gegen Besitzübergabe. Verzugszinsen: 5% über Basiszinssatz (Verbraucher), 9% (Unternehmer). Verzug: Ab Mahnung oder Fälligkeit bei Kalenderdatum. Sicherung: Notaranderkonto, Treuhandkonto. Zahlung vor Eigentumsumschreibung: Auflassungsvormerkung schützt Käufer. Ratenzahlung: Nur mit ausdrücklicher Vereinbarung.""",
        "category": "Kaufrecht",
        "subcategory": "Kaufpreis"
    },
    {
        "title": "Mietvertrag: Staffelmiete Gestaltung",
        "content": """Staffelmiete nach § 557a BGB: Miete steigt zu festgelegten Zeitpunkten. Mindestlaufzeit pro Stufe: 1 Jahr. Schriftformerfordernis: Mieterhöhung muss im Vertrag stehen. Kappungsgrenze: Gilt nicht bei Staffelmiete. Indexmiete parallel: Nicht zulässig. Modernisierungsumlage: Zusätzlich möglich. Kündigung: Ordentliche Kündigung frühestens 4 Jahre nach Vertragsschluss.""",
        "category": "Mietrecht",
        "subcategory": "Staffelmiete"
    },
    {
        "title": "Kaufvertrag: Besitzübergabe Zeitpunkt",
        "content": """Besitzübergabe meist Zug-um-Zug gegen Kaufpreiszahlung. Protokoll: Übergabeprotokoll mit Zählerständen, Schlüsseln, Mängeln. Risiko: Ab Besitzübergabe trägt Käufer Betriebskosten und Verkehrssicherungspflicht. Frühere Übergabe: Nur mit Vereinbarung, Risiko beim Käufer. Nutzungsentschädigung: Bei verzögerter Übergabe. Versicherung: Ab Übergabe Käufer, vorher Verkäufer.""",
        "category": "Kaufrecht",
        "subcategory": "Besitzübergabe"
    },
    {
        "title": "Mietvertrag: Tierhaltung Rechtslage",
        "content": """Kleintiere (Hamster, Fische): Erlaubnisfrei. Hunde/Katzen: Einzelfallabwägung nach BGH. Generelles Verbot: Unwirksam. Erlaubnisvorbehalt: Wirksam, aber nicht willkürlich verweigerbar. Kriterien: Größe der Wohnung, Anzahl der Tiere, Rasse, Lärm. Gefährliche Tiere: Verbot zulässig. Bestandsschutz: Bei Vertragsschluss erlaubte Tiere geschützt.""",
        "category": "Mietrecht",
        "subcategory": "Tierhaltung"
    },
    {
        "title": "Kaufvertrag: Lasten und Beschränkungen",
        "content": """Grundbuch Abteilung II: Dienstbarkeiten, Reallasten, Vorkaufsrechte. Übernahme: Käufer übernimmt i.d.R. alle Lasten. Löschung: Verkäufer muss lastenfreies Eigentum verschaffen (außer vereinbart). Wegerecht: Dulden fremder Nutzung. Wohnrecht: Stärker als Nießbrauch. Altenteilsrecht: Lebenslange Versorgung. Vorkaufsrecht: Gemeinde bei Bauland.""",
        "category": "Kaufrecht",
        "subcategory": "Grundbuch"
    },
    {
        "title": "Mietvertrag: Betriebskosten Hausmeister",
        "content": """Umlagefähig nach § 2 BetrKV: Hausmeistertätigkeit (nicht Verwaltung/Reparatur). Abgrenzung: Nur laufende Betreuung, Reinigung, Gartenpflege. Nicht umlagefähig: Reparaturen, Verwaltungsaufgaben, Vermietung. Verteilerschlüssel: Nach Wohnfläche oder Personenzahl. Nachweis: Arbeitsvertrag, Aufgabenbeschreibung. Fremdfirma: Vollständig umlagefähig wenn nur hausmeisterliche Tätigkeiten.""",
        "category": "Mietrecht",
        "subcategory": "Betriebskosten"
    },
    {
        "title": "Kaufvertrag: Vorkaufsrecht der Gemeinde",
        "content": """Gesetzliches Vorkaufsrecht nach BauGB bei Grundstücken im Geltungsbereich von Bebauungsplänen oder Sanierungsgebieten. Ausübungsfrist: 2 Monate nach Mitteilung des Kaufvertrags. Vorkaufspreis: Zu gleichen Bedingungen wie Hauptkäufer. Ausnahmen: Verkauf an Verwandte, Miteigentümer. Negativattest: Gemeinde verzichtet, Käufer erhält Sicherheit. Verzögerung: Eintragung erst nach Fristablauf.""",
        "category": "Kaufrecht",
        "subcategory": "Vorkaufsrecht"
    },
    {
        "title": "Mietvertrag: Modernisierungsumlage Berechnung",
        "content": """Umlage nach § 559 BGB: 8% der Modernisierungskosten pro Jahr auf Jahresmiete. Modernisierung: Energieeinsparung, Wasser, Wohnwert. Kappungsgrenze: 3€/m² innerhalb 6 Jahren (2€ bei einfacher Lage). Ankündigungsfrist: 3 Monate, Schriftform. Duldung: Mieter muss Modernisierung dulden. Härtefalleinwand: Wenn unzumutbar. Sonderkündigungsrecht: Bis Ende des Monats nach Zugang der Ankündigung.""",
        "category": "Mietrecht",
        "subcategory": "Modernisierung"
    },
    {
        "title": "Kaufvertrag: Erschließungskosten",
        "content": """Anliegergebühren für Straße, Wasser, Abwasser, Strom. Umlegung: I.d.R. nach Grundstücksgröße. Zahlung: Einmalig nach Fertigstellung. Üblich: Verkäufer trägt vor Verkauf, aber verhandelbar. Wiederholungsbeiträge: Bei Erneuerung nach 25+ Jahren. Ablösung: Vorauszahlung aller zukünftigen Beiträge möglich. Wichtig: Vor Kauf Auskunft bei Gemeinde einholen.""",
        "category": "Kaufrecht",
        "subcategory": "Erschließung"
    },
    {
        "title": "Mietvertrag: Untermiete Genehmigung",
        "content": """Untervermietung nach § 553 BGB: Erlaubnis bei berechtigtem Interesse. Berechtigtes Interesse: Lebenspartner, finanzielle Gründe, berufliche Abwesenheit. Verweigerung: Nur bei wichtigem Grund (Überbelegung, Unzuverlässigkeit). Formerfordernis: Schriftliche Anfrage und Genehmigung. Mehrerlös: Steht Vermieter zu (Wuchergrenze). Kündigung: Bei unerlaubter Untervermietung fristlos möglich.""",
        "category": "Mietrecht",
        "subcategory": "Untermiete"
    },
    {
        "title": "Kaufvertrag: Grunderwerbsteuer Fälligkeit",
        "content": """Steuersatz: 3,5%-6,5% je nach Bundesland (Bayern/Sachsen 3,5%, NRW/Schleswig-Holstein 6,5%). Fälligkeit: 1 Monat nach Steuerbescheid. Unbedenklichkeitsbescheinigung: Voraussetzung für Grundbucheintragung. Steuerschuldner: Käufer (vertraglich umlagerbar). Bemessungsgrundlage: Kaufpreis inkl. Inventar wenn mitverkauft. Befreiung: Verwandte in gerader Linie.""",
        "category": "Steuerrecht",
        "subcategory": "Grunderwerbsteuer"
    },
    {
        "title": "Mietvertrag: Mietminderung Berechnung",
        "content": """Minderung nach § 536 BGB bei Mangel. Höhe: Nach Gebrauchsbeeinträchtigung (%). Unbewohnbarkeit: 100%, Heizungsausfall Winter: 50-100%, Schimmel: 20-50%, Lärmbelästigung: 10-50%. Berechnung: Von Bruttomiete inkl. Nebenkosten. Anzeigepflicht: Sofort bei Mangel. Fristlose Kündigung: Bei erheblichem Mangel nach Fristsetzung. Rückwirkung: Ab Mangeleintritt, auch ohne Minderungserklärung.""",
        "category": "Mietrecht",
        "subcategory": "Mietminderung"
    },
    {
        "title": "Kaufvertrag: Notarkosten Verteilung",
        "content": """Notarkosten: Käufer trägt i.d.R. (Notar, Grundbuch). Verteilung: Frei verhandelbar. GNotKG: 1,5-2% des Kaufpreises (Notar + Grundbuch). Löschungsbewilligung: Verkäufer trägt eigene Grundschuld-Löschung. Auflassungsvormerkung: Im Notarpreis enthalten. Vollmacht: Separate Gebühr. Grundbucheintragung: Ca. 0,5% zusätzlich.""",
        "category": "Kaufrecht",
        "subcategory": "Notarkosten"
    },
    {
        "title": "Mietvertrag: Kautionsrückzahlung Fristen",
        "content": """Rückzahlung nach Abrechnung aller Forderungen. Angemessene Frist: 3-6 Monate nach Rückgabe. Zurückbehaltungsrecht: Bei offenen Forderungen (Nebenkostenabrechnung ausstehend). Verzinsung: 4% über Basiszinssatz ab Verzug. Teilrückzahlung: Unstrittige Teile sofort. Verjährung: 3 Jahre. Anlage: Separates Konto, Zinsertrag für Mieter.""",
        "category": "Mietrecht",
        "subcategory": "Kaution"
    },
    {
        "title": "Kaufvertrag: Kaufpreisaufteilung Grundstück/Gebäude",
        "content": """Aufteilung relevant für AfA (Absetzung für Abnutzung). Gebäude: 2-3% AfA jährlich (50/33 Jahre). Grund und Boden: Keine AfA. Bewertung: Sachwertverfahren oder Bodenrichtwert. Empfehlung: Im Kaufvertrag aufteilen. Finanzamt: Prüft Angemessenheit. Gestaltung: 80/20 bis 70/30 üblich. Wichtig für Steueroptimierung.""",
        "category": "Steuerrecht",
        "subcategory": "Kaufpreisaufteilung"
    },
    {
        "title": "Mietvertrag: Zeitmietvertrag Voraussetzungen",
        "content": """Zeitmietvertrag nach § 575 BGB: Befristung ohne Kündigungsoption. Voraussetzung: Vermieter muss berechtigtes Interesse haben (Eigenbedarf, Sanierung, Abriss). Schriftform: Zwingend mit Begründung. Verlängerung: Nur durch Neuvertrag. Unwirksam: Bei fehlendem Grund wird unbefristet. Maximaldauer: Nicht gesetzlich begrenzt. Wichtig: Grund konkret beschreiben.""",
        "category": "Mietrecht",
        "subcategory": "Befristung"
    },
    {
        "title": "Kaufvertrag: Auflassungsvormerkung Funktion",
        "content": """Auflassungsvormerkung nach § 883 BGB: Sichert Käufer-Anspruch auf Eigentum. Eintragung: Abteilung II Grundbuch. Wirkung: Schutz gegen Verkauf an Dritte, Zwangsvollstreckung. Rangstelle: Sichert Position für spätere Eigentumsumschreibung. Löschung: Nach Eigentumsumschreibung automatisch. Kosten: Im Notarpreis enthalten.""",
        "category": "Kaufrecht",
        "subcategory": "Grundbuch"
    },
    {
        "title": "Mietvertrag: Eigenbedarfskündigung Anforderungen",
        "content": """Eigenbedarf nach § 573 BGB für Vermieter, Familie, Haushaltsangehörige. Darlegung: Konkrete Gründe, Person benennen. Kündigungsfrist: 3/6/9 Monate je nach Mietdauer. Sozialklausel: Härtefall kann Kündigung verhindern. Weitervermietungspflicht: Bei mehreren Wohnungen. Schadensersatz: Bei vorgetäuschtem Eigenbedarf. Räumungsfrist: Kann verlängert werden.""",
        "category": "Mietrecht",
        "subcategory": "Kündigung"
    },
    {
        "title": "Kaufvertrag: Grundschuld vs. Hypothek",
        "content": """Grundschuld: Abstraktes Sicherungsrecht, besteht unabhängig von Forderung. Hypothek: Akzessorisch, erlischt mit Darlehen. Praxis: 95% Grundschulden. Löschung: Nach Darlehensrückzahlung mit Löschungsbewilligung. Abtretung: Grundschuld kann abgetreten werden. Briefgrundschuld: Mit Brief. Buchgrundschuld: Ohne Brief, kostengünstiger.""",
        "category": "Finanzierung",
        "subcategory": "Sicherheiten"
    },
    {
        "title": "Mietvertrag: Kleinreparaturklausel Wirksamkeit",
        "content": """Kleinreparaturen nach § 535 BGB: Überwälzung auf Mieter möglich. Voraussetzung: Gegenstände häufiger Nutzung (Wasserhähne, Lichtschalter). Einzelbetrag: Max. 100-120€. Jahresobergrenze: 150-200€ oder 8% Jahresmiete. Unwirksam: Bei Überschreitung, fehlender Obergrenze. Installation: Nicht umlagefähig. Nur Reparaturen!""",
        "category": "Mietrecht",
        "subcategory": "Kleinreparaturen"
    },
    {
        "title": "Kaufvertrag: Zwangsversteigerung Ablauf",
        "content": """Verfahren nach ZVG: Amtsgericht auf Antrag des Gläubigers. Verkehrswertgutachten: Sachverständiger ermittelt Wert. Versteigerungstermin: Mindestgebot 50% (bei 2. Termin 70%). Zuschlag: Höchstbietender. Bargebot: Sofort Sicherheitsleistung (10%). Risiken: Keine Gewährleistung, Besichtigungsprobleme. Chancen: Günstiger Preis.""",
        "category": "Kaufrecht",
        "subcategory": "Zwangsversteigerung"
    },
    {
        "title": "Mietvertrag: Indexmiete Gestaltung",
        "content": """Indexmiete nach § 557b BGB: Anpassung an Verbraucherpreisindex. Schriftform: Erforderlich. Änderung: Mindestens jährlich, nach tatsächlicher Indexänderung. Kappungsgrenze: Gilt nicht. Mieterhöhung normal: Nicht parallel möglich. Modernisierungsumlage: Möglich. Kündigung: Ordentliche Kündigung frühestens nach 4 Jahren.""",
        "category": "Mietrecht",
        "subcategory": "Indexmiete"
    },
    {
        "title": "Kaufvertrag: Vorfälligkeitsentschädigung",
        "content": """Entschädigung bei vorzeitiger Darlehensablösung. Berechnung: Zinsverlust der Bank. Zinsfestschreibung: Bis Ende läuft Entschädigung. Nach 10 Jahren: Kostenlose Kündigung mit 6 Monaten Frist (§ 489 BGB). Umschuldung: Vorfälligkeitsentschädigung vermeiden. Forward-Darlehen: Frühzeitig neue Konditionen sichern.""",
        "category": "Finanzierung",
        "subcategory": "Vorfälligkeit"
    },
    {
        "title": "Mietvertrag: Nachmieter Berechtigung",
        "content": """Nachmieterstellung nach § 563 BGB: Nur bei berechtigtem Interesse. Berechtigtes Interesse: Berufliche Versetzung, finanzielle Notlage, Familienzuwachs. Geeigneter Nachmieter: Zahlungsfähig, vertretbare Nutzung. Verweigerung: Bei Unzuverlässigkeit, zu viele Personen. Keine Pflicht: Vermieter muss nicht akzeptieren. Vorteil: Vermeidung von Kündigungsfrist.""",
        "category": "Mietrecht",
        "subcategory": "Nachmieter"
    },
    {
        "title": "Kaufvertrag: Besichtigungsrecht vor Kauf",
        "content": """Besichtigung: Vor Kaufvertrag üblich und empfohlen. Umfang: Alle Räume, Keller, Dachboden. Gutachter: Käufer darf Sachverständigen mitbringen. Verkäufer: Muss Besichtigung ermöglichen. Mieter: Müssen dulden nach Ankündigung. Protokoll: Mängel dokumentieren. Mehrmalige Besichtigung: Bei berechtigtem Interesse.""",
        "category": "Kaufrecht",
        "subcategory": "Besichtigung"
    },
    {
        "title": "Mietvertrag: Betriebskosten Gartenpflege",
        "content": """Umlagefähig nach § 2 BetrKV: Pflege Grünanlagen (Rasen, Sträucher). Nicht umlagefähig: Neuanlage, größere Umgestaltung. Verteilerschlüssel: Nach Wohnfläche. Eigenleistung: Nicht ansetzbar. Fremdfirma: Vollständig umlagefähig. Spielplatz: Umlagefähig. Winterdienst: Separat umlagefähig.""",
        "category": "Mietrecht",
        "subcategory": "Betriebskosten"
    },
    {
        "title": "Kaufvertrag: Teilungserklärung Bedeutung",
        "content": """Teilungserklärung: Aufteilung Mehrfamilienhaus in Eigentumswohnungen (§ 8 WEG). Inhalt: Abgeschlossene Wohnungen, Miteigentumsanteile, Sondernutzungsrechte, Kostenverteilung. Gemeinschaftsordnung: Regelt Verwaltung, Nutzung. Bindung: Für alle Eigentümer. Änderung: Nur mit Mehrheit. Wichtig: Vor Kauf genau prüfen (Instandhaltungsrücklage, Beschlüsse).""",
        "category": "WEG-Recht",
        "subcategory": "Teilungserklärung"
    },
    {
        "title": "Mietvertrag: Mieterhöhung nach ortsüblicher Vergleichsmiete",
        "content": """Mieterhöhung nach § 558 BGB: Bis ortsübliche Vergleichsmiete. Voraussetzung: 15 Monate keine Erhöhung. Kappungsgrenze: 15-20% in 3 Jahren (je nach Stadt). Mietspiegel: Qualifiziert oder einfach. Begründung: Schriftform, 3 Vergleichswohnungen oder Mietspiegel/Gutachten. Zustimmung: 2 Monate Überlegungsfrist, 3 Monate Umsetzung. Widerspruch: Begründet möglich.""",
        "category": "Mietrecht",
        "subcategory": "Mieterhöhung"
    },
    {
        "title": "Kaufvertrag: Erbbaurecht Grundlagen",
        "content": """Erbbaurecht nach ErbbauRG: Recht, Bauwerk auf fremdem Grund zu errichten/nutzen. Laufzeit: 99 Jahre üblich. Erbbauzins: Jährliche Zahlung an Grundstückseigentümer. Heimfall: Gebäude fällt an Grundstückseigentümer (Entschädigung). Vererblich/Veräußerlich: Ja. Belastung: Mit Grundschuld möglich. Vorteile: Weniger Kapital, steuerliche Absetzung Erbbauzins.""",
        "category": "Kaufrecht",
        "subcategory": "Erbbaurecht"
    },
    {
        "title": "Mietvertrag: Schönheitsreparaturen bei möblierter Wohnung",
        "content": """Möblierte Wohnung: Kürzere Mietdauer, andere Regelungen. Schönheitsreparaturen: Oft Vermieter, da Möbel erschweren. Abnutzung: Stärker durch Möbel. Klausel: Muss eindeutig sein. Übergabeprotokoll: Besonders wichtig. Kaution: Höher wegen Inventar. Inventarliste: Zustand dokumentieren.""",
        "category": "Mietrecht",
        "subcategory": "Möblierte Wohnung"
    },
    {
        "title": "Kaufvertrag: Nießbrauch Regelungen",
        "content": """Nießbrauch nach § 1030 BGB: Recht zur Nutzung (Bewohnung oder Vermietung). Eintragung: Abteilung II Grundbuch. Lebenslang: Meist auf Lebenszeit. Verkehrswert: Mindert Immobilienwert. Kosten: Nießbraucher trägt laufende Kosten, Eigentümer außergewöhnliche. Vererblich: Nein. Schenkungssteuer: Günstiger durch Nießbrauchsvorbehalt.""",
        "category": "Kaufrecht",
        "subcategory": "Nießbrauch"
    },
    {
        "title": "Mietvertrag: Betriebskosten Versicherungen",
        "content": """Umlagefähig nach § 2 BetrKV: Gebäudeversicherung, Haftpflichtversicherung. Nicht umlagefähig: Rechtsschutz, Mietausfallversicherung, Hausratversicherung. Verteilerschlüssel: Wohnfläche. Prämienanpassung: Wird durchgereicht. Selbstbeteiligung: Nicht umlagefähig. Schadenszahlung: Keine Erstattung an Mieter.""",
        "category": "Mietrecht",
        "subcategory": "Betriebskosten"
    },
    {
        "title": "Kaufvertrag: KfW-Förderung Integration",
        "content": """KfW-Darlehen: Günstige Kredite für energetische Sanierung/Neubau. Antragstellung: Vor Baubeginn über Bank. Programme: Wohneigentum (124), Energieeffizient Sanieren (151/152). Tilgungszuschuss: Bis zu 48.000€ geschenkt. Kombination: Mit normaler Finanzierung. Energieberater: Oft Voraussetzung. Wichtig: Frühzeitig beantragen.""",
        "category": "Finanzierung",
        "subcategory": "Förderung"
    },
    {
        "title": "Mietvertrag: Mietaufhebungsvertrag Gestaltung",
        "content": """Mietaufhebungsvertrag: Einvernehmliche Beendigung. Schriftform: Erforderlich. Abfindung: Verhandelbar. Räumungsfrist: Frei vereinbar. Schönheitsreparaturen: Regelung treffen. Kaution: Rückzahlung nach Übergabe. Vorteil: Keine Kündigungsfrist. Wichtig: Keine Nachteile eintauschen.""",
        "category": "Mietrecht",
        "subcategory": "Beendigung"
    },
    {
        "title": "Kaufvertrag: Verkauf mit Leibrente",
        "content": """Leibrente: Wiederkehrende Zahlung statt Einmalkaufpreis. Eintragung: Abteilung II Grundbuch. Höhe: Nach Immobilienwert und Lebenserwartung. Reallast: Dinglich gesichert. Versteuerung: Ertragsanteil. Nießbrauch kombiniert: Üblich bei Übergabe an Kinder. Indexierung: Anpassung an Inflation möglich.""",
        "category": "Kaufrecht",
        "subcategory": "Leibrente"
    },
    {
        "title": "Mietvertrag: Betriebskosten Beleuchtung",
        "content": """Umlagefähig nach § 2 BetrKV: Beleuchtung Gemeinschaftsflächen (Flur, Keller, Außenbereich). Nicht umlagefähig: Wohnungsbeleuchtung. Verteilerschlüssel: Wohnfläche oder Personenzahl. Stromkosten: Nur Allgemeinstrom. Wartung: Lampen wechseln umlagefähig. Smart Lighting: Umlagefähig wenn Allgemeinflächen.""",
        "category": "Mietrecht",
        "subcategory": "Betriebskosten"
    },
    {
        "title": "Kaufvertrag: Rückauflassungsvormerkung",
        "content": """Rückauflassungsvormerkung: Sichert Verkäufer bei Ratenzahlung. Eintragung: Abteilung II. Wirkung: Rückforderung bei Zahlungsverzug. Löschung: Nach vollständiger Kaufpreiszahlung. Selten: Meist sofortige Kaufpreiszahlung üblich. Alternative: Notaranderkonto.""",
        "category": "Kaufrecht",
        "subcategory": "Sicherung"
    },
    {
        "title": "Mietvertrag: Kündigungssperrfrist nach Umwandlung",
        "content": """Kündigungssperrfrist nach § 577a BGB: 3 Jahre (10 Jahre in Gebieten mit Wohnungsknappheit). Umwandlung: Mietwohnung wird Eigentumswohnung. Eigenbedarf: Erst nach Sperrfrist. Ausnahmen: Verwandte, wirtschaftliche Verwertung unmöglich. Verlängerung: Bis zu 10 Jahre durch Gemeinde. Schadensersatz: Bei unberechtigter Kündigung.""",
        "category": "Mietrecht",
        "subcategory": "Kündigung"
    },
    {
        "title": "Kaufvertrag: Makler Doppeltätigkeit",
        "content": """Doppeltätigkeit: Makler für beide Seiten. Offenlegung: Pflicht nach § 654 BGB. Interessenkonflikt: Vermeiden. Provisionsanspruch: Gegen beide möglich. Bestellerprinzip Wohnraum: Käufer zahlt nur wenn selbst beauftragt. Gewerbe: Keine Einschränkung. Neutralitätspflicht: Ausgewogene Beratung.""",
        "category": "Maklerrecht",
        "subcategory": "Doppeltätigkeit"
    },
    {
        "title": "Mietvertrag: Betriebskosten Winterdienst",
        "content": """Umlagefähig nach § 2 BetrKV: Schneeräumung, Streuen. Eigenleistung: Nicht ansetzbar. Fremdfirma: Vollständig umlagefähig. Verkehrssicherungspflicht: Vermieter muss organisieren. Mieter-Pflicht: Nur wenn vertraglich vereinbart (dann nicht umlagefähig). Verteilerschlüssel: Wohnfläche. Pauschalvertrag: Umlagefähig.""",
        "category": "Mietrecht",
        "subcategory": "Betriebskosten"
    },
    {
        "title": "Kaufvertrag: Verkauf mit Rückkaufsrecht",
        "content": """Rückkaufsrecht: Recht des Verkäufers, Immobilie zurückzukaufen. Eintragung: Vormerkung im Grundbuch. Frist: Vereinbarung (oft 1-5 Jahre). Preis: Meist Kaufpreis plus Wertsteigerung. Absicherung: Bei unsicherer Finanzierung des Käufers. Steuer: Ggf. doppelte Grunderwerbsteuer. Selten in Praxis.""",
        "category": "Kaufrecht",
        "subcategory": "Rückkaufsrecht"
    },
    {
        "title": "Mietvertrag: Zeitmietvertrag bei Sanierung",
        "content": """Sanierungsabsicht als Grund für Befristung nach § 575 BGB. Konkrete Planung: Nachweispflicht (Kostenvoranschläge, Finanzierung). Zeitraum: Muss realistisch sein. Nichteinhaltung: Schadensersatzpflicht des Vermieters. Verlängerung: Bei Verzögerung schwierig. Alternative: Normale Kündigung wegen Sanierung.""",
        "category": "Mietrecht",
        "subcategory": "Befristung"
    }
]

print("🚀 BATCH 1: VERTRAGSRECHT DETAILS - START")
print("=" * 60)

successful = 0
failed = 0

for i, doc in enumerate(documents, 1):
    try:
        full_text = f"{doc['title']}\n\n{doc['content']}\n\nKategorie: {doc['category']}\nSubkategorie: {doc['subcategory']}"
        
        result = genai.embed_content(
            model="models/embedding-001",
            content=full_text,
            task_type="retrieval_document"
        )
        embedding = result['embedding']
        
        point_id = str(uuid.uuid4())
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"],
                "subcategory": doc["subcategory"],
                "full_text": full_text
            }
        )
        
        client.upsert(
            collection_name="legal_documents",
            points=[point]
        )
        
        successful += 1
        print(f"✅ {i}/50: {doc['title'][:60]}")
        
    except Exception as e:
        failed += 1
        print(f"❌ {i}/50: {doc['title'][:60]} - {str(e)[:50]}")

print("\n" + "=" * 60)
print(f"✅ Erfolgreich: {successful}")
print(f"❌ Fehlgeschlagen: {failed}")

# Count total
try:
    count = client.count(collection_name="legal_documents")
    total = count.count
    print(f"\n🎯 GESAMT DOKUMENTE: {total}")
    remaining = 4000 - total
    print(f"📊 Noch {remaining} bis zur 4.000!")
except:
    print("⚠️  Konnte Gesamtzahl nicht abrufen")

print("\n🔥 BATCH 1 COMPLETE! 🔥")
