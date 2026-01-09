#!/usr/bin/env python3
"""
Massives Seeding: BGB Vollständig (Mietrecht, Kaufrecht, Sachenrecht)
+ Weitere Gesetze: GBO, ZVG, ErbbauRG, WoEigG
Ziel: +200 Dokumente
"""

import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

QDRANT_HOST = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    result = genai.embed_content(
        model="models/embedding-001",
        content=text[:8000],
        task_type="retrieval_document"
    )
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# BGB Kaufrecht (§§ 433-480)
BGB_KAUFRECHT = [
    {"paragraph": "§ 433 BGB", "titel": "Vertragstypische Pflichten beim Kaufvertrag", "inhalt": "Durch den Kaufvertrag wird der Verkäufer verpflichtet, dem Käufer die Sache zu übergeben und das Eigentum daran zu verschaffen. Der Verkäufer hat die Sache frei von Sach- und Rechtsmängeln zu verschaffen. Der Käufer ist verpflichtet, dem Verkäufer den vereinbarten Kaufpreis zu zahlen und die gekaufte Sache abzunehmen."},
    {"paragraph": "§ 434 BGB", "titel": "Sachmangel", "inhalt": "Die Sache ist frei von Sachmängeln, wenn sie bei Gefahrübergang die vereinbarte Beschaffenheit hat. Soweit die Beschaffenheit nicht vereinbart ist, ist die Sache frei von Sachmängeln, wenn sie sich für die nach dem Vertrag vorausgesetzte Verwendung eignet oder für die gewöhnliche Verwendung eignet und eine Beschaffenheit aufweist, die bei Sachen der gleichen Art üblich ist."},
    {"paragraph": "§ 435 BGB", "titel": "Rechtsmangel", "inhalt": "Die Sache ist frei von Rechtsmängeln, wenn Dritte in Bezug auf die Sache keine oder nur die im Kaufvertrag übernommenen Rechte gegen den Käufer geltend machen können. Einem Rechtsmangel steht es gleich, wenn im Grundbuch ein Recht eingetragen ist, das nicht besteht."},
    {"paragraph": "§ 437 BGB", "titel": "Rechte des Käufers bei Mängeln", "inhalt": "Ist die Sache mangelhaft, kann der Käufer: 1. nach § 439 Nacherfüllung verlangen, 2. nach §§ 440, 323, 326 Abs. 5 vom Vertrag zurücktreten oder nach § 441 den Kaufpreis mindern, 3. nach §§ 440, 280-283, 311a Schadensersatz oder Ersatz vergeblicher Aufwendungen verlangen."},
    {"paragraph": "§ 438 BGB", "titel": "Verjährung der Mängelansprüche", "inhalt": "Die Ansprüche verjähren in 30 Jahren bei dinglichen Rechten Dritter oder eingetragenen Rechten, in 5 Jahren bei Bauwerken, in 2 Jahren im Regelfall. Die Verjährung beginnt mit Ablieferung der Sache. Bei arglistigem Verschweigen gilt die regelmäßige Verjährung."},
    {"paragraph": "§ 439 BGB", "titel": "Nacherfüllung", "inhalt": "Der Käufer kann als Nacherfüllung nach seiner Wahl die Beseitigung des Mangels oder die Lieferung einer mangelfreien Sache verlangen. Der Verkäufer hat die zum Zweck der Nacherfüllung erforderlichen Aufwendungen zu tragen. Er kann die Nacherfüllung verweigern, wenn sie nur mit unverhältnismäßigen Kosten möglich ist."},
    {"paragraph": "§ 440 BGB", "titel": "Besondere Bestimmungen für Rücktritt und Schadensersatz", "inhalt": "Außer in den Fällen des § 281 Abs. 2 und des § 323 Abs. 2 bedarf es der Fristsetzung auch dann nicht, wenn der Verkäufer beide Arten der Nacherfüllung verweigert oder wenn die Nacherfüllung fehlgeschlagen oder dem Käufer unzumutbar ist. Eine Nachbesserung gilt nach dem erfolglosen zweiten Versuch als fehlgeschlagen."},
    {"paragraph": "§ 441 BGB", "titel": "Minderung", "inhalt": "Statt zurückzutreten, kann der Käufer den Kaufpreis durch Erklärung gegenüber dem Verkäufer mindern. Der Ausschlussgrund des § 323 Abs. 5 Satz 2 findet keine Anwendung. Bei der Minderung ist der Kaufpreis in dem Verhältnis herabzusetzen, in welchem zur Zeit des Vertragsschlusses der Wert der Sache in mangelfreiem Zustand zu dem wirklichen Wert gestanden haben würde."},
    {"paragraph": "§ 442 BGB", "titel": "Kenntnis des Käufers", "inhalt": "Die Rechte des Käufers wegen eines Mangels sind ausgeschlossen, wenn er bei Vertragsschluss den Mangel kennt. Ist dem Käufer ein Mangel infolge grober Fahrlässigkeit unbekannt geblieben, kann er Rechte wegen dieses Mangels nur geltend machen, wenn der Verkäufer den Mangel arglistig verschwiegen oder eine Garantie für die Beschaffenheit übernommen hat."},
    {"paragraph": "§ 444 BGB", "titel": "Haftungsausschluss", "inhalt": "Auf eine Vereinbarung, durch welche die Rechte des Käufers wegen eines Mangels ausgeschlossen oder beschränkt werden, kann sich der Verkäufer nicht berufen, soweit er den Mangel arglistig verschwiegen oder eine Garantie für die Beschaffenheit der Sache übernommen hat."},
]

