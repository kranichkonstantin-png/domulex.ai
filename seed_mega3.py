#!/usr/bin/env python3
"""
Mega-Seeding Teil 3: Maklerrecht, Gewerbemiete, Immobilienbewertung
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

# Gewerbemietrecht
GEWERBEMIETE = [
    {"titel": "Gewerbemietrecht: Unterschiede zur Wohnraummiete", "inhalt": "Im Gewerbemietrecht gilt weitgehende Vertragsfreiheit. Es gibt keine Mietpreisbremse, keinen Kündigungsschutz und keine Schonfristzahlung. Kündigungsfristen können frei vereinbart werden. AGB-Kontrolle findet statt, aber mit großzügigeren Maßstäben. Umsatzmiete, Konkurrenzschutzklauseln und Betriebspflichten sind zulässig."},
    {"titel": "Gewerbemietrecht: Umsatzmiete", "inhalt": "Die Umsatzmiete setzt sich aus einer Mindestmiete (Fixum) und einem prozentualen Anteil am Umsatz zusammen. Sie ist besonders bei Einzelhandelsflächen verbreitet. Der Mieter muss dem Vermieter Auskunft über die Umsätze geben. Die Auskunftspflicht und Kontrollrechte sollten vertraglich geregelt werden."},
    {"titel": "Gewerbemietrecht: Konkurrenzschutz", "inhalt": "Der Vermieter ist grundsätzlich verpflichtet, im selben Objekt keine konkurrierenden Geschäfte zu vermieten, die den Mietgebrauch beeinträchtigen. Diese Pflicht kann vertraglich ausgeschlossen oder erweitert werden. Ein vertraglicher Konkurrenzschutz ist empfehlenswert."},
    {"titel": "Gewerbemietrecht: Betriebspflicht", "inhalt": "Eine vertragliche Betriebspflicht verpflichtet den Mieter, das Gewerbe tatsächlich zu betreiben. Sie ist bei Einkaufszentren üblich, um Leerstand zu vermeiden. Die Verletzung der Betriebspflicht kann Schadensersatzansprüche und außerordentliche Kündigung rechtfertigen."},
    {"titel": "Gewerbemietrecht: Mietanpassungsklauseln", "inhalt": "Im Gewerbemietrecht sind Wertsicherungsklauseln mit Indexbindung (Verbraucherpreisindex) zulässig. Die Anpassung kann jährlich oder bei bestimmten Schwellenwerten erfolgen. Auch Staffelmietvereinbarungen sind möglich. Eine automatische Anpassung muss klar geregelt sein."},
    {"titel": "Gewerbemietrecht: Schriftform § 550 BGB", "inhalt": "Für Gewerbemietverträge mit einer Laufzeit von mehr als einem Jahr gilt das Schriftformerfordernis. Alle wesentlichen Vertragsbedingungen müssen schriftlich festgehalten werden. Bei Formmangel gilt der Vertrag als auf unbestimmte Zeit geschlossen und kann ordentlich gekündigt werden."},
    {"titel": "Gewerbemietrecht: Mieterausbau und Rückbaupflicht", "inhalt": "Der Mieter ist bei Vertragsende grundsätzlich zur Wiederherstellung des ursprünglichen Zustands verpflichtet. Vertragliche Regelungen können den Rückbau ausschließen oder modifizieren. Ohne Regelung: Einbauten verbleiben gegen Entschädigung oder müssen entfernt werden."},
    {"titel": "Gewerbemietrecht: Option und Verlängerung", "inhalt": "Optionsklauseln geben dem Mieter das Recht, das Mietverhältnis einseitig zu verlängern. Die Option muss frist- und formgerecht ausgeübt werden. Verlängerungsoptionen können mit Mietanpassungsklauseln verknüpft werden. Mehrere Optionszeiträume sind möglich."},
]

# Immobilienbewertung
IMMOBILIENBEWERTUNG = [
    {"titel": "Immobilienbewertung: Vergleichswertverfahren", "inhalt": "Das Vergleichswertverfahren ermittelt den Wert durch Vergleich mit tatsächlich erzielten Kaufpreisen ähnlicher Grundstücke. Es ist das gebräuchlichste Verfahren bei Eigentumswohnungen und Einfamilienhäusern. Vergleichsfaktoren werden aus der Kaufpreissammlung des Gutachterausschusses abgeleitet."},
    {"titel": "Immobilienbewertung: Ertragswertverfahren", "inhalt": "Das Ertragswertverfahren wird bei vermieteten Objekten angewandt. Der Wert ergibt sich aus dem kapitalisierten Reinertrag. Berechnung: Rohertrag (Jahresnettokaltmiete) minus Bewirtschaftungskosten ergibt den Reinertrag. Dieser wird mit dem Vervielfältiger (Barwertfaktor) multipliziert."},
    {"titel": "Immobilienbewertung: Sachwertverfahren", "inhalt": "Das Sachwertverfahren ermittelt die Herstellungskosten des Gebäudes und addiert den Bodenwert. Es wird bei eigengenutzten Immobilien angewandt, wenn kein Mietertrag erzielt wird. Alterswertminderung wird berücksichtigt. Typische Anwendung: Einfamilienhäuser in ländlichen Regionen."},
    {"titel": "Immobilienbewertung: Bodenrichtwert", "inhalt": "Der Bodenrichtwert ist der durchschnittliche Lagewert des Bodens in einer Bodenrichtwertzone. Er wird vom Gutachterausschuss alle zwei Jahre ermittelt. Er bezieht sich auf ein unbebautes Grundstück. Der tatsächliche Grundstückswert kann je nach Erschließung, Form und Größe abweichen."},
    {"titel": "Immobilienbewertung: Wertermittlungsstichtag", "inhalt": "Der Verkehrswert bezieht sich auf einen bestimmten Stichtag. Maßgeblich sind die tatsächlichen und rechtlichen Gegebenheiten am Bewertungsstichtag. Spätere Entwicklungen werden nicht berücksichtigt. Bei gerichtlichen Verfahren: Tag der letzten mündlichen Verhandlung."},
    {"titel": "Immobilienbewertung: Verkehrswert Definition", "inhalt": "Der Verkehrswert (§ 194 BauGB) ist der Preis, der zum Wertermittlungsstichtag im gewöhnlichen Geschäftsverkehr nach den rechtlichen Gegebenheiten und tatsächlichen Eigenschaften ohne Rücksicht auf ungewöhnliche oder persönliche Verhältnisse zu erzielen wäre."},
    {"titel": "Immobilienbewertung: Beleihungswert", "inhalt": "Der Beleihungswert ist der Wert, der der Sicherheit einer Immobilienfinanzierung zugrunde gelegt wird. Er ist in der Regel niedriger als der Verkehrswert (80-90%). Er soll den langfristig erzielbaren Wert darstellen und Marktschwankungen glätten."},
]

# Mietrecht Spezialfälle
MIETRECHT_SPEZIAL = [
    {"titel": "Mietrecht: Zeitmietvertrag § 575 BGB", "inhalt": "Ein Zeitmietvertrag ist nur zulässig, wenn der Vermieter bei Vertragsschluss einen gesetzlichen Befristungsgrund (Eigenbedarf, wesentliche Baumaßnahmen, Werkswohnung) angibt. Ohne wirksamen Grund gilt der Vertrag als unbefristet. Der Mieter kann keine vorzeitige Beendigung verlangen."},
    {"titel": "Mietrecht: Möblierter Wohnraum", "inhalt": "Bei möbliertem Wohnraum, der Teil der vom Vermieter selbst bewohnten Wohnung ist, beträgt die Kündigungsfrist nur 15 Tage zum Monatsende. Der Vermieter braucht keinen Kündigungsgrund. Für andere möblierte Wohnungen gelten die normalen Mieterschutzvorschriften."},
    {"titel": "Mietrecht: Wohngemeinschaft (WG)", "inhalt": "Bei WGs gibt es verschiedene Konstruktionen: 1. Alle als gleichberechtigte Mieter (jeder kann nur für sich kündigen), 2. Einer als Hauptmieter, andere als Untermieter, 3. Vermieter vermietet Einzelzimmer. Die Rechte und Pflichten unterscheiden sich je nach Gestaltung."},
    {"titel": "Mietrecht: Staffelmiete § 557a BGB", "inhalt": "Bei der Staffelmiete wird vereinbart, dass die Miete in festgelegten Zeitabständen um einen bestimmten Betrag steigt. Die Staffelung muss in Euro ausgewiesen werden. Der Zeitraum zwischen den Erhöhungen muss mindestens ein Jahr betragen. Während der Staffelmietvereinbarung sind andere Mieterhöhungen ausgeschlossen."},
    {"titel": "Mietrecht: Indexmiete § 557b BGB", "inhalt": "Die Indexmiete koppelt die Miethöhe an den Verbraucherpreisindex. Ändert sich der Index, kann die Miete entsprechend angepasst werden. Die Anpassung muss schriftlich erklärt werden und tritt frühestens nach einem Jahr ein. Andere Mieterhöhungen sind ausgeschlossen."},
    {"titel": "Mietrecht: Untermiete § 540 BGB", "inhalt": "Der Mieter darf ohne Erlaubnis des Vermieters nicht untervermieten. Bei Wohnraum hat der Mieter Anspruch auf Erlaubnis zur Untervermietung eines Teils der Wohnung, wenn er ein berechtigtes Interesse hat und der Vermieter kein Gegeninteresse hat. Verweigert der Vermieter unberechtigt, kann der Mieter außerordentlich kündigen."},
    {"titel": "Mietrecht: Mietaufhebungsvertrag", "inhalt": "Mieter und Vermieter können das Mietverhältnis einvernehmlich durch Aufhebungsvertrag beenden. Eine Schriftform ist empfehlenswert. Häufig wird eine Abfindung vereinbart. Der Vermieter kann so lange Kündigungsfristen umgehen. Der Mieter sollte eine ausreichende Frist für den Auszug sichern."},
    {"titel": "Mietrecht: Tod des Mieters § 563 BGB", "inhalt": "Beim Tod des Mieters treten der Ehegatte oder Lebenspartner, danach Familienangehörige in das Mietverhältnis ein. Bei WGs treten die verbleibenden Mitmieter ein. Der eintretende hat ein Sonderkündigungsrecht binnen eines Monats. Der Vermieter kann bei wichtigem Grund kündigen."},
]

# WEG Spezialthemen
WEG_SPEZIAL = [
    {"titel": "WEG: Sondernutzungsrecht", "inhalt": "Ein Sondernutzungsrecht gibt einem Eigentümer das alleinige Nutzungsrecht an einem Teil des Gemeinschaftseigentums (z.B. Gartenfläche, Stellplatz). Es wird in der Teilungserklärung oder durch Vereinbarung begründet und im Grundbuch eingetragen. Die Instandhaltung trägt der Berechtigte."},
    {"titel": "WEG: Eigentümerversammlung", "inhalt": "Die ordentliche Eigentümerversammlung muss mindestens einmal jährlich stattfinden. Die Ladungsfrist beträgt mindestens 3 Wochen in Textform. Die Versammlung beschließt über die Jahresabrechnung, den Wirtschaftsplan und sonstige Angelegenheiten. Jeder Eigentümer hat grundsätzlich ein Stimmrecht pro Einheit."},
    {"titel": "WEG: Beschlussfassung seit WEG-Reform 2020", "inhalt": "Seit 2020 können die meisten Beschlüsse mit einfacher Mehrheit gefasst werden, auch bauliche Veränderungen. Doppelt qualifizierte Mehrheit (3/4 der Stimmen und mehr als 50% der Miteigentumsanteile) ist für grundlegende Beschlüsse nötig. Allstimmigkeit nur bei Veräußerung des Grundstücks."},
    {"titel": "WEG: Anfechtungsklage § 44 WEG", "inhalt": "Beschlüsse können innerhalb eines Monats nach Beschlussfassung durch Klage angefochten werden. Zuständig ist das Amtsgericht am Ort der Wohnung. Klagebefugt ist jeder Eigentümer. Die Anfechtung hat keine aufschiebende Wirkung. Nichtige Beschlüsse können jederzeit angegriffen werden."},
    {"titel": "WEG: Instandhaltungsrücklage", "inhalt": "Die Gemeinschaft muss eine angemessene Instandhaltungsrücklage ansammeln. Sie dient der Finanzierung zukünftiger Instandhaltungs- und Instandsetzungsmaßnahmen. Eine Faustregel: 0,8-1% des Gebäudewertes pro Jahr. Die Höhe wird im Wirtschaftsplan festgelegt."},
    {"titel": "WEG: Hausgeld und Wirtschaftsplan", "inhalt": "Das Hausgeld sind die monatlichen Vorschüsse auf die Kosten der Gemeinschaft. Es setzt sich zusammen aus Betriebskosten, Instandhaltungsrücklage und Verwaltungskosten. Die Höhe ergibt sich aus dem Wirtschaftsplan, der jährlich beschlossen wird."},
    {"titel": "WEG: Verwalter Rechte und Pflichten", "inhalt": "Der Verwalter wird von der Eigentümerversammlung bestellt (maximal 5 Jahre). Er führt die Beschlüsse aus, verwaltet die Finanzen, erstellt Jahresabrechnung und Wirtschaftsplan, lädt zur Versammlung und vertritt die Gemeinschaft nach außen. Die Gemeinschaft kann ihn jederzeit abberufen."},
    {"titel": "WEG: Sondereigentumsfähig", "inhalt": "Sondereigentumsfähig sind Räume, die abgeschlossen sind. Dazu gehören Wohnungen, Gewerbeeinheiten, aber auch abgeschlossene Kellerräume und Tiefgaragenstellplätze. Nicht sondereigentumsfähig: tragende Wände, Dach, Fundament, Versorgungsleitungen bis zum Anschluss an das Sondereigentum."},
]

# Erbbaurecht
ERBBAURECHT = [
    {"titel": "Erbbaurecht: Grundlagen", "inhalt": "Das Erbbaurecht (§ 1 ErbbauRG) berechtigt, auf fremdem Grund ein Bauwerk zu haben. Es ist ein dingliches, veräußerliches und vererbliches Recht. Die typische Laufzeit beträgt 75-99 Jahre. Das Gebäude ist wesentlicher Bestandteil des Erbbaurechts, nicht des Grundstücks."},
    {"titel": "Erbbaurecht: Erbbauzins", "inhalt": "Der Erbbauzins ist das Entgelt für das Erbbaurecht. Er wird jährlich gezahlt und orientiert sich am Grundstückswert (typisch: 3-5% des Bodenwerts). Anpassungsklauseln mit Bindung an Lebenshaltungskosten oder Bodenrichtwerte sind üblich und zulässig."},
    {"titel": "Erbbaurecht: Heimfall", "inhalt": "Der Heimfall ist das Recht des Grundstückseigentümers, das Erbbaurecht bei schweren Vertragsverletzungen gegen Entschädigung zurückzufordern. Typische Heimfallgründe: Zahlungsverzug, wesentliche Vertragsverletzung, Nichtbebauung. Die Entschädigung beträgt mindestens 2/3 des Verkehrswerts."},
    {"titel": "Erbbaurecht: Verlängerung und Ablauf", "inhalt": "Bei Ablauf des Erbbaurechts fällt das Gebäude an den Grundstückseigentümer. Der Erbbauberechtigte hat Anspruch auf Entschädigung (mindestens 2/3 des Gebäudewerts). Häufig werden Verlängerungsoptionen vereinbart. Der Erbbauberechtigte hat bei Verkauf ein Vorkaufsrecht."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Gewerbemiete
    for item in GEWERBEMIETE:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Gewerbemietrecht", "title": item['titel']}})
    
    # Immobilienbewertung
    for item in IMMOBILIENBEWERTUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Bewertung", "title": item['titel']}})
    
    # Mietrecht Spezial
    for item in MIETRECHT_SPEZIAL:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Mietrecht", "title": item['titel']}})
    
    # WEG Spezial
    for item in WEG_SPEZIAL:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "WEG", "title": item['titel']}})
    
    # Erbbaurecht
    for item in ERBBAURECHT:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Erbbaurecht", "title": item['titel']}})
    
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
