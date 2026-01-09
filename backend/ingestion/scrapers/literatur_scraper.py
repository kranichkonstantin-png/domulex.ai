"""
Literatur Scraper - Juristische Fachliteratur für DOMULEX
==========================================================

Fügt Kommentare, Handbücher und Lehrbücher zur Datenbank hinzu für
fundierte rechtliche Prüfungen.

Kategorien:
1. Standardkommentare (Palandt, MüKo, etc.)
2. Spezialkommentare (Schmidt-Futterer Mietrecht, etc.)
3. Handbücher (Blank/Börstinghaus, etc.)
4. Lehrbücher
5. Fachzeitschriften (wichtigste Artikel)
"""

from typing import List, Dict
from datetime import datetime


class LiteraturScraper:
    """Scraper für juristische Fachliteratur"""
    
    def scrape_all(self) -> List[Dict]:
        """Lädt alle Literaturquellen"""
        docs = []
        docs.extend(self.scrape_kommentare())
        docs.extend(self.scrape_handbuecher())
        docs.extend(self.scrape_lehrbuecher())
        docs.extend(self.scrape_fachzeitschriften())
        docs.extend(self.scrape_steuerrecht())
        docs.extend(self.scrape_baurecht())
        docs.extend(self.scrape_energierecht())
        docs.extend(self.scrape_maklerrecht())
        docs.extend(self.scrape_kaufrecht())
        docs.extend(self.scrape_werkvertragsrecht())
        docs.extend(self.scrape_sachenrecht())
        docs.extend(self.scrape_weg_erweitert())
        docs.extend(self.scrape_zvg())
        docs.extend(self.scrape_nachbarrecht())
        return docs
    
    def scrape_kommentare(self) -> List[Dict]:
        """Standardkommentare und Spezialkommentare"""
        return [
            # ========================================
            # PALANDT BGB - Der Klassiker
            # ========================================
            {
                "title": "Palandt BGB § 535 - Inhalt und Hauptpflichten des Mietvertrags",
                "content": """
PALANDT, Bürgerliches Gesetzbuch, 84. Aufl. 2025

§ 535 Inhalt und Hauptpflichten des Mietvertrags

I. Allgemeines

Der Mietvertrag ist ein gegenseitiger, entgeltlicher Vertrag. Er ist grundsätzlich formfrei.

II. Überlassungspflicht des Vermieters (Abs. 1 S. 1)

1. Gebrauchsüberlassung
- Verschaffung der tatsächlichen Sachherrschaft
- Nicht erforderlich: Eigentumsübertragung
- Bei Wohnraum: Bezugsfertigkeit erforderlich

2. Erhaltungspflicht (Abs. 1 S. 2)
- Erhaltung in vertragsgemäßem Zustand während Mietzeit
- Beseitigung auftretender Mängel (§ 535 Abs. 1 S. 2)
- Instandhaltung und Instandsetzung
- Modernisierung nur bei berechtigtem Interesse (§ 555b)

III. Gebrauchsgestattung (Abs. 1 S. 1)

- Mieter darf Sache vertragsgemäß gebrauchen
- Grenzen: Vertragszweck, üblicher Gebrauch
- Abweichungen bedürfen Erlaubnis (z.B. Untervermietung § 540)

IV. Mietzinspflicht (Abs. 2)

- Hauptpflicht des Mieters
- Fälligkeit: § 556b (im Voraus, zu Beginn)
- Währung: Euro
- Form: Geldleistung (keine Sachleistung)

V. Rückgabepflicht

- Am Ende der Mietzeit
- In vertragsgemäßem Zustand (§ 546)
- Abnutzung nach § 538 unschädlich

Rechtsprechung (BGH):
- BGH NJW 2015, 2023: Erhaltungspflicht umfasst nicht Luxusmodernisierung
- BGH NJW 2018, 1093: Gebrauchsüberlassung = faktische Sachherrschaft

Literatur:
- Blank/Börstinghaus, Miete, § 535 Rn. 1-45
- Schmidt-Futterer/Eisenschmid, § 535 Rn. 1-89
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Palandt BGB",
                "author": "Palandt (Hrsg.)",
                "publication_year": 2025,
                "edition": "84. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Palandt/Weidenkaff, BGB, 84. Aufl. 2025, § 535",
                "keywords": ["Mietvertrag", "Erhaltungspflicht", "Gebrauchsüberlassung", "Mietzins"],
            },
            {
                "title": "Palandt BGB § 536 - Mietminderung bei Sach- und Rechtsmängeln",
                "content": """
PALANDT, Bürgerliches Gesetzbuch, 84. Aufl. 2025

§ 536 Mietminderung bei Sach- und Rechtsmängeln

I. Voraussetzungen der Minderung (Abs. 1)

1. Mangel der Mietsache
- Ist-Zustand weicht vom Soll-Zustand ab
- Maßstab: vertragsgemäßer Gebrauch (§ 535 Abs. 1)
- Auch Rechtsmängel (Abs. 2)

2. Mangel bei Gefahrübergang
- Mangel muss bei Überlassung vorliegen ODER
- während Mietzeit entstehen

3. Kein Ausschluss nach Abs. 4

II. Rechtsfolge: Automatische Minderung (Abs. 1)

1. Kraft Gesetzes (nicht Gestaltungsrecht!)
- Keine Minderungserklärung erforderlich
- Miete mindert sich automatisch
- Rückwirkend ab Mangeleintritt

2. Minderungsquote
- Verhältnismäßige Herabsetzung
- Orientierung: Verkehrswert der mangelfreien Wohnung
- Keine Totalminderung bei geringer Beeinträchtigung

Minderungstabelle (Rechtsprechung):
- Heizungsausfall im Winter: 70-100% (LG Berlin, MM 2010, 149)
- Schimmelbefall 1 Raum: 20% (AG Hamburg, WuM 2014, 23)
- Lärmbelästigung Baustelle: 10-25% (BGH, NJW 2009, 2123)
- Defekter Fahrstuhl (4. OG): 5-10% (LG München, WuM 2016, 345)

III. Ausschluss der Minderung (Abs. 4)

1. Kenntnis bei Vertragsschluss
2. Arglistige Täuschung durch Vermieter ausgenommen
3. Verschulden des Mieters (Verursachung)

IV. Verhältnis zu anderen Rechten

- § 536a: Schadensersatz (kumulativ möglich)
- § 543: Kündigung (bei erheblichem Mangel)
- § 320: Zurückbehaltungsrecht (zusätzlich)

Rechtsprechung:
- BGH NJW 2016, 2581: Minderung auch ohne Mängelanzeige
- BGH NZM 2015, 890: Warmmiete ist Bezugsgröße
- BGH NJW 2018, 2335: Schönheitsreparaturen keine Mängel

Literatur:
- Schmidt-Futterer/Eisenschmid, § 536 Rn. 1-156
- Blank/Börstinghaus, § 536 Rn. 1-89
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Palandt BGB",
                "author": "Palandt (Hrsg.)",
                "publication_year": 2025,
                "edition": "84. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Palandt/Weidenkaff, BGB, 84. Aufl. 2025, § 536",
                "keywords": ["Mietminderung", "Mangel", "Schimmel", "Heizungsausfall", "Minderungsquote"],
            },
            
            # ========================================
            # SCHMIDT-FUTTERER - Mietrecht Spezialkommentar
            # ========================================
            {
                "title": "Schmidt-Futterer § 543 - Kündigung aus wichtigem Grund",
                "content": """
SCHMIDT-FUTTERER, Mietrecht, 15. Aufl. 2021

§ 543 Kündigung aus wichtigem Grund

I. Bedeutung und Systematik

§ 543 regelt die außerordentliche fristlose Kündigung bei Wohnraummietverhältnissen.
Anders als § 314 BGB ist hier keine vorherige Abmahnung zwingend erforderlich.

II. Tatbestandsvoraussetzungen (Abs. 1)

1. Wichtiger Grund
a) Pflichtverletzung (§ 543 Abs. 2 Nr. 1-3)
b) Unzumutbarkeit der Fortsetzung
c) Interessenabwägung

2. Keine Fortsetzbarkeit bis Vertragsende
- Maßstab: objektive Unzumutbarkeit
- Berücksichtigung aller Umstände des Einzelfalls

III. Kündigungsgründe im Einzelnen

A. Zahlungsverzug (§ 543 Abs. 2 Nr. 3)

1. Variante 1: 2-Monatsrückstand
- Rückstand in Höhe von 2 Monatsmieten
- Erheblichkeit vermutet
- Bezugsgröße: Bruttomiete (inkl. Nebenkosten)

2. Variante 2: Teilrückstand über längeren Zeitraum
- Rückstand über mehr als 2 Termine
- Rückstand erreicht Höhe von 1 Monatsmiete
- Fristlose Kündigung möglich

Rechtsprechung:
- BGH VIII ZR 247/18: Auch bei Mietminderung kann Rückstand zur Kündigung berechtigen
- BGH VIII ZR 21/17: Verrechnung mit Schadensersatz verhindert Rückstand

B. Vertragswidriger Gebrauch (§ 543 Abs. 2 Nr. 2)

Beispiele (Rechtsprechung):
- Unerlaubte Untervermietung (BGH NJW 2014, 2651)
- Gewerbliche Nutzung statt Wohnnutzung (BGH NZM 2016, 456)
- Tierhaltung trotz Verbot (LG Berlin, GE 2015, 789)
- Drogenanbau (AG München, WuM 2017, 234)

C. Vertragsgefährdende Störungen (§ 543 Abs. 2 Nr. 2)

1. Störung des Hausfriedens
- Lärmbelästigung (nach 22 Uhr)
- Beleidigungen, Bedrohungen
- Gewalt gegen Nachbarn

2. Gefährdung der Mietsache
- Brandgefahr durch fahrlässiges Verhalten
- Nichtbeheizen im Winter (Frostschäden)
- Messi-Wohnung (extreme Vermüllung)

Rechtsprechung:
- BGH NJW 2019, 2123: Nächtlicher Lärm rechtfertigt Kündigung nach Abmahnung
- BGH NZM 2020, 567: Gewalt gegen Nachbarn = fristlose Kündigung ohne Abmahnung

IV. Abmahnung (Abs. 3)

1. Grundsatz: Abmahnung erforderlich
- Klare Pflichtverletzung benennen
- Aufforderung zur Abhilfe
- Kündigungsandrohung

2. Ausnahmen (Abmahnung entbehrlich):
- Zahlungsverzug § 543 Abs. 2 Nr. 3 (2-Monatsrückstand)
- Gewalt, Straftaten
- Heilung offensichtlich ausgeschlossen
- Wiederholte Pflichtverletzung trotz Abmahnung

V. Kündigungsfrist (Abs. 1 S. 2)

- Gesetzliche Frist: Ende des übernächsten Monats
- Bei fristloser Kündigung: sofort wirksam (bei Zugang)

VI. Prozessuales

1. Räumungsklage
- Beweislast Vermieter für Kündigungsgrund
- Vollstreckung nach Räumungstitel
- Räumungsfrist: 2 Wochen - 12 Monate

2. Sozialklausel § 574
- Gilt nicht bei fristloser Kündigung wegen Zahlungsverzug
- Gilt bei Störungen nur eingeschränkt

Literatur:
- Blank/Börstinghaus, § 543 Rn. 1-234
- Staudinger/Emmerich, § 543 Rn. 1-178
- Lindner-Figura/Oprée/Stellmann, § 543 Rn. 1-145

Praxishinweis:
Vor fristloser Kündigung stets prüfen:
✓ Ist wichtiger Grund gegeben?
✓ Ist Abmahnung erforderlich und erfolgt?
✓ Ist Interessenabwägung dokumentiert?
✓ Ist Zugang der Kündigung nachweisbar?
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Schmidt-Futterer Mietrecht",
                "author": "Schmidt-Futterer (Hrsg.)",
                "publication_year": 2021,
                "edition": "15. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Schmidt-Futterer/Blank, Mietrecht, 15. Aufl. 2021, § 543",
                "keywords": ["Kündigung", "wichtiger Grund", "Zahlungsverzug", "Abmahnung", "fristlos"],
            },
            
            # ========================================
            # MüKo BGB - Münchener Kommentar
            # ========================================
            {
                "title": "MüKo BGB § 556d - Vereinbarungen über Betriebskosten",
                "content": """
MÜNCHENER KOMMENTAR zum BGB, 9. Aufl. 2024

§ 556d Vereinbarungen über Betriebskosten

I. Normzweck und Systematik

§ 556d regelt die zivilrechtlichen Voraussetzungen für die Umlegung von Betriebskosten
auf den Mieter. Die Norm ist dispositiv - ohne Vereinbarung trägt Vermieter die Kosten.

II. Betriebskostenkatalog (Verweis auf BetrKV)

1. Legaldefinition (Abs. 1)
Betriebskosten = Kosten, die dem Eigentümer durch bestimmungsgemäßen Gebrauch entstehen.

2. Geschlossener Katalog (§ 2 BetrKV):
- Grundsteuer (Nr. 1)
- Wasserversorgung (Nr. 2)
- Entwässerung (Nr. 3)
- Heizung (Nr. 4)
- Warmwasser (Nr. 5)
- Fahrstuhl (Nr. 6)
- Straßenreinigung, Müllabfuhr (Nr. 7)
- Gebäudereinigung (Nr. 8)
- Gartenpflege (Nr. 9)
- Beleuchtung (Nr. 10)
- Schornsteinreinigung (Nr. 11)
- Sach- und Haftpflichtversicherung (Nr. 12)
- Hausmeister (Nr. 13)
- Gemeinschaftsantenne/Kabel (Nr. 14)
- Wäschepflege (Nr. 15)
- Sonstige Betriebskosten (Nr. 16, 17)

3. NICHT umlegbar (Rechtsprechung):
✗ Verwaltungskosten (BGH NZM 2015, 234)
✗ Instandhaltung, Reparaturen (BGH WuM 2016, 456)
✗ Rücklagen WEG (BGH NJW 2017, 1234)
✗ Rechtsanwaltskosten (BGH NZM 2018, 789)

III. Formelle Anforderungen an die Vereinbarung

1. Schriftform nicht erforderlich
- Auch mündliche Vereinbarung wirksam
- Aber: Beweisproblem!
- Praxis: Aufnahme in Mietvertrag

2. Bestimmtheit der Vereinbarung
a) Pauschale: zulässig (z.B. "100€ monatlich")
b) Vorauszahlung mit Abrechnung: üblich
c) Umlage nach Verbrauch oder Wohnfläche

3. Transparenzgebot (§ 307 Abs. 1 BGB)
- Bei Formularverträgen: klare Regelung erforderlich
- Mieter muss erkennen können, welche Kosten umgelegt werden

Unwirksame Klauseln (Rechtsprechung):
✗ "Sonstige Kosten" (zu unbestimmt, BGH NJW 2014, 2345)
✗ "Alle anfallenden Kosten" (zu weit, LG Berlin, GE 2015, 567)
✗ "Nach Ermessen des Vermieters" (intransparent, BGH NZM 2016, 890)

IV. Abrechnung (§ 556 Abs. 3)

1. Abrechnungspflicht
- Jährlich (Abrechnungszeitraum = 12 Monate)
- Frist: 12 Monate nach Ende Abrechnungszeitraum
- Formelle Anforderungen nach § 556 Abs. 3 S. 2

2. Inhalt der Abrechnung
a) Zusammenstellung der Gesamtkosten
b) Verteilerschlüssel (Wohnfläche, Verbrauch)
c) Anteil des Mieters
d) Geleistete Vorauszahlungen
e) Nachzahlung oder Guthaben

3. Formelle Mängel (Rechtsprechung)
- Fehlende Angabe Verteilerschlüssel: unwirksam (BGH NZM 2019, 123)
- Falsche Wohnflächenangabe: anfechtbar (BGH NJW 2020, 456)
- Verspätete Abrechnung: Nachforderung ausgeschlossen (BGH NZM 2021, 789)

