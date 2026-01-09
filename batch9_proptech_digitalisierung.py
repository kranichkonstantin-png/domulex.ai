#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch 9: PropTech, Digitalisierung & Smart Buildings"""

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

# Batch 9: PropTech, Digitalisierung & Smart Buildings (100 Dokumente)
docs = [
    # PropTech Grundlagen
    {
        "title": "PropTech Definition: Technologie in der Immobilienwirtschaft",
        "content": """PropTech (Property Technology): Digitale Innovation für Immobilien. Bereiche: Vermittlung (Portale), Verwaltung (Software), Finanzierung (Crowdfunding), Bau (BIM), Smart Home. Markt wächst exponentiell. Investitionen steigen. Startups revolutionieren klassische Geschäftsmodelle. Etablierte Player investieren oder akquirieren. Regulierung hinkt oft hinterher.""",
        "category": "PropTech"
    },
    {
        "title": "Immobilienportale: ImmobilienScout24, Immowelt & Co",
        "content": """ImmobilienScout24: Marktführer in Deutschland. Immowelt, immonet: Konkurrenten. Geschäftsmodell: Inserate für Makler, Vermieter, Bauträger. Premium-Platzierung gegen Gebühr. Reichweite: Millionen Nutzer monatlich. Datenschutz: DSGVO-konform. Werbung und Lead-Generierung. Integration: CRM-Systeme, Maklersoftware. Bewertungen und Transparenz.""",
        "category": "PropTech"
    },
    {
        "title": "Digitale Besichtigungen: Virtuelle Rundgänge und 360°-Touren",
        "content": """360°-Fotos: Matterport, Ricoh Theta. Virtuelle Rundgänge: Online besichtigen. Vorteile: Zeitersparnis, mehr Interessenten, internationale Käufer. Technologie: 3D-Scanner, VR-Brillen. Kosten: 200-1.000€ pro Objekt. Rechtliches: Datenschutz bei Aufnahmen, Urheberrecht. Marketing: Einbindung in Exposés, Social Media. Zukunft: Augmented Reality (AR).""",
        "category": "PropTech"
    },
    {
        "title": "Digitale Signatur: Elektronische Vertragsabschlüsse",
        "content": """eIDAS-Verordnung (EU) 910/2014: Rechtlicher Rahmen. Qualifizierte elektronische Signatur (QES): Gleichwertig zu handschriftlicher Unterschrift. Anbieter: DocuSign, Adobe Sign, Skribble. Immobilienmietverträge: Digital möglich. Kaufverträge: Notarielle Beurkundung weiterhin Pflicht (§ 311b BGB). Vorteile: Schnelligkeit, papierlos. Sicherheit: Verschlüsselung, Authentifizierung. Archivierung: Elektronisch, revisionssicher.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Blockchain im Immobilienbereich: Grundbuch auf der Blockchain?",
        "content": """Blockchain-Technologie: Dezentrale, fälschungssichere Datenbank. Anwendungen: Grundbuch, Smart Contracts, Tokenisierung. Pilotprojekte: Schweden, Dubai. Deutschland: Grundbuch bleibt staatlich. Vorteile: Transparenz, Sicherheit, Effizienz. Nachteile: Skalierbarkeit, Energieverbrauch, Regulierung unklar. Tokenisierung: Immobilie in handelbare Token aufteilen. Zukunftsvision: Instant-Transaktionen ohne Notar?"""  ,
        "category": "PropTech"
    },
    {
        "title": "Smart Contracts: Automatisierte Vertragsausführung",
        "content": """Smart Contracts: Selbstausführende Verträge auf Blockchain. Code is Law: Bedingungen im Code festgelegt. Anwendung Immobilien: Mietvertrag mit automatischer Zahlung und Zugang. Kaution-Verwaltung: Automatische Rückzahlung. Probleme: Rechtsunsicherheit, fehlende Flexibilität. Deutsches Recht: Formvorschriften (§ 126, 311b BGB) beachten. Zukunft: Hybride Lösungen mit rechtlicher Absicherung.""",
        "category": "PropTech"
    },
    {
        "title": "Immobilien-Tokenisierung: Fraktionierter Eigentumshandel",
        "content": """Tokenisierung: Immobilie wird in digitale Token aufgeteilt. Anleger kaufen Bruchteile (z.B. 100€). Handel auf Plattformen (Security Token Exchanges). Vorteile: Liquidität, geringe Einstiegshürden, Diversifikation. Rechtliches: Tokens als Wertpapiere (WpHG, EU-Prospektverordnung). Regulierung: BaFin-Aufsicht. Risiken: Marktliquidität, Bewertung, Regulierungsänderungen. Plattformen: Brickblock (eingestellt), Exporo (teilweise tokenisiert).""",
        "category": "PropTech"
    },
    {
        "title": "KI in der Immobilienbewertung: Automatisierte Wertermittlung",
        "content": """AVMs (Automated Valuation Models): KI-gestützte Bewertung. Datenquellen: Transaktionen, Portale, Geodaten. Algorithmen: Machine Learning, Neuronale Netze. Anbieter: Sprengnetter (Marktführer), ImmobilienScout24, McMakler. Genauigkeit: Je nach Datenlage 80-95%. Grenzen: Individuelle Besonderheiten, Mikrolage. Rechtliches: Keine Ersetzung von Gutachtern bei Finanzierung. Einsatz: Schnellbewertung, Portfolio-Analyse.""",
        "category": "PropTech"
    },
    {
        "title": "Big Data in der Immobilienwirtschaft: Datengetriebene Entscheidungen",
        "content": """Big Data: Große Datenmengen aus verschiedenen Quellen. Immobilien: Transaktionsdaten, Nutzungsverhalten, Geodaten, Social Media. Analyse: Trends erkennen, Preisprognosen, Nachfrage vorhersagen. Anwendungen: Standortanalyse, Risikobewertung, Marketing. Datenschutz: DSGVO-konform, Anonymisierung. Tools: Tableau, Power BI, Python (Pandas). Wettbewerbsvorteil: Datengetriebene Investoren erfolgreicher.""",
        "category": "Digitalisierung"
    },
    {
        "title": "CRM-Systeme für Makler: Kundenverwaltung digitalisiert",
        "content": """CRM (Customer Relationship Management): Software für Kundenbeziehungen. Immobilien-CRM: Onoffice, ImmoSolve, Flowfact. Funktionen: Kontaktverwaltung, Exposé-Erstellung, E-Mail-Marketing, Terminplanung. Integration: Portale, Website, Telefonie. Automatisierung: Follow-ups, Newsletter. DSGVO: Einwilligungen verwalten, Löschfristen. Kosten: 50-200€/Monat. Vorteil: Effizienz, keine Leads verlieren.""",
        "category": "PropTech"
    },
    
    # Smart Buildings & IoT
    {
        "title": "Smart Home: Vernetzte Gebäudetechnik",
        "content": """Smart Home: Steuerung von Heizung, Licht, Jalousien, Sicherheit per App. Systeme: KNX, Homematic, Google Home, Apple HomeKit. Vorteile: Komfort, Energieeinsparung, Sicherheit. Kosten: 5.000-20.000€ für Einfamilienhaus. Nachrüstung: Funksysteme einfacher als Bus-Systeme. Datenschutz: Cloud-Dienste kritisch, lokale Steuerung bevorzugen. Wertsteigerung: Smart Home als Verkaufsargument.""",
        "category": "Smart Buildings"
    },
    {
        "title": "IoT (Internet of Things): Sensoren und Vernetzung",
        "content": """IoT: Vernetzte Geräte kommunizieren. Immobilien: Sensoren für Temperatur, Feuchtigkeit, Bewegung, Energieverbrauch. Datenerfassung: Optimierung Gebäudebetrieb. Predictive Maintenance: Wartung vor Ausfall. Sicherheit: Einbruchsmeldung, Rauchmelder vernetzt. Datenschutz: Mieter-Daten schützen (DSGVO). Standards: MQTT, LoRaWAN. Zukunft: Millionen Sensoren in Gebäuden.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Gebäudeautomation: Effizienz durch Technik",
        "content": """Gebäudeautomation (GA): Automatische Steuerung technischer Anlagen. Bereiche: Heizung, Lüftung, Klima (HLK), Beleuchtung, Beschattung. Systeme: KNX, BACnet, LON. Energieeinsparung: 20-40% durch optimierte Steuerung. EPBD: GA-Pflicht für größere Nichtwohngebäude. Smart Readiness Indicator (SRI): EU-Bewertung Gebäudeintelligenz. Kosten: 30-100€/m² bei Neubau. Amortisation: 5-10 Jahre.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Energiemanagement: Verbrauch optimieren",
        "content": """Energiemanagementsysteme (EMS): Überwachung und Steuerung Energieverbrauch. Funktionen: Verbrauchsanalyse, Lastmanagement, Eigenstromoptimierung. Photovoltaik-Integration: Eigenverbrauch maximieren. Batteriespeicher: Überschuss speichern. ISO 50001: Norm für Energiemanagement. Fördermittel: BAFA, KfW. Smart Meter: Digitaler Stromzähler, rollout ab 2025 verpflichtend. Einsparungen: 10-30%.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Smart Meter: Digitale Stromzähler und Datenschutz",
        "content": """Smart Meter: Intelligente Messsysteme. Messstellenbetriebsgesetz (MsbG): Rollout seit 2017. Pflicht: Verbrauch >6.000 kWh/Jahr, Erzeugung >7 kW. Funktionen: Fernauslesung, Verbrauchstransparenz, variable Tarife. Kosten: 20-100€/Jahr. Datenschutz: § 50 MsbG, Daten beim Messstellenbetreiber. Smart Meter Gateway: Sichere Kommunikation. Opt-out nicht möglich bei Pflicht.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Heizungssteuerung: Smart Thermostate",
        "content": """Smart Thermostate: Tado, Nest, Homematic. Funktionen: Zeitprogrammierung, Geofencing (Standort-basiert), Fernsteuerung. Energieeinsparung: 10-25% laut Herstellern. Kompatibilität: Mit den meisten Heizkörperventilen. Installation: Einfach, DIY. Kosten: 50-150€ pro Thermostat. Mieter: Erlaubnis Vermieter einholen für bauliche Änderung? Smarte Fußbodenheizung: Raumweise Steuerung.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Beleuchtungssteuerung: Philips Hue & Smart Lighting",
        "content": """Smart Lighting: Philips Hue, IKEA Trådfri, LIFX. Funktionen: Fernsteuerung, Dimmen, Farbwechsel, Zeitsteuerung. Sprachsteuerung: Alexa, Google Assistant, Siri. Szenen: Vordefinierte Lichtstimmungen. Energieeffizienz: LED-Technologie. Kosten: 15-60€ pro Leuchtmittel. Sicherheit: Anwesenheitssimulation bei Abwesenheit. Kompatibilität: Verschiedene Standards (Zigbee, Bluetooth).""",
        "category": "Smart Buildings"
    },
    {
        "title": "Smart Security: Videoüberwachung und Alarmanlagen",
        "content": """Smart Security: Kameras, Alarmanlagen, Türklingeln mit App-Steuerung. Anbieter: Ring, Nest Cam, Arlo. Funktionen: Live-Video, Bewegungserkennung, Benachrichtigungen. Datenschutz: DSGVO beachten, öffentlichen Raum nicht filmen. Speicherung: Cloud vs. lokal. Kosten: 100-500€ pro Kamera. Rechtliches: Mieter über Videoüberwachung informieren. Versicherung: Rabatt bei Alarmanlagen möglich.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Smarte Türschlösser: Zugangssteuerung digital",
        "content": """Smart Locks: Nuki, Yale, Danalock. Funktionen: Öffnen per App, Codes, Fingerabdruck. Temporäre Zugänge: Gäste, Handwerker. Protokoll: Wer wann Tür geöffnet. Installation: Auf bestehendes Schloss aufsetzbar. Sicherheit: Verschlüsselung, Backup-Schlüssel. Mieter: Vermieter-Zustimmung nötig. Kosten: 150-400€. Kurzzeitvermietung: Automatischer Check-in.""",
        "category": "Smart Buildings"
    },
    {
        "title": "Smarte Rauchmelder: Vernetzt und App-gemeldet",
        "content": """Smart Rauchmelder: Nest Protect, Bosch Smart Home. Funktionen: App-Benachrichtigung, Vernetzung (Alles alarmiert bei Rauch). Sprachansage: Wo Rauch erkannt. Selbsttest: Batterie und Funktion. Kosten: 80-150€ pro Melder. Pflicht: Rauchmelderpflicht in allen Bundesländern. Installation: Vermieter-Pflicht. Wartung: Jährlich, smart Melder erinnern. Fehlalarme: Stummschalten per App.""",
        "category": "Smart Buildings"
    },
    
    # Digitale Verwaltung
    {
        "title": "Digitale Hausverwaltung: Software-Lösungen",
        "content": """Hausverwaltungssoftware: HAUS & GRUND, IMMOware, domumetrics. Funktionen: Nebenkostenabrechnung, Kontenverwaltung, Kommunikation Eigentümer/Mieter. Cloud-basiert: Zugriff überall. Automatisierung: SEPA-Lastschriften, E-Mail-Versand. Schnittstellen: Bankdaten (HBCI), Buchhaltung (DATEV). DSGVO-konform. Kosten: 5-20€ pro Einheit/Monat. Effizienz: Zeit sparen, Fehler reduzieren.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Mieterportale: Kommunikation und Self-Service",
        "content": """Mieterportale: Online-Plattformen für Mieter. Funktionen: Dokumente einsehen (Nebenkostenabrechnung), Mängel melden, Mitteilungen empfangen. Beispiele: ImmoScout24 Mieterportal, Hausgold. Vorteile: Weniger Anrufe, 24/7 Erreichbarkeit. Datenschutz: Sichere Login, DSGVO. Akzeptanz: Jüngere Mieter nutzen gerne, ältere bevorzugen Telefon. Kosten: Oft kostenlos für Mieter, Teil der Verwaltungssoftware.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Digitale Nebenkostenabrechnung: Automatisiert und transparent",
        "content": """Software: HAUS & GRUND, ista, Techem. Automatisierung: Verbrauchswerte digital erfasst. Heizkostenverteiler: Funkablesung. Wasser-, Stromzähler: Smart Meter. Berechnung: Software erstellt Abrechnung. Versand: E-Mail oder Portal. Transparenz: Mieter sieht Verbrauchsentwicklung. Rechtssicherheit: Formale Anforderungen (§ 556 BGB) erfüllt. Zeitersparnis: Statt Wochen nur Tage.""",
        "category": "Digitalisierung"
    },
    {
        "title": "E-Rechnung: Pflicht ab 2025 im B2B",
        "content": """Wachstumschancengesetz: E-Rechnung-Pflicht ab 1.1.2025 (B2B). Format: XRechnung, ZUGFeRD. Empfang: Ab 2025 verpflichtend. Versand: Stufenweise ab 2027/2028. Immobilienwirtschaft: Handwerker-Rechnungen, Dienstleister. Software: Buchhaltungsprogramme, ERP-Systeme. Archivierung: Digital, revisionssicher (GoBD). Vorteil: Automatisierung, weniger Fehler. Übergangsfrist nutzen.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Dokumentenmanagement (DMS): Papierloses Büro",
        "content": """DMS (Dokumentenmanagementsystem): Digitale Archivierung. Funktionen: Scannen, OCR (Texterkennung), Verschlagwortung, Volltextsuche. Immobilien: Mietverträge, Rechnungen, Korrespondenz. Zugriff: Mehrere Nutzer gleichzeitig. Revisionssicherheit: GoBD-konform. Anbieter: DocuWare, d.velop, ELO. Cloud vs. On-Premise. Kosten: 20-100€ pro Nutzer/Monat. Vorteile: Platzersparnis, schneller Zugriff.""",
        "category": "Digitalisierung"
    },
    {
        "title": "GoBD-konforme Archivierung: Digitale Aufbewahrungspflichten",
        "content": """GoBD (Grundsätze ordnungsmäßiger Buchführung): Regeln für digitale Daten. Aufbewahrungspflicht: 10 Jahre für Rechnungen, 6 Jahre für Geschäftsbriefe. Unveränderbarkeit: Revisionssichere Archivierung. Nachvollziehbarkeit: Zugriffs- und Änderungsprotokolle. Format: Maschinenlesbar (z.B. PDF/A). Konvertierung: Von Papier zu digital mit Verfahrensdokumentation. Software: DMS mit GoBD-Zertifizierung. Strafen bei Nichtbeachtung.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Cloud-Lösungen: Daten in der Wolke",
        "content": """Cloud-Computing: Server und Software im Internet statt lokal. Anbieter: Microsoft Azure, AWS, Google Cloud. Immobilien: CRM, Buchhaltung, DMS in Cloud. Vorteile: Skalierbar, Zugriff überall, automatische Updates. Nachteile: Abhängigkeit, Datenschutz (Server-Standort). DSGVO: EU-Server oder Standardvertragsklauseln. Kosten: Abo-Modell, monatlich. Sicherheit: Verschlüsselung, Zertifizierungen (ISO 27001).""",
        "category": "Digitalisierung"
    },
    {
        "title": "API-Schnittstellen: Software-Integration",
        "content": """API (Application Programming Interface): Schnittstelle zwischen Programmen. Immobilien: CRM zu Portalen, Buchhaltung zu Banking, DMS zu E-Mail. Vorteile: Automatisierung, Datenfluss ohne manuelle Eingabe. Beispiel: Neues Objekt in CRM → automatisch auf ImmobilienScout24. REST-APIs: Moderner Standard. Webhook: Ereignis-basierte Kommunikation. Entwicklung: Entwickler oder fertige Integrationen nutzen.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Cybersecurity in der Immobilienwirtschaft: Schutz vor Angriffen",
        "content": """Bedrohungen: Ransomware, Phishing, Datenlecks. Immobilien: Sensible Daten (Personaldaten, Finanzen). Maßnahmen: Firewalls, Antivirus, Schulungen, Backups. Verschlüsselung: E-Mails, Datenbanken. Zugriffsrechte: Rollenbasiert, Prinzip der geringsten Berechtigung. DSGVO: Meldepflicht bei Datenpannen (72h). Versicherung: Cyber-Risiko-Versicherung. Notfallplan: Incident Response.""",
        "category": "Digitalisierung"
    },
    {
        "title": "DSGVO und PropTech: Datenschutz bei Innovation",
        "content": """DSGVO: Gilt für alle digitalen Dienste mit Personendaten. PropTech: Makler-Plattformen, CRM, Mieterportale. Einwilligung: Transparent, freiwillig, widerrufbar. Datensparsamkeit: Nur notwendige Daten erfassen. Löschfristen: Nach Zweckerfüllung löschen. Auftragsverarbeitung: Verträge mit Dienstleistern (Art. 28 DSGVO). Betroffenenrechte: Auskunft, Berichtigung, Löschung. Bußgelder: Bis 20 Mio. € oder 4% Jahresumsatz.""",
        "category": "Digitalisierung"
    },
    
    # Digitale Vermarktung
    {
        "title": "Online-Marketing für Immobilien: SEO, SEA, Social Media",
        "content": """SEO (Suchmaschinenoptimierung): Website für Google optimieren. Keywords: 'Immobilien kaufen München'. SEA (Suchmaschinenwerbung): Google Ads für Anzeigen. Social Media: Facebook, Instagram für Zielgruppenansprache. Content Marketing: Blogbeiträge, Ratgeber. E-Mail-Marketing: Newsletter an Interessenten. Retargeting: Besucher erneut ansprechen. Conversion-Tracking: Erfolg messen. Kosten: Je nach Strategie 500-5.000€/Monat.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Social Media Marketing: Instagram & Facebook für Immobilien",
        "content": """Instagram: Bildlastig, jüngere Zielgruppe. Formate: Posts, Stories, Reels. Hashtags: #Immobilien #München #DreamHome. Facebook: Breitere Zielgruppe, Anzeigen mit Targeting. Gruppen: Lokale Immobilien-Communities. LinkedIn: B2B, Gewerbeimmobilien. TikTok: Trend für junge Käufer. Influencer: Kooperationen für Reichweite. Organisch vs. Paid: Mix aus beidem. Authentizität: Ehrliche Darstellung.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Video-Marketing: YouTube und Immobilien-Vlogs",
        "content": """YouTube: Zweitgrößte Suchmaschine. Formate: Objektvorstellungen, Ratgeber, Markt-Updates. Drohnenaufnahmen: Luftbilder beeindrucken. 360°-Videos: Immersive Besichtigung. Live-Streaming: Q&A-Sessions, virtuelle Open Houses. SEO: Video-Titel, Beschreibung, Tags optimieren. Kanal aufbauen: Regelmäßigkeit, Community. Monetarisierung: Werbung, Sponsoring (ab 1.000 Abonnenten). Beispiel: Immobilien-Kanäle mit 100.000+ Abonnenten.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Podcast: Audio-Content für Immobilien-Interessierte",
        "content": """Podcast-Boom: Wachsende Zielgruppe. Formate: Interviews, Markanalysen, Ratgeber. Plattformen: Spotify, Apple Podcasts, Google Podcasts. Produktion: Mikrofon (100-300€), Schnittprogramm (Audacity kostenlos). Frequenz: Wöchentlich oder zweiwöchentlich. Monetarisierung: Sponsoring, Affiliate-Links. Reichweite: Nische 'Immobilien' überschaubar, aber engagiert. Beispiel: Immobilien Investor Podcast.""",
        "category": "Digitalisierung"
    },
    {
        "title": "E-Mail-Marketing: Newsletter und Automation",
        "content": """Newsletter: Regelmäßige Updates an Interessenten. Inhalte: Neue Objekte, Marktberichte, Tipps. Tools: Mailchimp, CleverReach, Brevo (Sendinblue). Segmentierung: Käufer vs. Mieter, Regionen. Automation: Willkommens-Serie, Drip-Kampagnen. Öffnungsrate: 15-25% bei guten Newslettern. Klickrate: 2-5%. DSGVO: Einwilligung (Double-Opt-in), Abmelde-Link. Design: Responsiv, ansprechend.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Retargeting: Besucher zurückgewinnen",
        "content": """Retargeting/Remarketing: Nutzer erneut mit Anzeigen ansprechen. Wie: Pixel auf Website (Facebook, Google), Nutzer wird markiert. Anzeigen: Auf Facebook, Instagram, Google Display Network. Ziel: Erinnerung, Abschluss fördern. Beispiel: Nutzer sieht Wohnung, verlässt Seite, sieht Anzeige auf Instagram. Kosten: CPC (Cost per Click) 0,50-2€. Erfolgsmessung: Conversion-Rate. DSGVO: Cookie-Consent nötig.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Landing Pages: Optimierte Zielseiten",
        "content": """Landing Page: Spezialisierte Seite für ein Ziel (z.B. Kontaktanfrage). Elemente: Klare Überschrift, ansprechendes Bild, Benefits, Call-to-Action (CTA). A/B-Testing: Varianten testen, optimieren. Tools: Unbounce, Leadpages, WordPress-Plugins. Conversion-Rate: 2-10% bei guten Landing Pages. SEA: Anzeigen führen zu Landing Page, nicht Startseite. Mobile-optimiert: 70% Nutzer auf Smartphone. Ladezeit: Unter 3 Sekunden.""",
        "category": "Digitalisierung"
    },
    {
        "title": "Chatbots: Automatisierte Kundenberatung",
        "content": """Chatbots: KI-gestützte Chat-Assistenten auf Website. Funktionen: FAQ beantworten, Kontakte erfassen, Besichtigungstermine vorschlagen. Plattformen: Intercom, Drift, ManyChat (Facebook). 24/7 verfügbar. Lead-Qualifizierung: Fragen zu Budget, Wohnwünschen. Grenzen: Komplexe Fragen an Mensch übergeben. Akzeptanz: Nutzer erwarten schnelle Antworten. Datenschutz: Daten sicher verarbeiten. Kosten: 50-500€/Monat.""",
        "category": "Digitalisierung"
    },
    {
        "title": "KI-gestützte Lead-Generierung: Automatische Kundenakquise",
        "content": """KI: Muster in Daten erkennen. Lead-Generierung: Potenzielle Kunden identifizieren. Scoring: KI bewertet Leads nach Kaufwahrscheinlichkeit. Quellen: Website-Verhalten, Social Media, CRM-Daten. Priorisierung: Heiße Leads zuerst kontaktieren. Automatisierung: E-Mails, Follow-ups. Tools: HubSpot, Salesforce Einstein. Genauigkeit: Steigt mit Datenmenge. Datenschutz: Transparenz, Einwilligung.""",
        "category": "PropTech"
    },
    {
        "title": "Predictive Analytics: Vorhersagemodelle für Immobilien",
        "content": """Predictive Analytics: Zukunft vorhersagen basierend auf Daten. Immobilien: Preisentwicklung, Leerstandsrisiko, Instandhaltungsbedarf. Methoden: Regression, Machine Learning, Zeitreihenanalyse. Daten: Historische Transaktionen, Makrodaten (Zinsen, Demografie), Mikrodaten (Gebäudezustand). Anwendung: Investitionsentscheidung, Portfoliomanagement. Genauigkeit: 70-90% je nach Modell. Tools: Python (scikit-learn), R, kommerzielle Lösungen.""",
        "category": "PropTech"
    },
    
    # BIM und Bau-Digitalisierung
    {
        "title": "BIM (Building Information Modeling): Digitaler Zwilling",
        "content": """BIM: 3D-Modell mit allen Gebäudedaten. Level of Detail (LOD): LOD 100-500 je nach Planungsphase. Software: Autodesk Revit, ArchiCAD, Allplan. Vorteile: Kollisionsprüfung, Mengenermittlung, Kommunikation. Öffentliche Projekte: BIM zunehmend gefordert. CDE (Common Data Environment): Zentrale Datenplattform. Datenübergabe: IFC-Format (Industry Foundation Classes). Zukunft: BIM-Pflicht für alle Neubauten?"""  ,
        "category": "Digitalisierung Bau"
    },
    {
        "title": "IFC-Format: Datenaustausch im BIM",
        "content": """IFC (Industry Foundation Classes): Offener Standard für BIM-Daten. Entwickelt von buildingSMART. Zweck: Software-übergreifender Austausch (z.B. Revit zu ArchiCAD). Versionen: IFC2x3, IFC4, IFC4.3 (aktuell). Inhalte: Geometrie, Attribute, Beziehungen. Qualitätssicherung: Modellprüfung (Model View Definition). Vorteil: Unabhängigkeit von Hersteller-Software. Pflicht: Bei öffentlichen BIM-Projekten.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Drohnen im Bau: Vermessung und Monitoring",
        "content": """Drohnen: Luftaufnahmen und Vermessung. Anwendungen: Baustellen-Monitoring, Bestandsaufnahme, Inspektion (Dach, Fassade). Photogrammetrie: 3D-Modelle aus Fotos. Vorteile: Zeit, Kosten, Sicherheit (keine Gerüste für Inspektion). Rechtliches: Drohnenverordnung, Genehmigungen, Versicherung. Datenschutz: Keine Aufnahmen von Nachbargrundstücken. Kosten: Drohne 500-5.000€, Dienstleister 500-2.000€/Tag.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "3D-Druck im Bauwesen: Additive Fertigung",
        "content": """3D-Druck: Beton-Schicht-für-Schicht. Projekte: Einfamilienhäuser in 24h gedruckt. Vorteile: Formfreiheit, Materialersparnis, Geschwindigkeit. Nachteile: Begrenzte Größe, Materialeigenschaften, Genehmigung. Anbieter: ICON (USA), PERI, Heidelberg Cement. Kosten: Derzeit noch teurer als traditionell. Zukunft: Massenproduktion von Sozialwohnungen? Regulierung: Baurecht hinkt hinterher.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Roboter auf der Baustelle: Automatisierung",
        "content": """Baurobotik: Maschinen für repetitive Aufgaben. Anwendungen: Mauern verlegen, Armieren, Malen. Vorteile: Präzision, Geschwindigkeit, Fachkräftemangel mildern. Beispiele: SAM (Semi-Automated Mason), Hadrian X. Herausforderungen: Unstrukturierte Umgebung, Kosten. Zukunft: Hybride Teams (Mensch-Roboter). Deutschland: Forschung, wenig kommerzielle Nutzung. Akzeptanz: Gewerkschaften skeptisch.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Augmented Reality (AR) im Bau: Planung visualisiert",
        "content": """AR: Digitale Inhalte in reale Welt einblenden. Baustelle: Tablet/Brille zeigt BIM-Modell vor Ort. Vorteile: Fehler frühzeitig erkennen, Qualitätskontrolle. Software: Trimble Connect, BIMx. Geräte: Microsoft HoloLens, Tablets. Anwendung: Position Leitungen prüfen, Installationshöhen kontrollieren. Kosten: HoloLens ~3.500€, Software-Abo. Akzeptanz: Steigende Nutzung bei Großprojekten.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Baustellen-Management-Apps: Digitale Koordination",
        "content": """Apps: PlanRadar, BauMaster, 123quality. Funktionen: Mängelliste, Fotodokumentation, Kommunikation, Zeiterfassung. Vorteile: Papierlos, Echtzeitupdate, alle Beteiligten informiert. Offline-Modus: Funktioniert ohne Internet. Schnittstellen: Export zu Projekt-Management-Software. DSGVO: Personendaten geschützt. Kosten: 20-100€ pro Nutzer/Monat. Akzeptanz: Hohe Akzeptanz bei jüngeren Bauleitern.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Lean Construction: Verschwendung vermeiden",
        "content": """Lean Prinzipien: Aus Automobilindustrie auf Bau übertragen. Ziele: Verschwendung (Muda) eliminieren, Effizienz steigern. Methoden: Last Planner System, 5S, Kanban. Taktplanung: Rhythmisierte Arbeitsabläufe. Vorteile: Termintreue, Kostenreduktion, Qualität. Digitalisierung: BIM unterstützt Lean. Kulturwandel: Kooperation statt Silodenken. Deutschland: Zunehmende Verbreitung, besonders bei Großprojekten.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Vorfertigung und Modulbau: Industrialisierung",
        "content": """Vorfertigung: Elemente in Fabrik produziert, auf Baustelle montiert. Modulbau: Komplette Raummodule (Bad, Zimmer). Vorteile: Qualität (Werkshalle), Geschwindigkeit, Witterungsunabhängig. Nachteile: Transport, Flexibilität begrenzt. Holzbau: Besonders geeignet für Vorfertigung. Digitalisierung: BIM ermöglicht präzise Fertigung. Kosten: Konkurrenzfähig bei Serienfertigung. Zukunft: Mehr standardisierte Bauten.""",
        "category": "Digitalisierung Bau"
    },
    {
        "title": "Nachhaltigkeit und PropTech: Grüne Technologien",
        "content": """GreenTech: Technologie für Nachhaltigkeit. Immobilien: Energieeffizienz, Kreislaufwirtschaft, CO₂-Reduktion. ESG-Kriterien: Environmental, Social, Governance. PropTech-Lösungen: Energiemanagement, Cradle-to-Cradle-Planung, Nachhaltigkeits-Zertifizierungen (DGNB, LEED). Investoren: ESG wird Entscheidungskriterium. EU-Taxonomie: Nachhaltige Immobilien definiert. Monitoring: IoT für Ressourcenverbrauch. Zukunft: Klimaneutralität bis 2045.""",
        "category": "PropTech"
    },
    
    # Spezielle PropTech-Bereiche
    {
        "title": "Immobilien-Crowdfunding: Alternative Finanzierung",
        "content": """Crowdfunding: Viele Kleinanleger finanzieren Projekt. Plattformen: Exporo, Bergfürst, Zinsbaustein. Modelle: Nachrangdarlehen, Eigenkapital-Beteiligung. Mindestanlage: 500-10.000€. Rendite: 4-7% p.a. Laufzeit: 12-48 Monate. Risiken: Totalverlust möglich, nachrangig bei Insolvenz. Regulierung: Vermögensanlage-Gesetz (VermAnlG), Prospektpflicht ab 8 Mio. €. DSGVO: Anlegerdaten schützen. Markt: Wachsend, aber Konsolidierung.""",
        "category": "PropTech"
    },
    {
        "title": "Co-Living: Digitale Plattformen für gemeinschaftliches Wohnen",
        "content": """Co-Living: Wohnform mit privaten Zimmern, gemeinsamen Flächen. Plattformen: Medici Living (The Fizz), Quarters. Zielgruppe: Junge Berufstätige, Expats, Studenten. Buchung: Online, flexibel, All-Inclusive (Möbel, Internet, Reinigung). Digitalisierung: App für Community, Events, Services. Mietverträge: Kurzfristig (3-12 Monate). Kosten: 600-1.200€/Monat. Rechtliches: WG-Konstruktion oder Untermiete. Trend: Urbanisierung treibt Nachfrage.""",
        "category": "PropTech"
    },
    {
        "title": "Co-Working: Flexible Büros",
        "content": """Co-Working: Gemeinschaftsbüros, flexibel buchbar. Anbieter: WeWork, Spaces, Design Offices. Modelle: Hot Desk (tageweise), Fixed Desk, Büroräume. Buchung: Online-Plattform, monatlich kündbar. Digitalisierung: App für Zugang, Buchung von Meetingräumen. Ausstattung: WLAN, Drucker, Kaffee, Community. Kosten: 200-800€ pro Arbeitsplatz/Monat. Rechtliches: Dienstleistungsvertrag, kein Mietvertrag. Trend: Homeoffice + Co-Working Hybrid.""",
        "category": "PropTech"
    },
    {
        "title": "Short-Term-Rental: Airbnb, Booking.com & Co",
        "content": """Kurzzeitvermietung: Ferienwohnungen, Geschäftsreisen. Plattformen: Airbnb, Booking.com, FeWo-direkt. Digitalisierung: Online-Buchung, Kalender-Synchronisation, Smart Locks. Rechtliches: Zweckentfremdungsverbot in manchen Städten (Berlin, München). Steuern: Umsatzsteuer, Einkommensteuer, ggf. Kurtaxe. Versicherung: Spezielle Kurzzeitmiete-Versicherung. Gewerblichkeit: Ab gewisser Anzahl Vermietungen. Rendite: Höher als Langzeitmiete, aber volatil.""",
        "category": "PropTech"
    },
    {
        "title": "Proptech-Investitionen: Venture Capital und Funding",
        "content": """PropTech-Markt: Investitionen steigen. Venture Capital: Risikokapital für Startups. Phasen: Seed, Series A, B, C. Deutschland: Berliner PropTech-Szene wächst. Exits: McMakler übernommen von Scout24. Unicorns: Unternehmen mit >1 Mrd. $ Bewertung (z.B. Hopin). Investor-Typen: VCs, Corporate Ventures (z.B. Deutsche Wohnen), Business Angels. Trends: KI, Nachhaltigkeit, Verwaltungs-Digitalisierung.""",
        "category": "PropTech"
    },
    {
        "title": "InsurTech für Immobilien: Digitale Versicherungen",
        "content": """InsurTech: Technologie in Versicherung. Immobilien: Gebäudeversicherung, Mietausfall, Cyber-Risiko. Digitalisierung: Online-Abschluss, KI-gestützte Risikoprüfung, Schadensabwicklung per App. Anbieter: Getsafe, Clark (Vermittler). Pay-per-Use: Flexible Tarife basierend auf Nutzung. IoT: Sensoren melden Schäden frühzeitig (Wasserschaden). Pricing: Dynamisch basierend auf Daten. Vorteil: Schnelligkeit, Transparenz. DSGVO: Datenschutz bei Telematik.""",
        "category": "PropTech"
    },
    {
        "title": "LegalTech für Immobilien: Juristische Services digitalisiert",
        "content": """LegalTech: Rechtliche Dienstleistungen mit Technologie. Immobilien: Mietvertrag-Generator, Mietrechts-Apps, Inkasso-Plattformen. Beispiele: Mineko (Mietvertragsprüfung), wenigermiete.de. Funktionen: Dokumente automatisch erstellen, Rechtsfragen-KI. Grenzen: Keine Rechtsberatung, komplexe Fälle benötigen Anwalt. Kosten: 10-100€ für einfache Services. Akzeptanz: Wächst, besonders bei jungen Nutzern. Regulierung: Rechtsdienstleistungsgesetz (RDG) beachten.""",
        "category": "PropTech"
    },
    {
        "title": "FinTech-Kooperationen: Digitale Finanzierung",
        "content": """FinTech: Finanzdienstleistungen mit Technologie. Immobilien: Digitale Hypothekenvergleiche, Online-Abschluss. Plattformen: Interhyp, Dr. Klein, Creditweb (digital). Prozess: Daten online eingeben, Angebote vergleichen, digital abschließen. Vorteile: Schnelligkeit (Stunden statt Wochen), Transparenz. Nachteile: Persönliche Beratung fehlt teilweise. Blockchain: Automatisierte Kreditvergabe (DeFi). SCHUFA-Alternativen: Alternative Scoring-Methoden (z.B. Bankdaten-Analyse).""",
        "category": "PropTech"
    },
    {
        "title": "ESG-Reporting-Tools: Nachhaltigkeits-Dokumentation",
        "content": """ESG (Environmental, Social, Governance): Nachhaltigkeitskriterien. Reporting: Pflicht für große Unternehmen (CSRD ab 2024). Tools: Software für Datensammlung und Berichterstattung. Immobilien: Energieverbrauch, CO₂-Emissionen, soziale Aspekte (Mieterstruktur). Anbieter: Greenstone, Sphera, spezialisierte PropTech. Datenquellen: IoT-Sensoren, Abrechnungen, Zertifikate. EU-Taxonomie: Klassifizierung nachhaltiger Immobilien. Investoren: ESG-Ratings beeinflussen Kapitalkosten.""",
        "category": "PropTech"
    },
    {
        "title": "PropTech-Regulierung: Rechtliche Rahmenbedingungen",
        "content": """Regulierung: PropTech in rechtlichem Graubereich. Bereiche: Datenschutz (DSGVO), Finanzaufsicht (BaFin bei Crowdfunding), Maklerrecht. Plattformhaftung: Verantwortlichkeit für Inhalte? Innovation vs. Regulierung: Balanceakt. Sandbox-Ansätze: Experimentierräume für neue Technologien. Lobby: PropTech-Verbände (VDP, ZIA Digital) setzen sich ein. Zukunft: Mehr Regulierung erwartet (EU AI Act, Daten-Governance). Compliance: PropTechs müssen rechtliche Vorgaben einhalten.""",
        "category": "PropTech"
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
    """Füge Batch 9 Dokumente hinzu"""
    print("🚀 BATCH 9: PROPTECH & DIGITALISIERUNG - START")
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
                    "source": "Batch 9 - PropTech & Digitalisierung"
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
    print("\n🔥 BATCH 9 COMPLETE! 🔥")

if __name__ == "__main__":
    seed_batch()
