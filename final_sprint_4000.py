#!/usr/bin/env python3
"""FINAL SPRINT: Letzte 100 Dokumente zur 4.000!"""

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
    # WEG-Recht & Verwaltung (30 Dokumente)
    {
        "title": "WEG: Eigentümerversammlung Beschlussfähigkeit",
        "content": """Beschlussfähigkeit: Mindestens 50% der Miteigentumsanteile anwesend (§ 25 WEG). Erste Versammlung: Oft nicht beschlussfähig. Zweite Versammlung: Immer beschlussfähig (unabhängig von Teilnehmerzahl). Einladungsfrist: 2 Wochen schriftlich mit Tagesordnung. Wichtig: Beschlüsse ungültig wenn formelle Fehler!""",
        "category": "WEG-Recht",
        "subcategory": "Eigentümerversammlung"
    },
    {
        "title": "WEG: Mehrheitserfordernisse",
        "content": """Einfache Mehrheit: >50% der abgegebenen Stimmen (z.B. Hausverwalter-Bestellung, Wirtschaftsplan). Doppelte qualifizierte Mehrheit: >75% aller Stimmen + >50% der Köpfe (bauliche Veränderungen). Einstimmig: Nur bei Grundlagenänderung (Änderung Teilungserklärung). Wichtig: Stimmen nach Miteigentumsanteilen, nicht Köpfen!""",
        "category": "WEG-Recht",
        "subcategory": "Beschlüsse"
    },
    {
        "title": "WEG: Verwalterbeirat Aufgaben",
        "content": """Verwalterbeirat: Bindeglied zwischen Eigentümern und Verwalter. Aufgaben: Unterstützung Verwalter, Kontrolle Jahresabrechnung, Einsicht Unterlagen. Wahl: Durch Eigentümerversammlung. Anzahl: Meist 1-3 Personen. Haftung: Bei grober Pflichtverletzung. Vergütung: Möglich, meist ehrenamtlich. Wichtig: Stärkt Eigentümerrechte!""",
        "category": "WEG-Recht",
        "subcategory": "Verwalterbeirat"
    },
    {
        "title": "WEG: Instandhaltungsrücklage Höhe",
        "content": """Instandhaltungsrücklage: Rücklagen für zukünftige Reparaturen. Höhe: Mind. 0,80€/m² pro Monat (Empfehlung: 1-2€/m²). Altbau: Höher (2-3€/m²). Verwendung: Nur für Instandhaltung/-setzung Gemeinschaftseigentum. Wichtig: Bei Kauf prüfen (sollte mind. 50€/m² Wohnfläche sein)!""",
        "category": "WEG-Recht",
        "subcategory": "Instandhaltungsrücklage"
    },
    {
        "title": "WEG: Hausverwalter Bestellung",
        "content": """Hausverwalter: Verwaltet Gemeinschaft. Bestellung: Durch Beschluss (einfache Mehrheit). Vertrag: Meist 1-3 Jahre. Kündigung: Jederzeit mit 6 Monaten Frist oder wichtigem Grund. Aufgaben: Wirtschaftsplan, Jahresabrechnung, Instandhaltung organisieren, Versammlungen einberufen. Vergütung: 20-40€ pro Wohnung/Monat. Wichtig: Guter Verwalter ist Gold wert!""",
        "category": "WEG-Recht",
        "subcategory": "Hausverwalter"
    },
    {
        "title": "WEG: Wirtschaftsplan",
        "content": """Wirtschaftsplan: Haushaltsplan für kommendes Jahr. Inhalt: Geplante Einnahmen (Hausgelder), Ausgaben (Betriebskosten, Instandhaltung, Verwaltung). Beschluss: Vor Jahresbeginn. Nachtragshaushalt: Bei unvorhergesehenen Ausgaben. Wichtig: Bindend für Verwalter!""",
        "category": "WEG-Recht",
        "subcategory": "Wirtschaftsplan"
    },
    {
        "title": "WEG: Jahresabrechnung Frist",
        "content": """Jahresabrechnung: Abrechnung Wirtschaftsjahr. Frist: Spätestens 6 Monate nach Jahresende. Inhalt: Einnahmen, Ausgaben, Einzelabrechnung pro Wohnung. Prüfung: Verwalterbeirat + Eigentümer. Einwendungen: Innerhalb Jahresfrist. Genehmigung: Durch Eigentümerversammlung. Wichtig: Genau prüfen, Belege anfordern!""",
        "category": "WEG-Recht",
        "subcategory": "Jahresabrechnung"
    },
    {
        "title": "WEG: Sonderumlagen",
        "content": """Sonderumlage: Zusätzliche Zahlung für außerplanmäßige Ausgaben (z.B. Dachsanierung). Beschluss: Einfache Mehrheit. Fälligkeit: Nach Beschluss. Zahlung: Innerhalb festgelegter Frist. Wichtig: Bei großen Reparaturen üblich! Sollte aus Instandhaltungsrücklage vermieden werden.""",
        "category": "WEG-Recht",
        "subcategory": "Sonderumlagen"
    },
    {
        "title": "WEG: Gemeinschaftseigentum Definition",
        "content": """Gemeinschaftseigentum: Teile des Gebäudes, die allen gehören. Beispiele: Grundstück, Dach, Fassade, Treppenhaus, Heizung, Aufzug. Nicht: Wohnung innen (Sondereigentum). Grenzfälle: Fenster, Balkone (oft Gemeinschaftseigentum, Sondernutzung). Wichtig: Teilungserklärung prüfen!""",
        "category": "WEG-Recht",
        "subcategory": "Gemeinschaftseigentum"
    },
    {
        "title": "WEG: Sondereigentum Umfang",
        "content": """Sondereigentum: Wohnung + Sondernutzungsrechte. Umfang: Innenräume, Bodenbeläge, Innentüren, Sanitär/Elektro innerhalb Wohnung. Nicht: Außenwände (tragende Teile), Fenster (oft Gemeinschaftseigentum). Wichtig: Änderungen an tragenden Wänden genehmigungspflichtig!""",
        "category": "WEG-Recht",
        "subcategory": "Sondereigentum"
    },
    {
        "title": "WEG: Sondernutzungsrechte",
        "content": """Sondernutzungsrecht: Exklusive Nutzung von Gemeinschaftseigentum. Beispiele: Garten, Terrasse, Stellplatz, Keller. Eintragung: Teilungserklärung. Pflichten: Instandhaltung oft beim Nutzer. Kosten: Meist keine laufenden, nur Instandhaltung. Wichtig: Beim Kauf prüfen (wertsteigernd)!""",
        "category": "WEG-Recht",
        "subcategory": "Sondernutzungsrechte"
    },
    {
        "title": "WEG: Beschlussanfechtung",
        "content": """Beschlussanfechtung: Klage gegen Eigentümerbeschluss. Frist: 1 Monat nach Beschluss. Gründe: Formfehler (Einladung), Mehrheitsfehler, Verstoß gegen Gesetz/Teilungserklärung. Gericht: Amtsgericht. Wichtig: Frist unbedingt einhalten! Anwalt empfohlen.""",
        "category": "WEG-Recht",
        "subcategory": "Beschlussanfechtung"
    },
    {
        "title": "WEG: Miteigentumsanteil Berechnung",
        "content": """Miteigentumsanteil (MEA): Anteil am Gemeinschaftseigentum. Berechnung: Nach Wohnfläche (meist in Tausendstel). Bedeutung: Stimmrecht, Kostenbeteiligung. Beispiel: 80m² Wohnung bei 2.000m² Gesamt = 40/1000 MEA. Wichtig: Bestimmt Hausgeldhöhe!""",
        "category": "WEG-Recht",
        "subcategory": "Miteigentumsanteil"
    },
    {
        "title": "WEG: Hausordnung Inhalt",
        "content": """Hausordnung: Regelt Zusammenleben. Inhalt: Ruhezeiten, Tierhaltung, Treppenhaus-Nutzung, Müllentsorgung, Gemeinschaftsräume. Beschluss: Einfache Mehrheit. Bindung: Für Eigentümer + Mieter. Verstoß: Abmahnung, Bußgeld, Kündigung (Mieter). Wichtig: Muss verhältnismäßig sein!""",
        "category": "WEG-Recht",
        "subcategory": "Hausordnung"
    },
    {
        "title": "WEG: Modernisierung Balkonverglasung",
        "content": """Balkonverglasung: Bauliche Veränderung, braucht Beschluss. Mehrheit: Einfache Mehrheit wenn wirtschaftlich vernünftig und Beeinträchtigung zumutbar. Nachteile: Optik, Statik. Vorteil: Lärmschutz, Wetterschutz. Kosten: Trägt Antragsteller. Wichtig: Einheitliches Erscheinungsbild!""",
        "category": "WEG-Recht",
        "subcategory": "Modernisierung"
    },
    {
        "title": "WEG: Ladestation E-Auto Anspruch",
        "content": """Ladestation: Anspruch auf Genehmigung seit 2020 (§ 20 WEG). Beschluss: Gemeinschaft kann nur Modalitäten (Art, Ort) bestimmen. Kosten: Trägt Antragsteller + laufende Kosten. Installation: Durch Fachfirma. Nutzung: Nur für Antragsteller (Sondernutzung). Wichtig: Durchbruch für E-Mobilität!""",
        "category": "WEG-Recht",
        "subcategory": "E-Ladestation"
    },
    {
        "title": "WEG: Barrierefreiheit Anspruch",
        "content": """Barrierefreiheit: Anspruch auf bauliche Maßnahmen (Rampe, Aufzug, Türverbreiterung) seit 2020. Beschluss: Kann nur ablehnen bei unbilliger Härte. Kosten: Antragsteller + ggf. KfW-Förderung. Wichtig: Ältere Eigentümer / Behinderung haben starken Anspruch!""",
        "category": "WEG-Recht",
        "subcategory": "Barrierefreiheit"
    },
    {
        "title": "WEG: Eigenverwaltung vs. WEG-Verwalter",
        "content": """Eigenverwaltung: Eigentümer verwalten selbst (nur bei kleinen Anlagen sinnvoll, <5 Einheiten). WEG-Verwalter: Professionelle Verwaltung (ab 5 Einheiten empfohlen). Vorteile Verwalter: Expertise, Neutralität, Zeitersparnis. Kosten: 20-40€ pro Einheit/Monat. Wichtig: Bei großen WEG zwingend notwendig!""",
        "category": "WEG-Recht",
        "subcategory": "Verwaltung"
    },
    {
        "title": "WEG: Versammlungsprotokoll Bedeutung",
        "content": """Versammlungsprotokoll: Dokumentiert Beschlüsse. Inhalt: Anwesende, Tagesordnung, Beschlüsse, Abstimmungsergebnisse. Frist: Versand innerhalb 2 Wochen. Widerspruch: Innerhalb 1 Monat schriftlich. Wichtig: Sorgfältig prüfen, Grundlage für Anfechtung!""",
        "category": "WEG-Recht",
        "subcategory": "Protokoll"
    },
    {
        "title": "WEG: Wohnungskauf Unterlagenprüfung",
        "content": """Vor Wohnungskauf prüfen: Teilungserklärung, letzten 3 Jahresabrechnungen, Wirtschaftsplan, Versammlungsprotokolle (2 Jahre), Instandhaltungsrücklage, Beschlüsse zu Sanierungen. Wichtig: Versteckte Kosten erkennen! Anwalt/Berater hinzuziehen.""",
        "category": "WEG-Recht",
        "subcategory": "Kaufprüfung"
    },
    {
        "title": "WEG: Rücklagen zu niedrig - Risiko",
        "content": """Niedrige Instandhaltungsrücklage: Risiko für Sonderumlagen. Warnzeichen: <30€/m² Wohnfläche, alte Gebäude mit niedriger Rücklage. Folge: Bei Sanierung hohe Sonderumlagen (10.000-50.000€). Wichtig: Vor Kauf prüfen, ggf. Verhandeln oder ablehnen!""",
        "category": "WEG-Recht",
        "subcategory": "Rücklagen"
    },
    {
        "title": "WEG: Eigentümer-Streit Schlichtung",
        "content": """Eigentümer-Streit: Häufig über Lärm, Baumaßnahmen, Kosten. Schlichtung: Außergerichtlich (Mediator, Ombudsmann). Klage: Amtsgericht (teuer, langwierig). Wichtig: Frühzeitig Kommunikation suchen! Eskalation vermeiden.""",
        "category": "WEG-Recht",
        "subcategory": "Streitschlichtung"
    },
    {
        "title": "WEG: Zwangsverwaltung bei Zahlungsverzug",
        "content": """Zwangsverwaltung: Bei Zahlungsverzug Hausgeld kann Gemeinschaft Zwangsverwaltung beantragen. Folge: Mieteinnahmen gehen an Gemeinschaft. Dauer: Bis Schulden beglichen. Kosten: Trägt säumiger Eigentümer. Wichtig: Drastisches Mittel, aber wirksam!""",
        "category": "WEG-Recht",
        "subcategory": "Zwangsverwaltung"
    },
    {
        "title": "WEG: Gewerbliche Nutzung Zulässigkeit",
        "content": """Gewerbliche Nutzung: Nur wenn Teilungserklärung erlaubt. Einschränkungen: Ruhestörung, Kundenverkehr, Geruch. Beschluss: Kann Nutzung untersagen wenn Störung. Wichtig: Vor Kauf prüfen wenn gewerbliche Nutzung geplant!""",
        "category": "WEG-Recht",
        "subcategory": "Gewerbenutzung"
    },
    {
        "title": "WEG: Beirat Haftung",
        "content": """Beirat haftet bei grober Fahrlässigkeit (z.B. Unterschlagung übersehen). Versicherung: D&O-Versicherung für Beirat empfohlen. Ehrenamt: Meist ohne Vergütung, daher nur leichte Haftung. Wichtig: Sorgfältig prüfen, dokumentieren!""",
        "category": "WEG-Recht",
        "subcategory": "Beiratshaftung"
    },
    {
        "title": "WEG: Sanierung Fassade Kostenbeteiligung",
        "content": """Fassadensanierung: Gemeinschaftseigentum, alle zahlen nach MEA. Ausnahme: Balkone in Sondernutzung (Nutzer zahlt mehr). Kosten: 50-200€/m² Fassade. Finanzierung: Aus Rücklage + Sonderumlage. KfW: Förderung möglich bei energetischer Sanierung. Wichtig: Frühzeitig planen!""",
        "category": "WEG-Recht",
        "subcategory": "Fassadensanierung"
    },
    {
        "title": "WEG: Dachsanierung Dringlichkeit",
        "content": """Dachsanierung: Lebenserwartung Dach 30-50 Jahre. Kosten: 100-250€/m² Dachfläche. Finanzierung: Rücklage sollte ausreichen, sonst Sonderumlage. Wichtig: Regelmäßige Wartung verlängert Lebensdauer! Bei Kauf Zustand prüfen.""",
        "category": "WEG-Recht",
        "subcategory": "Dachsanierung"
    },
    {
        "title": "WEG: Heizungserneuerung",
        "content": """Heizungserneuerung: Nach ca. 20-30 Jahren fällig. Kosten: 20.000-50.000€ je nach Größe und System. Beschluss: Einfache Mehrheit. Förderung: BAFA (Wärmepumpe bis 40%). Wichtig: Frühzeitig planen, Rücklage aufbauen!""",
        "category": "WEG-Recht",
        "subcategory": "Heizungserneuerung"
    },
    {
        "title": "WEG: Aufzug Einbau Anspruch",
        "content": """Aufzug-Einbau: Anspruch bei berechtigtem Interesse (Alter, Behinderung). Kosten: 50.000-100.000€. Finanzierung: Antragsteller + KfW-Förderung + anteilig Gemeinschaft wenn Wertsteigerung. Wichtig: Seit 2020 einfacher durchsetzbar!""",
        "category": "WEG-Recht",
        "subcategory": "Aufzug"
    },
    {
        "title": "WEG: Tierhaltung Regelung",
        "content": """Tierhaltung: Teilungserklärung/Hausordnung kann regeln. Verbot: Nur bei sachlichem Grund. Hunde/Katzen: Erlaubnisvorbehalt möglich, aber nicht willkürlich. Kleintiere: Erlaubnisfrei. Beschluss: Kann nicht pauschal verbieten. Wichtig: Einzelfallentscheidung!""",
        "category": "WEG-Recht",
        "subcategory": "Tierhaltung"
    },
    
    # Immobilienbewertung & Investment (30 Dokumente)
    {
        "title": "Verkehrswert: Ermittlungsverfahren",
        "content": """Verkehrswert (Marktwert): Preis bei normalem Verkauf. Verfahren: Vergleichswertverfahren (Eigentumswohnungen), Ertragswertverfahren (Mietobjekte), Sachwertverfahren (selbstgenutzte Eigenheime). Gutachter: Sachverständiger, Bank, Online-Tool. Abweichung: Angebot kann höher/niedriger sein (Marktlage). Wichtig: Für Finanzierung entscheidend!""",
        "category": "Bewertung",
        "subcategory": "Verkehrswert"
    },
    {
        "title": "Vergleichswertverfahren: Anwendung",
        "content": """Vergleichswertverfahren: Bewertung anhand vergleichbarer Verkäufe. Anwendung: Eigentumswohnungen, Grundstücke. Grundlage: Kaufpreissammlung Gutachterausschuss. Anpassung: Nach Lage, Zustand, Ausstattung. Vorteil: Marktnahe Bewertung. Wichtig: Für Eigentumswohnungen Standard!""",
        "category": "Bewertung",
        "subcategory": "Vergleichswertverfahren"
    },
    {
        "title": "Ertragswertverfahren: Berechnung",
        "content": """Ertragswertverfahren: Bewertung nach erzielbaren Mieterträgen. Formel: Jahresrohertrag - Bewirtschaftungskosten = Reinertrag → Kapitalisierung. Anwendung: Vermietete Mehrfamilienhäuser, Gewerbeimmobilien. Wichtig: Je höher Mietrendite, desto höher Wert. Für Investoren relevant!""",
        "category": "Bewertung",
        "subcategory": "Ertragswertverfahren"
    },
    {
        "title": "Sachwertverfahren: Grundlagen",
        "content": """Sachwertverfahren: Bewertung nach Herstellungskosten. Berechnung: Bodenwert + Gebäudewert (Herstellungskosten abzgl. Alterswertminderung). Anwendung: Selbstgenutzte Eigenheime ohne Vergleichswerte. Nachteil: Oft über Marktwert. Wichtig: Für Eigenheime mit individuellen Merkmalen!""",
        "category": "Bewertung",
        "subcategory": "Sachwertverfahren"
    },
    {
        "title": "Bodenrichtwert: Bedeutung",
        "content": """Bodenrichtwert: Durchschnittlicher Wert unbebauter Grundstücke. Veröffentlichung: Gutachterausschuss alle 2 Jahre. Nutzung: Für Grundstücksbewertung, Grundsteuer-Reform. Abweichung: Individuelle Grundstücke können teurer/günstiger sein (Lage, Erschließung). Wichtig: Orientierung für Kaufpreis!""",
        "category": "Bewertung",
        "subcategory": "Bodenrichtwert"
    },
    {
        "title": "Renditeberechnung: Brutto vs. Netto",
        "content": """Bruttorendite: Jahresmiete / Kaufpreis x 100%. Nettorendite: (Jahresmiete - Kosten) / (Kaufpreis + Nebenkosten) x 100%. Kosten: Verwaltung, Instandhaltung, Mietausfall, Grundsteuer. Wichtig: Nur Nettorendite ist aussagekräftig! Ziel: >4% netto bei Vermietung.""",
        "category": "Bewertung",
        "subcategory": "Rendite"
    },
    {
        "title": "Mietmultiplikator: Kaufpreisfaktor",
        "content": """Mietmultiplikator: Kaufpreis / Jahreskaltmiete. Bedeutung: Wie viele Jahresmieten kostet Immobilie. Bewertung: <15 = günstig, 15-20 = normal, >20 = teuer. Regional: In Großstädten oft 25-30. Wichtig: Für schnelle Einschätzung Kaufpreis!""",
        "category": "Bewertung",
        "subcategory": "Mietmultiplikator"
    },
    {
        "title": "Wertsteigerung: Faktoren",
        "content": """Wertsteigerung durch: Lage (Top-Lage steigt stärker), Zustand (Modernisierung), Marktlage (Angebot/Nachfrage), Infrastruktur-Entwicklung. Historisch: 2-4% p.a. im Schnitt. Risiko: Kann auch fallen! Wichtig: Langfristig investieren, nicht spekulieren!""",
        "category": "Bewertung",
        "subcategory": "Wertsteigerung"
    },
    {
        "title": "Lage-Bewertung: 1a vs. 1b vs. 2 Lage",
        "content": """1a-Lage: Zentrum, beste Infrastruktur, höchste Preise, stabile Nachfrage. 1b-Lage: Stadtteil gut angebunden, etwas günstiger. 2. Lage: Stadtrand, günstig, aber Wertsteigerung begrenzt. Wichtig: Lage ist entscheidend für Wertentwicklung! 1a-Lage = sicheres Investment.""",
        "category": "Bewertung",
        "subcategory": "Lage"
    },
    {
        "title": "Mikrolage: Feinhei ten",
        "content": """Mikrolage: Straße, direkte Umgebung. Faktoren: Lärmbelastung, Grünflächen, Schulen/Kitas, Einkaufsmöglichkeiten, ÖPNV-Anbindung, Nachbarschaft. Unterschied: Gleiche Straße kann 20% Preisunterschied haben! Wichtig: Vor Ort besichtigen, Umfeld prüfen!""",
        "category": "Bewertung",
        "subcategory": "Mikrolage"
    },
    {
        "title": "Cashflow-Rechnung: Liquidität",
        "content": """Cashflow: Einnahmen minus Ausgaben. Positiv: Mieteinnahmen > Ausgaben (inkl. Darlehensrate). Negativ: Nachschuss erforderlich. Berechnung: Kaltmiete - Bewirtschaftungskosten - Darle hensrate. Ziel: Neutraler oder positiver Cashflow. Wichtig: Liquidität sichern!""",
        "category": "Bewertung",
        "subcategory": "Cashflow"
    },
    {
        "title": "Eigenkapitalrendite: Hebeleffekt",
        "content": """Eigenkapitalrendite: Gewinn / Eigenkapital x 100%. Hebeleffekt: Je weniger Eigenkapital, desto höher Rendite (aber auch Risiko). Beispiel: 5% Objektrendite mit 20% EK = 25% EK-Rendite. Risiko: Bei Wertverlust Totalverlust EK möglich. Wichtig: Balance finden!""",
        "category": "Bewertung",
        "subcategory": "Eigenkapitalrendite"
    },
    {
        "title": "Due Diligence: Immobilienprüfung",
        "content": """Due Diligence: Sorgfältige Prüfung vor Kauf. Aspekte: Rechtlich (Grundbuch, Baulasten), technisch (Zustand, Mängel), wirtschaftlich (Mieten, Kosten). Gutachten: Bausachverständiger empfohlen. Kosten: 500-2.000€. Wichtig: Schützt vor Fehlkauf!""",
        "category": "Bewertung",
        "subcategory": "Due Diligence"
    },
    {
        "title": "Bausubstanz: Bewertung Zustand",
        "content": """Bausubstanz-Zustand: Neuwertig (0-5 Jahre), gepflegt (5-15 Jahre), durchschnittlich (15-30 Jahre), renovierungsbedürftig (30-50 Jahre), sanierungsbedürftig (>50 Jahre). Bewertung: Dach, Fassade, Fenster, Heizung, Elektro, Sanitär. Wichtig: Sanierungskosten einkalkulieren!""",
        "category": "Bewertung",
        "subcategory": "Bausubstanz"
    },
    {
        "title": "Energieausweis: Einfluss auf Wert",
        "content": """Energieausweis: Verbrauchsausweis (tatsächlicher Verbrauch) oder Bedarfsausweis (berechnet). Klassen: A+ bis H (A+ = beste Effizienz). Einfluss: Energieeffizienz steigert Wert (10-20% Unterschied). Pflicht: Bei Verkauf/Vermietung vorlegen. Wichtig: Sanierung lohnt sich langfristig!""",
        "category": "Bewertung",
        "subcategory": "Energieausweis"
    },
    {
        "title": "Marktphasen: Käufer- vs. Verkäufermarkt",
        "content": """Verkäufermarkt: Hohe Nachfrage, wenig Angebot → Preise steigen. Käufermarkt: Viel Angebot, wenig Nachfrage → Preise sinken. Aktuell (2024): Regional unterschiedlich, Großstädte oft Verkäufermarkt. Strategie: In Käufermarkt kaufen, in Verkäufermarkt verkaufen. Wichtig: Marktlage beobachten!""",
        "category": "Bewertung",
        "subcategory": "Marktphasen"
    },
    {
        "title": "Mietpreis einschätzung: Ortsübliche Miete",
        "content": """Ortsübliche Miete: Nach Mietspiegel, Vergleichswohnungen. Online-Tools: Immoscout, WOWI. Faktoren: Lage, Größe, Zustand, Ausstattung. Überhöht: >20% über Mietspiegel schwer vermietbar. Wichtig: Realistische Miete ansetzen für Rendite-Kalkulation!""",
        "category": "Bewertung",
        "subcategory": "Mietpreisschätzung"
    },
    {
        "title": "Nebenwerte: Stadt-Umland-Verhältnis",
        "content": """Nebenwerte: Umland von Metropolen. Vorteil: Günstiger, Pendler-Nachfrage. Nachteil: Langsamere Wertsteigerung, schlechtere Vermietbarkeit. Sweet Spot: 20-30km von Großstadt, gute Verkehrsanbindung. Wichtig: Infrastruktur-Entwicklung prüfen!""",
        "category": "Bewertung",
        "subcategory": "Nebenwerte"
    },
    {
        "title": "Studentenwohnungen: Rendite-Chancen",
        "content": """Studentenwohnungen: Oft hohe Rendite (5-7% brutto). Vorteil: Hohe Nachfrage, kleine Wohnungen. Nachteil: Höherer Verwaltungsaufwand, Fluktuation, möbliert. Lage: Uni-Nähe essentiell. Wichtig: Nur in Uni-Städten mit steigenden Studentenzahlen!""",
        "category": "Bewertung",
        "subcategory": "Studentenwohnungen"
    },
    {
        "title": "Denkmalimmobilien: Investment-Aspekte",
        "content": """Denkmalimmobilien: Steuervorteile (erhöhte AfA), aber Auflagen. Rendite: Steuerersparnis kann 10-20% bringen. Risiko: Sanierungskosten höher, Wiederverkauf schwieriger. Zielgruppe: Gutverdiener mit hoher Steuerlast. Wichtig: Gesamtrechnung mit Steuerberater!""",
        "category": "Bewertung",
        "subcategory": "Denkmalimmobilien"
    },
    {
        "title": "Gewerbimmobilien: Rendite-Unterschiede",
        "content": """Gewerbeimmobilien: Höhere Renditen (5-8%), aber höheres Risiko. Typen: Büro, Einzelhandel, Logistik, Hotel. Risiko: Längere Leerstandszeiten, spezialisierte Objekte. Vorteil: Professionelle Mieter, längere Mietverträge. Wichtig: Nur für erfahrene Investoren!""",
        "category": "Bewertung",
        "subcategory": "Gewerbeimmobilien"
    },
    {
        "title": "Pflegeimmobilien: Rendite-Modell",
        "content": """Pflegeimmobilien: Investment in Pflege-Apartments. Rendite: 3,5-5% p.a. sicher. Vertrag: Pachtvertrag mit Betreiber (20-30 Jahre). Risiko: Betreiber-Insolvenz, demografische Entwicklung. Vorteil: Planbare Einnahmen, wenig Aufwand. Wichtig: Seriösen Betreiber prüfen!""",
        "category": "Bewertung",
        "subcategory": "Pflegeimmobilien"
    },
    {
        "title": "Projektentwicklung: Bauträger-Modell",
        "content": """Projektentwicklung: Kauf vom Bauträger (Plan/Bau). Vorteil: Neu, Gewährleistung, steuerliche Abschreibung. Nachteil: Baurisiko, Fertigstellung verzögert. MaBV: Schützt Käufer (Zahlung nach Baufortschritt). Wichtig: Nur seriöse Bauträger, Referenzen prüfen!""",
        "category": "Bewertung",
        "subcategory": "Projektentwicklung"
    },
    {
        "title": "Zwangsversteigerung: Chancen und Risiken",
        "content": """Zwangsversteigerung: Kauf unter Verkehrswert möglich (10-30% günstiger). Risiko: Keine Gewährleistung, eingeschränkte Besichtigung, Altlasten. Mindestgebot: 50% Verkehrswert (70% bei 2. Termin). Wichtig: Gründliche Vorbereitung, Gutachten lesen, Finanzierung bereit!""",
        "category": "Bewertung",
        "subcategory": "Zwangsversteigerung"
    },
    {
        "title": "Teilverkauf: Modell Leibrente",
        "content": """Teilverkauf: Verkauf von 25-50% an Investor, Wohnrecht bleibt. Vorteil: Liquidität ohne Auszug. Kosten: Nutzungsentgelt für bewohnten Teil. Risiko: Wertsteigerung nur teilweise, komplexer Vertrag. Zielgruppe: Senioren mit Liquiditätsbedarf. Wichtig: Vergleich mit Leibrente!""",
        "category": "Bewertung",
        "subcategory": "Teilverkauf"
    },
    {
        "title": "Immobilienfonds: REITs",
        "content": """REITs (Real Estate Investment Trusts): Börsengehandelte Immobilienfonds. Vorteil: Diversifikation, Liquidität, keine Grunderwerbsteuer. Rendite: 3-6% Dividende. Risiko: Kursschwankungen, keine Kontrolle. Wichtig: Für Einsteiger oder Beimischung zum Portfolio!""",
        "category": "Bewertung",
        "subcategory": "REITs"
    },
    {
        "title": "Crowdinvesting: Immobilien-Schwarmfinanzierung",
        "content": """Crowdinvesting: Investment ab 500€ in Immobilien-Projekte. Rendite: 5-7% p.a. angestrebt. Risiko: Totalverlust möglich (Nachrang-Darlehen). Laufzeit: 1-5 Jahre. Plattformen: Exporo, Zinsland, iFunded. Wichtig: Nur als Beimischung, Risiko streuen!""",
        "category": "Bewertung",
        "subcategory": "Crowdinvesting"
    },
    {
        "title": "Portfoliodiversifikation: Immobilien-Mix",
        "content": """Diversifikation: Nicht alles auf eine Karte. Strategien: Mehrere Objekte (Standorte, Typen), Mix Eigennutzung/Vermietung, Beimischung REITs/Crowdinvesting. Vorteil: Risikominimierung. Wichtig: Für größere Investments essentiell!""",
        "category": "Bewertung",
        "subcategory": "Portfoliodiversifikation"
    },
    {
        "title": "Exit-Strategie: Verkaufszeitpunkt",
        "content": """Exit-Strategie: Wann verkaufen? Faktoren: Marktlage (Hochphase), Steuer (nach 10 Jahren), Lebensphase. Timing: Schwierig vorherzusagen. Regel: Langfristig halten außer bei dringendem Bedarf. Wichtig: Emotionen rausnehmen, rational entscheiden!""",
        "category": "Bewertung",
        "subcategory": "Exit-Strategie"
    },
    {
        "title": "Sanierungsaufwand: Kalkulation",
        "content": """Sanierungskosten: Dach (100-250€/m²), Fassade (50-200€/m²), Fenster (400-800€/Stück), Heizung (15.000-30.000€), Bad (10.000-25.000€), Elektro (50-100€/m²). Puffer: +20% für Unvorhergesehenes. Wichtig: Vor Kauf Gutachten, realistische Kalkulation!""",
        "category": "Bewertung",
        "subcategory": "Sanierungskosten"
    },
    
    # Sonstiges / Zusätzliche Themen (23 Dokumente)
    {
        "title": "Immobilienmakler: Bestellerprinzip",
        "content": """Bestellerprinzip bei Wohnraum-Vermietung: Wer bestellt, bezahlt. Vermietung: Vermieter zahlt Makler wenn er beauftragt. Kauf: Käufer + Verkäufer teilen (je nach Bundesland 3-7% Gesamt). Wichtig: Bei Vermietung kein Makler für Mieter mehr!""",
        "category": "Maklerrecht",
        "subcategory": "Bestellerprinzip"
    },
    {
        "title": "Vorkaufsrecht: Mieter und Gemeinde",
        "content": """Mieter-Vorkaufsrecht: Bei Umwandlung Miet- zu Eigentumswohnung (10 Jahre). Gemeinde-Vorkaufsrecht: Bei Grundstücken in Bebauungsplan-/Sanierungsgebieten. Frist: 2 Monate. Preis: Zu gleichen Bedingungen wie Käufer. Wichtig: Verzögerung einkalkulieren!""",
        "category": "Kaufrecht",
        "subcategory": "Vorkaufsrecht"
    },
    {
        "title": "Besichtigung: Rechte und Pflichten",
        "content": """Besichtigungsrecht Vermieter: Bei berechtigtem Interesse (Verkauf, Reparatur) mit Ankündigung (mind. 24 Stunden). Häufigkeit: Nicht zu oft (max. 1x Monat). Mieter: Muss dulden zu normalen Zeiten. Verweigerung: Bei wichtigem Grund erlaubt. Wichtig: Mieter hat Privatsphäre-Schutz!""",
        "category": "Mietrecht",
        "subcategory": "Besichtigung"
    },
    {
        "title": "Räumungsklage: Ablauf",
        "content": """Räumungsklage: Bei Mietrückstand, fristloser Kündigung. Verfahren: Klage → Verhandlung → Urteil → Zwangsräumung. Dauer: 3-12 Monate. Kosten: 2.000-5.000€. Räumungsfrist: 2 Wochen bis 3 Monate. Wichtig: Letzte Option, sehr belastend für beide Seiten!""",
        "category": "Mietrecht",
        "subcategory": "Räumungsklage"
    },
    {
        "title": "Mietrückstand: Folgen",
        "content": """Mietrückstand: Ab 2 Monatsmieten fristlose Kündigung möglich. Mahnung: Erst Mahnung, dann Kündigung. Nachzahlung: Heilung möglich bis 2 Monate nach Kündigung. Räumungsklage: Letzter Schritt. Schufa: Negativeintrag wahrscheinlich. Wichtig: Frühzeitig kommunizieren, Ratenzahlung anbieten!""",
        "category": "Mietrecht",
        "subcategory": "Mietrückstand"
    },
    {
        "title": "Zwischenmiete: Rechtslage",
        "content": """Zwischenmiete: Mieter vermietet befristet weiter. Erlaubnis: Vermieter muss zustimmen (berechtigtes Interesse). Dauer: Meist 6-24 Monate. Haftung: Hauptmieter haftet. Mehrerlös: Steht Vermieter zu (Wuchergrenze). Wichtig: Schriftliche Genehmigung einholen!""",
        "category": "Mietrecht",
        "subcategory": "Zwischenmiete"
    },
    {
        "title": "Wohnungsübergabe: Protokoll",
        "content": """Übergabeprotokoll: Dokumentiert Zustand bei Ein-/Auszug. Inhalt: Zählerstände, Mängel, Schlüsselanzahl, Reinigung. Fotos: Zusätzlich empfohlen. Bedeutung: Beweismittel bei Streit über Kaution. Wichtig: Beide Parteien unterschreiben, jeder Exemplar!""",
        "category": "Mietrecht",
        "subcategory": "Wohnungsübergabe"
    },
    {
        "title": "Versicherungen Eigentümer: Übersicht",
        "content": """Pflicht: Gebäudeversicherung (Feuer, Leitungswasser). Empfohlen: Haftpflicht, Rechtsschutz, Elementarschaden (Hochwasser), Glasversicherung. Vermietung: Mietausfallversicherung, Rechtsschutz. Kosten: 500-1.500€ pro Jahr. Wichtig: Nicht überver sichern, aber Grundschutz!""",
        "category": "Versicherung",
        "subcategory": "Eigentümer"
    },
    {
        "title": "Versicherungen Mieter: Notwendigkeit",
        "content": """Pflicht: Keine. Empfohlen: Hausratversicherung (Einbruch, Feuer), Haftpflicht (Schäden an Mietsache). Glasversicherung: Meist nicht nötig (Vermieter). Kosten: 100-300€ pro Jahr. Wichtig: Haftpflicht schützt vor hohen Kosten!""",
        "category": "Versicherung",
        "subcategory": "Mieter"
    },
    {
        "title": "Hausverwaltung: Aufgaben",
        "content": """Hausverwaltung (nicht WEG): Für Mietobjekte. Aufgaben: Mieterbetreuung, Nebenkostenabrechnung, Instandhaltung organisieren, Mietersuche. Kosten: 20-35€ pro Wohnung/Monat. Wichtig: Entlastet Vermieter erheblich, bei mehreren Objekten fast unverzichtbar!""",
        "category": "Verwaltung",
        "subcategory": "Hausverwaltung"
    },
    {
        "title": "Grundbuch: Aufbau und Abteilungen",
        "content": """Grundbuch dokumentiert Eigentumsverhältnisse. Abteilung I: Eigentümer. Abteilung II: Lasten (Wegerechte, Wohnrechte, Baulasten). Abteilung III: Grundschulden, Hypotheken. Einsicht: Berechtigtes Interesse erforderlich. Wichtig: Vor Kauf prüfen!""",
        "category": "Grundbuch",
        "subcategory": "Aufbau"
    },
    {
        "title": "Auflassung: Eigentumsübertragung",
        "content": """Auflassung: Einigung über Eigentumsübertragung beim Notar (§ 925 BGB). Voraussetzung: Beide Parteien anwesend oder vertreten. Wirkung: Zusammen mit Eintragung Grundbuch Eigentumsübergang. Wichtig: Notartermin nicht versäumen!""",
        "category": "Kaufrecht",
        "subcategory": "Auflassung"
    },
    {
        "title": "Notaranderkonto: Kaufpreissicherung",
        "content": """Notaranderkonto (Treuhandkonto): Notar verwahrt Kaufpreis. Ablauf: Käufer überweist an Notar → Notar prüft Bedingungen → Auszahlung an Verkäufer. Sicherheit: Für beide Seiten. Kosten: Ca. 0,1-0,3% Kaufpreis. Wichtig: Standard-Verfahren bei Immobilienkäufen!""",
        "category": "Kaufrecht",
        "subcategory": "Notaranderkonto"
    },
    {
        "title": "Lastenzuschuss: Wohngeld für Eigentümer",
        "content": """Lastenzuschuss: Wohngeld für Eigentümer selbstgenutzter Immobilien. Voraussetzung: Geringes Einkommen, angemessener Wohnraum. Höhe: Nach Einkommen, Haushaltsgröße, Belastung. Antrag: Bei Wohngeldstelle. Wichtig: Kann Hunderte Euro pro Monat bringen!""",
        "category": "Förderung",
        "subcategory": "Wohngeld"
    },
    {
        "title": "Baukindergeld: Abgeschafft",
        "content": """Baukindergeld: Förderung für Familien 2018-2021 (12.000€ pro Kind). Abschaffung: 2021 eingestellt. Ersatz: Keine direkte Förderung mehr für Eigenheimkauf mit Kindern. KfW: Nur noch über Energieeffizienz-Programme. Wichtig: Keine Neuzusagen mehr!""",
        "category": "Förderung",
        "subcategory": "Baukindergeld"
    },
    {
        "title": "Mietpreisbremse: Regelungen",
        "content": """Mietpreisbremse: Miete max. 10% über ortsüblicher Vergleichsmiete (in angespannten Märkten). Ausnahmen: Neubau (1. Bezug), Modernisierung (11%), vorherige Miete höher. Geltung: Großstädte mit Wohnungsknappheit. Rückforderung: Bis 30 Monate. Wichtig: Mietspiegel prüfen, Auskunft verlangen!""",
        "category": "Mietrecht",
        "subcategory": "Mietpreisbremse"
    },
    {
        "title": "Betreuungsvollmacht: Vorsorge",
        "content": """Betreuungsvollmacht: Regelt Verfügung über Immobilie bei Geschäftsunfähigkeit. Inhalt: Bevollmächtigter kann verkaufen/belasten. Form: Notariell. Wichtig: Vorsorge für Alter/Krankheit! Hinterlegung beim Notar empfohlen.""",
        "category": "Vorsorge",
        "subcategory": "Vollmacht"
    },
    {
        "title": "Smart Home: Wertsteigerung",
        "content": """Smart Home: Automatisierung Beleuchtung, Heizung, Sicherheit. Wertsteigerung: Moderate 3-5% bei hochwertiger Installation. Nachrüstung: 3.000-15.000€. Vorteil: Komfort, Energieersparnis. Wichtig: Standard-Systeme bevorzugen, keine Insellösungen!""",
        "category": "Modernisierung",
        "subcategory": "Smart Home"
    },
    {
        "title": "Altlasten: Haftung bei Grundstücken",
        "content": """Altlasten: Bodenkontamination durch frühere Nutzung (Tankstelle, Gewerbe). Haftung: Eigentümer haftet auch wenn er nicht Verursacher! Kosten: Sanierung 50.000-500.000€+. Schutz: Vor Kauf Bodengutachten, Altlastenkataster prüfen. Wichtig: Kann Grundstück unverkäuflich machen!""",
        "category": "Kaufrecht",
        "subcategory": "Altlasten"
    },
    {
        "title": "Erbbaurecht: Heimfall und Entschädigung",
        "content": """Heimfall: Gebäude fällt nach Erbbaurechts-Ende an Grundstückseigentümer. Entschädigung: 2/3 des Verkehrswertes üblich. Verlängerung: Oft möglich. Finanzierung: Banken finanzieren Erbbaurecht. Wichtig: Heimfall-Bedingungen im Vertrag prüfen!""",
        "category": "Erbbaurecht",
        "subcategory": "Heimfall"
    },
    {
        "title": "Airbnb: Rechtliche Lage",
        "content": """Airbnb kurzfristige Vermietung: Zweckentfremdung in vielen Städten genehmigungspflichtig. Berlin/München: Strenge Regelungen, Bußgelder bis 500.000€. WEG: Zustimmung erforderlich. Steuer: Einnahmen voll versteuern (Werbungskosten absetzbar). Wichtig: Rechtslage prüfen!""",
        "category": "Vermietung",
        "subcategory": "Kurzzeitvermietung"
    },
    {
        "title": "Ferienwohnung: Zweitwohnung Steuer",
        "content": """Ferienwohnung als Zweitwohnung: Zweitwohnungssteuer (2-15% Jahresnettokaltmiete). Befreiungen: Bei beruflicher Notwendigkeit. Vermietung: Reduziert Steuer (anteilig nach Eigennutzung). Wichtig: Vor Kauf Steuerhöhe bei Gemeinde erfragen!""",
        "category": "Steuerrecht",
        "subcategory": "Zweitwohnungssteuer"
    },
    {
        "title": "Leerstand: Kosten und Risiken",
        "content": """Leerstand: Keine Mieteinnahmen, aber laufende Kosten (Betriebskosten, Darle hensrate). Dauer: Durchschnitt 2-3 Monate bei Mieterwechsel. Kosten: 500-1.500€ pro Monat. Vermeidung: Gute Lage, faire Miete, professionelle Vermarktung. Wichtig: Rücklagen für Leerstand bilden!""",
        "category": "Vermietung",
        "subcategory": "Leerstand"
    }
]

print("🚀🚀🚀 FINAL SPRINT: LETZTE 100 ZUR 4.000! 🚀🚀🚀")
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
    print(f"\n🎯🎯🎯 GESAMT DOKUMENTE: {total} 🎯🎯🎯")
    if total >= 4000:
        print("🏆🏆🏆 *** 4.000 MEILENSTEIN ERREICHT!!! *** 🏆🏆🏆")
        print("🎉🎉🎉 HISTORISCHER ERFOLG! 🎉🎉🎉")
    else:
        remaining = 4000 - total
        print(f"📊 Noch {remaining} bis zur 4.000!")
except Exception as e:
    print(f"⚠️  Konnte Gesamtzahl nicht abrufen: {e}")

print("\n🔥🔥🔥 FINAL SPRINT COMPLETE! 🔥🔥🔥")