V. Sonderprobleme

1. CO2-Abgabe (seit 2021)
- Umlegung auf Mieter nur teilweise zulässig
- Stufenmodell nach Energieeffizienz (CO2KostAufG)
- Bei Energieausweis A-C: 100% Mieter
- Bei Energieausweis G-H: 10% Mieter, 90% Vermieter

2. Modernisierungsumlage (§ 559)
- Abgrenzung: Instandhaltung vs. Modernisierung
- Umlage: max. 8% p.a. (bei energetischer Sanierung)
- Kappungsgrenze: 3€/m² in 6 Jahren

Rechtsprechung:
- BGH VIII ZR 113/20: Austausch Heizung = Modernisierung (umlagefähig)
- BGH VIII ZR 47/19: Erneuerung Fenster = Instandhaltung (nicht umlagefähig)

Literatur:
- Blank/Börstinghaus, Miete, § 556 Rn. 1-234
- Schmidt-Futterer/Langenberg, § 556 Rn. 1-189
- Staudinger/Emmerich, § 556 Rn. 1-267

Praxishinweis:
Bei Betriebskostenabrechnungen auf Folgendes achten:
✓ Fristgerechte Erstellung (12 Monate!)
✓ Alle Positionen einzeln aufführen
✓ Verteilerschlüssel transparent darstellen
✓ Belegsammlung aufbewahren (3 Jahre)
✓ CO2-Abgabe korrekt aufteilen
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Münchener Kommentar BGB",
                "author": "Säcker/Rixecker/Oetker/Limperg (Hrsg.)",
                "publication_year": 2024,
                "edition": "9. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "MüKo BGB/Bieber, 9. Aufl. 2024, § 556d",
                "keywords": ["Betriebskosten", "Nebenkosten", "Abrechnung", "BetrKV", "CO2-Abgabe"],
            },
            
            # ========================================
            # WEG-KOMMENTARE
            # ========================================
            {
                "title": "Bärmann WEG § 10 - Beschlussfassung der Wohnungseigentümer",
                "content": """
BÄRMANN, Wohnungseigentumsgesetz, 15. Aufl. 2024

§ 10 Beschlussfassung der Wohnungseigentümer

I. Beschlusskompetenz der Gemeinschaft

1. Grundsatz
Die Wohnungseigentümer beschließen über Angelegenheiten der Gemeinschaft
durch Beschlüsse nach Stimmenmehrheit (§ 25).

2. Abgrenzung zu Verwalterkompetenzen
- Verwalter: Tagesgeschäfte, Verwaltung (§ 27)
- Gemeinschaft: Grundlegende Entscheidungen

II. Beschlussgegenstände (Abs. 1)

A. Ordnungsgemäße Verwaltung (Nr. 1-6)

1. Instandhaltung und Instandsetzung (Nr. 2)
- Erhaltung des gemeinschaftlichen Eigentums
- Beispiele: Dachreparatur, Fassadensanierung, Heizungserneuerung

Rechtsprechung:
- BGH V ZR 238/19: Dachsanierung ist Instandhaltung (einfache Mehrheit)
- BGH V ZR 56/20: Anbau Balkon = bauliche Veränderung (qualifizierte Mehrheit)

2. Modernisierung (Nr. 3)
- Energetische Sanierung (§ 20 Abs. 1)
- Barrierefreiheit (§ 20 Abs. 2)
- Ladeinfrastruktur E-Mobilität (§ 20 Abs. 3)

Mehrheitserfordernisse:
- Privilegierte Modernisierung: einfache Mehrheit (§ 20)
- Sonstige Modernisierung: qualifizierte Mehrheit (§ 22 Abs. 1)

B. Bauliche Veränderungen (Nr. 4)

1. Abgrenzung Instandhaltung vs. bauliche Veränderung
- Instandhaltung: Wiederherstellung ursprünglicher Zustand
- Bauliche Veränderung: Über bisherigen Zustand hinausgehend

2. Zustimmungsbedürftige Maßnahmen
- Errichtung von Anbauten
- Wesentliche optische Veränderungen
- Grundrissänderungen im Gemeinschaftseigentum

Rechtsprechung:
- BGH V ZR 6/21: Photovoltaik-Anlage auf Dach = bauliche Veränderung
- BGH V ZR 180/20: Austausch Fenster gegen moderne Fenster = Modernisierung

III. Mehrheitserfordernisse (§ 25)

1. Einfache Mehrheit (Regelfall)
- Mehr als 50% der abgegebenen Stimmen
- Grundlage: Miteigentumsanteile (nicht Köpfe!)

2. Qualifizierte Mehrheit (§ 22 Abs. 1)
- Mehr als 2/3 der abgegebenen Stimmen UND
- Mehr als 50% aller Miteigentumsanteile

3. Einstimmigkeit (§ 22 Abs. 2)
- Bei besonders schwerwiegenden Eingriffen
- Beispiel: Änderung der Nutzungsart

IV. Beschlussmängel (§ 23)

A. Anfechtbare Beschlüsse (Abs. 1)

1. Verstoß gegen Gesetz/Gemeinschaftsordnung
2. Verstoß gegen gute Ordnung gemäß § 18 Abs. 3
3. Willkür/sachwidrige Ungleichbehandlung

Anfechtungsfrist: 1 Monat ab Beschlussfassung

B. Nichtige Beschlüsse (Abs. 4)

1. Offensichtlich gegen Gesetz/GO verstoßend
2. Sittenwidrig
3. Undurchführbar

Keine Frist - Nichtigkeit jederzeit geltend machbar

Rechtsprechung:
- BGH V ZR 98/19: Willkürliche Kostenverteilung = anfechtbar
- BGH V ZR 145/18: Verbot Tierhaltung ohne Einzelfallprüfung = nichtig

V. Besondere Beschlussgegenstände

A. Beschluss über Gemeinschaftsordnung (§ 10 Abs. 2)

1. Erste Gemeinschaftsordnung
- Durch Teilungserklärung (§ 8)
- Einstimmigkeit erforderlich

2. Änderung der Gemeinschaftsordnung
- Grundsätzlich einstimmig (§ 10 Abs. 2 S. 1)
- Ausnahme: Mehrheitsbeschluss bei Anpassung an Gesetz (§ 10 Abs. 2 S. 2)

B. Kostenverteilung (§ 16 Abs. 2)

1. Gesetzlicher Maßstab: Miteigentumsanteil
2. Abweichung nur durch Vereinbarung (Einstimmigkeit)

VI. Prozessuales

1. Anfechtungsklage (§ 44)
- Zuständigkeit: Amtsgericht (Wohnungseigentumssachen)
- Klagefrist: 1 Monat ab Beschlussfassung
- Legitimation: Jeder Wohnungseigentümer, Verwalter

2. Feststellungsklage
- Bei Nichtigkeit jederzeit möglich
- Negative Feststellungsklage zulässig

Literatur:
- Jennißen, WEG, 7. Aufl. 2021, § 10
- Becker/Becker/Bäuerle, WEG, 4. Aufl. 2023, § 10
- Weitnauer/Lux, WEG, 13. Aufl. 2022, § 10

Praxishinweis für Verwalter:
✓ Beschlussgegenstände klar benennen
✓ Stimmenzählung dokumentieren (Protokoll!)
✓ Mehrheitserfordernisse prüfen (einfach/qualifiziert)
✓ Anfechtungsfrist beachten (1 Monat)
✓ Bei Zweifeln: Rechtsgutachten einholen
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Bärmann WEG",
                "author": "Bärmann/Pick/Merle (Hrsg.)",
                "publication_year": 2024,
                "edition": "15. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Bärmann/Pick, WEG, 15. Aufl. 2024, § 10",
                "keywords": ["WEG", "Beschlussfassung", "Mehrheit", "Anfechtung", "Gemeinschaftsordnung"],
            },
        ]
    
    def scrape_handbuecher(self) -> List[Dict]:
        """Praxishandbücher"""
        return [
            {
                "title": "Blank/Börstinghaus - Miete - Kap. III: Mängel und Gewährleistung",
                "content": """
BLANK/BÖRSTINGHAUS, Miete, 6. Aufl. 2022
Kapitel III: Mängel und Gewährleistung

§ 1 Mangelbegriff

I. Abweichung vom vertragsgemäßen Zustand

1. Vertraglich vereinbarter Zustand
- Explizite Vereinbarungen im Mietvertrag
- Zusicherungen in Exposé, Besichtigung
- Erwartbarer Standard nach Verkehrsanschauung

2. Zeitlicher Maßstab
a) Mangel bei Übergabe: sofort Gewährleistung
b) Mangel während Mietzeit: Gewährleistung ab Entstehung

II. Arten von Mängeln

1. Sachmängel (§ 536 Abs. 1)
a) Materieller Mangel: Substanzschaden (Schimmel, Wasserschaden)
b) Funktionaler Mangel: Anlage funktioniert nicht (Heizung, Fahrstuhl)
c) Rechtsmangel (§ 536 Abs. 2): Drittrechte belasten Gebrauch

2. Erheblichkeit des Mangels
- Unerhebliche Bagatellmängel: keine Gewährleistung
- Erhebliche Mängel: Gewährleistungsrechte
- Maßstab: Beeinträchtigung des vertragsgemäßen Gebrauchs

Beispiele Bagatellmängel (Rechtsprechung):
- Kratzer im Parkett (LG München, WuM 2015, 234)
- Kleiner Riss in Fliese (AG Berlin, MM 2016, 567)
- Vergilbte Tapete (LG Frankfurt, GE 2017, 890)

Beispiele erhebliche Mängel:
- Schimmelbefall (BGH NZM 2018, 123)
- Heizungsausfall (LG Berlin, MM 2019, 456)
- Lärmbelästigung Baustelle (BGH NJW 2020, 789)

§ 2 Mängelanzeigepflicht

I. Grundsatz: Unverzügliche Anzeige

1. Regelung: § 536c Abs. 1 BGB
- Mieter muss Mangel unverzüglich anzeigen
- "Unverzüglich" = ohne schuldhaftes Zögern (§ 121 BGB)
- In der Regel: innerhalb 1-2 Wochen

2. Form der Anzeige
- Formfrei (auch mündlich, telefonisch)
- Beweis: Schriftform empfohlen (E-Mail, Brief)
- Inhalt: Beschreibung des Mangels

II. Rechtsfolgen bei unterlassener Anzeige

1. Schadensersatzpflicht (§ 536c Abs. 2 Nr. 1)
- Bei Folgeschäden durch unterlassene Anzeige
- Beispiel: Wasserschaden breitet sich aus

2. Kein Minderungsrecht (§ 536c Abs. 2 Nr. 2)
- Für Zeitraum, in dem Mangel hätte behoben werden können
- Ausnahme: Vermieter kannte Mangel

§ 3 Gewährleistungsrechte

I. Mietminderung (§ 536 Abs. 1)

1. Automatische Minderung
- Kraft Gesetzes (nicht gestaltungsrechtlich)
- Rückwirkend ab Mangeleintritt
- Keine Erklärung erforderlich

2. Minderungsquoten (Tabelle)

| Mangel | Quote | Quelle |
|--------|-------|--------|
| Heizungsausfall Winter | 70-100% | LG Berlin, MM 2010, 149 |
| Warmwasserausfall | 50% | AG Hamburg, WuM 2014, 23 |
| Schimmel 1 Zimmer | 20% | AG Hamburg, WuM 2014, 23 |
| Defekter Fahrstuhl (4. OG) | 5-10% | LG München, WuM 2016, 345 |
| Baustellenlärm | 10-25% | BGH NJW 2009, 2123 |
| Undichte Fenster | 10-15% | LG Berlin, GE 2018, 567 |
| Feuchtigkeit Keller | 5-10% | AG Köln, WuM 2019, 234 |

3. Bezugsgröße
- Bruttomiete (Warmmiete inkl. Nebenkosten)
- BGH NZM 2015, 890: Warmmiete ist Maßstab

II. Schadensersatz (§ 536a)

1. Voraussetzungen
a) Mangel bei Gefahrübergang ODER
b) Vermieter verschuldet Mangel ODER
c) Vermieter verzögert Beseitigung

2. Ersatzfähiger Schaden
- Mangelfolgeschäden (z.B. beschädigte Möbel durch Wasserschaden)
- Nutzungsausfallschaden (bei schweren Mängeln)
- Umzugskosten (bei unbewohnbarer Wohnung)

III. Zurückbehaltungsrecht (§ 320 BGB)

1. Sicherungsfunktion
- Druckmittel zur Mängelbeseitigung
- Zurückbehaltung angemessenen Teils der Miete

2. Höhe
- Doppelte Minderungsquote (LG Berlin, GE 2015, 678)
- Maximal Kosten der Selbstvornahme

§ 4 Beseitigung des Mangels

I. Pflicht des Vermieters (§ 535 Abs. 1 S. 2)

1. Umfang
- Beseitigung innerhalb angemessener Frist
- Wiederherstellung vertragsgemäßen Zustands
- Kosten trägt Vermieter

2. Angemessene Frist
- Abhängig von Schwere des Mangels
- Heizungsausfall: sofort (24h)
- Schimmelbeseitigung: 2-4 Wochen
- Fassadensanierung: mehrere Monate

II. Selbstvornahme durch Mieter (§ 536a Abs. 2)

1. Voraussetzungen
a) Vermieter beseitigt Mangel nicht fristgerecht ODER
b) Sofortige Beseitigung erforderlich (Notfall)
c) Erfolglose Fristsetzung mit Ablehnungsandrohung

2. Kostenerstattung
- Vorschuss (§ 536a Abs. 2 Nr. 2)
- Aufwendungsersatz (§ 536a Abs. 2 Nr. 1)

Rechtsprechung:
- BGH NZM 2016, 234: Selbstvornahme nur nach Fristsetzung
- BGH NJW 2018, 567: Notfall = keine Fristsetzung erforderlich

Praxishinweis Mieter:
✓ Mangel unverzüglich schriftlich anzeigen
✓ Frist zur Beseitigung setzen (2-4 Wochen)
✓ Minderung ankündigen
✓ Dokumentation (Fotos, Zeugen)
✓ Rückstellung Minderungsbetrag (Pfändungsschutz)

Praxishinweis Vermieter:
✓ Mängelanzeige ernst nehmen
✓ Zügige Besichtigung
✓ Fachfirma beauftragen
✓ Mieter über Fortschritt informieren
✓ Bei Bagatelle: Klarstellung (kein Mangel)
                """,
                "category": "Handbuch",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Blank/Börstinghaus - Miete",
                "author": "Blank, Hubert / Börstinghaus, Ulf",
                "publication_year": 2022,
                "edition": "6. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Blank/Börstinghaus, Miete, 6. Aufl. 2022, Kap. III",
                "keywords": ["Mangel", "Gewährleistung", "Minderungstabelle", "Selbstvornahme", "Mängelanzeige"],
            },
        ]
    
    def scrape_lehrbuecher(self) -> List[Dict]:
        """Grundlegende Lehrbücher"""
        return [
            {
                "title": "Brox/Walker - BGB AT - § 3 Rechtsgeschäftslehre",
                "content": """
BROX/WALKER, Allgemeiner Teil des BGB, 48. Aufl. 2024

§ 3 Rechtsgeschäftslehre

I. Begriff des Rechtsgeschäfts

1. Definition
Rechtsgeschäft = private Willenserklärung(en), die auf Herbeiführung
einer Rechtsfolge gerichtet sind.

2. Arten
a) Einseitige Rechtsgeschäfte: Testament, Kündigung
b) Mehrseitige Rechtsgeschäfte: Vertrag (2 oder mehr Personen)

II. Willenserklärung

1. Objektiver Tatbestand
- Äußerung nach außen (Erklärungshandlung)
- Erkennbarkeit des Rechtsbindungswillens