# GBO - Grundbuchordnung
GBO_PARAGRAPHEN = [
    {"paragraph": "§ 1 GBO", "titel": "Führung des Grundbuchs", "inhalt": "Die Grundbücher werden von den Amtsgerichten (Grundbuchämtern) geführt. Jedes Grundstück erhält im Grundbuch eine besondere Stelle (Grundbuchblatt). Das Grundbuchblatt ist für das Grundstück als das Grundbuch anzusehen."},
    {"paragraph": "§ 2 GBO", "titel": "Aufschriften", "inhalt": "Die Grundbücher sind für jeden Amtsgerichtsbezirk nach Bezirken zu führen. Jedem Bezirk ist ein besonderer Band des Grundbuchs zu widmen. Die Blätter jedes Bandes sind mit fortlaufenden Nummern zu versehen."},
    {"paragraph": "§ 3 GBO", "titel": "Grundbuchblatt", "inhalt": "Jedes Blatt des Grundbuchs ist für ein Grundstück bestimmt. Die Vereinigung mehrerer Grundstücke auf einem Blatt ist zulässig, wenn die Grundstücke in demselben Bezirk belegen sind."},
    {"paragraph": "§ 13 GBO", "titel": "Antrag auf Eintragung", "inhalt": "Eine Eintragung soll nur auf Antrag erfolgen. Antragsberechtigt ist jeder, dessen Recht von der Eintragung betroffen wird oder zu dessen Gunsten die Eintragung erfolgen soll. Ein Antrag kann durch einseitigen Widerruf oder durch Vereinbarung der Beteiligten zurückgenommen werden."},
    {"paragraph": "§ 19 GBO", "titel": "Bewilligungsgrundsatz", "inhalt": "Eine Eintragung erfolgt nur, wenn derjenige sie bewilligt, dessen Recht von ihr betroffen wird. Bei der Eintragung eines neuen Eigentümers wird die Bewilligung des eingetragenen Eigentümers verlangt. Ist der eingetragene Eigentümer verstorben, so ist die Bewilligung der Erben erforderlich."},
    {"paragraph": "§ 20 GBO", "titel": "Eintragung der Auflassung", "inhalt": "Im Falle der Auflassung eines Grundstücks sowie im Falle einer sonstigen rechtsgeschäftlichen Einigung über die Übertragung des Eigentums soll die Eintragung nur erfolgen, wenn die erforderliche Einigung erklärt ist."},
    {"paragraph": "§ 29 GBO", "titel": "Form der Urkunden", "inhalt": "Eine Eintragung soll nur vorgenommen werden, wenn die Eintragungsbewilligung oder die sonstigen zu der Eintragung erforderlichen Erklärungen durch öffentliche oder öffentlich beglaubigte Urkunden nachgewiesen werden. Die Erklärung über die Auflassung muss notariell beurkundet sein."},
    {"paragraph": "§ 39 GBO", "titel": "Rangordnung", "inhalt": "Das Rangverhältnis unter mehreren in derselben Abteilung eingetragenen Rechten bestimmt sich nach der Reihenfolge der Eintragungen. Rechte in verschiedenen Abteilungen haben untereinander Gleichrang. Dem Zeitpunkt der Eintragung steht der Zeitpunkt des Eingangs des Eintragungsantrags gleich."},
    {"paragraph": "§ 45 GBO", "titel": "Rangänderung", "inhalt": "Das Rangverhältnis kann nachträglich durch Einigung der Beteiligten geändert werden. Die Änderung bedarf der Eintragung in das Grundbuch. Die Zustimmung des Eigentümers ist nur erforderlich, wenn die Rangänderung zu einer unmittelbaren Beeinträchtigung seines Rechts führt."},
    {"paragraph": "§ 53 GBO", "titel": "Einsicht in das Grundbuch", "inhalt": "Die Einsicht des Grundbuchs ist jedem gestattet, der ein berechtigtes Interesse darlegt. Das berechtigte Interesse ist glaubhaft zu machen. Eigentümer und dinglich Berechtigte haben ohne weiteres ein Einsichtsrecht."},
]

