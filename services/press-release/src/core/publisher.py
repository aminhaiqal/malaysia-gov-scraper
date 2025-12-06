import uuid
from qdrant_client import QdrantClient, models
from typing import Optional
from .models import Article
from src.embeddings.embedder import embed_text, get_embedding_dimension


class QdrantPublisher:
    def __init__(self, url: str, collection_name: str = "gov_docs", api_key: Optional[str] = None):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection_name
        
        dimm = get_embedding_dimension()
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection not in existing:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(size=dimm, distance=models.Distance.COSINE)
            )
            print(f"Created missing Qdrant collection '{self.collection}'")
    
    def publish(self, docs: list[Article]):
        points = []

        for doc in docs:
            embedded = embed_text(doc.cleaned_text or doc.text)

            if isinstance(embedded, dict):
                embedded = [embedded]

            for chunk in embedded:
                points.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=chunk["embedding"],
                        payload={
                            **doc.to_payload(),
                            "chunk_text": chunk["text"]
                        }
                    )
                )


        self.client.upload_points(
            collection_name=self.collection,
            points=points
        )
