from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str):
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.tolist()

def get_embedding_dimension() -> int:
    return model.get_sentence_embedding_dimension()