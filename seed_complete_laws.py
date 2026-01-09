#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seed ECHTE Gesetzestexte - Paragraph für Paragraph"""

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import time

genai.configure(api_key='AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls')
client = QdrantClient(
    url='11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333',
    api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw',
    https=True
)

print("🏛️ SEED COMPLETE GERMAN REAL ESTATE LAW")
print("=" * 70)

# WICHTIGSTE GESETZE mit echten Paragraphen (Auszug)
LAWS = {
    "BGB": {
        # Mietrecht (nur Auswahl, vollständig wären §§ 535-577a)
        "§ 535 BGB": "Mietvertrag - Inhalt und Hauptpflichten. (1) Durch den Mietvertrag wird der Vermieter verpflichtet, dem Mieter den Gebrauch der Mietsache während der Mietzeit zu gewähren. Der Vermieter hat die Mietsache dem Mieter in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu überlassen und sie während der Mietzeit in diesem Zustand zu erhalten. Er hat die auf der Mietsache ruhenden Lasten zu tragen. (2) Der Mieter ist verpflichtet, dem Vermieter die vereinbarte Miete zu entrichten.",
        
        "§ 536 BGB": "Mietminderung bei Sach- und Rechtsmängeln. (1) Hat die Mietsache zur Zeit der Überlassung an den Mieter einen Mangel, der ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufhebt, oder entsteht während der Mietzeit ein solcher Mangel, so ist der Mieter für die Zeit, in der die Tauglichkeit aufgehoben ist, von der Entrichtung der Miete befreit. Für die Zeit, während der die Tauglichkeit gemindert ist, hat er nur eine angemessen herabgesetzte Miete zu entrichten.",
        
        "§ 536a BGB": "Schadensersatzanspruch des Mieters wegen eines Mangels. (1) Verletzt der Vermieter eine ihm gegenüber dem Mieter obliegende Pflicht, hat der Mieter Anspruch auf Schadensersatz oder Aufwendungsersatz nach den Vorschriften der §§ 280, 281, 283 und 284. Dies gilt auch bei einer Pflichtverletzung nach § 536 Abs. 4.",
        
        "§ 537 BGB": "Selbstbeseitigungsrecht des Mieters. (1) Der Mieter kann einen Mangel der Mietsache selbst beseitigen und Ersatz der erforderlichen Aufwendungen verlangen, wenn 1. der Vermieter mit der Beseitigung des Mangels in Verzug ist, oder 2. die unverzügliche Beseitigung des Mangels zur Erhaltung oder Wiederherstellung des vertragsgemäßen Gebrauchs notwendig ist.",
        
        "§ 538 BGB": "Kenntnis des Mieters vom Mangel bei Vertragsschluss. Kannte der Mieter bei Vertragsschluss den Mangel der Mietsache, so stehen ihm die Rechte aus den §§ 536 und 536a nur zu, wenn er sich seine Rechte bei Vertragsschluss vorbehält.",
        
        "§ 543 BGB": "Außerordentliche fristlose Kündigung aus wichtigem Grund. (1) Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen. Ein wichtiger Grund liegt vor, wenn dem Kündigenden unter Berücksichtigung aller Umstände des Einzelfalls, insbesondere eines Verschuldens der Vertragsparteien, und unter Abwägung der beiderseitigen Interessen die Fortsetzung des Mietverhältnisses bis zum Ablauf der Kündigungsfrist oder bis zur sonstigen Beendigung des Mietverhältnisses nicht zugemutet werden kann.",
        
        "§ 556d BGB": "Mietpreisbremse - Zulässige Miethöhe bei Mietbeginn. (1) Wird in einem Gebiet mit einem angespannten Wohnungsmarkt Wohnraum vermietet, darf die Miete zu Beginn des Mietverhältnisses höchstens 10 Prozent über der ortsüblichen Vergleichsmiete (§ 558) liegen. (2) Absatz 1 ist nicht anzuwenden auf 1. die erste Vermietung nach der Fertigstellung einer neuen Wohnung, 2. Wohnraum, der nach umfassenden Modernisierungsmaßnahmen erstmals vermietet wird.",
        
        "§ 558 BGB": "Mieterhöhung bis zur ortsüblichen Vergleichsmiete. (1) Der Vermieter kann die Zustimmung zu einer Erhöhung der Miete bis zur ortsüblichen Vergleichsmiete verlangen, wenn die Miete seit 15 Monaten unverändert ist. (2) Die ortsübliche Vergleichsmiete wird gebildet aus den üblichen Entgelten, die in der Gemeinde oder einer vergleichbaren Gemeinde für Wohnraum vergleichbarer Art, Größe, Ausstattung, Beschaffenheit und Lage einschließlich der energetischen Ausstattung und Beschaffenheit in den letzten sechs Jahren vereinbart oder geändert worden sind.",
        
        "§ 559 BGB": "Mieterhöhung nach Modernisierung. (1) Hat der Vermieter Modernisierungsmaßnahmen im Sinne des § 555b Nummer 1, 3, 4, 5 oder 6 durchgeführt, so kann er die jährliche Miete um 8 Prozent der für die Wohnung aufgewendeten Kosten erhöhen.",
        
        "§ 569 BGB": "Außerordentliche fristlose Kündigung aus wichtigem Grund. Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen. § 543 Abs. 1 Satz 2, Abs. 2 Satz 1 und 2 sowie Abs. 3 gilt entsprechend.",
        
        "§ 573 BGB": "Ordentliche Kündigung des Vermieters. (1) Der Vermieter kann nur kündigen, wenn er ein berechtigtes Interesse an der Beendigung des Mietverhältnisses hat. Ein berechtigtes Interesse liegt insbesondere vor, wenn 1. der Mieter seine vertraglichen Pflichten schuldhaft nicht unerheblich verletzt hat, 2. der Vermieter die Räume als Wohnung für sich, seine Familienangehörigen oder Angehörige seines Haushalts benötigt (Eigenbedarf) oder 3. der Vermieter durch die Fortsetzung des Mietverhältnisses an einer angemessenen wirtschaftlichen Verwertung des Grundstücks gehindert und dadurch erhebliche Nachteile erleiden würde.",
        
        "§ 574 BGB": "Widerspruch des Mieters gegen die Kündigung. (1) Der Mieter kann der Kündigung des Vermieters widersprechen und von ihm die Fortsetzung des Mietverhältnisses verlangen, wenn die Beendigung des Mietverhältnisses für den Mieter, seine Familie oder einen anderen Angehörigen seines Haushalts eine Härte bedeuten würde, die auch unter Würdigung der berechtigten Interessen des Vermieters nicht zu rechtfertigen ist.",
        
        # Kaufrecht (Auswahl)
        "§ 433 BGB": "Vertragstypische Pflichten beim Kaufvertrag. (1) Durch den Kaufvertrag wird der Verkäufer einer Sache verpflichtet, dem Käufer die Sache zu übergeben und das Eigentum an der Sache zu verschaffen. Der Verkäufer hat dem Käufer die Sache frei von Sach- und Rechtsmängeln zu verschaffen. (2) Der Käufer ist verpflichtet, dem Verkäufer den vereinbarten Kaufpreis zu zahlen und die gekaufte Sache abzunehmen.",
        
        "§ 434 BGB": "Sachmangel. (1) Die Sache ist frei von Sachmängeln, wenn sie bei Gefahrübergang die vereinbarte Beschaffenheit hat. (2) Die Sache ist frei von Sachmängeln, wenn sie sich für die nach dem Vertrag vorausgesetzte Verwendung eignet, sonst wenn sie sich für die gewöhnliche Verwendung eignet und eine Beschaffenheit aufweist, die bei Sachen der gleichen Art üblich ist.",
        
        "§ 437 BGB": "Rechte des Käufers bei Mängeln. Ist die Sache mangelhaft, kann der Käufer, wenn die Voraussetzungen der folgenden Vorschriften vorliegen und soweit nicht ein anderes bestimmt ist, 1. nach § 439 Nacherfüllung verlangen, 2. nach den §§ 440, 323 und 326 Abs. 5 vom Vertrag zurücktreten oder nach § 441 den Kaufpreis mindern und 3. nach den §§ 440, 280, 281, 283 und 311a Schadensersatz oder nach § 284 Ersatz vergeblicher Aufwendungen verlangen.",
        
        # Sachenrecht (Auswahl)
        "§ 873 BGB": "Erwerb durch Einigung und Eintragung. (1) Zur Übertragung des Eigentums an einem Grundstück, zur Belastung eines Grundstücks mit einem Recht sowie zur Übertragung oder Belastung eines solchen Rechts ist die Einigung des Berechtigten und des anderen Teils über den Eintritt der Rechtsänderung und die Eintragung der Rechtsänderung in das Grundbuch erforderlich, soweit nicht das Gesetz ein anderes vorschreibt.",
        
        "§ 925 BGB": "Auflassung. (1) Die zur Übertragung des Eigentums an einem Grundstück nach § 873 erforderliche Einigung des Veräußerers und des Erwerbers (Auflassung) muss bei gleichzeitiger Anwesenheit beider Teile vor einer zuständigen Stelle erklärt werden. Zuständig sind 1. die Notare, 2. die Gerichte.",
        
        "§ 1004 BGB": "Beseitigungs- und Unterlassungsanspruch. (1) Wird das Eigentum in anderer Weise als durch Entziehung oder Vorenthaltung des Besitzes beeinträchtigt, so kann der Eigentümer von dem Störer die Beseitigung der Beeinträchtigung verlangen. Sind weitere Beeinträchtigungen zu besorgen, so kann der Eigentümer auf Unterlassung klagen.",
        
        "§ 1093 BGB": "Nießbrauch an Grundstücken. Gegenstand des Nießbrauchs kann ein Grundstück sein. Auf den Nießbrauch an Grundstücken finden die Vorschriften der §§ 1068 bis 1084 entsprechende Anwendung.",
        
        "§ 1113 BGB": "Hypothek. (1) Ein Grundstück kann in der Weise belastet werden, dass an denjenigen, zu dessen Gunsten die Belastung erfolgt, eine bestimmte Geldsumme aus dem Grundstück zu zahlen ist (Hypothek). (2) Die Hypothek kann auch für eine künftige oder eine bedingte Forderung bestellt werden.",
    },
    
    "WEG": {
        "§ 1 WEG": "Begriffsbestimmungen. (1) Nach Maßgabe dieses Gesetzes können an Gebäuden Sondereigentum und gemeinschaftliches Eigentum begründet werden (Wohnungseigentum, Teileigentum). (2) Wohnungseigentum ist das Sondereigentum an einer Wohnung in Verbindung mit dem Miteigentumsanteil an dem gemeinschaftlichen Eigentum, zu dem es gehört. (3) Teileigentum ist das Sondereigentum an nicht zu Wohnzwecken dienenden Räumen eines Gebäudes in Verbindung mit dem Miteigentumsanteil an dem gemeinschaftlichen Eigentum, zu dem es gehört.",
        
        "§ 13 WEG": "Gemeinschaft der Wohnungseigentümer. (1) Die Wohnungseigentümer bilden die Gemeinschaft der Wohnungseigentümer. (2) Für die Gemeinschaft können Rechte erworben, kann sie verklagt werden und kann sie klagen.",
        
        "§ 14 WEG": "Kosten der Gemeinschaft. (1) Die Wohnungseigentümer tragen die Kosten, die mit dem gemeinschaftlichen Eigentum zusammenhängen, nach dem Verhältnis ihrer Anteile (§ 16), soweit nichts anderes vereinbart ist. (2) Dies gilt auch für die Kosten einer Maßnahme, die einem einzelnen oder einigen Wohnungseigentümern gemäß § 18 Absatz 1 obliegt, soweit nichts anderes vereinbart ist.",
        
        "§ 16 WEG": "Nutzungen und Lasten. (1) Jedem Wohnungseigentümer gebühren die Nutzungen des Sondereigentums und des gemeinschaftlichen Eigentums, soweit sie nicht nach § 14 Absatz 1 zu den Kosten gehören. (2) Jedem Wohnungseigentümer obliegen die Lasten seines Sondereigentums und seines Anteils. Die Lasten des gemeinschaftlichen Eigentums tragen die Wohnungseigentümer nach dem Verhältnis ihrer Anteile, soweit nichts anderes vereinbart ist.",
        
        "§ 20 WEG": "Bauliche Veränderungen. (1) Jeder Wohnungseigentümer kann angemessene bauliche Veränderungen vornehmen, die dem Gebrauch oder der Nutzung seines Sondereigentums dienen. (2) Der Wohnungseigentümer hat bauliche Veränderungen zu dulden, die für die ordnungsgemäße Instandhaltung oder Instandsetzung des gemeinschaftlichen Eigentums erforderlich sind.",
        
        "§ 23 WEG": "Beschluss. (1) Die Wohnungseigentümer beschließen über Maßnahmen, die sich auf das gemeinschaftliche Eigentum beziehen. (2) Ein Beschluss ist gültig, wenn er den Vorgaben dieses Gesetzes und der Gemeinschaftsordnung entspricht.",
        
        "§ 24 WEG": "Beschlussgegenstand. (1) Die Wohnungseigentümer können durch Beschluss Maßnahmen ordnungsgemäßer Verwaltung beschließen. (2) Für bauliche Veränderungen gilt § 20.",
        
        "§ 28 WEG": "Verwaltung. (1) Die Verwaltung des gemeinschaftlichen Eigentums steht den Wohnungseigentümern zu. (2) Die Wohnungseigentümer können durch Beschluss einen Verwalter bestellen.",
    },
    
    "GrEStG": {
        "§ 1 GrEStG": "Erwerbsvorgänge. (1) Der Grunderwerbsteuer unterliegen die folgenden Rechtsvorgänge, soweit sie sich auf inländische Grundstücke beziehen: 1. ein Kaufvertrag oder ein anderes Rechtsgeschäft, das den Anspruch auf Übereignung begründet, 2. die Auflassung, wenn kein Rechtsgeschäft vorausgegangen ist, das den Anspruch auf Übereignung begründet.",
        
        "§ 8 GrEStG": "Bemessungsgrundlage. (1) Die Steuer bemisst sich nach dem Wert der Gegenleistung. (2) Zur Gegenleistung gehören auch die vom Erwerber übernommenen sonstigen Leistungen und die dem Veräußerer vorbehaltenen Nutzungen.",
        
        "§ 9 GrEStG": "Steuersatz. Die Steuer beträgt 3,5 Prozent. Die Landesregierungen werden ermächtigt, den Steuersatz durch Rechtsverordnung zu bestimmen.",
        
        "§ 13 GrEStG": "Steuerschuldner. (1) Steuerschuldner sind die an einem Erwerbsvorgang als Vertragsteile beteiligten Personen. Sie sind Gesamtschuldner.",
    },
    
    "GEG": {
        "§ 1 GEG": "Zweck und Anwendungsbereich. (1) Zweck dieses Gesetzes ist ein möglichst sparsamer Einsatz von Energie in Gebäuden einschließlich einer zunehmenden Nutzung erneuerbarer Energien zur Erzeugung von Wärme, Kälte und Strom für den Gebäudebetrieb.",
        
        "§ 10 GEG": "Anforderungen an zu errichtende Wohngebäude. (1) Ein zu errichtendes Wohngebäude ist so zu errichten, dass der Jahres-Primärenergiebedarf für Heizung, Warmwasserbereitung, Lüftung und Kühlung das 0,55-fache des auf die Gebäudenutzfläche bezogenen Wertes des Jahres-Primärenergiebedarfs eines Referenzgebäudes gleicher Geometrie, Gebäudenutzfläche und Ausrichtung mit der in Anlage 1 angegebenen technischen Referenzausführung nicht überschreitet.",
        
        "§ 71 GEG": "Heizungspflicht - Austauschpflicht für Heizkessel. (1) Eigentümer müssen Heizkessel, die mit einem flüssigen oder gasförmigen Brennstoff beschickt werden und vor dem 1. Januar 1991 eingebaut oder aufgestellt worden sind, außer Betrieb nehmen. Absatz 1 ist nicht anzuwenden auf Niedertemperatur-Heizkessel oder Brennwertkessel.",
    }
}

