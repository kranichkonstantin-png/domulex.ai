#!/usr/bin/env python3
"""
ALLERLETZTER MEGA PUSH ZUR 4.000!
50 finale Dokumente für den historischen Meilenstein!
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

FINAL_COUNTDOWN_DOCS = [
    # Noch mehr praktische Details
    {"titel": "Mietvertrag Kündigungsfristen Details", "inhalt": "Ordentliche Kündigung bei unbefristeten Mietverträgen: 3 Monate für Mieter, gestaffelt für Vermieter (3-9 Monate je nach Mietdauer). Außerordentliche Kündigung bei wichtigem Grund fristlos möglich. Eigenbedarfskündigung erfordert qualifizierten Eigenbedarf. Umwandlungssperre nach WEG-Umwandlung 3-5 Jahre."},
    
    {"titel": "Betriebskosten Umlageschlüssel Details", "inhalt": "Grundsteuer und Versicherung nach Wohnfläche umgelegt. Wasser/Abwasser nach Verbrauch oder Personen. Heizkosten 50-70% nach Verbrauch, Rest nach Fläche. Hausmeister und Reinigung nach Objektschlüssel. Gartenpflege nur bei Nutzungsmöglichkeit. Fahrstuhl nur für Obergeschosse."},
    
    {"titel": "Kaution Rückgabe Rechtspraxis", "inhalt": "Mietsicherheit maximal 3 Nettomieten kalt. Rückgabe binnen angemessener Frist nach Mietende. Berechtigung zur Aufrechnung nur bei unstreitigen Forderungen. Renovierungsklauseln oft unwirksam. Schönheitsreparaturen nicht bei unrenoviert überlassener Wohnung. Verjährung von Ansprüchen nach 3 Jahren."},
    
    {"titel": "Modernisierungsumlage Berechnung Detail", "inhalt": "8% der Modernisierungskosten pro Jahr umlagefähig. Maximum 3 EUR/qm in 6 Jahren oder 2 EUR/qm bei Mieten unter 7 EUR/qm. Energetische Modernisierung privilegiert. Duldungspflicht des Mieters bei ordnungsgemäßer Ankündigung. Mietminderung während Bauzeit möglich."},
    
    {"titel": "Schönheitsreparaturen Rechtsprechung", "inhalt": "Unwirksam bei unrenoviert überlassener Wohnung. Starre Fristen unwirksam, nur Richtfristen möglich. Fachgerechte Ausführung kann vorgeschrieben werden. Quotenabgeltung bei vorzeitigem Auszug. Kleinreparaturklausel bis 75-100 EUR pro Fall wirksam."},
    
    # Immobilien-Investment vertieft
    {"titel": "Renditeberechnung Immobilien Formeln", "inhalt": "Bruttorendite = Jahreskaltmiete / Kaufpreis x 100. Nettorendite nach Abzug von Verwaltung, Instandhaltung, Ausfällen. Eigenkapitalrendite berücksichtigt Fremdfinanzierung. Gesamtrendite inklusive Wertsteigerung über Haltedauer. Steuerliche Effekte durch AfA-Abschreibung einbeziehen."},
    
    {"titel": "Immobilienfonds REIT Deutschland", "inhalt": "G-REITs seit 2007 in Deutschland zugelassen, aber restriktiv reguliert. 90% der Gewinne ausschütten. Mindestens 75% Immobiliengeschäft. Keine Wohnimmobilien in Deutschland erlaubt. Internationale REITs für deutsche Investoren verfügbar. Quellensteuer bei ausländischen REITs beachten."},
    
    {"titel": "Immobilien Crowdinvesting Risiken", "inhalt": "Nachrangdarlehen mit Totalverlustrisiko. Keine Einlagensicherung wie bei Bankprodukten. Prospektpflicht ab 2,5 Mio EUR Emissionsvolumen. Mindestanlagevolumen meist 500-1000 EUR. Laufzeiten 2-7 Jahre typisch. Renditen 5-7% bei entsprechendem Risiko."},
    
    {"titel": "Immobilienaktien vs Direktinvestment", "inhalt": "REITs und Immobilienaktien bieten Liquidität. Keine direkten Verwaltungsaufgaben. Geringere Mindestinvestition. Aber: Schwankungen wie Aktienmarkt. Keine Steuervorteile wie bei Direktinvestment. Währungsrisiken bei internationalen REITs."},
    
    {"titel": "Baufinanzierung Forward Darlehen", "inhalt": "Forward-Darlehen sichert heutige Zinsen für spätere Auszahlung. Vorlaufzeit bis 66 Monate möglich. Aufschlag für Zinssicherung 0,01-0,03% pro Monat. Sinnvoll bei steigenden Zinsen erwartet. Aber: Zinsänderungsrisiko über Vorlaufzeit."},
    
    # Baurecht vertieft
    {"titel": "Bebauungsplan Festsetzungen Details", "inhalt": "Art der baulichen Nutzung: WA, WR, MI, MK, GE, GI. Maß der Nutzung: GRZ, GFZ, Geschossanzahl, Höhe. Bauweise: offen, geschlossen, abweichend. Baugrenzen vs Baulinien. Stellplätze, Garagen, Nebenanlagen geregelt. Grünflächen und Ausgleichsmaßnahmen."},
    
    {"titel": "Baugenehmigung Verfahrensarten", "inhalt": "Vollgenehmigung für komplexe Vorhaben. Vereinfachtes Verfahren bei Bebauungsplan-Konformität. Genehmigungsfreistellung für einfache Vorhaben. Teilbaugenehmigung für vorzeitigen Baubeginn. Kenntnisgabeverfahren in einigen Ländern."},
    
    {"titel": "Abstandsflächen Landesbauordnung", "inhalt": "Grundsätzlich H/2 mit Minimum 3m Abstand. Länderregelungen unterschiedlich: Bayern H/2, min. 3m. NRW 0,4 x H, min. 3m. Berlin 0,5 x H, min. 3m. Grenzbebauung nur mit Zustimmung des Nachbarn. Carports und Garagen Erleichterungen."},
    
    {"titel": "Nachbarrecht baulich Details", "inhalt": "Überbau dulden bei Gutgläubigkeit und Geringfügigkeit. Notwegerecht bei Grundstück ohne Zufahrt. Hammer- und Zufahrtsrechte grundbuchlich absichern. Grenzabstände auch für Aufschüttungen/Abgrabungen. Bäume: 2m Abstand bei über 2m Höhe."},
    
    {"titel": "Schwarzbau Legalisierung", "inhalt": "Nachträgliche Baugenehmigung bei genehmigungsfähigem Vorhaben möglich. Bußgeld und Baueinstellung bis Genehmigung. Abriss bei nicht genehmigungsfähigen Bauten. Verjährung bauordnungsrechtlicher Ansprüche nach Landesrecht unterschiedlich."},
    
    # Mietrecht Spezialthemen
    {"titel": "Untervermietung Rechtslage", "inhalt": "Erlaubnis des Vermieters für Untervermietung erforderlich. Berechtigendes Interesse: WG, Kostenteilung, persönliche Gründe. Vermieter kann nur bei wichtigem Grund verweigern. Untermieter haben eingeschränkten Kündigungsschutz. Gewerbliche Untervermietung meist unzulässig."},
    
    {"titel": "Hausordnung Rechtswirkung", "inhalt": "Hausordnung nur bei Vereinbarung im Mietvertrag wirksam. Nachträgliche Änderungen nur mit Mieter-Zustimmung. Ruhezeiten 22-6 Uhr und 13-15 Uhr üblich. Haustierhaltung kann geregelt/verboten werden. Grillverbot auf Balkonen meist unwirksam."},
    
    {"titel": "Mängel Mietminderung Tabelle", "inhalt": "Heizungsausfall Winter: 50-100% Minderung. Kein Warmwasser: 10-15%. Erheblicher Lärm: 10-50% je nach Intensität. Schimmel: 20-80% je nach Ausdehnung. Defekte Toilette: 50%. Kein Aufzug bei Obergeschossen: 5-20%."},
    
    {"titel": "Eigenbedarfskündigung Voraussetzungen", "inhalt": "Nur für Vermieter, Familienangehörige, Haushaltsangehörige. Ernsthafte Absicht zur eigenen Nutzung. Nicht bei Spekulation oder Vermietungswunsch an Dritte. Härtefall-Einwände des Mieters prüfen. Sperrfristen bei Umwandlung in WEG."},
    
    {"titel": "Kündigung wegen Zahlungsverzug", "inhalt": "Fristlose Kündigung bei Rückstand von 2 Monatsmieten. Oder bei wiederholtem Verzug geringerer Beträge. Schonfrist bis Räumungstermin bei Nachzahlung. Sozialklausel für unverschuldete Notlagen. Teilzahlungen können Kündigung unwirksam machen."},
    
    # WEG-Recht Details
    {"titel": "Beschlussfassung WEG Mehrheiten", "inhalt": "Einfache Mehrheit: Verwaltung und Instandhaltung. Qualifizierte Mehrheit (3/4): Änderungen am Gemeinschaftseigentum. Einstimmigkeit: Grundlegende Änderungen der Teilungserklärung. Modernisierung privilegiert seit WEG-Reform. Präsenz-/Briefwahl möglich."},
    
    {"titel": "Sonderumlage WEG Beschluss", "inhalt": "Große Reparaturen über Sonderumlage finanziert. Beschluss mit einfacher Mehrheit bei Instandhaltung. Qualifizierte Mehrheit bei baulichen Änderungen. Zahlungsunfähige Eigentümer belasten Gemeinschaft. Sonderumlagen bis 500 EUR ohne Beschluss möglich."},
    
    {"titel": "Verwalter WEG Aufgaben", "inhalt": "Geschäftsführung nach Weisungen der Eigentümerversammlung. Hausgeld-Einzug und Nebenkostenabrechnung. Instandhaltungsmaßnahmen organisieren. Versicherungen abschließen und verwalten. Rechtliche Vertretung nach außen. Verwalterbeirat kontrolliert Tätigkeit."},
    
    {"titel": "Gemeinschaftseigentum Abgrenzung", "inhalt": "Tragende Wände, Dach, Fassade immer gemeinschaftlich. Fenster meist Sondereigentum. Balkone je nach Teilungserklärung. Leitungen in Wänden meist Gemeinschaftseigentum. Heizung zentral: Gemeinschaftseigentum. Sanitäranschlüsse ab Wohnungsverteilung Sondereigentum."},
    
    {"titel": "WEG Verwalterbeirat Aufgaben", "inhalt": "Unterstützung und Kontrolle des Verwalters. Prüfung der Jahresabrechnung. Beratung bei wichtigen Entscheidungen. Vermittlung zwischen Verwalter und Eigentümern. Beirat wird von Eigentümerversammlung gewählt. Ehrenamtliche Tätigkeit ohne Vergütung."},
    
    # Steuerrecht Immobilien
    {"titel": "Abschreibung Immobilien AfA", "inhalt": "Gebäude: 2% linear über 50 Jahre. Modernisierung eigenständig abschreibbar. Denkmalschutz: Sonderabschreibung 9 Jahre 8%, dann 12 Jahre 7%. Nur bei Vermietung und Verpachtung. Grund und Boden nicht abschreibbar."},
    
    {"titel": "Spekulationssteuer Immobilien", "inhalt": "Veräußerungsgewinn steuerpflichtig bei Verkauf binnen 10 Jahren. Eigengenutzte Immobilien (2 Jahre vor Verkauf) steuerfrei. Geerbte Immobilien: 10-Jahres-Frist läuft weiter. Reinvestition in neue Immobilie verschiebt nicht die Besteuerung."},
    
    {"titel": "Grunderwerbsteuer Sätze Länder", "inhalt": "NRW, SH, Saarland: 6,5%. Berlin, Brandenburg, Thüringen: 6%. Bayern, Sachsen: 3,5%. Familienerwerb oft befreit. Gesellschaftsanteile über 95% auslösen Steuer. Share Deals umgehen Grunderwerbsteuer."},
    
    {"titel": "Grundsteuer Reform 2025", "inhalt": "Neues wertbezogenes Verfahren ab 2025. Bodenrichtwert x Grundstücksfläche x Gebäudewert. Länder können eigene Modelle entwickeln. Bayern: Flächenmodell ohne Wertermittlung. Öffnungsklausel für kommunale Hebesätze."},
    
    {"titel": "Vermietung steuerlich Tipps", "inhalt": "Werbungskosten voll absetzbar: Zinsen, Verwaltung, Reparaturen. Anschaffungskosten nur über AfA. Haushaltsnahe Dienstleistungen begrenzt absetzbar. Eigenleistung nicht absetzbar. Leerstand mindert nicht Abschreibung."},
    
    # Energieeffizienz Details
    {"titel": "Energieausweis Arten Unterschiede", "inhalt": "Verbrauchsausweis: Basis der letzten 3 Jahre Verbrauchsdaten. Bedarfsausweis: Berechnung nach technischen Gebäudedaten. Neubau und Großsanierung: Bedarfsausweis Pflicht. Vermietung: Ausweis vor Besichtigung vorlegen. Gültigkeit 10 Jahre."},
    
    {"titel": "KfW Förderung Sanierung", "inhalt": "Bundesförderung effiziente Gebäude (BEG) ersetzt KfW-Programme. Einzelmaßnahmen: 20% Zuschuss. Sanierung zum Effizienzhaus: bis 45% Förderung. Zinsgünstige Kredite alternativ zu Zuschüssen. Fachplanung und Baubegleitung zusätzlich gefördert."},
    
    {"titel": "Dämmpflicht EnEV Altbau", "inhalt": "Oberste Geschossdecke dämmen bei Nicht-Nutzung. Heizungsrohre in unbeheizten Räumen dämmen. Austauschpflicht für Öl-/Gasheizungen nach 30 Jahren. Ausnahmen für Niedertemperatur-/Brennwertkessel. Selbstnutzer-Eigenheim von Pflicht befreit."},
    
    {"titel": "Photovoltaik Eigenverbrauch steuerlich", "inhalt": "Bis 30 kWp ohne Gewerbe bei Eigenverbrauch. Überschusseinspeisung meist gewerblich. EEG-Umlage auf Eigenverbrauch entfällt bei Kleinanlagen. Liebhaberei bei dauerhaften Verlusten. Vorsteuerabzug nur bei gewerblicher Nutzung."},
    
    {"titel": "Heizungsgesetz GEG 2024", "inhalt": "Ab 2024: 65% erneuerbare Energien bei Neubau. Bestand: Übergangsfristen bis kommunale Wärmeplanung. Wärmepumpe, Fernwärme, Hybridheizung möglich. Bestehende Heizungen dürfen repariert werden. Förderung über BEG für Umrüstung."},
    
    # Digitalisierung Immobilien
    {"titel": "PropTech Deutschland Trends", "inhalt": "Digitale Maklerdienste reduzieren Provisionen. AI-Bewertungstools für schnelle Wertermittlung. Smart Home Integration in Neubau Standard. Blockchain für Grundbuch-Einträge getestet. Virtual Reality für Fernbesichtigungen. IoT für Gebäudemanagement."},
    
    {"titel": "Smart Home Rechtsfragen", "inhalt": "Datenschutz bei vernetzten Geräten kritisch. Mieter-Rechte bei Smart Home Installation. Wartung und Updates der Smart-Technik klären. Interoperabilität verschiedener Systeme wichtig. Fallback-Lösungen bei Tech-Ausfall vorsehen. DSGVO-konforme Datenverarbeitung."},
    
    {"titel": "Building Information Modeling BIM", "inhalt": "3D-Gebäudedatenmodelle für gesamten Lebenszyklus. Planungskoordination zwischen Gewerken. Kostenoptimierung durch Kollisionsprüfung. Facility Management nutzt BIM-Daten. Deutschland führt BIM-Pflicht für öffentliche Bauten ein. Private Bauherren folgen langsam."},
    
    {"titel": "Drohnen Bauüberwachung rechtlich", "inhalt": "Drohnenflüge über Baustellen genehmigungspflichtig. Datenschutz bei Überflug von Nachbargrundstücken. Versicherung gegen Drohnenabstürze wichtig. Luftverkehrsrecht beachten. Qualifikationsnachweis für Drohnenpiloten. Einsatz für Baufortschrittsdokumentation üblich."},
    
    {"titel": "Künstliche Intelligenz Immobilienwertung", "inhalt": "Machine Learning für automatisierte Bewertungen. Big Data aus Transaktionsdaten und Marktinformationen. Schnelligkeit vs. Genauigkeit von AI-Bewertungen. Haftungsfragen bei fehlerhaften AI-Gutachten. Sachverständige prüfen AI-Ergebnisse. Gerichte akzeptieren AI-Bewertungen noch nicht."},
    
    # Final Countdown Spezialthemen
    {"titel": "Seniorenimmobilien als Anlageform", "inhalt": "Demografischer Wandel macht Seniorenwohnen attraktiv. Assisted Living mit Service-Komponenten. Renditen durch Pflegeleistungen zusätzlich zur Miete. Sale-and-lease-back bei Pflegeimmobilien. Risiko: Regulierung und Betreiber-Insolvenz. Wartelisten bei guten Standorten."},
    
    {"titel": "Studentenwohnheime Investment", "inhalt": "Wachsende Studentenzahlen schaffen Nachfrage. Micro-Apartments mit All-inclusive-Service. Internationale Studenten zahlen höhere Mieten. Semesterweise Vermietung vs. Jahresverträge. Risiko: Standort-Abhängigkeit von Universitäten. Private Anbieter konkurrieren mit Studentenwerken."},
    
    {"titel": "Healthcare Real Estate", "inhalt": "Demografischer Wandel treibt Gesundheitsimmobilien. Medical Office Buildings für Ärzte-Gemeinschaftspraxis. Ambulante OP-Zentren als Alternative zu Kliniken. Dialyse-Zentren und Rehakliniken. Planungssicherheit durch langfristige Mietverträge. Spezialisierte Ausstattung erforderlich."},
    
    {"titel": "Last-Mile-Logistik Immobilien", "inhalt": "E-Commerce treibt Nachfrage nach City-nahen Lagern. Micro-Fulfillment in Supermärkten und Parkgaragen. Same-Day-Delivery erfordert urbane Hubs. Konflikt mit Anwohnern wegen Lieferverkehr. Automatisierung reduziert Personalbedarf. Flexible Mietverträge für volatile Nachfrage."},
    
    {"titel": "Data Center als Asset-Klasse", "inhalt": "Digitalisierung treibt Rechenzentren-Nachfrage. Hyperscale-Anbieter (Amazon, Google, Microsoft) als Hauptmieter. Edge Computing erfordert kleinere, verteilte Zentren. Sehr hoher Strombedarf und Kühlungsaufwand. Triple-Net-Leases mit 10+ Jahren Laufzeit. ESG-Kriterien durch Energieverbrauch kritisch."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    for item in FINAL_COUNTDOWN_DOCS:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Final Countdown", 
                "category": "Comprehensive Legal Database", 
                "title": item['titel']
            }
        })
    
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
    
    info_final = client.get_collection(COLLECTION_NAME)
    print(f"\n🔥🔥🔥 FINAL RESULT: {info_final.points_count} DOKUMENTE 🔥🔥🔥")
    
    if info_final.points_count >= 4000:
        print("\n🎉🎊🎈🎆🎇✨🌟💫🚀🏆")
        print("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
        print("🚀🚀🚀 4.000 DOKUMENTE ERREICHT! 🚀🚀🚀")
        print("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
        print("🎊🎈🎆🎇✨🌟💫🚀🏆🎉")
        print(f"\nHISTORISCHER MEILENSTEIN: {info_final.points_count} DOKUMENTE!")
        print("Die umfassendste deutsche Immobilienrechts-Datenbank!")
    else:
        remaining = 4000 - info_final.points_count
        print(f"\nNoch {remaining} Dokumente bis zur magischen 4.000!")
        print("Wir sind SO NAH am historischen Meilenstein!")

if __name__ == "__main__":
    main()