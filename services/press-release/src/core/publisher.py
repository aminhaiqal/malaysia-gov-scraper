from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from typing import Dict, Optional


class QdrantPublisher:
    def __init__(self, url: str, collection_name: str = "gov_docs", api_key: Optional[str] = None, vector_size: int = 1536):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection_name
        
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection not in existing:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"Created missing Qdrant collection '{self.collection}'")
    
    def publish(self, doc_id: str, text: str, metadata: Dict, embedding: list):
        point = PointStruct(id=doc_id, vector=embedding, payload={**metadata, "text": text})
        self.client.upsert(collection_name=self.collection, points=[point])