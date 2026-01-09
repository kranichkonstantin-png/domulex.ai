#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch 8: Internationale Aspekte, EU-Recht & Grenzüberschreitende Immobilientransaktionen"""

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

# Batch 8: Internationale Immobilientransaktionen & EU-Recht (90 Dokumente)
docs = [
    # EU-Grundlagen
    {
        "title": "EU-Niederlassungsfreiheit: Immobilienerwerb durch EU-Bürger",
        "content": """Nach Art. 49, 63 AEUV haben EU-Bürger Niederlassungsfreiheit und freien Kapitalverkehr. Diskriminierungsverbot beim Immobilienerwerb. Keine Beschränkungen für EU-Bürger in Deutschland. Ausnahmen nur bei zwingenden Allgemeininteressen (z.B. Raumordnung). Meldepflichten beachten. Steuerliche Gleichbehandlung. Bei Vermietung: Umsatzsteueroptionen prüfen.""",
        "category": "EU-Recht"
    },
    {
        "title": "EU-Dienstleistungsrichtlinie: Grenzüberschreitende Immobiliendienstleistungen",
        "content": """Richtlinie 2006/123/EG ermöglicht freien Dienstleistungsverkehr. Makler, Verwalter, Gutachter können EU-weit tätig sein. Anerkennungsverfahren für Berufsqualifikationen. Herkunftslandprinzip vs. Bestimmungslandprinzip. Verbraucherschutzstandards des Tätigkeitslandes. Haftpflichtversicherung nachweisen. Sprache der Vertragsunterlagen beachten.""",
        "category": "EU-Recht"
    },
    {
        "title": "EU-Verbraucherrechte-Richtlinie: Widerrufsrecht bei Immobilienverträgen",
        "content": """Richtlinie 2011/83/EU: 14-tägiges Widerrufsrecht bei Fernabsatzverträgen. Bei Immobilienvermittlung außerhalb Geschäftsräume: Widerruf möglich. Ausnahme: Notarielle Beurkundung. Informationspflichten verstärkt. Muster-Widerrufsbelehrung verwenden. Grenzüberschreitende Verträge: Richtlinie anwendbar. Rechtswahl-Klauseln: Verbraucherschutz-Mindeststandard bleibt.""",
        "category": "EU-Recht"
    },
    {
        "title": "EU-Geldwäscherichtlinie: Immobilienkauf als Hochrisikobereich",
        "content": """5. Geldwäscherichtlinie (EU) 2018/843: Immobilienmakler als Verpflichtete. Sorgfaltspflichten bei Transaktionen über 10.000€. Wirtschaftlich Berechtigten identifizieren. Transparenzregister-Abfrage. Verdachtsmeldungen an FIU. Barzahlungsverbot über 10.000€. Dokumentationspflichten 5 Jahre. Sanktionen bei Verstoß erheblich. Notar führt ebenfalls GW-Prüfung durch.""",
        "category": "EU-Recht"
    },
    {
        "title": "EU-Energieeffizienzrichtlinie: Gebäudestandards europaweit",
        "content": """Richtlinie 2010/31/EU (EPBD): Energieausweis bei Verkauf/Vermietung Pflicht. Nearly Zero-Energy Buildings (NZEB) ab 2021 Standard. Gesamtenergieeffizienz-Berechnung harmonisiert. Sanierungsempfehlungen im Energieausweis. Smart Readiness Indicator eingeführt. Elektromobilität-Infrastruktur vorgeschrieben. Grenzwerte für CO₂-Emissionen. Gebäudeautomation bei größeren Gebäuden.""",
        "category": "EU-Recht"
    },
    
    # Grenzüberschreitende Transaktionen
    {
        "title": "Auslandsimmobilie Spanien: Kaufprozess und Besonderheiten",
        "content": """NIE-Nummer (Número de Identificación de Extranjeros) erforderlich. Reservierungsvertrag mit Anzahlung üblich. Notartermin: Escritura Pública. Grundbucheintrag: Registro de la Propiedad. IBI (Grundsteuer) und Müllgebühren jährlich. Gemeinschaftskosten bei Apartmentanlagen. Plusvalía-Steuer bei Verkauf. Non-Resident-Status: 3% Quellensteuer. Rechtswahl möglich, aber spanisches Sachenrecht gilt.""",
        "category": "Internationales"
    },
    {
        "title": "Auslandsimmobilie Frankreich: Notaire und französisches Kaufrecht",
        "content": """Notaire hat zentrale Rolle (staatlich bestellt). Compromis de vente: Vorvertrag mit 7-10 Tagen Widerrufsrecht. Acte de vente: notarielle Kaufurkunde. Hypothek: Hypothèque eingetragen. Taxe foncière (Grundsteuer) vom Eigentümer. Taxe d'habitation für Bewohner. Vorkaufsrecht Gemeinde beachten. DPE (Energieausweis) verpflichtend. Assainissement (Abwasser) prüfen.""",
        "category": "Internationales"
    },
    {
        "title": "Auslandsimmobilie Italien: Rogito und Registro",
        "content": """Codice Fiscale (Steuernummer) notwendig. Compromesso (Vorvertrag) mit Anzahlung. Rogito Notarile (notarielle Kaufurkunde). Registro (Grundbuch) beim Katasteramt. IMU (Gemeindesteuer) jährlich. TARI (Müllsteuer). Condominio-Kosten bei Eigentumswohnungen. Geometra für technische Prüfungen. Certificazione energetica erforderlich. Rechtswahl: Italienisches Sachenrecht maßgeblich.""",
        "category": "Internationales"
    },
    {
        "title": "Auslandsimmobilie Portugal: Escritura und IMI",
        "content": """NIF (Número de Identificação Fiscal) beantragen. Promessa de Compra e Venda (Vorvertrag). CPCV mit Anzahlung 10-30%. Escritura Pública vor Notar. Conservatória do Registo Predial (Grundbuch). IMI (Imposto Municipal sobre Imóveis) jährlich. IMT (Grunderwerbsteuer) gestaffelt. Energieausweis (Certificado Energético). Golden Visa bei Investition über 500.000€ möglich.""",
        "category": "Internationales"
    },
    {
        "title": "Auslandsimmobilie Österreich: Grundverkehrsgesetz und Genehmigungen",
        "content": """Grundverkehrsgesetze der Bundesländer beachten. Genehmigungspflicht für Ausländer in manchen Regionen. Notarielle Beurkundung nicht immer zwingend. Grundbuch: Eintragung beim Bezirksgericht. Grunderwerbsteuer 3,5% (0,5% mit Selbstberechnung). Eintragungsgebühr 1,1%. Immobilienertragsteuer (ImmoESt) 30% bei Verkauf. Wohnungseigentumsgesetz (WEG) ähnlich deutschem Recht.""",
        "category": "Internationales"
    },
    {
        "title": "Schweiz Immobilienerwerb: Lex Koller und Bewilligungspflicht",
        "content": """Bundesgesetz über Erwerb von Grundstücken durch Ausländer (BewG - 'Lex Koller'). Bewilligungspflicht für Nicht-Schweizer. Ausnahmen: Erstwohnsitz EU/EFTA-Bürger in bestimmten Kantonen. Ferienwohnungen: Kontingente pro Gemeinde. Handänderungssteuer kantonalunterschiedlich. Grundbucheintrag beim Grundbuchamt. Notarkosten und Grundbuchgebühren. Quellensteuer auf Mietertrag für Ausländer.""",
        "category": "Internationales"
    },
    {
        "title": "USA Immobilienkauf: Title Insurance und Closing",
        "content": """Title Search: Eigentumshistorie prüfen. Title Insurance gegen Altlasten. Purchase Agreement (Kaufvertrag). Escrow Account: Treuhandkonto. Home Inspection empfohlen. Closing: Vertragsabschluss mit allen Parteien. Deed (Eigentumsurkunde) wird übertragen. Recording beim County Recorder. Property Tax jährlich. HOA Fees bei Eigentümergemeinschaften. FIRPTA: Quellensteuer für Ausländer beim Verkauf.""",
        "category": "Internationales"
    },
    
    # Steuerliche Aspekte International
    {
        "title": "Doppelbesteuerungsabkommen (DBA): Immobilien im Ausland",
        "content": """DBA verhindern Doppelbesteuerung. Belegenheitsprinzip: Besteuerung am Immobilienstandort. Deutschland behält Progressionsvorbehalt. Einkünfte aus Vermietung: Im Belegenheitsstaat steuerpflichtig. Veräußerungsgewinn: Meist im Belegenheitsstaat. Erbschaft-/Schenkungsteuer: Länderspezifische DBA. Anrechnungsmethode vs. Freistellungsmethode. Steuererklärung in beiden Ländern abgeben.""",
        "category": "Steuerrecht International"
    },
    {
        "title": "Ausländische Mieteinnahmen: Steuerpflicht in Deutschland",
        "content": """Unbeschränkte Steuerpflicht bei Wohnsitz Deutschland. Welteinkommensprinzip: Alle Einkünfte erfassen. Ausländische Mieteinnahmen in Anlage V. Werbungskosten: AfA, Instandhaltung, Verwaltung, Reisekosten. Quellensteuer im Ausland anrechenbar. DBA beachten. Progressionsvorbehalt erhöht Steuersatz. Steuerberater mit Auslandserfahrung konsultieren.""",
        "category": "Steuerrecht International"
    },
    {
        "title": "Grunderwerbsteuer international: Unterschiedliche Systeme",
        "content": """Deutschland: 3,5-6,5% je Bundesland. Spanien: 6-10% ITP oder 10% IVA+AJD (Neubau). Frankreich: ~7-8% (inkl. Notarkosten). Italien: 2-9% (Erstimmobilie günstiger). Portugal: 0-8% IMT gestaffelt. Österreich: 3,5% + Gebühren. Schweiz: Kantonal unterschiedlich 1-3%. UK: Stamp Duty 0-12% gestaffelt. USA: Je State unterschiedlich, oft Transfer Tax.""",
        "category": "Steuerrecht International"
    },
    {
        "title": "Erbschaftsteuer Auslandsimmobilie: Deutsches vs. ausländisches Recht",
        "content": """Bei Wohnsitz Deutschland: Welterbschaftsteuer. Auslandsimmobilie unterliegt deutschem ErbStG. Belegenheitsstaat kann ebenfalls besteuern. DBA-Erbschaftsteuer prüfen (nicht mit allen Ländern). Anrechnung ausländischer Steuer möglich. Freibeträge gelten für Gesamtvermögen. Bewertung: Verkehrswert im Ausland ermitteln. Nachlassverfahren im Belegenheitsstaat durchführen.""",
        "category": "Steuerrecht International"
    },
    {
        "title": "Wegzugsbesteuerung: Immobilienvermögen bei Auswanderung",
        "content": """§ 6 AStG: Wegzugsbesteuerung bei wesentlicher Beteiligung. Immobilien als Privatvermögen: Keine Wegzugsteuer. Immobilien im Betriebsvermögen: Entstrickung möglich. Wechsel in Niedrigsteuerland: Besondere Prüfung. Aufschub der Wegzugsteuer in EU-Staaten. Rückkehr-Option innerhalb 7 Jahren. Meldepflichten an Finanzamt. Private Vermietung nicht betroffen.""",
        "category": "Steuerrecht International"
    },
    
    # Internationales Vertragsrecht
    {
        "title": "Haager Übereinkommen: Rechtswahl bei Immobilienkaufverträgen",
        "content": """Rom I-VO (593/2008): Vertragsrecht bei internationalem Kaufvertrag. Rechtswahl durch Parteien möglich. Ohne Rechtswahl: Recht des Verkäufers-Wohnsitzes. Sachenrecht: Immer lex rei sitae (Belegenheitsrecht). Formvorschriften des Belegenheitsstaates beachten. Verbraucherschutz-Mindeststandard gilt. Schriftform und Beurkundung nach localem Recht.""",
        "category": "Internationales Vertragsrecht"
    },
    {
        "title": "Internationale Gerichtszuständigkeit: Immobilienstreitigkeiten",
        "content": """EuGVVO (1215/2012): Zuständigkeit bei grenzüberschreitenden Streitigkeiten. Ausschließliche Zuständigkeit: Gerichte am Belegenheitsort (Art. 24 EuGVVO). Mietstreitigkeiten: Wahlrecht für Mieter (Wohnsitz oder Belegenheit). Prorogation (Gerichtsstandsvereinbarung) unwirksam bei dinglichen Rechten. Vollstreckung: EU-weit vereinfachtes Verfahren. Drittstaaten: Internationale Abkommen oder nationale Regeln.""",
        "category": "Internationales Vertragsrecht"
    },
    {
        "title": "EU-Erbrechtsverordnung (EuErbVO): Immobilien im Nachlass",
        "content": """Verordnung 650/2012: Einheitliches Erbrecht ab 2015. Letzter gewöhnlicher Aufenthalt bestimmt Erbrecht. Rechtswahl zugunsten Heimatrechts möglich. Europäisches Nachlasszeugnis (ENZ) vereinfacht Verfahren. Immobilien: Sachenrecht bleibt Belegenheitsrecht. Registerverfahren im Belegenheitsstaat erforderlich. Pflichtteilsrechte: Nach gewähltem Erbrecht. UK, Irland, Dänemark: Nicht anwendbar.""",
        "category": "Internationales Erbrecht"
    },
    {
        "title": "Apostille: Beglaubigung für Auslandsdokumente",
        "content": """Haager Übereinkommen von 1961: Apostille ersetzt Legalisation. Öffentliche Urkunden (Geburtsurkunden, Vollmachten, notarielle Dokumente). Apostille durch zuständige Behörde (meist Landgericht). Für Nicht-Haager-Staaten: Konsularische Legalisation. Übersetzungen: Vereidigte Übersetzer nutzen. Immobilienkauf im Ausland: Vollmacht mit Apostille. Gültigkeit unbegrenzt.""",
        "category": "Internationales Recht"
    },
    {
        "title": "Internationale Vollmacht: Immobilien im Ausland verwalten",
        "content": """Notarielle Vollmacht für Immobiliengeschäfte empfohlen. Apostille oder Legalisation erforderlich. Übersetzung in Landessprache durch vereidigten Übersetzer. Spezialbevollmächtigung für Kaufvertrag sicherer. Generalvollmacht: Umfassende Regelung, Missbrauchsrisiko. Widerrufbarkeit regeln. Registrierung im Ausland teilweise nötig. Haftung des Vollmachtgebers für Bevollmächtigten.""",
        "category": "Internationales Recht"
    },
    
    # Währung und Finanzierung International
    {
        "title": "Währungsrisiko Auslandsimmobilie: Absicherungsstrategien",
        "content": """Fremdwährungsrisiko bei Nicht-Euro-Immobilien. Wertschwankungen beeinflussen Rendite. Natürliches Hedging: Mieteinnahmen in Landeswährung. Währungsswaps und Forwards zur Absicherung. Fremdwährungskredit: Niedrigzins vs. Wechselkursrisiko. CHF-Kredite: Historische Risiken beachten. Diversifikation über mehrere Währungen. Regelmäßige Umschichtung erwägen.""",
        "category": "Finanzierung International"
    },
    {
        "title": "Auslandsfinanzierung: Kredit im Belegenheitsstaat vs. Deutschland",
        "content": """Lokale Finanzierung: Kenntnis des Marktes, lokale Konditionen. Deutsche Bank: Höhere Sicherheitsanforderungen im Ausland. Beleihungswert: Oft niedriger bei Auslandsimmobilien. Zinsen: Marktabhängig, teilweise günstiger im Ausland. Währungsrisiko bei Fremdwährungskredit. Vorfälligkeitsentschädigung: Länderunterschiede. Tilgungsmodalitäten flexibler im Ausland möglich. Grundschuld vs. Hypothek je nach Land.""",
        "category": "Finanzierung International"
    },
    {
        "title": "FATCA und CRS: Meldepflichten bei Auslandsimmobilien",
        "content": """FATCA (Foreign Account Tax Compliance Act): US-Personen. CRS (Common Reporting Standard): Automatischer Informationsaustausch. Banken melden Konten an Finanzbehörden. Immobilieneigentum selbst nicht meldepflichtig. Aber: Mieteinnahmen-Konten werden gemeldet. Steuerhinterziehung zunehmend schwierig. Transparenzregister in vielen Ländern. Selbstanzeige bei Altfällen prüfen.""",
        "category": "Steuerrecht International"
    },
    {
        "title": "Offshore-Strukturen: Immobilien in Gesellschaften",
        "content": """Holdinggesellschaften im Ausland für Immobilienbesitz. Gründe: Vermögensschutz, Anonymität, Steuern. Länderwahl: Malta, Zypern, Luxemburg (EU). Transparenzregister: Wirtschaftlich Berechtigte melden. Deutschland: § 1 AStG Hinzurechnungsbesteuerung. Niedrigbesteuerung unter 25%: Einkünfte zugerechnet. Gestaltungsmissbrauch: § 42 AO. Compliance-Risiken hoch. Rechtliche Beratung zwingend.""",
        "category": "Internationales Steuerrecht"
    },
    {
        "title": "Trust-Strukturen: Anglo-amerikanisches Immobilieneigentum",
        "content": """Trust: Treuhänderische Vermögensverwaltung (Common Law). Settlor (Stifter) überträgt Eigentum an Trustee. Beneficiaries (Begünstigte) profitieren. Immobilien in Trust: Vermögensschutz, Erbplanung. Deutsches Recht: Trust steuerlich komplex. Transparenzprinzip vs. Intransparenz. Erbschaftsteuer: Trust als Schenkung. Anerkennung in Deutschland begrenzt.""",
        "category": "Internationales Recht"
    },
    
    # Spezielle Länder und Regionen
    {
        "title": "Brexit-Auswirkungen: Immobilien in Großbritannien",
        "content": """UK kein EU-Mitglied mehr seit 2020. Niederlassungsfreiheit entfallen. Visa-Regelungen für längere Aufenthalte. Immobilienerwerb weiterhin ohne Einschränkungen. Steuerliche DBA mit UK besteht. Stamp Duty: 0-12% gestaffelt. Council Tax jährlich. Leashold vs. Freehold beachten. Mieteinnahmen: UK-Steuerpflicht, Anrechnung in Deutschland. Buy-to-let Hypotheken verfügbar.""",
        "category": "Internationales"
    },
    {
        "title": "Dubai Immobilien: Freehold für Ausländer",
        "content": """Freehold-Gebiete: Ausländer können Eigentum erwerben. Dubai Land Department: Registrierung. Oqood: Vorvertrag. Title Deed: Eigentumsurkunde. Keine Grundsteuer, keine Einkommensteuer auf Mieteinnahmen. Service Charges für Gemeinschaftsanlagen. Kühlungskosten (Chiller) oft separat. Maklergebühr: 2% vom Käufer, 2% vom Verkäufer. DLD Fee: 4% bei Registrierung. Residency Visa bei Immobilienwert über AED 750.000 möglich.""",
        "category": "Internationales"
    },
    {
        "title": "Türkei Immobilien: Tapu und Ausländerrechte",
        "content": """Tapu: Grundbuchamt. Ausländer können Eigentum erwerben (Reziprozität). Beschränkungen in militärischen Sperrgebieten. Iskan (Nutzungserlaubnis) für Neubau prüfen. Satış Vaadi Sözleşmesi: Vorvertrag. Tapu Senedi: Eigentumsurkunde. Emlak Vergisi: Grundsteuer 0,1-0,6%. MTV: Umweltsteuer. KDV (Mehrwertsteuer) bei Neubau 18%. Ausländer: Aufenthaltserlaubnis bei Immobilienkauf erleichtert.""",
        "category": "Internationales"
    },
    {
        "title": "Griechenland Immobilien: Krise und Chancen",
        "content": """Golden Visa: Aufenthaltserlaubnis bei Kauf über 250.000€ (ab 2023: 500.000€ in Athen/Thessaloniki). Notarielle Beurkundung erforderlich. AFM (Steuernummer) beantragen. Hypotheken-Eintragung beim Hypothekenamt. ENFIA (Grundsteuer) jährlich. Übertragungssteuer 3% (Neubau: MwSt 24%). Anwalt prüft Eigentumsverhältnisse. Inseln: Besondere Regelungen möglich.""",
        "category": "Internationales"
    },
    {
        "title": "Kroatien Immobilien: EU-Beitritt und Immobilienmarkt",
        "content": """EU-Mitglied seit 2013. EU-Bürger: Freier Immobilienerwerb. Grundbuch (Zemljišna knjiga) beim Katasteramt. Notarielle Beurkundung nicht zwingend, aber üblich. Porez na promet nekretnina: Grunderwerbsteuer 3%. Porez na nekretnine: Grundsteuer 3-15‰. Küstengebiete: Bauvorschriften streng. Touristische Vermietung: Lizenzen erforderlich. Euro-Einführung 2023 erleichtert Transaktionen.""",
        "category": "Internationales"
    },
    {
        "title": "Polen Immobilien: Notariusz und Księga Wieczysta",
        "content": """EU-Bürger: Keine Genehmigung erforderlich. Akt notarialny: Notarielle Urkunde zwingend. Księga Wieczysta: Grundbuch. Podatek od nieruchomości: Grundsteuer von Gemeinde. PCC: Stempelsteuer 2% (PIT 19% bei gewerblich). Czynsz: Miete. VAT 23% bei Neubau. Mieszkanie: Eigentumswohnung. DOM: Haus. Działka: Grundstück. Stabile Rechtslage, wachsender Markt.""",
        "category": "Internationales"
    },
    {
        "title": "Zypern Immobilien: Title Deed Problematik",
        "content": """EU-Mitglied, englisches Rechtssystem. Title Deed (Eigentumsnachweis) oft verzögert. Contract of Sale: Kaufvertrag beim District Land Office registrieren. Interim Agreement bis Title Deed. Immovable Property Tax abgeschafft 2017. Grunderwerbsteuer 3-8%. Kapitalertragsteuer 20% bei Verkauf. Non-Dom-Status: Steuervorteile. Zypern-Passport-Programm eingestellt 2020. Rechtsunsicherheit bei älteren Objekten.""",
        "category": "Internationales"
    },
    {
        "title": "Malta Immobilien: Permits und Ausländerrechte",
        "content": """EU-Bürger: Erstwohnsitz frei erwerbbar. Zweitwohnsitz: Acquisition of Immovable Property (AIP) Permit. Final Deed: Notarielle Kaufurkunde. Public Registry: Grundbuch. Stamp Duty: 5% (reduziert auf 1,5% für Erstwohnsitz). Notarkosten ~1%. Property Transfer Tax bei Verkauf. Malta Permanent Residence Programme (MPRP) für Nicht-EU-Bürger. Englischsprachiges Rechtssystem, EU-Recht anwendbar.""",
        "category": "Internationales"
    },
    {
        "title": "Thailand Immobilien: Condominium Foreign Quota",
        "content": """Ausländer können Condominiums erwerben (max. 49% Ausländeranteil pro Gebäude). Land nicht erwerbbar (nur Leasehold 30+30+30 Jahre). Chanote: Vollwertiges Grundbuch. Nor Sor 3 Gor: Landtitel. Transfer Fee: 2%. Stamp Duty: 0,5%. Withholding Tax: 1%. Business Tax wenn <5 Jahre Eigentum. Thailändisches Bankkonto: Geldtransfer dokumentieren. Rechtssystem: Civil Law, aber lokale Besonderheiten.""",
        "category": "Internationales"
    },
    {
        "title": "Mexiko Immobilien: Fideicomiso in Küstennähe",
        "content": """Restricted Zone: 50km Küste, 100km Grenze. Fideicomiso (Bank-Trust) für Ausländer erforderlich. Trust-Laufzeit: 50 Jahre verlängerbar. Escritura Pública: Notarielle Urkunde. RFC (Steuernummer) beantragen. Predial: Grundsteuer von Gemeinde. Notarkosten ~4-6%. Closing Costs total ~8-10%. Capital Gains Tax bei Verkauf bis 35%. Permanent Residency bei Immobilieninvestition erleichtert.""",
        "category": "Internationales"
    },
    
    # Praktische Aspekte
    {
        "title": "Hausverwaltung im Ausland: Professionelle Betreuung",
        "content": """Property Management unerlässlich bei Auslandsimmobilie. Leistungen: Mietersuche, Mieteinzug, Instandhaltung, Kommunikation mit Behörden. Kosten: 8-15% der Mieteinnahmen. Vertrag: Leistungsumfang genau definieren. Reporting: Regelmäßige Berichte über Zustand und Finanzen. Sprache: Lokale Manager kennen Markt und Recht. Haftung bei Pflichtverletzung. Vertrauen essentiell: Referenzen prüfen.""",
        "category": "Hausverwaltung"
    },
    {
        "title": "Internationale Mietverträge: Rechtswahl und Währung",
        "content": """Rechtswahl: Grundsätzlich möglich, aber Verbraucherschutz-Mindeststandard. Vermieter bevorzugt Belegenheitsrecht. Währung: Mieteinnahmen in Landeswährung üblich. Euro-Klausel: Umrechnung zu festem Kurs? Indexierung: Inflation ausgleichen. Kündigungsfristen: Nach lokalem Recht. Nebenkosten: Umlageschlüssel transparent. Kaution: Höhe nach Landesrecht (z.B. Frankreich max. 1 Monatsmiete).""",
        "category": "Mietrecht International"
    },
    {
        "title": "Sprachbarrieren: Übersetzer und Rechtsberatung",
        "content": """Verträge in Landessprache: Vereidigte Übersetzung nutzen. Anwalt vor Ort: Kenntnisse des lokalen Rechts. Deutscher Anwalt mit Auslandserfahrung zusätzlich. Notar: In vielen Ländern neutral, in manchen nur Beurkundungsfunktion. Dolmetscher bei Terminen sinnvoll. Missverständnisse vermeiden: Schriftform bevorzugen. Kosten: Einkalkulieren für Übersetzungen und Beratung. Vertragssprache: Englisch als Kompromiss möglich.""",
        "category": "Internationales"
    },
    {
        "title": "Kulturelle Unterschiede: Verhandlungen im Ausland",
        "content": """Verhandlungsstil: Direktheit vs. Indirektheit kulturabhängig. Zeitverständnis: Pünktlichkeit unterschiedlich gewertet. Hierarchien: Entscheidungswege beachten. Vertragsauffassung: Detailtiefe vs. Rahmenvereinbarung. Geschenke und Einladungen: Gepflogenheiten respektieren. Geduld: Prozesse dauern oft länger als in Deutschland. Beziehungsaufbau: In manchen Kulturen vor Geschäft. Lokale Experten einbeziehen.""",
        "category": "Internationales"
    },
    {
        "title": "Risikomanagement Auslandsimmobilie: Diversifikation und Absicherung",
        "content": """Diversifikation: Nicht alles auf eine Karte setzen. Länderrisiko: Politische Stabilität, Rechtssicherheit bewerten. Währungsrisiko: Hedging-Strategien. Vermietungsrisiko: Leerstand kalkulieren. Versicherungen: Gebäude-, Haftpflicht-, Mietausfall-Versicherung. Liquiditätsreserve: Für unvorhergesehene Kosten. Exit-Strategie: Verkäuflichkeit prüfen. Regelmäßige Überprüfung der Investition.""",
        "category": "Investition"
    },
    {
        "title": "EU-Binnenmarkt: Chancen für Immobilieninvestoren",
        "content": """Freier Kapital- und Personenverkehr. Harmonisierte Standards (EPBD, Verbraucherschutz). Wegfall Wechselkursrisiko in Euro-Zone. Diverse Märkte: Von Hochpreis (München) bis günstig (Bulgarien). Renditeunterschiede nutzen. Demografische Entwicklungen unterschiedlich. EU-Fördermittel für Sanierungen. Rechtssicherheit durch EU-Recht. Risiken: Regionale Immobilienblasen.""",
        "category": "Investition"
    },
    {
        "title": "Nicht-EU-Länder: Zusätzliche Herausforderungen",
        "content": """Visapflicht und Aufenthaltsgenehmigungen. Kapitalverkehrskontrollen möglich. Grundbuchsysteme weniger transparent. Korruptionsrisiko in manchen Ländern. Politische Risiken: Enteignung, Währungskrise. Rechtssystem: Ungewohnte Strukturen. Sprachbarrieren stärker. Aber: Höhere Renditen möglich. Golden Visa Programme nutzen. Sorgfältige Due Diligence essentiell.""",
        "category": "Internationales"
    },
    {
        "title": "Immobilien-Crowdinvesting International: Chancen und Risiken",
        "content": """Plattformen ermöglichen Teilinvestitionen im Ausland. Geringe Einstiegssummen (ab 500€). Diversifikation über viele Projekte. Transparenz: Projektinformationen online. Risiken: Totalverlust möglich, keine Einlagensicherung. Rendite: 4-8% p.a. angestrebt. Laufzeiten: Meist 12-48 Monate. Regulierung: Je nach Plattform-Sitz. Steuern: Kapitalertragsteuer in Deutschland. Plattformen: Exporo, Bergfürst (mit Auslandsprojekten).""",
        "category": "Investition"
    },
    {
        "title": "REITs International: Immobilienaktien weltweit",
        "content": """Real Estate Investment Trusts (REITs): Börsennotierte Immobilien-AGs. Diversifikation über viele Objekte und Länder. Liquidität: Börsentäglich handelbar. Dividendenpflicht: 90% Gewinnausschüttung (USA). Steuer: Transparenzprinzip, Dividenden voll steuerpflichtig. Deutsche REITs (G-REITs): Begrenzte Anzahl. US-REITs: Größter Markt. Sektor-Spezialisierung: Office, Retail, Industrial, Residential. Risiken: Kursschwankungen, Zinsänderungen.""",
        "category": "Investition"
    },
    {
        "title": "Internationale Immobilienmessen: Networking und Marktüberblick",
        "content": """MIPIM Cannes: Größte Immobilienmesse weltweit. Expo Real München: Fokus Europa. Immobilienscout24-Partnertag. Internationale Netzwerke knüpfen. Markttrends erkennen. Produktneuheiten (PropTech). Vorträge und Panels zu Rechtsfragen. Kontakte zu Entwicklern, Investoren, Dienstleistern. Kosten: Eintrittskarten, Reise, Unterkunft. Vorbereitung: Termine im Voraus vereinbaren.""",
        "category": "Internationales"
    },
    
    # Weitere spezielle Themen
    {
        "title": "Internationale Schiedsgerichtsbarkeit: Immobilienstreitigkeiten",
        "content": """Schiedsklausel im Kaufvertrag: Alternative zu staatlichen Gerichten. ICC (International Chamber of Commerce), LCIA, DIS. Vorteile: Neutralität, Vertraulichkeit, Schnelligkeit. Nachteile: Kosten, begrenzte Rechtsmittel. New York Convention: Anerkennung von Schiedssprüchen weltweit. Immobiliensachen: Beschränkungen bei dinglichen Rechten. Mediationsklausel: Vorgeschaltete Streitbeilegung. Rechtsanwaltskosten höher als bei staatlichen Gerichten.""",
        "category": "Internationales Recht"
    },
    {
        "title": "EU-Transparenzrichtlinie: Beneficial Ownership von Immobilien",
        "content": """5. Geldwäscherichtlinie: Transparenzregister für wirtschaftlich Berechtigte. Immobiliengesellschaften: Eintragungspflicht. Angaben: Name, Geburtsdatum, Wohnsitz, Art der Beteiligung. Öffentlicher Zugang zu bestimmten Informationen. Sanktionen bei Nichtmeldung. Ziel: Bekämpfung von Geldwäsche und Terrorismusfinanzierung. Kritik: Datenschutz vs. Transparenz. EuGH-Urteile beachten. Nationale Umsetzung unterschiedlich.""",
        "category": "EU-Recht"
    },
    {
        "title": "GDPR (DSGVO) und Immobilien: Datenschutz bei internationalen Transaktionen",
        "content": """Verordnung 2016/679 (DSGVO): Gilt in gesamter EU. Personenbezogene Daten bei Immobilientransaktionen: Name, Adresse, Bonitätsdaten. Einwilligung oder berechtigtes Interesse erforderlich. Datensparsamkeit und Zweckbindung. Weitergabe an Drittländer: Angemessenheitsbeschluss oder Standardvertragsklauseln. Makler, Verwalter: Auftragsverarbeitungsvertrag. Betroffenenrechte: Auskunft, Löschung. Bußgelder bis 20 Mio. € oder 4% Jahresumsatz.""",
        "category": "EU-Recht"
    },
    {
        "title": "Internationale Grundpfandrechte: Hypothek vs. Grundschuld",
        "content": """Deutschland: Grundschuld (abstrakt). Viele Länder: Hypothek (akzessorisch). Spanien: Hipoteca. Frankreich: Hypothèque. Italien: Ipoteca. UK: Mortgage. USA: Mortgage (Foreclosure). Rangfolge im Grundbuch. Löschung nach Tilgung. Kosten der Eintragung länderspezifisch. Vollstreckung: Verfahren unterschiedlich. Internationale Kredite: Mehrere Grundpfandrechte möglich.""",
        "category": "Internationales Sachenrecht"
    },
    {
        "title": "Vorkaufsrecht kommunal: Internationale Vergleiche",
        "content": """Deutschland: § 24 ff. BauGB – Vorkaufsrecht der Gemeinde. Frankreich: Droit de préemption urbain. Spanien: Derecho de tanteo y retracto. Italien: Prelazione. Zweck: Stadtplanung, soziale Wohnungspolitik. Frist zur Ausübung: Meist 2-3 Monate. Preis: Kaufpreis des Vertrages. Nichtausübung: Vertrag wird wirksam. Rechtssicherheit: Negativattest einholen.""",
        "category": "Baurecht International"
    },
    {
        "title": "Servituten international: Dienstbarkeiten im Vergleich",
        "content": """Deutschland: Grunddienstbarkeit (§ 1018 BGB). Common Law: Easement. Frankreich: Servitude. Italien: Servitù. Spanien: Servidumbre. Arten: Wegerecht, Leitungsrecht, Überbau. Eintragung im Grundbuch. Löschung: Vereinbarung oder Verjährung. Streitigkeiten: Oft zwischen Nachbarn. Bewertung: Minderung Verkehrswert.""",
        "category": "Internationales Sachenrecht"
    },
    {
        "title": "Internationale Immobilien-Due-Diligence: Checkliste",
        "content": """1. Legal: Eigentumsnachweis, Grundbuch, Lasten. 2. Tax: Lokale Steuern, DBA-Prüfung. 3. Technical: Zustand, Baumängel, Gutachten. 4. Financial: Cashflow, Finanzierung, Rendite. 5. Environmental: Altlasten, Umweltauflagen. 6. Regulatory: Baugenehmigungen, Nutzungsänderungen. 7. Commercial: Mietverträge, Mieterstruktur. 8. Insurance: Versicherungsdeckung. Experten einschalten: Anwalt, Steuerberater, Gutachter.""",
        "category": "Internationales"
    },
    {
        "title": "Exit-Strategien Auslandsimmobilie: Verkauf und Rückzug",
        "content": """Verkaufsplanung: Zeitpunkt und Marktlage beachten. Makler vor Ort: Kenntnis des lokalen Marktes. Preisfindung: Gutachten, Vergleichswerte. Steuern: Capital Gains Tax, Spekulationsfrist. Währungsrisiko beim Verkaufserlös. Rückführung des Kapitals: Banküberweisung dokumentieren. Kredit ablösen: Vorfälligkeitsentschädigung? Renovierung vor Verkauf: Kosten vs. Nutzen. Alternative: Vermietung langfristig, Verkauf später.""",
        "category": "Investition"
    },
    {
        "title": "Diplomatischer Schutz: Deutsche Staatsangehörige im Ausland",
        "content": """Bei Rechtsstreitigkeiten im Ausland: Botschaft kontaktieren. Konsularische Unterstützung: Anwaltslisten, Dolmetscher. Kein direktes Eingreifen in Verfahren. Haft: Konsularischer Beistand möglich. Rechtshilfeabkommen nutzen. Deutsche Auslandsvertretungen informieren. Reisewarnung bei instabilen Ländern beachten. Versicherungen: Rechtsschutz mit Auslandsschutz.""",
        "category": "Internationales"
    },
    {
        "title": "UN-Kaufrecht (CISG): Anwendbarkeit bei Immobilien?",
        "content": """UN-Kaufrecht (CISG): Für bewegliche Waren. Immobilien: Grundsätzlich ausgeschlossen (Art. 2 CISG). Aber: Bauträgerverträge teilweise erfasst. Rechtswahl: CISG kann abbedungen werden. Internationaler Kauf von Ausstattung: CISG anwendbar. Kollisionsrecht: Bei Immobilien Rom I-VO. Schiedsgerichtsbarkeit: CISG oft gewählt. Praktische Relevanz für Immobilien gering.""",
        "category": "Internationales Vertragsrecht"
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
    """Füge Batch 8 Dokumente hinzu"""
    print("🚀 BATCH 8: INTERNATIONALE ASPEKTE & EU-RECHT - START")
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
                    "source": "Batch 8 - Internationale Aspekte & EU-Recht"
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
    print("\n🔥 BATCH 8 COMPLETE! 🔥")

if __name__ == "__main__":
    seed_batch()
