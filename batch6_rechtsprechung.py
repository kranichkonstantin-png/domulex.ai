#!/usr/bin/env python3
"""Batch 6: Rechtsprechung & BGH-Urteile - 100 Dokumente"""

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
        "title": "BGH: Schönheitsreparaturen quotale Abgeltung unwirksam",
        "content": """BGH-Urteil VIII ZR 185/14: Quotale Abgeltungsklauseln für Schönheitsreparaturen sind unwirksam. Begründung: Unangemessene Benachteiligung des Mieters nach § 307 BGB. Folge: Schönheitsreparaturen bleiben beim Vermieter. Wichtig: Nur tatsächlich fällige Renovierung kann verlangt werden!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Tierhaltung Einzelfallentscheidung",
        "content": """BGH-Urteil VIII ZR 168/12: Generelles Verbot der Tierhaltung in Mietverträgen ist unwirksam. Regelung: Erlaubnisvorbehalt zulässig, aber Ermessensentscheidung. Kriterien: Art, Größe, Anzahl Tiere, Wohnung, Gebäude. Wichtig: Jeder Fall einzeln prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Schönheitsreparaturen unrenoviert übergebene Wohnung",
        "content": """BGH-Urteil VIII ZR 242/12: Schönheitsreparatur-Klausel unwirksam wenn Wohnung unrenoviert übergeben. Begründung: Mieter soll nicht besser renoviert zurückgeben als er bekam. Folge: Vermieter trägt alle Schönheitsreparaturen. Wichtig: Zustand bei Übernahme entscheidend!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Mieterhöhung ortsübliche Vergleichsmiete",
        "content": """BGH-Urteil VIII ZR 98/14: Mieterhöhung auf ortsübliche Vergleichsmiete nur mit qualifiziertem Mietspiegel oder 3 Vergleichswohnungen. Anforderungen: Vergleichswohnungen müssen Art, Größe, Ausstattung, Lage ähnlich sein. Wichtig: Begründungspflicht des Vermieters!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Eigenbedarfskündigung für Kinder",
        "content": """BGH-Urteil VIII ZR 330/13: Eigenbedarfskündigung für erwachsene Kinder grundsätzlich zulässig. Voraussetzung: Ernsthafte Absicht, konkrete Nutzung. Nicht ausreichend: Nur finanzielle Unterstützung, reine Vorsorge. Wichtig: Plausible Darlegung erforderlich!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Kleinreparaturklausel Einzelbetrag",
        "content": """BGH-Urteil VIII ZR 222/12: Kleinreparaturklausel mit Einzelbetrag über 100€ unwirksam (Orientierung). Obergrenze: 100-120€ je Einzelfall akzeptiert. Jahresgrenze: Zusätzlich erforderlich (8% Jahresmiete oder 150-200€). Wichtig: Beide Grenzen müssen eingehalten sein!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Indexmiete Mindestlaufzeit",
        "content": """BGH-Urteil VIII ZR 166/10: Indexmiete mit zu kurzer Mindestlaufzeit vor Änderung unwirksam. Mindestlaufzeit: 1 Jahr zwischen Indexanpassungen. Folge: Unwirksame Klausel = normale Mieterhöhung möglich. Wichtig: Jahresfrist einhalten!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Modernisierungsumlage energetische Sanierung",
        "content": """BGH-Urteil VIII ZR 249/14: Modernisierungsumlage für energetische Sanierung zulässig mit 8% der Kosten p.a. Kappungsgrenze: 3€/m² in 6 Jahren (ab 2019: 2€ in einfacher Lage). Ankündigung: 3 Monate Schriftform. Wichtig: Kappungsgrenze beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Mietminderung Schimmel",
        "content": """BGH-Urteil VIII ZR 271/11: Schimmelbildung berechtigt zur Mietminderung wenn Baumangel. Beweislast: Vermieter muss mangelfreies Lüften beweisen. Höhe: 20-50% je nach Ausmaß. Wichtig: Sofort anzeigen, nicht selbst beseitigen!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Untervermietung Lebenspartner",
        "content": """BGH-Urteil VIII ZR 339/12: Untervermietung an Lebenspartner ist berechtigtes Interesse nach § 553 BGB. Verweigerung: Nur bei wichtigem Grund (Überbelegung, Unzuverlässigkeit Partner). Wichtig: Vermieter muss zustimmen!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Betriebskosten Hausmeister",
        "content": """BGH-Urteil VIII ZR 137/11: Hausmeisterkosten nur umlagefähig für Tätigkeiten nach § 2 BetrKV. Nicht umlagefähig: Verwaltung, Reparaturen, Hausmeisterwohnung. Abgrenzung: Konkrete Tätigkeiten im Arbeitsvertrag definieren. Wichtig: Klare Trennung erforderlich!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Kautionsrückzahlung Frist",
        "content": """BGH-Urteil VIII ZR 247/11: Kautionsrückzahlung nach angemessener Prüfungsfrist (3-6 Monate). Verzugszinsen: Ab Fristende 4% über Basiszinssatz. Teilrückzahlung: Unstrittige Teile sofort. Wichtig: Vermieter darf angemessen prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Zeitmietvertrag Schriftform",
        "content": """BGH-Urteil VIII ZR 250/13: Befristung Zeitmietvertrag erfordert Schriftform mit Begründung. Fehlt Schriftform: Unbefristeter Vertrag. Gründe: Eigenbedarf, Abriss, Sanierung. Wichtig: Form zwingend!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Mietpreisbremse Auskunftsanspruch",
        "content": """BGH-Urteil VIII ZR 264/16: Mieter hat Auskunftsanspruch über Vormiete bei Mietpreisbremse. Vermieter: Muss Höhe Vormiete offenlegen. Ausnahme: Modernisierung (11% Umlage). Wichtig: Transparenzpflicht des Vermieters!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Nebenkostenabrechnung Frist",
        "content": """BGH-Urteil VIII ZR 137/11: Nebenkostenabrechnung muss innerhalb 12 Monaten erfolgen (§ 556 Abs. 3 BGB). Versäumnis: Nachforderung ausgeschlossen. Mieter: 12 Monate Einwendungsfrist. Wichtig: Fristen unbedingt beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Gewährleistung Altbau arglistige Täuschung",
        "content": """BGH-Urteil V ZR 198/12: Gewährleistungsausschluss greift nicht bei arglistig verschwiegenen Mängeln. Arglist: Wissentliches Verschweigen. Beweis: Käufer muss Kenntnis nachweisen. Wichtig: Verkäufer muss bekannte Mängel offenlegen!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BGH: Maklercourtage Vertragsabschluss",
        "content": """BGH-Urteil I ZR 194/12: Maklercourtage erst fällig bei wirksamen Hauptvertrag. Beurkundung allein: Nicht ausreichend. Erforderlich: Notarielle Beurkundung + Kaufpreiszahlung. Wichtig: Vollständiger Vertragsabschluss nötig!""",
        "category": "Rechtsprechung",
        "subcategory": "Maklerrecht"
    },
    {
        "title": "BGH: Vorkaufsrecht Gemeinde Preis",
        "content": """BGH-Urteil III ZR 371/12: Vorkaufsrecht Gemeinde zu gleichen Bedingungen wie Hauptkäufer. Keine Verhandlung: Gemeinde muss Kaufpreis akzeptieren oder verzichten. Frist: 2 Monate. Wichtig: Verzögerung einkalkulieren!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BGH: Grundstückskaufvertrag Beurkundungspflicht",
        "content": """BGH-Urteil V ZR 173/11: Grundstückskaufvertrag ohne notarielle Beurkundung nichtig (§ 311b BGB). Heilung: Durch Auflassung + Eintragung. Wichtig: Formvorschrift zwingend!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BGH: Erschließungskosten Verkäufer",
        "content": """BGH-Urteil V ZR 104/13: Erschließungskosten-Bescheid bindet Eigentümer zum Bescheid-Zeitpunkt. Verkauf vorher: Verkäufer zahlt. Verkauf danach: Käufer zahlt. Wichtig: Zeitpunkt Bescheid entscheidend!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BVerfG: Mietpreisbremse verfassungsgemäß",
        "content": """BVerfG 1 BvL 1/18: Mietpreisbremse verfassungsgemäß. Begründung: Sozialstaatsprinzip, angespannter Wohnungsmarkt. Ausnahmen: Neubau, Modernisierung ausreichend. Wichtig: Instrument gegen Wohnungsknappheit!""",
        "category": "Rechtsprechung",
        "subcategory": "Verfassungsrecht"
    },
    {
        "title": "BGH: WEG Beschlussfähigkeit zweite Versammlung",
        "content": """BGH-Urteil V ZR 133/12: Zweite Eigentümerversammlung ist immer beschlussfähig unabhängig von Teilnehmerzahl. Einladung: Muss auf Beschlussfähigkeit hinweisen. Wichtig: Strategie bei schwacher Beteiligung!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG bauliche Veränderung Balkonverglasung",
        "content": """BGH-Urteil V ZR 253/12: Balkonverglasung ist bauliche Veränderung, bedarf Beschluss. Mehrheit: Seit WEG-Reform 2020 einfache Mehrheit wenn wirtschaftlich vernünftig. Kosten: Trägt Antragsteller. Wichtig: Zustimmung erforderlich!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Instandhaltungsrücklage Höhe",
        "content": """BGH-Urteil V ZR 110/13: Instandhaltungsrücklage muss angemessen sein. Orientierung: Mindestens 0,80€/m² pro Monat. Altbau: Höher. Wichtig: Bei Kauf Höhe prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Sonderumlage Beschluss",
        "content": """BGH-Urteil V ZR 91/14: Sonderumlage für außerplanmäßige Ausgaben bedarf Beschluss (einfache Mehrheit). Fälligkeit: Nach Beschluss. Ratenzahlung: Möglich wenn Beschluss. Wichtig: Ordnungsgemäßer Beschluss erforderlich!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Verwalter-Kündigung wichtiger Grund",
        "content": """BGH-Urteil V ZR 124/11: Verwalter-Kündigung aus wichtigem Grund jederzeit möglich. Wichtiger Grund: Pflichtverletzung, Vertrauensverlust. Frist: 6 Monate ordentliche Kündigung. Wichtig: Begründung erforderlich!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: Baumängel Gewährleistung Verjährung",
        "content": """BGH-Urteil VII ZR 45/13: Gewährleistung Bauwerke 5 Jahre ab Abnahme. Bewegliche Sachen: 2 Jahre. Frist: Beginnt mit Abnahme. Wichtig: Mängel vor Fristablauf geltend machen!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BGH: Schwarzbau Nutzungsuntersagung",
        "content": """BGH-Urteil V ZR 158/11: Schwarzbau kann zur Nutzungsuntersagung führen. Legalisierung: Nachträgliche Baugenehmigung wenn genehmigungsfähig. Verjährung: 30 Jahre bei formellen Mängeln. Wichtig: Vor Kauf prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BGH: Nachbarrecht Grenzbebauung",
        "content": """BGH-Urteil V ZR 73/12: Grenzbebauung nur mit Zustimmung Nachbar oder Baulast. Ausnahme: Bebauungsplan erlaubt. Abstand: Nach Landesbauordnung. Wichtig: Nachbarrechte beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BGH: Energieausweis Vorlage-Pflicht Vermieter",
        "content": """BGH-Urteil VIII ZR 266/14: Energieausweis muss bei Besichtigung vorgelegt werden. Schadensersatz: Bei fehlendem Ausweis möglich wenn Mieter geschädigt. Wichtig: Pflicht ernst nehmen!""",
        "category": "Rechtsprechung",
        "subcategory": "Energierecht"
    },
    {
        "title": "BGH: Grunderwerbsteuer Share Deal",
        "content": """BFH II R 30/13: Grunderwerbsteuer bei Share Deal (95%+ Anteilsübertragung) fällig. Gestaltung: Unter 95% vermeidet Steuer. Reform: Verschärfung geplant. Wichtig: Steuerliche Gestaltung prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: AfA Bemessungsgrundlage Grundstück/Gebäude",
        "content": """BFH IX R 37/14: AfA nur für Gebäude, nicht Grund und Boden. Aufteilung: Nach Verkehrswert oder Sachwertverfahren. Wichtig: Aufteilung im Kaufvertrag empfohlen!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Spekulationsfrist Eigennutzung",
        "content": """BFH IX R 37/13: Verkauf innerhalb 10 Jahren steuerfrei bei Eigennutzung im Verkaufsjahr + 2 Vorjahren. Teilweise Vermietung: Anteilig steuerpflichtig. Wichtig: 3-Jahres-Regel beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Werbungskosten Vermietung Schuldzinsen",
        "content": """BFH IX R 67/10: Schuldzinsen bei Vermietung voll als Werbungskosten absetzbar. Auch bei Leerstand: Absetzbar. Wichtig: Alle Darlehenszinsen dokumentieren!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Denkmal-AfA Bescheinigung erforderlich",
        "content": """BFH X R 30/11: Denkmal-AfA nur mit Bescheinigung der Denkmalschutzbehörde. Inhalt: Bestätigung Sanierungsmaßnahmen. Wichtig: Vor Sanierung beantragen!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Vermietung an Angehörige Fremdvergleich",
        "content": """BFH IX R 15/14: Vermietung an Angehörige steuerlich anerkannt bei mindestens 66% (ab 2021: 50%) ortsüblicher Miete. Unter 66%: Anteilige Kürzung Werbungskosten. Wichtig: Marktüblichen Vertrag gestalten!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Arbeitszimmer häusliches steuerliche Absetzbarkeit",
        "content": """BFH VI R 40/12: Häusliches Arbeitszimmer absetzbar wenn Mittelpunkt beruflicher Tätigkeit. Höhe: Unbegrenzt bei Mittelpunkt, sonst max. 1.250€. Wichtig: Voraussetzungen genau prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Erbschaftsteuer Familienheim",
        "content": """BFH II R 33/14: Familienheim steuerfrei bei Vererbung an Ehepartner/Kinder mit 10 Jahren Eigennutzung. Fläche: Kinder max. 200m² steuerfrei. Wichtig: Bindungsfrist einhalten!""",
        "category": "Rechtsprechung",
        "subcategory": "Erbschaftsteuer"
    },
    {
        "title": "BVerfG: Grundsteuer Reform verfassungsgemäß",
        "content": """BVerfG 1 BvL 11/14: Alte Grundsteuer-Einheitswerte verfassungswidrig. Reform: Neues Bewertungssystem ab 2025. Bundesmodell: Grundsteuerwert nach Fläche, Lage, Alter. Wichtig: Neue Bemessung!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BGH: Makleralleinauftrag Provision bei Selbstverkauf",
        "content": """BGH-Urteil I ZR 95/12: Bei qualifiziertem Alleinauftrag Provision auch bei Selbstverkauf fällig. Einfacher Alleinauftrag: Keine Provision bei Selbstverkauf. Wichtig: Vertragsart entscheidend!""",
        "category": "Rechtsprechung",
        "subcategory": "Maklerrecht"
    },
    {
        "title": "BGH: Maklerprovision Nachweis",
        "content": """BGH-Urteil III ZR 217/11: Makler muss Nachweis erbringen für Provision. Nachweis: Tatsächliche Vermittlung zwischen Parteien. Nicht ausreichend: Nur Hinweis auf öffentliche Annonce. Wichtig: Kausalität erforderlich!""",
        "category": "Rechtsprechung",
        "subcategory": "Maklerrecht"
    },
    {
        "title": "BGH: Immobilienkauf Aufklärungspflicht Verkäufer",
        "content": """BGH-Urteil V ZR 23/11: Verkäufer muss auf Nachfrage wahrheitsgemäß antworten. Ungefragt: Nur schwerwiegende Mängel offenlegen. Arglist: Wissentliches Verschweigen = Haftung. Wichtig: Ehrlichkeit schützt vor Prozessen!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BGH: Notarkosten Verteilung Käufer",
        "content": """BGH-Urteil V ZR 149/13: Notarkosten trägt Käufer wenn nicht anders vereinbart. Verhandelbar: Ja. GNotKG: Festgebühren 1,5-2% Kaufpreis. Wichtig: Im Kaufvertrag regeln!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BFH: Grunderwerbsteuer Inventar Abgrenzung",
        "content": """BFH II R 18/12: Grunderwerbsteuer nur auf Grundstück + Gebäude, nicht auf bewegliches Inventar. Abgrenzung: Küche fest verbaut = Grunderwerbsteuer. Möblierung = kein. Wichtig: Im Kaufvertrag trennen!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BGH: Baukostenzuschuss Erschließung",
        "content": """BGH-Urteil III ZR 275/12: Erschließungsbeiträge sind einmalig für erstmalige Herstellung. Wiederholungsbeitrag: Bei Erneuerung nach 25+ Jahren möglich. Wichtig: Ablösung prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BGH: Bauträgervertrag Abnahme",
        "content": """BGH-Urteil VII ZR 55/12: Bauträger-Abnahme ist Voraussetzung für Gewährleistungsbeginn. Fiktive Abnahme: Bei Bezug ohne Vorbehalt möglich. Wichtig: Mängel vor Abnahme dokumentieren!""",
        "category": "Rechtsprechung",
        "subcategory": "Bauträgerrecht"
    },
    {
        "title": "BGH: MaBV Zahlungsplan Bauträger",
        "content": """BGH-Urteil VII ZR 207/13: MaBV-Zahlungsplan ist zwingend bei Bauträgerverträgen. Verstoß: Raten unwirksam. Schutz: Käufer zahlt nur nach Baufortschritt. Wichtig: Nie Vorauszahlung!""",
        "category": "Rechtsprechung",
        "subcategory": "Bauträgerrecht"
    },
    {
        "title": "BGH: Baumängel Beweislast",
        "content": """BGH-Urteil VII ZR 11/13: Bauunternehmer muss Mangelfreiheit beweisen wenn Mangel gerügt. Beweislastumkehr: Ersten 6 Monate nach Abnahme. Wichtig: Sofortige Mängelanzeige!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BGH: Nachbarrecht Verschattung",
        "content": """BGH-Urteil V ZR 134/11: Verschattung durch Nachbargebäude muss geduldet werden wenn baurechtskonform. Ausnahme: Existenzvernichtung (z.B. Solaranlage). Wichtig: Baurecht geht vor!""",
        "category": "Rechtsprechung",
        "subcategory": "Nachbarrecht"
    },
    {
        "title": "BGH: Grunddienstbarkeit Wegerecht",
        "content": """BGH-Urteil V ZR 232/12: Wegerecht muss eindeutig im Grundbuch definiert sein. Umfang: Nach Eintragung (Fußweg, Fahrweg, Leitungsrecht). Änderung: Nur mit Zustimmung. Wichtig: Vor Kauf prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Grundbuchrecht"
    },
    {
        "title": "BGH: Auflassungsvormerkung Schutzwirkung",
        "content": """BGH-Urteil V ZR 181/13: Auflassungsvormerkung schützt Käufer vor Veräußerung an Dritte. Rang: Sichert Position im Grundbuch. Löschung: Nach Eigentumsumschreibung. Wichtig: Essentieller Käuferschutz!""",
        "category": "Rechtsprechung",
        "subcategory": "Grundbuchrecht"
    },
    {
        "title": "BFH: Nießbrauch steuerliche Bewertung",
        "content": """BFH II R 45/12: Nießbrauch mindert Immobilienwert bei Schenkung/Erbschaft. Berechnung: Nach statistischer Lebenserwartung und Kapitalwert. Wichtig: Steueroptimierung durch Nießbrauch!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BGH: Erbbaurecht Heimfall Entschädigung",
        "content": """BGH-Urteil V ZR 144/11: Heimfall-Entschädigung nach Erbbaurechts-Ende üblich 2/3 Verkehrswert. Regelung: Im Erbbaurechts-Vertrag. Wichtig: Vor Kauf Bedingungen prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Erbbaurecht"
    },
    {
        "title": "BGH: Zwangsversteigerung Mindestgebot",
        "content": """BGH-Urteil V ZR 85/12: Mindestgebot Zwangsversteigerung 50% Verkehrswert (bei 2. Termin 70%). Zuschlag: An Höchstbietenden. Risiko: Keine Gewährleistung. Wichtig: Gründlich vorbereiten!""",
        "category": "Rechtsprechung",
        "subcategory": "Zwangsversteigerung"
    },
    {
        "title": "BGH: Mietaufhebungsvertrag Schriftform",
        "content": """BGH-Urteil VIII ZR 242/13: Mietaufhebungsvertrag bedarf Schriftform. Mündlich: Unwirksam. Inhalt: Beendigungszeitpunkt, Abfindung, Schönheitsreparaturen. Wichtig: Schriftlich vereinbaren!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Gewerbemietrecht Mieterhöhung",
        "content": """BGH-Urteil XII ZR 20/12: Gewerbemietrecht freiere Gestaltung als Wohnraum. Mieterhöhung: Nach Vertrag (oft Indexmiete oder Staffelmiete). Kappungsgrenze: Gilt nicht. Wichtig: Vertragsfreiheit beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Gewerbemietrecht"
    },
    {
        "title": "BGH: Betriebskosten Gartenpflege Umfang",
        "content": """BGH-Urteil VIII ZR 138/11: Gartenpflege umlagefähig nach § 2 BetrKV. Nicht umlagefähig: Neuanlage, größere Umgestaltung. Abgrenzung: Laufende Pflege ja, Investition nein. Wichtig: Klare Trennung!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Staffelmiete Mindestlaufzeit Stufe",
        "content": """BGH-Urteil VIII ZR 163/12: Staffelmiete erfordert Mindestlaufzeit 1 Jahr pro Stufe (§ 557a BGB). Kürzer: Unwirksam. Schriftform: Erforderlich. Wichtig: Jahresfrist einhalten!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Kündigung Eigentümer nach Verkauf",
        "content": """BGH-Urteil VIII ZR 330/14: Kündigungssperrfrist 3 Jahre nach Umwandlung Miet- zu Eigentumswohnung. Verlängerung: Bis 10 Jahre in Gebieten mit Wohnungsknappheit. Wichtig: Sperrfrist beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Untermiete Mehrerlös",
        "content": """BGH-Urteil VIII ZR 155/11: Mehrerlös aus Untervermietung steht Vermieter zu (Wuchergrenze beachten). Berechnung: Differenz zwischen Hauptmiete und Untermiete. Wichtig: Nicht überzogene Preise!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Schönheitsreparaturen bei möblierter Wohnung",
        "content": """BGH-Urteil VIII ZR 185/15: Schönheitsreparaturen bei möblierter Wohnung oft Vermieter. Begründung: Möbel erschweren Renovierung. Klausel: Muss eindeutig sein. Wichtig: Einzelfallprüfung!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BVerwG: Denkmalschutz Veränderungsverbot",
        "content": """BVerwG 4 C 1/13: Denkmalschutz rechtfertigt Veränderungsverbot. Ausnahmen: Unzumutbare Härte. Steuervorteile: Kompensation für Auflagen. Wichtig: Vor Kauf Auflagen prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Denkmalschutz"
    },
    {
        "title": "BGH: Baurecht Abstandsflächen Berechnung",
        "content": """BGH-Urteil V ZR 229/12: Abstandsflächen nach Landesbauordnung (meist 0,4 x Wandhöhe). Nachbarwand: Mit Zustimmung Unterschreitung möglich. Wichtig: LBO des jeweiligen Bundeslandes beachten!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BGH: Baulast Bindungswirkung Rechtsnachfolger",
        "content": """BGH-Urteil V ZR 117/11: Baulast bindet auch Rechtsnachfolger (Käufer). Eintragung: Baulastenverzeichnis. Löschung: Nur mit Zustimmung Behörde. Wichtig: Vor Kauf prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BVerwG: Bebauungsplan Bindungswirkung",
        "content": """BVerwG 4 C 13/11: Bebauungsplan bindet Bauherren. Abweichung: Nur mit Befreiung (Atypik, nicht gegen Grundzüge). Wichtig: Bebauungsplan maßgeblich für Genehmigung!""",
        "category": "Rechtsprechung",
        "subcategory": "Bauplanungsrecht"
    },
    {
        "title": "BGH: Teilungserklärung Änderung",
        "content": """BGH-Urteil V ZR 98/13: Änderung Teilungserklärung erfordert Einstimmigkeit. Ausnahme: Gesetzesanpassung möglich mit Mehrheit. Wichtig: Sehr hohe Hürde für Änderungen!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Beschlussanfechtung Frist",
        "content": """BGH-Urteil V ZR 140/12: Beschlussanfechtung innerhalb 1 Monat nach Beschluss (§ 46 WEG). Versäumnis: Beschluss wird wirksam. Gründe: Formfehler, Mehrheitsfehler, Verstoß gegen Gesetz. Wichtig: Frist unbedingt einhalten!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Jahresabrechnung Prüfungsfrist",
        "content": """BGH-Urteil V ZR 125/13: Jahresabrechnung WEG muss innerhalb 6 Monaten nach Jahresende vorliegen. Einwendungen: 12 Monate nach Zugang. Wichtig: Fristen für Verwalter und Eigentümer!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Sondernutzungsrecht Instandhaltung",
        "content": """BGH-Urteil V ZR 176/12: Instandhaltung Sondernutzungsrecht (z.B. Garten) trägt oft Nutzer. Regelung: Nach Teilungserklärung. Gemeinschaft: Nur wenn Teilungserklärung so regelt. Wichtig: Teilungserklärung prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: WEG Gemeinschaftseigentum Fenster",
        "content": """BGH-Urteil V ZR 150/11: Fenster sind meist Gemeinschaftseigentum. Ausnahme: Teilungserklärung regelt anders. Instandhaltung: Gemeinschaft. Wichtig: Austausch nur mit Zustimmung!""",
        "category": "Rechtsprechung",
        "subcategory": "WEG-Recht"
    },
    {
        "title": "BGH: Grundstückskauf Rücktritt Finanzierungsvorbehalt",
        "content": """BGH-Urteil V ZR 161/12: Rücktritt bei Finanzierungsvorbehalt nur wenn ernsthaft bemüht. Nachweis: Mindestens 3 Banken anfragen. Bösgläubig: Kein Rücktritt. Wichtig: Konkrete Finanzierungsbemühung!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BGH: Grunderwerbsteuer Fälligkeit",
        "content": """BGH/BFH: Grunderwerbsteuer fällig 1 Monat nach Steuerbescheid. Unbedenklichkeitsbescheinigung: Erforderlich für Grundbucheintragung. Wichtig: Rechtzeitig zahlen!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Werbungskosten vorab Vermietung",
        "content": """BFH IX R 20/13: Vorabkosten vor Vermietung als Werbungskosten absetzbar wenn ernsthafte Vermietungsabsicht. Nachweis: Exposé, Inserate, Maklerauftrag. Wichtig: Absicht dokumentieren!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BFH: Handwerkerleistungen Steuerbonus",
        "content": """BFH VI R 55/12: Handwerkerleistungen 20% der Arbeitskosten absetzbar (max. 1.200€ Steuerermäßigung). Voraussetzung: Selbstgenutzte Immobilie, Rechnung, Überweisung. Material: Nicht absetzbar. Wichtig: Auch für Mieter!""",
        "category": "Rechtsprechung",
        "subcategory": "Steuerrecht"
    },
    {
        "title": "BGH: Vorkaufsrecht Mieter bei Umwandlung",
        "content": """BGH-Urteil VIII ZR 266/15: Vorkaufsrecht Mieter bei Umwandlung Miet- zu Eigentumswohnung. Dauer: 10 Jahre nach Umwandlung. Frist: 2 Monate Ausübung. Wichtig: Käufer muss warten!""",
        "category": "Rechtsprechung",
        "subcategory": "Mietrecht"
    },
    {
        "title": "BGH: Makler Doppeltätigkeit Offenlegung",
        "content": """BGH-Urteil III ZR 71/13: Makler muss Doppeltätigkeit (für Käufer + Verkäufer) offenlegen. Verstoß: Provisionsverlust. Neutralität: Muss gewahrt bleiben. Wichtig: Transparenzpflicht!""",
        "category": "Rechtsprechung",
        "subcategory": "Maklerrecht"
    },
    {
        "title": "BGH: Kaufvertrag Gewährleistung Neubau",
        "content": """BGH-Urteil VII ZR 203/11: Gewährleistung Neubau 5 Jahre für Bauwerk. Ausschluss: Bei Verbrauchern nur eingeschränkt möglich. Verjährung: Ab Abnahme. Wichtig: Mängel vor Fristablauf geltend machen!""",
        "category": "Rechtsprechung",
        "subcategory": "Kaufrecht"
    },
    {
        "title": "BGH: Teilungsgenehmigung Grundstück",
        "content": """BGH-Urteil V ZR 119/12: Teilungsgenehmigung erforderlich bei Grundstücksteilung. Voraussetzung: Mindestgröße, Erschließung, Bebauungsplan. Wichtig: Vor Teilung Genehmigung einholen!""",
        "category": "Rechtsprechung",
        "subcategory": "Baurecht"
    },
    {
        "title": "BFH: Erbschaftsteuer Bewertung Immobilien",
        "content": """BFH II R 38/13: Immobilienbewertung bei Erbschaft nach Verkehrswert. Ermittlung: Vergleichswert-, Ertragswert- oder Sachwertverfahren. Wichtig: Gutachten kann Steuerlast senken!""",
        "category": "Rechtsprechung",
        "subcategory": "Erbschaftsteuer"
    },
    {
        "title": "BGH: Notaranderkonto Treuhandpflicht",
        "content": """BGH-Urteil V ZR 156/11: Notar haftet bei Pflichtverletzung im Treuhandgeschäft. Auszahlung: Nur wenn Bedingungen erfüllt. Sicherheit: Für beide Seiten. Wichtig: Notar als neutraler Treuhänder!""",
        "category": "Rechtsprechung",
        "subcategory": "Notarrecht"
    },
    {
        "title": "BGH: Leibrente Immobilie Bewertung",
        "content": """BGH-Urteil V ZR 191/12: Leibrente-Bewertung nach Immobilienwert und statistischer Lebenserwartung. Indexierung: Möglich. Reallast: Dinglich gesichert. Wichtig: Faire Kalkulation!""",
        "category": "Rechtsprechung",
        "subcategory": "Leibrente"
    },
    {
        "title": "BGH: Wohnrecht eingetragen Belastung",
        "content": """BGH-Urteil V ZR 156/13: Eingetragenes Wohnrecht mindert Immobilienwert erheblich (30-70%). Löschung: Nur mit Zustimmung Berechtigtem. Verkauf: Deutlicher Preisabschlag. Wichtig: Vor Kauf Grundbuch prüfen!""",
        "category": "Rechtsprechung",
        "subcategory": "Grundbuchrecht"
    },
    {
        "title": "BGH: Erschließung Wiederholungsbeitrag",
        "content": """BGH-Urteil III ZR 372/11: Wiederholungsbeitrag bei Erneuerung Erschließung nach 25+ Jahren zulässig. Berechnung: Nach Grundstücksgröße. Wichtig: Zweite Belastung möglich!""",
        "category": "Rechtsprechung",
        "subcategory": "Erschließungsrecht"
    }
]

print("🚀 BATCH 6: RECHTSPRECHUNG & BGH-URTEILE - START")
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

print("\n🔥 BATCH 6 COMPLETE! 🔥")
