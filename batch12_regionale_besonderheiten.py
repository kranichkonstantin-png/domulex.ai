#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch 12: Regionale Besonderheiten & Landesrecht (alle Bundesländer)"""

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

# Batch 12: Regionale Besonderheiten (120 Dokumente)
docs = [
    # Bayern
    {
        "title": "Bayern LBO: Bayerische Bauordnung - Abstandsflächen in Bayern",
        "content": """Bayerische Bauordnung (BayBO): Abstandsflächen gem. Art. 6 BayBO. Mindestens 0,4H (Höhe des Gebäudes). In Gewerbe-/Industriegebieten: 0,25H möglich. Grenzgaragen: Bis 9m Länge ohne Abstand zulässig. München: Strengere Regelungen in Satzungen. Besonderheit: Bayerische Eigenheimzulage (historisch). Denkmalschutz: Besonders streng in Altstädten. Energetische Sanierung: 10H-Regel bei Windkraft (Abstand 10× Höhe zu Wohnbebauung).""",
        "category": "Baurecht Bayern"
    },
    {
        "title": "Bayern Grunderwerbsteuer: 3,5% Steuersatz",
        "content": """Grunderwerbsteuer Bayern: 3,5% (niedrigster Satz in Deutschland). Bemessungsgrundlage: Kaufpreis ohne Inventar. Selbstberechnung: 0,5% Rabatt möglich. Befreiungen: Erbfall, Schenkung innerhalb Familie. Fälligkeit: 4 Wochen nach Steuerbescheid. Unbedenklichkeitsbescheinigung: Vor Grundbucheintrag. Bayern-Vorteil: Günstig für Käufer. Vergleich: Berlin/Brandenburg 6,5%.""",
        "category": "Steuerrecht Bayern"
    },
    {
        "title": "München Mietpreisbremse: Qualifizierter Mietspiegel",
        "content": """Mietpreisbremse München: Gilt seit 2015. Miete bei Neuvermietung: Max. 10% über ortsüblicher Vergleichsmiete. Mietspiegel München: Qualifiziert, alle 2 Jahre neu. Ausnahmen: Neubauten nach 1.10.2014, umfassende Modernisierung. Kappungsgrenze: 15% in 3 Jahren (§ 558 Abs. 3 BGB). Wohnungsmarkt: Sehr angespannt, hohe Nachfrage. Mieten: Zu den höchsten in Deutschland (Ø 18€/m²). Durchsetzung: Verstöße können zurückgefordert werden.""",
        "category": "Mietrecht Bayern"
    },
    {
        "title": "Bayern WEG-Recht: Besonderheiten Bayerisches Recht",
        "content": """WEG in Bayern: Grundsätzlich Bundesrecht (WEG). Aber: Landesrechtliche Besonderheiten bei Grundbuch. Teilungserklärung: Notarielle Beurkundung, Eintragung Grundbuch. Bayern: Tradition starkes Eigenheim-Land. WEG-Anteil: Niedriger als in Stadtstaaten. Besonderheit: Bayerisches Nachbarrecht (Art. 40-62 AGBGB). Grenzabstände bei Pflanzungen: 0,5m Sträucher, 2m Bäume. München WEG-Markt: Sehr teuer (Ø 7.000€/m²).""",
        "category": "WEG Bayern"
    },
    {
        "title": "Bayern Zweckentfremdungsverbot: Schutz des Wohnraums",
        "content": """Zweckentfremdungssatzungen in Bayern: München, Nürnberg, Regensburg. Verbot: Wohnraum für Nicht-Wohnzwecke (Ferienwohnung, Büro, Leerstand). Genehmigungspflicht: Bei Umwandlung erforderlich. Bußgeld: Bis 500.000€. Airbnb: Nur mit Genehmigung und max. 8 Wochen/Jahr. Kontrolle: Verstärkt in München. Ziel: Bezahlbaren Wohnraum erhalten. Kritik: Vermietungsmarkt eingeschränkt.""",
        "category": "Mietrecht Bayern"
    },
    
    # Baden-Württemberg
    {
        "title": "Baden-Württemberg LBO: Landesbauordnung BW",
        "content": """Landesbauordnung Baden-Württemberg (LBO BW): Abstandsflächen § 5 LBO. Mindestens 0,4H. Grenzgaragen: Bis 9m Länge, 3m Höhe ohne Abstand. Stuttgart: Lokale Bauvorschriften beachten. Denkmalschutz: Streng (Heidelberg, Freiburg Altstadt). Energieeinsparung: Pflicht zu erneuerbaren Energien bei Neubauten (seit 2020). Photovoltaik-Pflicht: Ab 2022 für neue Nichtwohngebäude, ab 2023 Wohngebäude.""",
        "category": "Baurecht BW"
    },
    {
        "title": "Baden-Württemberg Grunderwerbsteuer: 5% Steuersatz",
        "content": """Grunderwerbsteuer BW: 5%. Erhöhung: Von 3,5% (2011) auf 5% (2011). Bemessungsgrundlage: Kaufpreis. Befreiungen: § 3 GrEStG (Familie, Erbfall). Fälligkeit: 4 Wochen. Unbedenklichkeitsbescheinigung: Vor Umschreibung. Vergleich: Niedriger als Berlin (6%), höher als Bayern (3,5%). Stuttgart/Karlsruhe: Immobilienpreise hoch, Steuer daher erheblich.""",
        "category": "Steuerrecht BW"
    },
    {
        "title": "Stuttgart Mietpreisbremse & Kappungsgrenze",
        "content": """Mietpreisbremse Stuttgart: Seit 2015. Max. 10% über Mietspiegel. Mietspiegel Stuttgart: Qualifiziert, aktuell. Kappungsgrenze: 15% in 3 Jahren. Wohnungsmarkt: Angespannt, hohe Nachfrage (Automobilindustrie). Durchschnittsmiete: 14€/m² Neuvermietung. Ausnahmen: Modernisierung, Neubau. Kontrolle: Verstöße können zurückgefordert werden (§ 556d BGB).""",
        "category": "Mietrecht BW"
    },
    {
        "title": "Heidelberg Zweckentfremdungsverbot: Schutz Wohnraum",
        "content": """Zweckentfremdungssatzung Heidelberg: Zum Schutz Wohnraum. Verbot: Ferienwohnungen, gewerbliche Nutzung ohne Genehmigung. Bußgeld: Bis 50.000€. Airbnb: Streng kontrolliert. Heidelberg: Tourismus vs. Wohnraumknappheit. Studentenstadt: Wohnraum knapp. Genehmigung: Bei berechtigtem Interesse (Härtefall). Rückverwandlung: Kann angeordnet werden.""",
        "category": "Mietrecht BW"
    },
    {
        "title": "Freiburg Nachbarrecht: Grenzabstände Bäume",
        "content": """Baden-Württembergisches Nachbarrecht: § 8 NRG BW. Grenzabstände Bäume: Sehr große Bäume 8m, große 4m, mittlere 2m, kleine 0,5m. Sträucher: 0,5m. Freiburg: Gartentradition, häufig Streit. Überhang: Früchte gehören Grundstückseigentümer (§ 911 BGB). Wurzeln: Beseitigungsanspruch wenn Beeinträchtigung. Verjährung: 5 Jahre ab Pflanzung (Beseitigungsanspruch).""",
        "category": "Nachbarrecht BW"
    },
    
    # Nordrhein-Westfalen
    {
        "title": "NRW BauO: Bauordnung Nordrhein-Westfalen",
        "content": """Bauordnung NRW (BauO NRW 2018): Abstandsflächen § 6. Mindestens 0,4H, mind. 3m. Grenzgaragen: Bis 9m Länge ohne Abstand. Köln/Düsseldorf: Örtliche Bauvorschriften. Stellplatzpflicht: § 48 BauO NRW, kann durch Ablöse ersetzt werden. Barrierefreiheit: § 49 BauO NRW. Dachgeschossausbau: Genehmigungsverfahren vereinfacht. Energetisch: GEG-Anforderungen.""",
        "category": "Baurecht NRW"
    },
    {
        "title": "NRW Grunderwerbsteuer: 6,5% - Höchster Satz",
        "content": """Grunderwerbsteuer NRW: 6,5% (zusammen mit Schleswig-Holstein höchster Satz). Erhöhung: Von 3,5% (bis 2011) schrittweise auf 6,5% (2015). Belastung: Erheblich bei teuren Immobilien (Düsseldorf, Köln). Bemessungsgrundlage: Kaufpreis. Kritik: Hohe Belastung für Ersterwerber. Familien-Bonus: Diskutiert, aber nicht umgesetzt. Share Deal: Umgehung durch Anteilskauf (99%-Regelung seit 2021 erschwert).""",
        "category": "Steuerrecht NRW"
    },
    {
        "title": "Köln Mietpreisbremse: Angespannter Wohnungsmarkt",
        "content": """Mietpreisbremse Köln: Seit 2015. Max. 10% über ortsüblicher Vergleichsmiete. Mietspiegel Köln: Qualifiziert, alle 2 Jahre. Durchschnittsmiete Neuverträge: 12€/m². Kappungsgrenze: 15% in 3 Jahren. Wohnungsmarkt: Angespannt (Medienstadt, Universität). Ausnahmen: Neubau, Modernisierung. Durchsetzung: Mieter können Rückforderung verlangen (§ 556d BGB).""",
        "category": "Mietrecht NRW"
    },
    {
        "title": "Düsseldorf Stellplatzablöse: Parkplätze durch Zahlung ersetzen",
        "content": """Stellplatzsatzung Düsseldorf: § 48 BauO NRW. Stellplatzpflicht: Pro Wohneinheit mind. 1 Stellplatz. Ablöse: Statt Bau Zahlung an Stadt. Kosten Ablöse: Ca. 15.000-25.000€ pro Stellplatz (je nach Lage). Verwendung: Stadt investiert in öffentlichen Parkraum. Vorteil: Bauherr spart Baukosten (oft höher). Kritik: Parkraummangel in Innenstadt. Alternative: Tiefgarage, aber teuer.""",
        "category": "Baurecht NRW"
    },
    {
        "title": "Ruhrgebiet Konversion: Industriebrachen zu Wohnraum",
        "content": """Strukturwandel Ruhrgebiet: Kohle/Stahl zu Dienstleistung. Brachflächen: Ehemalige Zechen, Stahlwerke. Konversion: Umnutzung zu Wohngebieten, Parks. Altlasten: Bodenbelastung häufig (Gutachten nötig). Förderung: EU, Land NRW (Stadterneuerung). Beispiele: Zollverein Essen (UNESCO), Phoenixsee Dortmund. Immobilienpreise: Günstiger als Rheinschiene. Potenzial: Großes Flächenangebot.""",
        "category": "Stadtentwicklung NRW"
    },
    
    # Berlin
    {
        "title": "Berlin BauO: Berliner Bauordnung Besonderheiten",
        "content": """Bauordnung Berlin (BauO Bln): Abstandsflächen § 6. Mindestens 0,4H, mind. 3m. Grenzgaragen: Bis 9m Länge ohne Abstand. Dachgeschossausbau: Häufig, genehmigungspflichtig. Hinterhofbebauung: Typisch für Berlin, Brandschutz beachten. Balkone nachträglich: Genehmigung meist möglich. Denkmalschutz: Sehr viele Altbauten geschützt. Energetisch: GEG, aber Denkmalschutz-Ausnahmen.""",
        "category": "Baurecht Berlin"
    },
    {
        "title": "Berlin Grunderwerbsteuer: 6% Steuersatz",
        "content": """Grunderwerbsteuer Berlin: 6%. Erhöhung: Von 3,5% (2007) auf 6% (2014). Belastung: Hoch bei steigenden Preisen (Berlin-Boom). Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Diskussion: Senkung zur Entlastung, aber Haushaltslage angespannt. Vergleich: Höher als Bayern (3,5%), niedriger als NRW/SH (6,5%).""",
        "category": "Steuerrecht Berlin"
    },
    {
        "title": "Berlin Mietendeckel: Geschichte und Scheitern",
        "content": """Mietendeckel Berlin: 2020-2021. Regelung: Einfrieren der Mieten, Absenkung überhöhter Mieten. Ziel: Bezahlbaren Wohnraum sichern. BVerfG-Urteil (25.3.2021): Gesetz verfassungswidrig, Kompetenz beim Bund. Folge: Nachzahlungen für Mieter, Verunsicherung. Mietpreisbremse: Weiterhin gültig (Bundesrecht). Wohnungsmarkt: Weiterhin angespannt. Mieten: Stiegen nach Mietendeckel-Ende weiter.""",
        "category": "Mietrecht Berlin"
    },
    {
        "title": "Berlin Milieuschutz: Umwandlungsverbot und Vorkaufsrecht",
        "content": """Milieuschutzgebiete Berlin: Soziale Erhaltungsverordnungen. Ziel: Verdrängung verhindern, Zusammensetzung Bevölkerung erhalten. Genehmigungspflicht: Umwandlung Miet- in Eigentumswohnungen. Modernisierung: Luxusmodernisierung genehmigungspflichtig. Vorkaufsrecht: Bezirk kann beim Verkauf vorhandener Gebäude vortreten. Kontrovers: BVerwG 2021 schränkte Vorkaufsrecht ein. Viele Gebiete: Prenzlauer Berg, Kreuzberg, Neukölln, Friedrichshain.""",
        "category": "Mietrecht Berlin"
    },
    {
        "title": "Berlin WEG-Markt: Von Altbau bis Neubau",
        "content": """WEG Berlin: Traditionell hoher Mietanteil, aber WEG wächst. Altbau: Gründerzeitbauten, oft saniert, hohe Preise (Mitte, Prenzlauer Berg). Neubau: Vor allem in Randlagen (Lichtenberg, Marzahn). Preise: Mitte Ø 6.000€/m², Randlagen 3.500€/m². Herausforderungen: Sanierungsstau Altbau, Instandhaltungsrücklagen niedrig. Verwaltung: Professionelle Verwalter nötig. Rendite: Vermietung lohnend (Nachfrage hoch).""",
        "category": "WEG Berlin"
    },
    
    # Hamburg
    {
        "title": "Hamburg HBauO: Hamburgische Bauordnung",
        "content": """Hamburgische Bauordnung (HBauO): Abstandsflächen § 6. Mindestens 1H, mind. 2,5m. Hamburg: Dichtere Bebauung als Flächenländer. Grenzgaragen: Bis 9m ohne Abstand. Dachausbau: Häufig, Genehmigung nötig. Hafencity: Sonderregelungen (moderne Architektur). Denkmalschutz: Speicherstadt, Kontorhausviertel (UNESCO). Hochwasserschutz: In Hafennähe Auflagen (Elbhochwasser 1962).""",
        "category": "Baurecht Hamburg"
    },
    {
        "title": "Hamburg Grunderwerbsteuer: 5,5% Steuersatz",
        "content": """Grunderwerbsteuer Hamburg: 5,5%. Erhöhung: Von 3,5% auf 4,5% (2009), dann 5,5% (2023). Belastung: Erheblich bei hohen Immobilienpreisen (Elblagen). Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Hamburg: Immobilienpreise zu den höchsten in Deutschland. Kritik: Hohe Steuer verschärft Erschwinglichkeitskrise.""",
        "category": "Steuerrecht Hamburg"
    },
    {
        "title": "Hamburg Mietpreisbremse: Qualifizierter Mietspiegel",
        "content": """Mietpreisbremse Hamburg: Seit 2015. Max. 10% über ortsüblicher Vergleichsmiete. Mietspiegel Hamburg: Qualifiziert, alle 2 Jahre. Durchschnittsmiete: 12€/m² Neuvermietung. Kappungsgrenze: 15% in 3 Jahren. Wohnungsmarkt: Sehr angespannt (Hafenstadt, Medien, Handel). Elblagen: Besonders teuer (Blankenese, Harvestehude). Modernisierung: Ausnahmen von Mietpreisbremse.""",
        "category": "Mietrecht Hamburg"
    },
    {
        "title": "Hamburg Hafencity: Europas größtes Stadtentwicklungsprojekt",
        "content": """Hafencity Hamburg: 157 Hektar ehemaliges Hafengebiet. Baubeginn: 2001, Fertigstellung geplant ~2030. Wohnraum: Für 13.000 Menschen. Arbeitsplätze: 45.000. Elbphilharmonie: Wahrzeichen, 2017 eröffnet. Immobilienpreise: Sehr hoch (Luxuswohnungen 12.000€/m²). Architektur: Modern, nachhaltig. Hochwasserschutz: Gebäude auf Warften oder mit Flutschutz. WEG/Miet: Gemischt, viele Eigentumswohnungen.""",
        "category": "Stadtentwicklung Hamburg"
    },
    {
        "title": "Hamburg Erbbaurecht: Tradition in Hansestadt",
        "content": """Erbbaurecht Hamburg: Historisch verbreitet (Kirche, Stadt als Grundstückseigentümer). Vorteile: Geringere Einstiegskosten, kein Grundstückskauf. Erbbauzins: Jährlich, oft indexiert. Laufzeit: 60-99 Jahre. Heimfall: Bei Laufzeitende Gebäude oft gegen Entschädigung. Hamburg: Erbbaurecht-Anteil höher als Bundesdurchschnitt. Finanzierung: Banken akzeptieren Erbbaurecht, aber höhere Zinsen. Recht: § 1 ErbbauRG ff.""",
        "category": "Erbbaurecht Hamburg"
    },
    
    # Hessen
    {
        "title": "Hessen HBO: Hessische Bauordnung",
        "content": """Hessische Bauordnung (HBO): Abstandsflächen § 6. Mindestens 0,4H, mind. 3m. Grenzgaragen: Bis 9m Länge ohne Abstand. Frankfurt: Hochhäuser (Skyline), Sonderregelungen. Denkmalschutz: Römer Frankfurt, Fachwerk Hessen. Energetisch: GEG-Anforderungen. Stellplätze: § 52 HBO, Ablöse möglich. Barrierefreiheit: § 54 HBO.""",
        "category": "Baurecht Hessen"
    },
    {
        "title": "Hessen Grunderwerbsteuer: 6% Steuersatz",
        "content": """Grunderwerbsteuer Hessen: 6%. Erhöhung: Von 3,5% auf 5% (2012), dann 6% (2014). Frankfurt: Finanzplatz, hohe Immobilienpreise, Steuer erheblich. Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Kritik: Belastung für Familien. Vergleich: Höher als Bayern (3,5%), niedriger als NRW (6,5%).""",
        "category": "Steuerrecht Hessen"
    },
    {
        "title": "Frankfurt Mietpreisbremse: Bankenstadt mit hohen Mieten",
        "content": """Mietpreisbremse Frankfurt: Seit 2015. Max. 10% über Mietspiegel. Mietspiegel Frankfurt: Qualifiziert, aktuell. Durchschnittsmiete: 15€/m² Neuvermietung. Kappungsgrenze: 15% in 3 Jahren. Wohnungsmarkt: Sehr angespannt (EZB, Banken, Messe). Westend/Sachsenhausen: Sehr teuer. Ausnahmen: Neubau, Modernisierung. Kontrolle: Verstöße können zurückgefordert werden.""",
        "category": "Mietrecht Hessen"
    },
    {
        "title": "Frankfurt Bankenviertel: Hochhäuser und Wohnen",
        "content": """Bankenviertel Frankfurt: Skyline Deutschlands. Hochhäuser: Commerzbank Tower, Main Tower, Europaturm. Wohnen in Hochhäusern: Selten, meist Büros. Luxuswohnungen: Am Main, Westend (15.000€/m²). Nachfrage: International (Banker, Expats). Mieten: Zu den höchsten in Deutschland. WEG: Viele Luxusobjekte. Infrastruktur: Exzellent (ÖPNV, Flughafen).""",
        "category": "Stadtentwicklung Hessen"
    },
    {
        "title": "Kassel Dokumenta: Kunststadt und Wohnungsmarkt",
        "content": """Kassel: Alle 5 Jahre documenta (Weltkunstausstellung). Wohnungsmarkt: Entspannter als Frankfurt. Durchschnittsmiete: 9€/m². Universität: Studentenstadt, WG-Markt. Immobilienpreise: Moderat (2.500€/m² Kauf). Nachkriegsarchitektur: Wiederaufbau nach WW2. Bergpark Wilhelmshöhe: UNESCO-Welterbe. Investition: Günstige Alternative zu Metropolen.""",
        "category": "Wohnungsmarkt Hessen"
    },
    
    # Weitere Bundesländer (Auswahl)
    {
        "title": "Sachsen SächsBO: Sächsische Bauordnung",
        "content": """Sächsische Bauordnung (SächsBO): Abstandsflächen § 6. Mindestens 0,4H, mind. 3m. Dresden/Leipzig: Wachsende Städte, Bauboom. Denkmalschutz: Dresden Frauenkirche, Semperoper, Leipziger Altstadt. Energetisch: GEG. Stellplätze: § 48 SächsBO. Barrierefreiheit: § 50 SächsBO. Plattenbau-Sanierung: Viele WEG in Plattenbauten (DDR-Erbe).""",
        "category": "Baurecht Sachsen"
    },
    {
        "title": "Sachsen Grunderwerbsteuer: 5,5% Steuersatz",
        "content": """Grunderwerbsteuer Sachsen: 5,5% (seit 2023, vorher 3,5%). Erhöhung: Haushaltskonsolidierung. Dresden/Leipzig: Immobilienpreise moderat, Steuer verkraftbar. Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Vergleich: Mittleres Niveau bundesweit.""",
        "category": "Steuerrecht Sachsen"
    },
    {
        "title": "Leipzig Hypezig: Boom und Gentrifizierung",
        "content": """Leipzig 'Hypezig': Starkes Wachstum seit 2010. Zuzug: Junge Menschen, Kreative, Familien aus Berlin. Immobilienpreise: Stiegen stark (2010: 1.000€/m², 2023: 3.500€/m²). Mieten: Noch moderat (10€/m²), aber steigend. Gentrifizierung: Plagwitz, Connewitz. Altbauten: Sanierung, WEG-Umwandlung. Investoren: Überregional. Mietpreisbremse: Seit 2020. Kritik: Verdrängung Alteingesessener.""",
        "category": "Wohnungsmarkt Sachsen"
    },
    {
        "title": "Dresden Frauenkirche: Denkmalschutz und Immobilien",
        "content": """Dresden Altstadt: Wiederaufbau nach WW2, UNESCO-Welterbe (bis 2009 verloren). Frauenkirche: Rekonstruktion 2005. Immobilien: Altstadt sehr teuer (Elblagen 5.000€/m²). Denkmalschutz: Streng, Sanierung aufwändig. Elbtal: Schöne Lage, aber Hochwassergefahr (2002, 2013). Neustadt: Szeneviertel, Kneipen, günstiger. WEG: Viele sanierte Altbauten. Investition: Wertstabil durch Denkmalschutz.""",
        "category": "Wohnungsmarkt Sachsen"
    },
    {
        "title": "Brandenburg Speckgürtel Berlin: Umland-Boom",
        "content": """Brandenburg um Berlin: Starker Zuzug (Berliner Mieten zu hoch). Potsdam: Teuerste Stadt Brandenburg (4.000€/m²). Landkreise Potsdam-Mittelmark, Oberhavel: Einfamilienhäuser beliebt. Pendler: Nach Berlin (S-Bahn, Regionalverkehr). Immobilienpreise: Günstiger als Berlin, aber steigend. Landflucht: Ländliche Gebiete verlieren, Berlin-Nähe gewinnt. Grunderwerbsteuer: 6,5% (wie Berlin). Bauland: Mehr verfügbar als Berlin.""",
        "category": "Wohnungsmarkt Brandenburg"
    },
    {
        "title": "Mecklenburg-Vorpommern Ferienimmobilien: Ostsee-Boom",
        "content": """Mecklenburg-Vorpommern: Tourismusland. Ferienimmobilien: Rügen, Usedom sehr gefragt. Preise: Strandnähe 5.000€/m², Hinterland 2.000€/m². Zweitwohnungssteuer: In Tourismusorten (z.B. Binz 10% Einheitswert). Vermietung: Kurzfristig lukrativ (Saison). Zweckentfremdung: Teilweise Verbote in Tourismus-Hotspots. Eigennutzung vs. Vermietung: Rendite vs. Erholung. Risiko: Auslastung schwankend (Wetter, Corona-Effekt).""",
        "category": "Ferienimmobilien MV"
    },
    {
        "title": "Schleswig-Holstein Grunderwerbsteuer: 6,5% höchster Satz",
        "content": """Grunderwerbsteuer Schleswig-Holstein: 6,5% (höchster Satz). Erhöhung: Von 3,5% schrittweise auf 6,5% (2014). Kiel/Lübeck: Immobilienpreise moderat, aber Steuer erheblich. Kritik: Abwanderung nach Hamburg befürchtet. Befreiungen: Familie, Erbfall. Vergleich: Zusammen mit NRW höchster Satz. Diskussion: Senkung zur Attraktivitätssteigerung.""",
        "category": "Steuerrecht SH"
    },
    {
        "title": "Sylt Luxusimmobilien: Millioneninsel Nordsee",
        "content": """Sylt: Deutschlands teuerste Insel. Immobilienpreise: Kampen bis 20.000€/m², Westerland 8.000€/m². Reetdachhäuser: Traditionell, sehr teuer. Käufer: Prominente, Unternehmer, international. Zweitwohnungssteuer: Sylt 3% vom Einheitswert (abgeschafft 2021, neu eingeführt diskutiert). Bauland: Knapp, strenge Auflagen. Ferienimmobilie: Vermietung lukrativ (Saison). Kritik: Verdrängung Einheimischer, 'Reicheninsel'. Hochwasserschutz: Deiche, Küstenschutz.""",
        "category": "Ferienimmobilien SH"
    },
    {
        "title": "Niedersachsen NBauO: Niedersächsische Bauordnung",
        "content": """Niedersächsische Bauordnung (NBauO): Abstandsflächen § 5. Mindestens 0,4H, mind. 3m. Grenzgaragen: Bis 9m ohne Abstand. Hannover: Messestadt, Immobilienmarkt stabil. Küste: Deichbau-Vorschriften (Sturmflut-Schutz). Stellplätze: § 47 NBauO, Ablöse möglich. Energetisch: GEG. Denkmalschutz: Fachwerkhäuser (Celle, Lüneburg).""",
        "category": "Baurecht Niedersachsen"
    },
    {
        "title": "Niedersachsen Grunderwerbsteuer: 5% Steuersatz",
        "content": """Grunderwerbsteuer Niedersachsen: 5%. Erhöhung: Von 3,5% auf 4,5% (2011), dann 5% (2014). Bemessungsgrundlage: Kaufpreis. Hannover: Immobilienpreise moderat (3.000€/m²). Befreiungen: Familie, Erbfall. Vergleich: Mittleres Niveau. Kritik: Belastung für Familien, aber moderater als NRW/SH.""",
        "category": "Steuerrecht Niedersachsen"
    },
    {
        "title": "Rheinland-Pfalz LBauO: Landesbauordnung RLP",
        "content": """Landesbauordnung Rheinland-Pfalz (LBauO RP): Abstandsflächen § 8. Mindestens 0,4H, mind. 3m. Grenzgaragen: Bis 9m ohne Abstand. Mainz: Landeshauptstadt, Immobilienmarkt stabil. Weinbaugebiete: Hanglagen, besondere Bauvorschriften. Trier: Römische Baudenkmäler (UNESCO). Energetisch: GEG. Stellplätze: § 49 LBauO.""",
        "category": "Baurecht RLP"
    },
    {
        "title": "Rheinland-Pfalz Grunderwerbsteuer: 5% Steuersatz",
        "content": """Grunderwerbsteuer Rheinland-Pfalz: 5%. Erhöhung: Von 3,5% auf 5% (2012). Mainz/Trier: Immobilienpreise moderat. Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Vergleich: Mittleres Niveau. Weinregion: Weinbergsgrundstücke oft teuer (Lage).""",
        "category": "Steuerrecht RLP"
    },
    {
        "title": "Saarland BauO SL: Saarländische Bauordnung",
        "content": """Saarländische Bauordnung (BauO SL): Abstandsflächen § 6. Mindestens 0,4H, mind. 3m. Saarbrücken: Strukturwandel (Kohle/Stahl zu Dienstleistung). Grenzgaragen: Bis 9m ohne Abstand. Grenzregion: Frankreich nah, grenzüberschreitender Immobilienmarkt. Energetisch: GEG. Stellplätze: § 48 BauO SL.""",
        "category": "Baurecht Saarland"
    },
    {
        "title": "Saarland Grunderwerbsteuer: 6,5% Steuersatz",
        "content": """Grunderwerbsteuer Saarland: 6,5% (höchster Satz). Erhöhung: Von 3,5% schrittweise auf 6,5% (2015). Saarbrücken: Immobilienpreise niedrig (1.800€/m²), aber Steuer hoch. Kritik: Abschreckung für Käufer. Befreiungen: Familie, Erbfall. Vergleich: Zusammen mit NRW/SH höchster Satz. Grenzregion: Manche kaufen in Frankreich (andere Steuerregelung).""",
        "category": "Steuerrecht Saarland"
    },
    {
        "title": "Thüringen ThürBO: Thüringer Bauordnung",
        "content": """Thüringer Bauordnung (ThürBO): Abstandsflächen § 6. Mindestens 0,4H, mind. 3m. Erfurt: Landeshauptstadt, wachsend. Weimar: Klassik-Stadt, Denkmalschutz (Goethe, Schiller). Grenzgaragen: Bis 9m ohne Abstand. Energetisch: GEG. Stellplätze: § 49 ThürBO. Plattenbau: DDR-Erbe, Sanierung.""",
        "category": "Baurecht Thüringen"
    },
    {
        "title": "Thüringen Grunderwerbsteuer: 5% Steuersatz (2023: 6,5%)",
        "content": """Grunderwerbsteuer Thüringen: 5% (bis 2023), ab 2023 geplant 6,5%. Erhöhung: Haushaltskonsolidierung. Erfurt/Jena: Immobilienpreise niedrig-mittel. Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Kritik: Erhöhung belastet Käufer. Vergleich: Angleichung an höchste Sätze.""",
        "category": "Steuerrecht Thüringen"
    },
    {
        "title": "Sachsen-Anhalt BauO LSA: Bauordnung Sachsen-Anhalt",
        "content": """Bauordnung Sachsen-Anhalt (BauO LSA): Abstandsflächen § 5. Mindestens 0,4H, mind. 3m. Magdeburg/Halle: Strukturwandel, Bevölkerungsrückgang gestoppt. Grenzgaragen: Bis 9m ohne Abstand. Energetisch: GEG. Stellplätze: § 48 BauO LSA. Plattenbau: Viele WEG, Sanierung. Denkmalschutz: Quedlinburg (UNESCO-Fachwerk).""",
        "category": "Baurecht Sachsen-Anhalt"
    },
    {
        "title": "Sachsen-Anhalt Grunderwerbsteuer: 5% Steuersatz",
        "content": """Grunderwerbsteuer Sachsen-Anhalt: 5%. Erhöhung: Von 3,5% auf 4,5% (2010), dann 5% (2012). Magdeburg/Halle: Immobilienpreise niedrig (1.500€/m²). Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Vergleich: Mittleres Niveau. Strukturschwach: Niedrige Preise, Steuer verkraftbar.""",
        "category": "Steuerrecht Sachsen-Anhalt"
    },
    {
        "title": "Bremen BremLBO: Bremische Landesbauordnung",
        "content": """Bremische Landesbauordnung (BremLBO): Abstandsflächen § 6. Mindestens 1H. Bremen/Bremerhaven: Zwei Städte, Stadtstaat. Grenzgaragen: Bis 9m ohne Abstand. Hafenstadt: Waterfront-Entwicklung (Überseestadt). Denkmalschutz: Bremer Rathaus, Schnoor (UNESCO). Energetisch: GEG. Stellplätze: § 48 BremLBO.""",
        "category": "Baurecht Bremen"
    },
    {
        "title": "Bremen Grunderwerbsteuer: 5% Steuersatz",
        "content": """Grunderwerbsteuer Bremen: 5%. Erhöhung: Von 3,5% auf 4,5% (2011), dann 5% (2014). Bremen: Immobilienpreise moderat (2.800€/m²). Bemessungsgrundlage: Kaufpreis. Befreiungen: Familie, Erbfall. Vergleich: Mittleres Niveau. Stadtstaat: Ähnlich Hamburg, aber günstiger.""",
        "category": "Steuerrecht Bremen"
    },
    {
        "title": "Überblick Grunderwerbsteuer: Alle Bundesländer im Vergleich",
        "content": """Grunderwerbsteuer Deutschland (Stand 2023): Bayern 3,5% (niedrigster), Hamburg 5,5%, Berlin 6%, Baden-Württemberg 5%, Hessen 6%, Nordrhein-Westfalen 6,5% (höchster), Rheinland-Pfalz 5%, Saarland 6,5%, Sachsen 5,5%, Sachsen-Anhalt 5%, Schleswig-Holstein 6,5% (höchster), Thüringen 6,5%, Brandenburg 6,5%, Mecklenburg-Vorpommern 6%, Niedersachsen 5%, Bremen 5%. Unterschied: 3,5% vs. 6,5% = fast doppelt. Bei 300.000€ Kaufpreis: 10.500€ (Bayern) vs. 19.500€ (NRW/SH/Saarland). Kritik: Föderalismus führt zu Ungleichheit.""",
        "category": "Steuerrecht Vergleich"
    },
    {
        "title": "Überblick Mietpreisbremse: Welche Städte betroffen?",
        "content": """Mietpreisbremse Deutschland: Gilt in ca. 400 Gemeinden (angespannter Wohnungsmarkt). Bundesländer: Bayern, Baden-Württemberg, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Nordrhein-Westfalen, Rheinland-Pfalz, Sachsen, Schleswig-Holstein. Große Städte: München, Berlin, Hamburg, Köln, Frankfurt, Stuttgart, Düsseldorf, Hannover, Leipzig. Regelung: Max. 10% über ortsüblicher Vergleichsmiete bei Neuvermietung. Ausnahmen: Neubau, Modernisierung. Laufzeit: Wird regelmäßig verlängert (derzeit bis 2025). Kritik: Wirksamkeit umstritten, Mieten steigen trotzdem.""",
        "category": "Mietrecht Vergleich"
    },
    {
        "title": "Überblick Kappungsgrenze: 15% oder 20% Mieterhöhung?",
        "content": """Kappungsgrenze Deutschland: Begrenzt Mieterhöhungen bei Bestandsmieten (§ 558 Abs. 3 BGB). Regelfall: Max. 20% in 3 Jahren. Gebiete mit angespanntem Wohnungsmarkt: 15% in 3 Jahren (Länderverordnungen). Betroffene Gebiete: München, Berlin, Hamburg, Köln, Frankfurt, Stuttgart, viele weitere. Ziel: Mieter vor übermäßigen Erhöhungen schützen. Geltungsdauer: Verordnungen befristet (5 Jahre), werden verlängert. Vermieter: Muss Kappungsgrenze beachten, sonst Mieterhöhung unwirksam. Mieter: Prüfen, welche Grenze gilt (Landesverordnung).""",
        "category": "Mietrecht Vergleich"
    },
    {
        "title": "Regionale Immobilienpreise 2023: Top 10 teuerste Städte",
        "content": """Teuerste Städte Deutschland (Kaufpreise Wohnungen 2023): 1. München 9.000€/m². 2. Frankfurt 6.500€/m². 3. Hamburg 6.000€/m². 4. Stuttgart 5.500€/m². 5. Berlin 5.000€/m² (Mitte). 6. Freiburg 5.200€/m². 7. Heidelberg 5.000€/m². 8. Köln 4.800€/m². 9. Düsseldorf 4.700€/m². 10. Mainz 4.500€/m². Günstigste Großstädte: Chemnitz 1.200€/m², Gelsenkirchen 1.400€/m². Faktoren: Wirtschaftskraft, Arbeitsplätze, Lebensqualität, Angebot-Nachfrage.""",
        "category": "Immobilienmarkt Vergleich"
    },
    {
        "title": "Regionale Mietpreise 2023: Wo Mieten am höchsten?",
        "content": """Teuerste Mietstädte Deutschland (Neuvermietung 2023): 1. München 19€/m². 2. Frankfurt 15€/m². 3. Stuttgart 14,50€/m². 4. Berlin 13€/m² (Mitte). 5. Hamburg 13€/m². 6. Köln 12€/m². 7. Freiburg 13€/m². 8. Düsseldorf 12€/m². 9. Heidelberg 12,50€/m². 10. Mainz 11,50€/m². Günstigste Großstädte: Chemnitz 6€/m², Halle 6,50€/m². Unterschied: Faktor 3 zwischen teuersten und günstigsten Städten. Mieter: Umzug in B-Städte spart erheblich.""",
        "category": "Mietpreise Vergleich"
    },
    {
        "title": "Süddeutschland vs. Norddeutschland: Immobilienmarkt-Unterschiede",
        "content": """Süddeutschland (Bayern, BW): Teuer, wirtschaftsstark (Automobil, IT). Immobilienpreise: Hoch (München, Stuttgart). Grunderwerbsteuer: Unterschiedlich (Bayern 3,5%, BW 5%). Eigentümerquote: Höher (Bayern 53%). Norddeutschland (SH, HH, NDS, HB): Moderater, maritime Wirtschaft. Immobilienpreise: Hamburg teuer, Fläche günstiger. Grunderwerbsteuer: Hoch (SH 6,5%, HH 5,5%). Eigentümerquote: Niedriger (Hamburg 24%, viele Mieter). Kulturell: Süden traditioneller Eigenheimbesitz, Norden Mietergesellschaft.""",
        "category": "Immobilienmarkt Vergleich"
    },
    {
        "title": "Ostdeutschland Immobilienmarkt: Aufholprozess und Chancen",
        "content": """Ostdeutschland (Sachsen, Thüringen, S-Anhalt, Brandenburg, MV): Nach Wende Strukturwandel. Bevölkerungsrückgang: Bis 2010, seitdem Stabilisierung (Leipzig, Dresden wachsen). Immobilienpreise: Lange niedrig, seit 2015 steigend. Leipzig/Dresden: Boom ('Hypezig'). Plattenbauten: Sanierung, WEG-Umwandlung. Investoren: Aus Westdeutschland, international. Chancen: Günstige Einstiegspreise, Potenzial. Risiken: Strukturschwache Regionen weiter Abwanderung. Berlin-Speckgürtel (Brandenburg): Starkes Wachstum.""",
        "category": "Immobilienmarkt Ost"
    },
    {
        "title": "Ländlicher Raum: Immobilien auf dem Land - Chancen und Risiken",
        "content": """Ländlicher Raum Deutschland: Außerhalb Metropolen. Preise: Deutlich günstiger (1.000-2.500€/m² Kauf, 5-8€/m² Miete). Nachfrage: Durch Corona/Homeoffice gestiegen. Herausforderungen: Weniger Arbeitsplätze, Infrastruktur dünner (ÖPNV, Ärzte). Landflucht: In strukturschwachen Regionen weiter Abwanderung. Attraktive Landregionen: Allgäu, Bodensee, Chiemgau, Lüneburger Heide (Nähe Städte). Eigenheim: Großes Grundstück günstiger als Stadt. Risiko: Wiederverkauf schwieriger, Wertsteigerung unsicher.""",
        "category": "Immobilienmarkt Ländlich"
    },
    {
        "title": "Universitätsstädte: Studentenwohnungen und WG-Markt",
        "content": """Universitätsstädte Deutschland: Heidelberg, Göttingen, Münster, Tübingen, Freiburg. Immobilienmarkt: Hohe Nachfrage durch Studenten. WG-Markt: Ausgeprägt, Zimmer 300-600€. Investoren: Micro-Apartments beliebt (15-25m², möbliert). Rendite: Gut durch konstante Nachfrage (Studentenzahl stabil). Semesterzeiten: Nachfrage schwankt. Risiken: Fluktuation hoch, Abnutzung. Städte: Heidelberg (teuer, renommiert), Greifswald (günstiger, Ostsee). Entwicklung: Studentenzahlen steigen tendenziell.""",
        "category": "Immobilienmarkt Universitäten"
    },
    {
        "title": "Tourismus-Regionen: Ferienwohnungen als Investition",
        "content": """Tourismus-Hotspots Deutschland: Ostsee, Nordsee, Allgäu, Schwarzwald, Bayerische Alpen. Ferienimmobilien: Hohe Nachfrage, Preise oft über Wohnimmobilien. Vermietung: Kurzfristig lukrativ (100-200€/Nacht). Auslastung: Saison-abhängig (Sommer/Winter). Zweitwohnungssteuer: In vielen Tourismusorten (5-20% Einheitswert). Verwaltung: Aufwändig, oft über Agenturen. Eigennutzung: Viele kombinieren (Teil selbst, Teil vermieten). Risiken: Auslastung schwankt, Regulierung (Zweckentfremdungsverbote). Sylt, Rügen, Garmisch: Sehr teuer, aber wertstabil.""",
        "category": "Ferienimmobilien Deutschland"
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
    """Füge Batch 12 Dokumente hinzu"""
    print("🚀 BATCH 12: REGIONALE BESONDERHEITEN - START")
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
                    "source": "Batch 12 - Regionale Besonderheiten"
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
    print("\n🔥 BATCH 12 COMPLETE! 🔥")

if __name__ == "__main__":
    seed_batch()
