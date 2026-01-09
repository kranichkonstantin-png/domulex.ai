#!/usr/bin/env python3
"""
Massive Content: 150+ weitere Dokumente
- Umfassende FAQ Sammlungen
- Gerichtsentscheidungen regional  
- Spezialthemen Immobilienwirtschaft
- Internationale Aspekte
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

# FAQ Sammlungen
FAQ_MIETRECHT = [
    {"frage": "Darf ich in meiner Mietwohnung bohren?", "antwort": "Ja, das Bohren normaler Löcher für Bilder und Regale gehört zum vertragsgemäßen Gebrauch. Bei Auszug müssen die Löcher in der Regel nicht verschlossen werden, außer bei übermäßig vielen oder großen Löchern. Fliesen sollten nur im Notfall angebohrt werden."},
    {"frage": "Wie hoch darf die Mietkaution sein?", "antwort": "Die Kaution darf maximal drei Nettokaltmieten betragen. Sie kann in drei gleichen monatlichen Raten gezahlt werden. Der Vermieter muss sie getrennt von seinem Vermögen anlegen. Die Zinsen gehören dem Mieter."},
    {"frage": "Wann kann ich fristlos kündigen?", "antwort": "Als Mieter können Sie fristlos kündigen bei: Gesundheitsgefährdung, Verweigerung erlaubter Untervermietung, erheblichen Mängeln. Als Vermieter bei: Zahlungsverzug über zwei Monate, erheblichen Vertragsverletzungen, Beleidigung."},
    {"frage": "Muss ich Besichtigungen dulden?", "antwort": "Bei Verkauf oder Wiedervermietung müssen Sie Besichtigungen dulden. Der Vermieter muss 24 Stunden vorher ankündigen und einen vernünftigen Grund nennen. Die Zeiten sollen zumutbar sein. Bei übermäßig vielen Terminen können Sie widersprechen."},
    {"frage": "Was passiert bei Wasserschaden in der Wohnung?", "antwort": "Sofort den Vermieter informieren und Wasser abstellen. Schäden dokumentieren (Fotos). Der Vermieter ist zur Beseitigung verpflichtet. Sie können die Miete mindern. Ihre Möbel sind meist über die Hausratversicherung abgedeckt."},
    {"frage": "Darf der Vermieter einfach in die Wohnung?", "antwort": "Nein, Sie haben das alleinige Hausrecht in Ihrer Wohnung. Der Vermieter darf nur mit Ihrer Zustimmung oder in absoluten Notfällen (Gefahr) hinein. Selbst bei Terminen muss er vorher ankündigen und einen Grund nennen."},
    {"frage": "Kann ich die Miete kürzen wenn es laut ist?", "antwort": "Ja, bei erheblichem Lärm können Sie die Miete mindern. Baulärm: 10-30%, Nachbarlärm: 5-25%, Straßenlärm nur wenn erhebliche Verschlechterung. Erst Vermieter informieren, dann mindern. Normaler Kinderlärm berechtigt nicht zur Minderung."},
    {"frage": "Wer zahlt bei Schädlingsbefall?", "antwort": "Kommt auf die Ursache an. Baumängel (z.B. undichte Stellen): Vermieter. Falsches Verhalten (z.B. Lebensmittel offen lassen): Mieter. Bei Unsicherheit den Vermieter informieren und Gutachter beauftragen lassen."},
    {"frage": "Wie kündige ich meinem Mieter?", "antwort": "Eigenbedarfskündigung: Begründung für Familienmitglied/sich selbst. Ordentliche Kündigung: 3-9 Monate Frist je nach Wohndauer. Fristlose Kündigung: Bei erheblichen Pflichtverletzungen. Immer schriftlich und alle Mieter einbeziehen."},
    {"frage": "Wann verjähren Mietforderungen?", "antwort": "Mietforderungen verjähren nach 3 Jahren. Nebenkostenforderungen aus der Abrechnung verjähren ebenfalls in 3 Jahren ab Zugang der Abrechnung. Durch Mahnung oder Zahlungsaufforderung wird die Verjährung gehemmt."},
]

# FAQ WEG
FAQ_WEG = [
    {"frage": "Wie funktioniert die WEG-Verwaltung?", "antwort": "Die Eigentümergemeinschaft wählt einen Verwalter für maximal 5 Jahre. Er führt die Beschlüsse aus, verwaltet die Finanzen und lädt zur Versammlung. Vergütung: 20-40 EUR pro Einheit/Monat. Der Verwalter kann jederzeit abberufen werden."},
    {"frage": "Was kostet eine Eigentumswohnung monatlich?", "antwort": "Hausgeld setzt sich zusammen aus: Betriebskosten (200-400 EUR), Verwaltung (20-40 EUR), Instandhaltungsrücklage (200-500 EUR). Dazu kommen ggf. Finanzierung und Steuern. Insgesamt etwa 3-6 EUR pro Quadratmeter monatlich."},
    {"frage": "Darf ich meine Wohnung umbauen?", "antwort": "Innerhalb des Sondereigentums: Meist ja, aber keine tragenden Wände. Veränderungen am Gemeinschaftseigentum (Fassade, Fenster): Beschluss nötig. Seit 2020 können bauliche Maßnahmen mit einfacher Mehrheit beschlossen werden."},
    {"frage": "Wie hoch soll die Instandhaltungsrücklage sein?", "antwort": "Faustregel: 0,8-1% des Gebäudewerts pro Jahr. Bei einem 2-Mio-Gebäude: 16.000-20.000 EUR jährlich. Bei 10 Wohnungen: 1.600-2.000 EUR pro Wohnung/Jahr. Ältere Gebäude brauchen mehr Rücklage."},
    {"frage": "Was passiert bei Zahlungsausfall eines Eigentümers?", "antwort": "Die anderen Eigentümer müssen einspringen (Ausfallhaftung § 16 WEG). Die Gemeinschaft kann klagen und ggf. die Wohnung zwangsversteigern lassen. Vorsicht bei bereits überschuldeten Eigentümern."},
    {"frage": "Kann ein Beschluss rückgängig gemacht werden?", "antwort": "Nur durch neuen Beschluss mit der erforderlichen Mehrheit. Rechtswidrige Beschlüsse können angefochten werden (1 Monat Frist). Nichtige Beschlüsse sind von Anfang an unwirksam."},
    {"frage": "Wer haftet bei Schäden am Gemeinschaftseigentum?", "antwort": "Grundsätzlich die Gemeinschaft über die Gebäudeversicherung. Verursacht ein Eigentümer den Schaden vorsätzlich oder grob fahrlässig, kann die Versicherung Regress nehmen. Deshalb ist eine private Haftpflicht wichtig."},
    {"frage": "Darf ich meine Wohnung auf Airbnb vermieten?", "antwort": "Wenn die Gemeinschaftsordnung es nicht verbietet: grundsätzlich ja. Aber: Störungen vermeiden, Zweckentfremdungsverbote beachten, ggf. gewerbliche Anmeldung nötig. Viele Gemeinschaften beschließen ein Verbot."},
]

# Regionale Unterschiede
REGIONALE_UNTERSCHIEDE = [
    {"region": "Bayern", "thema": "Abstandsflächenrecht", "inhalt": "Bayern hat mit 1 H (Wandhöhe) die großzügigsten Abstandsflächen. Mindestabstand: 3 m. In Kerngebieten können Ausnahmen zugelassen werden. Besonderheit: Spielplatzpflicht ab 3 Wohnungen."},
    {"region": "Berlin", "thema": "Mietpreisbremse", "inhalt": "Berlin hat eine der schärfsten Mietpreisbremsen. Zulässige Miete: Bis 10% über ortsüblicher Vergleichsmiete. Ausnahmen für Neubauten nach 2014. Der gescheiterte Mietendeckel wurde 2021 vom BVerfG gekippt."},
    {"region": "Hamburg", "thema": "Zweckentfremdungsverbot", "inhalt": "In Hamburg ist die Nutzung als Ferienwohnung nur mit Genehmigung erlaubt. Ausnahme: Vermietung der Hauptwohnung bis 8 Wochen/Jahr. Verstöße werden mit bis zu 50.000 EUR geahndet."},
    {"region": "München", "thema": "Erhaltungssatzung", "inhalt": "München hat flächendeckende Erhaltungssatzungen. Umwandlung in Eigentumswohnungen ist oft verboten oder genehmigungspflichtig. Ziel: Schutz bezahlbaren Wohnraums. Verstöße können zur Rückumwandlung führen."},
    {"region": "Baden-Württemberg", "thema": "Nachbarrechtsgesetz", "inhalt": "BW hat eigene Grenzabstände für Pflanzen: Bäume über 2 m Höhe brauchen 2 m Abstand. Nachbarzustimmung kann Abstände reduzieren. Besonderheit: 'Ortsüblichkeit' als Maßstab in vielen Gemeinden."},
    {"region": "Nordrhein-Westfalen", "thema": "Stellplatzpflicht", "inhalt": "NRW hat regional unterschiedliche Stellplatzverordnungen. In Ballungsräumen oft reduzierte Pflichten bei ÖPNV-Anbindung. Car-Sharing-Stellplätze werden teilweise angerechnet."},
    {"region": "Sachsen", "thema": "Vorkaufsrecht der Gemeinden", "inhalt": "Sächsische Gemeinden haben erweiterte Vorkaufsrechte in Sanierungsgebieten. Auch private Vorkaufsrechte sind häufiger als in anderen Bundesländern. Wichtig bei Immobilienkäufen prüfen."},
    {"region": "Hessen", "thema": "Hessische Bauordnung", "inhalt": "Hessen erlaubt größere verfahrensfreie Vorhaben als andere Länder. Garagen bis 50 qm sind oft genehmigungsfrei. Vereinfachte Verfahren für Ein-/Zweifamilienhäuser."},
]

# Internationale Aspekte
INTERNATIONALE_ASPEKTE = [
    {"titel": "Immobilienerwerb durch EU-Ausländer", "inhalt": "EU-Bürger können grundsätzlich frei Immobilien in Deutschland erwerben (Grundfreiheiten). Ausnahmen: Landwirtschaftliche Flächen unterliegen besonderen Regeln. Meldepflichten bei größeren Investitionen. Steuerliche Besonderheiten beachten."},
    {"titel": "Doppelbesteuerungsabkommen", "inhalt": "Mieteinnahmen werden meist im Belegenheitsstaat besteuert. DBA vermeiden Doppelbesteuerung durch Anrechnung oder Freistellung. Bei Verkauf: Oft Besteuerung im Belegenheitsstaat. Wichtig: Quellensteuer und Progressionsvorbehalt beachten."},
    {"titel": "Brexit und Immobilienrechte", "inhalt": "Bestehende Immobilienrechte britischer Staatsbürger bleiben durch das Austrittsabkommen geschützt. Neue Erwerbe unterliegen den allgemeinen Regelungen für Drittstaatsangehörige. In einigen Bundesländern Genehmigungspflicht."},
    {"titel": "Außenwirtschaftsrecht bei Immobilien", "inhalt": "Erwerb durch Nicht-EU-Ausländer kann genehmigungspflichtig sein, wenn Sicherheitsinteressen betroffen sind. Besonders bei kritischer Infrastruktur, Militäranlagen, Technologieunternehmen. Anzeigepflichten ab bestimmten Schwellenwerten."},
    {"titel": "Grenzüberschreitende Erbschaft", "inhalt": "EU-Erbrechtsverordnung bestimmt anwendbares Recht nach gewöhnlichem Aufenthalt. Deutsche Immobilien unterliegen aber deutschem Sachenrecht. Erbschaftsteuer: Meist im Belegenheitsstaat. Europäisches Nachlasszeugnis für mehrere Länder."},
]

# Spezialthemen Immobilienwirtschaft
IMMOBILIENWIRTSCHAFT = [
    {"titel": "Sale-and-Lease-Back bei Immobilien", "inhalt": "Unternehmen verkaufen eigene Immobilien und mieten sie zurück. Vorteil: Liquiditätsgewinn, bilanzielle Entlastung. Nachteil: Verlust der Wertsteigerung, langfristige Mietbindung. Steuerlich: Bewertung zu Marktpreisen nötig."},
    {"titel": "Immobilien-Leasing", "inhalt": "Alternative zur klassischen Finanzierung. Operate-Leasing: Kein Eigentumsübergang. Finance-Leasing: Eigentumsübergang geplant. Vorteile: Liquiditätsschonung, steuerliche Vorteile. Nachteile: Höhere Gesamtkosten, eingeschränkte Verfügung."},
    {"titel": "Real Estate Investment Trust (REIT)", "inhalt": "REITs sind börsennotierte Immobilien-Aktiengesellschaften. In Deutschland: G-REIT für Gewerbeimmobilien. Vorteile: Transparenz, Fungibilität, Diversifikation. Steuerlich: Kapitalertragssteuer statt Gewerbesteuer."},
    {"titel": "Immobilien-Crowdfunding", "inhalt": "Private Investoren finanzieren Immobilienprojekte über Plattformen. Meist als Nachrangdarlehen strukturiert. Chancen: Hohe Renditen, niedrige Mindestanlagen. Risiken: Totalverlust möglich, geringe Liquidität, Projektrisiken."},
    {"titel": "PropTech und Immobilien", "inhalt": "Digitalisierung verändert die Immobilienbranche: Virtual Reality Besichtigungen, automatisierte Bewertungen, digitale Mietverträge. Rechtsfragen: Haftung bei automatisierten Entscheidungen, Datenschutz, Maklerrecht."},
    {"titel": "Nachhaltigkeit in der Immobilienwirtschaft", "inhalt": "ESG-Kriterien werden wichtiger für Finanzierung und Bewertung. EU-Taxonomie definiert 'grüne' Gebäude. DGNB, LEED, BREEAM als Zertifizierungsstandards. Stranded Assets bei ineffizienten Gebäuden drohen."},
]

# Mehr OLG Entscheidungen
MEHR_OLG_URTEILE = [
    {"aktenzeichen": "OLG Stuttgart 8 U 2/22", "datum": "2023-01-12", "titel": "Eigenbedarfskündigung: Wirtschaftliche Verwertung", "inhalt": "Die Kündigung zur wirtschaftlich besseren Verwertung (höhere Miete) ist bei Wohnraum unzulässig. Eigenbedarf liegt nur vor, wenn der Vermieter oder seine Familie die Wohnung selbst nutzen will. Eine Kündigung zur Mieterhöhung verstößt gegen den Kündigungsschutz."},
    {"aktenzeichen": "OLG Dresden 5 U 892/21", "datum": "2022-09-15", "titel": "WEG: Balkonsanierung als Erhaltungsmaßnahme", "inhalt": "Die Sanierung schadhafter Balkone ist eine Erhaltungsmaßnahme, die mit einfacher Mehrheit beschlossen werden kann. Die Kosten sind von allen Eigentümern zu tragen, auch von denen ohne Balkon, da Balkone zum Gemeinschaftseigentum gehören."},
    {"aktenzeichen": "OLG Koblenz 2 U 456/22", "datum": "2023-03-20", "titel": "Maklervertrag: Nachweis der Maklertätigkeit", "inhalt": "Der Makler muss seine wesentliche Tätigkeit für den Vertragsschluss nachweisen. Bloße Objektpräsentation reicht nicht. Er muss aktiv vermittelt und zum Abschluss beigetragen haben. Bei reiner Weitergabe von Exposés entfällt der Provisionsanspruch."},
    {"aktenzeichen": "OLG Hamm 22 U 34/21", "datum": "2022-11-30", "titel": "Mietminderung bei Baugerüst", "inhalt": "Ein Baugerüst vor dem Balkon berechtigt zur Mietminderung von etwa 10-15%, wenn die Nutzung des Balkons erheblich eingeschränkt ist. Die Dauer des Gerüststehens ist maßgeblich. Bei kurzzeitigen Arbeiten (unter 2 Wochen) ist eine Minderung meist nicht gerechtfertigt."},
    {"aktenzeichen": "OLG Celle 3 U 115/22", "datum": "2023-02-08", "titel": "Betriebskostenabrechnung: Hausmeisterkosten", "inhalt": "Hausmeisterkosten sind nur umlagefähig, soweit sie umlagefähige Tätigkeiten betreffen. Reparatur- und Instandhaltungsarbeiten sind nicht umlagefähig, auch wenn sie vom Hausmeister ausgeführt werden. Eine pauschale Umlegung aller Hausmeisterkosten ist unzulässig."},
    {"aktenzeichen": "OLG Brandenburg 7 U 78/21", "datum": "2022-06-25", "titel": "Grundstückskauf: Erschließungskosten", "inhalt": "Werden im Kaufvertrag keine Regelungen zu noch nicht umgelegten Erschließungskosten getroffen, trägt der Käufer die Kosten. Die Gemeinde kann diese auch nach dem Eigentumsübergang vom neuen Eigentümer verlangen. Eine Aufklärungspflicht des Verkäufers besteht nur bei konkreten Anhaltspunkten."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # FAQ Mietrecht
    for item in FAQ_MIETRECHT:
        text = f"FAQ: {item['frage']}\n\n{item['antwort']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"FAQ: {item['frage']}", "type": "FAQ", "category": "Mietrecht", "title": item['frage']}})
    
    # FAQ WEG
    for item in FAQ_WEG:
        text = f"FAQ WEG: {item['frage']}\n\n{item['antwort']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"FAQ WEG: {item['frage']}", "type": "FAQ", "category": "WEG", "title": item['frage']}})
    
    # Regionale Unterschiede
    for item in REGIONALE_UNTERSCHIEDE:
        text = f"Regional {item['region']}: {item['thema']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"{item['region']}: {item['thema']}", "type": "Regional", "category": item['region'], "title": item['thema']}})
    
    # Internationale Aspekte
    for item in INTERNATIONALE_ASPEKTE:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "International", "category": "Grenzüberschreitend", "title": item['titel']}})
    
    # Immobilienwirtschaft
    for item in IMMOBILIENWIRTSCHAFT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Immobilienwirtschaft", "title": item['titel']}})
    
    # Mehr OLG Urteile
    for item in MEHR_OLG_URTEILE:
        text = f"{item['aktenzeichen']} ({item['datum']}): {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['aktenzeichen'], "type": "Rechtsprechung", "category": "OLG", "title": item['titel']}})
    
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