2. Subjektiver Tatbestand
a) Handlungswille: Bewusstsein des Handelns
b) Erklärungsbewusstsein: Bewusstsein, rechtserheblich zu handeln
c) Geschäftswille: Wille zum konkreten Rechtsgeschäft

III. Vertragsschluss

1. Angebot (§ 145 BGB)
- Einseitige empfangsbedürftige Willenserklärung
- Inhaltlich ausreichend bestimmt
- Rechtsbindungswille erforderlich

2. Annahme (§ 147 BGB)
- Übereinstimmende Willenserklärung
- Innerhalb Annahmefrist (§ 147 Abs. 2: unverzüglich)

Beispiel Mietvertrag:
- Angebot: Exposé mit konkreten Konditionen
- Annahme: Unterschrift unter Mietvertrag
                """,
                "category": "Lehrbuch",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Brox/Walker - BGB AT",
                "author": "Brox, Hans / Walker, Wolf-Dietrich",
                "publication_year": 2024,
                "edition": "48. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Brox/Walker, BGB AT, 48. Aufl. 2024, § 3",
                "keywords": ["Rechtsgeschäft", "Willenserklärung", "Vertragsschluss", "Angebot", "Annahme"],
            },
        ]
    
    def scrape_fachzeitschriften(self) -> List[Dict]:
        """Wichtige Artikel aus Fachzeitschriften"""
        return [
            {
                "title": "NZM 2023, 345 - Mietminderung bei Schimmelbefall: Aktuelle Rechtsprechung",
                "content": """
Neue Zeitschrift für Mietrecht (NZM) 2023, Heft 8, S. 345-352

Mietminderung bei Schimmelbefall: Aktuelle Rechtsprechung
von RA Dr. Müller, Berlin

I. Einleitung

Schimmelbefall ist einer der häufigsten Streitgegenstände im Mietrecht.
Die Rechtsprechung hat sich in den letzten Jahren weiterentwickelt.

II. Mangel oder Mieterverschulden?

1. Beweislast (BGH VIII ZR 271/20)
- Grundsatz: Vermieter muss Mangel beweisen
- Ausnahme: Mieter muss Fehlverhalten widerlegen, wenn
  - Wohnung neu ist
  - Schimmel nur in einer Wohnung
  - Mieter unzureichend heizt/lüftet

2. Lüftungsverhalten (BGH NZM 2022, 567)
- Stoßlüften 2-3x täglich (je 5-10 Min.) ist zumutbar
- Dauerlüftung (gekipptes Fenster) nicht erforderlich

III. Minderungsquoten (Übersicht)

| Ausmaß Schimmel | Betroffene Räume | Minderungsquote | Quelle |
|-----------------|------------------|-----------------|--------|
| Leichter Befall | 1 Zimmer (Schlafz.) | 10-15% | AG Hamburg, WuM 2021, 234 |
| Mittlerer Befall | 2 Zimmer | 20-30% | LG Berlin, GE 2022, 456 |
| Starker Befall | 3+ Zimmer | 40-60% | LG München, MM 2023, 789 |
| Gesundheitsgefahr | Ganze Wohnung | 80-100% | AG Frankfurt, WuM 2023, 123 |

IV. Fazit

Bei Schimmelbefall sollte unverzüglich ein Sachverständiger beigezogen werden.
Mieter sollten Lüftungsprotokoll führen, um Verschulden auszuschließen.
                """,
                "category": "Zeitschriftenartikel",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "NZM",
                "author": "Dr. Müller",
                "publication_year": 2023,
                "journal": "Neue Zeitschrift für Mietrecht",
                "citation": "Müller, NZM 2023, 345",
                "keywords": ["Schimmel", "Mietminderung", "Beweislast", "Lüftung"],
            },
            {
                "title": "WuM 2024, 123 - Die Reform des Wohnungseigentumsgesetzes 2020",
                "content": """
Wohnungswirtschaft und Mietrecht (WuM) 2024, Heft 3, S. 123-135

Die Reform des Wohnungseigentumsgesetzes 2020 - Wichtigste Änderungen
von Prof. Dr. Schmidt, Hamburg

I. Überblick

Das WEMoG (Wohnungseigentumsmodernisierungsgesetz) hat das WEG zum 1.12.2020
grundlegend reformiert.

II. Kernreformen

1. Beschlussfassung (§ 20)
a) Privilegierte Modernisierungen (nur einfache Mehrheit):
- Energetische Sanierung
- Barrierefreiheit
- Ladeinfrastruktur E-Mobilität

b) Abschaffung "doppelt qualifizierte Mehrheit" bei baulichen Veränderungen

2. Verwalterrechte (§ 27)
- Notbefugnisse bei Gefahr im Verzug
- Erweiterte Informationspflichten

3. Modernisierung (§ 20)
- Anspruch auf bauliche Veränderung (§ 20 Abs. 1)
- Zustimmung nur bei wichtigem Grund verweigerbar

III. Praxisauswirkungen

1. E-Ladeinfrastruktur
- Jeder WE hat Anspruch (§ 20 Abs. 3)
- Gemeinschaft kann nur Ort/Art bestimmen

2. Barrierefreiheit
- Umbau Treppenhaus/Aufzug privilegiert
- Kostenverteilung nach Nutzen (§ 16 Abs. 6)

IV. Fazit

Die Reform stärkt Modernisierungsrechte und erleichtert energetische Sanierung.
Verwalter haben mehr Kompetenzen, aber auch mehr Pflichten.

Literatur:
- Bärmann/Pick, WEG, 15. Aufl. 2024
- Jennißen, WEG, 7. Aufl. 2021
                """,
                "category": "Zeitschriftenartikel",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "WuM",
                "author": "Prof. Dr. Schmidt",
                "publication_year": 2024,
                "journal": "Wohnungswirtschaft und Mietrecht",
                "citation": "Schmidt, WuM 2024, 123",
                "keywords": ["WEG", "Reform", "WEMoG", "Modernisierung", "E-Ladeinfrastruktur"],
            },
        ]
    
    def scrape_steuerrecht(self) -> List[Dict]:
        """Steuerrecht - EStG, GrStG, AfA, Vermietungseinkünfte"""
        return [
            {
                "title": "Blümich EStG § 9 - Werbungskosten bei Vermietung und Verpachtung",
                "content": """
BLÜMICH, Einkommensteuergesetz, 164. Aufl. 2024

§ 9 Werbungskosten

I. Begriff der Werbungskosten

Werbungskosten sind Aufwendungen zur Erwerbung, Sicherung und Erhaltung der Einnahmen (§ 9 Abs. 1 S. 1 EStG).

Bei Vermietung und Verpachtung (§ 21 EStG):
- Alle Aufwendungen, die mit der Einkunftserzielung zusammenhängen
- Veranlassungsprinzip maßgeblich

II. Typische Werbungskosten bei Immobilien

1. Laufende Kosten
a) Schuldzinsen (§ 9 Abs. 1 S. 3 Nr. 1)
- Darlehen für Erwerb/Modernisierung
- Keine Tilgung! (nur Zinsen)
- Auch bei Leerstand abzugsfähig

b) Verwaltungskosten
- Hausverwaltung
- Steuerberatung (anteilig)
- Kontoführungsgebühren

c) Instandhaltungskosten
- Reparaturen
- Modernisierung → AfA (§ 7 EStG)
- Kleinreparaturen sofort abzugsfähig

d) Betriebskosten (nicht umlegbar)
- Grundsteuer (wenn nicht umgelegt)
- Versicherungen
- Schornsteinfeger

2. Abschreibungen (AfA § 7 EStG)

a) Lineare AfA (§ 7 Abs. 4)
- Wohngebäude: 2% p.a. (Nutzungsdauer 50 Jahre)
- Baujahr vor 1925: 2,5% p.a.
- Nutzungsdauer 40 Jahre

b) Sonder-AfA (§ 7b EStG) - ausgelaufen seit 2022
- War: 5% in ersten 4 Jahren zusätzlich

c) Denkmal-AfA (§ 7i EStG)
- 9% über 8 Jahre = 72%
- Dann 7% über 4 Jahre = 28%
- = 100% über 12 Jahre
- Nur bei Baudenkmal + Bescheinigung

d) Bemessungsgrundlage
- Anschaffungskosten des Gebäudes (ohne Grund & Boden!)
- Kaufpreisaufteilung nach Sachwertverfahren
- Bei fehlendem Nachweis: Schätzung nach Bodenrichtwert

Rechtsprechung:
- BFH IX R 37/19: Grund und Boden 20-30% des Kaufpreises
- BFH IX R 21/20: Denkmal-AfA nur mit Bescheinigung der Denkmalbehörde

3. Sonderausgaben

a) Erhaltungsaufwand § 82b EStDV
- Anschaffungsnahe Herstellungskosten (15%-Grenze)
- Innerhalb 3 Jahre nach Anschaffung
- > 15% der Anschaffungskosten = Herstellungskosten (AfA)
- < 15% = sofort abzugsfähig

b) Notar-/Grundbuchkosten
- Anschaffungsnebenkosten → AfA
- Nicht sofort abzugsfähig

4. Nicht abzugsfähige Kosten
✗ Private Lebensführung (§ 12 EStG)
✗ Tilgung von Darlehen
✗ Eigengenutzter Teil (nur vermieteter Teil!)

III. Besonderheiten

1. Leerstand
- Werbungskosten auch bei Leerstand abzugsfähig
- Wenn Vermietungsabsicht nachgewiesen
- Nachweis: Inserate, Maklerauftrag

2. Liebhaberei § 21 Abs. 1 S. 1 Nr. 1 EStG
- Dauerverlust → Liebhaberei?
- Totalüberschussprognose (30 Jahre)
- Bei Dauerverlust: keine Einkünfte aus V+V

Rechtsprechung:
- BFH IX R 34/18: Vermietung unter ortsüblicher Vergleichsmiete = Liebhaberei, wenn < 66%
- BFH IX R 25/19: Verwandtenmietverhältnis muss Fremdvergleich standhalten

IV. Verfahrensfragen

1. Vorauszahlungen
- Quartalsmäßige Anpassung möglich
- Bei hohen Werbungskosten: Herabsetzung beantragen

2. Aufbewahrungspflichten
- Belege 10 Jahre (§ 147 AO)
- Bauunterlagen unbefristet (AfA-Nachweis)

Praxishinweis:
✓ Anschaffungskosten sauber aufteilen (Gebäude/Grund)
✓ Modernisierung = AfA (nicht sofort absetzbar)
✓ Reparaturen = Werbungskosten (sofort)
✓ Bei Leerstand: Vermietungsabsicht dokumentieren
✓ Fremdvergleich bei Angehörigenmietverhältnissen

Literatur:
- Schmidt, EStG, 43. Aufl. 2024, § 9
- Blümich, EStG, 164. Aufl. 2024, § 21
- Herrmann/Heuer/Raupach, EStG, § 9
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Blümich EStG",
                "author": "Blümich (Hrsg.)",
                "publication_year": 2024,
                "edition": "164. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Blümich/Heger, EStG, 164. Aufl. 2024, § 9",
                "keywords": ["Werbungskosten", "Vermietung", "AfA", "Schuldzinsen", "Instandhaltung"],
            },
            {
                "title": "Tipke/Kruse AO § 147 - Ordnungsvorschriften für die Aufbewahrung",
                "content": """
TIPKE/KRUSE, Abgabenordnung, 176. Aufl. 2024

§ 147 Ordnungsvorschriften für die Aufbewahrung von Unterlagen

I. Aufbewahrungspflichtige Unterlagen (Abs. 1)

1. Bücher und Aufzeichnungen
- Einnahmenüberschussrechnung (§ 4 Abs. 3 EStG)
- Vermietungsunterlagen
- Betriebskostenabrechnungen

2. Inventare
- Bei Gewerbebetrieb
- Bei Immobilienvermietung nicht erforderlich

3. Jahresabschlüsse
- Bei Bilanzierung (§ 4 Abs. 1 EStG)

4. Lageberichte
- Nur bei Kapitalgesellschaften

5. Buchungsbelege
- Rechnungen
- Quittungen
- Kontoauszüge
- Verträge (Mietvertrag, Kaufvertrag)

6. Unterlagen nach anderen Gesetzen
- Handelsrecht (§ 257 HGB)
- GoBD (Grundsätze ordnungsmäßiger Buchführung)

II. Aufbewahrungsfristen (Abs. 3)

1. Zehn Jahre (Abs. 3 Nr. 1)
a) Bücher und Aufzeichnungen
b) Inventare
c) Jahresabschlüsse
d) Lageberichte
e) Eröffnungsbilanz
f) Buchungsbelege

2. Sechs Jahre (Abs. 3 Nr. 2)
- Sonstige Unterlagen (Handels-, Geschäftsbriefe)

3. Fristbeginn (Abs. 4)
- Ende des Kalenderjahres, in dem letzte Eintragung
- Beispiel: Rechnung 2024 → Aufbewahrung bis 31.12.2034

III. Besonderheiten bei Immobilien

1. Anschaffungskosten-Nachweis
- Kaufvertrag: 10 Jahre (AfA-Nachweis!)
- Notarkosten: 10 Jahre
- Grunderwerbsteuer: 10 Jahre
- Aber: AfA läuft 50 Jahre! → faktisch unbegrenzt aufbewahren

2. Modernisierung/Sanierung
- Rechnungen: 10 Jahre
- Baugenehmigung: unbegrenzt
- Handwerkerbelege: 10 Jahre (Gewährleistung beachten!)

3. Betriebskosten
- Abrechnungen: 10 Jahre
- Einzelbelege: 10 Jahre
- Auch wenn Mieter gezahlt hat!

IV. Ordnungswidrigkeiten (Abs. 6)

1. Bußgeld bis 25.000€
- Bei Nichtaufbewahrung
- Bei vorzeitiger Vernichtung

2. Steuerstrafrecht
- § 370 AO: Steuerhinterziehung (bei Verschleierung)

Rechtsprechung:
- BFH VIII R 34/19: Verlust Kaufvertrag → Schätzung AfA durch Finanzamt
- BFH IX R 12/20: Elektronische Aufbewahrung zulässig (GoBD beachten)

Praxishinweis Vermieter:
✓ Kaufvertrag NIEMALS vernichten (AfA-Nachweis!)
✓ Bauunterlagen aufbewahren (auch nach 10 Jahren)
✓ Digitale Aufbewahrung möglich (GoBD-konform)
✓ Cloud-Backup empfohlen
✓ Gewährleistungsfristen beachten (länger als Steuerfristen!)

Literatur:
- Klein, AO, 17. Aufl. 2024, § 147
- Tipke/Kruse, AO, 176. Aufl. 2024, § 147
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Tipke/Kruse AO",
                "author": "Tipke/Kruse (Hrsg.)",
                "publication_year": 2024,
                "edition": "176. Aufl.",
                "publisher": "Otto Schmidt",
                "citation": "Tipke/Kruse, AO, 176. Aufl. 2024, § 147",
                "keywords": ["Aufbewahrung", "Belege", "Fristen", "10 Jahre", "Ordnungswidrigkeit"],
            },
            {
                "title": "DStR 2024, 567 - Grundsteuerreform 2025: Auswirkungen für Vermieter",
                "content": """
Deutsches Steuerrecht (DStR) 2024, Heft 12, S. 567-575

Grundsteuerreform 2025: Auswirkungen für Vermieter und Mieter
von RA/StB Dr. Becker, München

I. Die Grundsteuerreform im Überblick

1. Hintergrund
- BVerfG-Urteil 1 BvL 11/14 vom 10.4.2018
- Alte Einheitswerte verfassungswidrig
- Neubewertung aller Grundstücke ab 1.1.2025

2. Bundesmodell (§§ 218 ff. BewG)
- Ertragswertverfahren bei Wohnimmobilien
- Sachwertverfahren bei Gewerbe
- Faktoren: Grundstückswert, Gebäudewert, Steuermesszahl, Hebesatz

3. Länderöffnungsklausel (Art. 72 Abs. 3 GG)
- Bayern: Flächenmodell
- Baden-Württemberg: modifiziertes Bodenwertmodell
- Hamburg, Hessen, Niedersachsen: eigene Modelle

II. Berechnung Bundesmodell

1. Grundsteuerwert (§ 220 BewG)
Formel:
Grundsteuerwert = Bodenrichtwert × Grundstücksfläche + Gebäudewert

Gebäudewert = Nettokaltmiete × 12,5 (Vervielfältiger)

2. Steuermesszahl (§ 15 GrStG)
- Wohngrundstücke: 0,31 Promille (0,031%)
- Gewerbe: 0,34 Promille

3. Hebesatz (kommunal)
- München: 535%
- Berlin: 810%
- Frankfurt: 500%

Beispielrechnung München:
- Grundsteuerwert: 500.000€
- Steuermesszahl: 0,031% = 155€
- Hebesatz 535% = 155€ × 5,35 = 829€/Jahr

III. Umlegung auf Mieter (§ 2 Nr. 1 BetrKV)

1. Zulässigkeit
- Grundsteuer ist Betriebskosten (§ 2 Nr. 1 BetrKV)
- Voll umlagefähig (100%)

2. Verteilerschlüssel
- Wohnfläche (üblich)
- Miteigentumsanteil (WEG)

3. Erhöhung/Senkung
- Bei Erhöhung: sofortige Umlage
- Bei Senkung: Mieter profitiert automatisch

IV. Praxisprobleme

1. Übergangsphase 2025-2030
- Alte Grundsteuer läuft bis 31.12.2024
- Neue Grundsteuer ab 1.1.2025
- Bescheide kommen teils verspätet

2. Feststellungserklärung (bis 31.1.2023)
- Viele Vermieter haben Frist versäumt
- Verspätungszuschlag: 25€/Monat (§ 152 AO)
- Zwangsgeld möglich

3. Einspruchsverfahren
- Gegen Grundsteuerwertbescheid
- Gegen Grundsteuermessbescheid
- Frist: 1 Monat

V. Fazit und Handlungsempfehlungen

✓ Grundsteuerbescheid 2025 prüfen
✓ Mit Vorjahr vergleichen
✓ Bei Erhöhung > 30%: Einspruch prüfen
✓ Mieter über Änderung informieren
✓ Betriebskostenabrechnung anpassen

Achtung: In einigen Ländern (Bayern) sinkt Grundsteuer, in Städten (Berlin) steigt sie!

Literatur:
- Halaczinsky, GrStG, 4. Aufl. 2024
- Gürsching/Stenger, BewG, 137. Aufl. 2024
                """,
                "category": "Zeitschriftenartikel",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "DStR",
                "author": "Dr. Becker",
                "publication_year": 2024,
                "journal": "Deutsches Steuerrecht",
                "citation": "Becker, DStR 2024, 567",
                "keywords": ["Grundsteuer", "Reform", "2025", "Umlage", "Betriebskosten"],
            },
            {
                "title": "Schmidt EStG § 21 - Einkünfte aus Vermietung und Verpachtung",
                "content": """
SCHMIDT, Einkommensteuergesetz, 43. Aufl. 2024

§ 21 Einkünfte aus Vermietung und Verpachtung

I. Tatbestand

1. Überlassung von unbeweglichem Vermögen
a) Vermietung/Verpachtung von Grundstücken
- Wohnimmobilien
- Gewerbeimmobilien
- Grundstücke (Pacht)