# Generiere Dokumente
docs = []
for law_abbr, paragraphs in LAWS.items():
    for para_key, content in paragraphs.items():
        docs.append({
            "title": para_key,
            "content": content,
            "category": f"Gesetz: {law_abbr}",
            "unique_id": f"{law_abbr}_{para_key.replace(' ', '_').replace('§', 'Para')}",
            "source": f"{law_abbr} - Bundesrecht",
            "type": "Gesetzestext"
        })

print(f"📦 {len(docs)} Gesetzesparagraphen vorbereitet")
print(f"   - BGB: {len([d for d in docs if 'BGB' in d['category']])} Paragraphen")
print(f"   - WEG: {len([d for d in docs if 'WEG' in d['category']])} Paragraphen")
print(f"   - GrEStG: {len([d for d in docs if 'GrEStG' in d['category']])} Paragraphen")
print(f"   - GEG: {len([d for d in docs if 'GEG' in d['category']])} Paragraphen")

count_before = client.count('legal_documents').count
print(f"\n📊 Aktueller Stand: {count_before} Dokumente")

# Hole Start-ID
try:
    res = client.scroll('legal_documents', limit=1, with_vectors=False, with_payload=False)
    start_id = max([p.id for p in res[0]]) + 1 if res[0] else count_before + 1
