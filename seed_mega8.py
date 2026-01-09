#!/usr/bin/env python3
"""
Mega-Seeding Teil 8: 50+ Dokumente - Formulare, Formularerklärungen, Vertragstypen
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

# Formulierungshilfen Mieter
FORMULIERUNGEN_MIETER = [
    {"titel": "Musterformulierung: Mängelanzeige an Vermieter", "inhalt": "Betreff: Mängelanzeige - [Beschreibung des Mangels]\n\nSehr geehrte/r [Vermieter],\n\nHiermit zeige ich folgenden Mangel in der von mir gemieteten Wohnung [Adresse] an:\n\n[Detaillierte Beschreibung des Mangels mit Fotos im Anhang]\n\nIch fordere Sie auf, den Mangel bis zum [Frist: 14 Tage] zu beseitigen. Bis zur Beseitigung behalte ich mir vor, die Miete angemessen zu mindern.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Widerspruch gegen Betriebskostenabrechnung", "inhalt": "Betreff: Widerspruch gegen Betriebskostenabrechnung [Jahr]\n\nSehr geehrte/r [Vermieter],\n\nGegen die Betriebskostenabrechnung vom [Datum] für den Zeitraum [Jahr] widerspreche ich aus folgenden Gründen:\n\n1. [Grund 1, z.B. Nicht umlagefähige Kosten enthalten]\n2. [Grund 2, z.B. Falscher Verteilerschlüssel]\n\nBitte korrigieren Sie die Abrechnung entsprechend. Bis zur Klärung zahle ich die Nachforderung nur unter Vorbehalt.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Antrag auf Untervermietung", "inhalt": "Betreff: Antrag auf Genehmigung zur Teiluntervermietung\n\nSehr geehrte/r [Vermieter],\n\nIch bitte um Ihre Zustimmung zur Untervermietung eines Zimmers meiner Wohnung [Adresse] an [Name des Untermieters].\n\nGrund: [z.B. Berufliche Veränderung, Kostenteilung]\n\nDer Untermieter ist [kurze Beschreibung: Beruf, Alter]. Die Untervermietung soll ab [Datum] erfolgen. Anbei die Unterlagen des Untermieters.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Mietminderung ankündigen", "inhalt": "Betreff: Mietminderung wegen [Mangel]\n\nSehr geehrte/r [Vermieter],\n\nTrotz meiner Mängelanzeige vom [Datum] wurde der Mangel [Beschreibung] bis heute nicht behoben. Daher mindere ich die Miete ab dem [Datum] um [Prozentsatz] entsprechend der Beeinträchtigung des Mietgebrauchs.\n\nSobald der Mangel beseitigt ist, werde ich die volle Miete wieder entrichten.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Härtefall-Widerspruch bei Kündigung", "inhalt": "Betreff: Widerspruch gegen Kündigung wegen Härte gemäß § 574 BGB\n\nSehr geehrte/r [Vermieter],\n\nGegen Ihre Kündigung vom [Datum] widerspreche ich und berufe mich auf die Härteregelung des § 574 BGB.\n\nGründe:\n- [Hohes Alter, lange Mietdauer]\n- [Gesundheitliche Beeinträchtigungen]\n- [Keine zumutbare Ersatzwohnung verfügbar]\n\nIch bitte um Fortsetzung des Mietverhältnisses.\n\nMit freundlichen Grüßen"},
]

# Formulierungshilfen Vermieter
FORMULIERUNGEN_VERMIETER = [
    {"titel": "Musterformulierung: Eigenbedarfskündigung", "inhalt": "Betreff: Kündigung des Mietverhältnisses wegen Eigenbedarfs\n\nSehr geehrte/r [Mieter],\n\nHiermit kündige ich das Mietverhältnis über die Wohnung [Adresse] ordentlich zum [Datum, unter Beachtung der gesetzlichen Frist] wegen Eigenbedarfs.\n\nIch benötige die Wohnung für [Bedarfsperson: z.B. meine Tochter], weil [Begründung: z.B. sie hat eine Arbeitsstelle in der Nähe angenommen].\n\nIch weise auf Ihr Widerspruchsrecht nach § 574 BGB hin.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Abmahnung wegen Zahlungsverzug", "inhalt": "Betreff: Abmahnung wegen Zahlungsverzug\n\nSehr geehrte/r [Mieter],\n\nSie befinden sich mit der Mietzahlung für [Monat/e] in Höhe von [Betrag] EUR im Rückstand.\n\nIch fordere Sie auf, den offenen Betrag bis zum [Frist: 7-14 Tage] auf mein Konto zu überweisen. Sollte die Zahlung nicht fristgerecht erfolgen, behalte ich mir rechtliche Schritte, einschließlich der Kündigung des Mietverhältnisses, vor.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Mieterhöhung auf Vergleichsmiete", "inhalt": "Betreff: Mieterhöhung nach § 558 BGB\n\nSehr geehrte/r [Mieter],\n\nIch bitte um Ihre Zustimmung zur Erhöhung der Nettokaltmiete von derzeit [aktuell] EUR auf [neu] EUR ab dem [Datum, frühestens nach Ablauf von 15 Monaten].\n\nDie Erhöhung ist gerechtfertigt, da die ortsübliche Vergleichsmiete laut Mietspiegel [Wert] EUR/qm beträgt [Verweis auf Mietspiegel, Feld/Spalte].\n\nBitte teilen Sie mir Ihre Zustimmung bis zum [Frist] mit.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Modernisierungsankündigung", "inhalt": "Betreff: Ankündigung einer Modernisierungsmaßnahme nach § 555c BGB\n\nSehr geehrte/r [Mieter],\n\nIch kündige folgende Modernisierungsmaßnahme an:\n\nArt der Maßnahme: [z.B. Einbau neuer Fenster]\nVoraussichtlicher Beginn: [Datum]\nVoraussichtliche Dauer: [Wochen]\n\nDie Maßnahme führt zu einer nachhaltigen Energieeinsparung. Die voraussichtliche Mieterhöhung beträgt [Betrag] EUR monatlich.\n\nBitte teilen Sie mir bis zum [Datum] mit, ob Härtegründe vorliegen.\n\nMit freundlichen Grüßen"},
    {"titel": "Musterformulierung: Fristlose Kündigung wegen Zahlungsverzug", "inhalt": "Betreff: Außerordentliche fristlose Kündigung\n\nSehr geehrte/r [Mieter],\n\nSie befinden sich mit der Mietzahlung für mehr als zwei Monate in Höhe von insgesamt [Betrag] EUR in Verzug.\n\nHiermit kündige ich das Mietverhältnis über die Wohnung [Adresse] außerordentlich fristlos gemäß § 543 Abs. 2 Nr. 3 BGB.\n\nHilfsweise kündige ich ordentlich zum nächstmöglichen Termin.\n\nIch fordere Sie auf, die Wohnung bis zum [Datum, ca. 2 Wochen] zu räumen und an mich zu übergeben.\n\nMit freundlichen Grüßen"},
]

# Vertragsarten
VERTRAGSARTEN = [
    {"titel": "Mietvertragstypen: Unbefristeter Mietvertrag", "inhalt": "Der unbefristete Mietvertrag ist der Regelfall bei Wohnraum. Er kann nur mit gesetzlicher Frist und Kündigungsgrund (Vermieter) bzw. ohne Grund (Mieter) gekündigt werden. Kündigungsfristen: 3-9 Monate je nach Wohndauer. Der Mieter genießt vollen Kündigungsschutz."},
    {"titel": "Mietvertragstypen: Zeitmietvertrag", "inhalt": "Der Zeitmietvertrag endet automatisch nach Ablauf der vereinbarten Dauer, ohne dass eine Kündigung erforderlich ist. Er ist nur bei Vorliegen eines Befristungsgrundes zulässig: Eigenbedarf, wesentliche Baumaßnahmen oder Werkswohnung. Der Grund muss bei Vertragsschluss schriftlich genannt werden."},
    {"titel": "Mietvertragstypen: Staffelmietvertrag", "inhalt": "Im Staffelmietvertrag werden die Miete und zukünftige Erhöhungen bereits bei Vertragsschluss festgelegt. Die Staffeln müssen in Euro-Beträgen angegeben sein. Zwischen den Staffeln muss mindestens ein Jahr liegen. Andere Mieterhöhungen sind während der Staffelzeit ausgeschlossen."},
    {"titel": "Mietvertragstypen: Indexmietvertrag", "inhalt": "Die Indexmiete ist an den Verbraucherpreisindex gekoppelt. Ändert sich der Index, kann die Miete entsprechend angepasst werden. Die Anpassung muss schriftlich erklärt werden und ist frühestens nach einem Jahr möglich. Andere Mieterhöhungen sind ausgeschlossen."},
    {"titel": "Kaufvertragstypen: Notarieller Kaufvertrag Grundstück", "inhalt": "Der Kaufvertrag über ein Grundstück muss notariell beurkundet werden (§ 311b BGB). Er regelt: Kaufgegenstand, Kaufpreis, Fälligkeit, Gewährleistung, Besitzübergang. Die Eigentumsübertragung erfolgt durch Auflassung und Grundbucheintragung."},
    {"titel": "Kaufvertragstypen: Share Deal vs. Asset Deal", "inhalt": "Beim Share Deal werden die Anteile an einer Gesellschaft übertragen, die das Grundstück hält. Beim Asset Deal wird das Grundstück direkt verkauft. Share Deal: Vermeidung von Grunderwerbsteuer bei unter 90% der Anteile, aber komplexere Due Diligence. Asset Deal: Klare Verhältnisse, volle Grunderwerbsteuer."},
]

# Dienstbarkeiten
DIENSTBARKEITEN = [
    {"titel": "Grunddienstbarkeit: Begriff und Arten", "inhalt": "Die Grunddienstbarkeit (§ 1018 BGB) belastet ein Grundstück zugunsten des Eigentümers eines anderen Grundstücks. Arten: Benutzungsdienstbarkeit (Wegerecht, Leitungsrecht), Unterlassungsdienstbarkeit (Bauverbote), Ausschlussdienstbarkeit (Ausschluss von Immissionen). Sie wird im Grundbuch eingetragen."},
    {"titel": "Beschränkte persönliche Dienstbarkeit: Wohnungsrecht", "inhalt": "Die beschränkte persönliche Dienstbarkeit (§ 1090 BGB) steht einer bestimmten Person zu, nicht einem Grundstück. Das Wohnungsrecht berechtigt zur Nutzung eines Gebäudes als Wohnung. Es ist nicht übertragbar und erlischt mit dem Tod des Berechtigten. Unterschied zum Nießbrauch: Nur Wohnnutzung, keine Vermietung."},
    {"titel": "Reallast: Wiederkehrende Leistungen", "inhalt": "Die Reallast (§ 1105 BGB) verpflichtet den jeweiligen Eigentümer zu wiederkehrenden Leistungen (Geld, Naturalien, Dienste). Typisch: Altenteil bei Hofübergabe, Erbbauzins. Die Reallast wird im Grundbuch eingetragen und belastet jeden künftigen Eigentümer."},
    {"titel": "Nießbrauch: Umfassendes Nutzungsrecht", "inhalt": "Der Nießbrauch (§ 1030 BGB) berechtigt zur umfassenden Nutzung einer Sache. Der Nießbraucher darf die Früchte ziehen, also auch vermieten. Er trägt die laufenden Kosten (ordentliche Lasten). Der Eigentümer behält nur das nackte Eigentum. Erlöschen: Tod, Zeitablauf, Verzicht."},
    {"titel": "Vorkaufsrecht: Dinglich und obligatorisch", "inhalt": "Das dingliche Vorkaufsrecht (§ 1094 BGB) wird im Grundbuch eingetragen und wirkt gegen jeden Käufer. Das obligatorische Vorkaufsrecht bindet nur die Vertragsparteien. Bei Ausübung tritt der Vorkaufsberechtigte in den geschlossenen Kaufvertrag ein. Frist zur Ausübung: 2 Monate ab Mitteilung."},
]

# Verwaltung
IMMOBILIENVERWALTUNG = [
    {"titel": "Hausverwaltung: Aufgaben der Mietverwaltung", "inhalt": "Die Mietverwaltung umfasst: Mietersuche und -auswahl, Mietvertragsverwaltung, Mietinkasso und Mahnwesen, Betriebskostenabrechnung, Organisation von Instandhaltung, Kommunikation mit Mietern. Die Kosten sind nicht auf Mieter umlagefähig. Vergütung: 20-30 EUR/Einheit/Monat."},
    {"titel": "WEG-Verwaltung: Aufgaben und Bestellung", "inhalt": "Die WEG-Verwaltung wird von der Eigentümerversammlung bestellt (maximal 5 Jahre). Aufgaben: Beschlussausführung, Kontoführung, Wirtschaftsplan und Jahresabrechnung, Versammlungsladung, Vertretung der Gemeinschaft. Die Kosten sind Verwaltungskosten und werden im Hausgeld umgelegt."},
    {"titel": "Sondereigentumsverwaltung: Unterschied zur Mietverwaltung", "inhalt": "Die Sondereigentumsverwaltung kümmert sich um vermietete Eigentumswohnungen aus Sicht des Eigentümers. Sie umfasst die Mietverwaltung, aber nicht die WEG-Verwaltung. Bei vermieteten ETW hat der Eigentümer also ggf. zwei Verwalter: WEG-Verwalter + Mietverwalter."},
    {"titel": "Facility Management: Technisches und kaufmännisches FM", "inhalt": "Facility Management umfasst das Gebäudemanagement in seiner Gesamtheit. Technisches FM: Wartung, Instandhaltung, Betrieb der Gebäudetechnik. Kaufmännisches FM: Flächenmanagement, Vertragsmanagement, Kostenoptimierung. Bei größeren Gewerbeimmobilien üblich."},
]

# Mieterschutz
MIETERSCHUTZ = [
    {"titel": "Kündigungsschutz: Sozialklausel § 574 BGB", "inhalt": "Der Mieter kann einer Kündigung widersprechen, wenn die Beendigung des Mietverhältnisses eine Härte bedeuten würde, die auch unter Würdigung der Interessen des Vermieters nicht zu rechtfertigen ist. Härtegründe: Alter, Krankheit, Schwangerschaft, keine Ersatzwohnung. Das Gericht entscheidet über die Fortsetzung."},
    {"titel": "Kündigungsschutz: Sperrfrist nach Wohnungsumwandlung", "inhalt": "Wird Mietwohnraum in Wohnungseigentum umgewandelt, kann der neue Eigentümer erst nach Ablauf von 3 Jahren (in manchen Städten 10 Jahre) wegen Eigenbedarfs kündigen. Die Sperrfrist gilt ab Eintragung des neuen Eigentümers. Kündigungsgründe außer Eigenbedarf bleiben möglich."},
    {"titel": "Bestandsschutz: Übernahme bei Eigentümerwechsel", "inhalt": "Kauf bricht nicht Miete (§ 566 BGB). Der neue Eigentümer tritt in das bestehende Mietverhältnis ein. Alle Rechte und Pflichten gehen über, einschließlich der Kaution. Der Mieter muss den Eigentümerwechsel nicht akzeptieren, das Mietverhältnis besteht automatisch fort."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Formulierungen Mieter
    for item in FORMULIERUNGEN_MIETER:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Muster", "category": "Formulierung Mieter", "title": item['titel']}})
    
    # Formulierungen Vermieter
    for item in FORMULIERUNGEN_VERMIETER:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Muster", "category": "Formulierung Vermieter", "title": item['titel']}})
    
    # Vertragsarten
    for item in VERTRAGSARTEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Vertragsarten", "title": item['titel']}})
    
    # Dienstbarkeiten
    for item in DIENSTBARKEITEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Dienstbarkeiten", "title": item['titel']}})
    
    # Immobilienverwaltung
    for item in IMMOBILIENVERWALTUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Verwaltung", "title": item['titel']}})
    
    # Mieterschutz
    for item in MIETERSCHUTZ:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Mieterschutz", "title": item['titel']}})
    
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