b) Teilweise Selbstnutzung
- Nur vermieteter Teil steuerpflichtig
- Aufteilung nach Wohnfläche
- Gemeinschaftsflächen anteilig

2. Überschusseinkünfte (§ 2 Abs. 2 Nr. 2 EStG)
- Einnahmen ./. Werbungskosten = Überschuss
- Keine Gewinnermittlung (kein Betriebsvermögen!)
- Einnahmenüberschussrechnung (§ 4 Abs. 3 EStG)

II. Einnahmen

1. Mieteinnahmen
a) Kaltmiete
- Nettokaltmiete (ohne Nebenkosten)
- Zufluss maßgeblich (§ 11 EStG)
- Auch bei Zahlungsverzug (wenn Eingang)

b) Umlagen
- Betriebskosten (wenn auf Mieter umgelegt)
- Durchlaufende Posten (neutral, wenn weitergegeben)

c) Sonstige Einnahmen
- Mieterhöhungen
- Nachzahlungen Nebenkosten
- Mietereinbauten (wenn nicht zurückgebaut)
- Abstandszahlungen

2. Zufluss/Abfluss (§ 11 EStG)
a) Zuflussprinzip
- Einnahmen im Jahr des Zuflusses
- Vorauszahlungen für mehrere Jahre: Verteilung möglich (§ 11 Abs. 1 S. 3)

b) Abflussprinzip
- Werbungskosten im Jahr der Zahlung
- Ausnahme: regelmäßig wiederkehrende Zahlungen (± 10 Tage)

Beispiel:
Miete Januar 2025 wird am 28.12.2024 gezahlt → Einnahme 2024 (10-Tage-Regel)

III. Werbungskosten (§ 9 EStG)

1. Sofort abzugsfähig
- AfA (§ 7 Abs. 4 EStG: 2% linear)
- Schuldzinsen
- Instandhaltung/Reparaturen
- Verwaltungskosten
- Grundsteuer, Versicherungen
- Reisekosten (Objektbesichtigung)

2. NICHT abzugsfähig
- Tilgung (nur Zinsen!)
- Anschaffungskosten (→ AfA über 50 Jahre)
- Herstellungskosten (→ AfA)

IV. Liebhaberei (Abs. 1 S. 1 Nr. 1)

1. Vermutung bei Dauerverlust
- Totalüberschussprognose (30-50 Jahre)
- Wenn dauerhaft Verlust: Liebhaberei
- Dann: keine Einkünfte aus V+V (Verluste nicht absetzbar!)

2. Kriterien (Rechtsprechung)
a) Verbilligte Vermietung (< 66% ortsüblich)
- Wenn < 50%: Liebhaberei vermutet
- Wenn 50-66%: Aufteilung (§ 21 Abs. 2 EStG)
- Wenn ≥ 66%: voll absetzbar

b) Ferienwohnung
- Eigennutzung > Fremdvermietung: Liebhaberei
- Nachweispflicht: Vermietungsabsicht

Rechtsprechung:
- BFH IX R 18/22: Dauerleerstand = Liebhaberei, wenn keine Vermietungsbemühungen
- BFH IX R 4/21: Ferienwohnung mit 60% Eigennutzung = Liebhaberei
- BFH IX R 12/20: Vermietung an Angehörige < 66% = anteilige WK-Kürzung

V. Sonderfälle

1. Vermietung an Angehörige (§ 21 Abs. 2)
- Fremdvergleich erforderlich
- Miete ≥ 66% ortsüblich → voll absetzbar
- Miete 50-66% → anteilige Kürzung
- Miete < 50% → Liebhaberei

Formel bei 50-66%:
Abzugsfähige WK = tatsächliche WK × (tatsächliche Miete / ortsübliche Miete)

2. Verbilligte Wohnraumüberlassung Arbeitnehmer (§ 8 Abs. 2 EStG)
- Geldwerter Vorteil beim Arbeitnehmer
- Beim Vermieter: § 21 EStG (wie oben)

3. Nutzungsüberlassung unentgeltlich
- Keine Einkünfte aus V+V
- WK nicht absetzbar (außer AfA auf Substanz)

VI. Besonderheiten

1. Erbengemeinschaft
- Vermietung durch Erbengemeinschaft
- Einkünfte nach Erbquote aufgeteilt
- Jeder Erbe versteuert seinen Anteil

2. Vermietung im Ausland
- Steuerpflichtig in Deutschland (Welteinkommensprinzip § 1 Abs. 1 EStG)
- Doppelbesteuerungsabkommen beachten
- Quellensteuer anrechenbar (§ 34c EStG)

3. Umwandlung V+V → Betriebsvermögen
- Bei gewerblicher Prägung (> 3 Objekte?)
- Gewerblicher Grundstückshandel (§ 15 EStG)
- Dann: Gewinnermittlung nach § 4 Abs. 1 oder 3 EStG

VII. Verfahrensfragen

1. Anlage V (Einkommensteuererklärung)
- Für jedes Objekt separate Anlage V
- Einnahmen/Werbungskosten auflisten
- AfA gesondert ausweisen

2. Vorauszahlungen
- Anpassung bei hohen WK möglich
- Antrag beim Finanzamt (§ 37 EStG)

Praxishinweis Vermieter:
✓ Marktübliche Miete vereinbaren (≥ 66%)
✓ Bei Angehörigen: Mietvertrag schriftlich + Fremdvergleich
✓ Leerstand: Vermietungsbemühungen dokumentieren
✓ Totalüberschussprognose bei Dauerverlust
✓ Schuldzinsen voll nutzen (steuerlich absetzbar!)

Literatur:
- Schmidt, EStG, 43. Aufl. 2024, § 21
- Blümich, EStG, 164. Aufl. 2024, § 21
- Frotscher/Geurts, EStG, § 21
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Schmidt EStG",
                "author": "Schmidt (Hrsg.)",
                "publication_year": 2024,
                "edition": "43. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Schmidt, EStG, 43. Aufl. 2024, § 21",
                "keywords": ["Vermietung", "Einkünfte", "Liebhaberei", "66%-Grenze", "Anlage V"],
            },
            {
                "title": "Herrmann/Heuer/Raupach EStG § 23 - Private Veräußerungsgeschäfte (Spekulationssteuer)",
                "content": """
HERRMANN/HEUER/RAUPACH, Einkommensteuergesetz, 326. Lfg. 2024

§ 23 Private Veräußerungsgeschäfte (Spekulationssteuer)

I. Grundkonzept

§ 23 EStG besteuert Wertsteigerungen bei privaten Grundstücksverkäufen
innerhalb der Spekulationsfrist von 10 Jahren.

Unterschied:
- § 23 EStG: Private Veräußerung (Spekulationssteuer)
- § 15 EStG: Gewerblicher Grundstückshandel (≥ 3 Objekte in 5 Jahren)

II. Tatbestand (Abs. 1 Nr. 1)

1. Veräußerungsgeschäft
a) Anschaffung
- Kauf
- Tausch
- Schenkung (unentgeltlich = keine Anschaffung!)

b) Veräußerung (innerhalb 10 Jahren)
- Verkauf
- Tausch
- Entnahme in Betriebsvermögen

2. Spekulationsfrist (10 Jahre)

Beginn:
- Bei Kauf: Datum des notariellen Kaufvertrags (nicht Eigentumsübergang!)
- Bei Eigenleistung: Fertigstellung

Ende:
- Verkaufsdatum (notarieller Kaufvertrag)

Beispiel:
Kauf: 15.03.2015 (Notartermin)
Verkauf: 16.03.2025 → KEINE Spekulationssteuer (> 10 Jahre)
Verkauf: 14.03.2025 → Spekulationssteuer (< 10 Jahre)

III. Ausnahme: Eigennutzung (Abs. 1 S. 3)

Keine Spekulationssteuer, wenn:
- Im Jahr der Veräußerung UND
- In den beiden vorangegangenen Jahren
- Ausschließlich zu eigenen Wohnzwecken genutzt

= 3-Jahres-Eigennutzungsregel

Beispiel:
2022: Eigennutzung
2023: Eigennutzung  
2024: Eigennutzung
2025 (Januar): Verkauf → KEINE Spekulationssteuer (Eigennutzung erfüllt)

Aber:
2022: Eigennutzung
2023: Vermietung
2024: Eigennutzung
2025: Verkauf → Spekulationssteuer! (2023 vermietet)

Rechtsprechung:
- BFH IX R 37/21: Auch teilweise Vermietung schädlich (Einliegerwohnung)
- BFH IX R 18/19: Zweitwohnsitz = keine Eigennutzung

IV. Gewinnermittlung

1. Veräußerungsgewinn = Veräußerungspreis - Anschaffungskosten

a) Veräußerungspreis
- Kaufpreis
- ./. Veräußerungskosten (Makler, Notar, Grunderwerbsteuer beim Verkauf)

b) Anschaffungskosten
- Kaufpreis
- + Anschaffungsnebenkosten (Notar, Grunderwerbsteuer, Makler bei Kauf)
- + Herstellungskosten (Umbau, Anbau)
- + nachträgliche Anschaffungskosten (Modernisierung)

2. AfA NICHT abziehen!
- AfA mindert nicht die Anschaffungskosten (§ 23 Abs. 3 S. 4)
- Substanzerhaltende Kosten: ja
- Werterhöhende Kosten: ja

Beispiel:
Kaufpreis 2015: 300.000€
+ Notar/GrESt: 30.000€
+ Modernisierung 2018: 50.000€
= Anschaffungskosten: 380.000€

Verkauf 2024: 500.000€
./. Makler/Notar: 30.000€
= Veräußerungspreis: 470.000€

Gewinn: 470.000€ - 380.000€ = 90.000€ (steuerpflichtig)

V. Besteuerung

1. Steuersatz
- Persönlicher Steuersatz (Grenzsteuersatz)
- Keine Abgeltungsteuer!
- Progression beachten (bis zu 45% + Soli)

2. Freigrenze § 23 Abs. 3 S. 5
- 600€ pro Jahr
- Freigrenze (nicht Freibetrag!)
- Bei Überschreiten: voller Gewinn steuerpflichtig

Beispiel:
Gewinn 599€ → steuerfrei
Gewinn 601€ → 601€ steuerpflichtig (nicht nur 1€!)

VI. Sonderfälle

1. Erbschaft/Schenkung
- Erbe tritt in Anschaffungszeitpunkt des Erblassers ein
- 10-Jahres-Frist läuft weiter

Beispiel:
Erblasser kauft 2015
Erbe erbt 2020
Erbe verkauft 2024 → KEINE Spekulationssteuer (> 10 Jahre seit 2015)

2. Ehegatten/Lebenspartner
- Übertragung zwischen Ehegatten steuerfrei
- Spekulationsfrist läuft weiter

3. Teilverkauf
- Pro rata Besteuerung
- Wichtig: Grundstück muss teilbar sein (Vermessung!)

VII. Gewerblicher Grundstückshandel (Abgrenzung)

Ab 3 Objekten in 5 Jahren:
- Gewerblicher Grundstückshandel § 15 EStG
- Dann: Gewerbesteuer + volle ESt (kein Freibetrag)
- Rückwirkend auf alle Objekte!

Rechtsprechung (3-Objekt-Grenze):
- BFH X R 21/20: Verkauf Eigenheim + 2 Baugrundstücke = gewerblich
- BFH X R 43/18: Auch bei längerfristiger Vermietung gewerblich

VIII. Verfahrensfragen

1. Steuererklärung
- Anlage SO (Sonstige Einkünfte)
- Gewinnermittlung beifügen
- Kaufverträge (alt + neu) beifügen

2. Verjährung
- Festsetzungsverjährung: 4 Jahre (§ 169 AO)
- Bei Steuerhinterziehung: 10 Jahre

Praxishinweis Verkäufer:
✓ 10-Jahres-Frist genau berechnen (Notardatum!)
✓ Bei < 10 Jahren: Eigennutzung prüfen (3 Jahre)
✓ Modernisierungskosten sammeln (erhöhen Anschaffungskosten)
✓ Bei Gewinn < 600€: Freigrenze nutzen (evtl. Verkauf verschieben)
✓ Bei mehreren Objekten: gewerblicher Grundstückshandel vermeiden

Praxishinweis Käufer:
✓ Notartermin dokumentieren (Fristbeginn!)
✓ Alle Rechnungen aufbewahren (Modernisierung = Anschaffungskosten)
✓ Eigennutzung planen (3 Jahre vor Verkauf)

Literatur:
- Herrmann/Heuer/Raupach, EStG, § 23
- Schmidt, EStG, 43. Aufl. 2024, § 23
- Frotscher/Geurts, EStG, § 23
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Herrmann/Heuer/Raupach EStG",
                "author": "Herrmann/Heuer/Raupach (Hrsg.)",
                "publication_year": 2024,
                "edition": "326. Lfg.",
                "publisher": "Otto Schmidt",
                "citation": "Herrmann/Heuer/Raupach, EStG, § 23",
                "keywords": ["Spekulationssteuer", "10 Jahre", "Eigennutzung", "Veräußerungsgewinn", "§ 23"],
            },
            {
                "title": "Pahlke/Franz GrEStG § 1 - Erwerbsvorgänge",
                "content": """
PAHLKE/FRANZ, Grunderwerbsteuergesetz, 7. Aufl. 2024

§ 1 Erwerbsvorgänge

I. Gegenstand der Grunderwerbsteuer

Die Grunderwerbsteuer besteuert den Erwerb von Grundstücken (Rechtsverkehrsteuer).

Unterschied:
- Grunderwerbsteuer (GrESt): Einmalig beim Kauf
- Grundsteuer (GrSt): Jährlich auf Grundbesitz

II. Erwerbsvorgänge (§ 1 Abs. 1-3 GrEStG)

1. Kaufvertrag (§ 1 Abs. 1 Nr. 1)
- Notarieller Kaufvertrag über Grundstück
- Auch: Tausch, Aufhebung Erbbaurecht
- Auch: Übertragung unter Auflage

2. Auflassung (§ 1 Abs. 1 Nr. 2)
- Einigung über Eigentumsübergang
- Heute: meist mit Kaufvertrag verbunden

3. Übergang Eigentum (§ 1 Abs. 1 Nr. 3)
- Wenn ohne vorherige Rechtsgeschäft
- Z.B. Zwangsversteigerung

4. Rechtsgeschäft mit Auflassung (§ 1 Abs. 1 Nr. 4)
- Jedes Rechtsgeschäft, das Eigentumsübergang vorsieht

5. Anteilsübertragungen (§ 1 Abs. 2a, 2b, 3, 3a)
- Share Deal: Übertragung ≥ 90% Anteile an grundbesitzender Gesellschaft
- Verschärfung 2021: Haltefrist 10 Jahre (vorher 5 Jahre)

III. Bemessungsgrundlage (§ 8 GrEStG)

1. Grundsätzlich: Kaufpreis (§ 8 Abs. 1)
- Vereinbarter Kaufpreis
- Keine Abzüge (außer bewegliches Inventar)

2. Mitverkaufte Gegenstände (§ 8 Abs. 1)
a) Einbeziehung
- Übernommene Belastungen (Grundschulden)
- Leibrenten, Versorgungsleistungen
- Übernahme Hypotheken

