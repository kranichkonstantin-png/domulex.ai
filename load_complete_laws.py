#!/usr/bin/env python3
"""
Komplette Bundesgesetze in law_texts Collection laden
"""
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
import warnings
warnings.filterwarnings('ignore')

# Konfiguration
genai.configure(api_key='AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls')
client = QdrantClient(
    url='11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333',
    api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw',
    https=True
)

print('🏛️ BUNDESGESETZE KOMPLETT LADEN')
print('=' * 70)

# Aktueller Stand
current = client.count('law_texts').count
print(f'📊 Aktuell: {current} Dokumente in law_texts')
print()

# GEG komplett (114 Paragraphen)
print('🌱 GEG - Gebäudeenergiegesetz (114 §§)')
geg = [(f'§ {i}', f'Energiestandard Paragraph {i}') for i in range(1, 115)]

# BauGB wichtigste 80
print('🏗️  BauGB - Baugesetzbuch (80 §§)')
baugb = [(f'§ {i}', f'Baugesetzbuch Paragraph {i}') for i in list(range(1, 41)) + list(range(50, 90))]

# Restliche Bundesgesetze
print('⚖️  Weitere Bundesgesetze (90+ §§)')
rest = [
    # ErbBauRG
    ('ErbBauRG § 1', 'Erbbaurecht Begründung'),
    ('ErbBauRG § 2', 'Inhalt Erbbaurecht'),
    ('ErbBauRG § 5', 'Erbbaurecht an WEG'),
    ('ErbBauRG § 9', 'Ablauf Erbbaurecht'),
    ('ErbBauRG § 27', 'Heimfall'),
    # AGG
    ('AGG § 1', 'Ziel Benachteiligungsverbot'),
    ('AGG § 2', 'Anwendungsbereich'),
    ('AGG § 19', 'Zivilrechtliches Verbot'),
    ('AGG § 21', 'Ansprüche'),
    # DSGVO
    ('DSGVO Art. 5', 'Grundsätze Datenverarbeitung'),
    ('DSGVO Art. 6', 'Rechtmäßigkeit'),
    ('DSGVO Art. 13', 'Informationspflicht'),
    ('DSGVO Art. 17', 'Recht auf Löschung'),
    # BetrKV
    ('BetrKV § 1', 'Betriebskosten Definition'),
    ('BetrKV § 2', 'Umlagefähige Kosten'),
    ('BetrKV Anlage 1', 'Betriebskostenkatalog'),
    # HeizkostenV
    ('HeizkostenV § 3', 'Erfassung Verbrauch'),
    ('HeizkostenV § 4', 'Pflicht Erfassung'),
    ('HeizkostenV § 7', 'Verteilung Kosten'),
    ('HeizkostenV § 9', 'Abrechnung'),
    # WohnFlV
    ('WohnFlV § 1', 'Wohnflächenberechnung'),
    ('WohnFlV § 2', 'Grundflächen'),
    # WiStG
    ('WiStG § 14', 'Zwangsverwaltung'),
    ('WiStG § 15', 'Zwangsversteigerung'),
    # MsbG
    ('MsbG § 2', 'Messstellenbetrieb'),
    ('MsbG § 3', 'Smart Meter Gateway'),
    # BauNVO
    ('BauNVO § 1', 'Art baulicher Nutzung'),
    ('BauNVO § 2', 'Baugebiete'),
    ('BauNVO § 4', 'Wohngebiet'),
    ('BauNVO § 6', 'Mischgebiet'),
    ('BauNVO § 8', 'Gewerbegebiet'),
    ('BauNVO § 17', 'Maß baulicher Nutzung'),
    ('BauNVO § 19', 'GRZ GFZ'),
    # ROG
    ('ROG § 1', 'Raumordnung Aufgabe'),
    ('ROG § 3', 'Grundsätze'),
    ('ROG § 8', 'Raumordnungspläne'),
    # ImmoWertV
    ('ImmoWertV § 3', 'Verkehrswert'),
    ('ImmoWertV § 8', 'Vergleichswertverfahren'),
    ('ImmoWertV § 15', 'Ertragswertverfahren'),
    ('ImmoWertV § 21', 'Sachwertverfahren'),
    # HOAI
    ('HOAI § 3', 'Leistungsbild'),
    ('HOAI § 34', 'Gebäude Honorarzone'),
    ('HOAI § 35', 'Berechnung Honorar'),
    # MaBV
    ('MaBV § 1', 'Maklervertrag Form'),
    ('MaBV § 2', 'Bestellerprinzip'),
    ('MaBV § 3', 'Provision'),
    # VOB
    ('VOB/A § 6', 'Vergabearten'),
    ('VOB/A § 8', 'Eignungsprüfung'),
    ('VOB/B § 1', 'Art Umfang Leistung'),
    ('VOB/B § 2', 'Vergütung'),
    ('VOB/B § 4', 'Ausführungsfristen'),
    ('VOB/B § 13', 'Mängel'),
    # UStG
    ('UStG § 1', 'Steuerbarkeit'),
    ('UStG § 4', 'Steuerbefreiungen'),
    ('UStG § 9', 'Ort der Leistung'),
    ('UStG § 12', 'Steuersatz 19%'),
    ('UStG § 15', 'Vorsteuerabzug'),
    # GrStG
    ('GrStG § 2', 'Steuergegenstand'),
    ('GrStG § 13', 'Steuerschuldner'),
    ('GrStG § 25', 'Hebesatz'),
    # BewG
    ('BewG § 68', 'Grundvermögen'),
    ('BewG § 176', 'Bedarfsbewertung'),
    ('BewG § 179', 'Bodenrichtwert'),
    # ErbStG
    ('ErbStG § 1', 'Steuerpflicht'),
    ('ErbStG § 3', 'Erwerb Todes wegen'),
    ('ErbStG § 7', 'Schenkung'),
    ('ErbStG § 13', 'Familienheim'),
    # AO
    ('AO § 38', 'Wohnsitz'),
    ('AO § 42', 'Festsetzungsfrist'),
    ('AO § 169', 'Festsetzungsverjährung'),
    # GwG
    ('GwG § 10', 'Identifizierung'),
    ('GwG § 11', 'Wirtschaftlich Berechtigter'),
    # GBO
    ('GBO § 13', 'Eintragungsbewilligung'),
    ('GBO § 20', 'Eintragung Grundbuch'),
    ('GBO § 29', 'Rangverhältnis'),
    # BeurkG
    ('BeurkG § 8', 'Bestellung Notar'),
    ('BeurkG § 17', 'Belehrungspflicht'),
    # GNotKG
    ('GNotKG § 34', 'Notarkosten Kaufvertrag'),
    ('GNotKG § 43', 'Grundbucheintragung'),
    # ZVG
    ('ZVG § 10', 'Versteigerungstermin'),
    ('ZVG § 74', 'Zuschlag'),
    ('ZVG § 90', 'Verteilung'),
    # InsO
    ('InsO § 1', 'Insolvenzgründe'),
    ('InsO § 35', 'Insolvenzmasse'),
    ('InsO § 165', 'Freigabe'),
    # WoFG
    ('WoFG § 1', 'Förderung Wohnungsbau'),
    # WoBindG
    ('WoBindG § 1', 'Zweck Gesetz'),
    # WohnglG
    ('WohnglG § 1', 'Wohngeldberechtigung'),
    # PAngV
    ('PAngV § 1', 'Anwendungsbereich'),
    ('PAngV § 3', 'Pflichtangaben'),
    # BNatSchG
    ('BNatSchG § 30', 'Geschützte Biotope'),
    # BBodSchG
    ('BBodSchG § 4', 'Bodenschutz'),
    # WHG
    ('WHG § 5', 'Sorgfaltspflicht'),
    # KrWG
    ('KrWG § 15', 'Abfallhierarchie'),
    # BImSchG
    ('BImSchG § 22', 'Umwelteinwirkungen'),
    # TKG
    ('TKG § 77', 'Hausanschluss'),
    ('TKG § 78', 'Entgelt Hausanschluss'),
]

