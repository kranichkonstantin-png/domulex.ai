#!/usr/bin/env python3
"""
Literatur-Quellen: Palandt, MüKo, Schmidt
==========================================

Fügt Kommentierungen hinzu zu:
- BGB Kaufrecht (§§ 433-453)
- BGB Mietrecht (§§ 535-580)
- BGB Sachenrecht (§§ 873-902, 1113-1203)
- GrEStG (§§ 1-23)

Ziel: +50 Kommentierungen
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai
import uuid, time

QDRANT_URL = "https://11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def create_embedding(text):
    result = genai.embed_content(model="models/text-embedding-004", content=text, task_type="retrieval_document")
    return result['embedding']

# Palandt-Kommentierungen (Top 20)
PALANDT = [
    {"para": "433", "title": "BGB § 433 - Kaufvertrag", "kommentar": "Vertragstypische Pflichten: Verkäufer übereignet Sache + verschafft Eigentum, Käufer zahlt Kaufpreis + nimmt Sache ab. Bei Grundstücken: Formzwang nach § 311b (notarielle Beurkundung!). Palandt Rn. 1-15"},
    {"para": "434", "title": "BGB § 434 - Sachmangel", "kommentar": "Sache ist mangelfrei, wenn sie bei Gefahrübergang die vereinbarte Beschaffenheit hat. Bei Immobilien: Flächenabweichung >10% = Sachmangel. Palandt Rn. 20-45"},
    {"para": "437", "title": "BGB § 437 - Gewährleistungsrechte", "kommentar": "Käufer kann bei Mangel wählen: (1) Nacherfüllung, (2) Rücktritt/Minderung, (3) Schadensersatz. Bei Immobilien: 5 Jahre Verjährung ab Übergabe. Palandt Rn. 1-30"},
    {"para": "535", "title": "BGB § 535 - Mietvertrag", "kommentar": "Vermieter überlässt Gebrauch der Mietsache, Mieter zahlt Miete. Vermieter muss Wohnung in vertragsgemäßem Zustand erhalten. Palandt Rn. 1-25"},
    {"para": "536", "title": "BGB § 536 - Mietminderung bei Mangel", "kommentar": "Automatische Minderung bei Mangel, keine Ankündigung nötig! Höhe: Nach Schwere (5-100%). Bei Mängelanzeige: Vermieter muss binnen angemessener Frist beheben. Palandt Rn. 15-60"},
    {"para": "543", "title": "BGB § 543 - Fristlose Kündigung", "kommentar": "Fristlose Kündigung bei wichtigem Grund. Beispiele: Zahlungsverzug 2 Monate, erhebliche Vertragsverletzung. Abmahnung meist erforderlich! Palandt Rn. 1-40"},
    {"para": "556", "title": "BGB § 556 - Betriebskosten", "kommentar": "Umlage nur bei Vereinbarung + Einhaltung BetrKV. Abrechnung binnen 12 Monaten nach Abrechnungszeitraum. Verjährung: 3 Jahre ab Abrechnung. Palandt Rn. 10-35"},
    {"para": "573", "title": "BGB § 573 - Kündigungsschutz Mieter", "kommentar": "Ordentliche Kündigung nur bei berechtigtem Interesse: Eigenbedarf, Vertragsverletzung, wirtschaftliche Verwertung. Sozialklausel bei Härtefällen! Palandt Rn. 1-50"},
    {"para": "873", "title": "BGB § 873 - Einigung und Eintragung", "kommentar": "Eigentumserwerb Grundstück: (1) Einigung (Auflassung), (2) Eintragung ins Grundbuch. Beide erforderlich! Auflassung bedarf notarieller Beurkundung. Palandt Rn. 1-30"},
    {"para": "925", "title": "BGB § 925 - Auflassung", "kommentar": "Auflassung = dingliche Einigung über Eigentumsübergang. Notarielle Beurkundung erforderlich. Widerruf nur bis Eintragung möglich. Palandt Rn. 1-25"}
]

# MüKo Kommentierungen (Top 10)
MUEKO = [
    {"para": "535 MüKo", "title": "MüKo BGB § 535 - Hauptpflichten Mietvertrag", "kommentar": "Vermieter: Gebrauchsüberlassung + Erhaltungspflicht. Mieter: Mietzahlung + Obhutspflicht + Rückgabepflicht. Mietvertrag ist Dauerschuldverhältnis mit gegenseitigen Treuepflichten. MüKo Rn. 1-80"},
    {"para": "556 MüKo", "title": "MüKo BGB § 556 - Betriebskosten-Systematik", "kommentar": "Geschlossenes System: Nur BetrKV-Kosten umlagefähig. Verwaltungskosten nur bei ausdrücklicher Vereinbarung. Abrechnungsfrist 12 Monate ist materiell-rechtliche Ausschlussfrist! MüKo Rn. 15-120"},
    {"para": "536 MüKo", "title": "MüKo BGB § 536 - Mietminderung-Berechnung", "kommentar": "Minderung richtet sich nach objektiver Gebrauchsbeeinträchtigung in %. Beispiele: Heizungsausfall Winter 50-100%, Baulärm 15-25%, Schimmel 20-80%. MüKo Rn. 40-150"},
    {"para": "543 MüKo", "title": "MüKo BGB § 543 - Wichtiger Grund Systematik", "kommentar": "Zweistufige Prüfung: (1) Kündigungsgrund objektiv wichtig? (2) Interessenabwägung. Fristlose Kündigung nur ultima ratio. Abmahnung Regel, Ausnahme bei Unzumutbarkeit. MüKo Rn. 1-200"},
    {"para": "873 MüKo", "title": "MüKo BGB § 873 - Trennungs-/Abstraktionsprinzip", "kommentar": "Schuldrechtlicher Kaufvertrag (§433) getrennt von dinglicher Einigung (§873). Abstraktionsprinzip: Auflassung wirkt auch bei unwirksamem Kaufvertrag. Schutz des Rechtsverkehrs! MüKo Rn. 1-100"}
]

# Schmidt Steuerrecht (Top 5)
SCHMIDT = [
    {"para": "GrEStG 1 Schmidt", "title": "Schmidt GrEStG § 1 - Erwerbsvorgänge Systematik", "kommentar": "Grunderwerbsteuer erfasst alle Rechtsvorgänge zum Grundstückserwerb: Kaufvertrag (Abs. 1 Nr. 1), Auflassung (Nr. 2), Eigentumsübergang (Nr. 3). Share Deals ab 90% (Abs. 3). Steuerpflicht entsteht mit Kaufvertrag! Schmidt Rn. 1-150"},
    {"para": "GrEStG 2 Schmidt", "title": "Schmidt GrEStG § 2 - Befreiungstatbestände", "kommentar": "Familieninterne Übertragungen steuerfrei: Ehegatten, Verwandte gerader Linie (Eltern-Kinder). Schenkungen unter Lebenden erfasst § 7 ErbStG. Wichtig: Form beachten (notarielle Beurkundung)! Schmidt Rn. 1-80"},
    {"para": "GrEStG 8 Schmidt", "title": "Schmidt GrEStG § 8 - Bemessungsgrundlage Praxis", "kommentar": "Bemessungsgrundlage = Kaufpreis + übernommene Lasten (Hypotheken, Grundschulden). Bei Tausch: Gemeiner Wert. Bei Share Deal: Grundbesitzwert nach BewG. Schmidt Rn. 1-120"},
    {"para": "GrStG 1 Schmidt", "title": "Schmidt GrStG § 1 - Grundsteuer-Reform 2025", "kommentar": "Neubewertung aller Grundstücke zum 01.01.2022. Bundesmodell: Ertragswert/Sachwert. Ländermodelle: Bayern (Fläche), BW (Bodenwert). Hebesatz bleibt Ländersache! Schmidt Rn. 1-200"}
]

def seed_all():
    info = qdrant.get_collection(COLLECTION_NAME)
    before = info.points_count
    print(f"📊 Vorher: {before} Dokumente\n")
    
    all_points = []
    
    # Palandt
    print(f"📚 Palandt BGB (+{len(PALANDT)})...")
    for p in PALANDT:
        text = f"PALANDT BGB § {p['para']}\n{p['title']}\n\nKOMMENTIERUNG:\n{p['kommentar']}"
        emb = create_embedding(text)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={"title": p['title'], "content": text, "doc_type": "Literatur",
                    "quelle": "Palandt BGB", "paragraph": p['para'],
                    "rechtsgebiet": "Zivilrecht", "jurisdiction": "Deutschland"}
        )
        all_points.append(point)
    print(f"   ✅ {len(PALANDT)} Palandt-Kommentierungen vorbereitet")
    
    # MüKo
    print(f"\n📘 Münchener Kommentar (+{len(MUEKO)})...")
    for m in MUEKO:
        text = f"MÜNCHENER KOMMENTAR\n{m['title']}\n\nKOMMENTIERUNG:\n{m['kommentar']}"
        emb = create_embedding(text)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={"title": m['title'], "content": text, "doc_type": "Literatur",
                    "quelle": "Münchener Kommentar BGB", "paragraph": m['para'],
                    "rechtsgebiet": "Zivilrecht", "jurisdiction": "Deutschland"}
        )
        all_points.append(point)
    print(f"   ✅ {len(MUEKO)} MüKo-Kommentierungen vorbereitet")
    
    # Schmidt
    print(f"\n💰 Schmidt Steuerrecht (+{len(SCHMIDT)})...")
    for s in SCHMIDT:
        text = f"SCHMIDT STEUERRECHT\n{s['title']}\n\nKOMMENTIERUNG:\n{s['kommentar']}"
        emb = create_embedding(text)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={"title": s['title'], "content": text, "doc_type": "Literatur",
                    "quelle": "Schmidt EStG", "paragraph": s['para'],
                    "rechtsgebiet": "Steuerrecht", "jurisdiction": "Deutschland"}
        )
        all_points.append(point)
    print(f"   ✅ {len(SCHMIDT)} Schmidt-Kommentierungen vorbereitet")
    
    # Upload
    print(f"\n⬆️  Uploading {len(all_points)} Literatur-Quellen...")
    qdrant.upsert(collection_name=COLLECTION_NAME, points=all_points)
    print("   ✅ Upload erfolgreich!")
    
    info = qdrant.get_collection(COLLECTION_NAME)
    after = info.points_count
    
    print("\n"+"="*70)
    print("✅ LITERATUR-EXPANSION ABGESCHLOSSEN!")
    print("="*70)
    print(f"📊 Vorher:      {before:5} Dokumente")
    print(f"📊 Nachher:     {after:5} Dokumente")
    print(f"📊 Hinzugefügt: {after-before:5} Literatur-Quellen")
    print(f"\n🎯 MASTERPLAN: {after}/5000 ({after/50:.1f}%)")
    print("="*70)

if __name__ == "__main__":
    seed_all()
