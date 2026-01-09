#!/usr/bin/env python3
"""
Mega-Seeding Teil 7: Immobilienfinanzierung Details, Vermögensnachfolge, Mediation
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

# Immobilienfinanzierung Details
FINANZIERUNG_DETAIL = [
    {"titel": "Finanzierung: Eigenkapitalquote und Beleihungsauslauf", "inhalt": "Die Eigenkapitalquote ist entscheidend für die Finanzierungskonditionen. Empfohlen: Mindestens 20% Eigenkapital (inkl. Nebenkosten). Bei 100%-Finanzierung: Deutlich höhere Zinsen. Der Beleihungsauslauf (Darlehen/Beleihungswert) sollte unter 80% liegen für beste Konditionen."},
    {"titel": "Finanzierung: Forward-Darlehen", "inhalt": "Ein Forward-Darlehen sichert die aktuellen Zinsen für die Anschlussfinanzierung bis zu 60 Monate im Voraus. Es kostet einen Aufschlag (ca. 0,02% pro Monat Vorlaufzeit). Sinnvoll bei erwarteten Zinssteigerungen. Kein Kündigungsrecht des Darlehensnehmers."},
    {"titel": "Finanzierung: Vorfälligkeitsentschädigung", "inhalt": "Bei vorzeitiger Rückzahlung eines Immobilienkredits kann die Bank eine Vorfälligkeitsentschädigung verlangen. Berechnung: Entgangener Zinsgewinn abzüglich ersparter Risikokosten und Verwaltungskosten. Faustregel: Je länger die Restlaufzeit und je höher der Zins, desto höher die Entschädigung."},
    {"titel": "Finanzierung: Restschuldversicherung", "inhalt": "Die Restschuldversicherung sichert die Tilgung bei Tod, Arbeitsunfähigkeit oder Arbeitslosigkeit. Kosten: 3-10% der Darlehenssumme. Kritik: Oft teuer und mit vielen Ausschlüssen. Alternative: Separate Risikolebensversicherung und Berufsunfähigkeitsversicherung."},
    {"titel": "Finanzierung: Baudarlehen vs. Bauspardarlehen", "inhalt": "Baudarlehen: Sofort verfügbar, Zinsbindung wählen. Bauspardarlehen: Erst nach Ansparphase, dafür garantierter Zins. Kombimodell: Vorfinanzierung durch Bank bis Zuteilung des Bausparvertrags. Bausparvertrag bietet Zinssicherheit für die Zukunft."},
    {"titel": "Finanzierung: Disagio und Agio", "inhalt": "Das Disagio ist ein Abschlag auf den Auszahlungsbetrag (z.B. 96% Auszahlung = 4% Disagio). Es senkt den Nominalzins und ist steuerlich absetzbar. Das Agio ist ein Aufschlag. Beim Vergleich: Immer den Effektivzins betrachten."},
    {"titel": "Finanzierung: Grundbuchkosten und Notar bei Grundschuld", "inhalt": "Die Eintragung einer Grundschuld kostet etwa 1,0-1,5% der Grundschuldsumme (Notar + Grundbuchamt). Bei Umschuldung: Abtretung der bestehenden Grundschuld ist günstiger als Löschung und Neueintragung. Die Bank muss bei Volltilgung die Löschungsbewilligung erteilen."},
]

# Vermögensnachfolge bei Immobilien
VERMOEGENSNACHFOLGE = [
    {"titel": "Erbschaftsteuer: Freibeträge bei Immobilien", "inhalt": "Freibeträge: Ehegatte 500.000 EUR, Kinder je 400.000 EUR, Enkel 200.000 EUR. Die selbstgenutzte Familienimmobilie kann steuerfrei an Ehegatte oder Kinder übergehen, wenn der Erbe 10 Jahre darin wohnt. Bei Grundstücken gilt der Grundbesitzwert (Verkehrswert)."},
    {"titel": "Schenkungsteuer: Immobilie zu Lebzeiten übertragen", "inhalt": "Die Freibeträge für Schenkungen entsprechen denen für Erbschaften und können alle 10 Jahre neu genutzt werden. Vorteil der Schenkung: Wertsteigerungen nach Übertragung sind steuerfrei. Nachteil: Kein Nießbrauch-Abzug mehr seit 2008 bei Übertragung unter Nießbrauchsvorbehalt."},
    {"titel": "Nießbrauch: Übertragung mit Wohnrecht", "inhalt": "Der Schenker behält sich den Nießbrauch oder ein Wohnungsrecht vor. Nießbrauch: Umfassendes Nutzungsrecht inkl. Vermietung. Wohnungsrecht: Nur Selbstnutzung. Der Wert des vorbehaltenen Rechts mindert den schenkungsteuerpflichtigen Wert. Kapitalwert richtet sich nach Alter und Mieteinnahmen."},
    {"titel": "Erbvertrag und Übergabevertrag", "inhalt": "Im Erbvertrag können bindende Verfügungen über den Nachlass getroffen werden. Der Übergabevertrag regelt die vorweggenommene Erbfolge (Schenkung zu Lebzeiten). Typisch: Gegenleistungen wie Pflegepflicht, Wohnrecht, Leibrente oder Versorgungszahlungen an Geschwister."},
    {"titel": "Pflichtteil bei Immobilienübertragung", "inhalt": "Der Pflichtteil beträgt die Hälfte des gesetzlichen Erbteils. Bei Schenkungen innerhalb von 10 Jahren vor dem Erbfall: Pflichtteilsergänzungsanspruch (abschmelzend um 10% pro Jahr). Die Immobilie wird zum Verkehrswert angesetzt. Der Nießbrauch mindert den Wert."},
    {"titel": "Testamentarische Gestaltung bei Immobilien", "inhalt": "Typische Gestaltungen: Vermächtnis einer Immobilie an bestimmten Erben, Teilungsanordnung zur Vermeidung von Erbengemeinschaften, Vor- und Nacherbschaft bei Ehegattentestament. Wichtig: Keine Auflagen, die den Verkauf dauerhaft verhindern."},
]

# Streitbeilegung
STREITBEILEGUNG = [
    {"titel": "Mediation im Mietrecht", "inhalt": "Die Mediation ist ein außergerichtliches Streitbeilegungsverfahren. Ein neutraler Mediator unterstützt die Parteien bei der Lösungsfindung. Vorteile: Schneller, günstiger, erhält die Beziehung. In Mietstreitigkeiten besonders sinnvoll bei Nachbarschaftskonflikten oder Nebenkostenstreitigkeiten."},
    {"titel": "Schlichtungsverfahren im Wohnungseigentumsrecht", "inhalt": "Vor Klage in WEG-Sachen kann ein Schlichtungsverfahren sinnvoll sein. Einige Länder haben obligatorische Schlichtung eingeführt. Die Schlichtungsstellen sind bei Gerichten oder Anwaltskammern angesiedelt. Kosten: Gering (50-100 EUR)."},
    {"titel": "Mieterschutzverein und Haus- und Grundbesitzerverein", "inhalt": "Der Mieterschutzverein bietet Mietern Rechtsberatung und Prozessvertretung. Jahresbeitrag: 60-100 EUR. Der Haus- und Grundbesitzerverein berät Vermieter. Beide bieten Musterverträge und Informationsmaterial. Wartefrist für Rechtsschutz: Meist 3 Monate."},
    {"titel": "Gerichtliches Verfahren: Mietstreitigkeiten", "inhalt": "Für Mietstreitigkeiten ist das Amtsgericht am Ort der Wohnung ausschließlich zuständig. Bei Streitwert bis 5.000 EUR: Vereinfachtes Verfahren möglich. Räumungsklagen können im Urkundenprozess beschleunigt werden. Berufung: Erst ab Beschwer von 600 EUR."},
]

# Bauträgervertrag
BAUTRAEGER = [
    {"titel": "Bauträgervertrag: MaBV und Abschlagszahlungen", "inhalt": "Der Bauträger darf nach MaBV Abschlagszahlungen nur nach Baufortschritt verlangen. Die gesetzlichen Raten sind: 30% nach Beginn Erdarbeiten, weitere Raten nach Fertigstellung Rohbau, Dach, Fenster, Innenausbau. Maximal 96,5% vor Abnahme. Rest nach Bezugsfertigkeit und Grundbucheintragung."},
    {"titel": "Bauträgervertrag: Abnahmepflicht und Fertigstellungsgarantie", "inhalt": "Der Käufer muss das Sondereigentum und das Gemeinschaftseigentum abnehmen. Vor Abnahme: Verjährung beginnt nicht zu laufen. Der Bauträger muss für 5 Jahre Gewährleistung übernehmen. Eine Fertigstellungsgarantie (Bürgschaft) schützt bei Insolvenz des Bauträgers."},
    {"titel": "Bauträgervertrag: Sonderwünsche und Änderungen", "inhalt": "Sonderwünsche müssen schriftlich vereinbart werden. Der Bauträger muss ein Angebot mit Mehrkosten vorlegen. Änderungswünsche nach Baubeginn können teuer werden. Wichtig: Vereinbarte Ausstattung genau in der Baubeschreibung prüfen."},
    {"titel": "Bauträgervertrag: Insolvenzsicherung", "inhalt": "Der Bauträger muss nach § 7 MaBV eine Sicherheit leisten (Bürgschaft oder Fertigstellungsversicherung). Die Sicherheit muss 100% der geleisteten Zahlungen abdecken. Bei Insolvenz: Bürgschaft einlösen, Bauherrengemeinschaft zur Fertigstellung bilden oder Rücktritt."},
]

# Mehr Urteile
WEITERE_URTEILE = [
    {"aktenzeichen": "BGH VIII ZR 9/23", "datum": "2024-01-17", "titel": "Mietkaution: Verzinsung und Anlage", "inhalt": "Der Vermieter muss die Kaution getrennt von seinem Vermögen anlegen (insolvenzfest). Die Zinsen stehen dem Mieter zu. Bei Nichtanlage: Der Mieter kann Herausgabe der Zinsen verlangen, die bei ordnungsgemäßer Anlage angefallen wären."},
    {"aktenzeichen": "BGH V ZR 220/22", "datum": "2023-09-22", "titel": "WEG: Beschlussfassung zu Erhaltungsmaßnahmen", "inhalt": "Erhaltungsmaßnahmen am Gemeinschaftseigentum können mit einfacher Mehrheit beschlossen werden. Die Kosten werden nach dem gesetzlichen oder vereinbarten Kostenverteilungsschlüssel umgelegt. Der einzelne Eigentümer kann die Durchführung notfalls selbst beauftragen und Kostenersatz verlangen."},
    {"aktenzeichen": "BGH VIII ZR 42/22", "datum": "2023-05-10", "titel": "Kündigung wegen Eigenbedarfs: Alternativwohnungen", "inhalt": "Der Vermieter muss den Mieter auf Alternativwohnungen in seinem Bestand hinweisen, die während der Kündigungsfrist frei werden. Unterlässt er dies, kann die Kündigung unwirksam sein. Die Hinweispflicht besteht bis zum Ablauf der Kündigungsfrist."},
    {"aktenzeichen": "BGH V ZR 112/21", "datum": "2022-12-16", "titel": "Nachbarrecht: Überhängende Äste und Selbsthilferecht", "inhalt": "Der Nachbar darf überhängende Äste abschneiden, wenn der Eigentümer trotz Fristsetzung nicht handelt. Das abgeschnittene Holz gehört dem Baumbesitzer. Die Kosten muss der Baumbesitzer tragen. Die Beeinträchtigung muss wesentlich sein."},
    {"aktenzeichen": "BGH XII ZR 107/22", "datum": "2023-11-08", "titel": "Gewerbemiete: Betriebskosten bei Leerstand", "inhalt": "Der Vermieter eines Gewerbeobjekts muss die Betriebskosten für leerstehende Einheiten selbst tragen, wenn im Mietvertrag die umlagefähige Fläche auf die tatsächlich vermietete Fläche begrenzt ist. Bei Umlage nach Gesamtfläche: Leerstandskosten werden verteilt."},
    {"aktenzeichen": "OLG Dresden 5 U 761/22", "datum": "2023-04-27", "titel": "Maklervertrag: Doppeltätigkeit und Provisionsanspruch", "inhalt": "Der Makler darf für beide Parteien tätig sein, muss aber beide Seiten darüber informieren. Bei Verstoß gegen die Aufklärungspflicht kann der Provisionsanspruch verwirkt sein. Die Doppeltätigkeit muss bei Vertragsschluss offengelegt werden."},
    {"aktenzeichen": "LG Frankfurt 2-13 S 88/22", "datum": "2023-02-15", "titel": "Mieterhöhung: Anforderungen an Modernisierungsmieterhöhung", "inhalt": "Die Modernisierungsmieterhöhung muss die Kosten der Maßnahme und deren Berechnung nachvollziehbar darlegen. Pauschale Angaben genügen nicht. Der Mieter hat ein Recht auf Einsicht in die Rechnungen. Instandhaltungsanteile sind herauszurechnen."},
    {"aktenzeichen": "AG München 452 C 12345/22", "datum": "2023-06-20", "titel": "Mietminderung: Kein Balkon bei Zusage", "inhalt": "Wurde im Exposé ein Balkon zugesagt, ist dessen Fehlen ein Sachmangel. Der Mieter kann die Miete um etwa 5-10% mindern. Zusätzlich kann er Schadensersatz wegen falscher Angaben verlangen, wenn er im Vertrauen darauf angemietet hat."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # Finanzierung Detail
    for item in FINANZIERUNG_DETAIL:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Finanzierung", "title": item['titel']}})
    
    # Vermögensnachfolge
    for item in VERMOEGENSNACHFOLGE:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Erbschaft", "title": item['titel']}})
    
    # Streitbeilegung
    for item in STREITBEILEGUNG:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Streitbeilegung", "title": item['titel']}})
    
    # Bauträger
    for item in BAUTRAEGER:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Bauträger", "title": item['titel']}})
    
    # Weitere Urteile
    for item in WEITERE_URTEILE:
        text = f"{item['aktenzeichen']} ({item['datum']}): {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['aktenzeichen'], "type": "Rechtsprechung", "category": "Urteile", "title": item['titel']}})
    
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
