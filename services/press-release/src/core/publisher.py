from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from typing import Dict


class QdrantPublisher:
    def __init__(self, url: str, collection_name: str = "gov_docs"):
        self.client = QdrantClient(url=url)
        self.collection = collection_name
        # Assume collection exists; caller manages schema
    
    def publish(self, doc_id: str, text: str, metadata: Dict, embedding: list):
        point = PointStruct(id=doc_id, vector=embedding, payload={**metadata, "text": text})
        self.client.upsert(collection_name=self.collection, points=[point])