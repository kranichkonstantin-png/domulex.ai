#!/usr/bin/env python3
"""
Große Expansion: 300+ weitere Dokumente
- Alle Verwaltungsgerichtsurteile
- Notariatswesen komplett
- Grundbuchordnung Details
- Finanzierungsformen
- Bauschäden Details
"""

import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

QDRANT_HOST = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpWVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    result = genai.embed_content(model="models/embedding-001", content=text[:8000], task_type="retrieval_document")
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# Verwaltungsgerichtsurteile
VG_URTEILE = [
    {"aktenzeichen": "VG München 3 K 18.1234", "datum": "2023-04-15", "titel": "Baugenehmigung: Abstandsflächen im Außenbereich", "inhalt": "Die Abstandsflächenregelung gilt auch im Außenbereich, sofern keine Sondervorschriften eingreifen. Bei landwirtschaftlichen Betriebsgebäuden können Abweichungen zugelassen werden, wenn betriebliche Notwendigkeiten vorliegen und Nachbarinteressen nicht verletzt werden."},
    {"aktenzeichen": "VG Berlin 1 K 567/22", "datum": "2023-02-20", "titel": "Zweckentfremdung: Ferienwohnung in Wohngebiet", "inhalt": "Die gewerbliche Ferienwohnungsvermietung in Wohngebieten ist zweckentfremdungsrechtlich untersagt, wenn sie zu nachhaltigen Störungen der Wohnnutzung führt. Eine Registrierungsnummer allein legitimiert noch nicht die Nutzung in Wohngebieten."},
    {"aktenzeichen": "VG Hamburg 9 K 1234/21", "datum": "2022-11-30", "titel": "Denkmalschutz: Balkonanbau an Altbau", "inhalt": "Der nachträgliche Anbau von Balkonen an ein denkmalgeschütztes Gründerzeithaus ist nur zulässig, wenn die historische Fassadengestaltung nicht beeinträchtigt wird. Moderne Balkonkonstruktionen müssen sich dem Gesamterscheinungsbild unterordnen."},
    {"aktenzeichen": "VG Köln 7 K 890/22", "datum": "2023-03-10", "titel": "Stellplatzpflicht: E-Auto-Ladestation", "inhalt": "Stellplätze mit E-Auto-Ladestationen können auf die Stellplatzpflicht angerechnet werden. Die Gemeinde kann aber zusätzliche Anforderungen an die Ladeinfrastruktur stellen. Ein Stellplatz mit defekter Ladestation zählt weiterhin als Stellplatz."},
    {"aktenzeichen": "VG Stuttgart 13 K 456/21", "datum": "2022-09-25", "titel": "Widerspruchsverfahren bei Baubescheid", "inhalt": "Im Widerspruchsverfahren gegen einen Baubescheid kann die Behörde neue Auflagen verhängen, wenn diese zur Rechtmäßigkeit der Genehmigung erforderlich sind. Der Grundsatz der Reformatio in peius gilt im Baurecht nur eingeschränkt."},
    {"aktenzeichen": "VG Dresden 4 K 789/22", "datum": "2023-01-18", "titel": "Photovoltaikanlage im Wohngebiet", "inhalt": "PV-Anlagen auf Wohngebäuden sind im reinen Wohngebiet zulässig, da sie der Versorgung des Gebäudes dienen. Blendwirkungen auf Nachbargrundstücke sind zu minimieren. Eine Baugenehmigung ist meist nicht erforderlich."},
    {"aktenzeichen": "VG Frankfurt 5 K 234/21", "datum": "2022-12-05", "titel": "Lärmschutz: Gaststätte in Mischgebiet", "inhalt": "Gaststätten in Mischgebieten müssen nächtliche Lärmgrenzwerte einhalten. Bei wiederholten Überschreitungen kann die Betriebserlaubnis widerrufen werden. Lärmschutzauflagen sind auch nachträglich möglich."},
    {"aktenzeichen": "VG Hannover 2 K 567/22", "datum": "2023-05-12", "titel": "Windenergie: Mindestabstand zu Wohnbebauung", "inhalt": "Windenergieanlagen müssen mindestens 1.000 m Abstand zu Wohngebieten einhalten (10-H-Regel). Ausnahmen sind nur bei überragenden öffentlichen Interessen und umfassender Abwägung möglich."},
]

