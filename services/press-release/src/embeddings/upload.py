from src.embeddings.embedder import embed_text
from src.embeddings.chunking import chunk_text
from src.core.publisher import QdrantPublisher as PUBLISHER

def upload_doc(doc):
    """
    Create embeddings for a document and upload to Qdrant
    """
    for chunk in chunk_text(doc['text']):
        embedding = embed_text(chunk)
        PUBLISHER.publish(
            doc_id=doc['id'],
            text=chunk,
            metadata=doc.get('metadata', {}),
            embedding=embedding
        )
