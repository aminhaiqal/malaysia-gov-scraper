from qdrant_client import QdrantClient
from src.embeddings.embedder import embed_text

QDRANT_URL = "http://localhost:6333"
API_KEY = "qdrjYgmlPGcjGgybJmEPEJvFOoQ9hdkjDcP"
COLLECTION_NAME = "gov_docs"
QUERY_TEXT = "Transformasi Semikonduktor"
TOP_K = 3

client = QdrantClient(url=QDRANT_URL, api_key=API_KEY)
client.get_collection(collection_name=COLLECTION_NAME)

# Embed query → should return list of floats
query_vector = embed_text(QUERY_TEXT)
if isinstance(query_vector, dict):
    query_vector = query_vector["embedding"]
elif isinstance(query_vector, list) and isinstance(query_vector[0], dict):
    # chunked embeddings → mean pool
    vectors = [x["embedding"] for x in query_vector]
    import numpy as np
    query_vector = np.mean(vectors, axis=0).tolist()
elif isinstance(query_vector, list) and isinstance(query_vector[0], (float, int)):
    # already single vector
    pass
else:
    raise ValueError("embed_text returned unsupported format")

# Semantic search
hits = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=TOP_K,
).points

# Display
for i, hit in enumerate(hits, 1):
    print(f"{i}. Score: {hit.score}")
    print("Payload:", hit.payload)
    print("-" * 50)
