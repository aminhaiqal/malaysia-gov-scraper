from qdrant_client import QdrantClient, models
import numpy as np
from src.embeddings.embedder import embed_text

# -------------------------------
# CONFIG
# -------------------------------
QDRANT_URL = "http://localhost:6333"
API_KEY = "qdrjYgmlPGcjGgybJmEPEJvFOoQ9hdkjDcP"
COLLECTION_NAME = "gov_docs"
QUERY_TEXT = "Transformasi Semikonduktor"
TOP_K = 3

# -------------------------------
# INIT CLIENT
# -------------------------------
client = QdrantClient(url=QDRANT_URL, api_key=API_KEY)
client.get_collection(collection_name=COLLECTION_NAME)  # assert exists

# -------------------------------
# Embed the query
# -------------------------------
query_result = embed_text(QUERY_TEXT)

# unify/flatten → ALWAYS return a SINGLE vector
if isinstance(query_result, dict):
    query_vector = np.array(query_result["embedding"], dtype=np.float32)
elif isinstance(query_result, list):
    vectors = [np.array(x["embedding"], dtype=np.float32) for x in query_result]
    query_vector = np.mean(vectors, axis=0)  # avg merge chunks
else:
    raise ValueError("Invalid embed_text output format")

# ensure list for Qdrant
query_vector = query_vector.tolist()

# -------------------------------
# Nearest Neighbors Search
# -------------------------------
hits = client.query(
    collection_name=COLLECTION_NAME,
    query_vector=query_vector,
    limit=TOP_K,
    search_params=models.SearchParams(
        hnsw_ef=128  # improves recall quality
    )
).points

# -------------------------------
# Display results
# -------------------------------
print(f"\nTop {TOP_K} results for query: '{QUERY_TEXT}':\n")
for i, hit in enumerate(hits, start=1):
    payload = hit.payload
    score = hit.score
    text = payload.get("chunk_text", "") or ""
    print(f"{i}. Score: {score:.4f}")
    print(f"   URL: {payload.get('url')}")
    print(f"   Title: {payload.get('title')}")
    print(f"   Chunk: {text[:150]}{'...' if len(text) > 150 else ''}")
    print("-" * 60)