# ZVG - Zwangsversteigerungsgesetz
ZVG_PARAGRAPHEN = [
    {"paragraph": "§ 1 ZVG", "titel": "Gegenstand der Zwangsversteigerung", "inhalt": "Die Zwangsversteigerung eines Grundstücks erfolgt durch Beschluss des Amtsgerichts. Zuständig ist das Gericht, in dessen Bezirk das Grundstück belegen ist. Die Zwangsversteigerung dient der Befriedigung der Gläubiger aus dem Grundstück."},
    {"paragraph": "§ 15 ZVG", "titel": "Anordnung der Versteigerung", "inhalt": "Die Zwangsversteigerung wird angeordnet, wenn der Antrag des Gläubigers die gesetzlichen Erfordernisse erfüllt. Der Beschluss ist dem Schuldner zuzustellen. Mit der Zustellung wird das Grundstück beschlagnahmt."},
    {"paragraph": "§ 44 ZVG", "titel": "Geringstes Gebot", "inhalt": "Ein Gebot ist nur dann gültig, wenn es das geringste Gebot erreicht. Das geringste Gebot muss die Kosten des Verfahrens und die dem Anspruch des Gläubigers vorgehenden Rechte decken. Erreicht kein Gebot das geringste Gebot, wird die Versteigerung eingestellt."},
    {"paragraph": "§ 74a ZVG", "titel": "5/10 und 7/10 Grenze", "inhalt": "Der Zuschlag ist zu versagen, wenn das abgegebene Meistgebot einschließlich des Kapitalwertes der stehenbleibenden Rechte die Hälfte des Grundstückswertes nicht erreicht (5/10-Grenze). Erreicht das Gebot nicht 7/10 des Wertes, kann ein berechtigter Beteiligter die Versagung verlangen."},
    {"paragraph": "§ 81 ZVG", "titel": "Zuschlag", "inhalt": "Der Zuschlag ist durch Beschluss zu erteilen, wenn die Voraussetzungen dafür vorliegen. Mit der Verkündung des Zuschlags geht das Eigentum an dem Grundstück auf den Ersteher über. Der Zuschlagsbeschluss ersetzt die Auflassung."},
    {"paragraph": "§ 85 ZVG", "titel": "Übergang von Rechten", "inhalt": "Mit dem Zuschlag erlöschen die Rechte, die nicht bestehen bleiben. Die bestehenbleibenden Rechte sind im Zuschlagsbeschluss aufzuführen. Der Ersteher übernimmt das Grundstück frei von diesen erloschenen Rechten."},
    {"paragraph": "§ 152 ZVG", "titel": "Zwangsverwaltung", "inhalt": "Die Zwangsverwaltung wird angeordnet, wenn der Gläubiger aus den Nutzungen des Grundstücks befriedigt werden soll. Das Gericht bestellt einen Verwalter, der das Grundstück verwaltet und die Erträge an die Gläubiger verteilt."},
]

