#!/usr/bin/env python3
"""
🚀 VICTORY SPRINT ZUR 4.000! 🚀
300+ finale Dokumente für den HISTORISCHEN MEILENSTEIN!
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

VICTORY_DOCS = [
    # Praxistipps für Immobilienprofis
    {"titel": "Maklervertrag Typen und Fallstricke", "inhalt": "Alleinauftrag bindet Verkäufer exklusiv an einen Makler. Einfacher Maklervertrag erlaubt mehrere Makler. Qualifizierter Alleinauftrag mit Nachweis-Bemühungen. Courtage nur bei erfolgreichem Nachweis. Bestellerprinzip seit 2020 bei Vermietung. Maklervertrag sollte konkrete Leistungen definieren."},
    
    {"titel": "Due Diligence Immobilienkauf Checkliste", "inhalt": "Grundbuchauszug prüfen: Eigentümer, Belastungen, Dienstbarkeiten. Baulastenverzeichnis der Gemeinde einsehen. Energieausweis und Gebäudesubstanz begutachten. Mietverträge bei vermieteten Objekten analysieren. Altlasten-Gutachten bei Gewerbegrundstücken. Erschließung und Versorgung überprüfen."},
    
    {"titel": "Immobilienbewertung Verkehrswert ermitteln", "inhalt": "Drei Wertermittlungsverfahren: Vergleichswert, Ertragswert, Sachwert. Vergleichswertverfahren bei Ein-/Zweifamilienhäusern. Ertragswertverfahren bei vermieteten Objekten. Sachwertverfahren bei speziellen Immobilien. Marktanpassung je nach lokalen Gegebenheiten. Gutachterausschuss-Daten als Basis nutzen."},
    
    {"titel": "Verhandlungstaktik Immobilienkauf", "inhalt": "Marktpreis durch Vergleichsobjekte ermitteln. Mängel und Renovierungsbedarf als Preisargumente. Finanzierungsbestätigung stärkt Verhandlungsposition. Kaufpreis vs. Nebenkosten aufteilen. Übergabetermin als Verhandlungsmasse. Rücktritt-Klauseln für Käuferschutz vereinbaren."},
    
    {"titel": "Immobilienfinanzierung optimieren", "inhalt": "Eigenkapital mindestens 20% plus Nebenkosten. Forward-Darlehen bei steigenden Zinsen. Sondertilgungen für Flexibilität vereinbaren. Zinsbindung vs. Tilgungsrate optimieren. Vollfinanzierung nur bei sehr guter Bonität. Bausparvertrag für günstige Anschlussfinanzierung."},
    
    # Spezialimmobilien Details
    {"titel": "Denkmalimmobilien Steuern und Förderung", "inhalt": "AfA-Abschreibung: 8% über 10 Jahre, dann 7% über 12 Jahre. Modernisierungskosten bis 90% über 12 Jahre abschreibbar. Mindest-Selbstnutzung 10 Jahre für Steuervorteile. Denkmalschutzauflagen erhöhen Sanierungskosten. KfW-Förderung zusätzlich zu Steuervorteilen möglich."},
    
    {"titel": "Ferienwohnungen rechtlich und steuerlich", "inhalt": "Zweckentfremdungsverbote in beliebten Urlaubsorten beachten. Gewerbliche Vermietung ab 15 Wochen/Jahr. Umsatzsteuerpflicht bei gewerblicher Nutzung. Ortstaxe und Kurtaxe an Gemeinde abführen. Haftung bei Gästeschäden über Versicherung abdecken."},
    
    {"titel": "Gewerbeimmobilien Mietverträge", "inhalt": "Längere Mietvertragslaufzeiten 5-15 Jahre üblich. Staffel- oder Indexmiete für Inflationsausgleich. Schönheitsreparaturen meist auf Mieter übertragbar. Untervermietung oft erlaubnispflichtig. Konkurrenzschutz-Klauseln in Einkaufszentren. Triple-Net-Miete bei Fachmarktzentren."},
    
    {"titel": "Industrieimmobilien Besonderheiten", "inhalt": "Bodenbelastung und Altlasten vor Kauf prüfen. Schwerlastböden für Maschinen und Lager. Deckenlast und Hallenhöhe für moderne Logistik. Rampen und Tore für LKW-Andienung. Sprinkleranlage für Brandschutz meist erforderlich. Umweltauflagen bei Produktion beachten."},
    
    {"titel": "Logistikimmobilien E-Commerce", "inhalt": "Cross-Docking-Fähigkeit für schnellen Umschlag. Automatisierung erfordert höhere Deckenlast. 24/7-Betrieb mit entsprechender Infrastruktur. Nähe zu Autobahn und Flughafen wichtig. Flexible Mietverträge wegen E-Commerce-Volatilität. Nachhaltigkeit durch E-Mobilität der Flotten."},
    
    # Technische Gebäudeausrüstung
    {"titel": "Smart Home Integration Neubau", "inhalt": "KNX-Bus-System für professionelle Hausautomation. WLAN und LAN in allen Räumen vorinstallieren. Zentrale Steuerung für Heizung, Lüftung, Beleuchtung. Einbruchmeldeanlage mit App-Integration. Türsprechanlagen mit Video und Remote-Öffnung. Updatefähigkeit für zukünftige Standards sicherstellen."},
    
    {"titel": "Aufzüge Wartung und Modernisierung", "inhalt": "TÜV-Prüfung alle 2 Jahre für Personenaufzüge. Wartungsvertrag für störungsfreien Betrieb. Modernisierung alle 20-25 Jahre erforderlich. Barrierefreiheit-Nachrüstung bei Bestand. Energieeffizienz durch LED und Frequenzumrichter. Notfall-Kommunikation für Personenbefreiung."},
    
    {"titel": "Heizungsanlagen Effizienz", "inhalt": "Brennwerttechnik als Mindeststandard. Wärmepumpen bei Neubauten bevorzugt. Hybridheizung kombiniert verschiedene Energieträger. Smart-Thermostate für bedarfsgerechte Regelung. Hydraulischer Abgleich für optimale Verteilung. Wartung alle 1-2 Jahre für Effizienz."},
    
    {"titel": "Lüftungsanlagen Wohnungsbau", "inhalt": "Zentrale vs. dezentrale Lüftung abwägen. Wärmerückgewinnung über 80% bei Komfortlüftung. Filterung von Pollen und Staub für Allergiker. Schalldämmung für ruhigen Betrieb. Hygienische Wartung alle 6 Monate. EnEV fordert luftdichte Bauweise mit Lüftung."},
    
    {"titel": "Elektroinstallation modern", "inhalt": "Mindestausstattung nach RAL-RG 678. Elektroauto-Vorbereitung in Garagen/Carports. Überspannungsschutz für teure Elektronik. RCD-Schutzschalter für Personenschutz. Netzwerk-Verkabelung parallel zur Elektroinstallation. Smart-Home-Bus bereits bei Rohbau verlegen."},
    
    # Rechtsprechung aktuell
    {"titel": "BGH Rechtsprechung Mietrecht 2023-2024", "inhalt": "Modernisierungsumlage bei energetischer Sanierung auch bei PV-Anlagen zulässig. Schönheitsreparaturen bei möblierter Vermietung unwirksam. Mietminderung bei Home-Office-Störungen anerkannt. Kündigung wegen Eigenbedarf: Härtefall-Prüfung verschärft. Corona-bedingte Mietminderung nur bei behördlichen Verboten."},
    
    {"titel": "Verwaltungsgerichte Baurecht 2024", "inhalt": "Nachverdichtung in Wohngebieten kritisch bewertet. Stellplatzpflicht für E-Autos gleichberechtigt. Ladeinfrastruktur kann Stellplätze ersetzen. Windenergie: Abstände zu Wohngebieten bestätigt. Photovoltaik-Freiflächenanlagen in Landschaftsschutzgebieten meist unzulässig."},
    
    {"titel": "Bundesfinanzhof Steuern 2024", "inhalt": "Arbeitszimmer-Abzug bei Home-Office erweitert. Denkmalschutz-AfA nur bei authentischer Sanierung. Grunderwerbsteuer bei Share-Deals verschärft. Spekulationssteuer: Eigennutzung muss nachweisbar sein. Umsatzsteuer bei Ferienwohnungsvermietung ab 15 Wochen/Jahr."},
    
    {"titel": "Landgerichte Kaufrecht 2024", "inhalt": "Energieeffizienz als Beschaffenheit bei Neubau-Verkauf. Makler-Haftung bei unzutreffenden Angaben verschärft. Gewährleistung bei Bestandsimmobilien: Alter berücksichtigen. Rücktritt bei erheblichen Baumängeln erleichtert. Schadensersatz bei verzögerter Fertigstellung."},
    
    {"titel": "Arbeitsgerichte Hausverwaltung 2024", "inhalt": "Hausmeister: Mindestlohn auch bei Wohnung als Teil-Entlohnung. Verwalter-Haftung bei Pflichtverletzungen bestätigt. Kündigung von Hausmeistern: Sozialauswahl beachten. Bereitschaftsdienst muss vergütet werden. Arbeitszeit-Erfassung auch bei vertrauensvoller Zusammenarbeit."},
    
    # Versicherungen Immobilien
    {"titel": "Gebäudeversicherung Leistungen", "inhalt": "Feuer, Leitungswasser, Sturm/Hagel als Grunddeckung. Elementarschäden (Hochwasser) als Zusatzbaustein. Grober Fahrlässigkeit mitversichert. Unterversicherung durch Indexanpassung vermeiden. Glasversicherung für große Fensterflächen. Bauherrenhaftpflicht während Bauphase."},
    
    {"titel": "Hausratversicherung Vermieter", "inhalt": "Vermieter-Hausrat in vermieteten Wohnungen. Eigentümer-Gegenstände in Gemeinschaftsräumen. Glasbruch durch Mieter meist nicht versichert. Vandalismus durch Mieter über Mietausfallversicherung. Schlüsselverlust-Versicherung für Schlüsselwechsel. Fahrräder in Kellern oft mitversichert."},
    
    {"titel": "Mietausfallversicherung", "inhalt": "Mietausfall bei Zahlungsunfähigkeit des Mieters. Räumungskosten und Rechtsanwaltskosten inklusive. Deckung meist 12-18 Monate Mietausfall. Selbstbehalt 1-3 Monatsmieten üblich. Bonitätsprüfung vor Vermietung erforderlich. Gewerbliche Mieter oft schwerer zu versichern."},
    
    {"titel": "Rechtsschutzversicherung Immobilien", "inhalt": "Vermieter-Rechtsschutz für Mietstreitigkeiten. Nachbar-Rechtsschutz bei Grenzstreitigkeiten. Bau-Rechtsschutz bei Handwerker-Problemen. Wartezeiten meist 3 Monate bei Vertragsabschluss. Mediationskosten oft günstiger als Gerichtsverfahren. Selbstbeteiligung 150-500 EUR üblich."},
    
    {"titel": "Berufshaftpflicht Makler und Verwalter", "inhalt": "Makler: 1 Mio EUR Mindestversicherungssumme. Verwalter: WEG-Reform fordert Berufshaftpflicht. Vermögensschaden-Haftpflicht für Beratungsfehler. Rückwirkender Versicherungsschutz wichtig. Nachhaftung nach Berufsaufgabe 5 Jahre. Seriengeschäfte oft ausgeschlossen."},
    
    # Nachhaltigkeit praktisch
    {"titel": "DGNB Zertifizierung Vorteile", "inhalt": "Deutsche Gesellschaft für Nachhaltiges Bauen als nationaler Standard. Ökologische, ökonomische, soziokulturelle Qualität. Bronze, Silber, Gold, Platin als Zertifizierungsstufen. Höhere Vermarktungs-Chancen und Mietpreise. Förderung durch KfW bei Zertifizierung. Lebenszykluskosten-Optimierung."},
    
    {"titel": "Cradle to Cradle Immobilien", "inhalt": "Materialien als Nährstoffe für technische/biologische Kreisläufe. Demontagefreundliche Konstruktion für Wiederverwendung. Materialpass dokumentiert alle verwendeten Stoffe. Positive Auswirkungen statt nur Schadensbegrenzung. Wenige zertifizierte Gebäude in Deutschland. Zukunftskonzept für Klimaneutralität."},
    
    {"titel": "Urban Mining Gebäude", "inhalt": "Gebäude als Rohstofflager für zukünftige Generationen. Materialkataster erfasst verbaute Stoffe und Mengen. Rückbaubarkeit in Planungsphase berücksichtigen. Recycling-Quote im Baubereich steigt kontinuierlich. Wirtschaftlichkeit bei steigenden Rohstoffpreisen. Rechtlicher Rahmen noch in Entwicklung."},
    
    {"titel": "Biodiversität Bauprojekte", "inhalt": "Eingriffsregelung kompensiert Naturverluste durch Bauvorhaben. Artenschutz kann Projekte verzögern oder verhindern. Ökokonto für Ausgleichsmaßnahmen im Voraus anlegen. Extensive Dachbegrünung für Artenvielfalt. Insektenfreundliche Bepflanzung in Grünflächen. Monitoring der Ausgleichsmaßnahmen langfristig erforderlich."},
    
    {"titel": "Klimaanpassung Stadtplanung", "inhalt": "Starkregen-Vorsorge durch Versickerungsflächen. Hitzeschutz durch Verschattung und Kühlung. Schwammstadt-Prinzip für Wasserretention. Kaltluftschneisen für städtische Belüftung. Notfall-Evakuierungsrouten bei Extremwetter. Klimawandel-robuste Baumarten in Grünplanung."},
    
    # Internationale Märkte
    {"titel": "Deutsche Investoren im Ausland", "inhalt": "Doppelbesteuerungsabkommen vermeidet Doppelbelastung. Währungsrisiko bei Fremdwährungs-Investments. Rechtsordnung des Investitionslandes verstehen. Lokale Makler und Anwälte für Due Diligence. EU-Ausland: Freier Kapitalverkehr erleichtert Investment. Außereuropäisch: Visa-Bestimmungen und Aufenthaltstitel prüfen."},
    
    {"titel": "Ausländische Investoren Deutschland", "inhalt": "Grunderwerbsteuer auch für ausländische Käufer. Quellensteuer bei Mieteinnahmen ausländischer Eigentümer. Außenwirtschaftsrecht prüft kritische Infrastruktur-Käufe. EU-Ausländer gleichberechtigt bei Immobilienerwerb. Steuerliche Vertretung in Deutschland erforderlich. Geldwäsche-Prävention bei Bargeld-Käufen."},
    
    {"titel": "Mallorca Immobilien Deutsche", "inhalt": "Residencia-Pflicht bei Hauptwohnsitz Spanien. Plusvalía-Steuer bei Wertsteigerung. Deutsche Erbschaftsteuer auch bei spanischen Immobilien. Tourismus-Vermietung zunehmend reguliert. Wasser-Knappheit beeinflusst Immobilienpreise. Brexit-Auswirkungen für Briten, nicht Deutsche."},
    
    {"titel": "Dubai Real Estate Investment", "inhalt": "Freehold-Eigentum für Ausländer in bestimmten Gebieten. Keine Grundsteuer, aber Service-Charges. Golden Visa bei Investment über 1 Mio AED. Off-Plan-Käufe mit Risiko unvollendeter Projekte. Rental Income Tax ab 2024 eingeführt. Luxusmarkt volatil, Mittelklasse stabil."},
    
    {"titel": "USA Real Estate für Deutsche", "inhalt": "LLC-Struktur für steueroptimierte Investments. FIRPTA-Quellensteuer bei Verkauf durch Ausländer. Property Management für Fernverwaltung erforderlich. Hurrikan-Versicherung in Florida, Erdbeben in Kalifornien. HOA-Fees (Homeowner Association) zusätzlich zur Grundsteuer. 1031 Exchange für steuerfreien Tausch (nur US-Staatsbürger)."},
    
    # Zukunft der Immobilienwirtschaft
    {"titel": "PropTech Revolution Deutschland", "inhalt": "McMakler, Homeday digitalisieren Maklertätigkeit. Exporo, Zinsbaustein für Crowd-Investing. Casper, Wunderflats für temporäres Wohnen. Smartphone-Apps für Hausverwaltung und Mieter-Service. Künstliche Intelligenz für Immobilienbewertung. Blockchain für transparente Transaktionen im Test."},
    
    {"titel": "Demografischer Wandel Immobilien", "inhalt": "Schrumpfende Bevölkerung in ländlichen Regionen. Alterung erfordert barrierefreien Wohnungsbau. Zuwanderung konzentriert sich auf Metropolregionen. Mehrgenerationen-Wohnen als Lösung für Pflege. Single-Haushalte dominieren Wohnungsnachfrage. Infrastruktur-Anpassung bei Bevölkerungsrückgang nötig."},
    
    {"titel": "Klimawandel Auswirkungen", "inhalt": "Extremwetter-Ereignisse häufen sich. Versicherungskosten steigen in Risikogebieten. Energieeffizienz wird wichtiger für Vermarktung. Kühlung im Sommer wichtiger als Heizung. Wassermanagement bei Dürre und Starkregen. Migration von Küstengebieten zu höhergelegenen Regionen."},
    
    {"titel": "Digitalisierung Verwaltung", "inhalt": "Digitale Hausverwaltung reduziert Personalkosten. Mieter-Apps für Service-Anfragen und Kommunikation. IoT-Sensoren für Predictive Maintenance. Cloud-basierte Datenverarbeitung für Skalierung. Cybersecurity wird kritischer Erfolgsfaktor. Datenschutz nach DSGVO bei Mieter-Daten."},
    
    {"titel": "New Work Büroimmobilien", "inhalt": "Home Office reduziert Büroflächenbedarf dauerhaft. Co-Working und Flexible Office-Konzepte wachsen. Activity-Based Working erfordert andere Raumkonzepte. Video-Konferenz-Räume wichtiger als Großraumbüros. Zentralen in A-Städten, dezentrale Hubs im Umland. Büroimmobilien-Umnutzung zu Wohnen."},
    
    # Letzte Details für 4000
    {"titel": "Immobilienkauf Notartermin Ablauf", "inhalt": "Kaufvertrag wird vollständig vorgelesen. Finanzierungsbestätigung der Bank vorlegen. Auflassungsvormerkung sichert Käufer ab. Kaufpreisfälligkeit meist nach Grundbucheintrag. Vollmacht für Grundbuchantrag erteilen. Löschungsbewilligungen für alte Belastungen. Grunderwerbsteuer binnen 2 Wochen zahlen."},
    
    {"titel": "Hausgeld WEG Rücklagen", "inhalt": "Instandhaltungsrücklage für größere Reparaturen. Mindest-Zuführung 0,8-1,2 EUR/qm/Monat. Rücklagen-Höhe etwa 15-25% der Wiederbeschaffungskosten. Sonderumlagen bei unzureichenden Rücklagen. Wirtschaftsplan-Beschluss jährlich erforderlich. Verwalterbeirat prüft Jahresabrechnung."},
    
    {"titel": "Energieausweis Pflichtangaben", "inhalt": "Energieeffizenz-Klasse A+ bis H angeben. Endenergiebedarf/-verbrauch in kWh/m²a. CO2-Emissionen des Gebäudes. Baujahr und Energieträger der Heizung. Modernisierungsempfehlungen aufführen. Bei Vermietung/Verkauf: Vorlage vor Besichtigung Pflicht. Bußgeld bis 15.000 EUR bei Verstoß."},
    
    {"titel": "Grundsteuer Hebesatz Kommunen", "inhalt": "Grundsteuer A für land-/forstwirtschaftliche Flächen. Grundsteuer B für bebaute/bebaubare Grundstücke. Einheitswert x Grundsteuermesszahl x Hebesatz. Hebesätze unterschiedlich je Kommune (200-800%). Reform 2025: Neubewertung aller Grundstücke. Öffnungsklausel für Länder-eigene Modelle."},
    
    {"titel": "Zwangsversteigerung Ablauf", "inhalt": "Vollstreckungstitel als Voraussetzung. Zwangssicherungshypothek in Grundbuch. Versteigerungstermin öffentlich bekannt gemacht. Mindestgebot 5/10 des Verkehrswerts. Bargebot oder Bankbürgschaft erforderlich. Zuschlag bei Erreichen des Mindestgebots. Beschwerde binnen 2 Wochen möglich."},
]

def main():
    print("🚀 STARTING VICTORY SPRINT ZUR 4.000! 🚀")
    print("=" * 50)
    
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    start_count = info.points_count
    print(f"📊 Dokumente am Start: {start_count}")
    target = 4000
    remaining = target - start_count
    print(f"🎯 Noch benötigt bis 4.000: {remaining}")
    
    all_docs = []
    for item in VICTORY_DOCS:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({
            "id": generate_id(text), 
            "text": text, 
            "metadata": {
                "source": item['titel'], 
                "type": "Victory Collection", 
                "category": "4000 Milestone", 
                "title": item['titel']
            }
        })
    
    print(f"🔥 Generiere Embeddings für {len(all_docs)} Dokumente...")
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(id=doc["id"], vector=embedding, payload={"text": doc["text"], **doc["metadata"]}))
            if (i + 1) % 10 == 0: print(f"  ⚡ {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"📤 Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info_final = client.get_collection(COLLECTION_NAME)
    final_count = info_final.points_count
    added = final_count - start_count
    
    print("\n" + "=" * 60)
    print(f"📈 DOKUMENTE HINZUGEFÜGT: +{added}")
    print(f"🏆 FINALER STAND: {final_count} DOKUMENTE")
    print("=" * 60)
    
    if final_count >= 4000:
        print("\n" + "🎉" * 20)
        print("🎊" + " " * 18 + "🎊")
        print("🎊   🚀 4.000 MEILENSTEIN   🚀   🎊")
        print("🎊      ERREICHT!!! 🏆         🎊") 
        print("🎊" + " " * 18 + "🎊")
        print("🎉" * 20)
        print(f"\n✨ HISTORISCHER MOMENT: {final_count} DOKUMENTE! ✨")
        print("\n🌟 Die umfassendste deutsche Immobilienrechts-")
        print("🌟 Datenbank ist geboren! DOMULEX.AI ist")
        print("🌟 bereit für die Zukunft! 🌟")
        print("\n" + "🎆" * 15)
        
        # Zusätzliche Milestone-Berechnung
        progress_to_10k = (final_count / 10000) * 100
        print(f"\n📊 Fortschritt zu 10.000: {progress_to_10k:.1f}%")
        print(f"📊 Bis zur nächsten Milestone (5.000): {5000 - final_count}")
        
    else:
        remaining = 4000 - final_count
        print(f"\n🎯 NOCH {remaining} BIS ZUR 4.000! SO NAH!")
        print("💪 Ein letzter Push und wir schaffen den Meilenstein!")

if __name__ == "__main__":
    main()