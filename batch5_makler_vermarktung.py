#!/usr/bin/env python3
"""Batch 5: Maklerrecht & Vermarktung - 100 Dokumente"""

import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai
import uuid

QDRANT_URL = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)
client = QdrantClient(url=f"https://{QDRANT_URL}", api_key=QDRANT_API_KEY, timeout=60)

documents = [
    {
        "title": "Maklervertrag: Arten und Unterschiede",
        "content": """Alleinauftrag: Nur ein Makler, höhere Erfolgschance, oft niedrigere Provision. Einfacher Maklerauftrag: Mehrere Makler parallel möglich. Qualifizierter Alleinauftrag: Mit Nachweispflicht, feste Laufzeit. Wichtig: Alleinauftrag bringt mehr Engagement des Maklers!""",
        "category": "Maklerrecht",
        "subcategory": "Maklervertrag"
    },
    {
        "title": "Exposé: Pflichtangaben",
        "content": """Pflichtangaben nach § 16 MaBV: Energieausweis-Kennwerte, Baujahr, Energieträger, Energieeffizienzklasse. Weitere wichtig: Wohnfläche, Zimmer, Ausstattung, Lage, Preis. Fotos: Aussagekräftig, professionell. Wichtig: Falschangaben können zur Haftung führen!""",
        "category": "Maklerrecht",
        "subcategory": "Exposé"
    },
    {
        "title": "Besichtigungstermin: Vorbereitung Verkäufer",
        "content": """Vorbereitung: Aufräumen, Lüften, Licht an, neutrale Deko, Gerüche vermeiden, Haustiere entfernen. Unterlagen: Grundrisse, Energieausweis, Nebenkostenabrechnung bereit. Verhalten: Freundlich, aber zurückhaltend, Makler sprechen lassen. Wichtig: Erster Eindruck zählt!""",
        "category": "Vermarktung",
        "subcategory": "Besichtigung"
    },
    {
        "title": "Home Staging: Wirkung",
        "content": """Home Staging: Möblierung/Dekoration für Verkauf. Wirkung: 5-15% höherer Preis, schnellerer Verkauf. Kosten: 1-3% des Kaufpreises. Maßnahmen: Neutrale Farben, aufgeräumt, hochwertige Möbel (gemietet). Wichtig: Lohnt sich besonders bei höherpreisigen Immobilien!""",
        "category": "Vermarktung",
        "subcategory": "Home Staging"
    },
    {
        "title": "Preisfindung: Strategien",
        "content": """Strategien: Vergleichswerte, Gutachten, Online-Bewertung, Makler-Einschätzung. Zu hoch: Keine Interessenten, lange Vermarktung. Zu niedrig: Geld verschenkt. Verhandlungsspielraum: 5-10% einkalkulieren. Wichtig: Realistischer Preis führt zu schnellem Verkauf!""",
        "category": "Vermarktung",
        "subcategory": "Preisfindung"
    },
    {
        "title": "Verkaufsdauer: Durchschnitt",
        "content": """Durchschnittliche Verkaufsdauer: 3-6 Monate. Faktoren: Lage, Preis, Zustand, Marketing. Schneller: 1a-Lage, attraktiver Preis, guter Zustand. Langsam: Spezielle Objekte, überhöhter Preis, schlechter Zustand. Wichtig: Nach 3 Monaten Preis überprüfen!""",
        "category": "Vermarktung",
        "subcategory": "Verkaufsdauer"
    },
    {
        "title": "Online-Portale: Reichweite",
        "content": """Wichtigste Portale: Immobilienscout24 (Marktführer), Immowelt, Ebay Kleinanzeigen. Reichweite: 95% der Kaufinteressenten nutzen Online-Portale. Kosten: 50-300€ pro Inserat. Kombination: Mehrere Portale parallel schalten. Wichtig: Professionelle Fotos essentiell!""",
        "category": "Vermarktung",
        "subcategory": "Online-Portale"
    },
    {
        "title": "Professionelle Fotografie: ROI",
        "content": """Professionelle Fotos: 300-800€ Investition. Wirkung: 50% mehr Anfragen, 10-20% höherer Preis möglich. Leistung: Professionelle Kamera, Weitwinkel, Bildbearbeitung, virtuelle Möblierung. ROI: 10-30x. Wichtig: Beste Investment beim Verkauf!""",
        "category": "Vermarktung",
        "subcategory": "Fotografie"
    },
    {
        "title": "Drohnenaufnahmen: Mehrwert",
        "content": """Drohnenaufnahmen: Luftbilder von Immobilie und Umgebung. Kosten: 200-500€. Mehrwert: Besonders bei Grundstücken, Einfamilienhäusern, Villen. Wirkung: Hebt sich ab von Konkurrenz. Genehmigung: Oft erforderlich. Wichtig: Für Premium-Objekte lohnend!""",
        "category": "Vermarktung",
        "subcategory": "Drohnenaufnahmen"
    },
    {
        "title": "Virtueller Rundgang: 360-Grad",
        "content": """360-Grad-Rundgang: Virtuelle Begehung am Bildschirm. Kosten: 300-1.000€. Vorteil: Vorqualifizierung Interessenten, weniger Besichtigungen. Technologie: Matterport, 360-Grad-Kameras. Wichtig: Standard bei modernen Vermarktungen!""",
        "category": "Vermarktung",
        "subcategory": "Virtueller Rundgang"
    },
    {
        "title": "Grundriss: Professionelle Erstellung",
        "content": """Grundriss: Zeigt Raumaufteilung, Größen. Erstellung: Selbst messen + Software (z.B. RoomSketcher) oder Dienstleister. Kosten: 50-200€ professionell. Wichtig: Maßstabsgetreu, übersichtlich, alle Räume beschriftet. Essentiell für Exposé!""",
        "category": "Vermarktung",
        "subcategory": "Grundriss"
    },
    {
        "title": "Interessenten-Qualifizierung: Vorgespräch",
        "content": """Qualifizierung vor Besichtigung: Finanzierung geklärt? Ernsthafte Kaufabsicht? Passt Budget? Zeitrahmen? Vorteil: Spart Zeit, nur ernsthafte Interessenten. Fragen: Per Telefon/E-Mail klären. Wichtig: Höflich aber bestimmt!""",
        "category": "Vermarktung",
        "subcategory": "Qualifizierung"
    },
    {
        "title": "Besichtigungsanzahl: Optimum",
        "content": """Optimale Besichtigungszahl bis Verkauf: 5-15. Zu wenig (<5): Vielleicht zu teuer/schlechtes Marketing. Zu viel (>20): Definitiv Problem (Preis, Zustand, Lage). Strategie: Gebündelte Termine (mehrere Interessenten kurz nacheinander = Nachfrage-Gefühl). Wichtig: Qualität vor Quantität!""",
        "category": "Vermarktung",
        "subcategory": "Besichtigungen"
    },
    {
        "title": "Mehrere Interessenten: Verhandlungstaktik",
        "content": """Mehrere Interessenten parallel: Verhandlungsposition stärken. Taktik: Transparenz über mehrere Interessenten, Angebotsfrist setzen, höchstes Angebot gewinnt. Bieterverfahren: Bei sehr begehrten Objekten. Wichtig: Fair bleiben, keine falschen Aussagen!""",
        "category": "Vermarktung",
        "subcategory": "Verhandlung"
    },
    {
        "title": "Verkaufsverhandlung: Vorbereitung",
        "content": """Vorbereitung: Untergrenze festlegen, Argumente sammeln (Lage, Zustand, Vergleichspreise), Gutachten bereit, Alternative Interessenten erwähnen. Taktik: Ruhig bleiben, nicht unter Druck setzen lassen, Zeit lassen. Wichtig: Nicht beim ersten Angebot zusagen!""",
        "category": "Vermarktung",
        "subcategory": "Verhandlung"
    },
    {
        "title": "Angebotsabgabe: Schriftform",
        "content": """Angebot: Schriftlich mit Kaufpreis, Bedingungen (Finanzierung, Besichtigungsvorbehalt), Frist. Bindung: Angebot bindet Käufer für Frist. Verkäufer: Kann annehmen oder ablehnen. Nachverhandlung: Gegenangebot möglich. Wichtig: Alle Bedingungen klar formulieren!""",
        "category": "Vermarktung",
        "subcategory": "Angebot"
    },
    {
        "title": "Reservierungsvereinbarung: Absicherung",
        "content": """Reservierungsvereinbarung: Käufer sichert sich Objekt für bestimmte Zeit (1-4 Wochen). Inhalt: Kaufpreis, Frist, Vertragsstrafe bei Rücktritt. Anzahlung: 1.000-5.000€ möglich. Wichtig: Schriftlich! Schützt vor Mitbietern während Finanzierungsklärung.""",
        "category": "Vermarktung",
        "subcategory": "Reservierung"
    },
    {
        "title": "Objektbeschreibung: Verkaufspsychologie",
        "content": """Verkaufspsychologie: Emotionale Sprache (Traumwohnung, Lichtdurchflutet), Storytelling (Familie aufgewachsen), Vorteil-Betonung (ruhige Lage, nahe Schule). Ehrlich bleiben: Keine Täuschung! Alleinstellungsmerkmale: Was macht diese Immobilie besonders? Wichtig: Wahrheit verkauft besser als Lüge!""",
        "category": "Vermarktung",
        "subcategory": "Objektbeschreibung"
    },
    {
        "title": "Tag der offenen Tür: Organisation",
        "content": """Tag der offenen Tür: Mehrere Interessenten gleichzeitig (Samstag/Sonntag 2-3 Stunden). Vorbereitung: Perfekte Präsentation, Snacks/Getränke, Unterlagen bereit. Vorteil: Nachfrage-Gefühl, Zeitersparnis. Nachteil: Weniger persönlich. Wichtig: Bei begehrten Objekten sehr effektiv!""",
        "category": "Vermarktung",
        "subcategory": "Tag der offenen Tür"
    },
    {
        "title": "Exklusive Vorbesichtigung: VIP-Käufer",
        "content": """Exklusive Vorbesichtigung: Für ausgewählte zahlungskräftige Interessenten vor offiziellem Start. Strategie: Höchstpreis erzielen, diskret verkaufen. Zielgruppe: Investoren, Gutverdiener. Wichtig: Bei Luxusimmobilien Standard!""",
        "category": "Vermarktung",
        "subcategory": "Exklusiv-Besichtigung"
    },
    {
        "title": "Zeitungsannonce: Noch relevant?",
        "content": """Zeitungsannonce: Nur noch für ältere Zielgruppe relevant (65+). Kosten: 100-500€. Reichweite: Stark gesunken. Kombination: Mit Online-Marketing. Wichtig: Nur als Ergänzung, nicht Hauptkanal!""",
        "category": "Vermarktung",
        "subcategory": "Zeitungsannonce"
    },
    {
        "title": "Social Media Marketing: Instagram/Facebook",
        "content": """Social Media: Instagram/Facebook für Immobilien-Marketing. Vorteil: Jüngere Zielgruppe, visuelle Präsentation. Kosten: 50-300€ Werbeanzeigen. Reichweite: Lokal targetieren möglich. Wichtig: Professionelle Fotos essentiell, regelmäßige Posts!""",
        "category": "Vermarktung",
        "subcategory": "Social Media"
    },
    {
        "title": "Video-Marketing: YouTube/TikTok",
        "content": """Video-Marketing: Rundgang-Video, Drohnenflug, Stadtteil-Vorstellung. Plattformen: YouTube, Instagram, TikTok, Immobilienportale. Kosten: 300-1.500€ professionell. Wirkung: Sehr hohe Engagement-Rate. Wichtig: Trend steigt massiv, bald Standard!""",
        "category": "Vermarktung",
        "subcategory": "Video-Marketing"
    },
    {
        "title": "Makler-Auswahl: Kriterien",
        "content": """Auswahlkriterien: Lokale Marktkenntnisse, Referenzen, Verkaufsstatistik, Sympathie, Marketing-Strategie, Provision. Interview: Mehrere Makler vergleichen. Bewertungen: Online-Rezensionen prüfen. Wichtig: Guter Makler ist 10-20% mehr Verkaufspreis wert!""",
        "category": "Maklerrecht",
        "subcategory": "Makler-Auswahl"
    },
    {
        "title": "Maklerprovision: Verhandlung",
        "content": """Provision verhandelbar: Ja! Standard: 3,57% (inkl. MwSt.) je Seite bei Wohnimmobilien. Verhandlung: Bei höherem Kaufpreis (>500.000€) oft 2,5-3%. Kombination: Alleinauftrag gegen niedrigere Provision. Wichtig: Im Vorfeld klären, schriftlich fixieren!""",
        "category": "Maklerrecht",
        "subcategory": "Provision"
    },
    {
        "title": "Makler-Kündigung: Fristen",
        "content": """Kündigung Maklervertrag: Ohne Grund nur bei unbefristetem Vertrag (4 Wochen). Wichtiger Grund: Pflichtverletzung, mangelnde Aktivität. Befristeter Vertrag: Kündigung schwierig. Provisionsanspruch: Auch nach Kündigung wenn Makler Nachweis erbracht. Wichtig: Kündigungsbedingungen im Vertrag prüfen!""",
        "category": "Maklerrecht",
        "subcategory": "Kündigung"
    },
    {
        "title": "Makler-Courtage: Fälligkeit",
        "content": """Courtage fällig bei: Wirksamer Hauptvertrag (notariell beurkundet UND Kaufpreis gezahlt). Nicht bei: Nur Reservierung, nur Beurkundung. Stundung: Bis Kaufpreiszahlung möglich. Wichtig: Makler kann Zahlung erst nach vollständigem Vertragsabschluss verlangen!""",
        "category": "Maklerrecht",
        "subcategory": "Courtage"
    },
    {
        "title": "Selbstverkauf: Vor- und Nachteile",
        "content": """Vorteile Selbstverkauf: Provisionersparnis (7-14%), volle Kontrolle. Nachteile: Zeitaufwand, fehlendes Know-how, emotionale Bindung, schlechtere Vermarktung. Kosten sparen: Professionelle Fotos trotzdem! Wichtig: Nur bei Standardimmobilien und viel Zeit sinnvoll!""",
        "category": "Vermarktung",
        "subcategory": "Selbstverkauf"
    },
    {
        "title": "Energieausweis: Vorlage-Pflicht",
        "content": """Vorlage-Pflicht: Bei Besichtigung, spätestens bei Vertragsabschluss. Kennwerte: In Anzeige angeben (§ 16a MaBV). Verbrauchsausweis: Tatsächlicher Verbrauch letzten 3 Jahre. Bedarfsausweis: Berechnet nach Gebäudezustand. Gültigkeit: 10 Jahre. Wichtig: Bußgeld bis 15.000€ bei fehlender Vorlage!""",
        "category": "Vermarktung",
        "subcategory": "Energieausweis"
    },
    {
        "title": "Mängel verschweigen: Haftung",
        "content": """Arglistig verschwiegene Mängel: Verkäufer haftet auch bei Gewährleistungsausschluss! Arglist: Bewusstes Verschweigen bekannter Mängel. Folge: Käufer kann Kaufpreis mindern, zurücktreten, Schadensersatz. Verjährung: 3 Jahre. Wichtig: Alle bekannten Mängel offenlegen!""",
        "category": "Kaufrecht",
        "subcategory": "Mängel"
    },
    {
        "title": "Verkäufer-Offenlegungspflichten: Umfang",
        "content": """Offenlegungspflicht: Auf Nachfrage wahrheitsgemäß antworten. Ungefragt: Nur schwerwiegende Mängel (Feuchtigkeit, Statik, Altlasten). Nachbarschaftsstreit: Muss erwähnt werden. Selbstmord: Nur wenn nachgefragt. Wichtig: Im Zweifel mehr offenlegen als verschweigen!""",
        "category": "Kaufrecht",
        "subcategory": "Offenlegung"
    },
    {
        "title": "Kaufpreisverhandlung: Taktiken Käufer",
        "content": """Käufer-Taktiken: Mängel betonen, Vergleichsobjekte nennen, Budget-Grenze vorschieben, Zeit lassen. Gegenstrategien: Gutachten vorlegen, Vergleichspreise kennen, weitere Interessenten erwähnen, nicht unter Wert verkaufen. Wichtig: Ruhe bewahren, Untergrenze kennen!""",
        "category": "Vermarktung",
        "subcategory": "Verhandlung"
    },
    {
        "title": "Notartermin: Vorbereitung Verkäufer",
        "content": """Vorbereitung: Personalausweis, Grundbuchauszug, Löschungsbewilligung Grundschuld (von Bank), Energieausweis, Teilungserklärung (WEG), Vollmacht (falls nicht beide Eigentümer kommen). Dauer: 30-60 Minuten. Kosten: Zahlt Käufer. Wichtig: Alle Unterlagen vollständig mitbringen!""",
        "category": "Kaufrecht",
        "subcategory": "Notartermin"
    },
    {
        "title": "Übergabe-Checkliste: Was beachten?",
        "content": """Übergabe-Checkliste: Zählerstände (Strom, Wasser, Gas, Heizung), Schlüsselübergabe (alle Exemplare!), Mängel dokumentieren, Protokoll unterschreiben, Bedienungsanleitungen übergeben, Kontakte (Hausmeister, Handwerker) weitergeben. Wichtig: Fotos machen, alles schriftlich!""",
        "category": "Kaufrecht",
        "subcategory": "Übergabe"
    },
    {
        "title": "Verkauf vermietetes Objekt: Besonderheiten",
        "content": """Verkauf vermietet: Kündigung nur bei Eigenbedarf möglich (3 Jahre Sperrfrist nach Umwandlung). Käufer: Tritt in Mietvertrag ein. Mieter: Muss Besichtigungen dulden (mit Ankündigung). Vorkaufsrecht: Mieter bei Umwandlung (10 Jahre). Wichtig: Mietvertrag vorlegen, Mieter informieren!""",
        "category": "Vermarktung",
        "subcategory": "Vermietetes Objekt"
    },
    {
        "title": "Teilverkauf Grundstück: Ablauf",
        "content": """Teilverkauf: Grundstück teilen, Teil verkaufen. Genehmigung: Teilungsgenehmigung Bauamt. Vermessung: Öffentlich bestellter Vermesser. Grundbuch: Neue Flurstücke eintragen. Kosten: 2.000-5.000€. Wichtig: Zufahrt/Erschließung für beide Teile sichern!""",
        "category": "Kaufrecht",
        "subcategory": "Teilverkauf"
    },
    {
        "title": "Verkauf Erbengemeinschaft: Regelung",
        "content": """Verkauf aus Erbengemeinschaft: Alle Erben müssen zustimmen. Uneinigkeit: Teilungsversteigerung möglich (teuer, Zeit!). Lösung: Ein Erbe kauft andere aus oder einvernehmlicher Verkauf. Notar: Alle Erben müssen anwesend sein oder Vollmacht. Wichtig: Frühzeitig einigen!""",
        "category": "Kaufrecht",
        "subcategory": "Erbengemeinschaft"
    },
    {
        "title": "Verkauf vor Tilgung: Vorfälligkeit",
        "content": """Verkauf mit noch laufendem Darlehen: Vorfälligkeitsentschädigung fällig (wenn vor Ende Zinsbindung). Berechnung: Zinsverlust Bank. Vermeidung: Käufer übernimmt Darlehen, oder nach 10 Jahren (§ 489 BGB). Wichtig: Mit Bank verhandeln, oft Kulanz!""",
        "category": "Finanzierung",
        "subcategory": "Vorfälligkeit"
    },
    {
        "title": "Scheidung: Immobilien-Aufteilung",
        "content": """Immobilie bei Scheidung: Realteilung (verkaufen, Erlös teilen), Übernahme durch einen (Auszahlung des anderen), Versteigerung (letztes Mittel). Bewertung: Verkehrswert ermitteln. Finanzierung: Oft Umschuldung nötig (nur ein Name). Wichtig: Einvernehmliche Lösung anstreben!""",
        "category": "Kaufrecht",
        "subcategory": "Scheidung"
    },
    {
        "title": "Gewerblicher Grundstückshandel: Grenze",
        "content": """Gewerblicher Grundstückshandel: Ab 3 Objekten in 5 Jahren möglich (Steuerrecht). Folge: Gewerbesteuer, keine 10-Jahres-Spekulationsfrist. Ausnahmen: Private Vermögensverwaltung bei Vermietung. Wichtig: Bei häufigem Handel Steuerberater konsultieren!""",
        "category": "Steuerrecht",
        "subcategory": "Grundstückshandel"
    },
    {
        "title": "Erbpacht-Verkauf: Besonderheiten",
        "content": """Verkauf Erbbaurecht: Nur Gebäude + Erbbaurecht, nicht Grundstück. Zustimmung: Grundstückseigentümer meist erforderlich. Preisfindung: Schwieriger (Restlaufzeit beachten). Finanzierung: Banken zurückhaltend bei kurzer Restlaufzeit. Wichtig: Verlängerungsoption prüfen!""",
        "category": "Kaufrecht",
        "subcategory": "Erbbaurecht"
    },
    {
        "title": "Zwangsversteigerung vermeiden: Optionen",
        "content": """Zwangsversteigerung droht: Optionen: Freiwilliger Verkauf (höherer Preis!), Stundung mit Bank vereinbaren, Privatinsolvenz, Teilverkauf. Zeitfenster: 3-12 Monate bis Versteigerung. Wichtig: Frühzeitig handeln, Bank kontaktieren, professionelle Hilfe!""",
        "category": "Finanzierung",
        "subcategory": "Zwangsversteigerung"
    },
    {
        "title": "Notar-Auswahl: Kriterien",
        "content": """Notar-Auswahl: Freie Wahl (meist Käufer wählt). Kriterien: Erreichbarkeit, Erfahrung, Empfehlung. Kosten: Festgelegt nach GNotKG (1,5-2% Kaufpreis). Service: Entwurf vorab zusenden, Fragen beantworten. Wichtig: Alle Notare haben gleiche Gebühren, daher Service/Nähe entscheidend!""",
        "category": "Kaufrecht",
        "subcategory": "Notar"
    },
    {
        "title": "Kaufvertrag: Rücktritt nach Beurkundung",
        "content": """Rücktritt nach Beurkundung: Nur bei wichtigem Grund oder Rücktrittsklausel. Wichtiger Grund: Finanzierung scheitert (wenn Vorbehalt), wesentlicher Mangel. Ohne Grund: Schadensersatz. Kosten: Notar meist schon fällig. Wichtig: Rücktrittsklauseln im Vertrag vereinbaren!""",
        "category": "Kaufrecht",
        "subcategory": "Rücktritt"
    },
    {
        "title": "Eigentumswechsel: Grundbuch-Dauer",
        "content": """Grundbuch-Eintragung: 4-12 Wochen nach Notartermin. Beschleunigung: Durch Notar, aber begrenzt. Vorher: Käufer noch nicht Eigentümer! Auflassungsvormerkung: Schützt Käufer in Zwischenzeit. Wichtig: Geduld, Prozess dauert!""",
        "category": "Kaufrecht",
        "subcategory": "Grundbuch"
    },
    {
        "title": "Verkauf an Bauträger: Besonderheiten",
        "content": """Verkauf an Bauträger: Oft für Entwicklung (Abriss + Neubau). Preis: Kann über/unter Wohnimmobilien-Preis sein (Entwicklungspotenzial). Bebauungsmöglichkeit: Entscheidend für Preis. Abwicklung: Meist schnell, Bauträger sind Profis. Wichtig: Mehrere Bauträger anfragen!""",
        "category": "Vermarktung",
        "subcategory": "Bauträger-Verkauf"
    },
    {
        "title": "Off-Market-Verkauf: Diskretion",
        "content": """Off-Market: Verkauf ohne öffentliche Vermarktung. Zielgruppe: VIP, Prominente, Luxus-Segment. Vorteil: Diskret, keine Besichtigungstouristen. Nachteil: Kleinerer Käuferkreis, eventuell niedrigerer Preis. Makler: Spezialisierte Luxus-Makler. Wichtig: Bei Bedarf nach Privatsphäre!""",
        "category": "Vermarktung",
        "subcategory": "Off-Market"
    },
    {
        "title": "Internationale Käufer: Besonderheiten",
        "content": """Internationale Käufer: Höhere Sprachbarriere, andere Kaufgewohnheiten, Finanzierung komplexer. Geldwäsche-Prüfung: Verschärft seit 2020. Notar: Dolmetscher oft erforderlich. Zahlung: International komplexer. Wichtig: Seriösen Makler/Notar mit Erfahrung einschalten!""",
        "category": "Vermarktung",
        "subcategory": "Internationale Käufer"
    },
    {
        "title": "Investoren als Käufer: Rendite-Fokus",
        "content": """Investoren: Fokus auf Rendite, Lage, Wertsteigerung. Verhandlung: Härter, professioneller. Geschwindigkeit: Oft schneller (Finanzierung steht). Preis: Meist etwas niedriger (kalkulieren streng). Vorteil: Sichere Abwicklung. Wichtig: Rendite-Kennzahlen vorbereiten!""",
        "category": "Vermarktung",
        "subcategory": "Investoren"
    },
    {
        "title": "Besichtigung: No-Gos für Verkäufer",
        "content": """No-Gos: Unaufgeräumte Wohnung, schlechte Gerüche, aufdringlich sein, zu viel/zu wenig reden, Haustiere frei laufen lassen, keine Unterlagen bereit, unpünktlich. Verhalten: Freundlich, zurückhaltend, ehrlich. Wichtig: Makler machen lassen wenn vorhanden!""",
        "category": "Vermarktung",
        "subcategory": "Besichtigung"
    },
    {
        "title": "Online-Bewertung: Genauigkeit",
        "content": """Online-Bewertung (Immoscout, Homeday): Erste Einschätzung, nicht exakt. Grundlage: Algorithmus + Vergleichswerte. Abweichung: ±15-25% möglich. Genauer: Makler-Bewertung, Gutachten. Wichtig: Als Anhaltspunkt ok, aber nicht für Preisfindung!""",
        "category": "Bewertung",
        "subcategory": "Online-Bewertung"
    },
    {
        "title": "Verkaufsverhandlung: Psychologie",
        "content": """Verkaufspsychologie: Knappheit erzeugen (weitere Interessenten), Wert betonen (Lage, Zustand), Sympathie aufbauen, aktiv zuhören. Anker-Effekt: Hoher Startpreis beeinflusst Verhandlung. Konzessionen: Langsam machen, Gegenleistung fordern. Wichtig: Emotionen managen!""",
        "category": "Vermarktung",
        "subcategory": "Verhandlung"
    },
    {
        "title": "Einkommensschwache Käufer: Risiken",
        "content": """Risiko schwache Bonität: Finanzierung scheitert, Verkauf platzt. Absicherung: Finanzierungszusage vorlegen lassen, Reservierungsgebühr, kurze Frist. Verkäufer-Finanzierung: Riskant, nur mit Grundschuld. Wichtig: Bonität prüfen, nicht zu lange warten!""",
        "category": "Vermarktung",
        "subcategory": "Käufer-Risiken"
    },
    {
        "title": "Timing Verkauf: Jahreszeit",
        "content": """Beste Verkaufszeit: Frühjahr (März-Juni), Herbst (September-Oktober). Schlechteste: Winter (November-Februar), Hochsommer (Juli-August). Grund: Wetter, Motivation, Urlaubszeit. Unterschied: 5-15% mehr Interessenten. Wichtig: Wenn möglich, Timing beachten!""",
        "category": "Vermarktung",
        "subcategory": "Timing"
    },
    {
        "title": "Renovierung vor Verkauf: Was lohnt sich?",
        "content": """Lohnt sich: Streichen (neutral!), kleine Reparaturen, Reinigung, Gartenpflege. Lohnt nicht: Große Sanierung (ROI <100%), individuelle Gestaltung. Kosten-Nutzen: 1€ Investment = 1-3€ Mehrpreis. Wichtig: Neutrale Maßnahmen bevorzugen!""",
        "category": "Vermarktung",
        "subcategory": "Renovierung"
    },
    {
        "title": "Käufer-Typen: Erkennen und bedienen",
        "content": """Käufer-Typen: Eigennutzer (emotional, Lage wichtig), Investor (rational, Rendite wichtig), Entwickler (Potential wichtig). Ansprache: Jeweils anpassen. Eigennutzer: Familie, Wohlfühlen betonen. Investor: Zahlen, Fakten. Wichtig: Typ früh erkennen!""",
        "category": "Vermarktung",
        "subcategory": "Käufer-Typen"
    },
    {
        "title": "Makler-Tätigkeitsbericht: Transparenz",
        "content": """Tätigkeitsbericht: Dokumentation der Makler-Aktivitäten. Inhalt: Anzahl Anfragen, Besichtigungen, Marketing-Maßnahmen, Markteinschätzung. Frequenz: Monatlich. Wichtig: Zeigt Makler-Leistung, Grundlage für Verlängerung/Kündigung!""",
        "category": "Maklerrecht",
        "subcategory": "Tätigkeitsbericht"
    },
    {
        "title": "Nachverhandlung nach Baugutachten: Ablauf",
        "content": """Käufer-Gutachten deckt Mängel auf: Nachverhandlung üblich. Optionen: Preisreduzierung, Verkäufer behebt Mängel, Käufer akzeptiert, Rücktritt. Umfang: Je nach Mangelschwere (5-20% Preisreduzierung). Wichtig: Kompromiss suchen, beide Seiten bewegen!""",
        "category": "Vermarktung",
        "subcategory": "Nachverhandlung"
    },
    {
        "title": "Sale-and-Lease-Back: Modell",
        "content": """Sale-and-Lease-Back: Verkauf + Rückmietung. Anwendung: Unternehmen (Liquidität), Privatpersonen (Eigenheim-Rente). Vorteil: Liquidität ohne Auszug. Nachteil: Mietzahlungen, kein Eigentum mehr. Wichtig: Verträge genau prüfen, meist ungünstig!""",
        "category": "Vermarktung",
        "subcategory": "Sale-and-Lease-Back"
    },
    {
        "title": "Immobilien-Auktion: Vor- und Nachteile",
        "content": """Auktion: Online/vor Ort, Mindestgebot. Vorteil: Schneller Verkauf, Spannung. Nachteil: Risiko Mindestpreis nicht erreicht. Kosten: 3-10% Provision an Auktionshaus. Zielgruppe: Besondere Objekte, Zeitdruck. Wichtig: Nur bei professionellen Auktionshäusern!""",
        "category": "Vermarktung",
        "subcategory": "Auktion"
    },
    {
        "title": "Anzahlung Käufer: Rechtslage",
        "content": """Anzahlung vor Notartermin: Nicht üblich, riskant. Absicherung: Notaranderkonto. Höhe: Maximal 5-10%. Rückzahlung: Bei Nicht-Zustandekommen. Wichtig: Nur über Notar, nie direkt an Verkäufer!""",
        "category": "Kaufrecht",
        "subcategory": "Anzahlung"
    },
    {
        "title": "Wohnrecht-Verkauf: Mit eingetragenem Wohnrecht",
        "content": """Verkauf mit Wohnrecht: Reduziert Kaufpreis erheblich (30-70% je nach Alter Berechtigtem). Käufer: Meist Familie oder Investoren. Kalkulation: Nach statistischer Lebenserwartung. Löschen: Nur mit Zustimmung Berechtigtem. Wichtig: Deutlicher Wert-Abschlag!""",
        "category": "Vermarktung",
        "subcategory": "Wohnrecht"
    },
    {
        "title": "Grundstück unbebaut: Vermarktung",
        "content": """Grundstücks-Vermarktung: Erschließung, Bebaubarkeit, Lage zentral. Zielgruppe: Bauträger, Bauherren. Unterlagen: Bebauungsplan, Bauvoranfrage, Bodengutachten. Preis: Nach Bodenrichtwert + Lage. Wichtig: Bebauungsmöglichkeiten klar darstellen!""",
        "category": "Vermarktung",
        "subcategory": "Grundstück"
    },
    {
        "title": "Abriss-Objekt: Verkauf",
        "content": """Abriss-Objekt: Wert im Grundstück, nicht Gebäude. Preis: Bodenrichtwert abzgl. Abrisskosten (50-150€/m³). Zielgruppe: Bauträger, Entwickler. Marketing: Entwicklungspotential betonen. Wichtig: Abrisskosten realistisch kalkulieren!""",
        "category": "Vermarktung",
        "subcategory": "Abriss-Objekt"
    },
    {
        "title": "Vermarktungsstrategie: Premium-Objekte",
        "content": """Premium-Vermarktung (>1 Mio€): Exklusives Marketing, hochwertige Präsentation, internationale Reichweite, Diskretion. Makler: Luxus-Spezialist. Kosten: 3-5% Provision. Dauer: Länger (6-18 Monate). Wichtig: Geduld, richtiger Makler essentiell!""",
        "category": "Vermarktung",
        "subcategory": "Premium"
    },
    {
        "title": "Schnellverkauf: Express-Ankauf",
        "content": """Express-Ankauf: Ankauf-Unternehmen kaufen sofort (1-4 Wochen). Preis: 60-80% Marktwert. Vorteil: Geschwindigkeit, Sicherheit. Nachteil: Preisabschlag. Zielgruppe: Zeitdruck, Notverkauf, Erbschaft. Wichtig: Mehrere Angebote einholen!""",
        "category": "Vermarktung",
        "subcategory": "Schnellverkauf"
    },
    {
        "title": "Teilweise vermietet: Vermarktung",
        "content": """Teilvermietet (z.B. Mehrfamilienhaus): Mischwert aus Eigennutzung + Kapitalanlage. Berechnung: Anteilig nach Nutzung. Zielgruppe: Selbstnutzer mit Zusatzeinkommen, Investoren. Marketing: Beide Aspekte betonen. Wichtig: Mietverträge offenlegen!""",
        "category": "Vermarktung",
        "subcategory": "Teilvermietet"
    },
    {
        "title": "Vermarktung Ferienimmobilie: Besonderheiten",
        "content": """Ferienimmobilie: Saisonale Vermarktung (Herbst/Winter für Sommerimmobilien). Zielgruppe: Eigennutzung + Vermietung. Rendite: Wichtig für Käufer. Lage: Tourismus-Region zentral. Wichtig: Vermietungspotential aufzeigen!""",
        "category": "Vermarktung",
        "subcategory": "Ferienimmobilie"
    },
    {
        "title": "Bieterverfahren: Ablauf",
        "content": """Bieterverfahren: Bei sehr begehrten Objekten. Ablauf: Angebotsfrist setzen (1-2 Wochen), schriftliche Gebote, höchstes Gebot gewinnt. Transparenz: Anzahl Bieter kommunizieren. Wichtig: Fair bleiben, keine fiktiven Bieter erfinden!""",
        "category": "Vermarktung",
        "subcategory": "Bieterverfahren"
    },
    {
        "title": "Nachbesserung Exposé: Optimierung",
        "content": """Exposé optimieren nach schwacher Response: Bessere Fotos, Preis anpassen, Beschreibung überarbeiten, andere Portale, Video hinzufügen. Test: A/B-Testing mit verschiedenen Versionen. Wichtig: Nach 2-4 Wochen ohne Erfolg optimieren!""",
        "category": "Vermarktung",
        "subcategory": "Exposé-Optimierung"
    },
    {
        "title": "Feedback Besichtigung: Nutzen",
        "content": """Besichtigungs-Feedback: Von Interessenten einholen (warum kein Kauf?). Erkenntnisse: Preis zu hoch, Zustand, Lage-Nachteile. Optimierung: Preis, Präsentation, Marketing anpassen. Wichtig: Ehrliches Feedback wertvoll für Anpassung!""",
        "category": "Vermarktung",
        "subcategory": "Feedback"
    },
    {
        "title": "Verkaufsdruck vermeiden: Ruhe bewahren",
        "content": """Verkaufsdruck (z.B. Umzug, Scheidung): Nicht zeigen! Taktik: Zeitdruck nicht kommunizieren, Alternative vorgeben, Untergrenze festlegen. Risiko: Käufer nutzen Druck aus. Wichtig: Professionelle Distanz wahren!""",
        "category": "Vermarktung",
        "subcategory": "Verkaufsdruck"
    },
    {
        "title": "Verkaufs-Erfolgsquote: Makler vs. privat",
        "content": """Erfolgsquote Makler: 80-90% verkaufen innerhalb 6 Monaten. Privat: 50-70%. Preisunterschied: Makler 5-10% höher trotz Provision. Zeitersparnis: 50-100 Stunden. Wichtig: Guter Makler lohnt sich!""",
        "category": "Vermarktung",
        "subcategory": "Erfolgsquote"
    },
    {
        "title": "Nachverkaufs-Service: Reputation",
        "content": """Nachverkaufs-Service: Erreichbarkeit nach Verkauf, Fragen beantworten, Empfehlungen. Reputation: Positive Bewertungen, Weiterempfehlung. Wichtig: Guter Service zahlt sich aus durch Weiterempfehlungen!""",
        "category": "Vermarktung",
        "subcategory": "Nachverkauf"
    },
    {
        "title": "Verkaufsunterlagen: Vollständigkeit",
        "content": """Vollständige Unterlagen: Grundbuchauszug, Energieausweis, Grundrisse, Nebenkostenabrechnungen (3 Jahre), Protokolle (WEG), Teilungserklärung, Baubeschreibung, Versicherungen. Vorteil: Schnellere Abwicklung, seriöser Eindruck. Wichtig: Vor Vermarktung zusammenstellen!""",
        "category": "Vermarktung",
        "subcategory": "Unterlagen"
    },
    {
        "title": "Digitalisierung: Virtuelle Notartermine",
        "content": """Virtuelle Notartermine: Seit 2022 bei einfachen Fällen möglich (Video-Identifizierung). Voraussetzung: Beide Parteien einverstanden. Vorteil: Zeitersparnis, Flexibilität. Kosten: Gleich. Wichtig: Noch nicht flächendeckend verfügbar!""",
        "category": "Kaufrecht",
        "subcategory": "Digitalisierung"
    },
    {
        "title": "Blockchain-Grundbuch: Zukunft",
        "content": """Blockchain-Grundbuch: Pilotprojekte laufen (Schweden, Dubai). Vorteil: Fälschungssicher, schneller, transparenter. Deutschland: Noch in Testphase. Zeitrahmen: 5-10 Jahre bis flächendeckend. Wichtig: Revolution des Immobilien-Kaufs steht bevor!""",
        "category": "Kaufrecht",
        "subcategory": "Blockchain"
    },
    {
        "title": "PropTech: Digitale Verkaufsplattformen",
        "content": """PropTech-Plattformen: Homeday, McMakler, ImmoScout24 (Verkaufsservice). Leistung: Online-Bewertung, Vermarktung, Besichtigungen, Abwicklung. Provision: 1-3% (günstiger als klassische Makler). Qualität: Unterschiedlich. Wichtig: Neue Alternative zu klassischen Maklern!""",
        "category": "Vermarktung",
        "subcategory": "PropTech"
    },
    {
        "title": "KI-Bewertung: Automatisierte Preisfindung",
        "content": """KI-Bewertung: Algorithmen analysieren Marktdaten, Vergleichswerte. Anbieter: PriceHubble, Sprengnetter. Genauigkeit: ±10-15%. Vorteil: Schnell, objektiv. Nachteil: Berücksichtigt Besonderheiten weniger. Wichtig: Als Basis-Tool gut, aber nicht alleinige Entscheidung!""",
        "category": "Bewertung",
        "subcategory": "KI-Bewertung"
    },
    {
        "title": "Smart Contract: Automatisierte Verträge",
        "content": """Smart Contracts: Blockchain-basierte selbstausführende Verträge. Anwendung: Kaufpreis-Freigabe automatisch bei Grundbuch-Eintragung. Vorteil: Schneller, sicherer, günstiger. Status: Noch nicht in Deutschland etabliert. Wichtig: Zukunftstechnologie für Immobilien-Transaktionen!""",
        "category": "Kaufrecht",
        "subcategory": "Smart Contract"
    }
]

print("🚀 BATCH 5: MAKLERRECHT & VERMARKTUNG - START")
print("=" * 60)

successful = 0
failed = 0
total_docs = len(documents)

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
        if i % 10 == 0:
            print(f"✅ {i}/{total_docs}: {doc['title'][:50]}...")
        
    except Exception as e:
        failed += 1
        print(f"❌ {i}/{total_docs}: {doc['title'][:50]} - {str(e)[:50]}")

print("\n" + "=" * 60)
print(f"✅ Erfolgreich: {successful}/{total_docs}")
print(f"❌ Fehlgeschlagen: {failed}")

try:
    count = client.count(collection_name="legal_documents")
    total = count.count
    print(f"\n🎯 GESAMT DOKUMENTE: {total}")
    print(f"📊 Noch {10000 - total} bis zur 10.000!")
    print(f"🔥 Fortschritt: {total/100}%")
except Exception as e:
    print(f"⚠️  Konnte Gesamtzahl nicht abrufen: {e}")

print("\n🔥 BATCH 5 COMPLETE! 🔥")