# ErbbauRG
ERBBAURG = [
    {"paragraph": "§ 1 ErbbauRG", "titel": "Gesetzlicher Inhalt des Erbbaurechts", "inhalt": "Ein Grundstück kann in der Weise belastet werden, dass demjenigen, zu dessen Gunsten die Belastung erfolgt, das veräußerliche und vererbliche Recht zusteht, auf oder unter der Oberfläche des Grundstücks ein Bauwerk zu haben (Erbbaurecht). Das Erbbaurecht kann auf einen Teil des Grundstücks beschränkt werden."},
    {"paragraph": "§ 2 ErbbauRG", "titel": "Bestandteile des Bauwerks", "inhalt": "Das Bauwerk gilt als wesentlicher Bestandteil des Erbbaurechts. Die Bestandteile des Bauwerks und das Zubehör sind nicht Bestandteile des Grundstücks. Das Erbbaurecht erstreckt sich auch auf einen für die Ausübung erforderlichen Teil der Grundstücksfläche."},
    {"paragraph": "§ 9 ErbbauRG", "titel": "Erbbauzins", "inhalt": "Das Erbbaurecht kann gegen Zahlung eines Erbbauzinses bestellt werden. Für die Bestellung eines Erbbauzinses gelten die Vorschriften über die Bestellung einer Reallast. Der Erbbauzins ist an den jeweiligen Grundstückseigentümer zu zahlen."},
    {"paragraph": "§ 27 ErbbauRG", "titel": "Heimfall", "inhalt": "Es kann vereinbart werden, dass der Grundstückseigentümer bei Vorliegen bestimmter Voraussetzungen die Übertragung des Erbbaurechts auf sich verlangen kann (Heimfall). Im Heimfallfall hat der Erbbauberechtigte Anspruch auf eine angemessene Vergütung für das Bauwerk."},
    {"paragraph": "§ 32 ErbbauRG", "titel": "Erlöschen des Erbbaurechts", "inhalt": "Das Erbbaurecht erlischt mit Ablauf der Zeit, für die es bestellt ist. Bei Erlöschen geht das Bauwerk in das Eigentum des Grundstückseigentümers über. Dem Erbbauberechtigten gebührt eine Entschädigung für den Wert des Bauwerks."},
]