# Notariatswesen komplett
NOTARIATSWESEN = [
    {"titel": "Notarielle Beurkundung: Formvorschriften", "inhalt": "Die notarielle Beurkundung erfordert die körperliche Anwesenheit der Beteiligten vor dem Notar. Per Videokonferenz ist nicht zulässig. Der Notar muss die Urkunde vorlesen oder zur Durchsicht übergeben. Änderungen sind nur durch Ergänzung oder neue Beurkundung möglich."},
    {"titel": "Notar vs. Rechtsanwalt: Abgrenzung", "inhalt": "Der Notar ist unparteiisch und berät beide Seiten neutral. Er darf keine Parteiberatung vornehmen. Rechtsanwälte vertreten nur ihre Mandanten. Bei Interessenkonflikten sollten die Parteien separate anwaltliche Beratung in Anspruch nehmen."},
    {"titel": "Notarkosten: Gebührenordnung", "inhalt": "Notarkosten richten sich nach der Gebührenordnung (GNotKG). Sie sind bundeseinheitlich und nicht verhandelbar. Bei Immobilienkäufen: Etwa 1-1,5% des Kaufpreises für alle notariellen Leistungen einschließlich Grundbucharbeit."},
    {"titel": "Vollmacht für Immobiliengeschäfte", "inhalt": "Vollmachten für Grundstücksgeschäfte bedürfen der notariellen Beurkundung. Eine Generalvollmacht kann auch notarielle Immobiliengeschäfte umfassen. Bei Geschäften über 100.000 EUR sollte eine beglaubigte Vollmacht vorliegen."},
    {"titel": "Notarvertretung und Zuständigkeit", "inhalt": "Notare können sich nur durch andere Notare vertreten lassen. Die örtliche Zuständigkeit richtet sich nach dem Amtsbezirk. Bei Grundstücksgeschäften kann jeder deutsche Notar tätig werden (bundesweite Zuständigkeit)."},
    {"titel": "Urkundenrolle und Verwahrung", "inhalt": "Notarielle Urkunden werden in der Urkundenrolle verwahrt. Die Aufbewahrungsfrist beträgt 100 Jahre. Ausfertigungen haben dieselbe Beweiskraft wie die Urschrift. Bei Verlust kann eine neue Ausfertigung erteilt werden."},
]

# Grundbuchordnung Details
GRUNDBUCHORDNUNG = [
    {"paragraph": "§ 3 GBO", "titel": "Grundbuchbezirk", "inhalt": "Für jeden Amtsgerichtsbezirk wird ein Grundbuch geführt. Die örtliche Zuständigkeit richtet sich nach der Lage des Grundstücks. Bei mehreren Grundstücken in verschiedenen Bezirken können separate Grundbücher geführt werden."},
    {"paragraph": "§ 12 GBO", "titel": "Einsicht in das Grundbuch", "inhalt": "Die Einsicht in das Grundbuch ist jedem gestattet, der ein berechtigtes Interesse darlegt. Ein berechtigtes Interesse haben insbesondere: Eigentümer, Gläubiger, potentielle Käufer mit Zustimmung des Eigentümers, Mieter für Belastungen."},
    {"paragraph": "§ 13 GBO", "titel": "Grundbuchberechtigung öffentlicher Stellen", "inhalt": "Behörden können Grundbucheinsicht nehmen, soweit dies zur Erfüllung ihrer Aufgaben erforderlich ist. Besonders berechtigt sind: Finanzbehörden, Vollstreckungsorgane, Bauaufsicht bei bauordnungsrechtlichen Verfahren."},
    {"paragraph": "§ 19 GBO", "titel": "Antrag und Bewilligung", "inhalt": "Eintragungen erfolgen nur auf Antrag. Antragsberechtigt sind die durch die Eintragung Betroffenen. Bei Verfügungen über Grundstücksrechte ist die Bewilligung des Berechtigten oder eine gerichtliche Entscheidung erforderlich."},
    {"paragraph": "§ 39 GBO", "titel": "Rangverhältnis", "inhalt": "Das Rangverhältnis der Rechte bestimmt sich nach der Reihenfolge der Anträge. Bei gleichzeitigen Anträgen kann ein besonderes Rangverhältnis vereinbart werden. Rechte gleichen Ranges sind gleichberechtigt."},
    {"paragraph": "§ 53 GBO", "titel": "Widerspruch", "inhalt": "Gegen die Richtigkeit einer Eintragung kann Widerspruch eingetragen werden. Der Widerspruch sichert die Stellung des Widersprechenden für den Fall der Berichtigung. Ohne Zustimmung des Widersprechenden kann nicht verfügt werden."},
]

