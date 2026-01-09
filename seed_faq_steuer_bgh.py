#!/usr/bin/env python3
"""
Massives Seeding: 200+ Dokumente
- Weitere BGH-Urteile
- Steuerrecht vertieft
- Bauordnungsrecht
- FAQ-Sammlung
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

# Steuerrecht vertieft
STEUERRECHT = [
    {"titel": "AfA für Gebäude - Abschreibungssätze", "inhalt": "Die lineare Abschreibung für Wohngebäude beträgt: Gebäude vor 1925: 2,5% (40 Jahre), Gebäude 1925-2022: 2% (50 Jahre), Gebäude ab 2023: 3% (33 Jahre). Bei Gewerbeimmobilien gilt 3% (33 Jahre). Degressive AfA ist für Neubauten ab 2023 mit 6% möglich."},
    {"titel": "Anschaffungsnahe Herstellungskosten § 6 Abs. 1 Nr. 1a EStG", "inhalt": "Übersteigen die Aufwendungen für Instandsetzung und Modernisierung innerhalb von 3 Jahren nach Anschaffung 15% der Gebäude-Anschaffungskosten (netto, ohne Grund und Boden), werden sie den Herstellungskosten zugerechnet und sind nur über die Nutzungsdauer abzuschreiben."},
    {"titel": "Grunderwerbsteuer - Steuersätze nach Bundesland", "inhalt": "Grunderwerbsteuer je Bundesland (Stand 2024): Bayern 3,5%, Sachsen 5,5%, Berlin 6%, Brandenburg 6,5%, Nordrhein-Westfalen 6,5%, Schleswig-Holstein 6,5%, Hamburg 5,5%, Bremen 5%, Niedersachsen 5%, Hessen 6%, Rheinland-Pfalz 5%, Saarland 6,5%, Baden-Württemberg 5%, Thüringen 5%, Sachsen-Anhalt 5%, Mecklenburg-Vorpommern 6%."},
    {"titel": "Spekulationsfrist § 23 EStG", "inhalt": "Private Veräußerungsgeschäfte bei Immobilien sind steuerpflichtig, wenn zwischen Anschaffung und Veräußerung weniger als 10 Jahre liegen. Ausnahmen: Eigennutzung im Jahr der Veräußerung und den beiden Vorjahren. Verluste können nur mit Gewinnen aus privaten Veräußerungsgeschäften verrechnet werden."},
    {"titel": "Vermietung an Angehörige - 66%-Grenze", "inhalt": "Bei Vermietung an nahe Angehörige zu weniger als 66% der ortsüblichen Miete werden Werbungskosten nur anteilig anerkannt. Bei mindestens 66% der Vergleichsmiete sind Werbungskosten voll abzugsfähig. Die Totalüberschussprognose muss positiv sein."},
    {"titel": "Erhaltungsaufwand vs. Herstellungskosten", "inhalt": "Erhaltungsaufwand (sofort abzugsfähig): Reparaturen, Ersatz von Teilen, Malerarbeiten. Herstellungskosten (über Nutzungsdauer): Erweiterung (mehr Fläche), wesentliche Verbesserung (Standardhebung), Erneuerung nach Verbrauch von mind. 3 Kernbereichen (Heizung, Sanitär, Elektro, Fenster)."},
    {"titel": "Denkmalschutz-AfA § 7i EStG", "inhalt": "Für Baudenkmale gilt: Herstellungskosten bei Eigennutzung 9% (8 Jahre), dann 7% (4 Jahre). Bei Vermietung 9% (8 Jahre), dann 7% (4 Jahre). Erhaltungsaufwand kann über 2-5 Jahre verteilt werden. Bescheinigung der Denkmalbehörde erforderlich."},
    {"titel": "Grundsteuerreform 2025", "inhalt": "Ab 2025 gilt die neue Grundsteuer. Bundesmodell: Berechnung nach Bodenwert und Gebäudefläche. Baden-Württemberg: Bodenwertmodell. Bayern: Flächenmodell. Hamburg/Niedersachsen: Flächen-Lage-Modell. Grundstückseigentümer mussten bis 31.01.2023 Feststellungserklärung abgeben."},
    {"titel": "Umsatzsteuer bei Vermietung § 4 Nr. 12 UStG", "inhalt": "Vermietung von Wohnraum ist umsatzsteuerfrei. Option zur Umsatzsteuerpflicht bei Gewerbevermietung möglich, wenn Mieter vorsteuerabzugsberechtigt. Vorteil: Vorsteuerabzug aus Baukosten. Nachteil: Umsatzsteuerpflicht bei Verkauf innerhalb von 10 Jahren."},
    {"titel": "Erbschaftsteuer - Freibeträge", "inhalt": "Freibeträge Erbschaftsteuer: Ehegatte 500.000 EUR, Kinder 400.000 EUR, Enkel 200.000 EUR, Eltern bei Erwerb 100.000 EUR, sonstige 20.000 EUR. Familienheim ist steuerfrei bei Übernahme durch Ehegatte oder Kind mit 10-jähriger Selbstnutzung."},
]

# FAQ-Sammlung Mietrecht
FAQ_MIETRECHT = [
    {"frage": "Wie hoch darf die Mietkaution sein?", "antwort": "Die Mietkaution darf maximal drei Nettokaltmieten betragen (§ 551 BGB). Der Mieter kann die Kaution in drei gleichen Monatsraten zahlen, beginnend mit der ersten Rate bei Mietbeginn. Der Vermieter muss die Kaution getrennt von seinem Vermögen anlegen."},
    {"frage": "Wann darf der Vermieter die Wohnung betreten?", "antwort": "Der Vermieter darf die Wohnung nur mit Zustimmung des Mieters betreten. Ausnahmen: Notfälle (Brand, Wasserrohrbruch), vereinbarte Besichtigungstermine bei Verkauf/Neuvermietung, notwendige Instandhaltungsarbeiten mit angemessener Vorankündigung (in der Regel 3-7 Tage)."},
    {"frage": "Wie lange ist die Kündigungsfrist für Mieter?", "antwort": "Die gesetzliche Kündigungsfrist für Mieter beträgt einheitlich 3 Monate zum Monatsende (§ 573c BGB). Die Kündigung muss spätestens am 3. Werktag eines Monats eingehen, damit sie zum Ende des übernächsten Monats wirksam wird."},
    {"frage": "Wann darf ich die Miete mindern?", "antwort": "Mietminderung ist zulässig bei erheblichen Mängeln, die die Gebrauchstauglichkeit beeinträchtigen (§ 536 BGB). Voraussetzung: Der Mangel muss dem Vermieter angezeigt werden. Die Minderungshöhe richtet sich nach der Schwere der Beeinträchtigung. Bei selbst verursachten Mängeln keine Minderung."},
    {"frage": "Sind Haustiere in der Mietwohnung erlaubt?", "antwort": "Kleintiere (Hamster, Fische, Vögel) dürfen ohne Erlaubnis gehalten werden. Hunde und Katzen: Der Vermieter muss im Einzelfall entscheiden, ein generelles Verbot ist unwirksam. Bei der Entscheidung sind Interessen aller Beteiligten abzuwägen."},
    {"frage": "Was sind Schönheitsreparaturen?", "antwort": "Schönheitsreparaturen umfassen: Tapezieren, Anstreichen von Wänden/Decken, Streichen von Heizkörpern, Innentüren, Fenstern innen. Starre Fristenklauseln sind unwirksam. Bei unrenoviert übernommener Wohnung schuldet der Mieter keine Schönheitsreparaturen."},
    {"frage": "Wie funktioniert die Mieterhöhung?", "antwort": "Mieterhöhung bis zur ortsüblichen Vergleichsmiete: Schriftliche Erklärung mit Begründung (Mietspiegel, Vergleichswohnungen), Einhaltung der 15-Monats-Frist seit letzter Erhöhung, Kappungsgrenze 20% (lokal 15%) in 3 Jahren, Zustimmungsfrist für Mieter bis Ende des übernächsten Monats."},
    {"frage": "Was ist bei der Nebenkostenabrechnung zu beachten?", "antwort": "Die Abrechnung muss innerhalb von 12 Monaten nach Ende des Abrechnungszeitraums zugehen. Sie muss den Abrechnungszeitraum, Gesamtkosten, Umlageschlüssel, Berechnung für die Wohnung und Vorauszahlungen ausweisen. Nur umlagefähige Kosten nach § 2 BetrKV."},
    {"frage": "Kann ich untervermieten?", "antwort": "Untervermietung erfordert grundsätzlich die Erlaubnis des Vermieters. Nach § 553 BGB muss der Vermieter die Erlaubnis erteilen, wenn ein berechtigtes Interesse besteht (z.B. wirtschaftliche Gründe) und keine wichtigen Gründe dagegen sprechen."},
    {"frage": "Wann kann mir wegen Eigenbedarf gekündigt werden?", "antwort": "Eigenbedarfskündigung ist möglich, wenn der Vermieter die Wohnung für sich, Familienangehörige oder Haushaltsangehörige benötigt. Die Gründe müssen konkret und nachvollziehbar sein. Es gelten die gesetzlichen Kündigungsfristen (3-9 Monate je nach Mietdauer)."},
]

# FAQ WEG
FAQ_WEG = [
    {"frage": "Wer bezahlt Reparaturen am Gemeinschaftseigentum?", "antwort": "Reparaturen am Gemeinschaftseigentum (tragende Wände, Dach, Fassade, Treppenhaus, Heizungsanlage) werden von allen Eigentümern nach Miteigentumsanteilen bezahlt. Die Kosten werden aus der Instandhaltungsrücklage oder durch Sonderumlage finanziert."},
    {"frage": "Was darf ich in meiner Eigentumswohnung ändern?", "antwort": "Im Sondereigentum (Wohnung innen) dürfen Sie Änderungen vornehmen, sofern das Gemeinschaftseigentum und andere Eigentümer nicht beeinträchtigt werden. Änderungen an Gemeinschaftseigentum (Fassade, Balkongeländer) bedürfen der Zustimmung der Eigentümerversammlung."},
    {"frage": "Wie wird bei der Eigentümerversammlung abgestimmt?", "antwort": "Grundsätzlich gilt das Kopfstimmenprinzip: jeder Eigentümer eine Stimme. Die Gemeinschaftsordnung kann abweichend das Wertprinzip (nach Miteigentumsanteilen) vorsehen. Beschlüsse werden mit einfacher Mehrheit der abgegebenen Stimmen gefasst."},
    {"frage": "Was ist die Instandhaltungsrücklage?", "antwort": "Die Instandhaltungsrücklage ist eine Rückstellung für zukünftige Reparaturen und Sanierungen am Gemeinschaftseigentum. Die Beiträge werden monatlich mit dem Hausgeld gezahlt. Empfohlen: 0,80-1,50 EUR/qm Wohnfläche monatlich, abhängig von Alter und Zustand."},
    {"frage": "Kann ich gegen einen WEG-Beschluss vorgehen?", "antwort": "Beschlüsse können innerhalb eines Monats beim Amtsgericht angefochten werden. Die Frist beginnt mit der Beschlussfassung. Gründe: Verstoß gegen Gesetz oder Vereinbarung, Ermessensfehler, Verfahrensfehler. Nicht angefochten Beschlüsse werden bestandskräftig."},
]

# FAQ Immobilienkauf
FAQ_KAUF = [
    {"frage": "Welche Nebenkosten fallen beim Immobilienkauf an?", "antwort": "Kaufnebenkosten: Grunderwerbsteuer (3,5-6,5% je Bundesland), Notar (ca. 1-1,5%), Grundbuch (ca. 0,5%), ggf. Makler (3,57-7,14% inkl. MwSt.). Insgesamt 8-15% des Kaufpreises. Diese Kosten müssen meist aus Eigenkapital finanziert werden."},
    {"frage": "Was ist eine Auflassungsvormerkung?", "antwort": "Die Auflassungsvormerkung sichert den Käufer vor Zwischenverfügungen des Verkäufers (z.B. Weiterverkauf an Dritte). Sie wird direkt nach Beurkundung im Grundbuch eingetragen. Nach Kaufpreiszahlung erfolgt die endgültige Eigentumsumschreibung."},
    {"frage": "Was bedeutet Gewährleistungsausschluss beim Hauskauf?", "antwort": "Bei Gebrauchsimmobilien wird oft ein Gewährleistungsausschluss vereinbart (Kauf wie besehen). Der Ausschluss gilt nicht bei arglistig verschwiegenen Mängeln oder Zusicherungen. Der Käufer sollte vor dem Kauf eine gründliche Prüfung durchführen."},
    {"frage": "Wann geht das Eigentum auf mich über?", "antwort": "Das Eigentum geht mit Eintragung im Grundbuch auf den Käufer über, nicht mit Beurkundung. Dies dauert mehrere Wochen bis Monate. Der Besitz (Nutzung, Lasten, Gefahr) geht in der Regel mit vollständiger Kaufpreiszahlung über."},
    {"frage": "Was prüft der Notar?", "antwort": "Der Notar prüft: Identität der Parteien, Grundbuchinhalt, Kaufvertragsentwurf, Genehmigungen (Vorkaufsrechte), belehrt über rechtliche Folgen. Er beurkundet den Vertrag, beantragt Vormerkung und Eigentumsumschreibung und überwacht die Kaufpreiszahlung."},
]

# Mehr BGH Urteile
BGH_WEITERE = [
    {"az": "VIII ZR 115/22", "datum": "2023-03-15", "titel": "Indexmiete - Anpassung bei Inflation", "inhalt": "Bei einer Indexmietvereinbarung darf die Miete nur in dem Maße erhöht werden, wie der Verbraucherpreisindex gestiegen ist. Die Erhöhungserklärung muss in Textform erfolgen und die Berechnung nachvollziehbar darlegen."},
    {"az": "VIII ZR 60/22", "datum": "2023-01-25", "titel": "Mieterhöhung - Begründung durch Sachverständigengutachten", "inhalt": "Ein Mieterhöhungsverlangen kann durch Sachverständigengutachten begründet werden. Das Gutachten muss den Anforderungen an ein Gerichtsgutachten entsprechen und die wesentlichen Wertermittlungsmerkmale enthalten."},
    {"az": "VIII ZR 187/21", "datum": "2022-07-20", "titel": "Betriebskosten - Vorauszahlungsanpassung", "inhalt": "Der Vermieter darf die Betriebskostenvorauszahlungen nach einer Abrechnung einseitig anpassen. Die Anpassung muss sich im Rahmen der zu erwartenden Kosten halten. Eine unangemessen hohe Erhöhung ist unwirksam."},
    {"az": "V ZR 75/22", "datum": "2023-02-17", "titel": "Nachbarrecht - Überhang von Bäumen", "inhalt": "Der Eigentümer eines Grundstücks kann überhängende Zweige des Nachbarn selbst abschneiden, wenn er dem Nachbarn erfolglos eine angemessene Frist zur Beseitigung gesetzt hat. Die Kosten trägt der Störer."},
    {"az": "V ZR 42/22", "datum": "2022-11-11", "titel": "Wegerecht - Grunddienstbarkeit", "inhalt": "Ein Wegerecht als Grunddienstbarkeit berechtigt zur Nutzung des dienenden Grundstücks zu Gehzwecken oder zur Durchfahrt. Die Art der Nutzung richtet sich nach der Eintragung und dem Inhalt der Bestellungsurkunde."},
    {"az": "V ZR 102/21", "datum": "2022-05-06", "titel": "Vorkaufsrecht - Ausübungsfrist", "inhalt": "Das Vorkaufsrecht muss innerhalb von zwei Monaten nach Mitteilung des Kaufvertrags ausgeübt werden. Die Frist beginnt erst mit vollständiger Information über den Vertragsinhalt. Bei unvollständiger Mitteilung läuft die Frist nicht."},
    {"az": "XII ZR 108/20", "datum": "2021-12-15", "titel": "Gewerbemietvertrag - AGB-Kontrolle", "inhalt": "Auch bei Gewerbemietverträgen unterliegen vorformulierte Vertragsklauseln der AGB-Kontrolle. Eine Klausel, die die Instandhaltung vollständig auf den Mieter überträgt, kann auch im Gewerbe unwirksam sein."},
    {"az": "VIII ZR 320/21", "datum": "2022-09-28", "titel": "Mietvertrag - Haustierhaltung", "inhalt": "Ein formularmäßiges generelles Verbot der Hunde- und Katzenhaltung ist unwirksam. Der Vermieter muss im Einzelfall prüfen und abwägen. Bei Störungen oder Gefährdung kann die Erlaubnis versagt werden."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Steuerrecht
    for item in STEUERRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Steuerrecht", "category": "Immobiliensteuer", "title": item['titel']}})
    
    # FAQ Mietrecht
    for item in FAQ_MIETRECHT:
        text = f"FAQ: {item['frage']}\n\nAntwort: {item['antwort']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": "FAQ Mietrecht", "type": "FAQ", "category": "Mietrecht", "title": item['frage']}})
    
    # FAQ WEG
    for item in FAQ_WEG:
        text = f"FAQ: {item['frage']}\n\nAntwort: {item['antwort']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": "FAQ WEG", "type": "FAQ", "category": "WEG", "title": item['frage']}})
    
    # FAQ Kauf
    for item in FAQ_KAUF:
        text = f"FAQ: {item['frage']}\n\nAntwort: {item['antwort']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": "FAQ Immobilienkauf", "type": "FAQ", "category": "Immobilienkauf", "title": item['frage']}})
    
    # BGH weitere
    for item in BGH_WEITERE:
        text = f"BGH {item['az']} vom {item['datum']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": f"BGH {item['az']}", "type": "Rechtsprechung", "category": "BGH", "court": "BGH", "date": item['datum'], "title": item['titel']}})
    
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
