def chunk_text(text: str, size: int = 500):
    """
    Split text into chunks for embeddings
    """
    for i in range(0, len(text), size):
        yield text[i:i+size]