except:
    start_id = count_before + 1

print("\n🚀 STARTE UPLOAD...")
erfolg = 0
fehler = 0

for idx, doc in enumerate(docs, start=start_id):
    try:
        # Embedding generieren
        embedding = genai.embed_content(
            model='models/embedding-001',
            content=f"{doc['title']} {doc['content']} GESETZ:{doc['unique_id']}",
            task_type='retrieval_document'
        )['embedding']
        
        # Upsert
        client.upsert(
            collection_name='legal_documents',
            points=[PointStruct(
                id=idx,
                vector=embedding,
                payload=doc
            )]
        )
        
        erfolg += 1
        
        if erfolg % 10 == 0:
            print(f"✅ {erfolg}/{len(docs)}")
        
    except Exception as e:
        fehler += 1
        if fehler <= 5:
            print(f"❌ Fehler: {str(e)[:60]}")

count_after = client.count('legal_documents').count

print("\n" + "=" * 70)
print(f"✅ Erfolgreich: {erfolg}/{len(docs)}")
print(f"❌ Fehler: {fehler}")
print(f"➕ Neu: {count_after - count_before}")
print(f"\n🎯 GESAMT: {count_after} Dokumente ({count_after/100:.1f}%)")
print(f"🏁 Noch {10000 - count_after} bis 10.000")
print("\n✅ GESETZESTEXTE GELADEN!")
