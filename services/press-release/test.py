from qdrant_client import QdrantClient
from src.embeddings.embedder import embed_text

# -------------------------------
# CONFIG
# -------------------------------
QDRANT_URL = "http://localhost:6333"
API_KEY = "qdrjYgmlPGcjGgybJmEPEJvFOoQ9hdkjDcP"
COLLECTION_NAME = "gov_docs"

# -------------------------------
# INIT CLIENT
# -------------------------------
client = QdrantClient(url=QDRANT_URL, api_key=API_KEY)
info = client.get_collection(collection_name=COLLECTION_NAME)

hits = client.query_points(
    collection_name=COLLECTION_NAME,
    query=embed_text("Raise of Ron95 and Ron97"),
    limit=3,
).points

for hit in hits:
    print(hit.payload, "score:", hit.score)