#!/usr/bin/env python3
"""Batch 7: Spezielle Immobilienarten & Gewerbeimmobilien - 100 Dokumente"""

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

# 100 Dokumente zu speziellen Immobilienarten
documents = []

# Gewerbeimmobilien (20 Docs)
gewimmo = [
    {"title": "Büroimmobilien: Standortfaktoren", "content": "Büro-Standort: ÖPNV-Anbindung, Parkplätze, Gastronomie, Image-Lage entscheidend. Mietpreise: CBD (City) höher als Peripherie. Trends: Home Office reduziert Flächenbedarf. Moderne Büros: Flexible Raumkonzepte, Co-Working-Bereiche. Wichtig: Digitale Infrastruktur essentiell!", "category": "Gewerbeimmobilien", "subcategory": "Büro"},
    {"title": "Einzelhandel: 1a-Lage Definition", "content": "1a-Lage Einzelhandel: Fußgängerzone, hohe Passantenfrequenz (>5.000/Tag), etablierte Filialisten als Nachbarn. Mietpreis: 100-500€/m² je nach Stadt. Risiko: E-Commerce-Konkurrenz. Wichtig: Lagequalität entscheidend für Erfolg!", "category": "Gewerbeimmobilien", "subcategory": "Einzelhandel"},
    {"title": "Logistikimmobilien: Standortkriterien", "content": "Logistik-Standort: Autobahnnähe (<5km), Flughafennähe, Güterbahnhof. Hallenhöhe: Mind. 10m für Hochregallager. Grundstücksgröße: Mind. 10.000m² für Logistikzentren. Wichtig: E-Commerce treibt Nachfrage!", "category": "Gewerbeimmobilien", "subcategory": "Logistik"},
    {"title": "Hotelimmobilien: Rendite-Struktur", "content": "Hotel-Rendite: Pachtmodell (6-8% fix) oder Managementvertrag (variabel). Risiko: Konjunkturabhängig, Standort kritisch. Bewertung: Nach Zimmerzahl x RevPAR. Wichtig: Betreiber-Bonität prüfen!", "category": "Gewerbeimmobilien", "subcategory": "Hotel"},
    {"title": "Gastronomie-Immobilien: Besonderheiten", "content": "Gastronomie: Hohe Fluktuation, spezielle Ausstattung (Küche, Lüftung). Miete: Oft umsatzabhängig. Nutzungsänderung: Schwierig (Lärm, Gerüche). Wichtig: Langfristige Verträge selten!", "category": "Gewerbeimmobilien", "subcategory": "Gastronomie"},
    {"title": "Arztpraxen: Standortanforderungen", "content": "Arztpraxen: EG bevorzugt, barrierefrei, Parkplätze, Sichtbarkeit. Mietdauer: Langfristig (10-20 Jahre). Umbau: Spezielle Anforderungen (Hygiene, Medizintechnik). Wichtig: Stabile Mieteinnahmen!", "category": "Gewerbeimmobilien", "subcategory": "Arztpraxis"},
    {"title": "Produktionshallen: Bauliche Anforderungen", "content": "Produktion: Deckenhöhe, Traglasten, Stromanschluss (Starkstrom), Hallentor-Größe. Genehmigung: Oft B-Plan GE/GI erforderlich. Lärm: Schallschutz bei Wohnbebauung. Wichtig: Spezialanforderungen beachten!", "category": "Gewerbeimmobilien", "subcategory": "Produktion"},
    {"title": "Pflegeheime: Investment-Struktur", "content": "Pflegeheim: Pachtvertrag 20-30 Jahre, Rendite 4-6%. Risiko: Betreiber-Insolvenz, Regulierung, Demografischer Wandel positiv. Wichtig: Betreiber-Bonität entscheidend!", "category": "Gewerbeimmobilien", "subcategory": "Pflegeheim"},
    {"title": "Kitas: Rendite und Förderung", "content": "Kitas: Stabiler Mieter (Träger oft öffentlich), Rendite 4-5%. Förderung: KfW, Kommunen. Standort: Wohngebiete, Erreichbarkeit. Wichtig: Langfristige Mietverträge!", "category": "Gewerbeimmobilien", "subcategory": "Kita"},
    {"title": "Fitnessstudios: Mietvertrag-Klauseln", "content": "Fitnessstudio: Lange Laufzeiten, hohe Mieten, spezielle Ausstattung. Risiko: Ketten-Insolvenz (McFit, FitX). Schallschutz: Wichtig bei Wohnbebauung. Wichtig: Bonität prüfen!", "category": "Gewerbeimmobilien", "subcategory": "Fitness"},
    {"title": "Coworking-Spaces: Trend", "content": "Coworking: Flexible Arbeitsplätze, kurze Mietverträge. Betreiber: WeWork, Design Offices. Rendite: 5-7%, aber volatil. Wichtig: Trend zu flexiblen Arbeitsformen!", "category": "Gewerbeimmobilien", "subcategory": "Coworking"},
    {"title": "Discounter-Immobilien: Triple-Net", "content": "Discounter (Aldi, Lidl): Triple-Net-Verträge (Mieter zahlt alles). Laufzeit: 10-15 Jahre, Rendite 4,5-5,5%. Standort: Wohngebiete, Parkplätze. Wichtig: Sehr stabile Investments!", "category": "Gewerbeimmobilien", "subcategory": "Einzelhandel"},
    {"title": "Bankfilialen: Rückgang", "content": "Bankfilialen: Massive Schließungen durch Digitalisierung. Nachnutzung: Gastronomie, Einzelhandel. Leerstand: Risiko bei Altverträgen. Wichtig: Trend zu weniger Filialen!", "category": "Gewerbeimmobilien", "subcategory": "Bank"},
    {"title": "Rechenzentren: Spezialanforderungen", "content": "Rechenzentren: Extreme Kühlung, Stromversorgung (Megawatt), Redundanz. Standort: Glasfaser, Strompreis. Sicherheit: Physisch + digital. Wichtig: Hochtechnologie-Immobilie!", "category": "Gewerbeimmobilien", "subcategory": "Rechenzentrum"},
    {"title": "Parkhäuser: Rendite-Kalkulation", "content": "Parkhäuser: Rendite 3-5%, Standort entscheidend (Innenstädte). Risiko: Elektromobilität, ÖPNV-Ausbau reduziert Bedarf. Betrieb: Oft outgesourct. Wichtig: Zukunftsfähigkeit fraglich!", "category": "Gewerbeimmobilien", "subcategory": "Parkhaus"},
    {"title": "Tankstellen: Altlasten-Risiko", "content": "Tankstellen: Hohes Altlasten-Risiko (Bodenkontamination). Pacht: Meist Ölkonzerne. Zukunft: E-Mobilität bedroht Geschäftsmodell. Wichtig: Umweltgutachten zwingend!", "category": "Gewerbeimmobilien", "subcategory": "Tankstelle"},
    {"title": "Gewerbeparks: Mixed-Use", "content": "Gewerbeparks: Mischung Büro, Produktion, Lager. Infrastruktur: Zentral organisiert (Kantine, Security). Vorteile: Synergien, Flexibilität. Wichtig: Professionelles Management!", "category": "Gewerbeimmobilien", "subcategory": "Gewerbepark"},
    {"title": "Freizeitimmobilien: Kino, Bowling", "content": "Freizeitimmobilien: Lange Laufzeiten, umsatzabhängige Mieten. Risiko: Streaming, Trends ändern sich. Standort: Erlebnis-Einkaufszentren. Wichtig: Volatiles Segment!", "category": "Gewerbeimmobilien", "subcategory": "Freizeit"},
    {"title": "Gewerbemietrecht: Unterschiede zu Wohnraum", "content": "Gewerbemiete: Freiere Vertragsgestaltung, keine Mietpreisbremse, keine Kündigungsfristen wie Wohnraum. Indexierung: Üblich. Wichtig: Vertragsfreiheit beachten!", "category": "Gewerbeimmobilien", "subcategory": "Gewerbemietrecht"},
    {"title": "Gewerbemiete: Umsatzmiete Modelle", "content": "Umsatzmiete: Grundmiete + Prozent vom Umsatz (5-15%). Vorteil: Risikoteilung. Nachteil: Umsatzoffenlegung, Kontrolle schwierig. Wichtig: Für Einzelhandel typisch!", "category": "Gewerbeimmobilien", "subcategory": "Gewerbemietrecht"},
]
documents.extend(gewimmo)

