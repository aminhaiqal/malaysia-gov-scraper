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

# Scroll all points
scroll_result = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=100  # number of points per batch
)

print(f"Retrieved {len(scroll_result)} points in first batch")
print(scroll_result)

hits = client.query_points(
    collection_name=COLLECTION_NAME,
    query=embed_text("Ron97 and Ron95 price update"),
    limit=3,
).points

print(hits)

for hit in hits:
    print(hit.payload, "score:", hit.score)