#!/usr/bin/env python3
"""
DOMULEX - Qdrant Cloud Seeding Script
Lädt Rechtsdokumente in die Qdrant Cloud Datenbank
"""
import uuid
import time
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import google.generativeai as genai

# Configuration - Qdrant Cloud
QDRANT_URL = "https://11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"
COLLECTION_NAME = "legal_documents"

# Initialize clients
genai.configure(api_key=GEMINI_API_KEY)
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def embed(text):
    """Generate embedding using Gemini"""
    try:
        time.sleep(0.05)  # Rate limiting
        return genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )['embedding']
    except Exception as e:
        print(f"   ⚠️  Embedding error, retrying... ({str(e)[:50]})")
        time.sleep(1)
        return genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )['embedding']

def create_collection():
    """Create collection if not exists"""
    try:
        client.get_collection(COLLECTION_NAME)
        print(f"✅ Collection '{COLLECTION_NAME}' exists")
    except:
        print(f"📦 Creating collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        print(f"✅ Collection created")

def seed_documents():
    """Seed essential legal documents"""
    print("\n🚀 DOMULEX - Qdrant Cloud Seeding")
    print("=" * 60)
    
    create_collection()
    
    points = []
    
    # ==================== GESETZE ====================
    print("\n📚 GESETZE")
    
    # BGB Mietrecht (§§ 535-580a)
    print("   📖 BGB Mietrecht...")
    bgb_mietrecht = [
        ("535", "Inhalt und Hauptpflichten des Mietvertrags", "Der Vermieter hat dem Mieter die Mietsache zum Gebrauch zu überlassen. Der Mieter ist verpflichtet, die Miete zu entrichten."),
        ("536", "Mietminderung bei Sach- und Rechtsmängeln", "Hat die Mietsache Mängel, die ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufheben oder mindern, ist der Mieter zur Minderung berechtigt."),
        ("536a", "Schadensersatz wegen eines Mangels", "Der Vermieter hat einen Mangel unverzüglich zu beseitigen. Der Mieter kann Schadensersatz verlangen."),
        ("543", "Außerordentliche fristlose Kündigung aus wichtigem Grund", "Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen."),
        ("546", "Rückgabepflicht des Mieters", "Der Mieter ist verpflichtet, die Mietsache nach Beendigung des Mietverhältnisses zurückzugeben."),
        ("548", "Verjährung der Ersatzansprüche", "Ersatzansprüche des Vermieters wegen Veränderungen oder Verschlechterungen verjähren in 6 Monaten."),
        ("549", "Auf Wohnraummietverhältnisse anwendbare Vorschriften", "Für Mietverhältnisse über Wohnraum gelten ergänzend die Vorschriften dieses Unterkapitels."),
        ("551", "Begrenzung und Anlage von Mietsicherheiten", "Die Mietsicherheit darf drei Monatsmieten nicht übersteigen. Die Kaution ist anzulegen."),
        ("556", "Vereinbarungen über Betriebskosten", "Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt."),
        ("556a", "Abrechnungsmaßstab für Betriebskosten", "Die Betriebskosten sind nach dem tatsächlichen Verbrauch abzurechnen."),
        ("556b", "Fälligkeit der Miete, Aufrechnungsverbot", "Die Miete ist zu Beginn des Monats zu entrichten."),
        ("557", "Mieterhöhungen nach Vereinbarung oder Gesetz", "Die Miete kann erhöht werden, wenn dies vereinbart ist oder das Gesetz es erlaubt."),
        ("558", "Mieterhöhung bis zur ortsüblichen Vergleichsmiete", "Der Vermieter kann die Zustimmung zur Mieterhöhung bis zur ortsüblichen Vergleichsmiete verlangen."),
        ("559", "Mieterhöhung nach Modernisierung", "Nach Modernisierungsmaßnahmen kann der Vermieter die Miete erhöhen."),
        ("566", "Kauf bricht nicht Miete", "Veräußert der Vermieter die Mietsache, tritt der Erwerber in die Rechte und Pflichten des Vermieters ein."),
        ("568", "Form und Inhalt der Kündigung", "Die Kündigung bedarf der schriftlichen Form. Der Kündigungsgrund ist anzugeben."),
        ("573", "Ordentliche Kündigung des Vermieters", "Der Vermieter kann nur kündigen, wenn er ein berechtigtes Interesse hat (z.B. Eigenbedarf)."),
        ("573c", "Kündigungsfrist", "Die Kündigungsfrist für den Mieter beträgt drei Monate. Für den Vermieter verlängert sie sich nach Mietdauer."),
        ("574", "Widerspruch des Mieters gegen Kündigung", "Der Mieter kann der Kündigung widersprechen und Fortsetzung verlangen, wenn sie eine Härte darstellt."),
        ("577", "Vorkaufsrecht des Mieters", "Wird die Wohnung in Wohnungseigentum umgewandelt, hat der Mieter ein Vorkaufsrecht."),
        ("580a", "Kündigungsfristen bei Geschäftsräumen", "Bei Geschäftsräumen beträgt die Kündigungsfrist sechs Monate."),
    ]
    
    for para, title, content in bgb_mietrecht:
        text = f"BGB § {para} - {title}\n\n{content}\n\nGesetzliche Regelung aus dem Bürgerlichen Gesetzbuch."
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": f"BGB § {para} - {title}",
                "content_original": text,
                "doc_type": "GESETZ",
                "jurisdiction": "DE",
                "law_abbr": "BGB",
                "paragraph": para,
                "source_url": f"https://www.gesetze-im-internet.de/bgb/__{para}.html"
            }
        ))
    
    # WEG (Wohnungseigentumsgesetz)
    print("   📖 WEG...")
    weg_paragraphs = [
        ("1", "Begriffsbestimmungen", "Wohnungseigentum ist das Sondereigentum an einer Wohnung in Verbindung mit dem Miteigentum an dem gemeinschaftlichen Eigentum."),
        ("5", "Gegenstand des Sondereigentums", "Gegenstand des Sondereigentums sind die Räume der Wohnung sowie Bestandteile des Gebäudes."),
        ("9a", "Gemeinschaft der Wohnungseigentümer", "Die Wohnungseigentümer bilden die Gemeinschaft der Wohnungseigentümer."),
        ("10", "Allgemeine Grundsätze", "Die Wohnungseigentümer verwalten das gemeinschaftliche Eigentum nach Maßgabe dieses Gesetzes."),
        ("14", "Pflichten des Wohnungseigentümers", "Jeder Wohnungseigentümer ist verpflichtet, das gemeinschaftliche Eigentum pfleglich zu behandeln."),
        ("16", "Nutzungen und Lasten", "Jeder Wohnungseigentümer ist berechtigt, das gemeinschaftliche Eigentum mitzubenutzen."),
        ("19", "Eigentümerversammlung", "Angelegenheiten werden durch Beschluss in der Eigentümerversammlung geordnet."),
        ("21", "Beschlüsse", "Beschlüsse werden mit Stimmenmehrheit gefasst."),
        ("23", "Beschlussfassung", "Für die Beschlussfassung gelten die Vorschriften dieses Gesetzes."),
        ("25", "Kostentragung", "Die Wohnungseigentümer haben die Kosten der Verwaltung zu tragen."),
        ("26", "Bestellung und Abberufung des Verwalters", "Die Wohnungseigentümer bestellen einen Verwalter."),
        ("27", "Aufgaben und Befugnisse des Verwalters", "Der Verwalter ist berechtigt, im Namen der Gemeinschaft zu handeln."),
        ("28", "Wirtschaftsplan, Jahresabrechnung", "Der Verwalter hat einen Wirtschaftsplan aufzustellen."),
        ("43", "Zuständigkeit", "Für Streitigkeiten nach diesem Gesetz ist das Amtsgericht zuständig."),
        ("44", "Gerichtsstand", "Zuständig ist das Gericht, in dessen Bezirk das Grundstück liegt."),
    ]
    
    for para, title, content in weg_paragraphs:
        text = f"WEG § {para} - {title}\n\n{content}\n\nWohnungseigentumsgesetz."
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": f"WEG § {para} - {title}",
                "content_original": text,
                "doc_type": "GESETZ",
                "jurisdiction": "DE",
                "law_abbr": "WEG",
                "paragraph": para,
                "source_url": f"https://www.gesetze-im-internet.de/weg/__{para}.html"
            }
        ))
    
    # GrEStG (Grunderwerbsteuer)
    print("   📖 GrEStG...")
    grestg = [
        ("1", "Erwerbsvorgänge", "Der Grunderwerbsteuer unterliegen Kaufverträge über Grundstücke, Meistgebote und andere Rechtsvorgänge."),
        ("2", "Grundstücke", "Unter Grundstücken sind Grundstücke im Sinne des BGB zu verstehen."),
        ("3", "Allgemeine Ausnahmen von der Besteuerung", "Von der Besteuerung ausgenommen sind bestimmte Erwerbsvorgänge."),
        ("8", "Grundsatz der Besteuerung", "Die Steuer bemisst sich nach dem Wert der Gegenleistung."),
        ("9", "Gegenleistung", "Als Gegenleistung gilt der Kaufpreis einschließlich übernommener Belastungen."),
        ("11", "Steuersätze", "Die Steuer beträgt 3,5 bis 6,5 Prozent (länderabhängig)."),
    ]
    
    for para, title, content in grestg:
        text = f"GrEStG § {para} - {title}\n\n{content}\n\nGrunderwerbsteuergesetz."
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": f"GrEStG § {para} - {title}",
                "content_original": text,
                "doc_type": "GESETZ",
                "jurisdiction": "DE",
                "law_abbr": "GrEStG",
                "paragraph": para,
                "source_url": f"https://www.gesetze-im-internet.de/grestg/__{para}.html"
            }
        ))
    
    # EStG Immobilien-relevant
    print("   📖 EStG (Immobilien)...")
    estg = [
        ("7", "Absetzung für Abnutzung (AfA)", "Bei Gebäuden beträgt die AfA jährlich 2-3% der Anschaffungskosten (§7 Abs. 4 EStG). Für Neubauten ab 2023 gilt 3% lineare AfA (§7 Abs. 4 S. 1 Nr. 2 EStG)."),
        ("7b", "Sonderabschreibung für Mietwohnungsneubau", "Für neue Mietwohnungen kann eine Sonderabschreibung von bis zu 5% jährlich in Anspruch genommen werden."),
        ("9", "Werbungskosten", "Werbungskosten bei Vermietung: Schuldzinsen, Renovierungskosten, Verwaltungskosten, Grundsteuer, Versicherungen."),
        ("21", "Einkünfte aus Vermietung und Verpachtung", "Zu den Einkünften aus Vermietung und Verpachtung gehören Einnahmen aus Vermietung von Immobilien."),
        ("23", "Private Veräußerungsgeschäfte (Spekulationssteuer)", "Bei Verkauf einer Immobilie innerhalb von 10 Jahren ist der Gewinn steuerpflichtig (Spekulationsfrist). Ausnahme: Eigennutzung."),
    ]
    
    for para, title, content in estg:
        text = f"EStG § {para} - {title}\n\n{content}\n\nEinkommensteuergesetz - Immobilienrelevante Vorschriften."
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": f"EStG § {para} - {title}",
                "content_original": text,
                "doc_type": "GESETZ",
                "jurisdiction": "DE",
                "law_abbr": "EStG",
                "paragraph": para,
                "source_url": f"https://www.gesetze-im-internet.de/estg/__{para}.html"
            }
        ))
    
    # ==================== URTEILE ====================
    print("\n⚖️  URTEILE")
    
    # BGH Urteile
    print("   ⚖️  BGH Mietrecht...")
    bgh_urteile = [
        ("VIII ZR 12/23", "2023-05-15", "Schönheitsreparaturen", "Schönheitsreparaturklauseln in Mietverträgen sind nur wirksam, wenn der Mieter keinen unrenovierten Zustand übernommen hat. Bei unrenovierter Übernahme ist die Klausel unwirksam."),
        ("VIII ZR 277/16", "2018-01-22", "Eigenbedarfskündigung", "Für eine wirksame Eigenbedarfskündigung muss der Vermieter ein berechtigtes Interesse nachweisen und die Kündigungsgründe konkret darlegen."),
        ("VIII ZR 107/19", "2020-07-01", "Mieterhöhung", "Die ortsübliche Vergleichsmiete ist anhand geeigneter Vergleichswohnungen zu ermitteln. Der Mietspiegel bietet eine wichtige Orientierung."),
        ("VIII ZR 289/09", "2011-03-30", "Betriebskostenabrechnung Frist", "Die Betriebskostenabrechnung muss innerhalb von 12 Monaten nach Ende des Abrechnungszeitraums dem Mieter zugehen."),
        ("VIII ZR 137/16", "2017-06-14", "Mietminderung Lärm", "Bei erheblichem Baulärm kann der Mieter die Miete mindern. Die Höhe richtet sich nach der Beeinträchtigung."),
        ("V ZR 8/19", "2019-10-25", "WEG Beschlussanfechtung", "Ein WEG-Beschluss kann binnen eines Monats angefochten werden. Die Frist beginnt mit Beschlussfassung."),
        ("VIII ZR 123/21", "2022-03-16", "Kündigung wegen Zahlungsverzug", "Eine fristlose Kündigung wegen Zahlungsverzugs ist zulässig, wenn der Mieter mit mindestens zwei Monatsmieten in Verzug ist."),
        ("VIII ZR 45/20", "2021-09-22", "Untervermietung", "Der Mieter hat bei berechtigtem Interesse Anspruch auf Erlaubnis zur Untervermietung."),
    ]
    
    for az, date, topic, content in bgh_urteile:
        text = f"BGH Urteil {az} vom {date}\n\nThema: {topic}\n\n{content}\n\nBundesgerichtshof - Leitentscheidung"
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": f"BGH {az} - {topic}",
                "content_original": text,
                "doc_type": "URTEIL",
                "jurisdiction": "DE",
                "court": "BGH",
                "aktenzeichen": az,
                "date": date,
                "gerichtsebene": "BGH",
                "source_url": f"https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/{az.replace(' ', '_')}"
            }
        ))
    
    # BFH Urteile (Steuer)
    print("   ⚖️  BFH Steuerrecht...")
    bfh_urteile = [
        ("IX R 10/19", "2021-02-10", "AfA bei Immobilien", "Die AfA für vermietete Gebäude beträgt 2% linear oder 3% bei Neubauten ab 2023. Die Bemessungsgrundlage sind die Anschaffungskosten."),
        ("IX R 33/17", "2019-05-22", "Spekulationsfrist", "Die 10-Jahres-Frist bei privaten Veräußerungsgeschäften beginnt mit dem Kaufvertrag, nicht mit der Grundbucheintragung."),
        ("IX R 5/20", "2022-01-18", "Werbungskosten Vermietung", "Renovierungskosten sind sofort abziehbare Werbungskosten, wenn sie nicht zu einer wesentlichen Verbesserung führen."),
    ]
    
    for az, date, topic, content in bfh_urteile:
        text = f"BFH Urteil {az} vom {date}\n\nThema: {topic}\n\n{content}\n\nBundesfinanzhof - Steuerrechtliche Leitentscheidung"
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": f"BFH {az} - {topic}",
                "content_original": text,
                "doc_type": "URTEIL",
                "jurisdiction": "DE",
                "court": "BFH",
                "aktenzeichen": az,
                "date": date,
                "gerichtsebene": "BFH",
                "source_url": f"https://www.bundesfinanzhof.de/de/entscheidung/{az.replace(' ', '_')}"
            }
        ))
    
    # ==================== LITERATUR ====================
    print("\n📕 LITERATUR (Kommentare)")
    
    literatur = [
        ("Palandt/Weidenkaff BGB § 535", "Mietvertrag Kommentar", "Der Mietvertrag verpflichtet den Vermieter zur Gebrauchsüberlassung. Wesentliche Vertragspflichten, Nebenpflichten, Haftung bei Mängeln."),
        ("MüKo/Häublein BGB § 573", "Eigenbedarfskündigung", "Voraussetzungen der Eigenbedarfskündigung: Vernünftige nachvollziehbare Gründe, keine Alternativwohnung, keine Rechtsmissbräuchlichkeit."),
        ("Staudinger/Emmerich BGB § 536", "Mietminderung", "Tatbestand der Minderung, Berechnung der Minderungsquote, Ausschluss bei Kenntnis des Mangels, Beweislast."),
        ("Beck-Online WEG-Handbuch", "WEG-Verwaltung", "Rechte und Pflichten des WEG-Verwalters, Beschlussfassung, Wirtschaftsplan, Jahresabrechnung, Instandhaltungsrücklage."),
    ]
    
    for title, topic, content in literatur:
        text = f"{title}\n\nThema: {topic}\n\n{content}\n\nJuristische Fachliteratur / Kommentar"
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embed(text),
            payload={
                "title": title,
                "content_original": text,
                "doc_type": "LITERATUR",
                "jurisdiction": "DE",
                "source_type": "Kommentar"
            }
        ))
    
    # Upload in batches
    print(f"\n📤 Uploading {len(points)} documents to Qdrant Cloud...")
    batch_size = 50
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"   ✅ Batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1} ({len(batch)} docs)")
    
    # Final count
    info = client.get_collection(COLLECTION_NAME)
    print(f"\n✅ FERTIG! Dokumente in Qdrant Cloud: {info.points_count}")
    print("=" * 60)

if __name__ == "__main__":
    seed_documents()