# Sonderimmobilien (15 Docs)
sonder = [
    {"title": "Landwirtschaftliche Immobilien: Bewertung", "content": "Landwirtschaft: Bewertung nach Ertragswert (Bodenqualität). Hofstelle: Wohn- und Wirtschaftsgebäude. Vorkaufsrecht: Landwirtschaftliche Siedlung. Wichtig: Spezielle Regelungen!", "category": "Sonderimmobilien", "subcategory": "Landwirtschaft"},
    {"title": "Forstwirtschaft: Waldflächen", "content": "Wald: Bewertung nach Holzbestand + Bodenwert. Bewirtschaftung: FSC/PEFC-Zertifizierung wertsteigernd. Steuer: Forstwirtschaft begünstigt. Wichtig: Langfristige Investition!", "category": "Sonderimmobilien", "subcategory": "Forstwirtschaft"},
    {"title": "Windkraftanlagen: Grundstücksnutzung", "content": "Windkraft: Pachtvertrag 20-30 Jahre, Pacht 30.000-80.000€/Anlage p.a. Standort: Windstärke entscheidend. Genehmigung: Komplex (Naturschutz). Wichtig: Stabile Einnahmen!", "category": "Sonderimmobilien", "subcategory": "Windkraft"},
    {"title": "Photovoltaik-Freiflächen: Pacht", "content": "PV-Freiflächenanlagen: Pacht 1.000-3.000€/ha pro Jahr. Laufzeit: 20-30 Jahre. Standort: Sonneneinstrahlung, Netzanschluss. Wichtig: EEG-Förderung!", "category": "Sonderimmobilien", "subcategory": "Photovoltaik"},
    {"title": "Golfplätze: Investment", "content": "Golfplatz: Hoher Flächenbedarf (50-100ha), hohe Unterhaltskosten. Mitglieder: Stabilität. Risiko: Demografischer Wandel (Golf altert). Wichtig: Nischen-Investment!", "category": "Sonderimmobilien", "subcategory": "Golf"},
    {"title": "Freizeitparks: Rendite", "content": "Freizeitpark: Hohe Initialinvestition, saisonale Einnahmen. Rendite: 3-5% bei etablierten Parks. Risiko: Wetter, Konkurrenz. Wichtig: Standort + Attraktionen entscheidend!", "category": "Sonderimmobilien", "subcategory": "Freizeitpark"},
    {"title": "Campingplätze: Boom", "content": "Camping: Boom durch Corona, steigende Nachfrage. Rendite: 4-7%. Saisonalität: In D meist April-Oktober. Wichtig: Glamping-Trend nutzen!", "category": "Sonderimmobilien", "subcategory": "Camping"},
    {"title": "Yachthäfen: Liegeplatz-Vermietung", "content": "Yachthafen: Liegeplatz-Vermietung + Nebenleistungen (Werkstatt, Shop). Standort: Küste, Seen. Genehmigung: Wasserrecht, Umweltschutz. Wichtig: Exklusives Segment!", "category": "Sonderimmobilien", "subcategory": "Yachthafen"},
    {"title": "Reitanlagen: Pferdepensionen", "content": "Reitanlage: Boxenvermietung + Reithalle + Weiden. Rendite: 3-5%. Aufwand: Personalintensiv. Zielgruppe: Pferdebesitzer (zahlungskräftig). Wichtig: Standort nah an Wohngebieten!", "category": "Sonderimmobilien", "subcategory": "Reitanlage"},
    {"title": "Winzer-Immobilien: Weingut", "content": "Weingut: Kombination Produktion + Tourismus (Weinprobe). Standort: Weinregionen. Investment: Komplex, Know-how erforderlich. Wichtig: Lifestyle-Investment!", "category": "Sonderimmobilien", "subcategory": "Weingut"},
    {"title": "Bergbahnen: Seilbahnen", "content": "Seilbahnen: Hohe Investition, Konzession erforderlich. Rendite: Von Wintersport-Tourismus abhängig. Risiko: Klimawandel. Wichtig: Tourismus-Region entscheidend!", "category": "Sonderimmobilien", "subcategory": "Bergbahn"},
    {"title": "Schwimmbäder: Öffentlich vs. Privat", "content": "Schwimmbäder: Öffentlich meist defizitär. Private: Fitnessstudio-Kombi erfolgreicher. Kosten: Energie, Personal hoch. Wichtig: Schwieriges Geschäftsmodell!", "category": "Sonderimmobilien", "subcategory": "Schwimmbad"},
    {"title": "Kiesgruben: Abbaurechte", "content": "Kiesgrube: Abbaurecht zeitlich begrenzt (10-30 Jahre). Rekultivierung: Pflicht nach Abbau. Wertentwicklung: Während Abbau steigend, danach Rekultivierung. Wichtig: Umweltauflagen!", "category": "Sonderimmobilien", "subcategory": "Kiesgrube"},
    {"title": "Solarparks: Freiflächenanlagen", "content": "Solarpark: Langfristige Pacht, EEG-Vergütung 20 Jahre. Flächenbedarf: 1-2ha pro MW. Standort: Sonnenstunden, Netzanschluss. Wichtig: Stabile Rendite!", "category": "Sonderimmobilien", "subcategory": "Solarpark"},
    {"title": "Biogasanlagen: Landwirtschaft", "content": "Biogasanlage: Substrate (Mais, Gülle), Strom + Wärme. Investition: 2-5 Mio€. EEG: Förderung. Risiko: Substrat-Verfügbarkeit, Nachbarschaftskonflikte. Wichtig: Komplexes Investment!", "category": "Sonderimmobilien", "subcategory": "Biogas"},
]
documents.extend(sonder)

