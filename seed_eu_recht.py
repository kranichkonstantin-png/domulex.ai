#!/usr/bin/env python3
"""EU-Recht und Richtlinien"""

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import uuid

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
client = QdrantClient(host=os.environ['QDRANT_HOST'], port=6333, api_key=os.environ['QDRANT_API_KEY'], https=True)

def embed(text):
    return genai.embed_content(model='models/text-embedding-004', content=text[:8000])['embedding']

print('🚀 EU-RECHT SEEDING')

eu_docs = [
    # DSGVO
    {'title': 'DSGVO Art. 6 - Rechtmäßigkeit der Verarbeitung', 'content': 'Die Verarbeitung ist nur rechtmäßig, wenn mindestens eine der nachstehenden Bedingungen erfüllt ist: Die betroffene Person hat ihre Einwilligung zu der Verarbeitung gegeben; die Verarbeitung ist für die Erfüllung eines Vertrags erforderlich; die Verarbeitung ist zur Erfüllung einer rechtlichen Verpflichtung erforderlich; die Verarbeitung ist erforderlich, um lebenswichtige Interessen zu schützen; die Verarbeitung ist für die Wahrnehmung einer Aufgabe im öffentlichen Interesse erforderlich; die Verarbeitung ist zur Wahrung der berechtigten Interessen des Verantwortlichen erforderlich.', 'source': 'DSGVO', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    {'title': 'DSGVO Art. 7 - Bedingungen für die Einwilligung', 'content': 'Beruht die Verarbeitung auf einer Einwilligung, muss der Verantwortliche nachweisen können, dass die betroffene Person in die Verarbeitung ihrer personenbezogenen Daten eingewilligt hat. Die Einwilligung muss freiwillig, für den bestimmten Fall, in informierter Weise und unmissverständlich abgegeben werden. Die betroffene Person hat das Recht, ihre Einwilligung jederzeit zu widerrufen.', 'source': 'DSGVO', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    {'title': 'DSGVO Art. 12 - Transparenz und Modalitäten', 'content': 'Der Verantwortliche trifft geeignete Maßnahmen, um der betroffenen Person alle Informationen und Mitteilungen in präziser, transparenter, verständlicher und leicht zugänglicher Form in einer klaren und einfachen Sprache zu übermitteln. Die Informationen werden schriftlich oder in anderer Form, gegebenenfalls elektronisch, bereitgestellt.', 'source': 'DSGVO', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    {'title': 'DSGVO Art. 15 - Auskunftsrecht', 'content': 'Die betroffene Person hat das Recht, von dem Verantwortlichen eine Bestätigung darüber zu verlangen, ob sie betreffende personenbezogene Daten verarbeitet werden. Ist dies der Fall, so hat sie ein Recht auf Auskunft über diese personenbezogenen Daten und auf die in den Absätzen genannten Informationen.', 'source': 'DSGVO', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    {'title': 'DSGVO Art. 17 - Recht auf Löschung', 'content': 'Die betroffene Person hat das Recht, von dem Verantwortlichen zu verlangen, dass sie betreffende personenbezogene Daten unverzüglich gelöscht werden, und der Verantwortliche ist verpflichtet, personenbezogene Daten unverzüglich zu löschen, sofern einer der Gründe zutrifft: Die Daten sind nicht mehr notwendig; die betroffene Person widerruft ihre Einwilligung; die Daten wurden unrechtmäßig verarbeitet.', 'source': 'DSGVO', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    
    # EU-Richtlinien Immobilien
    {'title': 'EU-Richtlinie 2014/17/EU - Wohnimmobilienkreditrichtlinie', 'content': 'Die Richtlinie über Wohnimmobilienkreditverträge für Verbraucher regelt die Vergabe von Krediten für Wohnimmobilien. Sie enthält Bestimmungen über Kreditwürdigkeitsprüfung, Beratungspflichten, vorzeitige Rückzahlung und Standards für Immobilienbewertung. Kreditgeber müssen die Kreditwürdigkeit sorgfältig prüfen und dürfen Kredite nur vergeben, wenn der Verbraucher sie zurückzahlen kann.', 'source': 'EU-Richtlinie 2014/17/EU', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Richtlinie 2018/844/EU - Gesamtenergieeffizienz Gebäude', 'content': 'Die überarbeitete Richtlinie über die Gesamtenergieeffizienz von Gebäuden stärkt die Renovierungsstrategien und die E-Mobilität. Alle neuen Gebäude müssen ab 2021 Niedrigstenergiegebäude sein. Mitgliedstaaten müssen langfristige Renovierungsstrategien entwickeln. Bei größeren Renovierungen sind Ladestationen für Elektrofahrzeuge vorzusehen.', 'source': 'EU-Richtlinie 2018/844/EU', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Verordnung 305/2011/EU - Bauproduktenverordnung', 'content': 'Die Bauproduktenverordnung legt harmonisierte Bedingungen für die Vermarktung von Bauprodukten fest. Bauprodukte müssen eine CE-Kennzeichnung tragen und den grundlegenden Anforderungen an Bauwerke genügen: mechanische Festigkeit, Brandschutz, Hygiene, Sicherheit, Schallschutz, Energieeinsparung und Nachhaltigkeit.', 'source': 'EU-VO 305/2011', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    
    # EU-Grundfreiheiten
    {'title': 'Art. 21 AEUV - Freizügigkeit', 'content': 'Jeder Unionsbürger hat das Recht, sich im Hoheitsgebiet der Mitgliedstaaten vorbehaltlich der in den Verträgen und in den Durchführungsvorschriften vorgesehenen Beschränkungen und Bedingungen frei zu bewegen und aufzuhalten. Das Europäische Parlament und der Rat können Vorschriften erlassen, um die Ausübung der Rechte nach Absatz 1 zu erleichtern.', 'source': 'AEUV', 'category': 'EU-Recht', 'doc_type': 'Vertrag'},
    {'title': 'Art. 49 AEUV - Niederlassungsfreiheit', 'content': 'Die Beschränkungen der freien Niederlassung von Staatsangehörigen eines Mitgliedstaats im Hoheitsgebiet eines anderen Mitgliedstaats sind verboten. Dies gilt auch für die Beschränkungen der Errichtung von Agenturen, Zweigniederlassungen oder Tochtergesellschaften durch Angehörige eines Mitgliedstaats, die im Hoheitsgebiet eines anderen Mitgliedstaats ansässig sind.', 'source': 'AEUV', 'category': 'EU-Recht', 'doc_type': 'Vertrag'},
    {'title': 'Art. 56 AEUV - Dienstleistungsfreiheit', 'content': 'Die Beschränkungen des freien Dienstleistungsverkehrs innerhalb der Union für Angehörige der Mitgliedstaaten, die in einem anderen Mitgliedstaat als demjenigen des Leistungsempfängers ansässig sind, sind verboten. Das Europäische Parlament und der Rat können mit Richtlinien die Liberalisierung bestimmter Dienstleistungen regeln.', 'source': 'AEUV', 'category': 'EU-Recht', 'doc_type': 'Vertrag'},
    
    # EU-Verbraucherrecht
    {'title': 'EU-Richtlinie 2011/83/EU - Verbraucherrechte', 'content': 'Die Verbraucherrechterichtlinie regelt Verträge zwischen Unternehmern und Verbrauchern. Sie enthält Informationspflichten vor Vertragsschluss, Widerrufsrecht bei Fernabsatz und außerhalb von Geschäftsräumen geschlossenen Verträgen. Das Widerrufsrecht beträgt 14 Tage. Bei Immobilienverträgen gelten besondere Regelungen.', 'source': 'EU-Richtlinie 2011/83/EU', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Richtlinie 93/13/EWG - Missbräuchliche Klauseln', 'content': 'Die Richtlinie über missbräuchliche Klauseln in Verbraucherverträgen schützt Verbraucher vor unfairen Vertragsbestimmungen. Missbräuchliche Klauseln sind unwirksam. Eine Klausel ist missbräuchlich, wenn sie ein erhebliches Ungleichgewicht der Vertragsrechte zum Nachteil des Verbrauchers verursacht.', 'source': 'EU-Richtlinie 93/13/EWG', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    
    # Weitere EU-Gesetze
    {'title': 'EU-Geldwäscherichtlinie (5. GWR)', 'content': 'Die 5. EU-Geldwäscherichtlinie erweitert die Sorgfaltspflichten und Transparenzanforderungen. Immobilienmakler, Notare und Rechtsanwälte sind verpflichtete Personen und müssen Verdachtsmeldungen abgeben. Beneficial Owner von Immobiliengesellschaften müssen in öffentlichen Registern erfasst werden. Kryptowährungen werden in den Anwendungsbereich einbezogen.', 'source': 'EU-Richtlinie 2018/843/EU', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Taxonomie-Verordnung', 'content': 'Die EU-Taxonomie-Verordnung etabliert ein Klassifikationssystem für ökologisch nachhaltige Wirtschaftstätigkeiten. Immobilieninvestments müssen Nachhaltigkeitskriterien erfüllen. Wesentliche Beiträge zum Klimaschutz, zur Klimaanpassung, zum Schutz von Wasser und Meeresressourcen, zur Kreislaufwirtschaft, zur Vermeidung von Umweltverschmutzung und zum Schutz von Ökosystemen sind erforderlich.', 'source': 'EU-VO 2020/852', 'category': 'EU-Recht', 'doc_type': 'Verordnung'},
    {'title': 'EU-Richtlinie 2009/103/EG - KH-Versicherung', 'content': 'Die Kraftfahrzeug-Haftpflichtversicherungsrichtlinie regelt die obligatorische KH-Versicherung in der EU. Jedes Kraftfahrzeug muss versichert sein. Die Mindestdeckungssummen betragen 1,22 Mio. EUR für Personenschäden je Schadenfall und 1,22 Mio. EUR für Sachschäden je Schadenfall. Bei Immobilienschäden gelten besondere Regelungen.', 'source': 'EU-Richtlinie 2009/103/EG', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Dienstleistungsrichtlinie 2006/123/EG', 'content': 'Die Dienstleistungsrichtlinie schafft einen Rechtsrahmen für die Niederlas­sungs­freiheit von Dienstleistern und den freien Dienstleistungsverkehr. Makler, Architekten und andere Immobiliendienstleister profitieren von vereinfachten Verwaltungsverfahren und gegenseitiger Anerkennung von Qualifikationen. Ungerechtfertigte Beschränkungen sind verboten.', 'source': 'EU-Richtlinie 2006/123/EG', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Richtlinie 2014/65/EU - MiFID II', 'content': 'Die Finanzmarktrichtlinie MiFID II regelt auch Immobilienanlageprodukte. Anlageberater müssen über ausreichende Kenntnisse verfügen und Interessenkonflikte offenlegen. Bei der Beratung über Immobilienfonds gelten verschärfte Informationspflichten. Geeignetheits- und Angemessenheitsprüfungen sind durchzuführen.', 'source': 'EU-Richtlinie 2014/65/EU', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Richtlinie 2014/24/EU - Vergaberecht', 'content': 'Die Vergaberichtlinie regelt die Auftragsvergabe öffentlicher Auftraggeber. Bau-, Liefer- und Dienstleistungsaufträge müssen EU-weit ausgeschrieben werden ab bestimmten Schwellenwerten. Für Bauaufträge liegt der Schwellenwert bei 5,35 Mio. EUR. Nachhaltigkeits- und Sozialkriterien können berücksichtigt werden.', 'source': 'EU-Richtlinie 2014/24/EU', 'category': 'EU-Recht', 'doc_type': 'Richtlinie'},
    {'title': 'EU-Klima- und Energiepaket 2030', 'content': 'Das EU-Klima- und Energiepaket setzt verbindliche Ziele: 55% weniger Treibhausgasemissionen bis 2030, 32% erneuerbare Energien, 32,5% Energieeffizienz. Für Gebäude bedeutet dies strengere Energiestandards, Sanierungspflichten und Förderung erneuerbarer Energien. Die Renovation Wave Strategy zielt auf eine Verdopplung der Sanierungsrate ab.', 'source': 'EU-Kommission', 'category': 'EU-Recht', 'doc_type': 'Strategie'},
    
    # EuGH Rechtsprechung
    {'title': 'EuGH C-415/11 Aziz - Missbräuchliche Klauseln', 'content': 'Der EuGH entschied, dass nationale Gerichte missbräuchliche Klauseln in Verbraucherverträgen von Amts wegen prüfen müssen, auch wenn der Verbraucher dies nicht beantragt. Dies gilt auch für Zwangsvollstreckungsverfahren bei Immobilienkrediten. Verbraucher müssen vor missbräuchlichen Klauseln geschützt werden.', 'source': 'EuGH', 'category': 'EU-Rechtsprechung', 'doc_type': 'Urteil'},
    {'title': 'EuGH C-34/13 Kušionová - Verhältnismäßigkeit', 'content': 'Der EuGH betonte das Verhältnismäßigkeitsprinzip bei Zwangsvollstreckungen in Wohnimmobilien. Nationale Gerichte müssen prüfen, ob der Verlust der Wohnung eine unverhältnismäßige Folge darstellt. Das Recht auf Wohnung aus der EU-Grundrechtecharta ist zu beachten.', 'source': 'EuGH', 'category': 'EU-Rechtsprechung', 'doc_type': 'Urteil'},
    {'title': 'EuGH C-169/14 Sánchez Morcillo - Berufungsverfahren', 'content': 'Der EuGH entschied zur Vereinbarkeit nationaler Verfahrensregeln mit der Verbraucherrechterichtlinie. Beschränkungen des Berufungsrechts bei Verbraucherkreditverträgen können gegen EU-Recht verstoßen, wenn sie den effektiven Rechtsschutz beeinträchtigen.', 'source': 'EuGH', 'category': 'EU-Rechtsprechung', 'doc_type': 'Urteil'},
]

print(f'📤 Uploading {len(eu_docs)} Dokumente...')
points = []
for i, doc in enumerate(eu_docs):
    vector = embed(doc['content'])
    points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=doc))
    if (i+1) % 10 == 0:
        print(f'  📝 {i+1}/{len(eu_docs)} embedded...')

for i in range(0, len(points), 25):
    batch = points[i:i+25]
    client.upsert(collection_name='legal_documents', points=batch)
    print(f'  ✅ Batch {i//25+1}: {len(batch)} docs')

info = client.get_collection('legal_documents')
print(f'📊 Gesamt: {info.points_count} Dokumente')