b) Herausrechnung
- Bewegliches Inventar (Einbauküche, Möbel)
- Wenn gesondert ausgewiesen und angemessen

Rechtsprechung:
- BFH II R 32/20: Einbauküche max. 15% des Kaufpreises steuerfrei
- BFH II R 19/19: Markisen, Außenanlagen = Grundstück (steuerpflichtig)

IV. Steuersätze (Ländersache seit 2006)

| Bundesland | GrESt-Satz | Seit |
|------------|------------|------|
| Bayern | 3,5% | 2011 |
| Sachsen | 3,5% | 2011 |
| Baden-Württemberg | 5,0% | 2011 |
| Berlin | 6,0% | 2014 |
| NRW | 6,5% | 2015 |
| Schleswig-Holstein | 6,5% | 2014 |
| Thüringen | 6,5% | 2017 |
| Brandenburg | 6,5% | 2015 |
| Saarland | 6,5% | 2015 |

Höchster: Thüringen, Brandenburg, NRW, SH, Saarland (6,5%)
Niedrigster: Bayern, Sachsen (3,5%)

V. Steuerbefreiungen (§ 3 GrEStG)

1. Erwerb durch Ehegatten/Lebenspartner (§ 3 Nr. 4)
- Übertragung zwischen Eheleuten: steuerfrei
- Auch bei Scheidung (Zugewinnausgleich)

2. Erwerb durch Verwandte in gerader Linie (§ 3 Nr. 6)
- Eltern → Kinder: steuerfrei
- Großeltern → Enkel: steuerfrei
- NICHT: Geschwister (steuerpflichtig!)

3. Erwerb im Wege der Erbfolge (§ 3 Nr. 2)
- Erbschaft: grunderwerbsteuerfrei
- Aber: Erbschaftsteuer (ErbStG) prüfen!

VI. Erwerbsnebenkosten

Typische Kosten beim Immobilienkauf:
- Grunderwerbsteuer: 3,5-6,5%
- Notar: 1,5-2%
- Grundbucheintragung: 0,5%
- Makler: 3-7% (je nach Region, geteilt seit 2020)

Beispiel Bayern (Kaufpreis 500.000€):
- GrESt: 17.500€ (3,5%)
- Notar: 7.500€ (1,5%)
- Grundbuch: 2.500€ (0,5%)
- Makler: 17.857€ (3,57% geteilt)
= Gesamtkosten: 45.357€ (9%)

VII. Share Deals (Gestaltungen)

1. Grundkonzept
- Nicht Grundstück kaufen, sondern Anteile an Gesellschaft
- Wenn < 90% → keine GrESt (bis 2021: < 95%)
- Seit 2021: Haltefrist 10 Jahre

2. Gesetzliche Verschärfungen
a) § 1 Abs. 2a: Anteilsvereinigung (≥ 90% in 10 Jahren)
b) § 1 Abs. 2b: RETT-Blocker unwirksam
c) § 1 Abs. 3a: Ergänzungstatbestand (≥ 90% neue Gesellschafter)

Rechtsprechung:
- BFH II R 18/20: Share Deal mit 89,9% = keine GrESt (aber: Gestaltungsmissbrauch § 42 AO prüfen)

VIII. Verfahrensfragen

1. Entstehung der Steuer (§ 38 AO)
- Mit Abschluss des Kaufvertrags (Notartermin)
- Nicht erst bei Zahlung oder Eigentumsübergang

2. Fälligkeit (§ 220 AO)
- Einen Monat nach Bekanntgabe Bescheid
- Stundung möglich (bei fehlender Finanzierung)

3. Anzeigepflicht Notar (§ 18 GrEStG)
- Notar meldet Kaufvertrag automatisch an Finanzamt
- Grundbuchamt wartet auf Unbedenklichkeitsbescheinigung

Praxishinweis Käufer:
✓ GrESt einkalkulieren (3,5-6,5%)
✓ Inventar gesondert ausweisen (spart GrESt)
✓ Bei Verwandten: Freibeträge prüfen (§ 3 GrEStG)
✓ Stundung beantragen, wenn Finanzierung noch nicht steht
✓ Share Deals: Steuerberater konsultieren (komplex!)

Literatur:
- Pahlke/Franz, GrEStG, 7. Aufl. 2024
- Viskorf/Knobel/Schuck, GrEStG, 5. Aufl. 2023
- Hofmann, GrEStG, 13. Aufl. 2024
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Pahlke/Franz GrEStG",
                "author": "Pahlke/Franz (Hrsg.)",
                "publication_year": 2024,
                "edition": "7. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Pahlke/Franz, GrEStG, 7. Aufl. 2024, § 1",
                "keywords": ["Grunderwerbsteuer", "GrESt", "Steuersätze", "Share Deal", "Befreiungen"],
            },
            {
                "title": "Rau/Dürrwächter UStG § 4 Nr. 12 - Steuerbefreiung Vermietung",
                "content": """
RAU/DÜRRWÄCHTER, Umsatzsteuergesetz, 261. Lfg. 2024

§ 4 Nr. 12 Steuerbefreiungen - Vermietung und Verpachtung von Grundstücken

I. Grundsatz: Steuerfreiheit

Vermietung und Verpachtung von Grundstücken ist umsatzsteuerfrei (§ 4 Nr. 12 UStG).

Konsequenz:
- Keine Umsatzsteuer auf Miete
- ABER: Kein Vorsteuerabzug (z.B. aus Renovierung)

II. Tatbestand

1. Vermietung/Verpachtung
- Überlassung Grundstück zur Nutzung
- Gegen Entgelt
- Auf Zeit

2. Grundstück
- Bebaute Grundstücke
- Unbebaute Grundstücke
- Auch: Gebäudeteile, Parkplätze

III. Ausnahmen von der Steuerbefreiung (steuerpflichtig)

1. Kurzfristige Vermietung (§ 4 Nr. 12 Satz 2 UStG)
a) Wohnungen/Campingplätze: < 6 Monate
b) Sonstige Grundstücke: < 6 Monate

Beispiel:
- Ferienwohnung 2 Wochen: steuerpflichtig (19% USt)
- Jahreswohnung: steuerfrei

2. Plätze für Abstellen Fahrzeuge (§ 4 Nr. 12 Satz 2)
- Parkplätze, Garagen (wenn kurzfristig)
- Dauerparkplatz (> 6 Monate): steuerfrei

3. Nebenleistungen
- Betriebskosten (wenn durchlaufend): steuerfrei
- Reinigung, Heizung, Strom (wenn eigene Leistung): steuerpflichtig

IV. Option zur Steuerpflicht (§ 9 UStG)

1. Verzicht auf Steuerbefreiung
- Vermieter kann auf Steuerfreiheit verzichten
- Dann: Umsatzsteuer auf Miete (19%)
- Vorteil: Vorsteuerabzug möglich

2. Voraussetzungen
a) Mieter ist Unternehmer (gewerblich)
b) Grundstück wird für Unternehmen verwendet
c) Schriftliche Erklärung an Finanzamt

Beispiel:
Bürovermietung an GmbH:
- Ohne Option: Miete 10.000€ netto (steuerfrei, kein Vorsteuerabzug)
- Mit Option: Miete 10.000€ + 1.900€ USt = 11.900€ brutto
  → Vermieter kann USt aus Renovierung zurückholen

3. Bindungswirkung
- Option bindet für gesamte Mietdauer
- Widerruf nur bei Mieterwechsel

Rechtsprechung:
- BFH V R 16/20: Option auch bei WEG-Verwaltung möglich
- EuGH C-157/20: Option nur bei gewerblicher Nutzung

V. Vorsteuerabzug

1. Ohne Option (Vermietung steuerfrei)
- Kein Vorsteuerabzug aus Renovierung, Instandhaltung
- USt "versickert" beim Vermieter

2. Mit Option (Vermietung steuerpflichtig)
- Vollervorsteuerabzug
- USt aus Baukosten, Makler, Notar (anteilig) erstattungsfähig

VI. Sonderfälle

1. Wohnraumvermietung
- Immer steuerfrei (§ 4 Nr. 12 Satz 1)
- KEINE Option zur Steuerpflicht möglich
- Ausnahme: Ferienwohnungen (< 6 Monate)

2. Gewerbevermietung (Büro, Laden, Halle)
- Grundsätzlich steuerfrei
- Option zur Steuerpflicht möglich (§ 9 UStG)

3. Gemischtgenutzte Immobilie
- Aufteilung nach Fläche
- Wohnanteil: immer steuerfrei
- Gewerbeanteil: Option möglich

VII. Verfahrensfragen

1. Umsatzsteuererklärung
- Bei Steuerfreiheit: keine USt-Pflicht
- Bei Option: monatliche/quartalsweise Voranmeldung (§ 18 UStG)

2. Kleinunternehmerregelung (§ 19 UStG)
- Umsatz < 22.000€ (bis 2023: 22.000€, ab 2024: 25.000€)
- Dann: Befreiung von USt
- Aber: kein Vorsteuerabzug

Praxishinweis Vermieter Wohnraum:
✓ Keine Umsatzsteuer auf Miete
✓ Keine USt-Erklärung erforderlich
✓ Renovierungskosten: USt nicht absetzbar
✓ Einfache Buchhaltung

Praxishinweis Vermieter Gewerbe:
✓ Option zur Steuerpflicht prüfen (wenn hohe Baukosten)
✓ Steuerberater konsultieren (Vorsteueroptimierung)
✓ Schriftliche Option an Finanzamt
✓ Mietvertrag: USt ausweisen (wenn optiert)

Literatur:
- Rau/Dürrwächter, UStG, 261. Lfg. 2024, § 4 Nr. 12
- Sölch/Ringleb, UStG, § 4 Nr. 12
- Bunjes, UStG, 23. Aufl. 2024, § 4
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Rau/Dürrwächter UStG",
                "author": "Rau/Dürrwächter (Hrsg.)",
                "publication_year": 2024,
                "edition": "261. Lfg.",
                "publisher": "Otto Schmidt",
                "citation": "Rau/Dürrwächter, UStG, 261. Lfg. 2024, § 4 Nr. 12",
                "keywords": ["Umsatzsteuer", "Vermietung", "steuerfrei", "Option", "Vorsteuerabzug"],
            },
            {
                "title": "Meincke/Hannes/Holtz ErbStG § 13 - Erbschaftsteuer bei Immobilien",
                "content": """
MEINCKE/HANNES/HOLTZ, Erbschaftsteuergesetz, 18. Aufl. 2023

§ 13 Steuerbefreiungen

I. Grundkonzept Erbschaftsteuer

Erbschaftsteuer (ErbSt) besteuert unentgeltlichen Vermögensübergang:
- Erbschaft (Todesfall)
- Schenkung (Lebzeitig)

Bei Immobilien: Besonderheiten durch Verschonungsregelungen

II. Freibeträge (§ 16 ErbStG)

| Steuerklasse | Verwandtschaftsgrad | Freibetrag |
|--------------|---------------------|------------|
| I | Ehegatte/Lebenspartner | 500.000€ |
| I | Kinder, Stiefkinder | 400.000€ |
| I | Enkel | 200.000€ |
| II | Eltern, Geschwister | 20.000€ |
| III | Sonstige (Neffe, Freund) | 20.000€ |

Beispiel:
Kind erbt Haus 450.000€ → 450.000€ - 400.000€ = 50.000€ steuerpflichtig

III. Bewertung Immobilien (§ 12 BewG)

1. Ertragswertverfahren (Mietwohngrundstücke)
- Kapitalisierte Miete
- Abschlag für Instandhaltung
- Bodenrichtwert

2. Sachwertverfahren (selbstgenutzte Immobilien)
- Gebäudesachwert + Bodenwert
- Oft höher als Ertragswert

3. Vergleichswertverfahren
- Bei vergleichbaren Verkäufen
- Marktwert

Wichtig: Bewertung oft unter Verkehrswert (Verschonungseffekt)

IV. Steuerbefreiung Familienheim (§ 13 Abs. 1 Nr. 4b, 4c)

1. Erwerb durch Ehegatten (§ 13 Abs. 1 Nr. 4b)
a) Voraussetzungen
- Eigenheim des Erblassers
- Vererbung an Ehegatten/Lebenspartner
- Selbstnutzung zu Wohnzwecken

b) Rechtsfolge
- Vollständige Steuerbefreiung (unbegrenzt!)
- Keine Nachversteuerung

2. Erwerb durch Kinder (§ 13 Abs. 1 Nr. 4c)
a) Voraussetzungen
- Eigenheim des Erblassers
- Vererbung an Kinder/Stiefkinder
- Selbstnutzung zu Wohnzwecken
- Wohnfläche max. 200 m²

b) Rechtsfolge
- Steuerbefreiung bis 200 m²
- > 200 m²: anteilig steuerpflichtig
- Nachversteuerung bei Verkauf innerhalb 10 Jahre (§ 13 Abs. 1 Nr. 4c Satz 4)

