from qdrant_client import QdrantClient
from src.embeddings.embedder import embed_text
from numpy import dot
from numpy.linalg import norm
import numpy as np

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
print(info)
# -------------------------------
# 1. Inspect first 5 points
# -------------------------------
print("Checking stored vectors and metadata...")
points = client.scroll(collection_name=COLLECTION_NAME, limit=5)
for p in points:
    # Ensure it's a Record, not a nested list
    if isinstance(p, list):
        for r in p:
            print("ID:", r.id)
            print("Vector length:", len(r.vector) if r.vector else None)
            print("Title:", r.payload.get("title"))
            text = r.payload.get("text") or r.payload.get("metadata", {}).get("text")
            print("Text snippet:", text[:200] if text else None)
            print("---")

# -------------------------------
# 2. Semantic search test
# -------------------------------
query_text = "RON97 and RON95 petrol price update"
query_emb = embed_text(query_text)

# Flatten if nested
query_vector = query_emb[0] if isinstance(query_emb, list) and isinstance(query_emb[0], list) else query_emb

# Convert to numpy and normalize
query_vector = np.array(query_vector, dtype=np.float32)
query_vector /= np.linalg.norm(query_vector)

print("\nSemantic search test for query:", query_text)

response = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=5,
    with_payload=True,
)

# Determine points from response
if isinstance(response, tuple):
    _, points = response
elif hasattr(response, "points"):
    points = response.points
else:
    points = response

# Iterate safely
for i, r in enumerate(points, start=1):
    if isinstance(r, dict):
        payload = r.get("payload", {})
        score = r.get("score")
    elif hasattr(r, "payload"):
        payload = getattr(r, "payload", {}) or {}
        score = getattr(r, "score", None)
    else:
        print("Unexpected item:", r)
        continue

    title = payload.get("title", "No title")
    text_snippet = payload.get("text", "")[:300].replace("\n", " ")

    print(f"Result {i}:")
    print(f"  Score: {score:.4f}")
    print(f"  Title: {title}")
    print(f"  Snippet: {text_snippet}")
    print("---")

# -------------------------------
# 3. Cosine similarity check
# -------------------------------
text_a = "RON97 price increase in Malaysia"
text_b = "Retail price of RON97 goes up"

# Embed texts
emb_a = embed_text(text_a)
emb_b = embed_text(text_b)

# Flatten if nested
emb_a = np.array(emb_a[0] if isinstance(emb_a[0], list) else emb_a)
emb_b = np.array(emb_b[0] if isinstance(emb_b[0], list) else emb_b)

# Ensure same dimension
min_len = min(len(emb_a), len(emb_b))
emb_a = emb_a[:min_len]
emb_b = emb_b[:min_len]

# Compute cosine similarity
cos_sim = dot(emb_a, emb_b) / (norm(emb_a) * norm(emb_b))
print("\nCosine similarity between sample texts:", cos_sim)