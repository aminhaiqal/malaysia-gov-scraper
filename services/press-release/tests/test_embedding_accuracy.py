import pytest
import numpy as np
from qdrant_client import QdrantClient, models
from src.embeddings import embedder

# -------------------------------
# CONFIG
# -------------------------------
QDRANT_URL = "http://localhost:6333"
API_KEY = "qdrjYgmlPGcjGgybJmEPEJvFOoQ9hdkjDcP"
COLLECTION_NAME = "embedding_test"
VECTOR_SIZE = 384

# -------------------------------
# FIXTURE: Qdrant client
# -------------------------------
@pytest.fixture(scope="session")
def client():
    client = QdrantClient(url=QDRANT_URL, api_key=API_KEY)

    # Recreate collection (clean slate)
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
    )
    return client

# -------------------------------
# FIXTURE: Monkeypatch embed_text
# -------------------------------
@pytest.fixture
def inserted_point(client, monkeypatch):
    """
    Inserts a deterministic vector into Qdrant for testing.
    Monkeypatches embed_text to ensure reproducible vectors.
    """

    def fake_embed(text: str):
        # Deterministic vector from text
        seed = sum(ord(c) for c in text)
        rng = np.random.default_rng(seed)
        vec = rng.random(VECTOR_SIZE).astype("float32")
        return {"embedding": vec.tolist()}

    # Monkeypatch the real embed_text function
    monkeypatch.setattr(embedder, "embed_text", fake_embed)

    sample_text = "Malaysia fiscal policy improves semiconductor industry growth."
    vec = fake_embed(sample_text)["embedding"]

    # Upsert into Qdrant
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(id=1, vector=vec, payload={"text": sample_text})
        ],
        wait=True
    )

    return vec

# -------------------------------
# HELPER: search vector
# -------------------------------
def search_vec(client, vec, limit=1):
    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vec,
        limit=limit
    ).points
    return hits[0] if hits else None

# -------------------------------
# TESTS
# -------------------------------
def test_self_similarity(client, inserted_point):
    """The same text should be extremely similar to itself"""
    hit = search_vec(client, inserted_point)
    print("Self-similarity score:", hit.score)
    assert hit.score >= 0.95

def test_near_duplicate_similarity(client, inserted_point):
    """Small paraphrase → high similarity"""
    vec2 = embedder.embed_text("Malaysia’s fiscal policies support growth in the semiconductor sector.")["embedding"]
    hit = search_vec(client, vec2)
    print("Near-duplicate similarity score:", hit.score)
    assert hit.score >= 0.70

def test_unrelated_similarity(client, inserted_point):
    """Random unrelated topic → low similarity"""
    vec2 = embedder.embed_text("Wild animals in African savannah are adapting to new conditions.")["embedding"]
    hit = search_vec(client, vec2)
    print("Unrelated similarity score:", hit.score)
    assert hit.score <= 0.20
