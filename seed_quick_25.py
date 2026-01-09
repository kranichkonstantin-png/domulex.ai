#!/usr/bin/env python3
"""
Quick Push: 25 wichtige Dokumente
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

# Wichtige rechtsprechung
DOKUMENTE = [
    {"titel": "BGH zur Beschaffenheitsvereinbarung", "inhalt": "Der BGH hat klargestellt: Eine Beschaffenheitsvereinbarung liegt vor, wenn der Verkäufer bestimmte Eigenschaften zusagt. Wird eine zugesagte Eigenschaft nicht erfüllt, kann der Käufer Nacherfüllung oder bei Fehlschlagen Minderung/Rücktritt verlangen. Verjährung: 5 Jahre."},
    
    {"titel": "Mietpreisbremse: Ausnahmen und Grenzen", "inhalt": "Die Mietpreisbremse gilt in angespannten Wohnungsmärkten. Ausnahmen: Neubau ab 2014, Modernisierung mit 11% Kostenumlage, qualifizierter Mietspiegel zeigt höhere Miete. Vermieter muss über Ausnahme informieren. Rückforderung überzahlter Miete möglich."},
    
    {"titel": "Energetische Modernisierung: Kostenumlage", "inhalt": "Nach energetischer Modernisierung können 8% der Kosten jährlich auf die Miete umgelegt werden. Maximum: 3 EUR/qm in 6 Jahren bzw. 2 EUR/qm bei Mieten unter 7 EUR/qm. Duldungspflicht des Mieters für 3 Monate bei Härtefall länger."},
    
    {"titel": "WEG-Reform 2020: Wichtigste Änderungen", "inhalt": "Wichtigste Änderungen: Vereinfachte Beschlussfassung bei baulichen Veränderungen. Barrierefreiheit: Einfache Mehrheit statt Einstimmigkeit. E-Mobilität: Anspruch auf Ladeinfrastruktur. Modernisierung energetisch: Privilegierung bei Beschlussfassung."},
    
    {"titel": "Maklercourtage: Bestellerprinzip", "inhalt": "Seit 2020 gilt das Bestellerprinzip: Wer den Makler beauftragt, zahlt die Courtage. Bei Vermietung trägt meist der Vermieter die Kosten. Bei Verkauf: Teilung 50/50 oder Verkäufer allein. Umgehung durch Nebenabsprachen ist unwirksam."},
    
    {"titel": "Vorkaufsrecht: Gemeinde vs. Mieter", "inhalt": "Bei Umwandlung in Eigentumswohnungen haben Mieter Vorkaufsrecht. In sozialen Erhaltungsgebieten kann auch die Gemeinde ein Vorkaufsrecht haben. Das gemeindliche Vorkaufsrecht geht dem Mieter-Vorkaufsrecht vor. Ausübung binnen 2 Monaten nach Anzeige."},
    
    {"titel": "Bauträgervertrag: Sicherheiten", "inhalt": "Bauträger müssen Sicherheiten für Anzahlungen stellen. Bankbürgschaft oder Treuhandkonto erforderlich. Anzahlungen nur nach Baufortschritt. Käufer kann bei Insolvenz des Bauträgers die Fertigstellung vom Sicherungsgeber verlangen."},
    
    {"titel": "Erbbaurecht: Verlängerung und Heimfall", "inhalt": "Erbbaurecht kann verlängert werden. Bei Heimfall fällt das Erbbaurecht an den Grundstückseigentümer zurück. Entschädigung für das Gebäude ist zu zahlen. Heimfall tritt ein bei groben Verstößen gegen den Erbbaurechtsvertrag."},
    
    {"titel": "Zwangsversteigerung: Mindestgebot", "inhalt": "Das Mindestgebot beträgt 5/10 des Verkehrswerts. Bei erstem Termin auch 7/10 möglich. Gläubiger können unter dem Mindestgebot nicht zum Zuge kommen. Eigentümer kann die Einstellung beantragen, wenn Erlös zur Gläubigerbefriedigung nicht ausreicht."},
    
    {"titel": "Nachbarrecht: Überbau und Grenzabstand", "inhalt": "Überbau auf Nachbargrundstück kann zur Duldung verpflichten, wenn gutgläubig und geringfügig. Ausgleichszahlung erforderlich. Grenzabstände müssen eingehalten werden. Ausnahmen nur bei Einverständnis des Nachbarn oder bauordnungsrechtlichen Befreiungen."},
    
    {"titel": "Wohnungseigentumsrecht: Beschlussanfechtung", "inhalt": "Beschlüsse der WEG können binnen eines Monats angefochten werden. Anfechtungsgrund: Verstoß gegen Gesetz oder Gemeinschaftsordnung. Anfechtungsberechtigt sind alle Wohnungseigentümer. Bei Nichtigkeitsgründen ist keine Frist zu beachten."},
    
    {"titel": "Mietminderung bei Mängeln: Höhe und Nachweis", "inhalt": "Mietminderung richtet sich nach der Beeinträchtigung der Gebrauchstauglichkeit. Erhebliche Mängel: 10-50% Minderung. Kompletter Ausfall: 100% möglich. Mieter muss Mangel nachweisen und dem Vermieter anzeigen. Minderung gilt ab Auftreten des Mangels."},
    
    {"titel": "Grundschuld vs. Hypothek", "inhalt": "Grundschuld ist nicht an eine Forderung gebunden, Hypothek schon. Bei Tilgung der Hypothek erlischt diese automatisch. Grundschuld bleibt bestehen und kann für neue Kredite verwendet werden. Löschung der Grundschuld erfordert Löschungsbewilligung des Gläubigers."},
    
    {"titel": "Teilungserklärung: Inhalt und Änderung", "inhalt": "Teilungserklärung regelt Aufteilung in Sonder- und Gemeinschaftseigentum sowie Nutzungsrechte. Enthält Gemeinschaftsordnung mit Verwaltungs- und Benutzungsregeln. Änderungen erfordern meist Zustimmung aller Eigentümer. Nur formelle Änderungen mit einfacher Mehrheit."},
    
    {"titel": "Schönheitsreparaturen: Renovierungsklauseln", "inhalt": "Schönheitsreparaturen können auf Mieter übertragen werden. Starre Fristen sind unwirksam, nur Richtfristen zulässig. Bei unrenoviert überlassener Wohnung dürfen keine Schönheitsreparaturen verlangt werden. Fachgerechte Ausführung kann vorgeschrieben werden."},
    
    {"titel": "Stellplatzverordnung: Ablöse und Nachweis", "inhalt": "Bei Neu- und Umbauten sind Stellplätze nachzuweisen. Stellplätze können durch Ablösebetrag ersetzt werden. Höhe: 10.000-25.000 EUR je nach Gemeinde. Stellplätze müssen dauerhaft verfügbar sein. Zweckentfremdung ist untersagt."},
    
    {"titel": "Denkmalschutz: Genehmigungspflicht", "inhalt": "An Baudenkmälern sind alle Veränderungen genehmigungspflichtig. Auch Instandsetzung kann Genehmigung erfordern. Denkmaleigenschaft wird durch Aufnahme in die Denkmalliste begründet. Steuervorteile bei denkmalgerechter Sanierung (AfA-Abschreibung)."},
    
    {"titel": "Lärmschutz: Grenzwerte und Durchsetzung", "inhalt": "Lärmgrenzwerte richten sich nach Gebietsart: Wohngebiet nachts 35 dB(A), Mischgebiet 40 dB(A). Bei Überschreitungen drohen Bußgelder oder Betriebsuntersagung. Lärmprotokoll als Nachweis wichtig. Lärmschutzauflagen können nachträglich verhängt werden."},
    
    {"titel": "Fernwärme: Anschlusszwang und Kosten", "inhalt": "Gemeinden können Fernwärme-Anschlusszwang verhängen. Anschlussnehmer müssen Hausanschluss und Wärmelieferungsvertrag abschließen. Preise unterliegen der AVBFernwärmeV. Preisänderungen müssen begründet und angemessen sein. Sonderkündigungsrecht bei Verkauf."},
    
    {"titel": "Bauabnahme: Förmliche vs. konkludente Abnahme", "inhalt": "Abnahme kann förmlich oder konkludent erfolgen. Förmliche Abnahme: Ausdrückliche Erklärung. Konkludente Abnahme: Einzug oder Nutzung trotz bekannter Mängel. Mit Abnahme beginnt Gewährleistungsfrist. Bekannte Mängel sind bei Abnahme vorzubehalten."},
    
    {"titel": "Baubeschreibung: Verbindlichkeit", "inhalt": "Die Baubeschreibung wird Vertragsbestandteil und ist verbindlich. Abweichungen nur mit Zustimmung des Käufers. Mehrvergütung bei Änderungswünschen möglich. Gleichwertige Materialien sind zulässig, wenn im Vertrag vorbehalten. Qualitätsstandard muss gleich bleiben."},
    
    {"titel": "Indexmiete: Anpassung und Grenzen", "inhalt": "Indexmiete richtet sich nach Verbraucherpreisindex. Anpassung frühestens nach einem Jahr und um mindestens 5%. Schriftliche Mitteilung erforderlich. Modernisierungsumlage ist bei Indexmiete ausgeschlossen. Mietpreisbremse gilt nicht für Indexmieten."},
    
    {"titel": "WEG-Verwaltung: Aufgaben und Haftung", "inhalt": "Verwalter führt Geschäfte der WEG nach Weisung der Eigentümerversammlung. Haftet für schuldhaftes Handeln. Mindestausstattung: Berufshaftpflichtversicherung. Verwalterbeirat kontrolliert Verwalter. Bestellung und Abberufung durch Eigentümerversammlung."},
    
    {"titel": "Gewerbemietvertrag: Besonderheiten", "inhalt": "Für Gewerberäume gelten weniger Schutzvorschriften als bei Wohnraum. Kündigungsschutz schwächer. Schönheitsreparaturen meist wirksam auf Mieter übertragbar. Umsatzmiete möglich. Konkurrenzschutz kann vereinbart werden. Untermietung meist erlaubnispflichtig."},
    
    {"titel": "Erbbauzins: Anpassung und Zahlung", "inhalt": "Erbbauzins ist meist wertsicherungsklauselgebunden. Anpassung nach Lebenshaltungskostenindex oder Bodenrichtwerten. Zahlung meist jährlich im Voraus. Bei Zahlungsverzug droht Heimfall. Erbbauzins ist grundschuldähnlich dinglich gesichert."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    try:
        client = QdrantClient(
            host=QDRANT_HOST, 
            port=QDRANT_PORT, 
            api_key=QDRANT_API_KEY, 
            https=True,
            timeout=30.0
        )
        
        info = client.get_collection(COLLECTION_NAME)
        print(f"Dokumente vorher: {info.points_count}")
    except Exception as e:
        print(f"Verbindungsfehler: {e}")
        return
    
    all_docs = []
    
    for item in DOKUMENTE:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Rechtspraxis", 
                "category": "Immobilienrecht", 
                "title": item['titel']
            }
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
            if (i + 1) % 5 == 0: 
                print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler bei Dokument {i}: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    try:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        
        info = client.get_collection(COLLECTION_NAME)
        print(f"Dokumente nachher: {info.points_count}")
    except Exception as e:
        print(f"Upload-Fehler: {e}")

if __name__ == "__main__":
    main()