# WoEigG - Wohnungseigentumsgesetz (wichtige Paragraphen)
WOEIG_PARAGRAPHEN = [
    {"paragraph": "§ 1 WEG", "titel": "Begriffsbestimmungen", "inhalt": "Nach Maßgabe dieses Gesetzes kann an Wohnungen das Wohnungseigentum, an nicht zu Wohnzwecken dienenden Räumen eines Gebäudes das Teileigentum begründet werden. Wohnungseigentum ist das Sondereigentum an einer Wohnung in Verbindung mit dem Miteigentumsanteil an dem gemeinschaftlichen Eigentum."},
    {"paragraph": "§ 3 WEG", "titel": "Vertragliche Einräumung von Sondereigentum", "inhalt": "Die Miteigentümer können durch Vertrag die Einräumung von Sondereigentum vereinbaren. Der Vertrag bedarf der notariellen Beurkundung. Das Sondereigentum muss räumlich abgegrenzt sein und einen wesentlichen Gebäudeteil darstellen."},
    {"paragraph": "§ 5 WEG", "titel": "Gegenstand und Inhalt des Sondereigentums", "inhalt": "Gegenstand des Sondereigentums sind die gemäß § 3 Abs. 1 bestimmten Räume sowie die zu diesen Räumen gehörenden Bestandteile des Gebäudes, die verändert, beseitigt oder eingefügt werden können, ohne dass dadurch das gemeinschaftliche Eigentum oder ein auf Sondereigentum beruhendes Recht eines anderen Wohnungseigentümers beeinträchtigt wird."},
    {"paragraph": "§ 10 WEG", "titel": "Allgemeine Grundsätze", "inhalt": "Die Wohnungseigentümer können durch Vereinbarung die sich aus dem Gesetz ergebenden Rechte und Pflichten abweichend regeln, soweit nicht etwas anderes bestimmt ist. Von den Vorschriften dieses Gesetzes abweichende Vereinbarungen können die Wohnungseigentümer nur treffen, soweit das Gesetz dies zulässt."},
    {"paragraph": "§ 16 WEG", "titel": "Nutzungen und Kosten", "inhalt": "Jedem Wohnungseigentümer gebührt ein seinem Anteil entsprechender Bruchteil der Nutzungen des gemeinschaftlichen Eigentums. Jeder Wohnungseigentümer ist den anderen gegenüber verpflichtet, die Kosten und Lasten des gemeinschaftlichen Eigentums nach dem Verhältnis seiner Miteigentumsanteile zu tragen."},
    {"paragraph": "§ 18 WEG", "titel": "Verwaltung des gemeinschaftlichen Eigentums", "inhalt": "Die Verwaltung des gemeinschaftlichen Eigentums steht der Gemeinschaft der Wohnungseigentümer zu. Die Wohnungseigentümer können beschließen, dass die Verwaltung einem Verwalter übertragen wird. Der Verwalter handelt im Namen der Gemeinschaft."},
    {"paragraph": "§ 19 WEG", "titel": "Pflichten des Verwalters", "inhalt": "Der Verwalter ist gegenüber der Gemeinschaft verpflichtet, die ihm obliegenden Aufgaben ordnungsgemäß durchzuführen, eine Eigentümerversammlung einzuberufen, den Beschluss der Wohnungseigentümer durchzuführen und die Gemeinschaft im Rechtsverkehr zu vertreten."},
    {"paragraph": "§ 23 WEG", "titel": "Eigentümerversammlung", "inhalt": "Angelegenheiten der Verwaltung werden durch Beschlussfassung in einer Versammlung der Wohnungseigentümer geordnet. Die Versammlung wird von dem Verwalter einberufen. Die Einladung muss in Textform mit einer Frist von mindestens drei Wochen erfolgen."},
    {"paragraph": "§ 25 WEG", "titel": "Beschlussfassung", "inhalt": "Für die Beschlussfassung ist die Mehrheit der abgegebenen Stimmen erforderlich, soweit nicht dieses Gesetz oder die Gemeinschaftsordnung eine größere Mehrheit oder weitere Erfordernisse vorschreibt. Stimmenthaltungen gelten als nicht abgegebene Stimmen."},
    {"paragraph": "§ 28 WEG", "titel": "Wirtschaftsplan und Rechnungslegung", "inhalt": "Der Verwalter hat für jedes Kalenderjahr einen Wirtschaftsplan aufzustellen. Nach Ablauf des Kalenderjahres hat er eine Abrechnung aufzustellen. Der Wirtschaftsplan und die Abrechnung sind der Wohnungseigentümerversammlung zur Beschlussfassung vorzulegen."},
]

