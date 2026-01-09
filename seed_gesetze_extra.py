#!/usr/bin/env python3
"""Extra Gesetze Seeding"""

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import uuid

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
client = QdrantClient(host=os.environ['QDRANT_HOST'], port=6333, api_key=os.environ['QDRANT_API_KEY'], https=True)

def embed(text):
    return genai.embed_content(model='models/text-embedding-004', content=text[:8000])['embedding']

print('🚀 EXTRA GESETZE SEEDING')

gesetze = [
    # BGB Mietrecht §§ 535-580a
    {'title': 'BGB § 535 - Inhalt und Hauptpflichten des Mietvertrags', 'content': 'Durch den Mietvertrag wird der Vermieter verpflichtet, dem Mieter den Gebrauch der Mietsache während der Mietzeit zu gewähren. Der Vermieter hat die Mietsache dem Mieter in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu überlassen und sie während der Mietzeit in diesem Zustand zu erhalten. Der Mieter ist verpflichtet, dem Vermieter die vereinbarte Miete zu entrichten.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 536 - Mietminderung bei Sach- und Rechtsmängeln', 'content': 'Hat die Mietsache zur Zeit der Überlassung an den Mieter einen Mangel, der ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufhebt, oder entsteht während der Mietzeit ein solcher Mangel, so ist der Mieter für die Zeit, in der die Tauglichkeit aufgehoben ist, von der Entrichtung der Miete befreit.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 543 - Außerordentliche fristlose Kündigung aus wichtigem Grund', 'content': 'Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen. Ein wichtiger Grund liegt vor, wenn dem Kündigenden unter Berücksichtigung aller Umstände des Einzelfalls die Fortsetzung des Mietverhältnisses bis zum Ablauf der Kündigungsfrist nicht zugemutet werden kann.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 546 - Rückgabepflicht des Mieters', 'content': 'Der Mieter ist verpflichtet, die Mietsache nach Beendigung des Mietverhältnisses zurückzugeben. Hat der Mieter den Gebrauch der Mietsache einem Dritten überlassen, so kann der Vermieter die Sache nach Beendigung des Mietverhältnisses auch von dem Dritten zurückfordern.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 548 - Verjährung der Ersatzansprüche', 'content': 'Die Ersatzansprüche des Vermieters wegen Veränderungen oder Verschlechterungen der Mietsache verjähren in sechs Monaten. Die Verjährung beginnt mit dem Zeitpunkt, in dem der Vermieter die Mietsache zurückerhält.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 549 - Auf Wohnraummietverhältnisse anwendbare Vorschriften', 'content': 'Für Mietverhältnisse über Wohnraum gelten die besonderen Vorschriften der §§ 549-577a. Diese Vorschriften sind grundsätzlich nicht abdingbar.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 556 - Betriebskosten', 'content': 'Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer durch das Eigentum am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes laufend entstehen.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 556a - Abrechnungsmaßstab für Betriebskosten', 'content': 'Der Vermieter hat bei der Abrechnung den Abrechnungsmaßstab zu wählen, der einer verbrauchsabhängigen Abrechnung am nächsten kommt. Hat der Vermieter die Betriebskosten abgerechnet, kann er eine Korrektur der Abrechnung innerhalb der Abrechnungsfrist vornehmen.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 557 - Mieterhöhungen nach Vereinbarung oder Gesetz', 'content': 'Die Miete kann durch Vereinbarung der Parteien, aufgrund einer Staffelmietvereinbarung oder aufgrund einer Indexmietvereinbarung erhöht werden. Im Übrigen kann der Vermieter bei Wohnraummietverhältnissen eine Erhöhung nur nach Maßgabe der §§ 558 bis 560 verlangen.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 558 - Mieterhöhung bis zur ortsüblichen Vergleichsmiete', 'content': 'Der Vermieter kann die Zustimmung zu einer Erhöhung der Miete bis zur ortsüblichen Vergleichsmiete verlangen. Die Kappungsgrenze beträgt 20 Prozent innerhalb von drei Jahren, in Gebieten mit angespanntem Wohnungsmarkt 15 Prozent.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 559 - Mieterhöhung nach Modernisierungsmaßnahmen', 'content': 'Hat der Vermieter Modernisierungsmaßnahmen durchgeführt, kann er die jährliche Miete um 8 Prozent der für die Wohnung aufgewendeten Kosten erhöhen. Die Kosten für Instandhaltungsmaßnahmen gehören nicht zu den aufgewendeten Kosten.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 560 - Veränderungen von Betriebskosten', 'content': 'Bei einer Betriebskostenänderung kann der Vermieter den auf den Mieter entfallenden Teil der Umlage entsprechend anpassen. Die Anpassung muss dem Mieter in Textform erklärt werden.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 561 - Sonderkündigungsrecht des Mieters bei Mieterhöhung', 'content': 'Macht der Vermieter eine Mieterhöhung geltend, kann der Mieter bis zum Ablauf des zweiten Monats nach Zugang der Erklärung das Mietverhältnis außerordentlich zum Ablauf des übernächsten Monats kündigen.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 566 - Kauf bricht nicht Miete', 'content': 'Wird der vermietete Wohnraum nach der Überlassung an den Mieter von dem Vermieter an einen Dritten veräußert, so tritt der Erwerber anstelle des Vermieters in die sich während der Dauer seines Eigentums aus dem Mietverhältnis ergebenden Rechte und Pflichten ein.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 568 - Form und Inhalt der Kündigung', 'content': 'Die Kündigung des Mietverhältnisses bedarf der schriftlichen Form. Der Vermieter soll den Mieter bei der Kündigung auf sein Widerspruchsrecht nach § 574 hinweisen.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 573 - Ordentliche Kündigung des Vermieters', 'content': 'Der Vermieter kann nur kündigen, wenn er ein berechtigtes Interesse an der Beendigung des Mietverhältnisses hat. Ein berechtigtes Interesse liegt insbesondere vor bei Eigenbedarf, erheblicher Pflichtverletzung des Mieters oder wirtschaftlicher Verwertung.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 573c - Fristen der ordentlichen Kündigung', 'content': 'Die Kündigungsfrist beträgt drei Monate. Nach fünf Jahren erhöht sie sich um drei Monate auf sechs Monate. Nach acht Jahren beträgt sie neun Monate.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 574 - Widerspruch des Mieters gegen die Kündigung', 'content': 'Der Mieter kann der Kündigung widersprechen und Fortsetzung des Mietverhältnisses verlangen, wenn die Beendigung für ihn eine Härte bedeuten würde, die auch unter Würdigung der berechtigten Interessen des Vermieters nicht zu rechtfertigen ist.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 575 - Zeitmietvertrag', 'content': 'Ein Mietverhältnis kann auf bestimmte Zeit eingegangen werden, wenn der Vermieter nach Ablauf der Mietzeit die Räume als Wohnung für sich, seine Familienangehörigen oder Angehörige seines Haushalts nutzen will.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 577 - Vorkaufsrecht des Mieters', 'content': 'Werden vermietete Wohnräume in Wohnungseigentum umgewandelt und an einen Dritten verkauft, so ist der Mieter zum Vorkauf berechtigt. Der Vorkaufsfall tritt nicht ein, wenn der Vermieter die Wohnung an einen Familienangehörigen verkauft.', 'source': 'BGB', 'category': 'Mietrecht', 'doc_type': 'Gesetz'},

    # WEG
    {'title': 'WEG § 1 - Begriffsbestimmungen', 'content': 'Nach Maßgabe dieses Gesetzes kann an Wohnungen das Wohnungseigentum, an nicht zu Wohnzwecken dienenden Räumen eines Gebäudes das Teileigentum begründet werden.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 5 - Gegenstand und Inhalt des Sondereigentums', 'content': 'Gegenstand des Sondereigentums sind die gemäß § 3 Absatz 1 bestimmten Räume sowie die zu diesen Räumen gehörenden Bestandteile des Gebäudes, die verändert, beseitigt oder eingefügt werden können, ohne dass dadurch das gemeinschaftliche Eigentum oder ein auf Sondereigentum beruhendes Recht eines anderen Wohnungseigentümers beeinträchtigt wird.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 10 - Allgemeine Grundsätze', 'content': 'Die Wohnungseigentümer bilden eine Gemeinschaft. Das Verhältnis der Wohnungseigentümer untereinander und zur Gemeinschaft bestimmt sich nach den Vorschriften dieses Gesetzes und, soweit dieses Gesetz keine besonderen Bestimmungen enthält, nach dem Bürgerlichen Gesetzbuch.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 14 - Pflichten des Wohnungseigentümers', 'content': 'Jeder Wohnungseigentümer ist gegenüber der Gemeinschaft der Wohnungseigentümer verpflichtet, die gesetzlichen Regelungen, Vereinbarungen und Beschlüsse einzuhalten und das Betreten seines Sondereigentums zu dulden, soweit dies zur Instandhaltung und Instandsetzung des gemeinschaftlichen Eigentums erforderlich ist.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 19 - Verwaltung durch die Wohnungseigentümer', 'content': 'Die Wohnungseigentümer beschließen über die Verwaltung des gemeinschaftlichen Eigentums. Die Beschlüsse werden mit Stimmenmehrheit gefasst. Grundlage ist das Kopfprinzip, sofern nicht durch Vereinbarung etwas anderes bestimmt ist.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 20 - Bauliche Veränderungen', 'content': 'Maßnahmen, die über die ordnungsmäßige Erhaltung des gemeinschaftlichen Eigentums hinausgehen (bauliche Veränderungen), können beschlossen werden. Jeder Wohnungseigentümer kann angemessene bauliche Veränderungen verlangen, die dem Gebrauch durch Menschen mit Behinderungen oder der Nutzung von Elektromobilität dienen.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 21 - Nutzungen und Kosten bei baulichen Veränderungen', 'content': 'Die Kosten einer baulichen Veränderung tragen die Wohnungseigentümer, die für sie gestimmt haben. Alle Wohnungseigentümer tragen die Kosten, wenn die bauliche Veränderung mit mehr als zwei Dritteln der abgegebenen Stimmen beschlossen wurde und diese Stimmen mehr als die Hälfte aller Miteigentumsanteile repräsentieren.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 25 - Versammlung der Wohnungseigentümer', 'content': 'Die Versammlung der Wohnungseigentümer wird vom Verwalter mindestens einmal im Jahr einberufen. Die Einberufung erfolgt in Textform. Die Eigentümerversammlung ist beschlussfähig, wenn die erschienenen stimmberechtigten Wohnungseigentümer mehr als die Hälfte der Miteigentumsanteile vertreten.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 26 - Bestellung und Abberufung des Verwalters', 'content': 'Die Wohnungseigentümer bestellen einen Verwalter. Die Bestellung kann auf höchstens fünf Jahre erfolgen. Die Abberufung des Verwalters kann jederzeit erfolgen.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    {'title': 'WEG § 28 - Hausgeld und Wirtschaftsplan', 'content': 'Jeder Wohnungseigentümer ist verpflichtet, Vorschüsse auf die von ihm zu tragenden Kosten (Hausgeld) zu leisten. Der Verwalter hat einen Wirtschaftsplan aufzustellen. Die Wohnungseigentümer beschließen über den Wirtschaftsplan.', 'source': 'WEG', 'category': 'WEG', 'doc_type': 'Gesetz'},
    
    # GBO
    {'title': 'GBO § 1 - Grundbuchämter', 'content': 'Die Grundbücher werden von den Amtsgerichten als Grundbuchämtern geführt. Für jedes Grundstück wird ein besonderes Grundbuchblatt angelegt.', 'source': 'GBO', 'category': 'Grundbuchrecht', 'doc_type': 'Gesetz'},
    {'title': 'GBO § 13 - Antragsgrundsatz', 'content': 'Eine Eintragung soll nur auf Antrag erfolgen. Antragsberechtigt ist jeder, dessen Recht von der Eintragung betroffen wird, oder der Notar, der die Urkunde über das der Eintragung zugrunde liegende Rechtsgeschäft beurkundet hat.', 'source': 'GBO', 'category': 'Grundbuchrecht', 'doc_type': 'Gesetz'},
    {'title': 'GBO § 19 - Bewilligung', 'content': 'Eine Eintragung erfolgt, wenn derjenige sie bewilligt, dessen Recht von ihr betroffen wird. Bei einer Auflassung genügt die Erklärung der Auflassung.', 'source': 'GBO', 'category': 'Grundbuchrecht', 'doc_type': 'Gesetz'},
    {'title': 'GBO § 29 - Formvorschriften', 'content': 'Eine Eintragung soll nur vorgenommen werden, wenn die Eintragungsbewilligung oder die sonstigen zu der Eintragung erforderlichen Erklärungen durch öffentliche oder öffentlich beglaubigte Urkunden nachgewiesen werden.', 'source': 'GBO', 'category': 'Grundbuchrecht', 'doc_type': 'Gesetz'},
    {'title': 'GBO § 45 - Grundbucheinsicht', 'content': 'Die Einsicht des Grundbuchs ist jedem gestattet, der ein berechtigtes Interesse darlegt. Das berechtigte Interesse ist glaubhaft zu machen.', 'source': 'GBO', 'category': 'Grundbuchrecht', 'doc_type': 'Gesetz'},
    
    # BetrKV
    {'title': 'BetrKV § 1 - Betriebskosten', 'content': 'Betriebskosten sind die Kosten, die dem Eigentümer durch das Eigentum am Grundstück oder durch den bestimmungsmäßigen Gebrauch des Gebäudes, der Nebengebäude, Anlagen, Einrichtungen und des Grundstücks laufend entstehen.', 'source': 'BetrKV', 'category': 'Mietrecht', 'doc_type': 'Verordnung'},
    {'title': 'BetrKV § 2 - Aufstellung der Betriebskosten', 'content': 'Zu den Betriebskosten gehören: Grundsteuer, Wasserversorgung, Entwässerung, Heizkosten, Warmwasser, Aufzug, Straßenreinigung, Müllbeseitigung, Gebäudereinigung, Gartenpflege, Beleuchtung, Schornsteinreinigung, Versicherungen, Hauswart, Gemeinschaftsantenne, Waschraum, sonstige Betriebskosten.', 'source': 'BetrKV', 'category': 'Mietrecht', 'doc_type': 'Verordnung'},

    # GrEStG
    {'title': 'GrEStG § 1 - Erwerbsvorgänge', 'content': 'Der Grunderwerbsteuer unterliegen Kaufverträge und andere Rechtsgeschäfte, die den Anspruch auf Übereignung eines inländischen Grundstücks begründen. Die Auflassung, wenn kein Rechtsgeschäft vorausgegangen ist. Der Übergang des Eigentums, wenn kein den Anspruch auf Übereignung begründendes Rechtsgeschäft vorausgegangen ist.', 'source': 'GrEStG', 'category': 'Steuerrecht', 'doc_type': 'Gesetz'},
    {'title': 'GrEStG § 3 - Allgemeine Ausnahmen', 'content': 'Von der Besteuerung sind ausgenommen: Der Erwerb eines Grundstücks, wenn der für die Berechnung der Steuer maßgebende Wert 2.500 Euro nicht übersteigt. Erwerbe von Todes wegen und Schenkungen. Erwerbe zwischen Ehegatten oder Lebenspartnern.', 'source': 'GrEStG', 'category': 'Steuerrecht', 'doc_type': 'Gesetz'},
    {'title': 'GrEStG § 8 - Bemessungsgrundlage', 'content': 'Die Steuer bemisst sich nach dem Wert der Gegenleistung. Bei einem Kauf ist Gegenleistung der Kaufpreis einschließlich der vom Käufer übernommenen sonstigen Leistungen und der dem Verkäufer vorbehaltenen Nutzungen.', 'source': 'GrEStG', 'category': 'Steuerrecht', 'doc_type': 'Gesetz'},
    {'title': 'GrEStG § 11 - Steuersatz', 'content': 'Die Steuer beträgt 3,5 Prozent der Bemessungsgrundlage. Die Länder können durch Gesetz einen abweichenden Steuersatz bestimmen.', 'source': 'GrEStG', 'category': 'Steuerrecht', 'doc_type': 'Gesetz'},

    # MaBV
    {'title': 'MaBV § 1 - Anwendungsbereich', 'content': 'Diese Verordnung gilt für Gewerbetreibende, die als Bauträger oder als Baubetreuer tätig sind, sowie für Makler.', 'source': 'MaBV', 'category': 'Maklerrecht', 'doc_type': 'Verordnung'},
    {'title': 'MaBV § 3 - Sicherheiten bei Bauträgern', 'content': 'Der Bauträger darf Vermögenswerte des Auftraggebers nur nach Maßgabe der Vorschriften dieser Verordnung entgegennehmen. Er hat eine Sicherheit für die Erfüllung seiner Verpflichtungen zu leisten.', 'source': 'MaBV', 'category': 'Maklerrecht', 'doc_type': 'Verordnung'},

    # GEG
    {'title': 'GEG § 1 - Zweck und Ziel', 'content': 'Zweck dieses Gesetzes ist ein möglichst sparsamer Einsatz von Energie in Gebäuden einschließlich einer zunehmenden Nutzung erneuerbarer Energien zur Erzeugung von Wärme, Kälte und Strom für den Gebäudebetrieb.', 'source': 'GEG', 'category': 'Baurecht', 'doc_type': 'Gesetz'},
    {'title': 'GEG § 79 - Ausstellung und Verwendung von Energieausweisen', 'content': 'Bei der Errichtung eines Gebäudes ist ein Energieausweis auszustellen. Bei bestehenden Gebäuden ist auf Verlangen eines Eigentümers ein Energieausweis auszustellen. Der Energieausweis ist dem Käufer oder Mieter bei Verkauf oder Vermietung vorzulegen.', 'source': 'GEG', 'category': 'Baurecht', 'doc_type': 'Gesetz'},

    # HeizkostenV
    {'title': 'HeizkostenV § 1 - Anwendungsbereich', 'content': 'Diese Verordnung gilt für die Verteilung der Kosten des Betriebs zentraler Heizungsanlagen und zentraler Warmwasserversorgungsanlagen.', 'source': 'HeizkostenV', 'category': 'Mietrecht', 'doc_type': 'Verordnung'},
    {'title': 'HeizkostenV § 7 - Verteilung der Kosten der Versorgung mit Wärme', 'content': 'Die Kosten des Betriebs einer zentralen Heizungsanlage sind mindestens zu 50 Prozent, höchstens zu 70 Prozent nach dem erfassten Wärmeverbrauch der Nutzer zu verteilen. In sonstigen Fällen sind die Kosten nach der Wohn- oder Nutzfläche oder nach dem umbauten Raum zu verteilen.', 'source': 'HeizkostenV', 'category': 'Mietrecht', 'doc_type': 'Verordnung'},
    {'title': 'HeizkostenV § 9 - Verteilung der Kosten der Versorgung mit Warmwasser', 'content': 'Die Kosten des Betriebs einer zentralen Warmwasserversorgungsanlage sind mindestens zu 50 Prozent, höchstens zu 70 Prozent nach dem erfassten Warmwasserverbrauch zu verteilen.', 'source': 'HeizkostenV', 'category': 'Mietrecht', 'doc_type': 'Verordnung'},
]

print(f'📤 Uploading {len(gesetze)} Dokumente...')
points = []
for i, doc in enumerate(gesetze):
    vector = embed(doc['content'])
    points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=doc))
    if (i+1) % 10 == 0:
        print(f'  📝 {i+1}/{len(gesetze)} embedded...')

for i in range(0, len(points), 25):
    batch = points[i:i+25]
    client.upsert(collection_name='legal_documents', points=batch)
    print(f'  ✅ Batch {i//25+1}: {len(batch)} docs')

info = client.get_collection('legal_documents')
print(f'📊 Gesamt: {info.points_count} Dokumente')