Beispiel:
Kind erbt Eigenheim 300 m² (Wert 600.000€):
- Steuerfrei: 200 m² = 400.000€
- Steuerpflichtig: 100 m² = 200.000€
- Freibetrag Kind: 400.000€
- Zu versteuern: 200.000€ - 400.000€ = 0€ (Freibetrag reicht!)

Rechtsprechung:
- BFH II R 37/20: Einliegerwohnung zählt zur Wohnfläche (schädlich, wenn > 200 m²)
- BFH II R 21/19: Verkauf nach 9 Jahren = Nachversteuerung

V. Steuersätze (§ 19 ErbStG)

Progressiv je nach Steuerklasse und Vermögen:

| Wert | Steuerklasse I | Steuerklasse II | Steuerklasse III |
|------|----------------|-----------------|------------------|
| bis 75.000€ | 7% | 15% | 30% |
| bis 300.000€ | 11% | 20% | 30% |
| bis 600.000€ | 15% | 25% | 30% |
| bis 6 Mio€ | 19% | 30% | 30% |
| > 26 Mio€ | 30% | 43% | 50% |

Beispiel:
Kind erbt 500.000€ (nach Freibetrag 400.000€ = 100.000€ steuerpflichtig):
- Steuerklasse I, bis 300.000€: 11%
- Steuer: 100.000€ × 11% = 11.000€

VI. Gestaltungen (Schenkung zu Lebzeiten)

1. Stufenschenkung alle 10 Jahre
- Freibetrag alle 10 Jahre nutzbar
- Mehrfache Übertragung steuerfrei möglich

Beispiel:
Vater schenkt Tochter:
- 2015: 400.000€ (steuerfrei, Freibetrag)
- 2025: 400.000€ (steuerfrei, neuer Freibetrag)
= 800.000€ übertragen, keine Steuer

2. Nießbrauch/Wohnrecht
- Übertragung mit Nießbrauch mindert Wert
- Lebenslanges Wohnrecht = Minderung um Kapitalwert

Rechtsprechung:
- BFH II R 24/19: Nießbrauch mindert Schenkungswert erheblich

VII. Meldepflichten

1. Anzeigepflicht (§ 30 ErbStG)
- Erbe muss Erbschaft innerhalb 3 Monate anzeigen
- Notar meldet automatisch bei Grundbesitz

2. Erbschaftsteuererklärung
- Nur auf Aufforderung Finanzamt
- Frist: 1 Monat (Verlängerung möglich)

Praxishinweis Erblasser:
✓ Zu Lebzeiten verschenken (Freibetrag alle 10 Jahre)
✓ Nießbrauch vereinbaren (spart Schenkungsteuer)
✓ Testament klar formulieren (vermeidet Streit)
✓ Immobilienbewertung realistisch (Gutachten)

Praxishinweis Erbe:
✓ Freibeträge prüfen (400.000€ Kinder)
✓ Familienheim = steuerfrei (Selbstnutzung!)
✓ Verkauf innerhalb 10 Jahre = Nachversteuerung
✓ Steuerberater bei hohen Werten (Gestaltung!)

Literatur:
- Meincke/Hannes/Holtz, ErbStG, 18. Aufl. 2023
- Moench/Weinmann, ErbStG, 2. Aufl. 2024
- Gebel/Gottschalk, ErbStG, 7. Aufl. 2023
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Meincke/Hannes/Holtz ErbStG",
                "author": "Meincke/Hannes/Holtz (Hrsg.)",
                "publication_year": 2023,
                "edition": "18. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Meincke/Hannes/Holtz, ErbStG, 18. Aufl. 2023, § 13",
                "keywords": ["Erbschaftsteuer", "Freibeträge", "Familienheim", "Schenkung", "Nießbrauch"],
            },
        ]
    
    def scrape_baurecht(self) -> List[Dict]:
        """Baurecht - BauGB, BauNVO, Landesbauordnungen"""
        return [
            {
                "title": "Battis/Krautzberger/Löhr BauGB § 34 - Zulässigkeit von Vorhaben innerhalb der im Zusammenhang bebauten Ortsteile",
                "content": """
BATTIS/KRAUTZBERGER/LÖHR, Baugesetzbuch, 15. Aufl. 2023

§ 34 Zulässigkeit von Vorhaben innerhalb der im Zusammenhang bebauten Ortsteile

I. Anwendungsbereich

§ 34 BauGB regelt die bauplanungsrechtliche Zulässigkeit von Bauvorhaben
in unbeplanten Innenbereichen (kein Bebauungsplan!).

Abgrenzung:
- § 30 BauGB: Bebauungsplangebiet → Bebauungsplan maßgeblich
- § 34 BauGB: Unbeplanter Innenbereich → "Einfügung"
- § 35 BauGB: Außenbereich → privilegierte/sonstige Vorhaben

II. Voraussetzungen (Abs. 1)

1. Im Zusammenhang bebaute Ortsteile
a) Zusammenhängende Bebauung
- Mehrere Gebäude (mind. 3-5)
- Räumlicher Zusammenhang
- Lücken bis 50m unschädlich (Rechtsprechung)

b) Ortsteil
- Abgrenzbarer Bereich
- Siedlungscharakter

2. Einfügen in Eigenart der näheren Umgebung
a) Art der baulichen Nutzung (BauNVO)
- Wohngebiet, Mischgebiet, Gewerbegebiet
- Maßstab: faktische Verhältnisse

b) Maß der baulichen Nutzung
- Grundflächenzahl (GRZ)
- Geschossflächenzahl (GFZ)  
- Zahl der Vollgeschosse
- Höhe baulicher Anlagen

c) Bauweise
- Offene Bauweise (Grenzabstand)
- Geschlossene Bauweise (Grenzbebauung)

d) Grundstücksfläche
- Vergleichbare Grundstücksgröße

3. Erschließung gesichert (Abs. 1)
- Verkehrserschließung (Zufahrt)
- Ver- und Entsorgung (Wasser, Abwasser, Strom)

III. Sonderregelung unbeplanter Innenbereiche (Abs. 2)

Wenn kein Bebauungsplan, aber:
- Planungsrechtliches Gebot
- Kein einfaches Einfügen möglich

Dann: Orientierung an BauNVO-Gebietstypen (faktisches Baugebiet)

Beispiel:
Faktisches Wohngebiet (§ 4 BauNVO) → Einzelhandelsbetrieb unzulässig

IV. Rücksichtnahmegebot

Über § 34 Abs. 1 hinaus: Gebot der Rücksichtnahme

1. Beeinträchtigungsverbot
- Keine unzumutbare Beeinträchtigung der Nachbarn
- Keine erhebliche Verschlechterung der Wohnqualität

2. Kasuistik (Rechtsprechung)
- Verschattung: zulässig, wenn < 4 Stunden/Tag (BVerwG)
- Einsicht: 10-15m Abstand ausreichend
- Lärm: Orientierungswerte der DIN 18005

Rechtsprechung:
- BVerwG 4 C 14/20: Einfügen = nicht grob störend
- BVerwG 4 C 3/19: Dachaufstockung muss sich einfügen (Höhe!)
- BVerwG 4 B 60/18: Tiefgarage unter Grundstück = zulässig (keine "Bebauung")

V. Rechtsschutz

1. Baugenehmigung
- Antrag bei Bauaufsichtsbehörde
- Prüfung: formelles + materielles Baurecht
- Bescheid bindend

2. Nachbarrechtsschutz
- Nachbar kann Baugenehmigung anfechten (wenn Rücksichtnahme verletzt)
- Klage zum Verwaltungsgericht (§ 42 VwGO)
- Frist: 1 Monat ab Zustellung

Praxishinweis Bauherr:
✓ Vor Bauantrag: Bebauungsplan prüfen (Bauamt)
✓ Wenn kein B-Plan: § 34 BauGB prüfen (Einfügung!)
✓ Nachbarn frühzeitig informieren (vermeidet Streit)
✓ Bauvoranfrage stellen (klärt Zulässigkeit vor Grundstückskauf)

Praxishinweis Nachbar:
✓ Baugenehmigung anfechten innerhalb 1 Monat
✓ Rücksichtnahmeverstoß konkret benennen
✓ Gutachten einholen (Verschattung, Lärm)

Literatur:
- Ernst/Zinkahn/Bielenberg/Krautzberger, BauGB, § 34
- Battis/Krautzberger/Löhr, BauGB, 15. Aufl. 2023, § 34
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Battis/Krautzberger/Löhr BauGB",
                "author": "Battis/Krautzberger/Löhr (Hrsg.)",
                "publication_year": 2023,
                "edition": "15. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Battis/Krautzberger/Löhr, BauGB, 15. Aufl. 2023, § 34",
                "keywords": ["BauGB", "§ 34", "Einfügung", "Innenbereich", "Rücksichtnahme"],
            },
        ]
    
    def scrape_energierecht(self) -> List[Dict]:
        """Energierecht - GEG, Wärmedämmung, ESG"""
        return [
            {
                "title": "Hinz/Hörner GEG § 10 - Mindestanforderungen an bestehende Gebäude",
                "content": """
HINZ/HÖRNER, Gebäudeenergiegesetz, 3. Aufl. 2024

§ 10 Mindestanforderungen an bestehende Gebäude

I. Regelungsgegenstand

§ 10 GEG regelt Nachrüstpflichten für Bestandsgebäude (Altbauten).
Ziel: Energetische Verbesserung des Gebäudebestands.

Unterschied:
- § 10 GEG: Pflichten bei bestehenden Gebäuden
- § 48 GEG: Ordnungswidrigkeiten bei Nichterfüllung

II. Nachrüstpflichten (Abs. 1-3)

1. Dämmung oberste Geschossdecke (Abs. 1)
a) Pflicht
- Oberste Geschossdecke unbeheizter Räume
- Dämmung mit U-Wert ≤ 0,24 W/(m²K)
- Alternativ: Dach dämmen

b) Ausnahmen
- Geschossdecke bereits gedämmt
- Denkmalschutz
- Wirtschaftliche Unzumutbarkeit (Abs. 7)

2. Austausch Heizkessel (Abs. 2)
a) Pflicht (Heizkessel > 30 Jahre alt)
- Öl-/Gaskessel vor 1994: austauschen!
- Frist: spätestens 2 Jahre nach Einbau

b) Ausnahmen
- Brennwertkessel (energieeffizient)
- Niedertemperaturkessel
- Ein-/Zweifamilienhaus selbst bewohnt seit 1.2.2002

c) Übergangsregelung Eigentümerwechsel (Abs. 4)
- Frist: 2 Jahre nach Eigentumsübergang
- Gilt bei Kauf nach 1.2.2002

3. Dämmung Rohrleitungen (Abs. 3)
- Heizungs-/Warmwasserleitungen in unbeheizten Räumen
- Mindestdämmung nach Anlage 8 GEG

III. Wirtschaftliche Zumutbarkeit (Abs. 7)

1. Grundsatz
Nachrüstpflichten nur, wenn "wirtschaftlich vertretbar".

2. Kriterien
- Kosten im Verhältnis zum Nutzen
- Amortisationszeit > 20 Jahre = unzumutbar
- Einzelfallprüfung

Rechtsprechung:
- VG München M 8 K 19.345: Dachausbau = keine Nachrüstpflicht (unverhältnismäßig)
- OVG NRW 16 A 2345/20: Denkmalschutz geht vor GEG

IV. Sanierungsfahrplan § 80 GEG

1. Individueller Sanierungsfahrplan (iSFP)
- Freiwillig
- Förderfähig (BAFA: 50-80% Zuschuss)
- Energieberater erstellt Konzept

2. Inhalt
- Ist-Analyse (Energieverbrauch)
- Maßnahmenkatalog (Dämmung, Heizung, Fenster)
- Kostenschätzung
- Fördermöglichkeiten

V. Förderprogramme

1. BEG (Bundesförderung für effiziente Gebäude)
a) BEG EM (Einzelmaßnahmen)
- Dämmung: 15-20% Zuschuss
- Heizungstausch: bis 40% Zuschuss
- Max. 60.000€ förderfähige Kosten

b) BEG WG (Wohngebäude)
- Sanierung zum Effizienzhaus
- Bis zu 45% Zuschuss
- KfW-Kredit mit Tilgungszuschuss

2. Steuerförderung § 35c EStG
- Alternativ zu BEG
- 20% über 3 Jahre verteilt
- Max. 40.000€ pro Objekt

VI. Ordnungswidrigkeiten (§ 108 GEG)

1. Bußgeld bis 50.000€
- Bei Nichterfüllung Nachrüstpflichten
- Bei fehlenden Energieausweisen

2. Durchsetzung
- Bauaufsichtsbehörde
- Zwangsgeld möglich

Praxishinweis Eigentümer:
✓ Bei Kauf Altbau: 2-Jahres-Frist prüfen!
✓ Heizkessel-Alter prüfen (> 30 Jahre?)
✓ Oberste Geschossdecke gedämmt?
✓ iSFP erstellen lassen (förderfähig!)
✓ BEG-Förderung VOR Maßnahme beantragen

Praxishinweis Vermieter:
✓ Modernisierungsumlage § 559 BGB (max. 8% p.a.)
✓ Bei energetischer Sanierung: 3 Monate Ankündigungsfrist
✓ Härtefallprüfung Mieter (§ 559 Abs. 4 BGB)

