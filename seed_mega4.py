#!/usr/bin/env python3
"""
Mega-Seeding Teil 4: 80+ Dokumente
- Notarrecht und Grundbuchrecht
- Zwangsversteigerung
- Denkmalschutz
- Energierecht und Klimaschutz
- Mehr BGB Sachenrecht
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
    result = genai.embed_content(model="models/embedding-001", content=text[:8000], task_type="retrieval_document")
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# Notarrecht
NOTARRECHT = [
    {"titel": "Notarrecht: Aufgaben des Notars beim Immobilienkauf", "inhalt": "Der Notar ist bei Grundstückskaufverträgen zwingend vorgeschrieben (§ 311b BGB). Er entwirft den Vertrag, belehrt die Parteien neutral, beurkundet die Willenserklärungen und wickelt den Vollzug ab (Kaufpreisfälligkeit, Grundbuchantrag, Löschungsbewilligungen). Der Notar ist unparteiisch und zur Verschwiegenheit verpflichtet."},
    {"titel": "Notarrecht: Notaranderkonto", "inhalt": "Der Notar kann ein Anderkonto führen, auf das der Käufer den Kaufpreis einzahlt. Der Notar zahlt erst nach Eintragung der Auflassungsvormerkung und Freigabe aus. Das Notaranderkonto bietet Sicherheit, verursacht aber zusätzliche Kosten. Alternative: Direktzahlung nach Fälligkeitsmitteilung."},
    {"titel": "Notarrecht: Beurkundungspflicht", "inhalt": "Beurkundungspflichtig sind: Grundstückskaufverträge, Übertragung von GmbH-Anteilen (über 25%), Eheverträge, Erbverträge, Schenkungsversprechen. Die Beurkundung erfordert die Anwesenheit der Parteien oder ihrer Vertreter vor dem Notar. Eine nachträgliche Heilung durch Erfüllung ist bei Grundstücken möglich."},
    {"titel": "Notarrecht: Notarkosten Immobilienkauf", "inhalt": "Die Notarkosten betragen etwa 1-1,5% des Kaufpreises. Sie umfassen Beurkundung, Vollzugstätigkeiten, Grundbuchanträge. Die Kosten richten sich nach dem Gerichts- und Notarkostengesetz (GNotKG). Wer die Kosten trägt, wird im Vertrag geregelt (üblich: Käufer)."},
    {"titel": "Notarrecht: Auflassungsvormerkung", "inhalt": "Die Auflassungsvormerkung sichert den Anspruch des Käufers auf Eigentumsübertragung. Sie wird vom Notar beantragt und schützt vor zwischenzeitlichen Verfügungen (Verkauf an Dritte, Belastungen). Nach Eintragung kann der Kaufpreis sicher gezahlt werden."},
]

# Grundbuchrecht
GRUNDBUCHRECHT = [
    {"titel": "Grundbuchrecht: Aufbau des Grundbuchs", "inhalt": "Das Grundbuch besteht aus dem Bestandsverzeichnis (Flurstücke), Abteilung I (Eigentümer), Abteilung II (Lasten und Beschränkungen wie Wegerechte, Wohnungsrechte, Nießbrauch) und Abteilung III (Grundpfandrechte: Hypotheken, Grundschulden). Jedes Grundstück hat ein eigenes Grundbuchblatt."},
    {"titel": "Grundbuchrecht: Grundbucheinsicht", "inhalt": "Jeder mit berechtigtem Interesse kann das Grundbuch einsehen (§ 12 GBO). Berechtigtes Interesse haben: potenzielle Käufer, Gläubiger, Mieter für Abteilung II. Der Eigentümer muss nicht zustimmen. Der Antrag erfolgt beim Grundbuchamt oder online über das Grundbuchportal (in einigen Bundesländern)."},
    {"titel": "Grundbuchrecht: Eintragungsprinzip", "inhalt": "Rechtsänderungen an Grundstücken werden erst mit der Eintragung im Grundbuch wirksam (§ 873 BGB). Ausnahmen: Erbschaft (Eintragung nur deklaratorisch), Zuschlag in der Zwangsversteigerung. Das Grundbuch genießt öffentlichen Glauben (§ 892 BGB)."},
    {"titel": "Grundbuchrecht: Rangfolge der Rechte", "inhalt": "Die Rangfolge richtet sich nach dem Datum der Eintragung. Ältere Rechte haben Vorrang. Bei Zwangsversteigerung werden Rechte nach Rangfolge befriedigt. Die Rangfolge kann durch Rangrücktritt oder Rangvorbehalt geändert werden."},
    {"titel": "Grundbuchrecht: Grundschuld vs. Hypothek", "inhalt": "Die Grundschuld ist nicht an eine bestimmte Forderung gebunden (abstrakt). Die Hypothek ist akzessorisch zur gesicherten Forderung. Bei Tilgung des Darlehens erlischt die Hypothek, die Grundschuld besteht fort. In der Praxis wird fast nur noch die Grundschuld verwendet."},
    {"titel": "Grundbuchrecht: Löschung einer Grundschuld", "inhalt": "Nach Rückzahlung des Darlehens kann der Eigentümer die Löschung der Grundschuld verlangen. Erforderlich: Löschungsbewilligung der Bank (in notarieller Form oder beglaubigt), Grundbuchantrag. Die Löschung kann sinnvoll verzögert werden (Grundschuld als Sicherungsreserve)."},
    {"titel": "Grundbuchrecht: Berichtigung des Grundbuchs", "inhalt": "Stimmt das Grundbuch nicht mit der wirklichen Rechtslage überein, kann der Berechtigte Berichtigung verlangen (§ 894 BGB). Die Berichtigung erfolgt auf Antrag mit Bewilligung des Betroffenen oder aufgrund eines Gerichtsurteils. Verjährung des Anspruchs: 30 Jahre."},
]

# Zwangsversteigerung
ZWANGSVERSTEIGERUNG = [
    {"titel": "Zwangsversteigerung: Ablauf des Verfahrens", "inhalt": "Die Zwangsversteigerung wird auf Antrag eines Gläubigers angeordnet. Das Amtsgericht bestimmt den Verkehrswert durch Gutachten. Im Versteigerungstermin werden Gebote abgegeben. Der Zuschlag erfolgt an den Meistbietenden, wenn die Mindestgebote erreicht werden."},
    {"titel": "Zwangsversteigerung: Mindestgebote", "inhalt": "Im ersten Termin muss das Gebot mindestens 5/10 des Verkehrswerts erreichen. Im zweiten Termin gibt es keine Mindestgrenze mehr. Der betreibende Gläubiger kann aber Einstellung beantragen. Erreicht das Gebot nicht 7/10, kann der Gläubiger die Versagung des Zuschlags verlangen."},
    {"titel": "Zwangsversteigerung: Sicherheitsleistung", "inhalt": "Bieter müssen 10% des Verkehrswerts als Sicherheit nachweisen (Bankbestätigung oder Verrechnungsscheck). Die Sicherheit wird vor der Gebotsabgabe geprüft. Ohne Sicherheitsnachweis wird das Gebot zurückgewiesen."},
    {"titel": "Zwangsversteigerung: Zuschlag und Verteilung", "inhalt": "Mit dem Zuschlag erwirbt der Ersteher das Eigentum. Er muss den Versteigerungserlös zahlen. Der Erlös wird nach Rangfolge auf die Gläubiger verteilt. Nicht befriedigte Forderungen bleiben bestehen. Im Grundbuch eingetragene Rechte können erlöschen (bestrangiges Recht)."},
    {"titel": "Zwangsversteigerung: Teilungsversteigerung", "inhalt": "Bei Miteigentum kann jeder Miteigentümer die Teilungsversteigerung beantragen, um die Gemeinschaft aufzulösen. Sie dient nicht der Gläubigerbefriedigung, sondern der Vermögensauseinandersetzung. Jeder Miteigentümer kann mitbieten."},
    {"titel": "Zwangsversteigerung: Räumung durch Ersteher", "inhalt": "Der Zuschlag enthält einen Vollstreckungstitel gegen den Schuldner auf Räumung. Der Ersteher kann unmittelbar die Zwangsräumung betreiben. Mieter haben Kündigungsschutz, Eigenbedarf kann aber geltend gemacht werden. Bei mietfreiem Eigenbedarf: Kündigung mit 3 Monaten Frist."},
]

# Denkmalschutz
DENKMALSCHUTZ = [
    {"titel": "Denkmalschutz: Genehmigungspflichten", "inhalt": "Wer ein Baudenkmal verändern, in der Umgebung bauen oder abreißen will, braucht eine denkmalrechtliche Genehmigung. Die Genehmigungspflicht gilt auch für Innenräume. Zuständig ist die untere Denkmalschutzbehörde. Verstöße können als Ordnungswidrigkeit geahndet werden."},
    {"titel": "Denkmalschutz: Steuerliche Förderung", "inhalt": "Sanierungsaufwendungen für Baudenkmäler können steuerlich abgesetzt werden. Vermieter: 9% über 8 Jahre, dann 7% über 4 Jahre (§ 7i EStG). Eigennutzer: 9% über 10 Jahre (§ 10f EStG). Voraussetzung: Bescheinigung der Denkmalbehörde vor Baubeginn."},
    {"titel": "Denkmalschutz: Erhaltungspflicht", "inhalt": "Eigentümer von Baudenkmälern sind zur Erhaltung verpflichtet, soweit dies wirtschaftlich zumutbar ist. Die Zumutbarkeit richtet sich nach den Erträgen und den Möglichkeiten, Fördermittel zu erhalten. Bei Unzumutbarkeit: Entschädigung oder Übernahme durch die öffentliche Hand möglich."},
    {"titel": "Denkmalschutz: Veräußerung von Baudenkmälern", "inhalt": "In einigen Bundesländern besteht ein Vorkaufsrecht der Gemeinde bei Verkauf von Baudenkmälern. Die Veräußerung kann anzeigepflichtig sein. Die Denkmaleigenschaft geht auf den Erwerber über. Keine Enthaftung von Erhaltungspflichten durch Verkauf."},
]

# Energierecht und Klimaschutz
ENERGIERECHT = [
    {"titel": "Gebäudeenergiegesetz (GEG): Überblick", "inhalt": "Das GEG regelt die energetischen Anforderungen an Gebäude. Es enthält Anforderungen für Neubauten und Bestand. Bei Neubauten: Primärenergiebedarf und Transmissionswärmeverlust begrenzt. Bei Bestandsgebäuden: Nachrüstpflichten bei wesentlichen Änderungen."},
    {"titel": "GEG: Energieausweis", "inhalt": "Bei Verkauf oder Vermietung muss der Eigentümer einen gültigen Energieausweis vorlegen. Es gibt den Bedarfsausweis (Berechnung) und den Verbrauchsausweis (tatsächlicher Verbrauch). Die Kennwerte müssen in Immobilienanzeigen angegeben werden. Bußgeld bei Verstößen: bis 15.000 EUR."},
    {"titel": "GEG: Heizungsaustausch und 65%-Regel", "inhalt": "Ab 2024 müssen neu eingebaute Heizungen 65% erneuerbare Energien nutzen. Ausnahmen: Übergangsfristen nach Gemeindevorgaben. Bei Havarie: Kurzfristige Übergangslösung möglich. Bestandsheizungen haben Bestandsschutz, können aber Austauschpflicht auslösen (Öl/Gas über 30 Jahre)."},
    {"titel": "GEG: Nachrüstpflichten im Bestand", "inhalt": "Im Bestand bestehen Nachrüstpflichten: Dämmung von Heizungs- und Warmwasserleitungen in unbeheizten Räumen, Dämmung der obersten Geschossdecke bei nicht begehbaren Dachräumen. Ausnahme: Wohngebäude mit max. 2 Wohnungen, wenn Eigentümer selbst darin wohnt."},
    {"titel": "Solarenergie: Solarpflicht der Länder", "inhalt": "Mehrere Bundesländer haben eine Solarpflicht eingeführt (z.B. Baden-Württemberg, Hamburg, Berlin). Sie gilt für Neubauten und/oder Dachsanierungen. Die Anforderungen variieren: Mindestfläche, Mindestleistung, Befreiungsmöglichkeiten bei Unwirtschaftlichkeit."},
    {"titel": "E-Mobilität: Ladeinfrastruktur in Gebäuden", "inhalt": "Das GEIG (Gebäude-Elektromobilitätsinfrastruktur-Gesetz) regelt die Pflicht zur Ladeinfrastruktur. Bei Neubauten mit mehr als 5 Stellplätzen: Leerrohre für jeden Stellplatz. Bei Nichtwohngebäuden: mindestens ein Ladepunkt ab 20 Stellplätzen. Bestandsgebäude: ab 2025 Nachrüstpflicht."},
]

# Mehr BGB Sachenrecht
BGB_SACHENRECHT = [
    {"paragraph": "§ 873 BGB", "titel": "Erwerb durch Einigung und Eintragung", "inhalt": "Zur Übertragung des Eigentums an einem Grundstück, zur Belastung eines Grundstücks mit einem Recht sowie zur Übertragung oder Belastung eines solchen Rechts ist die Einigung des Berechtigten und des anderen Teils über den Eintritt der Rechtsänderung und die Eintragung der Rechtsänderung in das Grundbuch erforderlich."},
    {"paragraph": "§ 883 BGB", "titel": "Vormerkung", "inhalt": "Zur Sicherung des Anspruchs auf Einräumung oder Aufhebung eines Rechts an einem Grundstück oder an einem das Grundstück belastenden Recht oder auf Änderung des Inhalts oder des Rangs eines solchen Rechts kann eine Vormerkung in das Grundbuch eingetragen werden."},
    {"paragraph": "§ 892 BGB", "titel": "Öffentlicher Glaube des Grundbuchs", "inhalt": "Zugunsten desjenigen, welcher ein Recht an einem Grundstück oder ein Recht an einem solchen Recht durch Rechtsgeschäft erwirbt, gilt der Inhalt des Grundbuchs als richtig, es sei denn, dass ein Widerspruch gegen die Richtigkeit eingetragen oder die Unrichtigkeit dem Erwerber bekannt ist."},
    {"paragraph": "§ 925 BGB", "titel": "Auflassung", "inhalt": "Die zur Übertragung des Eigentums an einem Grundstück nach § 873 erforderliche Einigung des Veräußerers und des Erwerbers (Auflassung) muss bei gleichzeitiger Anwesenheit beider Teile vor einer zuständigen Stelle erklärt werden. Die Auflassung kann nicht unter einer Bedingung oder Zeitbestimmung erfolgen."},
    {"paragraph": "§ 929 BGB", "titel": "Einigung und Übergabe beweglicher Sachen", "inhalt": "Zur Übertragung des Eigentums an einer beweglichen Sache ist erforderlich, dass der Eigentümer die Sache dem Erwerber übergibt und beide darüber einig sind, dass das Eigentum übergehen soll. Ist der Erwerber im Besitz der Sache, so genügt die Einigung über den Eigentumsübergang."},
    {"paragraph": "§ 932 BGB", "titel": "Gutgläubiger Erwerb vom Nichtberechtigten", "inhalt": "Durch eine nach § 929 erfolgte Veräußerung wird der Erwerber auch dann Eigentümer, wenn die Sache nicht dem Veräußerer gehört, es sei denn, dass er zu der Zeit, zu der er nach diesen Vorschriften das Eigentum erwerben würde, nicht in gutem Glauben ist. Der Erwerber ist nicht in gutem Glauben, wenn ihm bekannt oder grob fahrlässig unbekannt ist, dass die Sache nicht dem Veräußerer gehört."},
    {"paragraph": "§ 985 BGB", "titel": "Herausgabeanspruch", "inhalt": "Der Eigentümer kann von dem Besitzer die Herausgabe der Sache verlangen. Der Herausgabeanspruch ist der zentrale Vindikationsanspruch des Eigentümers gegen den unrechtmäßigen Besitzer."},
    {"paragraph": "§ 1004 BGB", "titel": "Beseitigungs- und Unterlassungsanspruch", "inhalt": "Wird das Eigentum in anderer Weise als durch Entziehung oder Vorenthaltung des Besitzes beeinträchtigt, so kann der Eigentümer von dem Störer die Beseitigung der Beeinträchtigung verlangen. Sind weitere Beeinträchtigungen zu besorgen, so kann der Eigentümer auf Unterlassung klagen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Notarrecht
    for item in NOTARRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Notarrecht", "title": item['titel']}})
    
    # Grundbuchrecht
    for item in GRUNDBUCHRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Grundbuchrecht", "title": item['titel']}})
    
    # Zwangsversteigerung
    for item in ZWANGSVERSTEIGERUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Zwangsversteigerung", "title": item['titel']}})
    
    # Denkmalschutz
    for item in DENKMALSCHUTZ:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Denkmalschutz", "title": item['titel']}})
    
    # Energierecht
    for item in ENERGIERECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Energierecht", "title": item['titel']}})
    
    # BGB Sachenrecht
    for item in BGB_SACHENRECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Sachenrecht", "title": item['titel']}})
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(id=doc["id"], vector=embedding, payload={"text": doc["text"], **doc["metadata"]}))
            if (i + 1) % 10 == 0: print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()