# Denkmalimmobilien & Spezialnutzungen (15 Docs)
denkmal = [
    {"title": "Denkmalschutz: Steuervorteile Details", "content": "Denkmal-AfA: 9% über 8 Jahre (Eigennutzung) oder 9% über 8 + 7% über 4 Jahre (Vermietung). Sanierungskosten: Voll absetzbar. Voraussetzung: Bescheinigung Denkmalamt. Wichtig: Hohe Steuerersparnis!", "category": "Denkmalimmobilien", "subcategory": "Steuer"},
    {"title": "Denkmalschutz: Auflagen Sanierung", "content": "Denkmal-Auflagen: Fassade, Dach, Fenster meist original erhalten. Inneren: Mehr Freiheit. Genehmigung: Denkmalamt + Bauamt. Kosten: 20-50% höher als Standardsanierung. Wichtig: Auflagen genau prüfen!", "category": "Denkmalimmobilien", "subcategory": "Auflagen"},
    {"title": "Baudenkmal: Finanzierung", "content": "Denkmal-Finanzierung: Banken zurückhaltend (höhere Kosten). Förderung: KfW, Denkmalschutz-Programme. Eigenkapital: 30-40% empfohlen. Wichtig: Spezialisierte Banken nutzen!", "category": "Denkmalimmobilien", "subcategory": "Finanzierung"},
    {"title": "Ensembleschutz: Gesamtanlagen", "content": "Ensembleschutz: Nicht nur Einzelgebäude, sondern gesamtes Ensemble geschützt. Auflagen: Auch für nicht-denkmalgeschützte Gebäude im Ensemble. Wichtig: Restriktiver als Einzeldenkmal!", "category": "Denkmalimmobilien", "subcategory": "Ensembleschutz"},
    {"title": "Kirchenimmobilien: Umnutzung", "content": "Kirchen-Umnutzung: Zu Wohnungen, Kulturzentren, Kletterh allen. Herausforderung: Hohe Räume, Akustik, Denkmalschutz. Markt: Wachsend (Kirchenschließungen). Wichtig: Kreative Lösungen gefragt!", "category": "Denkmalimmobilien", "subcategory": "Umnutzung"},
    {"title": "Bunker-Umbauten: Potenzial", "content": "Bunker: Massive Wände, oft denkmalgeschützt. Umnutzung: Wohnungen, Data Center, Urban Gardening. Herausforderung: Wenig Licht, Genehmigungen. Wichtig: Ausgefallene Projekte!", "category": "Sonderimmobilien", "subcategory": "Bunker"},
    {"title": "Leuchttürme: Nutzungskonzepte", "content": "Leuchtturm: Ferienwohnungen, Museum, Events. Eigentümer: Oft Bund, Länder. Pacht: Symbolische Beträge, aber hohe Unterhaltskosten. Wichtig: Romantik vs. Realität!", "category": "Sonderimmobilien", "subcategory": "Leuchtturm"},
    {"title": "Wassermühlen: Revitalisierung", "content": "Wassermühle: Wasserkraft-Nutzung möglich, Ferienwohnungen. Denkmalschutz: Meist geschützt. Kosten: Sanierung teuer. Wichtig: Spezielle Liebhaberei!", "category": "Denkmalimmobilien", "subcategory": "Wassermühle"},
    {"title": "Burgen und Schlösser: Instandhaltung", "content": "Burgen/Schlösser: Extrem hohe Unterhaltskosten (100.000-500.000€ p.a.). Nutzung: Hotel, Museum, Events. Förderung: Deutsche Stiftung Denkmalschutz. Wichtig: Finanzielle Belastung!", "category": "Denkmalimmobilien", "subcategory": "Burg"},
    {"title": "Fabrikhallen: Loft-Umbauten", "content": "Fabrik-Umnutzung: Zu Lofts, Ateliers, Galerien. Vorteile: Hohe Räume, Industriecharme. Herausforderung: Schallschutz, Wärmedämmung. Wichtig: Hipster-Trend!", "category": "Sonderimmobilien", "subcategory": "Fabrik"},
    {"title": "Bahnhöfe: Revitalisierung", "content": "Bahnhofs-Umnutzung: Zu Wohnungen, Büros, Gastronomie. Eigentümer: Deutsche Bahn. Denkmalschutz: Oft geschützt. Markt: Wachsend (Stilllegungen). Wichtig: Infrastruktur vor Ort!", "category": "Sonderimmobilien", "subcategory": "Bahnhof"},
    {"title": "Kasernen: Konversion", "content": "Kasernen-Konversion: Zu Wohnquartieren nach Bundeswehr-Abzug. Städtebau: Komplette Quartiere neu entwickelt. Herausforderung: Altlasten, Erschließung. Wichtig: Großprojekte!", "category": "Sonderimmobilien", "subcategory": "Kaserne"},
    {"title": "Flughafen-Konversion: Tempelhof", "content": "Flughafen-Konversion: Beispiel Tempelhof Berlin. Nutzung: Park, Events, teilweise Bebauung. Herausforderung: Riesen-Areale (300+ ha). Wichtig: Langfristige Stadtentwicklung!", "category": "Sonderimmobilien", "subcategory": "Flughafen"},
    {"title": "U-Boot-Bunker: Kiel, Hamburg", "content": "U-Boot-Bunker: Massive Beton-Bauwerke, denkmalgeschützt. Nutzung: Kultur, Gastronomie, Wohnen. Herausforderung: Wenig Licht, Fensteröffnungen aufwändig. Wichtig: Einzigartige Projekte!", "category": "Sonderimmobilien", "subcategory": "Bunker"},
    {"title": "Klöster: Säkularisierung Nutzung", "content": "Kloster-Umnutzung: Zu Hotels, Tagungszentren, Wohnungen. Denkmalschutz: Streng. Atmosphäre: Besonders. Nutzung: Oft Kirche behält Teilrechte. Wichtig: Spiritueller Ort!", "category": "Denkmalimmobilien", "subcategory": "Kloster"},
]
documents.extend(denkmal)