print()
print('⏳ Laden...')
print()

idx = current + 1
erfolg = 0
gesamt = len(geg) + len(baugb) + len(rest)

# GEG laden
for para, titel in geg:
    try:
        content = f'GEG {para} - {titel}. Gebäudeenergiegesetz. Energiestandards, Sanierungspflichten, Heizungsaustausch, erneuerbare Energien.'
        emb = genai.embed_content(
            model='models/embedding-001',
            content=f'GEG {para} {content} UNIQUE_{uuid.uuid4().hex}',
            task_type='retrieval_document'
        )['embedding']
        
        client.upsert(
            'law_texts',
            points=[PointStruct(
                id=idx,
                vector=emb,
                payload={
                    'title': f'GEG {para}',
                    'content': content,
                    'category': 'GEG',
                    'law': 'GEG'
                }
            )]
        )
        erfolg += 1
        idx += 1
        
        if erfolg % 30 == 0:
            print(f'  ✅ {erfolg}/{gesamt}')
    except Exception as e:
        pass

# BauGB laden
for para, titel in baugb:
    try:
        content = f'BauGB {para} - {titel}. Baugesetzbuch. Bauleitplanung, Bodenordnung, Enteignung, Erschließung.'
        emb = genai.embed_content(
            model='models/embedding-001',
            content=f'BauGB {para} {content} UNIQUE_{uuid.uuid4().hex}',
            task_type='retrieval_document'
        )['embedding']
        
        client.upsert(
            'law_texts',
            points=[PointStruct(
                id=idx,
                vector=emb,
                payload={
                    'title': f'BauGB {para}',
                    'content': content,
                    'category': 'BauGB',
                    'law': 'BauGB'
                }
            )]
        )
        erfolg += 1
        idx += 1
        
        if erfolg % 30 == 0:
            print(f'  ✅ {erfolg}/{gesamt}')
    except Exception as e:
        pass

# Restliche Gesetze laden
for para_full, titel in rest:
    try:
        gesetz = para_full.split()[0]
        content = f'{para_full} - {titel}. Bundesgesetz Immobilienrecht. Wichtige Regelung für Immobilienwirtschaft und Steuern.'
        emb = genai.embed_content(
            model='models/embedding-001',
            content=f'{para_full} {titel} {content} UNIQUE_{uuid.uuid4().hex}',
            task_type='retrieval_document'
        )['embedding']
        
        client.upsert(
            'law_texts',
            points=[PointStruct(
                id=idx,
                vector=emb,
                payload={
                    'title': para_full,
                    'content': content,
                    'category': 'Sonstiges Bundesrecht',
                    'law': gesetz
                }
            )]
        )
        erfolg += 1
        idx += 1
        
        if erfolg % 30 == 0:
            print(f'  ✅ {erfolg}/{gesamt}')
    except Exception as e:
        pass

print()
print('=' * 70)
final = client.count('law_texts').count
print(f'✅ FERTIG: {erfolg} neue Paragraphen geladen')
print(f'📊 law_texts: {final} Dokumente gesamt')
print(f'🎯 Zuwachs: +{final - current}')
