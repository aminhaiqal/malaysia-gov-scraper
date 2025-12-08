from typing import List
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str) -> List[float]:
    """Embed a single short text fragment."""
    text = text.strip()
    if not text:
        return []
    emb = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return emb.tolist()

def get_embedding_dimension() -> int:
    return model.get_sentence_embedding_dimension()