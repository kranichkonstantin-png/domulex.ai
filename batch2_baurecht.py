#!/usr/bin/env python3
"""Batch 2: Baurecht Spezifika - 50 Dokumente"""

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
        "title": "Baugenehmigung: Verfahrensdauer",
        "content": """Bearbeitungszeit je nach Bundesland und Bauvorhaben 2-6 Monate. Vereinfachtes Verfahren: Schneller (4-8 Wochen). Freistellungsverfahren: Keine formale Genehmigung nötig. Bauvoranfrage: Klärt Genehmigungsfähigkeit vorab. Beschleunigung: Vollständige Unterlagen, professioneller Bauantrag. Genehmigungsfiktion: Nach Fristablauf ohne Bescheid (nur bei bestimmten Bundesländern). Wichtig: Rechtzeitig beantragen!""",
        "category": "Baurecht",
        "subcategory": "Baugenehmigung"
    },
    {
        "title": "Abstandsflächen: Berechnung",
        "content": """Abstandsflächentiefe = 0,4 x Wandhöhe (je nach LBO unterschiedlich, Bayern 1H, Berlin 0,4H). Mindestabstand: 2,5-3m zur Grundstücksgrenze. Ausnahmen: Grenzbebauung bei Reihenhäusern, geringer Abstand bei niedriger Gebäudehöhe. Nachbareinwilligung: Kann Abweichung ermöglichen. Berechnung: Von Außenwand Oberkante Gelände. Wichtig: Landesbauordnung prüfen!""",
        "category": "Baurecht",
        "subcategory": "Abstandsflächen"
    },
    {
        "title": "Bebauungsplan: Grundflächenzahl (GRZ)",
        "content": """GRZ gibt zulässige Überbauung an (Verhältnis bebaute Fläche zu Grundstücksfläche). GRZ 0,4 = 40% bebaubar. Überschreitung: Bis zu 50% durch Nebenanlagen, Stellplätze, Zufahrten (§ 19 Abs. 4 BauNVO). Berechnung: Gebäudefläche + Terrasse + Garage. Versiegelung: Relevant für Regenwasser. Unterschreitung: Zulässig. Wichtig für Bauplanung!""",
        "category": "Baurecht",
        "subcategory": "Bebauungsplan"
    },
    {
        "title": "Bebauungsplan: Geschossflächenzahl (GFZ)",
        "content": """GFZ gibt zulässige Geschossfläche an (Verhältnis Geschossfläche zu Grundstücksfläche). GFZ 1,2 = 120% des Grundstücks als Geschossfläche. Beispiel: 500m² Grundstück mit GFZ 1,2 = 600m² Geschossfläche möglich (z.B. 2 Etagen á 300m²). Kellergeschoss: Zählt meist nicht mit. Dachgeschoss: Teilweise anrechenbar. Wichtig für Bebauungsdichte!""",
        "category": "Baurecht",
        "subcategory": "Bebauungsplan"
    },
    {
        "title": "Baulasten: Arten und Wirkung",
        "content": """Baulast: Öffentlich-rechtliche Verpflichtung gegenüber Bauaufsicht. Arten: Abstandsflächenbaulast, Stellplatzbaulast, Anbaubaulast, Grenzbebauungsbaulast. Eintragung: Baulastenverzeichnis. Wirkung: Bindet auch Rechtsnachfolger. Löschung: Nur mit Zustimmung der Behörde. Kaufrelevant: Vor Kauf prüfen! Stellplätze: Verpflichtung auf anderem Grundstück.""",
        "category": "Baurecht",
        "subcategory": "Baulasten"
    },
    {
        "title": "Dachgeschossausbau: Genehmigung",
        "content": """Ausbau meist genehmigungspflichtig wenn Nutzungsänderung (Lagerraum zu Wohnraum). Anforderungen: Brandschutz, Schallschutz, Wärmedämmung, Rettungswege. Kniestockhöhe: Mindestens 2,30m Raumhöhe für Aufenthaltsräume. Stellplätze: Zusätzliche Wohnfläche kann mehr Stellplätze erfordern. Statik: Prüfung notwendig. WEG: Zustimmung der Eigentümergemeinschaft nötig.""",
        "category": "Baurecht",
        "subcategory": "Umbau"
    },
    {
        "title": "Nutzungsänderung: Genehmigung",
        "content": """Nutzungsänderung (Gewerbe zu Wohnen, Wohnen zu Büro) ist genehmigungspflichtig. Anforderungen: Je nach neuer Nutzung (Brandschutz, Schallschutz, Stellplätze). Bebauungsplan: Muss neue Nutzung zulassen. Bagatellgrenze: Kleine Änderungen ggf. genehmigungsfrei. Zweckentfremdungsverbot: In Großstädten bei Wohnraum beachten! WEG: Beschluss erforderlich.""",
        "category": "Baurecht",
        "subcategory": "Nutzungsänderung"
    },
    {
        "title": "Anbau und Erweiterung: Voraussetzungen",
        "content": """Anbau ist genehmigungspflichtig. Anforderungen: Abstandsflächen, GRZ/GFZ einhalten, Brandschutz, Statik. Vereinfachtes Verfahren: Bei kleinen Anbauten möglich. Nachbarzustimmung: Bei Grenzabstand-Unterschreitung. Baufenster: Bebauungsplan beachten. Altbestand: Bestandsschutz gilt, aber Erweiterung nach neuem Recht. Kosten: 0,5-1,5% der Bausumme.""",
        "category": "Baurecht",
        "subcategory": "Anbau"
    },
    {
        "title": "Schwarzbau: Konsequenzen",
        "content": """Schwarzbau ist Ordnungswidrigkeit oder Straftat. Konsequenzen: Bußgeld bis 50.000€, Nutzungsuntersagung, Rückbau, Freiheitsstrafe bei schweren Fällen. Verjährung: 30 Jahre bei formellen Mängeln. Legalisierung: Nachträgliche Baugenehmigung möglich wenn genehmigungsfähig. Käufer: Haftet mit! Wichtig: Vor Kauf Baugenehmigung prüfen. Versicherung: Kann Leistung verweigern.""",
        "category": "Baurecht",
        "subcategory": "Schwarzbau"
    },
    {
        "title": "Grenzbebauung: Voraussetzungen",
        "content": """Grenzbebauung ohne Abstand zur Grenze nur unter bestimmten Voraussetzungen. Anforderungen: Bebauungsplan erlaubt, Nachbarzustimmung, Brandwand, maximale Länge (15-20m je nach LBO). Baulast: Kann Grenzbebauung ermöglichen. Reihenhäuser: Klassischer Fall. Nachbarwand-Recht: § 912 BGB. Nicht bei offener Bauweise ohne Grund.""",
        "category": "Baurecht",
        "subcategory": "Grenzbebauung"
    },
    {
        "title": "Stellplatzpflicht: Regelungen",
        "content": """Stellplatzpflicht je nach Landesbauordnung und örtlicher Satzung. Berechnung: 1 Stellplatz pro Wohnung (variiert nach Wohnungsgröße, Lage). Ausnahmen: ÖPNV-Nähe, Carsharing. Ablösung: Zahlung statt Bau (1.500-30.000€ je Stadt). E-Ladestation: Zunehmend verpflichtend (ab 2025). Fahrradstellplätze: Zusätzlich oft gefordert. Wichtig: Frühzeitig prüfen!""",
        "category": "Baurecht",
        "subcategory": "Stellplätze"
    },
    {
        "title": "Brandschutz: Anforderungen Mehrfamilienhaus",
        "content": """Brandschutzanforderungen nach Landesbauordnung. Rettungswege: 2. Rettungsweg ab Gebäudeklasse 3 (>7m). Rauchwarnmelder: Pflicht in allen Bundesländern. Feuerwiderstand: F30 bis F90 je nach Gebäudeklasse. Fluchtwege: Breite, Beschilderung. Feuerlöscher: Empfohlen, teils Pflicht. Prüfung: Alle 3-5 Jahre. Nachrüstung: Bestandsschutz teilweise aufgehoben.""",
        "category": "Baurecht",
        "subcategory": "Brandschutz"
    },
    {
        "title": "Wärmedämmung: Gesetzliche Pflichten",
        "content": """Dämmung nach GEG (Gebäudeenergiegesetz). Neubau: KfW-55-Standard oder besser. Altbau: Bei Austausch Außenwand, Dach, Fenster nachrüsten. U-Wert: Max. 0,24 W/(m²K) für Außenwand. Ausnahmen: Denkmalschutz, Kleindenkmal, unwirtschaftlich. Förderung: KfW, BAFA. Sanierungspflicht: Beim Eigentümerwechsel innerhalb 2 Jahren.""",
        "category": "Baurecht",
        "subcategory": "Energieeffizienz"
    },
    {
        "title": "Barrierefreiheit: Bauliche Anforderungen",
        "content": """Barrierefreiheit nach DIN 18040. Neubau: Ab 3 Wohnungen teilweise barrierefrei. Öffentliche Gebäude: Vollständig barrierefrei. Anforderungen: Stufenloser Zugang, Aufzug ab 3. OG, Türbreite 90cm, Bewegungsflächen 150x150cm. Badezimmer: Bodengleiche Dusche, unterfahrbarer Waschtisch. Förderung: KfW-Programm 455-B. Nachrüstung: Bei Neuvermietung empfohlen.""",
        "category": "Baurecht",
        "subcategory": "Barrierefreiheit"
    },
    {
        "title": "Schallschutz: Anforderungen",
        "content": """Schallschutz nach DIN 4109. Luftschallschutz: Wand zwischen Wohnungen min. 53 dB. Trittschallschutz: Max. 53 dB. Erhöhter Schallschutz: VDI 4100 empfiehlt besser (Stufe II-III). Neubau: Höhere Anforderungen als Altbau. Nachrüstung: Nur bei Modernisierung. Prüfung: Messungen nach Fertigstellung. Wichtig: In Mehrfamilienhäusern!""",
        "category": "Baurecht",
        "subcategory": "Schallschutz"
    },
    {
        "title": "Denkmalschutz: Auflagen",
        "content": """Denkmalschutz schränkt Veränderungen ein. Genehmigung: Denkmalschutzbehörde zusätzlich zu Bauamt. Änderungen: Fassade, Fenster, Dach nur eingeschränkt. Steuervorteile: Erhöhte AfA (9% über 8 Jahre), Sanierungskosten absetzbar. Zuschüsse: Denkmalschutz-Förderung. Energetische Sanierung: Ausnahmen vom GEG. Kaufpreis: Oft niedriger, aber Sanierungskosten höher.""",
        "category": "Baurecht",
        "subcategory": "Denkmalschutz"
    },
    {
        "title": "Baugenehmigung: Unterlagen",
        "content": """Erforderliche Unterlagen: Bauantrag (amtliches Formular), Lageplan, Bauzeichnungen (Grundrisse, Ansichten, Schnitte), Baubeschreibung, Standsicherheitsnachweis, Wärmeschutznachweis, Entwässerungsplan, Baumbestandsplan. Zusätzlich: Nachbarunterschriften (bei Grenzabstand-Unterschreitung), Brandschutznachweis. Vollständigkeit: Verzögerung bei fehlenden Unterlagen. Architekt/Bauingenieur: Erstellung durch Fachmann empfohlen.""",
        "category": "Baurecht",
        "subcategory": "Baugenehmigung"
    },
    {
        "title": "Teilungsgenehmigung: Voraussetzungen",
        "content": """Teilungsgenehmigung bei Aufteilung Grundstück. Anforderungen: Mindestgröße (300-800m² je nach Region), Zufahrt, Versorgung. Erschließung: Alle Grundstücke müssen erschlossen sein. Bebauungsplan: Muss Teilung zulassen. Gebäude: Bei Teilung mit Gebäude auch Eigentumswohnung möglich. Kosten: 100-500€. Grundbuch: Neue Flurstücke.""",
        "category": "Baurecht",
        "subcategory": "Grundstücksteilung"
    },
    {
        "title": "Bauvoranfrage: Nutzen",
        "content": """Bauvoranfrage klärt Genehmigungsfähigkeit vorab ohne detaillierten Bauantrag. Inhalt: Grundsatzfragen (Bebaubarkeit, Abstandsflächen, GRZ/GFZ). Geltungsdauer: 3 Jahre. Kosten: 50-300€. Vorteil: Planungssicherheit vor Grundstückskauf. Bindungswirkung: Behörde muss bei Bauantrag entsprechend entscheiden. Wichtig: Bei teurem Grundstück oder unklarer Rechtslage.""",
        "category": "Baurecht",
        "subcategory": "Bauvoranfrage"
    },
    {
        "title": "Baugenehmigung: Geltungsdauer",
        "content": """Baugenehmigung gilt 3-5 Jahre je nach Bundesland. Verlängerung: Auf Antrag meist 1-2 Jahre. Beginn: Mit Baubeginn, nicht Fertigstellung. Verfallende Genehmigung: Neu beantragen bei Rechtsänderung nach altem Recht möglich (Bestandsschutz). Wichtig: Rechtzeitig bauen! Fristverlängerung: Vor Ablauf beantragen.""",
        "category": "Baurecht",
        "subcategory": "Baugenehmigung"
    },
    {
        "title": "Rohbauabnahme: Zeitpunkt",
        "content": """Rohbauabnahme nach Fertigstellung Rohbau vor Innenausbau. Inhalt: Prüfung Maße, Fenster/Türöffnungen, Elektro-/Wasser-/Heizungsinstallation vorbereitet, Statik. Beteiligte: Bauherr, Architekt, Bauleiter, ggf. Sachverständiger. Protokoll: Mängel dokumentieren. Zahlung: Nächste Rate erst nach Abnahme. Versicherung: Rohbau gegen Elementarschäden versichern.""",
        "category": "Baurecht",
        "subcategory": "Bauabnahme"
    },
    {
        "title": "Schlussabnahme: Bedeutung",
        "content": """Schlussabnahme markiert Fertigstellung und Übergabe. Gewährleistung: Beginnt mit Abnahme (4-5 Jahre). Fälligkeit: Schlusszahlung nach Abnahme. Mängel: Im Protokoll dokumentieren, Frist zur Beseitigung setzen. Vorbehaltlose Abnahme: Nur bei mängelfreiem Werk. Teilabnahme: Einzelne Gewerke vor Schlussabnahme möglich. Wichtig: Sachverständigen hinzuziehen!""",
        "category": "Baurecht",
        "subcategory": "Bauabnahme"
    },
    {
        "title": "VOB/B: Bauvertrag nach Verdingungsordnung",
        "content": """VOB/B regelt Bauvertrag professionell. Vorteil: Detaillierte Regelungen, kürzere Gewährleistung (4 Jahre statt 5). Nachteil: Günstiger für Auftragnehmer. Abnahme: Formalisiert. Behinderungsanzeige: Pflicht bei Verzögerung. Kündigung: Regelungen für beide Seiten. Anwendung: Meist bei größeren Projekten, gewerblichen Bauherren. BGB: Alternativ bei Privatkunden.""",
        "category": "Baurecht",
        "subcategory": "Bauvertrag"
    },
    {
        "title": "Bauvertrag: Zahlungsplan",
        "content": """Zahlungsplan nach MaBV (Makler- und Bauträgerverordnung) bei Bauträgern. Raten: Max. 7 nach Baufortschritt (u.a. nach Bodenplatte, Rohbau, Dach, Fenster). Sicherheit: Keine Vorauszahlung ohne Baufortschritt. Bauträger: Strenge Regelung. Privater Bauherr: Freie Vereinbarung möglich. Wichtig: Nie mehr zahlen als gebaut!""",
        "category": "Baurecht",
        "subcategory": "Bauvertrag"
    },
    {
        "title": "Bauleiter: Aufgaben und Haftung",
        "content": """Bauleiter koordiniert Bauausführung. Aufgaben: Überwachung Qualität, Termine, Kosten, Koordination Gewerke. Haftung: Bei Pflichtverletzung gegenüber Bauherrn. Abgrenzung: Architekt plant, Bauleiter führt aus. Kosten: 5-10% der Baukosten. Wichtig: Klare Verträge, Haftpflichtversicherung. Bei großen Projekten zwingend.""",
        "category": "Baurecht",
        "subcategory": "Bauleitung"
    },
    {
        "title": "Architekt: Honorarordnung HOAI",
        "content": """HOAI (Honorarordnung für Architekten und Ingenieure) regelt Vergütung. Berechnung: Nach Anrechenbare Kosten, Honorarzonen, Leistungsphasen (1-9). Leistungsphasen: Grundlagenermittlung (1), Vorplanung (2), Entwurf (3), Genehmigung (4), Ausführung (5), Vorbereitung Vergabe (6), Mitwirkung Vergabe (7), Bauüberwachung (8), Betreuung (9). Seit 2021: Nur Orientierung, frei verhandelbar. Üblich: 10-15% der Baukosten.""",
        "category": "Baurecht",
        "subcategory": "Architektenvertrag"
    },
    {
        "title": "Baugrundgutachten: Bedeutung",
        "content": """Baugrundgutachten (Bodengutachten) untersucht Tragfähigkeit, Grundwasser, Altlasten. Inhalt: Bohrungen, Laboranalysen, Empfehlungen für Gründung. Kosten: 500-2.500€ je nach Grundstück. Wichtig: Vor Grundstückskauf bei unbekanntem Boden. Haftung: Bauherr trägt Risiko bei fehlendem Gutachten. Altlasten: Können Grundstück unverkäuflich machen.""",
        "category": "Baurecht",
        "subcategory": "Baugrundgutachten"
    },
    {
        "title": "Nachbarschutz: Abwehransprüche",
        "content": """Nachbar kann gegen baurechtswidrige Vorhaben vorgehen. Voraussetzung: Eigene Rechtsverletzung (Abstandsfläche, Verschattung). Widerspruch: Gegen Baugenehmigung innerhalb 1 Monat. Klage: Vor Verwaltungsgericht. Unterlassung: Bei Schwarzbau. Beseitigungsanspruch: Bei schwerwiegenden Verstößen. Wichtig: Nachbar hat starke Position!""",
        "category": "Baurecht",
        "subcategory": "Nachbarrecht"
    },
    {
        "title": "Bauordnungsrecht vs. Bauplanungsrecht",
        "content": """Bauordnungsrecht (Landesbauordnung): Wie gebaut wird (Statik, Brandschutz, Abstandsflächen). Bauplanungsrecht (BauGB, BauNVO): Ob und was gebaut wird (Bebauungsplan, Gebietsart). Zuständigkeit: Bauordnung Landesrecht, Bauplanung Bundesrecht. Genehmigung: Beide Bereiche werden geprüft. Wichtig: Beide beachten!""",
        "category": "Baurecht",
        "subcategory": "Grundlagen"
    },
    {
        "title": "Innenbereich vs. Außenbereich",
        "content": """Innenbereich (§ 34 BauGB): Zusammenhängend bebaut, einfügt in Umgebung. Außenbereich (§ 35 BauGB): Privilegierte Vorhaben (Landwirtschaft) oder Ausnahmen. Bebauungsplan: Spezielle Regelung geht vor. Zulässigkeit: Innenbereich großzügiger. Wichtig: Unterscheidung für Genehmigungsfähigkeit!""",
        "category": "Baurecht",
        "subcategory": "Bauplanung"
    },
    {
        "title": "Baugebiet-Arten: Überblick",
        "content": """BauNVO unterscheidet: WR (reines Wohngebiet), WA (allgemeines Wohngebiet), WB (besonderes Wohngebiet), MD (Dorfgebiet), MI (Mischgebiet), MK (Kerngebiet), GE (Gewerbegebiet), GI (Industriegebiet), SO (Sondergebiet). Zulässigkeit: Je nach Gebiet unterschiedliche Nutzungen. Wichtig: Bebauungsplan prüfen vor Kauf!""",
        "category": "Baurecht",
        "subcategory": "Baugebiete"
    },
    {
        "title": "Offene vs. geschlossene Bauweise",
        "content": """Offene Bauweise: Gebäude mit seitlichem Grenzabstand, max. 50m Länge. Geschlossene Bauweise: Gebäude an Grundstücksgrenze (Reihenhäuser). Abweichende Bauweise: z.B. Gebäudelänge über 50m in offener Bauweise. Wichtig: Bebauungsplan gibt vor!""",
        "category": "Baurecht",
        "subcategory": "Bauweise"
    },
    {
        "title": "Vollgeschoss: Definition",
        "content": """Vollgeschoss nach Landesbauordnung: Geschoss mit mindestens 2/3 über Geländeoberfläche, Höhe mindestens 2,30m. Dachgeschoss: Oft kein Vollgeschoss (Drempel zu niedrig). Kellergeschoss: Meist kein Vollgeschoss. Wichtig: Für GFZ-Berechnung, Gebäudeklasse!""",
        "category": "Baurecht",
        "subcategory": "Geschosse"
    },
    {
        "title": "Gebäudeklassen: Einteilung",
        "content": """Gebäudeklassen nach Musterbauordnung: GK1 (freistehend, max. 7m hoch), GK2 (max. 7m, max. 400m² Grundfläche), GK3 (max. 7m), GK4 (max. 13m), GK5 (über 13m). Relevanz: Brandschutz, Rettungswege, Statik-Anforderungen steigen mit Klasse. Wichtig: Bestimmt Aufwand und Kosten!""",
        "category": "Baurecht",
        "subcategory": "Gebäudeklassen"
    },
    {
        "title": "Rettungsweg: 2. Rettungsweg",
        "content": """2. Rettungsweg ab Gebäudeklasse 3 erforderlich. Möglichkeiten: Außentreppe, Balkon mit Leiter, Feuerwehrleiter (max. 8m). Anforderungen: Feuerbeständig, min. 90cm breit, beleuchtet. Nachrüstung: Bei Nutzungsänderung oft erforderlich. Wichtig: Bei Ausbau Dachgeschoss prüfen!""",
        "category": "Baurecht",
        "subcategory": "Brandschutz"
    },
    {
        "title": "Brandwand: Anforderungen",
        "content": """Brandwand verhindert Brandausbreitung zwischen Gebäuden oder Gebäudeteilen. Anforderungen: F90 (90 Min. Feuerwiderstand), 30cm über Dach, keine Öffnungen. Grenzbebauung: Zwingend erforderlich. Doppelhaus: Zwischen Hälften. Materialien: Beton, Ziegel, Kalksandstein. Kosten: 150-300€/m².""",
        "category": "Baurecht",
        "subcategory": "Brandschutz"
    },
    {
        "title": "Wohnfläche: Berechnung nach WoFlV",
        "content": """Wohnflächenverordnung (WoFlV) regelt Berechnung. Volle Anrechnung: Ab 2m Höhe. Halbe Anrechnung: 1-2m Höhe (Dachschrägen). Keine Anrechnung: Unter 1m, Keller, Abstellräume außerhalb Wohnung. Balkone/Terrassen: 25-50% je nach Wert. Wichtig: Für Miete, Nebenkosten, Wohnungsgröße!""",
        "category": "Baurecht",
        "subcategory": "Wohnfläche"
    },
    {
        "title": "Baunebenkosten: Überblick",
        "content": """Baunebenkosten ca. 15-20% der Baukosten. Positionen: Architekt (10-15%), Statiker (1-2%), Bodengutachten (0,5%), Baugenehmigung (0,2-0,5%), Versicherungen (0,5%), Außenanlagen (5-10%), Anschlüsse (2-5%). Wichtig: Frühzeitig einkalkulieren! Oft unterschätzt.""",
        "category": "Baurecht",
        "subcategory": "Baukosten"
    },
    {
        "title": "Bauherrenhaftpflicht: Notwendigkeit",
        "content": """Bauherrenhaftpflicht schützt vor Schäden Dritter während Bauphase. Abdeckung: Personenschäden, Sachschäden, Vermögensschäden. Kosten: 100-300€ für Bauzeit. Wichtig: Auch bei Eigenleistung! Bauhelfer: Separat versichern (Bauhelfer-Unfallversicherung). Bei Bauträger: Meist inklusive.""",
        "category": "Baurecht",
        "subcategory": "Versicherung"
    },
    {
        "title": "Feuerversicherung Rohbau: Wann?",
        "content": """Rohbauversicherung ab Baubeginn sinnvoll. Abdeckung: Feuer, Blitzschlag, Explosion, Leitungswasser. Kosten: 50-150€ pro Jahr. Übergang: In normale Gebäudeversicherung nach Fertigstellung. Wichtig: Keine Versicherungslücke! Bauträger: Meist inklusive.""",
        "category": "Baurecht",
        "subcategory": "Versicherung"
    },
    {
        "title": "Bauzeiten: Gesetzliche Regelungen",
        "content": """Baustellenlärm werktags 7-20 Uhr (je nach Gemeinde). Sonn- und Feiertage: Generell verboten. Ausnahmen: Mit Sondergenehmigung. Nachtarbeit: Nur bei zwingender Notwendigkeit. Bußgeld: Bei Verstößen bis 50.000€. Nachbarn: Können Unterlassung verlangen. Wichtig: Zeitplan einhalten!""",
        "category": "Baurecht",
        "subcategory": "Baustellenbetrieb"
    },
    {
        "title": "Baustelleneinrichtung: Genehmigung",
        "content": """Baustelleneinrichtung (Container, Kran, Gerüst) teilweise genehmigungspflichtig. Öffentlicher Raum: Sondernutzungserlaubnis erforderlich. Absperrung: Verkehrssicherungspflicht. Kosten: 100-500€ für Genehmigung. Halteverbot: Separat beantragen. Wichtig: Rechtzeitig planen!""",
        "category": "Baurecht",
        "subcategory": "Baustellenbetrieb"
    },
    {
        "title": "Baufertigstellungsanzeige: Pflicht",
        "content": """Fertigstellungsanzeige nach Baufertigstellung an Bauaufsicht. Inhalt: Bestätigung ordnungsgemäße Ausführung. Frist: Meist 2 Wochen nach Fertigstellung. Konsequenz: Abnahme durch Bauaufsicht möglich. Nutzung: Erst nach Freigabe. Wichtig: Nicht vergessen, sonst Bußgeld!""",
        "category": "Baurecht",
        "subcategory": "Bauabnahme"
    },
    {
        "title": "Abgeschlossenheitsbescheinigung: WEG",
        "content": """Abgeschlossenheitsbescheinigung bestätigt Aufteilung in Wohnungen. Voraussetzung: Bauliche Trennung (Wände, Decken, Türen). Erteilung: Bauaufsicht nach Prüfung. Kosten: 100-300€. Grundbuch: Erforderlich für Eintragung Wohnungseigentum. Wichtig: Vor Verkauf als Eigentumswohnung!""",
        "category": "Baurecht",
        "subcategory": "WEG"
    },
    {
        "title": "Erschließung: Beitragspflicht",
        "content": """Erschließungsbeitrag finanziert erstmalige Herstellung von Straße, Wasser, Abwasser. Höhe: Nach Frontmeter oder Grundstücksgröße. Fälligkeit: Nach Fertigstellung, 4 Jahre Zahlungsfrist. Vorauszahlung: Oft möglich mit Rabatt. Ablösung: Zahlung aller zukünftigen Beiträge. Wichtig: Vor Grundstückskauf Auskunft einholen!""",
        "category": "Baurecht",
        "subcategory": "Erschließung"
    },
    {
        "title": "Baumfällung: Genehmigung",
        "content": """Baumfällung ab bestimmtem Stammumfang genehmigungspflichtig (meist 60-80cm in 1m Höhe, je nach Baumschutzsatzung). Ausnahmen: Obstbäume meist frei. Ersatzpflanzung: Oft gefordert. Fällzeit: 1. Oktober bis 28. Februar (Bundesnaturschutzgesetz). Strafe: Bis 50.000€ bei illegaler Fällung. Wichtig: Vor Kauf Baumbestand prüfen!""",
        "category": "Baurecht",
        "subcategory": "Naturschutz"
    },
    {
        "title": "Regenwasser: Versickerung und Gebühren",
        "content": """Regenwassergebühr für versiegelte Flächen. Berechnung: Nach m² Dach, Terrasse, Zufahrt. Versickerung: Kann Gebühren reduzieren (Versickerungsmulde, Rigole). Genehmigung: Versickerung teilweise genehmigungspflichtig. Regenwassernutzung: Für WC, Garten senkt Trinkwasserkosten. Wichtig: Frühzeitig planen!""",
        "category": "Baurecht",
        "subcategory": "Entwässerung"
    }
]

print("🚀 BATCH 2: BAURECHT SPEZIFIKA - START")
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

print("\n🔥 BATCH 2 COMPLETE! 🔥")