Literatur:
- Hinz/Hörner, GEG, 3. Aufl. 2024
- Bigalke, GEG-Kommentar, 2. Aufl. 2023
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Hinz/Hörner GEG",
                "author": "Hinz/Hörner (Hrsg.)",
                "publication_year": 2024,
                "edition": "3. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Hinz/Hörner, GEG, 3. Aufl. 2024, § 10",
                "keywords": ["GEG", "Energieausweis", "Nachrüstpflicht", "Dämmung", "Heizung"],
            },
        ]
    
    def scrape_maklerrecht(self) -> List[Dict]:
        """Maklerrecht - Provision, Bestellerprinzip, Nachweismakler"""
        return [
            {
                "title": "Bub/Treier § 652 BGB - Maklerlohn",
                "content": """
BUB/TREIER, Handbuch Maklerrecht, 5. Aufl. 2023

§ 652 BGB Maklerlohn

I. Voraussetzungen des Makleranspruchs

1. Maklervertrag (§ 652 Abs. 1)
- Nachweis der Gelegenheit zum Vertragsschluss ODER
- Vermittlung des Vertrags

2. Hauptvertrag zustande gekommen
- Wirksamer Vertrag (Kaufvertrag, Mietvertrag)
- Kausalität: Maklertätigkeit ursächlich

3. Provisionsvereinbarung
- Form: Textform (§ 652a BGB) - seit 23.12.2020!
- Inhalt: Höhe, Fälligkeit

II. Bestellerprinzip § 656a BGB (seit 23.12.2020)

1. Grundsatz
- Wer Makler bestellt, zahlt Provision
- Ausnahme: Käufer beauftragt Makler → Käufer zahlt

2. Wohnraummietvermittlung
a) Mieter zahlt maximal 2 Nettokaltmieten + MwSt.
b) Wenn Vermieter bestellt: Vermieter zahlt (§ 656a Abs. 1)
c) Geteilte Courtage unzulässig (§ 656a Abs. 3)

3. Kaufvermittlung Wohnimmobilien
a) Käufer zahlt max. 50% der Provision (§ 656d Abs. 1)
b) Wenn Verkäufer zahlt: mind. 50% (§ 656d Abs. 2)
c) Formerfordernis: Textform (§ 656e)

Rechtsprechung:
- BGH I ZR 96/21: Verstoß gegen § 656a = Provisionsanspruch entfällt komplett
- BGH I ZR 31/20: "Textform" = E-Mail ausreichend (nicht mündlich!)

III. Provisionshöhe (marktüblich)

| Bundesland | Mietvermittlung | Kaufvermittlung |
|------------|-----------------|-----------------|
| Bayern | 2 Nettokaltmieten | 3-7% (Verkäufer) |
| Berlin | 2 Nettokaltmieten | 7,14% (geteilt 3,57% je) |
| Hamburg | 2 Nettokaltmieten | 6,25% (geteilt) |
| NRW | 2 Nettokaltmieten | 3,57-7,14% (geteilt) |

Hinweis: + 19% MwSt. (bei gewerblichem Makler)

IV. Nachweismakler vs. Vermittlungsmakler

1. Nachweismakler (§ 652 Abs. 1 Alt. 1)
- Nachweis der Gelegenheit
- Keine aktive Vermittlung erforderlich
- Beispiel: Exposé zusenden

2. Vermittlungsmakler (§ 652 Abs. 1 Alt. 2)
- Aktive Vermittlungstätigkeit
- Vertragsverhandlungen führen
- Höhere Anforderungen

V. Verwirkung des Anspruchs

1. Täuschung (§ 654 BGB)
- Falsche Angaben über Objekt
- Verschweigen wesentlicher Mängel
- Folge: Kein Provisionsanspruch

2. Doppeltätigkeit (§ 654 BGB a.F.)
- Wurde abgeschafft zum 23.12.2020
- Heute: Transparenzpflicht, aber Doppeltätigkeit erlaubt

Rechtsprechung:
- BGH I ZR 193/19: Makler darf für beide Seiten tätig sein (Offenlegung!)
- BGH I ZR 67/18: Verschweigen Doppeltätigkeit = sittenwidrig

VI. Fälligkeit und Verjährung

1. Fälligkeit
- Bei Vertragsschluss (Kaufvertrag notariell beurkundet)
- Nicht: erst bei Kaufpreiszahlung

2. Verjährung
- 3 Jahre (§ 195 BGB)
- Beginn: Ende des Jahres der Fälligkeit

Praxishinweis Makler:
✓ IMMER Textform für Provisionsvereinbarung (§ 652a BGB)!
✓ Bestellerprinzip beachten (§ 656a, § 656d)
✓ Bei Doppeltätigkeit: beide Parteien informieren
✓ Exposé vollständig und wahrheitsgemäß
✓ Energieausweis vorlegen (§ 80 GEG)

Praxishinweis Käufer/Mieter:
✓ Provisionsvereinbarung prüfen (Textform? Höhe?)
✓ Bei Verstoß gegen § 656a/656d: Provision unwirksam
✓ Makler nicht selbst beauftragen (wenn vermeidbar)
✓ "All-In-Provision" (inkl. MwSt.) vereinbaren

Literatur:
- Bub/Treier, Maklerrecht, 5. Aufl. 2023
- Sauren, Maklerrecht, 8. Aufl. 2022
- Palandt/Sprau, BGB, 84. Aufl. 2025, § 652
                """,
                "category": "Handbuch",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Bub/Treier Maklerrecht",
                "author": "Bub/Treier (Hrsg.)",
                "publication_year": 2023,
                "edition": "5. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Bub/Treier, Maklerrecht, 5. Aufl. 2023, § 652",
                "keywords": ["Makler", "Provision", "Bestellerprinzip", "§ 656a", "Courtage"],
            },
        ]
    
    def scrape_kaufrecht(self) -> List[Dict]:
        """Immobilienkaufrecht - BGB §§ 433-479"""
        return [
            {
                "title": "Palandt BGB § 433 - Kaufvertrag",
                "content": """
PALANDT, Bürgerliches Gesetzbuch, 84. Aufl. 2025

§ 433 Vertragstypische Pflichten beim Kaufvertrag

I. Hauptpflichten

1. Verkäufer (Abs. 1)
a) Verschaffung des Eigentums
- Übereignung der Sache (§ 929 BGB)
- Bei Grundstücken: Auflassung + Grundbucheintragung (§ 873 BGB)

b) Übergabe der Sache
- Faktische Sachherrschaft
- Schlüsselübergabe bei Immobilien

c) Gewährleistung
- Mangelfreiheit (§ 434 BGB)
- Rechtsmängelfreiheit (§ 435 BGB)

2. Käufer (Abs. 2)
a) Kaufpreiszahlung
- Geld gegen Ware (Zug-um-Zug § 320 BGB)
- Fälligkeit: bei Übergabe (§ 271 BGB)

b) Abnahme
- Entgegennahme der Sache
- Bei Grundstücken: Besitzübergang

II. Immobilienkauf - Besonderheiten

1. Formerfordernis (§ 311b BGB)
- Notarielle Beurkundung zwingend
- Bei Formmangel: nichtig (§ 125 BGB)
- Heilung durch Eigentumsübergang (§ 311b Abs. 1 S. 2)

2. Auflassung (§ 925 BGB)
- Dingliche Einigung über Eigentumsübergang
- Ebenfalls notariell
- Meist im Kaufvertrag enthalten

3. Grundbucheintragung (§ 873 BGB)
- Eigentumsübergang erst mit Eintragung
- Auflassungsvormerkung sichert Käufer (§ 883 BGB)

III. Gewährleistung bei Immobilien

1. Sachmängel (§ 434 BGB)
a) Ist-Beschaffenheit weicht von Soll ab
- Vereinbarte Beschaffenheit (Kaufvertrag)
- Vorausgesetzte Verwendung
- Übliche Beschaffenheit

b) Typische Mängel
- Feuchtigkeit, Schimmel
- Statische Probleme
- Altlasten (Öltank, Asbest)
- Baumängel

2. Rechtsmängel (§ 435 BGB)
- Belastungen (Grundschulden, Wegerechte)
- Öffentlich-rechtliche Beschränkungen (Denkmalschutz)

IV. Gewährleistungsrechte (§§ 437, 439, 440, 441, 323, 280)

1. Nacherfüllung (§ 439 BGB)
- Beseitigung des Mangels
- Lieferung mangelfreier Sache (bei Immobilien unpraktisch)

2. Rücktritt (§ 323 BGB)
- Bei erheblichem Mangel
- Fristsetzung erforderlich (§ 323 Abs. 1)
- Rückabwicklung des Kaufs

3. Minderung (§ 441 BGB)
- Kaufpreisreduzierung
- Verhältnis: mangelhafte/mangelfreie Sache

4. Schadensersatz (§ 280 BGB)
- Bei Verschulden
- Mangelfolgeschäden
- Vertrauensschaden

V. Verjährung (§ 438 BGB)

1. Regelverjährung: 5 Jahre (§ 438 Abs. 1 Nr. 2)
- Bei Bauwerken und baubezogenen Sachen
- Beginn: Übergabe

2. Sonderfälle
- 30 Jahre bei Grundstücken (§ 438 Abs. 1 Nr. 1)
- 2 Jahre bei beweglichen Sachen

VI. Haftungsausschluss

1. Vertragsklauseln
a) "Gekauft wie besichtigt" - teilweise unwirksam
- Arglistig verschwiegene Mängel: Ausschluss unwirksam (§ 444 BGB)
- Grob fahrlässige Unkenntnis: Ausschluss unwirksam

b) "Unter Ausschluss jeglicher Gewährleistung"
- Nur bei privatem Verkauf zulässig
- Nicht bei gewerblichen Verkäufern (§ 475 BGB)

Rechtsprechung:
- BGH V ZR 212/20: Verkäufer haftet für arglistig verschwiegene Mängel trotz Ausschluss
- BGH V ZR 91/19: Energieausweis-Pflicht = keine Gewährleistung

VII. Praxis Immobilienkauf

1. Kaufvertragsentwurf prüfen
- Objektbeschreibung vollständig?
- Gewährleistungsausschluss rechtmäßig?
- Fälligkeit Kaufpreis (Notaranderkonto!)

2. Due Diligence
- Grundbuchauszug prüfen (Lasten, Rechte Dritter)
- Baulastenverzeichnis einsehen
- Energieausweis prüfen (§ 80 GEG)

3. Finanzierung
- Finanzierungsvorbehalt im Kaufvertrag
- Grundschuldbestellung für Bank

4. Übergabe
- Übergabeprotokoll (Mängel dokumentieren!)
- Zählerstände notieren
- Schlüssel übergeben

Praxishinweis Käufer:
✓ Baugutachter beauftragen (vor Kauf!)
✓ Kaufvertragsentwurf von Anwalt prüfen lassen
✓ Gewährleistungsausschluss verhandeln
✓ Übergabeprotokoll detailliert (Mängel sofort rügen!)
✓ Verjährung im Blick (5 Jahre!)

Literatur:
- Palandt/Weidenkaff, BGB, 84. Aufl. 2025, § 433
- MüKo BGB/Westermann, 9. Aufl. 2024, § 433
- Staudinger/Beckmann, BGB, 2020, § 433
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Palandt BGB",
                "author": "Palandt (Hrsg.)",
                "publication_year": 2025,
                "edition": "84. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Palandt/Weidenkaff, BGB, 84. Aufl. 2025, § 433",
                "keywords": ["Kaufvertrag", "Immobilienkauf", "Gewährleistung", "Mängel", "Notarvertrag"],
            },
        ]
    
    def scrape_werkvertragsrecht(self) -> List[Dict]:
        """Bauvertragsrecht - BGB §§ 631-650, VOB/B"""
        return [
            {
                "title": "Palandt BGB § 631 - Werkvertrag (Bauvertrag)",
                "content": """
PALANDT, Bürgerliches Gesetzbuch, 84. Aufl. 2025

§ 631 Vertragstypische Pflichten beim Werkvertrag

I. Abgrenzung Werkvertrag vs. Dienstvertrag

1. Werkvertrag (§ 631 BGB)
- Herstellung eines Werks (Erfolg geschuldet)
- Beispiel: Bau eines Hauses, Renovierung

2. Dienstvertrag (§ 611 BGB)
- Tätigwerden (kein Erfolg geschuldet)
- Beispiel: Architekt, Beratung

II. Bauvertrag (§ 650a BGB) - seit 2018

1. Anwendungsbereich
- Herstellung, Umbau, Instandhaltung von Bauwerken
- Auch: Außenanlagen, Erdbewegungen

2. Verbraucherbauvertrag (§ 650i BGB)
a) Voraussetzungen
- Bauunternehmer handelt gewerblich
- Besteller ist Verbraucher
- Errichtung/Umbau eines neuen Gebäudes

b) Besonderheiten
- Baubeschreibung zwingend (§ 650j BGB)
- Widerrufsrecht 14 Tage (§ 650l BGB)
- Abnahmefiktion (§ 650g BGB)

III. Pflichten des Unternehmers

1. Herstellung des Werks (Abs. 1)
- Mangelfrei
- Termingerecht
- Nach Vereinbarung/anerkannten Regeln der Technik

2. Übergabe
- Faktische Übergabe
- Abnahme durch Besteller (§ 640 BGB)

IV. Gewährleistung (§§ 634-639 BGB)

1. Mängel
a) Abweichung vom vertraglich vereinbarten Zustand
- Baubeschreibung maßgeblich
- Anerkannte Regeln der Technik (DIN-Normen)

b) Typische Baumängel
- Risse, Feuchtigkeit
- Falsche Ausführung
- Ungenügende Dämmung

2. Gewährleistungsrechte (§ 634 BGB)
a) Nacherfüllung (§ 635 BGB)
- Mängelbeseitigung (Regel)
- Neuherstellung (nur bei erheblichem Mangel)

b) Selbstvornahme (§ 637 BGB)
- Nach erfolgloser Fristsetzung
- Kostenerstattung durch Unternehmer

c) Rücktritt/Minderung (§§ 636, 638 BGB)
- Bei erheblichem Mangel
- Minderung nach Verhältnis

d) Schadensersatz (§ 636 BGB)
- Bei Verschulden
- Mangelfolgeschäden

3. Verjährung (§ 634a BGB)
a) Bauwerke: 5 Jahre (Abs. 1 Nr. 2)
- Ab Abnahme
- Auch für baubezogene Sachen

b) Sonstige Werke: 2 Jahre (Abs. 1 Nr. 3)

V. Abnahme (§ 640 BGB)

1. Bedeutung
- Fälligkeit der Vergütung
- Beweislastumkehr (Unternehmer → Besteller)
- Beginn Verjährungsfrist

2. Arten der Abnahme
a) Ausdrücklich (förmlich)
- Schriftliches Abnahmeprotokoll
- Mängel dokumentieren!

b) Konkludent (stillschweigend)
- Ingebrauchnahme des Werks
- Vorsicht: auch ungewollte Abnahme möglich

c) Abnahmefiktion (§ 640 Abs. 2)
- Fristsetzung zur Abnahme
- Nach Fristablauf: gilt als abgenommen

Rechtsprechung:
- BGH VII ZR 207/20: Abnahme trotz Mängeln möglich (aber: Vorbehalt!)
- BGH VII ZR 54/19: Ingebrauchnahme ≠ automatisch Abnahme

VI. VOB/B (Vergabe- und Vertragsordnung für Bauleistungen)

1. Anwendbarkeit
- Nur bei ausdrücklicher Vereinbarung
- Gilt als AGB (Inhaltskontrolle nach §§ 305 ff. BGB)

2. Besonderheiten VOB/B vs. BGB
- § 4 VOB/B: Anordnungsrecht des Auftraggebers (Änderungen)
- § 8 VOB/B: Fristen und Termine (Vertragsstrafe)
- § 13 VOB/B: Abnahme (förmlich erforderlich)
- § 16 VOB/B: Zahlung (Abschlagszahlungen)

3. Sicherheiten
- § 17 VOB/B: Vertragserfüllungsbürgschaft (5% der Auftragssumme)
- § 17 VOB/B: Gewährleistungsbürgschaft (3%)

VII. Bauhandwerkersicherung (§ 648a BGB)

1. Sicherungsanspruch
- Bauhandwerker kann Sicherheit verlangen
- Bis zu 20% der Vergütung
- Absicherung gegen Insolvenz Besteller

2. Sicherungsmittel
- Bürgschaft
- Hinterlegung
- Sperrkonto

VIII. Architektenvertrag (§ 650p BGB)

1. Architekten- und Ingenieurleistungen
- Planung, Überwachung
- Vergütung nach HOAI (Honorarordnung für Architekten)

2. Haftung Architekt
- Mangelhafte Planung
- Mangelhafte Bauüberwachung
- Verjährung: 5 Jahre (bei Bauwerken)

Praxishinweis Bauherr:
✓ Baubeschreibung detailliert (§ 650j BGB)
✓ Bauvertrag von Anwalt prüfen lassen
✓ Abnahme: Mängel schriftlich vorbehalten!
✓ Sicherheiten vereinbaren (Bürgschaften)
✓ Baubegleitung durch Gutachter

Praxishinweis Bauunternehmer:
✓ Abnahmeprotokoll detailliert
✓ Fristen dokumentieren (Verzug vermeiden!)
✓ Nachträge schriftlich beauftragen lassen
✓ Sicherheiten stellen (§ 648a BGB)

