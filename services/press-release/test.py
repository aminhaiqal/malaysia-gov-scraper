from qdrant_client import QdrantClient
from src.embeddings.embedder import embed_text

# -------------------------------
# CONFIG
# -------------------------------
QDRANT_URL = "http://localhost:6333"
API_KEY = "qdrjYgmlPGcjGgybJmEPEJvFOoQ9hdkjDcP"
COLLECTION_NAME = "gov_docs"
QUERY_TEXT = "Transformasi Semikonduktor"
TOP_K = 3  # number of results

# -------------------------------
# INIT CLIENT
# -------------------------------
client = QdrantClient(url=QDRANT_URL, api_key=API_KEY)

# Make sure the collection exists
try:
    info = client.get_collection(collection_name=COLLECTION_NAME)
except Exception as e:
    raise RuntimeError(f"Collection '{COLLECTION_NAME}' not found: {e}")

# -------------------------------
# Embed the query locally
# -------------------------------
query_result = embed_text(QUERY_TEXT)

# If chunking returned multiple embeddings, take the first
if isinstance(query_result, dict):
    query_vector = query_result["embedding"]
elif isinstance(query_result, list):
    query_vector = query_result[0]["embedding"]
else:
    raise ValueError("Unexpected return type from embed_text()")

# -------------------------------
# Perform similarity search
# -------------------------------
# Use query_points (classic client method) with vector
hits = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=TOP_K
).points

# -------------------------------
# Display results
# -------------------------------
print(f"Top {TOP_K} results for query: '{QUERY_TEXT}'\n")
for i, hit in enumerate(hits, 1):
    payload = hit.payload
    score = hit.score
    chunk_text = payload.get("chunk_text", "(no chunk text)")
    print(f"{i}. Score: {score:.4f}")
    print(f"   Title: {payload.get('title')}")
    print(f"   URL: {payload.get('url')}")
    print(f"   Chunk: {chunk_text[:150]}{'...' if len(chunk_text) > 150 else ''}")
    print("-" * 80)