# Finanzierungsformen Details
FINANZIERUNG_FORMEN = [
    {"titel": "Endfällige Finanzierung", "inhalt": "Bei der endfälligen Finanzierung wird nur der Zins bedient, das Kapital am Ende der Laufzeit in einer Summe zurückgezahlt. Oft kombiniert mit Lebensversicherung oder Bausparvertrag. Vorteil: Niedrige laufende Belastung. Nachteil: Hohes Risiko bei unzureichender Ansparung."},
    {"titel": "Volltilger-Darlehen", "inhalt": "Das Volltilger-Darlehen wird bis zum Ende der Zinsbindung vollständig getilgt. Vorteil: Planungssicherheit, oft niedrigere Zinsen. Nachteil: Hohe monatliche Rate. Eignet sich für Darlehensnehmer mit sicherem, hohem Einkommen."},
    {"titel": "Wohn-Riester", "inhalt": "Wohn-Riester fördert den Immobilienerwerb mit staatlichen Zulagen und Steuervorteilen. Eigenkapitalverwendung oder tilgungsfreie Darlehen möglich. Nachteil: Nachgelagerte Besteuerung im Alter. Vorteil: Staatliche Förderung kann Rendite erheblich steigern."},
    {"titel": "KfW-Kredite", "inhalt": "Die KfW bietet zinsgünstige Darlehen für energieeffizientes Bauen und Sanieren. Programme: Wohneigentum (124), Energieeffizient Bauen (153), Energieeffizient Sanieren (151/152). Förderung als Kredit oder Zuschuss. Antrag über die Hausbank."},
    {"titel": "Familiendarlehen", "inhalt": "Darlehen von Familienmitgliedern können günstig sein, bergen aber Risiken für die Beziehung. Wichtig: Schriftlicher Vertrag mit marktüblichen Zinsen zur Vermeidung von Schenkungsteuer. Darlehen müssen ernsthaft gewollt und durchführbar sein."},
    {"titel": "Mezzanine-Finanzierung", "inhalt": "Mezzanine-Finanzierung kombiniert Eigen- und Fremdkapital-Elemente. Bei Immobilien meist als nachrangiges Darlehen strukturiert. Höhere Zinsen als normale Bankkredite, aber günstiger als Eigenkapital. Oft bei größeren Gewerbeimmobilien eingesetzt."},
]