# Spezielle Nutzungsformen (15 Docs)
nutzung = [
    {"title": "Sozialimmobilien: Rendite-Risiko", "content": "Sozialimmobilien: Pflegeheime, Kitas, betreutes Wohnen. Rendite: 4-6%, stabil. Risiko: Regulierung, Betreiber-Abhängigkeit. Wichtig: Demografischer Wandel positiv!", "category": "Spezialnutzungen", "subcategory": "Sozialimmobilien"},
    {"title": "Studentenwohnheime: Mikro-Apartments", "content": "Studentenwohnheime: Kleine Apartments (18-25m²), All-Inclusive. Rendite: 5-7%. Standort: Uni-Nähe essentiell. Risiko: Studentenzahl-Entwicklung. Wichtig: Hohe Nachfrage!", "category": "Spezialnutzungen", "subcategory": "Studentenwohnen"},
    {"title": "Serviced Apartments: Business", "content": "Serviced Apartments: Möbliert, Services (Reinigung, Rezeption). Zielgruppe: Geschäftsreisende, Expats. Rendite: 5-8%. Risiko: Hotelsteuer, Konkurrenzdruck. Wichtig: Flexible Alternative zu Hotels!", "category": "Spezialnutzungen", "subcategory": "Serviced Apartments"},
    {"title": "Boarding Houses: Langzeit-Miete", "content": "Boarding House: Möblierte Apartments für 1-12 Monate. Zielgruppe: Projektarbeiter, Interimsmanager. Rendite: 6-9%. Wichtig: Zwischen Hotel und Wohnung!", "category": "Spezialnutzungen", "subcategory": "Boarding House"},
    {"title": "Co-Living: Gemeinschaftswohnen", "content": "Co-Living: Private Zimmer + Gemeinschaftsflächen (Küche, Wohnzimmer). Zielgruppe: Junge Berufstätige, Singles. Rendite: 7-10%. Wichtig: Sozialer Trend!", "category": "Spezialnutzungen", "subcategory": "Co-Living"},
    {"title": "Tiny Houses: Bewegung", "content": "Tiny Houses: <50m² Wohnfläche, mobil oder fix. Rechtslage: Baurechtlich komplex (Wohnwagen vs. Gebäude). Standort: Spezielle Tiny-House-Siedlungen. Wichtig: Minimalismus-Trend!", "category": "Spezialnutzungen", "subcategory": "Tiny House"},
    {"title": "Container-Wohnen: Modulbau", "content": "Container-Wohnen: Günstig, schnell errichtet. Nutzung: Studentenwohnheime, Flüchtlingsunterkünfte. Lebensdauer: 10-25 Jahre. Wichtig: Temporäre Lösung!", "category": "Spezialnutzungen", "subcategory": "Container"},
    {"title": "Hausboote: Rechtslage", "content": "Hausboot: Wasserrecht-Genehmigung erforderlich. Liegeplatz: Oft knapp, teuer. Finanzierung: Schwierig (keine Grundschuld). Wichtig: Spezielle Lebensform!", "category": "Spezialnutzungen", "subcategory": "Hausboot"},
    {"title": "Baumhäuser: Genehmigung", "content": "Baumhaus: Baugenehmi gungspflichtig wenn >Gartenhäuschen-Größe. Sicherheit: Statik, Baumsicherheit. Nutzung: Freizeit, Ferienwohnung. Wichtig: Naturverbundenheit!", "category": "Spezialnutzungen", "subcategory": "Baumhaus"},
    {"title": "Erdhäuser: Energieeffizienz", "content": "Erdhaus: Teilweise/vollständig in Erde integriert. Vorteil: Extreme Energieeffizienz (konstante Temperatur). Nachteil: Wenig Licht, Feuchtigkeit. Wichtig: Ökologisches Bauen!", "category": "Spezialnutzungen", "subcategory": "Erdhaus"},
    {"title": "Strohballenhäuser: Nachhaltigkeit", "content": "Strohballenhaus: Stroh als Dämmung/Wandmaterial. Vorteil: Nachwachsend, CO2-speichernd. Nachteil: Brandschutz kritisch, Finanzierung schwer. Wichtig: Ökologisch wertvoll!", "category": "Spezialnutzungen", "subcategory": "Strohballenhaus"},
    {"title": "Passivhäuser: Standard", "content": "Passivhaus: Heizwärmebedarf <15 kWh/(m²a). Technik: Lüftung mit Wärmerückgewinnung, Dreifachverglasung. Mehrkosten: 5-10% vs. Standard. Wichtig: Höchste Energieeffizienz!", "category": "Spezialnutzungen", "subcategory": "Passivhaus"},
    {"title": "Null-Energie-Häuser: Autarkie", "content": "Null-Energie-Haus: Jahresbilanz Energie = 0 (PV-Anlage + Wärmepumpe). Plus-Energie: Überschuss ins Netz. Kosten: 10-15% Mehrkosten. Wichtig: Energieautonomie!", "category": "Spezialnutzungen", "subcategory": "Null-Energie-Haus"},
    {"title": "Fertighäuser: Industrielle Fertigung", "content": "Fertighaus: Vorfertigung in Fabrik, schneller Aufbau. Vorteil: Zeitersparnis (3-6 Monate), Festpreis. Nachteil: Wertentwicklung oft schlechter als Massivhaus. Wichtig: Marktanteil 20%!", "category": "Spezialnutzungen", "subcategory": "Fertighaus"},
    {"title": "Modulhäuser: Flexibilität", "content": "Modulhaus: Einzelne Module kombinierbar, erweiterbar. Vorteil: Flexibilität, Mobilität. Nutzung: Temporäre Wohnlösungen, Kitas, Schulen. Wichtig: Wachsender Markt!", "category": "Spezialnutzungen", "subcategory": "Modulhaus"},
]
documents.extend(nutzung)

