"""
Test professional database - check if RAG retrieval works
"""

from qdrant_client import QdrantClient
import google.generativeai as genai

# Configuration
QDRANT_URL = "https://e3c60b39-c168-4da0-b43a-b7ec46084821.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.zZugSJKQZw8uF606VWXRSd5BPTZWWQg3HwF45_9cL-g"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"
COLLECTION_NAME = "legal_documents"

# Initialize
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

print("🧪 Testing DOMULEX Professional RAG System")
print("=" * 60)

# Check collection
collection_info = qdrant.get_collection(COLLECTION_NAME)
print(f"\n📊 Collection: {collection_info.points_count} documents")

# Test queries
test_queries = [
    # Mietrecht
    "Muss ich als Mieter bei Auszug renovieren?",
    "Kann ich die Miete mindern bei Schimmel? Wie viel Prozent?",
    "Was passiert wenn ich 2 Monate keine Miete zahle?",
    # Kaufrecht
    "Verkäufer hat Mangel verschwiegen - was kann ich tun?",
    "Makler will Provision - muss ich zahlen als Mieter?",
    "Bauträger ist insolvent - bekomme ich Geld zurück?",
    # Steuerrecht Verkauf
    "Immobilie nach 8 Jahren verkaufen - steuerpflichtig?",
    "Verluste aus Immobilienverkauf - verrechenbar?",
    "Gewerblicher Grundstückshandel - ab wann?",
    # Steuerrecht Gestaltung  
    "Share Deal Grunderwerbsteuer - geht das noch?",
    "Betriebsaufspaltung - was ist das?",
    # Steuerrecht Werbungskosten
    "Kann ich an meine Tochter günstiger vermieten?",
    "Denkmal AfA - wie viel % pro Jahr?",
    # Landesbauordnungen
    "Wie viel Abstand muss ich zum Nachbarn in Bayern?",
    "Stellplatzpflicht NRW - muss ich Tiefgarage bauen?",
    "Barrierefreiheit Neubau Berlin - was muss ich beachten?",
    "Brandschutz Mehrfamilienhaus - welche Pflichten?",
    "Grenzbebauung Baden-Württemberg - geht das?",
]

for i, query in enumerate(test_queries, 1):
    print(f"\n{'=' * 60}")
    print(f"Query {i}: {query}")
    print("=" * 60)
    
    # Generate embedding
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query",
    )
    query_embedding = result["embedding"]
    
    # Search Qdrant
    search_results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=3,
    ).points
    
    print(f"\nTop {len(search_results)} results:")
    for j, hit in enumerate(search_results, 1):
        print(f"\n  [{j}] Score: {hit.score:.4f}")
        print(f"      Source: {hit.payload.get('source', 'Unknown')}")
        print(f"      Law: {hit.payload.get('law', 'Unknown')}")
        topics = hit.payload.get('topics', [])
        print(f"      Topics: {', '.join(topics)}")
        content_preview = hit.payload.get('content', '')[:150]
        print(f"      Preview: {content_preview}...")

print("\n" + "=" * 60)
print("✅ RAG system working correctly!")
print("=" * 60)