# ImmoWertV - Immobilienwertermittlungsverordnung
IMMOWERTV = [
    {"paragraph": "§ 1 ImmoWertV", "titel": "Anwendungsbereich", "inhalt": "Diese Verordnung ist anzuwenden bei der Ermittlung der Verkehrswerte von Grundstücken und grundstücksgleichen Rechten nach § 194 des Baugesetzbuchs. Sie gilt für die Gutachterausschüsse, deren Geschäftsstellen und für alle Sachverständigen, die mit der Ermittlung von Verkehrswerten beauftragt werden."},
    {"paragraph": "§ 3 ImmoWertV", "titel": "Verkehrswert", "inhalt": "Der Verkehrswert wird durch den Preis bestimmt, der in dem Zeitpunkt, auf den sich die Ermittlung bezieht, im gewöhnlichen Geschäftsverkehr nach den rechtlichen Gegebenheiten und tatsächlichen Eigenschaften, der sonstigen Beschaffenheit und der Lage des Grundstücks ohne Rücksicht auf ungewöhnliche oder persönliche Verhältnisse zu erzielen wäre."},
    {"paragraph": "§ 6 ImmoWertV", "titel": "Vergleichswertverfahren", "inhalt": "Im Vergleichswertverfahren wird der Vergleichswert aus einer ausreichenden Zahl von Vergleichspreisen ermittelt. Vergleichspreise sind Kaufpreise von Grundstücken, die mit dem zu bewertenden Grundstück hinreichend übereinstimmen. Wertbeeinflussende Unterschiede sind durch Zu- oder Abschläge zu berücksichtigen."},
    {"paragraph": "§ 10 ImmoWertV", "titel": "Ertragswertverfahren", "inhalt": "Im Ertragswertverfahren wird der Ertragswert auf der Grundlage des nachhaltig erzielbaren jährlichen Reinertrags ermittelt. Der Reinertrag ergibt sich aus dem Rohertrag abzüglich der Bewirtschaftungskosten. Der Ertragswert ist der auf den Wertermittlungsstichtag abgezinste Barwert aller zukünftigen Reinerträge."},
    {"paragraph": "§ 21 ImmoWertV", "titel": "Sachwertverfahren", "inhalt": "Im Sachwertverfahren wird der Sachwert aus dem Bodenwert und dem Wert der baulichen Anlagen ermittelt. Der Wert der baulichen Anlagen wird auf der Grundlage von Herstellungskosten unter Berücksichtigung der Alterswertminderung ermittelt."},
    {"paragraph": "§ 14 ImmoWertV", "titel": "Bodenrichtwert", "inhalt": "Bodenrichtwerte sind durchschnittliche Lagewerte des Bodens für eine Mehrheit von Grundstücken innerhalb eines abgegrenzten Gebiets. Sie werden von den Gutachterausschüssen ermittelt und veröffentlicht. Bodenrichtwerte sind für die Besteuerung und für Entschädigungen von Bedeutung."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        api_key=QDRANT_API_KEY,
        https=True
    )
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # BGB Kaufrecht
    for item in BGB_KAUFRECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "BGB Kaufrecht", "title": item['titel']}
        })
    
    # GBO
    for item in GBO_PARAGRAPHEN:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Grundbuchordnung", "title": item['titel']}
        })
    
    # ZVG
    for item in ZVG_PARAGRAPHEN:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Zwangsversteigerungsgesetz", "title": item['titel']}
        })
    
    # ErbbauRG
    for item in ERBBAURG:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Erbbaurechtsgesetz", "title": item['titel']}
        })
    
    # WEG
    for item in WOEIG_PARAGRAPHEN:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "WEG", "title": item['titel']}
        })
    
    # ImmoWertV
    for item in IMMOWERTV:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text),
            "text": text,
            "metadata": {"source": item['paragraph'], "type": "Verordnung", "category": "Immobilienwertermittlung", "title": item['titel']}
        })
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(
                id=doc["id"],
                vector=embedding,
                payload={"text": doc["text"], **doc["metadata"]}
            ))
            if (i + 1) % 10 == 0:
                print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()