# Internationale & spezielle Märkte (15 Docs)
intl = [
    {"title": "Auslandsimmobilien: Spanien", "content": "Spanien: Beliebtes Ferienwohnungs-Ziel für Deutsche. Kosten: Grunderwerbsteuer 8-11%, Notar. Risiko: Währung, Rechtssystem. Wichtig: Vor-Ort-Anwalt!", "category": "Auslandsimmobilien", "subcategory": "Spanien"},
    {"title": "Auslandsimmobilien: Mallorca spezial", "content": "Mallorca: Sehr hohe Preise (Palma 5.000-10.000€/m²). Vermietung: Touristisch lukrativ. Regulierung: Verschärft (Airbnb-Limits). Wichtig: Hotspot für Deutsche!", "category": "Auslandsimmobilien", "subcategory": "Mallorca"},
    {"title": "Auslandsimmobilien: Türkei", "content": "Türkei: Günstige Preise, aber politisches Risiko. Währung: Lira-Schwäche Vorteil für EUR-Käufer. Rechtssicherheit: Eingeschränkt. Wichtig: Hochrisiko-Investment!", "category": "Auslandsimmobilien", "subcategory": "Türkei"},
    {"title": "Auslandsimmobilien: USA Florida", "content": "Florida: Ferienwohnungen, Altersruhesitz. Steuern: Property Tax 1-2% p.a. Hurrikan: Versicherung teuer. Wichtig: Sunshine State!", "category": "Auslandsimmobilien", "subcategory": "USA"},
    {"title": "Auslandsimmobilien: Dubai", "content": "Dubai: Luxusimmobilien, steuerfrei. Eigentumsrecht: Nur in Freehold-Zonen für Ausländer. Markt: Volatil (Überangebot). Wichtig: Spekulative Investition!", "category": "Auslandsimmobilien", "subcategory": "Dubai"},
    {"title": "Auslandsimmobilien: Portugal", "content": "Portugal: Goldenes Visum-Programm (350.000€ Investment). Steuer: NHR-Status (10 Jahre Steuervorteil). Standort: Lissabon, Algarve. Wichtig: Aufstrebendes Ziel!", "category": "Auslandsimmobilien", "subcategory": "Portugal"},
    {"title": "Auslandsimmobilien: Österreich", "content": "Österreich: Ähnliches Rechtssystem wie D. Grunderwerbsteuer: 3,5%. Eigentumsrechte: Eingeschränkt für Nicht-Österreicher (Bundesländer). Wichtig: Ski-Resorts beliebt!", "category": "Auslandsimmobilien", "subcategory": "Österreich"},
    {"title": "Auslandsimmobilien: Schweiz", "content": "Schweiz: Sehr hohe Preise, strenge Beschränkungen für Ausländer (Lex Koller). Ferienimmobilien: Kontingente. Wichtig: Schwierig für Nicht-Schweizer!", "category": "Auslandsimmobilien", "subcategory": "Schweiz"},
    {"title": "Auslandsimmobilien: Italien", "content": "Italien: 1€-Häuser-Programme in Dörfern (Renovierungspflicht). Toskana: Teuer. Bürokratie: Komplex. Wichtig: Lebensqualität-Investment!", "category": "Auslandsimmobilien", "subcategory": "Italien"},
    {"title": "Auslandsimmobilien: Frankreich", "content": "Frankreich: Côte d'Azur teuer, Countryside günstiger. Steuern: Grundsteuer + Wohnsteuer. Erbrecht: Pflichtteil-Regelungen beachten. Wichtig: Notaire nutzen!", "category": "Auslandsimmobilien", "subcategory": "Frankreich"},
    {"title": "Auslandsimmobilien: Kroatien", "content": "Kroatien: EU-Mitglied, Adriaküste beliebt. Preise: Moderat (2.000-5.000€/m² Küste). Vermietung: Tourismus wachsend. Wichtig: Emerging Market!", "category": "Auslandsimmobilien", "subcategory": "Kroatien"},
    {"title": "Auslandsimmobilien: Griechenland", "content": "Griechenland: Inseln beliebt, Preise nach Krise gestiegen. Golden Visa: 250.000€ Investment. Wirtschaft: Risiko beachten. Wichtig: Mittelmeer-Traum!", "category": "Auslandsimmobilien", "subcategory": "Griechenland"},
    {"title": "Auslandsimmobilien: Thailand", "content": "Thailand: Eigentum für Ausländer nur Condos (max. 49% im Gebäude). Land: Nicht für Ausländer. Leasehold: 30+30+30 Jahre üblich. Wichtig: Alterswohnsitz-Ziel!", "category": "Auslandsimmobilien", "subcategory": "Thailand"},
    {"title": "Auslandsimmobilien: Karibik", "content": "Karibik: Citizenship by Investment (St. Kitts, Dominica). Steuern: Oft steuerfrei. Hurrikan: Hohes Risiko. Wichtig: Exotisches Investment!", "category": "Auslandsimmobilien", "subcategory": "Karibik"},
    {"title": "Auslandsimmobilien: Währungsrisiko", "content": "Währungsrisiko: EUR/USD, EUR/GBP, EUR/CHF. Absicherung: Währungs-Hedging, Finanzierung in Landeswährung. Wichtig: Kann Rendite deutlich schmälern!", "category": "Auslandsimmobilien", "subcategory": "Währungsrisiko"},
]
documents.extend(intl)