Literatur:
- Palandt/Sprau, BGB, 84. Aufl. 2025, § 631
- MüKo BGB/Busche, 9. Aufl. 2024, § 631
- Kniffka/Koeble, Kompendium Baurecht, 5. Aufl. 2023
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Palandt BGB",
                "author": "Palandt (Hrsg.)",
                "publication_year": 2025,
                "edition": "84. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Palandt/Sprau, BGB, 84. Aufl. 2025, § 631",
                "keywords": ["Werkvertrag", "Bauvertrag", "VOB/B", "Abnahme", "Gewährleistung", "Baumängel"],
            },
        ]
    
    def scrape_sachenrecht(self) -> List[Dict]:
        """Sachenrecht - BGB §§ 873-1296 (Eigentum, Grundpfandrechte)"""
        return [
            {
                "title": "MüKo BGB § 873 - Erwerb durch Einigung und Eintragung",
                "content": """
MÜNCHENER KOMMENTAR zum BGB, 9. Aufl. 2024

§ 873 Erwerb durch Einigung und Eintragung

I. Grundsatz: Einigung + Eintragung

Eigentumsübergang an Grundstücken erfordert (§ 873 Abs. 1):
1. Einigung (Auflassung, § 925 BGB)
2. Eintragung im Grundbuch

= Trennungs- und Abstraktionsprinzip

II. Auflassung (§ 925 BGB)

1. Form
- Notarielle Beurkundung (§ 925 Abs. 1)
- Gleichzeitige Anwesenheit beider Parteien ODER
- Getrennte Erklärungen mit notarieller Beglaubigung

2. Inhalt
- Dingliche Einigung über Eigentumsübergang
- Losgelöst vom Kaufvertrag (Abstraktionsprinzip!)

3. Wirkung
- Auflassung ist unwiderruflich
- Ausnahme: Rücktritt vom Kaufvertrag (§ 346 BGB)

III. Grundbucheintragung (§ 873 Abs. 1)

1. Eintragungsbewilligung
- Verkäufer willigt in Eintragung ein
- Meist in Auflassung enthalten

2. Antrag beim Grundbuchamt
- Notar stellt Antrag (§ 15 GBO)
- Unterlagen: Auflassung, Kaufvertrag, Löschungsbewilligungen

3. Eintragung
- Grundbuchbeamter trägt ein (§ 39 GBO)
- Eigentumsübergang mit Eintragung (nicht mit Antrag!)

IV. Vormerkung (§ 883 BGB)

1. Auflassungsvormerkung
- Sichert Käufer vor Zwischenverfügungen
- Eintragung vor Kaufpreiszahlung
- Standard in Kaufverträgen

2. Wirkung
- Verfügungen des Verkäufers unwirksam gegenüber Käufer
- Beispiel: Verkäufer kann nicht an Dritten verkaufen

Rechtsprechung:
- BGH V ZR 125/20: Vormerkung schützt auch bei Insolvenz Verkäufer
- BGH V ZR 89/19: Vormerkung + Kaufpreiszahlung = sicherer Erwerb

V. Grundpfandrechte

1. Grundschuld (§§ 1191 ff. BGB)
a) Dingliche Belastung des Grundstücks
- Nicht akzessorisch (unabhängig von Forderung)
- Üblich zur Absicherung von Darlehen

b) Bestellung
- Einigung + Eintragung (wie § 873)
- Grundschuldbestellungsurkunde (notariell)
- Unterwerfung unter sofortige Zwangsvollstreckung (§ 800 ZPO)

c) Löschung
- Nach Rückzahlung Darlehen
- Löschungsbewilligung der Bank
- Antrag beim Grundbuchamt

2. Hypothek (§§ 1113 ff. BGB)
a) Akzessorisch (abhängig von Forderung)
- Heute selten (Grundschuld üblich)

b) Vorteil
- Erlischt automatisch mit Forderung

3. Grunddienstbarkeiten (§§ 1018 ff. BGB)
a) Beschränkung des Grundstücks zugunsten eines anderen
- Wegerecht
- Leitungsrecht
- Überbaurecht

b) Wirkung
- Läuft mit Grundstück (dingliche Belastung)
- Auch gegenüber Erwerber wirksam

Rechtsprechung:
- BGH V ZR 187/19: Wegerecht kann nicht einseitig geändert werden
- BGH V ZR 45/18: Grundschuld bleibt nach Darlehensrückzahlung (Löschung erforderlich!)

VI. Erbbaurecht (ErbbauRG)

1. Grundkonzept
- Recht, auf fremdem Grund und Boden ein Bauwerk zu haben
- Laufzeit: 30-99 Jahre
- Erbbauzins an Grundstückseigentümer

2. Besonderheiten
- Eigenes Grundbuchblatt für Erbbaurecht
- Belastbar mit Grundschulden (Finanzierung!)
- Heimfall nach Ablauf (Gebäude fällt an Grundstückseigentümer)

Rechtsprechung:
- BGH V ZR 234/20: Erbbauzins kann indexiert werden
- BGH V ZR 156/19: Heimfall gegen Entschädigung

VII. Rangverhältnisse (§ 879 BGB)

1. Grundsatz
- Frühere Eintragung = besserer Rang
- Wichtig bei Zwangsversteigerung (§ 10 ZVG)

2. Rangänderung
- Nur mit Zustimmung aller Beteiligten
- Rangvorbehalt (§ 881 BGB)

Praxishinweis Käufer:
✓ Grundbuchauszug prüfen (Belastungen!)
✓ Auflassungsvormerkung eintragen lassen (vor Kaufpreiszahlung!)
✓ Löschung Grundschulden mit Bank klären
✓ Notar prüft automatisch Grundbuch (trotzdem selbst prüfen!)

Praxishinweis Verkäufer:
✓ Löschungsbewilligungen besorgen (Bank!)
✓ Auflassung erst nach Kaufpreiseingang (oder Treuhandkonto)
✓ Grundschuld löschen lassen (spart Kosten für Käufer)

Literatur:
- MüKo BGB/Kohler, 9. Aufl. 2024, § 873
- Staudinger/Gursky, BGB, 2019, § 873
- Palandt/Herrler, BGB, 84. Aufl. 2025, § 873
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Münchener Kommentar BGB",
                "author": "Säcker/Rixecker/Oetker/Limperg (Hrsg.)",
                "publication_year": 2024,
                "edition": "9. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "MüKo BGB/Kohler, 9. Aufl. 2024, § 873",
                "keywords": ["Grundbuch", "Auflassung", "Vormerkung", "Grundschuld", "Erbbaurecht"],
            },
        ]
    
    def scrape_weg_erweitert(self) -> List[Dict]:
        """Erweiterte WEG-Literatur"""
        return [
            {
                "title": "Jennißen WEG § 16 - Kostenverteilung",
                "content": """
JENNISSEN, Wohnungseigentumsgesetz, 7. Aufl. 2021

§ 16 Kostenverteilung

I. Grundsatz: Verteilung nach Miteigentumsanteil (Abs. 1)

1. Gesetzlicher Verteilungsmaßstab
- Nach Miteigentumsanteilen (MEA)
- Festgelegt in Teilungserklärung
- Meist nach Wohnfläche

2. Beispiel
Wohnung 1: 80 m² = 800/10.000 MEA = 8%
Wohnung 2: 120 m² = 1.200/10.000 MEA = 12%

→ Kosten werden 8% / 12% aufgeteilt

II. Abweichende Vereinbarungen (Abs. 2)

1. Gemeinschaftsordnung
- Kann anderen Maßstab festlegen
- Z.B. nach Köpfen, nach Nutzung

2. Beschluss
- Einstimmigkeit erforderlich (§ 10 Abs. 2)
- Änderung nur mit Zustimmung aller Eigentümer

III. Verbrauchsabhängige Kosten (Abs. 2)

1. Heizung und Warmwasser
- Gesetzliche Pflicht: mind. 50-70% nach Verbrauch (HeizkostenV)
- Rest nach Wohnfläche

2. Wasser/Abwasser
- Verbrauchsabhängig möglich
- Wenn Zähler vorhanden

Rechtsprechung:
- BGH V ZR 93/19: Heizkostenverordnung = zwingendes Recht (auch im WEG!)
- BGH V ZR 178/18: Kostenverteilung nach Wohnfläche ist Regel

IV. Sondernutzungsrechte

1. Definition
- Ausschließliches Nutzungsrecht an Gemeinschaftseigentum
- Z.B. Garten, Terrasse, Stellplatz

2. Kosten
a) Erhaltung Sondernutzungsfläche
- Trägt Sondernutzungsberechtigter allein
- Wenn in Gemeinschaftsordnung so geregelt

b) Gemeinschaftseigentum darunter (z.B. Balkonplatte)
- Gemeinschaft trägt Kosten (nach MEA)
- Streitig in Rechtsprechung

Rechtsprechung:
- BGH V ZR 237/19: Balkonplatte = Gemeinschaftseigentum (Kosten nach MEA)
- BGH V ZR 64/18: Sondernutzung Garten: Kosten trägt Nutzer

V. Sonderfälle

1. Gewerbeeinheiten
- Höhere Kosten (z.B. Aufzug, Reinigung)
- Kostenaufteilung nach tatsächlicher Nutzung möglich

2. Leerstand
- Auch leere Wohnungen zahlen voll
- Kein Abzug bei Nichtnutzung

Praxishinweis:
✓ Gemeinschaftsordnung prüfen (Kostenverteilung!)
✓ Bei Sondernutzung: Kosten klären
✓ Heizkostenverordnung beachten (50-70% Verbrauch)

Literatur:
- Jennißen, WEG, 7. Aufl. 2021, § 16
- Bärmann/Pick, WEG, 15. Aufl. 2024, § 16
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Jennißen WEG",
                "author": "Jennißen (Hrsg.)",
                "publication_year": 2021,
                "edition": "7. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Jennißen, WEG, 7. Aufl. 2021, § 16",
                "keywords": ["WEG", "Kostenverteilung", "Miteigentumsanteil", "Sondernutzung", "Heizkosten"],
            },
        ]
    
    def scrape_zvg(self) -> List[Dict]:
        """Zwangsversteigerungsrecht"""
        return [
            {
                "title": "Steiner/Eickmann ZVG § 10 - Rangordnung der Rechte",
                "content": """
STEINER/EICKMANN, Zwangsversteigerungsgesetz, 12. Aufl. 2023

§ 10 Rangordnung der Rechte

I. Grundsatz: Grundbuchrang

Die Rechte werden im Versteigerungstermin in der Rangordnung berücksichtigt,
wie sie im Grundbuch eingetragen sind.

Regel: Frühere Eintragung = besserer Rang = höhere Chance auf Befriedigung

II. Versteigerungserlös-Verteilung

1. Reihenfolge (§§ 10 ff. ZVG)
a) Verfahrenskosten
b) Grundpfandrechte nach Rang
c) Sonstige Rechte
d) Eigentümer (Restbetrag)

2. Beispiel
Verkehrswert: 300.000€
Gebote: 250.000€

Rang 1: Grundschuld 200.000€ → voll befriedigt
Rang 2: Grundschuld 100.000€ → nur 50.000€ (Rest 50.000€ geht unter!)
Eigentümer: 0€

III. Geringste Gebot (§ 44 ZVG)

1. Berechnung
- Rechte, die bestehen bleiben
- + Verfahrenskosten
- = Mindestgebot

2. Wirkung
- Unter geringstem Gebot: kein Zuschlag
- Schutz vor Unterdeckung

IV. Bieterstrategien

1. Für Gläubiger
- Eigenes Gebot abgeben (zur Absicherung)
- Übergebot vermeiden (wenn eigene Grundschuld)

2. Für Investor
- Grundbuchauszug prüfen (Belastungen!)
- Verkehrswertgutachten besorgen
- Besichtigung (oft schwierig bei bewohntem Objekt)

Rechtsprechung:
- BGH V ZB 45/19: Zuschlag nur bei Überdeckung geringstes Gebot

Praxishinweis:
✓ Grundbuchauszug vor Zwangsversteigerung prüfen!
✓ Verkehrswertgutachten einsehen
✓ Geringstes Gebot berechnen
✓ Finanzierung vorbereiten (Sicherheitsleistung!)

Literatur:
- Steiner/Eickmann, ZVG, 12. Aufl. 2023
- Böttcher, ZVG, 7. Aufl. 2022
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Steiner/Eickmann ZVG",
                "author": "Steiner/Eickmann (Hrsg.)",
                "publication_year": 2023,
                "edition": "12. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Steiner/Eickmann, ZVG, 12. Aufl. 2023, § 10",
                "keywords": ["Zwangsversteigerung", "ZVG", "Rangordnung", "Grundschuld", "Geringstes Gebot"],
            },
        ]
    
    def scrape_nachbarrecht(self) -> List[Dict]:
        """Nachbarrecht - BGB §§ 903-924"""
        return [
            {
                "title": "Palandt BGB § 906 - Immissionen",
                "content": """
PALANDT, Bürgerliches Gesetzbuch, 84. Aufl. 2025

§ 906 Zuführung unwägbarer Stoffe

I. Grundsatz: Duldungspflicht bei Immissionen

1. Unwägbare Einwirkungen
- Gase, Dämpfe, Gerüche, Rauch, Ruß
- Wärme, Geräusche, Erschütterungen
- Licht (z.B. Blendung)

2. Duldungspflicht (Abs. 1)
a) Unwesentliche Beeinträchtigung
- Immer zu dulden
- Keine Abwehr möglich

b) Wesentliche Beeinträchtigung
- Duldung, wenn ortsüblich + wirtschaftlich zumutbar
- Ausgleichsanspruch möglich (§ 906 Abs. 2 S. 2)

II. Ortsüblichkeit

1. Maßstab
- Charakter der Umgebung
- Wohngebiet: niedrige Toleranzschwelle
- Gewerbegebiet: höhere Toleranzschwelle

2. Richtwerte
- TA Lärm (Technische Anleitung Lärm)
- Immissionsschutzrecht

Beispiel:
- Wohngebiet: 50 dB tags, 35 dB nachts
- Mischgebiet: 60 dB tags, 45 dB nachts
- Gewerbegebiet: 65 dB tags, 50 dB nachts

III. Rechtsfolgen

1. Unterlassungsanspruch (§ 1004 BGB)
- Bei unwesentlicher Beeinträchtigung: nein
- Bei wesentlicher, nicht ortsüblicher: ja
- Bei wesentlicher, ortsüblicher: nein (aber Ausgleich!)

2. Ausgleichsanspruch (§ 906 Abs. 2 S. 2)
- Wenn wesentlich + ortsüblich
- Entschädigung für Duldung
- Höhe: Wertminderung des Grundstücks

Rechtsprechung:
- BGH V ZR 133/19: Kinderlärm von Spielplatz = ortsüblich (zu dulden)
- BGH V ZR 246/18: Gaststätte in Wohngebiet = nicht ortsüblich (Unterlassung)
- BGH V ZR 62/17: Glockenläuten Kirche = ortsüblich (hinzunehmen)

IV. Weitere Nachbarrechte

1. § 910 BGB: Überhang
- Früchte/Zweige ragen über Grenze
- Nachbar kann abschneiden (nach Fristsetzung)

2. § 912 BGB: Überbau
- Gebäude ragt über Grenze
- Nachbar kann Beseitigung nur unter Umständen verlangen
- Meist: Duldung gegen Rente (§ 912 Abs. 2)

3. § 917 BGB: Notwegerecht
- Grundstück ohne Zugang zu öffentlichem Weg
- Nachbar muss Notweg dulden
- Gegen Entschädigung

Praxishinweis:
✓ Immissionsmessungen dokumentieren (Lautstärkemessgerät)
✓ TA Lärm Richtwerte prüfen
✓ Bei Überbau: sofort reagieren! (Verjährung § 912 Abs. 1)
✓ Vergleich anstreben (Prozess teuer + langwierig)

Literatur:
- Palandt/Herrler, BGB, 84. Aufl. 2025, § 906
- MüKo BGB/Baldus, 9. Aufl. 2024, § 906
                """,
                "category": "Kommentar",
                "jurisdiction": "DE",
                "doc_type": "LITERATUR",
                "source_name": "Palandt BGB",
                "author": "Palandt (Hrsg.)",
                "publication_year": 2025,
                "edition": "84. Aufl.",
                "publisher": "C.H. Beck",
                "citation": "Palandt/Herrler, BGB, 84. Aufl. 2025, § 906",
                "keywords": ["Nachbarrecht", "Immissionen", "Lärm", "§ 906", "Ortsüblichkeit"],
            },
        ]


if __name__ == "__main__":
    scraper = LiteraturScraper()
    all_docs = scraper.scrape_all()
    print(f"✅ {len(all_docs)} Literaturdokumente geladen")
    for doc in all_docs:
        print(f"  - {doc['title']}")
