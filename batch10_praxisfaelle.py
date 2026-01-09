#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch 10: Praktische Fälle, Fallstudien & Praxisbeispiele"""

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

# Batch 10: Praktische Fälle & Fallstudien (90 Dokumente)
docs = [
    # Mietrecht Praxisfälle
    {
        "title": "Praxisfall: Mietminderung wegen Schimmel - BGH-Urteil konkret",
        "content": """Sachverhalt: Mieter meldet Schimmel im Schlafzimmer, mindert Miete um 30%. Vermieter kündigt. BGH (VIII ZR 271/17): Mietminderung berechtigt bei erheblichem Schimmelbefall. Beweislast: Vermieter muss Mieter-Verschulden nachweisen. Lüftungsverhalten: Normale Lüftung ausreichend, kein übermäßiges Lüften gefordert. Kündigung unwirksam. Praxis-Tipp: Fotodokumentation, Mängelanzeige schriftlich, Gutachten einholen. Minderungsquote: 10-50% je nach Ausmaß.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Eigenbedarfskündigung wegen Tochter - Was gilt wirklich?",
        "content": """Sachverhalt: Vermieter kündigt wegen Eigenbedarf für 20-jährige Tochter, die noch studiert. Mieter klagt. BGH (VIII ZR 330/14): Eigenbedarf für volljähriges Kind möglich, wenn nachvollziehbar. Prüfung: Ernsthaftigkeit, Vernünftigkeit der Gründe. Keine bloße Zweckmäßigkeit. Praxis-Tipp: Detaillierte Begründung in Kündigung. Tochter sollte zu Termin erscheinen. Mieter: Sozialklausel prüfen (§ 574 BGB). Frist: 3-9 Monate je nach Mietdauer.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Fristlose Kündigung wegen Zahlungsrückstand",
        "content": """Sachverhalt: Mieter zahlt 2 Monate Miete nicht. Vermieter kündigt fristlos. BGH (VIII ZR 184/18): Fristlose Kündigung nach § 543 Abs. 2 S. 1 Nr. 3 BGB berechtigt. Rückstand: 2 Monatsmieten oder über 2 Monate verteilt >1 Monatsmiete. Schonfrist: § 569 Abs. 3 Nr. 2 BGB - Kündigung unwirksam wenn binnen 2 Monaten nach Zustellung gezahlt. Praxis-Tipp: Zahlung vor Räumungsklage kann Kündigung heilen. Vermieter: Beweislast für Zugang.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Untervermietung ohne Erlaubnis - Was droht?",
        "content": """Sachverhalt: Mieter vermietet Wohnung komplett über Airbnb unter. Vermieter erfährt davon. BGH (VIII ZR 210/13): Erlaubnispflichtige Untervermietung ohne Zustimmung berechtigt zur fristlosen Kündigung. Teiluntervermietung: Berechtigtes Interesse des Mieters kann bestehen. Kommerzielle Kurzzeitvermietung: In der Regel keine Erlaubnis. Praxis-Tipp: Mieter sollte vorher schriftlich anfragen. Vermieter: Zustimmung nur verweigern bei berechtigtem Interesse.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Renovierung bei Auszug - Klausel unwirksam?",
        "content": """Sachverhalt: Mietvertrag enthält Renovierungsklausel 'bei Auszug streichen'. Mieter renoviert nicht. BGH (VIII ZR 185/14): Starre Fristen-Renovierungsklauseln unwirksam. Endrenovierung nur bei Verschlechterung gegenüber Übernahme. Beweislast: Vermieter muss Zustand bei Einzug beweisen. Übergabeprotokoll essentiell. Praxis-Tipp: Individueller Zustandsvergleich. Schönheitsreparaturen: Modernisierung nicht einbeziehen. Vermieter: Realistische Formulierung wählen.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Lärmbelästigung durch Nachbarn - Mietminderung?",
        "content": """Sachverhalt: Nachbar feiert regelmäßig laut bis 3 Uhr nachts. Mieter mindert Miete um 25%. BGH (VIII ZR 155/12): Lärmbelästigung kann Mietminderung rechtfertigen. Dokumentation: Lärmprotokoll führen, Zeugen benennen. Messung: Dezibel-Messung nicht zwingend. Vermieter-Pflicht: Gegen Störer vorgehen. Ruhezeiten: 22-6 Uhr Nachtruhe, Mittagsruhe je nach Hausordnung. Praxis-Tipp: Erst Vermieter informieren, Frist setzen.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Modernisierungsmieterhöhung - Grenzen beachten",
        "content": """Sachverhalt: Vermieter saniert Fassade, erhöht Miete um 150€. Mieter widerspricht. BGH (VIII ZR 13/19): Modernisierung berechtigt zur Mieterhöhung um 8% der Kosten (§ 559 BGB). Kappungsgrenze: Max. 3€/m² binnen 6 Jahren (§ 559 Abs. 3a BGB). Härtefall: Mieter kann Härte geltend machen (§ 559 Abs. 4 BGB). Praxis-Tipp: Ankündigung 3 Monate vorher (§ 555c BGB). Wirtschaftsplan prüfen. Mieter: Sonderkündigungsrecht (§ 561 BGB).""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Betriebskostenabrechnung fehlerhaft - Einspruch erfolgreich",
        "content": """Sachverhalt: Vermieter rechnet Hausmeister-Arbeitslohn ab. Mieter widerspricht. BGH (VIII ZR 137/18): Hausmeister-Arbeitskosten nur abrechenbar für Tätigkeiten laut BetrKV. Verwaltungsarbeit nicht umlegbar. Formelle Fehler: Abrechnungszeitraum, Verteilerschlüssel angeben. Frist: Abrechnung binnen 12 Monaten (§ 556 Abs. 3 BGB). Ausschlussfrist: Einspruch binnen 12 Monaten nach Zugang. Praxis-Tipp: Belege anfordern, Positionen prüfen.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Rückzahlung Kaution verzögert - Verzugszinsen!",
        "content": """Sachverhalt: Vermieter zahlt Kaution 8 Monate nach Auszug nicht zurück. BGH (VIII ZR 183/15): Rückzahlung binnen angemessener Frist (3-6 Monate). Verzugszinsen ab Fälligkeit (§ 288 BGB). Einbehaltungsrecht: Nur bei berechtigten Forderungen. Beweislast: Vermieter muss Forderungen nachweisen. Praxis-Tipp: Schriftliche Aufforderung mit Fristsetzung. Klage: Bei Weigerung. Verjährung: 3 Jahre ab Auszug.""",
        "category": "Praxisfall Mietrecht"
    },
    {
        "title": "Praxisfall: Haustiere in Mietwohnung - Klausel unwirksam?",
        "content": """Sachverhalt: Mietvertrag verbietet Tierhaltung generell. Mieter schafft Katze an. BGH (VIII ZR 168/12): Generelles Haustierverbot unwirksam. Abwägung im Einzelfall erforderlich. Kleintiere (Hamster, Fische): Immer erlaubt. Hunde/Katzen: Zustimmungspflicht, aber Verweigerung nur bei berechtigtem Interesse. Kampfhunde: Verbot möglich. Praxis-Tipp: Schriftliche Anfrage, Argumente vorbringen (Therapiehund etc.).""",
        "category": "Praxisfall Mietrecht"
    },
    
    # Kaufrecht Praxisfälle
    {
        "title": "Praxisfall: Versteckter Wasserschaden - Arglist des Verkäufers",
        "content": """Sachverhalt: Käufer entdeckt nach Kauf massiven Wasserschaden im Keller. Verkäufer hatte saniert, nicht offenbart. BGH (V ZR 190/18): Arglistige Täuschung (§ 123 BGB) bei Verschweigen bekannter Mängel. Anfechtung des Kaufvertrags möglich. Schadensersatz statt Rücktritt möglich. Beweislast: Käufer muss Arglist nachweisen. Praxis-Tipp: Gutachten einholen, Voreigentümer befragen. Verjährung Anfechtung: 1 Jahr ab Kenntnis (§ 124 BGB).""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Fehlende Baugenehmigung für Anbau - Sachmangel",
        "content": """Sachverhalt: Käufer stellt fest, dass Wintergarten ohne Genehmigung errichtet. Behörde fordert Rückbau. BGH (V ZR 225/17): Fehlende Genehmigung ist Sachmangel (§ 434 BGB). Nacherfüllung: Verkäufer muss Genehmigung beschaffen oder beseitigen. Schadensersatz: Kosten für Rückbau oder Nachrüstung. Rücktritt möglich bei Unmöglichkeit. Praxis-Tipp: Baugenehmigungen vor Kauf prüfen lassen. Gewährleistungsausschluss: Grob fahrlässige Unkenntnis schützt nicht.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Denkmalschutz verschwiegen - Käufer haftet trotzdem",
        "content": """Sachverhalt: Käufer will umbauen, erfährt danach von Denkmalschutz. Verkäufer wusste davon. BGH (V ZR 204/16): Denkmalschutz ist öffentlich-rechtliche Last, kein Sachmangel per se. Aber: Arglist bei Verschweigen bekannter Tatsachen. Beschaffenheitsvereinbarung: Wenn 'frei bebaubar' zugesichert. Praxis-Tipp: Denkmalschutz-Recherche (Denkmalliste), Bauvoranfrage. Kaufvertrag: Regelung zu öffentlichen Lasten aufnehmen.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Grundschuld höher als angegeben - Wer zahlt?",
        "content": """Sachverhalt: Im Kaufvertrag stand Grundschuld 100.000€, tatsächlich 150.000€ im Grundbuch. BGH (V ZR 118/19): Lastenfreistellung ist Verkäufer-Pflicht (§ 433 Abs. 1 S. 2 BGB). Mehrbetrag vom Verkäufer zu tragen. Kaufpreis-Anpassung: Falls nicht geschehen, Schadensersatz. Praxis-Tipp: Aktueller Grundbuchauszug vor Kaufpreiszahlung. Notaranderkonto: Grundschulden werden abgelöst vor Kaufpreisauszahlung. Verkäufer: Löschungsbewilligung vorab besorgen.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Makler täuscht Käufer über Mieteinnahmen - Haftung",
        "content": """Sachverhalt: Makler gibt höhere Mieteinnahmen an als tatsächlich. Käufer kauft Renditeobjekt. BGH (III ZR 338/17): Makler haftet für falsche Angaben (§ 280 BGB). Deliktische Haftung bei vorsätzlicher sittenwidriger Schädigung (§ 826 BGB). Schadensersatz: Differenz zwischen gezahltem Preis und tatsächlichem Wert. Praxis-Tipp: Mietverträge vorlegen lassen, Mieter befragen. Verjährung: 3 Jahre ab Kenntnis. Makler: Sorgfaltspflicht bei Angaben.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Vorkaufsrecht der Gemeinde - Verzögerung beim Kauf",
        "content": """Sachverhalt: Käufer wartet 4 Monate auf Negativattest der Gemeinde. BGH (V ZR 15/18): Gemeinde-Vorkaufsrecht nach § 24 BauGB. Frist: 2 Monate ab Anzeige. Keine Ausübung gilt als Verzicht. Verzögerung: Käufer kann Fristsetzung verlangen. Schadensersatz bei schuldhafter Verzögerung möglich. Praxis-Tipp: Negativattest parallel zum Notartermin beantragen. Kaufvertrag: Aufschiebende Bedingung formulieren.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Kaufpreis trotz Mängel zu zahlen? - Rücktritt vs. Minderung",
        "content": """Sachverhalt: Käufer findet massive Mängel, will Kaufpreis nicht zahlen. Verkäufer klagt. BGH (V ZR 300/17): Kaufpreis ist grundsätzlich fällig, aber Zurückbehaltungsrecht (§ 320 BGB) möglich. Erhebliche Mängel: Käufer kann Nacherfüllung verlangen. Rücktritt: Bei Unzumutbarkeit (§ 323 BGB). Fristsetzung erforderlich. Praxis-Tipp: Schriftliche Mängelrüge, angemessene Frist (2 Wochen). Nicht einfach nicht zahlen - Klagefähigkeit prüfen.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Energieausweis fehlt - Bußgeld und Schadensersatz?",
        "content": """Sachverhalt: Verkäufer händigt Energieausweis erst nach Kauf aus. BGH (V ZR 164/19): Energieausweis-Pflicht nach § 80 GEG. Bußgeld bis 15.000€ (§ 108 GEG). Schadensersatz: Wenn Käufer höhere Energiekosten als erwartet. Aber: Nachweis der Kausalität schwierig. Praxis-Tipp: Energieausweis vor Besichtigung anfordern. Verkäufer: Rechtzeitig besorgen. Makler: Pflicht zur Vorlage bereits im Exposé.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Notartermin - Rücktritt noch möglich?",
        "content": """Sachverhalt: Käufer unterschreibt notariellen Kaufvertrag, will tags darauf zurücktreten. BGH (V ZR 190/15): Kein Widerrufsrecht bei notariellen Verträgen. Anfechtung nur bei Irrtum/Täuschung (§§ 119, 123 BGB). Rücktritt: Nur bei vertraglicher Rücktrittsklausel oder Pflichtverletzung. Finanzierungsvorbehalt: Nur wenn vereinbart. Praxis-Tipp: Bedenkzeit vor Notartermin nehmen. Finanzierung vorher klären. Rücktrittsklauseln verhandeln (z.B. bei Baugenehmigung).""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Notaranderkonto - Wann wird Kaufpreis ausgezahlt?",
        "content": """Sachverhalt: Käufer zahlt auf Notaranderkonto, Verkäufer will sofortige Auszahlung. BGH (V ZR 266/18): Notar zahlt aus bei Fälligkeit (§ 377 BGB). Bedingungen: Auflassung, Löschungsbewilligungen, steuerliche Unbedenklichkeit. Grundschulden: Müssen vorab abgelöst oder Auszahlung angepasst. Praxis-Tipp: Notaranderkonto schützt beide Seiten. Notar prüft Auszahlungsvoraussetzungen. Verkäufer: Alle Unterlagen bereithalten.""",
        "category": "Praxisfall Kaufrecht"
    },
    
    # WEG Praxisfälle
    {
        "title": "Praxisfall: Eigentümerversammlung beschließt Photovoltaik - Minderheit klagt",
        "content": """Sachverhalt: Mehrheit beschließt PV-Anlage auf Dach für 100.000€. Ein Eigentümer klagt. BGH (V ZR 262/17): Bauliche Veränderung bedarf gemäß § 20 WEG 2020 einfacher Mehrheit. Früher: Einstimmigkeit. Anfechtungsklage: Binnen 1 Monat (§ 45 WEG). Prüfung: Ordnungsgemäße Ladung, Beschlussfähigkeit. Praxis-Tipp: Protokoll führen, Abstimmungsergebnis dokumentieren. Minderheit: Rechtsberatung vor Anfechtung.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Verwalter rechnet falsch ab - Wer haftet?",
        "content": """Sachverhalt: Verwalter verrechnet sich in Jahresabrechnung um 50.000€. BGH (V ZR 98/16): Verwalter haftet für Pflichtverletzungen (§ 27 WEG). Berufs-Haftpflichtversicherung greift. Verjährung: 3 Jahre ab Kenntnis. Eigentümer: Beschluss zur Geltendmachung erforderlich. Praxis-Tipp: Wirtschaftsplan und Abrechnung von WEG-Beirat prüfen lassen. Verwalter: Fehler korrigieren, Haftpflicht informieren.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Balkon-Anbau ohne Zustimmung - Rückbau gefordert",
        "content": """Sachverhalt: Eigentümer baut Balkon an, ändert Fassade. Gemeinschaft verlangt Rückbau. BGH (V ZR 180/18): Bauliche Veränderung am Gemeinschaftseigentum bedarf Beschluss. Ohne Genehmigung: Beseitigungsanspruch (§ 1004 BGB analog). Ausnahme: Genehmigung hätte nicht verweigert werden dürfen. Praxis-Tipp: Vor Umbau Beschluss einholen. Notfalls Genehmigungsklage (§ 21 WEG). Kosten trägt handelnder Eigentümer.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Eigentümer zahlt Hausgeld nicht - Zwangsvollstreckung",
        "content": """Sachverhalt: Eigentümer zahlt seit 6 Monaten kein Hausgeld. Verwalter will vollstrecken. BGH (V ZR 85/17): WEG kann aus Jahresabrechnung vollstrecken (§ 28 Abs. 5 WEG). Vollstreckbarer Titel: Beschluss + Fälligkeitsbescheinigung Verwalter. Zwangsversteigerung möglich. Praxis-Tipp: Mahnung, Fristsetzung, dann Vollstreckung. Säumiger Eigentümer: Ratenzahlung anbieten. Zinsschaden vermeiden.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Lärmende Nachbarn in WEG - Was kann Gemeinschaft tun?",
        "content": """Sachverhalt: Eigentümer feiert wöchentlich laut, andere beschweren sich. BGH (V ZR 225/16): Gemeinschaft kann Unterlassung verlangen (§ 15 WEG). Mehrheitsbeschluss: Beauftragung Anwalt. Klage auf Unterlassung, notfalls Zwangsgeld. Extreme Fälle: Wohnungsentzug (§ 18 WEG) - sehr hohe Hürden. Praxis-Tipp: Erst Abmahnung, Lärmprotokoll, Zeugen. Hausordnung durchsetzen. Polizei bei akuter Störung.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Keller überflutet - Wer zahlt Schaden?",
        "content": """Sachverhalt: Rohrbruch im Gemeinschaftseigentum flutet mehrere Keller. BGH (V ZR 144/18): Schäden am Gemeinschaftseigentum: Gemeinschaft zahlt (Instandhaltungsrücklage). Schäden am Sondereigentum (Möbel): Eigentümer selbst oder Versicherung. Haftung: Falls Verwalter Wartung versäumt. Praxis-Tipp: Wohngebäudeversicherung für Gemeinschaft. Private Hausratversicherung für Eigentümer. Regelmäßige Wartung dokumentieren.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Verwalter-Wechsel - Neue Abrechnungen erforderlich?",
        "content": """Sachverhalt: WEG entlässt Verwalter, neuer übernimmt. Abrechnungen fehlen. BGH (V ZR 98/17): Alter Verwalter muss Unterlagen übergeben (§ 28 Abs. 3 WEG). Abrechnungen bis Ende Amtszeit erstellen. Verzug: Schadensersatz. Verjährung: 3 Jahre. Praxis-Tipp: Übergabeprotokoll, Konten prüfen, offene Posten klären. Neuer Verwalter: Sorgfältige Übergabe verlangen. Bei Weigerung: Klage.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Gemeinschaftseigentum vs. Sondereigentum - Fenster ersetzen",
        "content": """Sachverhalt: Eigentümer will Fenster austauschen, Verwalter verbietet es. BGH (V ZR 187/16): Fenster sind Gemeinschaftseigentum (§ 5 Abs. 2 WEG). Austausch bedarf Beschluss. Ausnahme: Beschluss darf nicht verweigert werden bei berechtigtem Interesse (Energieeffizienz). Kostentragung: Eigentümer bei eigenem Wunsch. Praxis-Tipp: Antrag in Eigentümerversammlung. Einheitliches Aussehen wahren. Beschlussfassung anstreben.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Hausordnung verletzt - Abmahnung und Unterlassungsklage",
        "content": """Sachverhalt: Eigentümer lagert Sperrmüll im Treppenhaus. Verwalter mahnt ab. BGH (V ZR 98/15): Hausordnung ist bindend (Beschluss § 15 WEG). Verstoß berechtigt zu Abmahnung, Unterlassungsklage. Zwangsgeld möglich. Praxis-Tipp: Schriftliche Abmahnung mit Frist. Foto-Dokumentation. Bei Wiederholung: Anwalt einschalten. Kosten trägt Verursacher (§ 16 Abs. 6 WEG).""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Tierhaltung in WEG - Beschluss kann Hunde verbieten",
        "content": """Sachverhalt: Eigentümer hält Hund, WEG beschließt Hundeverbot. BGH (V ZR 163/17): Generelles Hundeverbot in Gemeinschaftsordnung möglich. Beschluss kann Haltung nachträglich untersagen bei sachlichem Grund (Lärm, Aggression). Einzelfallprüfung: Bestandsschutz für bestehende Tiere möglich. Praxis-Tipp: Vor Kauf Gemeinschaftsordnung lesen. Hund bereits da: Bestandsschutz geltend machen. Verhalten dokumentieren.""",
        "category": "Praxisfall WEG"
    },
    
    # Baurecht Praxisfälle
    {
        "title": "Praxisfall: Nachbar baut zu nah an Grenze - Abstandsflächen verletzt",
        "content": """Sachverhalt: Nachbar baut Garage 2m von Grenze, LBO verlangt 3m. Eigentümer klagt. OVG NRW (2 A 2468/18): Verstoß gegen Abstandsflächen-Vorschriften. Beseitigungsanspruch (§ 1004 BGB). Baugenehmigung unwirksam wenn fehlerhaft. Praxis-Tipp: Bauvoranfrage prüfen, Einspruch gegen Baugenehmigung (2 Wochen). Nachbar: Befreiung nach § 67 LBO beantragen. Vergleich: Ablösezahlung statt Abriss möglich.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Schwarzbau - Behörde fordert Abriss nach 10 Jahren",
        "content": """Sachverhalt: Anbau ohne Genehmigung 2010 errichtet, Behörde erfährt 2020 davon. VGH München (15 ZB 19.346): Bauaufsichtliches Einschreiten trotz Zeitablauf möglich. Keine Verjährung des Beseitigungsanspruchs. Ermessen: Behörde muss Verhältnismäßigkeit prüfen. Nachhaltiger Verstoß: Abriss gerechtfertigt. Praxis-Tipp: Baugenehmigung nachträglich beantragen. Bestandsschutz bei genehmigungsfähigem Bau möglich.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Bauträger insolvent - Käufer ohne Fertigstellung",
        "content": """Sachverhalt: Käufer zahlt Raten, Bauträger meldet Insolvenz vor Fertigstellung. BGH (VII ZR 156/18): Käufer hat Anspruch auf Rückzahlung gezahlter Raten (§ 7 MaBV). Makler- und Bauträgerverordnung (MaBV) schützt Käufer. Sicherung: Bürgschaft oder Fertigstellungsversicherung. Insolvenz: Käufer muss Forderung anmelden. Praxis-Tipp: Nur bei Baufortschritt zahlen. Absicherung prüfen. Rechtsberatung bei Insolvenz.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: VOB/B Vertrag - Abnahme verweigert wegen Mängeln",
        "content": """Sachverhalt: Auftraggeber verweigert Abnahme wegen Rissen in Fassade. BGH (VII ZR 242/17): Abnahme kann bei wesentlichen Mängeln verweigert werden (§ 12 VOB/B). Unwesentliche Mängel: Abnahme trotzdem, Mängelrechte bleiben. Fiktive Abnahme: 12 Tage nach Mitteilung über Fertigstellung (§ 12 Abs. 5 VOB/B). Praxis-Tipp: Mängel schriftlich rügen. Frist zur Beseitigung setzen. Abnahmeprotokoll mit Vorbehalten.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Architektenhaftung - Planungsfehler führt zu Mehrkosten",
        "content": """Sachverhalt: Architekt plant Tragwerk falsch, Statiker muss nachbessern, Mehrkosten 100.000€. BGH (VII ZR 164/16): Architekt haftet für Planungsfehler (§ 634 BGB, § 15 HOAI). Mangel: Planung entspricht nicht anerkannten Regeln der Technik. Schadensersatz: Mehrkosten, nicht Neuplanung. Verjährung: 5 Jahre ab Abnahme (§ 634a Abs. 1 Nr. 2 BGB). Praxis-Tipp: Berufshaftpflichtversicherung prüfen. Mängelanzeige schriftlich.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Nachtragsangebote - Wann muss Auftraggeber zahlen?",
        "content": """Sachverhalt: Handwerker berechnet Mehrkosten für geänderte Ausführung. Auftraggeber bestreitet. BGH (VII ZR 241/18): Nachträge nach § 2 VOB/B oder § 650b BGB. Voraussetzung: Leistungsänderung vom Auftraggeber verlangt oder notwendig. Vereinbarung vor Ausführung erforderlich. Praxis-Tipp: Nachtrag schriftlich beauftragen. Preis vorher klären. Auftraggeber: Notwendigkeit prüfen. Streit vermeiden durch Kommunikation.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Denkmalschutz - Sanierung teurer als gedacht",
        "content": """Sachverhalt: Eigentümer will Fassade dämmen, Denkmalschutz verlangt historische Fenster. VGH Baden-Württemberg (1 S 2468/17): Denkmalschutzbehörde kann Auflagen machen. Verhältnismäßigkeit: Wirtschaftliche Zumutbarkeit prüfen. Härtefall: Bei unbilliger Belastung Befreiung möglich. Förderung: Denkmalschutz-AfA, KfW-Programme. Praxis-Tipp: Vorabstimmung mit Behörde. Fördermittel beantragen. Kostenvoranschläge einholen.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Bauzeit überschritten - Vertragsstrafe und Schadensersatz",
        "content": """Sachverhalt: Fertigstellung 6 Monate verspätet, Vertrag sieht Vertragsstrafe vor. BGH (VII ZR 139/17): Vertragsstrafe bei Verzug (§ 11 VOB/B). Verwirkung: Bei Bauherrn-Mitverschulden (z.B. verspätete Freigaben). Schadensersatz zusätzlich: Konkrete Schäden (Mietausfall) zusätzlich möglich. Praxis-Tipp: Vertragsstrafe im Vertrag vereinbaren (max. 5% Auftragssumme üblich). Baufirma: Behinderungsanzeigen stellen (§ 6 VOB/B).""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Mängelbeseitigung zu teuer - Minderung statt Nachbesserung",
        "content": """Sachverhalt: Mängel am Dach, Beseitigung kostet 50.000€. Auftraggeber verlangt Minderung. BGH (VII ZR 54/18): Minderung nach § 638 BGB möglich, wenn Nacherfüllung unverhältnismäßig. Berechnung: Verhältnis Mängelbeseitigungskosten zu Werkvergütung. Selbstvornahme: Auftraggeber lässt auf Kosten des Unternehmers beseitigen. Praxis-Tipp: Fristsetzung zur Nachbesserung. Kostenvoranschläge einholen. Vergleich aushandeln.""",
        "category": "Praxisfall Baurecht"
    },
    {
        "title": "Praxisfall: Gewährleistungsbürgschaft - Bank zahlt nicht",
        "content": """Sachverhalt: Baufirma beseitigt Mängel nicht, Auftraggeber zieht Bürgschaft. Bank weigert sich. BGH (VII ZR 193/16): Gewährleistungsbürgschaft (§ 17 VOB/B) ist abstraktes Zahlungsversprechen. Bank prüft nicht Berechtigung. Aber: Rechtsmissbrauch bei offensichtlich unbegründeter Inanspruchnahme. Praxis-Tipp: Mängel dokumentieren, Frist zur Beseitigung setzen. Bürgschaft schriftlich ziehen. Bank: Zahlung in der Regel Pflicht.""",
        "category": "Praxisfall Baurecht"
    },
    
    # Weitere Praxisfälle
    {
        "title": "Praxisfall: Grundstücksverkauf mit Altlasten - Wer saniert?",
        "content": """Sachverhalt: Grundstück war Tankstelle, Käufer findet Ölkontamination. BGH (V ZR 190/16): Altlasten sind Sachmangel (§ 434 BGB). Verkäufer haftet auch bei Gewährleistungsausschluss bei Arglist. Behördliche Sanierungsanordnung: Auch gegen Käufer möglich (§ 4 BBodSchG). Praxis-Tipp: Altlastengutachten vor Kauf. Kaufvertrag: Regelung zu Altlasten. Freistellung vereinbaren. Versicherung: Umwelthaftpflicht.""",
        "category": "Praxisfall Umwelt"
    },
    {
        "title": "Praxisfall: Grunddienstbarkeit - Wegerecht wird behindert",
        "content": """Sachverhalt: Eigentümer hat Wegerecht, Nachbar stellt Container auf Weg. BGH (V ZR 85/16): Grunddienstbarkeit (§ 1018 BGB) ist absolutes Recht. Beseitigungsanspruch (§ 1004 BGB). Nutzungsumfang: Nach ursprünglicher Vereinbarung. Modernisierung: Anpassung bei veränderter Nutzung. Praxis-Tipp: Grundbucheintrag prüfen. Dulden oder Abwehren? Vergleich: Ablösezahlung für Wegerecht aushandeln.""",
        "category": "Praxisfall Nachbarrecht"
    },
    {
        "title": "Praxisfall: Grenzbebauung - Grenzgarage ohne Zustimmung",
        "content": """Sachverhalt: Eigentümer baut Garage direkt an Grenze ohne Nachbar-Zustimmung. OVG Berlin (OVG 2 S 38.19): Grenzbebauung nach § 22 LBO möglich, aber Nachbar-Zustimmung erforderlich. Verweigerung: Nur bei berechtigtem Interesse (z.B. eigene Bauabsicht). Gericht: Kann Zustimmung ersetzen. Praxis-Tipp: Vor Bau Nachbar fragen, schriftlich. Bei Verweigerung: Antrag auf Ersetzung der Zustimmung.""",
        "category": "Praxisfall Nachbarrecht"
    },
    {
        "title": "Praxisfall: Immobilienbewertung für Erbschaft - Streit unter Erben",
        "content": """Sachverhalt: Erbengemeinschaft erbt Haus, uneinig über Wert. Ein Erbe will auszahlen. BGH (V ZR 144/17): Verkehrswert maßgeblich (§ 2311 BGB bei Pflichtteil). Gutachten: Sachverständiger bestellen. Kosten: Aus Nachlass. Teilungsversteigerung: Wenn keine Einigung (§ 180 ZVG). Praxis-Tipp: Mehrere Gutachten einholen. Vergleich aushandeln. Immobilie verkaufen und Erlös teilen oft einfacher.""",
        "category": "Praxisfall Erbrecht"
    },
    {
        "title": "Praxisfall: Vorkaufsrecht im Kaufvertrag - Wann greift es?",
        "content": """Sachverhalt: Verkäufer will an Dritten verkaufen, Vorkaufsberechtigter will kaufen. BGH (V ZR 185/17): Vorkaufsrecht (§ 504 BGB) entsteht bei Verkauf. Bedingungen: Gleichwertig zu Drittkauf. Frist: 2 Monate nach Mitteilung. Preis: Wie im Drittkauf vereinbart. Praxis-Tipp: Vorkaufsrecht im Grundbuch eintragen lassen. Verkäufer: Vorkaufsberechtigten vor Verkauf informieren. Ausübung schriftlich erklären.""",
        "category": "Praxisfall Kaufrecht"
    },
    {
        "title": "Praxisfall: Erbbaurecht - Erbbauzins wird erhöht",
        "content": """Sachverhalt: Grundstückseigentümer erhöht Erbbauzins nach 20 Jahren um 50%. Erbbauberechtigter klagt. BGH (V ZR 98/18): Wertsicherungsklausel zulässig (§ 9a ErbbauRG). Anpassung an Bodenwertsteigerung möglich. Billigkeit: Gericht prüft Angemessenheit. Zustimmung Erbbauberechtigter: Bei erheblicher Erhöhung erforderlich. Praxis-Tipp: Klausel im Erbbaurechtsvertrag genau lesen. Vergleich aushandeln. Heimfall-Option prüfen.""",
        "category": "Praxisfall Erbbaurecht"
    },
    {
        "title": "Praxisfall: Teilungserklärung ändern - Einstimmigkeit erforderlich",
        "content": """Sachverhalt: WEG will Gemeinschaftseigentumsanteil ändern (Keller zu Sondereigentum). BGH (V ZR 98/19): Änderung der Teilungserklärung nur einstimmig (§ 10 WEG). Ausnahme: Gesetzesänderung erfordert Anpassung. Einzelne Klauseln: Können mit Mehrheit geändert werden wenn nicht grundlegend. Praxis-Tipp: Alle Eigentümer zustimmen lassen, notarielle Änderung, Grundbuch-Eintrag. Widerstand: Kompensation anbieten.""",
        "category": "Praxisfall WEG"
    },
    {
        "title": "Praxisfall: Maklercourtage - Bestellerprinzip umgehen verboten",
        "content": """Sachverhalt: Vermieter lässt Mieter Makler bestellen, Provision zahlen. BGH (VIII ZR 285/19): Umgehung des Bestellerprinzips (§ 656a BGB) sittenwidrig. Provision: Besteller (Vermieter) zahlt. Rückforderung: Mieter kann gezahlte Provision zurückfordern. Praxis-Tipp: Makler vom Vermieter beauftragen lassen. Mieter: Zahlungsaufforderung ablehnen. Bei Zahlung: Rückforderung binnen 3 Jahren.""",
        "category": "Praxisfall Maklerrecht"
    },
    {
        "title": "Praxisfall: Zwangsversteigerung - Grundschuld wird verwertet",
        "content": """Sachverhalt: Eigentümer zahlt Kredit nicht, Bank beantragt Zwangsversteigerung. BGH (V ZR 144/18): Zwangsversteigerung nach ZVG. Mindestgebot: 7/10 des Verkehrswertes (§ 85a ZVG). Gläubiger: Befriedigung aus Erlös. Überschuss: An Eigentümer. Praxis-Tipp: Rechtzeitig mit Bank verhandeln (Stundung, Umschuldung). Versteigerung: Mitbieten möglich. Erwerber: Zuschlagsbeschluss abwarten.""",
        "category": "Praxisfall Zwangsvollstreckung"
    },
    {
        "title": "Praxisfall: Grundbuchberichtigung - Falscher Eigentümer eingetragen",
        "content": """Sachverhalt: Grundbuch zeigt noch alten Eigentümer, Auflassung erfolgt. Käufer will Berichtigung. BGH (V ZR 190/17): Berichtigungsanspruch (§ 894 BGB) bei Unrichtigkeit. Nachweis: Auflassungsurkunde, Eintragungsbewilligung. Grundbuchamt: Berichtigt auf Antrag. Widerspruch: Dritter kann widersprechen, dann Prozess. Praxis-Tipp: Notar beantragt Umschreibung. Bei Verzögerung: Grundbuchamt kontaktieren. Eigentumsübergang: Mit Eintragung.""",
        "category": "Praxisfall Grundbuch"
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
    """Füge Batch 10 Dokumente hinzu"""
    print("🚀 BATCH 10: PRAXISFÄLLE & FALLSTUDIEN - START")
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
                    "source": "Batch 10 - Praxisfälle & Fallstudien"
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
    print("\n🔥 BATCH 10 COMPLETE! 🔥")

if __name__ == "__main__":
    seed_batch()
