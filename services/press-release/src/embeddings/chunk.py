from typing import List, Dict
from .embedder import embed_text

def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: The full text to chunk.
        chunk_size: Number of characters per chunk.
        overlap: Number of characters to overlap between chunks.

    Returns:
        List of text chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap  # move start forward with overlap

    return chunks

def embed_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[Dict]:
    """
    Split text into chunks and generate embeddings for each chunk.
    
    Returns:
        List of dicts with 'text' and 'embedding'.
    """
    chunks = chunk_text(text, chunk_size, overlap)
    embedded_chunks = []

    for chunk in chunks:
        embedding = embed_text(chunk)
        embedded_chunks.append({
            "text": chunk,
            "embedding": embedding
        })

    return embedded_chunks
