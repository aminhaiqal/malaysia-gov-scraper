from typing import List, Dict, Union
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MAX_CHUNK_CHAR_LEN = 800

model = SentenceTransformer(MODEL_NAME)

def _embed_single(text: str) -> List[float]:
    """Embed a single short text fragment."""
    emb = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return emb.tolist()

def embed_text(text: str) -> Union[Dict, List[Dict]]:
    """"
    Auto-detect text length and chunk only if needed.

    Returns:
      If short: { "text": ..., "embedding": [...] }
      If long:  [ { "text": ..., "embedding": [...] }, ... ]
    """
    from .chunk import chunk_text
    text = text.strip()
    if not text:
        return []

    if len(text) <= MAX_CHUNK_CHAR_LEN:
        # Direct embedding
        return {
            "text": text,
            "embedding": _embed_single(text)
        }
    
    chunks = chunk_text(text)
    return [
        {
            "text": chunk,
            "embedding": _embed_single(chunk)
        }
        for chunk in chunks
    ]

def get_embedding_dimension() -> int:
    return model.get_sentence_embedding_dimension()