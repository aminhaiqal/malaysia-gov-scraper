from sentence_transformers import SentenceTransformer

MODEL_NAME = "google/embeddinggemma-300m"

model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str):
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.tolist()

def get_embedding_dimension() -> int:
    return model.get_sentence_embedding_dimension()