# Zukunftstrends & Innovationen (20 Docs)
zukunft = [
    {"title": "Smart Cities: Konzepte", "content": "Smart Cities: Vernetzte Infrastruktur, IoT, Datenanalyse. Beispiele: Songdo (Korea), Masdar (UAE). Ziel: Effizienz, Nachhaltigkeit, Lebensqualität. Wichtig: Zukunft des Städtebaus!", "category": "Zukunftstrends", "subcategory": "Smart Cities"},
    {"title": "Vertical Farming: Urbane Landwirtschaft", "content": "Vertical Farming: Landwirtschaft in Hochhäusern. Vorteil: Ganzjährige Produktion, kein Pestizid. Herausforderung: Hoher Energieverbrauch. Wichtig: Stadtnahe Versorgung!", "category": "Zukunftstrends", "subcategory": "Vertical Farming"},
    {"title": "3D-Druck Häuser: Additive Fertigung", "content": "3D-Druck-Häuser: Schicht-für-Schicht Beton-Druck. Vorteil: Schnell (1-2 Wochen), günstig. Nachteil: Baugenehmigung unklar. Wichtig: Revolution des Bauens!", "category": "Zukunftstrends", "subcategory": "3D-Druck"},
    {"title": "Modulares Bauen: Skalierbarkeit", "content": "Modulares Bauen: Vorgefertigte Raummodule. Vorteil: Schnell, flexibel erweiterbar/umziehbar. Nutzung: Hotels, Studentenwohnheime. Wichtig: Industrialisierung Bau!", "category": "Zukunftstrends", "subcategory": "Modulbau"},
    {"title": "Holz-Hochhäuser: Nachhaltigkeit", "content": "Holz-Hochhäuser: Brettsperrholz (CLT) bis 80m Höhe. Vorteil: CO2-Speicherung, nachwachsend. Beispiel: HoHo Wien (84m). Wichtig: Renaissance des Holzbaus!", "category": "Zukunftstrends", "subcategory": "Holzbau"},
    {"title": "Begrünte Fassaden: Urban Green", "content": "Fassadenbegrünung: Pflanzen an Außenwänden. Vorteil: Kühlung, Luftreinigung, Biodiversität. Kosten: Bewässerung, Pflege. Wichtig: Grüne Architektur-Trend!", "category": "Zukunftstrends", "subcategory": "Fassadenbegrünung"},
    {"title": "Gründächer: Ökologischer Nutzen", "content": "Gründach: Extensive (Sedum) oder intensive (Dachgarten) Begrünung. Vorteil: Regenwasser-Rückhalt, Dämmung, Lebensraum. Förderung: Viele Kommunen. Wichtig: Pflicht in einigen Städten!", "category": "Zukunftstrends", "subcategory": "Gründach"},
    {"title": "Wasserstoff-Heizung: Alternative", "content": "Wasserstoff-Heizung: H2 als Energieträger. Status: Noch in Entwicklung, teuer. Vorteil: Klimaneutral wenn grüner H2. Wichtig: Langfristige Perspektive!", "category": "Zukunftstrends", "subcategory": "Wasserstoff"},
    {"title": "Geothermie: Erdwärme", "content": "Geothermie: Wärme aus Erdinneren. Tiefe: 1-4km für Heizung. Vorteil: Konstante Temperatur, klimaneutral. Kosten: Bohrung 500.000-2 Mio€. Wichtig: Standortabhängig!", "category": "Zukunftstrends", "subcategory": "Geothermie"},
    {"title": "Quartierspeicher: Energie-Speicherung", "content": "Quartierspeicher: Batterie für ganzes Wohnquartier. Nutzen: Solarstrom-Speicherung, Netzstabilität. Status: Pilotprojekte. Wichtig: Dezentrale Energieversorgung!", "category": "Zukunftstrends", "subcategory": "Energiespeicher"},
    {"title": "Blockchain Grundbuch: Digitalisierung", "content": "Blockchain-Grundbuch: Fälschungssicher, transparent, schnell. Status: Pilotprojekte (Schweden, Dubai). Deutschland: Noch Zukunft. Wichtig: Revolution Eigentumsübertragung!", "category": "Zukunftstrends", "subcategory": "Blockchain"},
    {"title": "Virtuelle Besichtigung: VR/AR", "content": "VR-Besichtigung: Immobilie virtuell begehen. AR: Möblierung einblenden. Vorteil: Zeitersparnis, internationale Käufer. Wichtig: Standard in Vermarktung!", "category": "Zukunftstrends", "subcategory": "VR/AR"},
    {"title": "PropTech: Digitale Innovation", "content": "PropTech: Technologie für Immobilienwirtschaft. Bereiche: Vermarktung, Verwaltung, Finanzierung, Bewertung. Startups: Immoscout, Homeday, PriceHubble. Wichtig: Digitalisierung der Branche!", "category": "Zukunftstrends", "subcategory": "PropTech"},
    {"title": "KI-Bewertung: Automatisierung", "content": "KI-Immobilienbewertung: Algorithmen analysieren Daten. Genauigkeit: ±10-15%. Vorteil: Schnell, objektiv. Nachteil: Besonderheiten schwer erfassbar. Wichtig: Tool, nicht Ersatz!", "category": "Zukunftstrends", "subcategory": "KI-Bewertung"},
    {"title": "Smart Locks: Digitaler Zugang", "content": "Smart Locks: Keyless Entry (Smartphone, Code, Fingerabdruck). Vorteil: Keine Schlüssel, Fernzugriff. Nutzung: Airbnb, Kurzzeitmiete. Wichtig: Sicherheitsaspekte beachten!", "category": "Zukunftstrends", "subcategory": "Smart Lock"},
    {"title": "Drohnen-Inspektion: Dach/Fassade", "content": "Drohnen-Inspektion: Dach, Fassade ohne Gerüst prüfen. Vorteil: Kostengünstig, schnell, sicher. Genehmigung: Teilweise erforderlich. Wichtig: Tool für Gutachter!", "category": "Zukunftstrends", "subcategory": "Drohnen"},
    {"title": "BIM: Building Information Modeling", "content": "BIM: 3D-Gebäudemodell mit allen Daten. Nutzen: Planung, Ausführung, Betrieb. Pflicht: Öffentliche Bauvorhaben. Wichtig: Standard der Zukunft!", "category": "Zukunftstrends", "subcategory": "BIM"},
    {"title": "Digital Twin: Gebäude-Zwilling", "content": "Digital Twin: Digitale Kopie des Gebäudes mit Echtzeitdaten. Nutzen: Simulation, Optimierung, Predictive Maintenance. Status: Noch Pionierphase. Wichtig: Zukunft Gebäudemanagement!", "category": "Zukunftstrends", "subcategory": "Digital Twin"},
    {"title": "Robotik: Bau-Automatisierung", "content": "Bau-Robotik: Mauern, Schweißen, 3D-Druck. Vorteil: Präzision, Geschwindigkeit. Status: Erste Piloten. Wichtig: Fachkräftemangel-Lösung!", "category": "Zukunftstrends", "subcategory": "Robotik"},
    {"title": "Cradle-to-Cradle: Kreislaufwirtschaft", "content": "Cradle-to-Cradle Bau: Alle Materialien wiederverwertbar oder biologisch abbaubar. Materialpass: Dokumentation aller Stoffe. Ziel: Zero Waste. Wichtig: Zukunft des nachhaltigen Bauens!", "category": "Zukunftstrends", "subcategory": "Cradle-to-Cradle"},
]
documents.extend(zukunft)

print(f"🚀 BATCH 7: SPEZIELLE IMMOBILIENARTEN & GEWERBE - START")
print(f"📦 {len(documents)} Dokumente werden verarbeitet...")
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
        if i % 10 == 0:
            print(f"✅ {i}/{len(documents)}: {doc['title'][:50]}...")
        
    except Exception as e:
        failed += 1
        print(f"❌ {i}/{len(documents)}: {doc['title'][:50]} - {str(e)[:50]}")

print("\n" + "=" * 60)
print(f"✅ Erfolgreich: {successful}/{len(documents)}")
print(f"❌ Fehlgeschlagen: {failed}")

try:
    count = client.count(collection_name="legal_documents")
    total = count.count
    print(f"\n🎯 GESAMT DOKUMENTE: {total}")
    print(f"📊 Noch {10000 - total} bis zur 10.000!")
    print(f"🔥 Fortschritt: {total/100:.1f}%")
except Exception as e:
    print(f"⚠️  Konnte Gesamtzahl nicht abrufen: {e}")

print("\n🔥 BATCH 7 COMPLETE! 🔥")
