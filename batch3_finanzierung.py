#!/usr/bin/env python3
"""Batch 3: Finanzierung & Steuern - 50 Dokumente"""

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
        "title": "Annuitätendarlehen: Funktionsweise",
        "content": """Annuitätendarlehen: Gleichbleibende Rate aus Zins und Tilgung. Beginn: Hoher Zinsanteil, niedriger Tilgungsanteil. Ende: Umgekehrt. Vorteil: Planungssicherheit. Zinsfestschreibung: 5, 10, 15, 20 Jahre. Sondertilgung: 5-10% p.a. kostenfrei. Tilgungssatz: Mind. 2% empfohlen (1% dauert 50+ Jahre). Wichtig: Auf Gesamtkosten achten!""",
        "category": "Finanzierung",
        "subcategory": "Darlehensarten"
    },
    {
        "title": "Volltilgerdarlehen: Besonderheiten",
        "content": """Volltilgerdarlehen: Komplett getilgt nach Zinsbindung. Laufzeit: Fest (z.B. 15 Jahre). Vorteil: Zinsrabatt (0,1-0,3%), keine Anschlussfinanzierung. Nachteil: Höhere Rate als Annuitätendarlehen. Flexibilität: Gering. Sondertilgung: Oft nicht nötig. Wichtig: Für sicherheitsorientierte Käufer!""",
        "category": "Finanzierung",
        "subcategory": "Darlehensarten"
    },
    {
        "title": "Forward-Darlehen: Zinsabsicherung",
        "content": """Forward-Darlehen: Zinskonditionen heute für Anschlussfinanzierung in 1-5 Jahren festlegen. Vorteil: Schutz vor Zinsanstieg. Nachteil: Forward-Aufschlag (0,01-0,03% pro Monat). Abschluss: Bis 66 Monate im Voraus. Wichtig: Bei niedrigen Zinsen absichern! Vergleich: Mehrere Banken anfragen.""",
        "category": "Finanzierung",
        "subcategory": "Anschlussfinanzierung"
    },
    {
        "title": "Bausparvertrag: Finanzierungsbaustein",
        "content": """Bausparvertrag: Sparen + günstiges Darlehen. Phase 1: Ansparphase (40-50% Bausparsumme). Phase 2: Zuteilung + Bauspardarlehen. Vorteil: Niedriger Darlehenszins (2-3%), Wohnungsbauprämie, Arbeitnehmersparzulage. Nachteil: Lange Ansparphase, Abschlussgebühr (1-1,6%). Kombifinanzierung: Mit Bankdarlehen kombinieren.""",
        "category": "Finanzierung",
        "subcategory": "Bausparvertrag"
    },
    {
        "title": "Eigenkapitalquote: Bedeutung",
        "content": """Eigenkapital empfohlen: 20-30% des Kaufpreises plus Nebenkosten. Minimum: 10-15% für gute Konditionen. Vollfinanzierung: Möglich aber teurer (Zinsaufschlag 0,5-1%). Berechnung: Kaufpreis + Nebenkosten (10-15%). Eigenkapital: Erspartes, Guthaben, Wertpapiere. Wichtig: Mehr Eigenkapital = bessere Zinsen!""",
        "category": "Finanzierung",
        "subcategory": "Eigenkapital"
    },
    {
        "title": "Zinsbindung: Laufzeiten",
        "content": """Zinsbindung: 5, 10, 15, 20, 30 Jahre. Kurze Zinsbindung (5 Jahre): Niedriger Zins, Risiko bei Anschlussfinanzierung. Lange Zinsbindung (15-20 Jahre): Höherer Zins, Sicherheit. Niedrigzinsphase: Lange Zinsbindung empfohlen. Hochzinsphase: Kurze Zinsbindung. Wichtig: Persönliche Risikobereitschaft beachten!""",
        "category": "Finanzierung",
        "subcategory": "Zinsbindung"
    },
    {
        "title": "Bereitstellungszinsen: Vermeidung",
        "content": """Bereitstellungszinsen: Wenn Darlehen nicht abgerufen wird (nach bereitstellungsfreier Zeit). Höhe: 0,15-0,25% pro Monat auf nicht abgerufene Summe. Bereitstellungsfreie Zeit: 3-12 Monate je nach Bank. Vermeidung: Passende Abrufzeit vereinbaren, bei Neubau längere Frist. Wichtig: Bei Bauträger rechtzeitig klären!""",
        "category": "Finanzierung",
        "subcategory": "Nebenkosten"
    },
    {
        "title": "Effektivzins vs. Sollzins",
        "content": """Sollzins: Reiner Darlehenszins. Effektivzins: Inkl. Nebenkosten (Bearbeitungsgebühr verboten seit 2014, aber Schätzkosten, Kontoführung). Vergleich: Immer Effektivzins nutzen! Unterschied: 0,1-0,3%. Wichtig: Gesamtkosten beachten, nicht nur Sollzins!""",
        "category": "Finanzierung",
        "subcategory": "Zinsen"
    },
    {
        "title": "Sondertilgung: Regelungen",
        "content": """Sondertilgung: Außerplanmäßige Tilgung. Üblich: 5-10% der Darlehenssumme pro Jahr kostenfrei. Vorteil: Schnellere Entschuldung, Zinsersparnis. Nachteil: Liquidität gebunden. Wichtig: Vertraglich vereinbaren! Nach 10 Jahren: Gesetzliches Sonderkündigungsrecht (§ 489 BGB).""",
        "category": "Finanzierung",
        "subcategory": "Tilgung"
    },
    {
        "title": "Schufa-Score: Bedeutung für Finanzierung",
        "content": """Schufa-Score: Bonität von 0-100%. Gut: >95%, Mittel: 90-95%, Schlecht: <90%. Einflussfaktoren: Zahlungsverhalten, Kreditnutzung, Anfragen. Verbesserung: Rechnungen pünktlich zahlen, Kredite reduzieren, falsche Einträge löschen. Finanzierung: Bei schlechtem Score höhere Zinsen oder Ablehnung. Selbstauskunft: 1x jährlich kostenlos.""",
        "category": "Finanzierung",
        "subcategory": "Bonität"
    },
    {
        "title": "Haushaltsrechnung: Ermittlung Budget",
        "content": """Haushaltsrechnung: Einnahmen minus Ausgaben = verfügbares Einkommen. Belastungsgrenze: Max. 40% Nettoeinkommen für Darlehensrate. Nebenkosten: 2-4€/m² pro Monat einkalkulieren. Puffer: 10% für Unvorhergesehenes. Wichtig: Realistisch rechnen, nicht zu knapp kalkulieren!""",
        "category": "Finanzierung",
        "subcategory": "Budgetplanung"
    },
    {
        "title": "Tilgungsplan: Verstehen",
        "content": """Tilgungsplan: Zeigt Verlauf der Rückzahlung über gesamte Laufzeit. Inhalt: Rate, Zinsanteil, Tilgungsanteil, Restschuld pro Jahr. Wichtig: Restschuld nach Zinsbindung zeigt Anschlussfinanzierungsbedarf. Berechnung: Online-Rechner nutzen. Vorteil: Transparenz über Gesamtkosten.""",
        "category": "Finanzierung",
        "subcategory": "Tilgung"
    },
    {
        "title": "AfA: Absetzung für Abnutzung",
        "content": """AfA (Abschreibung): Wertminderung Gebäude steuerlich absetzen. Neubau: 3% p.a. über 33 Jahre. Altbau (vor 1925): 2,5% p.a. über 40 Jahre. Altbau (nach 1925): 2% p.a. über 50 Jahre. Bemessungsgrundlage: Nur Gebäude, nicht Grund und Boden. Vermietung: Volle AfA absetzbar. Eigennutzung: Keine AfA.""",
        "category": "Steuerrecht",
        "subcategory": "AfA"
    },
    {
        "title": "Spekulationsfrist: 10-Jahres-Regel",
        "content": """Spekulationsfrist: Verkauf innerhalb 10 Jahren nach Kauf = steuerpflichtiger Gewinn. Ausnahme: Eigennutzung im Verkaufsjahr + 2 Vorjahren = steuerfrei. Vermietete Immobilie: Nach 10 Jahren steuerfrei verkaufbar. Berechnung: Verkaufspreis minus Anschaffungskosten minus Werbungskosten. Steuersatz: Persönlicher Einkommensteuersatz. Wichtig: Fristen beachten!""",
        "category": "Steuerrecht",
        "subcategory": "Spekulationssteuer"
    },
    {
        "title": "Werbungskosten: Vermietung",
        "content": """Werbungskosten bei Vermietung: Alle Kosten zur Erzielung von Mieteinnahmen. Beispiele: Darlehenszinsen, AfA, Instandhaltung, Verwaltung, Versicherungen, Grundsteuer, Fahrtkosten. Werbungskostenpauschale: Nicht bei Vermietung (nur tatsächliche Kosten). Verlust: Kann mit anderen Einkünften verrechnet werden. Wichtig: Alle Belege sammeln!""",
        "category": "Steuerrecht",
        "subcategory": "Werbungskosten"
    },
    {
        "title": "Eigenheimzulage: Abschaffung",
        "content": """Eigenheimzulage: Bis 2006 staatliche Förderung für selbstgenutztes Wohneigentum. Abschaffung: 2006. Ersatz: Wohnriester (für Altersvorsorge), KfW-Förderung (Energieeffizienz). Wichtig: Keine direkte Förderung mehr für Eigennutzer, nur indirekt über KfW!""",
        "category": "Steuerrecht",
        "subcategory": "Förderung"
    },
    {
        "title": "Wohnriester: Funktionsweise",
        "content": """Wohnriester: Riester-Rente für Immobilienfinanzierung. Förderung: Grundzulage 175€ p.a., Kinderzulage 300€, Steuerbonus bis 2.100€. Verwendung: Eigenkapital oder Tilgung. Wohn förderkonto: Rückzahlung im Alter (nachgelagerte Besteuerung). Wichtig: Nur für selbstgenutzte Immobilien! Verkauf: Förderung zurückzahlen.""",
        "category": "Steuerrecht",
        "subcategory": "Wohnriester"
    },
    {
        "title": "Grundsteuer: Berechnung",
        "content": """Grundsteuer: Jährliche Steuer auf Grundbesitz. Berechnung: Einheitswert x Grundsteuermesszahl x Hebesatz (Gemeinde). Reform 2025: Neues Bewertungsverfahren (Grundsteuerwert statt Einheitswert). Zahlung: Vierteljährlich. Umlage: Auf Mieter möglich. Höhe: Sehr unterschiedlich je nach Gemeinde (50-500€ pro Jahr). Wichtig: Steigt oft mit Grundstückspreisen!""",
        "category": "Steuerrecht",
        "subcategory": "Grundsteuer"
    },
    {
        "title": "Handwerkerleistungen: Steuerbonus",
        "content": """Handwerkerleistungen steuerlich absetzbar: 20% der Arbeitskosten (max. 1.200€ Steuerermäßigung pro Jahr). Voraussetzung: Rechnung, Überweisung, selbstgenutzte Immobilie. Absetzbar: Renovierung, Modernisierung, Wartung. Nicht absetzbar: Materialkosten, Neubau. Wichtig: Auch für Mieter! Zusammen mit Haushaltshilfe max. 5.200€.""",
        "category": "Steuerrecht",
        "subcategory": "Steuerbonus"
    },
    {
        "title": "Denkmal-AfA: Erhöhte Abschreibung",
        "content": """Denkmal-AfA: Erhöhte Abschreibung bei Sanierung denkmalgeschützter Immobilien. Eigennutzung: 9% über 10 Jahre (Sanierungskosten). Vermietung: 9% über 8 Jahre, dann 7% über 4 Jahre. Voraussetzung: Bescheinigung Denkmalschutzbehörde. Kombination: Mit normaler AfA möglich. Vorteil: Hohe Steuerersparnis! Nachteil: Auflagen bei Sanierung.""",
        "category": "Steuerrecht",
        "subcategory": "Denkmal-AfA"
    },
    {
        "title": "Umzugskosten: Steuerliche Absetzbarkeit",
        "content": """Umzugskosten absetzbar bei beruflichem Umzug. Werbungskosten: Transport, Makler (Mietwohnung), doppelte Miete, Reisekosten. Pauschale: Ledige 886€, Verheiratete 1.773€ (2023). Eigennutzer: Keine Absetzbarkeit bei privatem Umzug. Arbeitgeber: Steuerfreier Ersatz möglich. Wichtig: Berufliche Veranlassung nachweisen!""",
        "category": "Steuerrecht",
        "subcategory": "Werbungskosten"
    },
    {
        "title": "Vermietung an Angehörige: Steuerliche Anerkennung",
        "content": """Vermietung an Angehörige steuerlich anerkannt bei mindestens 66% (ab 2021: 50%) der ortsüblichen Miete. Unter 66%: Anteilige Kürzung der Werbungskosten. Unter 50%: Keine steuerliche Anerkennung. Wichtig: Mietvertrag schriftlich, marktüblich gestalten, Miete überweisen!""",
        "category": "Steuerrecht",
        "subcategory": "Vermietung"
    },
    {
        "title": "Eigennutzung: Steuerliche Nachteile",
        "content": """Eigennutzung steuerlich nicht absetzbar: Keine AfA, keine Werbungskosten, keine Darlehenszinsen. Vorteil: Mietfreies Wohnen. Handwerkerbonus: 20% der Arbeitskosten (max. 1.200€ Ersparnis). Verkauf: Steuerfrei (keine Spekulationssteuer bei Eigennutzung). Wichtig: Vermietung ist steuerlich attraktiver!""",
        "category": "Steuerrecht",
        "subcategory": "Eigennutzung"
    },
    {
        "title": "Betriebsvermögen: Immobilie im Unternehmen",
        "content": """Immobilie im Betriebsvermögen: Für Gewerbetreibende/Freiberufler möglich. Vorteil: AfA, Zinsen, alle Kosten als Betriebsausgaben absetzbar. Nachteil: Bei Verkauf Gewerbesteuer, keine 10-Jahres-Frist. Entnahme: Wird als Ertrag versteuert. Wichtig: Nur bei langfristiger Nutzung sinnvoll!""",
        "category": "Steuerrecht",
        "subcategory": "Betriebsvermögen"
    },
    {
        "title": "Erbschaftsteuer: Immobilien",
        "content": """Erbschaftsteuer: Bei Immobilienübertragung durch Erbschaft/Schenkung. Freibeträge: Ehepartner 500.000€, Kinder 400.000€ pro Person alle 10 Jahre. Bewertung: Verkehrswert (90% bei Vermietung). Familienheim: Steuerfrei bei Eigennutzung (10 Jahre Bindung). Nießbrauch: Mindert Wert. Wichtig: Frühzeitig planen!""",
        "category": "Steuerrecht",
        "subcategory": "Erbschaftsteuer"
    },
    {
        "title": "Schenkung zu Lebzeiten: Steueroptimierung",
        "content": """Schenkung zu Lebzeiten nutzt Freibeträge mehrfach (alle 10 Jahre). Freibeträge: Siehe Erbschaftsteuer. Nießbrauch: Schenker behält Nutzungsrecht (Wohnen/Miete), mindert Schenkungswert. Rückforderungsrecht: Bei vorzeitigem Tod des Beschenkten. Wichtig: Notar, Grundbucheintragung, Bindungsfrist bei Familienheim (10 Jahre für Steuerfreiheit).""",
        "category": "Steuerrecht",
        "subcategory": "Schenkung"
    },
    {
        "title": "KfW-Förderung: Programme im Überblick",
        "content": """KfW-Programme: 124 (Wohneigentum), 151/152 (Energieeffizient Sanieren), 153 (Energieeffizient Bauen), 455-B (Barrierearm Umbauen). Tilgungszuschuss: Bis 48.000€ geschenkt (bei KfW-55 oder besser). Zinsvergünstigung: Unter Marktzins. Antragstellung: Über Bank vor Baubeginn. Wichtig: Energieberater meist Voraussetzung!""",
        "category": "Finanzierung",
        "subcategory": "KfW-Förderung"
    },
    {
        "title": "BAFA-Förderung: Heizung und Energie",
        "content": """BAFA fördert: Wärmepumpen, Solarthermie, Pelletheizung, Brennstoffzelle. Förderquote: Bis 40% der Investitionskosten. Antragstellung: Online vor Auftragsvergabe. Wichtig: Förderliste beachten, zertifizierte Fachfirma. Kombination: Mit KfW-Kredit möglich (dann nur BAFA-Zuschuss, nicht beides für gleiche Maßnahme).""",
        "category": "Finanzierung",
        "subcategory": "BAFA-Förderung"
    },
    {
        "title": "Anschlussfinanzierung: Rechtzeitig planen",
        "content": """Anschlussfinanzierung: Wenn Zinsbindung ausläuft. Planung: 3-12 Monate vorher Angebote einholen. Prolongation: Verlängerung bei gleicher Bank (einfach, aber oft teurere Zinsen). Umschuldung: Wechsel zu anderer Bank (bessere Konditionen). Forward-Darlehen: Bis 5 Jahre im Voraus Zinsen sichern. Wichtig: Vergleichen spart Tausende Euro!""",
        "category": "Finanzierung",
        "subcategory": "Anschlussfinanzierung"
    },
    {
        "title": "Umschuldung: Wann lohnenswert?",
        "content": """Umschuldung lohnt bei Zinsdifferenz >0,2%. Kosten: Vorfälligkeitsentschädigung (wenn vor Ende Zinsbindung), Grundschuldabtretung (ca. 0,2%), Notarkosten (gering). Nach 10 Jahren: Kostenfrei kündbar (§ 489 BGB). Wichtig: Gesamtkosten berechnen! Vergleichsrechner nutzen.""",
        "category": "Finanzierung",
        "subcategory": "Umschuldung"
    },
    {
        "title": "Grundschuld: Löschung nach Rückzahlung",
        "content": """Grundschuld bleibt nach Darlehensrückzahlung bestehen (kein akzessorisches Recht). Löschung: Mit Löschungsbewilligung der Bank, Notar löscht im Grundbuch. Kosten: Ca. 0,2% der Grundschuldsumme. Alternative: Bestehen lassen für zukünftige Finanzierung. Wichtig: Löschungsbewilligung gut aufbewahren!""",
        "category": "Finanzierung",
        "subcategory": "Grundschuld"
    },
    {
        "title": "Grundschuldabtretung: Bei Bankwechsel",
        "content": """Grundschuldabtretung: Alte Bank tritt Grundschuld an neue Bank ab (bei Umschuldung). Kosten: Ca. 0,2% der Grundschuldsumme (günstiger als Neueintragung). Alternative: Löschung + Neueintragung (teurer). Wichtig: Immer Abtretung bevorzugen bei Umschuldung!""",
        "category": "Finanzierung",
        "subcategory": "Grundschuld"
    },
    {
        "title": "Bankgespräch: Vorbereitung",
        "content": """Unterlagen fürs Bankgespräch: Einkommensnachweise (3 Monate), Eigenkapitalnachweis, Objekt-Exposé, Schufa-Auskunft, Haushaltsrechnung. Vorbereitung: Budget berechnen, Finanzierungswunsch formulieren, Fragen notieren. Mehrere Banken: Vergleichen! Wichtig: Ehrlich sein, realistische Zahlen.""",
        "category": "Finanzierung",
        "subcategory": "Bankgespräch"
    },
    {
        "title": "Finanzierungszusage: Gültigkeit",
        "content": """Finanzierungszusage: Bank bestätigt Kreditvergabe. Gültigkeit: Meist 2-4 Wochen, bei Neubau länger. Bedingungen: Objektprüfung, keine Verschlechterung Bonität. Wichtig: Vor Kaufvertrag einholen! Schützt vor Fehlkauf.""",
        "category": "Finanzierung",
        "subcategory": "Finanzierungszusage"
    },
    {
        "title": "Darlehensbewilligung: Endgültige Zusage",
        "content": """Darlehensbewilligung: Endgültige Zusage nach Prüfung aller Unterlagen und Objekt. Objektprüfung: Bank prüft Wert (Verkehrswertgutachten). Auszahlung: Nach Grundbucheintragung Grundschuld. Wichtig: Kann 4-8 Wochen dauern!""",
        "category": "Finanzierung",
        "subcategory": "Darlehensbewilligung"
    },
    {
        "title": "Verkehrswertgutachten: Beleihungswert",
        "content": """Verkehrswertgutachten: Bank ermittelt Immobilienwert. Beleihungswert: Meist 80-90% des Verkehrswerts (Sicherheitsabschlag). Bedeutung: Maximale Darlehenssumme. Kosten: Zahlt Bank. Abweichung: Wenn unter Kaufpreis, Eigenkapital erhöhen! Wichtig: Beeinflusst Finanzierungskonditionen.""",
        "category": "Finanzierung",
        "subcategory": "Gutachten"
    },
    {
        "title": "Restschuldversicherung: Sinnvoll?",
        "content": """Restschuldversicherung: Zahlt Darlehen bei Tod, Arbeitsunfähigkeit, Arbeitslosigkeit. Kosten: 3-7% der Darlehenssumme. Alternative: Risikolebensversicherung (günstiger, flexibler). Wichtig: Oft nicht empfehlenswert (teuer, viele Ausschlüsse)! Vergleich: Risikolebensversicherung + Berufsunfähigkeitsversicherung besser.""",
        "category": "Finanzierung",
        "subcategory": "Versicherung"
    },
    {
        "title": "Risikolebensversicherung: Kreditabsicherung",
        "content": """Risikolebensversicherung: Zahlt bei Tod Versicherungssumme. Vorteil: Günstig, Familie abgesichert. Höhe: Restschuldsumme. Bezugsberechtigung: Partner (kann Darlehen tilgen). Kosten: 20-50€ pro Monat für 250.000€. Wichtig: Bei Immobilienfinanzierung dringend empfohlen!""",
        "category": "Finanzierung",
        "subcategory": "Versicherung"
    },
    {
        "title": "Berufsunfähigkeitsversicherung: Einkommensschutz",
        "content": """Berufsunfähigkeitsversicherung: Zahlt bei Berufsunfähigkeit monatliche Rente. Wichtig: Absicherung Einkommen für Kreditrate. Höhe: 1.500-2.500€ pro Monat. Kosten: 50-150€ pro Monat je nach Alter/Beruf. Abschluss: Vor Immobilienkauf (gesundheitliche Prüfung). Wichtig: Fundamentaler Schutz!""",
        "category": "Finanzierung",
        "subcategory": "Versicherung"
    },
    {
        "title": "Cap-Darlehen: Zinsabsicherung nach oben",
        "content": """Cap-Darlehen: Variabler Zins mit Obergrenze (Cap). Vorteil: Profitiert von sinkenden Zinsen, geschützt vor steigenden. Nachteil: Cap-Aufschlag (0,3-0,8%). Seltener: Meist Annuitätendarlehen attraktiver. Wichtig: Vergleich mit festem Zins!""",
        "category": "Finanzierung",
        "subcategory": "Darlehensarten"
    },
    {
        "title": "KfW-Wohneigentumsprogramm 124: Details",
        "content": """KfW 124: Kauf/Bau selbstgenutzter Immobilien. Darlehenssumme: Bis 100.000€ pro Wohneinheit. Zinsen: Unter Marktzins. Tilgung: Nach 1-5 Jahren Beginn. Kombination: Mit Hausbank-Darlehen. Voraussetzung: Selbstnutzung. Wichtig: Über Hausbank beantragen vor Kauf!""",
        "category": "Finanzierung",
        "subcategory": "KfW-Förderung"
    },
    {
        "title": "Modernisierungskredit: Zweckgebunden",
        "content": """Modernisierungskredit: Für Renovierung, Sanierung, Anbau. Zinsen: Oft günstiger als Ratenkredit. Absicherung: Meist ohne Grundschuld bis 50.000€. KfW: Programme für energetische Sanierung. Wichtig: Vergleich mit Aufstockung Immobilienkredit!""",
        "category": "Finanzierung",
        "subcategory": "Modernisierung"
    },
    {
        "title": "Disagio: Abgeld bei Darlehen",
        "content": """Disagio: Auszahlung unter Darlehenssumme (z.B. 95%), Rückzahlung 100%. Vorteil: Niedrigerer Sollzins. Nachteil: Weniger Auszahlung, steuerlich nur anteilig absetzbar. Effektivzins: Meist höher als ohne Disagio. Wichtig: Genau vergleichen, oft unvorteilhaft!""",
        "category": "Finanzierung",
        "subcategory": "Disagio"
    },
    {
        "title": "Bonität verbessern: Maßnahmen",
        "content": """Bonität verbessern: Alte Kredite tilgen, Dispozinsen vermeiden, Raten pünktlich zahlen, falsche Schufa-Einträge löschen, Kreditkarten-Limit senken, nicht zu viele Kreditanfragen. Dauer: 3-12 Monate. Wichtig: Schufa-Selbstauskunft prüfen, Fehler korrigieren!""",
        "category": "Finanzierung",
        "subcategory": "Bonität"
    },
    {
        "title": "Haushaltsrechnung: Vorlage Bank",
        "content": """Haushaltsrechnung für Bank: Einnahmen (Netto, Nebeneinkünfte), Ausgaben (Lebenshaltung, Versicherungen, Kredite, Auto, Freizeit). Verfügbar: Einnahmen minus Ausgaben. Belastbarkeit: Max. 40% verfügbares Einkommen. Wichtig: Realistisch kalkulieren, Puffer einrechnen!""",
        "category": "Finanzierung",
        "subcategory": "Budgetplanung"
    },
    {
        "title": "Muskelhypothek: Eigenleistung",
        "content": """Muskelhypothek: Eigenleistung als Eigenkapital. Anerkennung: Bis zu 15% (max. 30.000€). Voraussetzung: Handwerkliche Fähigkeiten, Zeit. Risiko: Überschätzung, längere Bauzeit. Bank: Prüft realistisch. Wichtig: Konservativ ansetzen!""",
        "category": "Finanzierung",
        "subcategory": "Eigenkapital"
    },
    {
        "title": "Familiendarlehen: Steuerliche Anerkennung",
        "content": """Familiendarlehen: Kredit von Verwandten. Voraussetzung: Schriftlicher Vertrag, marktübliche Zinsen, Rückzahlung tatsächlich. Steuer: Zinsen als Werbungskosten absetzbar (Vermietung). Schenkungssteuer: Bei zinslosen Darlehen ggf. Freibetrag prüfen. Wichtig: Fremdvergleich (wie mit fremdem Dritten)!""",
        "category": "Finanzierung",
        "subcategory": "Familiendarlehen"
    },
    {
        "title": "Kontoauszüge: Was prüft die Bank?",
        "content": """Bank prüft: Regelmäßiges Einkommen, Ausgabeverhalten, Dispo-Nutzung, Rückbuchungen, andere Kredite. Zeitraum: Meist 3 Monate. Wichtig: Geordnete Finanzen zeigen, Dispo vermeiden, Glücksspiel/Sportwetten negativ! Vorbereitung: 3 Monate vor Antrag Ausgaben kontrollieren.""",
        "category": "Finanzierung",
        "subcategory": "Bonität"
    },
    {
        "title": "Finanzierungsvermittler: Vor- und Nachteile",
        "content": """Finanzierungsvermittler: Vergleicht Banken, organisiert Finanzierung. Vorteil: Zeitersparnis, Marktüberblick, Verhandlungsgeschick. Nachteil: Provision (oft von Bank gezahlt, manchmal Kunde). Seriös: Keine Vorkasse, transparente Kosten. Wichtig: Vergleich trotzdem selbst prüfen!""",
        "category": "Finanzierung",
        "subcategory": "Vermittler"
    }
]

print("🚀 BATCH 3: FINANZIERUNG & STEUERN - START")
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

try:
    count = client.count(collection_name="legal_documents")
    total = count.count
    print(f"\n🎯 GESAMT DOKUMENTE: {total}")
    remaining = 4000 - total
    print(f"📊 Noch {remaining} bis zur 4.000!")
except:
    print("⚠️  Konnte Gesamtzahl nicht abrufen")

print("\n🔥 BATCH 3 COMPLETE! 🔥")