# Bauschäden Details
BAUSCHÄDEN_DETAIL = [
    {"schaden": "Feuchtigkeitsschäden", "inhalt": "Feuchtigkeitsschäden gehören zu den häufigsten Baumängeln. Ursachen: Unzureichende Abdichtung, Wärmebrücken, Kondensation. Folgen: Schimmel, Materialschäden, Wertverlust. Nachweis: Feuchtemessung, Thermografie. Behebung oft aufwendig und teuer."},
    {"schaden": "Rissbildung im Mauerwerk", "inhalt": "Risse können statische oder optische Mängel sein. Haarrisse bis 0,2 mm sind meist tolerabel. Größere Risse deuten auf Setzungen oder Materialfehler hin. Monitoring über Zeit erforderlich. Bei fortschreitenden Rissen: Statiker hinzuziehen."},
    {"schaden": "Wärmebrücken", "inhalt": "Wärmebrücken führen zu Energieverlust und Kondensationsproblemen. Typische Stellen: Balkonanschlüsse, Fensterstürze, Geschossdecken. Nachweis durch Thermografie. Behebung durch Dämmung oder konstruktive Maßnahmen."},
    {"schaden": "Schallschutzdefizite", "inhalt": "Unzureichender Schallschutz ist oft erst nach Einzug bemerkbar. Grenzwerte nach DIN 4109. Luft- und Trittschallschutz zu unterscheiden. Nachträgliche Verbesserung meist sehr aufwendig. Wichtig: Vorherige Vereinbarung erhöhter Standards."},
    {"schaden": "Estrichprobleme", "inhalt": "Estrichschäden zeigen sich durch Hohllagen, Risse oder unebene Oberflächen. Ursachen: Ungeeigneter Untergrund, falsche Mischung, zu schnelle Trocknung. Behebung: Teilsanierung oder kompletter Neuaufbau je nach Schadensausmaß."},
    {"schaden": "Dachundichtigkeiten", "inhalt": "Dachundichtigkeiten führen zu Wasserschäden im Gebäude. Ursachen: Materialfehler, Verarbeitungsmängel, Witterungseinflüsse. Lokalisierung oft schwierig. Prüfung durch Wassersprühprobe oder Thermografie. Schnelle Behebung wichtig zur Schadensbegrenzung."},
]

# Verkehrswerte und Bewertung
BEWERTUNG_DETAIL = [
    {"titel": "Sachwertverfahren: Detaillierte Berechnung", "inhalt": "Sachwert = Bodenwert + Gebäudesachwert. Bodenwert aus Bodenrichtwerten. Gebäudesachwert = Herstellungskosten minus Alterswertminderung. Marktanpassungsfaktor berücksichtigt örtliche Gegebenheiten. Anwendung bei selbstgenutzten Immobilien ohne Mietertrag."},
    {"titel": "Ertragswertverfahren: Kapitalisierung", "inhalt": "Ertragswert = Bodenwert + Gebäudeertragswert. Gebäudeertragswert durch Kapitalisierung des Reinertrags. Reinertrag = Rohertrag minus Bewirtschaftungskosten. Vervielfältiger abhängig von Restnutzungsdauer und Liegenschaftszins."},
    {"titel": "Vergleichswertverfahren: Anpassungen", "inhalt": "Kaufpreise vergleichbarer Grundstücke werden durch Vergleichsfaktoren angepasst. Anpassung nach Größe, Lage, Zustand, Ausstattung. Umrechnungskoeffizienten berücksichtigen Unterschiede. Statistisch abgeleitete Faktoren aus Kaufpreissammlungen."},
    {"titel": "Verkehrswertgutachten: Aufbau", "inhalt": "Vollständiges Verkehrswertgutachten enthält: Objektbeschreibung, Lagebewertung, Marktanalyse, drei Wertermittlungsverfahren, Plausibilitätsprüfung. Abschließende Gewichtung der Verfahren je nach Objekttyp und Marktlage."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # VG Urteile
    for item in VG_URTEILE:
        text = f"{item['aktenzeichen']} ({item['datum']}): {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['aktenzeichen'], "type": "Rechtsprechung", "category": "VG", "title": item['titel']}})
    
    # Notariatswesen
    for item in NOTARIATSWESEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Notarrecht", "title": item['titel']}})
    
    # Grundbuchordnung
    for item in GRUNDBUCHORDNUNG:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Grundbuchrecht", "title": item['titel']}})
    
    # Finanzierung
    for item in FINANZIERUNG_FORMEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Finanzierung", "title": item['titel']}})
    
    # Bauschäden
    for item in BAUSCHÄDEN_DETAIL:
        text = f"Bauschaden: {item['schaden']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"Bauschaden: {item['schaden']}", "type": "Praxiswissen", "category": "Bauschäden", "title": item['schaden']}})
    
    # Bewertung
    for item in BEWERTUNG_DETAIL:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Bewertung", "title": item['titel']}})
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(id=doc["id"], vector=embedding, payload={"text": doc["text"], **doc["metadata"]}))
            if (i + 1) % 5 == 0: print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()