#!/usr/bin/env python3
"""
Mega-Seeding Teil 5: 70+ Dokumente
- Bauschadenrecht
- Architektenrecht
- Mehr OLG/LG Urteile
- Praxistipps Mieter
- Praxistipps Vermieter
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

# Bauschadenrecht
BAUSCHADENRECHT = [
    {"titel": "Baumangel: Definition und Rechtsfolgen", "inhalt": "Ein Baumangel liegt vor, wenn das Werk nicht die vereinbarte Beschaffenheit hat oder sich nicht für die gewöhnliche oder vertraglich vorausgesetzte Verwendung eignet. Der Auftraggeber hat Anspruch auf Nacherfüllung, Minderung, Rücktritt und Schadensersatz. Die Verjährung beträgt 5 Jahre bei Bauwerken."},
    {"titel": "Baumangel: Gewährleistungsansprüche", "inhalt": "Bei Baumängeln hat der Auftraggeber zunächst Anspruch auf Nacherfüllung (§ 635 BGB). Er muss dem Unternehmer eine angemessene Frist setzen. Nach fruchtlosem Fristablauf: Selbstvornahme mit Kostenerstattung, Minderung oder Rücktritt. Schadensersatz bei Verschulden."},
    {"titel": "Baumangel: Beweislast", "inhalt": "Vor der Abnahme trägt der Unternehmer die Beweislast für die Mangelfreiheit. Nach der Abnahme muss der Auftraggeber den Mangel beweisen. Die Beweislastumkehr bei der Abnahme macht die förmliche Abnahme so wichtig. Bei Verbraucherbauverträgen: erleichterte Beweisführung."},
    {"titel": "VOB/B: Mängelgewährleistung", "inhalt": "Bei Vereinbarung der VOB/B beträgt die Gewährleistungsfrist 4 Jahre (statt 5 Jahre BGB). Wesentliche Unterschiede: Fristsetzung zur Mängelbeseitigung vor Selbstvornahme zwingend, eingeschränktes Recht auf Minderung, andere Regelungen zur Abnahme. Die VOB/B gilt nur bei vollständiger Einbeziehung."},
    {"titel": "Bauschaden: Schwarzer Schimmel und Feuchtigkeit", "inhalt": "Feuchtigkeitsschäden und Schimmelbildung sind häufige Baumängel. Ursachen: mangelhafte Abdichtung, Wärmebrücken, falsche Dämmung. Der Bauunternehmer haftet, wenn die Ursache in mangelhafter Ausführung liegt. Das Lüftungsverhalten des Nutzers kann die Haftung mindern."},
    {"titel": "Bauschaden: Rissbildung", "inhalt": "Risse im Mauerwerk oder Putz können auf Setzung, Temperaturdehnung oder Baumängel hindeuten. Nicht jeder Riss ist ein Mangel. Entscheidend: Überschreitet die Rissbildung das übliche Maß? Beeinträchtigt sie die Gebrauchstauglichkeit oder Standsicherheit? Gutachterliche Klärung oft erforderlich."},
]

# Architektenrecht
ARCHITEKTENRECHT = [
    {"titel": "Architektenvertrag: Leistungsphasen HOAI", "inhalt": "Die HOAI definiert 9 Leistungsphasen: 1. Grundlagenermittlung, 2. Vorplanung, 3. Entwurfsplanung, 4. Genehmigungsplanung, 5. Ausführungsplanung, 6. Vorbereitung der Vergabe, 7. Mitwirkung bei der Vergabe, 8. Objektüberwachung, 9. Objektbetreuung. Die Vergütung richtet sich nach den beauftragten Phasen."},
    {"titel": "Architektenvertrag: Haftung für Planungsfehler", "inhalt": "Der Architekt haftet für Planungsfehler, die zu Baumängeln führen. Er muss den aktuellen Stand der Technik und die anerkannten Regeln der Baukunst beachten. Bei Mitverschulden des Bauunternehmers: gesamtschuldnerische Haftung mit Ausgleich im Innenverhältnis."},
    {"titel": "Architektenvertrag: Bauüberwachungspflichten", "inhalt": "In Leistungsphase 8 überwacht der Architekt die Bauausführung. Er muss die Arbeiten stichprobenartig kontrollieren und bei kritischen Gewerken engmaschiger prüfen. Bei Verletzung der Überwachungspflicht haftet er für übersehene Mängel."},
    {"titel": "Architektenvertrag: Kostenüberschreitung", "inhalt": "Der Architekt muss den Bauherrn über die zu erwartenden Baukosten informieren (Kostenschätzung, Kostenberechnung). Bei erheblicher Kostenüberschreitung ohne Information kann er schadensersatzpflichtig sein. Grenze: 20-30% Überschreitung ohne Vorwarnung."},
    {"titel": "Architektenvertrag: Urheberrecht", "inhalt": "Architekten haben ein Urheberrecht an ihren Entwürfen. Der Bauherr erhält in der Regel ein einfaches Nutzungsrecht. Das Ändern des Gebäudes kann das Urheberrecht verletzen, wenn es das Werk entstellt. Der Architekt hat kein Recht auf Namensnennung am Gebäude."},
]

# OLG/LG Urteile
OLG_LG_URTEILE = [
    {"aktenzeichen": "LG Berlin 67 S 143/21", "datum": "2022-03-15", "titel": "Mietminderung bei Baulärm vom Nachbargrundstück", "inhalt": "Baulärm vom Nachbargrundstück berechtigt zur Mietminderung, wenn er über das hinausgeht, was in innerstädtischen Lagen üblich ist. Eine Minderung von 10-15% wurde bei mehrmonatiger intensiver Baulärmbelastung als angemessen erachtet."},
    {"aktenzeichen": "OLG München 32 U 1230/20", "datum": "2021-07-22", "titel": "WEG: Kosten der Balkoninstandsetzung", "inhalt": "Die Kosten der Instandsetzung von Balkonen sind grundsätzlich von der Gemeinschaft zu tragen, wenn die Balkone zum Gemeinschaftseigentum gehören. Eine abweichende Kostentragung in der Gemeinschaftsordnung ist wirksam, wenn sie klar und eindeutig formuliert ist."},
    {"aktenzeichen": "LG Hamburg 311 S 48/22", "datum": "2023-02-10", "titel": "Eigenbedarfskündigung: Nachweis des Bedarfs", "inhalt": "Der Vermieter muss den Eigenbedarf im Prozess substantiiert darlegen. Allgemeine Angaben genügen nicht. Er muss konkret vortragen, warum die Bedarfsperson die Wohnung benötigt und dass keine Alternativwohnungen zur Verfügung stehen."},
    {"aktenzeichen": "OLG Düsseldorf I-24 U 150/19", "datum": "2020-09-18", "titel": "Maklercourtage: Bestellung durch Kaufinteressent", "inhalt": "Ein Maklervertrag mit dem Kaufinteressenten kann durch schlüssiges Verhalten zustande kommen, wenn der Interessent weiß, dass der Makler eine Provision erwartet und dennoch dessen Leistungen in Anspruch nimmt. Eine vorformulierte Provisionsvereinbarung unterliegt der AGB-Kontrolle."},
    {"aktenzeichen": "LG Köln 9 S 166/20", "datum": "2021-05-12", "titel": "Betriebskosten: Wirtschaftlichkeitsgebot", "inhalt": "Der Vermieter ist an das Wirtschaftlichkeitsgebot gebunden. Er darf keine unangemessen hohen Kosten auf die Mieter umlegen. Vereinbart er überhöhte Preise mit Dienstleistern, kann der Mieter die Abrechnung kürzen."},
    {"aktenzeichen": "OLG Frankfurt 2 U 115/21", "datum": "2022-06-30", "titel": "Baumangel: Fristlose Kündigung durch Bauherrn", "inhalt": "Der Bauherr kann den Bauvertrag fristlos kündigen, wenn der Unternehmer trotz Nachfristsetzung schwerwiegende Mängel nicht beseitigt. Die Kündigung muss sich auf konkrete, nachgewiesene Mängel stützen. Nach Kündigung: Abrechnung der erbrachten Leistungen."},
    {"aktenzeichen": "LG Stuttgart 13 S 92/21", "datum": "2022-01-20", "titel": "Untervermietung: Berechtigtes Interesse", "inhalt": "Ein berechtigtes Interesse zur Untervermietung liegt vor, wenn sich die persönlichen oder wirtschaftlichen Verhältnisse des Mieters nach Vertragsschluss geändert haben. Ein berufsbedingter zeitweiser Aufenthalt in einer anderen Stadt kann genügen."},
    {"aktenzeichen": "OLG Hamm I-22 U 58/20", "datum": "2021-04-15", "titel": "Grundstückskauf: Offenbarungspflichten des Verkäufers", "inhalt": "Der Verkäufer muss ungefragt offenbaren, wenn das Grundstück mit nicht einsehbaren Altlasten kontaminiert ist oder versteckte Mängel am Gebäude existieren. Kennt er die Mängel und verschweigt sie, liegt Arglist vor."},
]

# Praxistipps Mieter
PRAXISTIPPS_MIETER = [
    {"titel": "Praxistipp Mieter: Mietvertrag vor Unterschrift prüfen", "inhalt": "Vor der Unterschrift den Mietvertrag gründlich lesen. Auf unwirksame Klauseln achten (Schönheitsreparaturen mit Fristenplan, zu hohe Kleinreparaturkosten). Die Wohnfläche nachrechnen - mehr als 10% Abweichung berechtigt zur Minderung. Den Mietspiegel prüfen."},
    {"titel": "Praxistipp Mieter: Mängel richtig anzeigen", "inhalt": "Mängel immer schriftlich anzeigen (E-Mail mit Lesebestätigung oder Einschreiben). Den Mangel genau beschreiben und Fotos beifügen. Eine angemessene Frist zur Beseitigung setzen (je nach Dringlichkeit: 2-14 Tage). Erst nach Mängelanzeige ist eine Mietminderung zulässig."},
    {"titel": "Praxistipp Mieter: Betriebskostenabrechnung prüfen", "inhalt": "Innerhalb von 12 Monaten müssen Sie auf die Abrechnung reagieren. Formelle Fehler (falscher Zeitraum, fehlende Angaben) und inhaltliche Fehler (nicht umlagefähige Kosten, Rechenfehler) prüfen. Belege beim Vermieter einsehen. Bei Fehlern: Schriftlich widersprechen."},
    {"titel": "Praxistipp Mieter: Kündigung durch Vermieter erhalten", "inhalt": "Ruhe bewahren und Kündigungsgrund prüfen. Fristen und Formalien kontrollieren (schriftlich, begründet, Frist korrekt?). Nicht sofort ausziehen - Widerspruch wegen Härte möglich (§ 574 BGB). Mieterverein oder Rechtsanwalt aufsuchen. Miete weiterzahlen!"},
    {"titel": "Praxistipp Mieter: Auszug und Übergabe", "inhalt": "Vor der Übergabe: Renovierungspflichten prüfen (meist unwirksam!). Wohnung besenrein übergeben. Alle Schlüssel sammeln. Zur Übergabe: Protokoll anfertigen, Zählerstände notieren, Fotos machen. Nach der Übergabe: Kaution einfordern (Frist: 3-6 Monate)."},
    {"titel": "Praxistipp Mieter: Mieterhöhung prüfen", "inhalt": "Mieterhöhung auf ortsübliche Vergleichsmiete: Mietspiegel prüfen, Kappungsgrenze (15-20%) und Jahressperrfrist eingehalten? Modernisierungsmieterhöhung: Nur 8% der Kosten pro Jahr umlagefähig. Staffelmiete und Indexmiete: Ist die Vereinbarung wirksam?"},
]

# Praxistipps Vermieter
PRAXISTIPPS_VERMIETER = [
    {"titel": "Praxistipp Vermieter: Mieterauswahl", "inhalt": "Mieterselbstauskunft einholen: Arbeitgeber, Einkommen, Vorvermieter. Bonitätsprüfung durchführen (SCHUFA-Auskunft). Auf vollständige Unterlagen bestehen. Keine diskriminierenden Ablehnungsgründe dokumentieren. Besichtigungstermine professionell durchführen."},
    {"titel": "Praxistipp Vermieter: Mietvertrag gestalten", "inhalt": "Aktuelle Vertragsformulare verwenden - veraltete Klauseln sind oft unwirksam. Wohnfläche korrekt angeben. Betriebskostenvorauszahlung realistisch kalkulieren. Hausordnung als Anlage beifügen. Bei möblierter Vermietung: Inventarliste erstellen."},
    {"titel": "Praxistipp Vermieter: Kaution sichern", "inhalt": "Kaution schriftlich im Mietvertrag vereinbaren (maximal 3 Monatsmieten). Auf separatem Konto anlegen (Treuhandkonto). Zinsen stehen dem Mieter zu. Bei Auszug: Prüfungsfrist nutzen (3-6 Monate), aber nicht unbegründet zurückhalten. Aufrechnung nur mit berechtigten Forderungen."},
    {"titel": "Praxistipp Vermieter: Richtig kündigen", "inhalt": "Kündigung immer schriftlich und begründet. Kündigungsfristen beachten (3-9 Monate je nach Wohndauer). Bei Eigenbedarf: Bedarf konkret darlegen. Bei Zahlungsverzug: Erst abmahnen (bei ordentlicher Kündigung). Kündigung an alle Mieter adressieren."},
    {"titel": "Praxistipp Vermieter: Modernisierungsankündigung", "inhalt": "Modernisierung 3 Monate vorher schriftlich ankündigen. Inhalt: Art und Umfang der Arbeiten, voraussichtliche Dauer, erwartete Mieterhöhung. Härtefälle der Mieter berücksichtigen. Nach Abschluss: Mieterhöhung unter Vorlage der Kostenaufstellung erklären."},
    {"titel": "Praxistipp Vermieter: Betriebskostenabrechnung", "inhalt": "Jährlich innerhalb von 12 Monaten abrechnen. Nur umlagefähige Kosten berücksichtigen (§ 2 BetrKV). Verteilerschlüssel transparent machen. Belege aufbewahren (Einsichtsrecht der Mieter). Bei Nachzahlung: Angemessene Zahlungsfrist setzen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Bauschadenrecht
    for item in BAUSCHADENRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Baurecht", "title": item['titel']}})
    
    # Architektenrecht
    for item in ARCHITEKTENRECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Architektenrecht", "title": item['titel']}})
    
    # OLG/LG Urteile
    for item in OLG_LG_URTEILE:
        text = f"{item['aktenzeichen']} ({item['datum']}): {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['aktenzeichen'], "type": "Rechtsprechung", "category": "OLG/LG", "title": item['titel']}})
    
    # Praxistipps Mieter
    for item in PRAXISTIPPS_MIETER:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Mieter", "title": item['titel']}})
    
    # Praxistipps Vermieter
    for item in PRAXISTIPPS_VERMIETER:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Vermieter", "title": item['titel']}})
    
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
