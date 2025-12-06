from pydantic import BaseModel
from typing import Optional, Dict, List


class Article(BaseModel):
    id: str
    title: Optional[str] = None
    ministry: Optional[str] = None
    date: Optional[str] = None
    source: Optional[str] = None
    url: str
    text: str
    cleaned_text: Optional[str] = None
    category: Optional[str] = None
    pdfs: Optional[List[str]] = []
    metadata: Optional[Dict] = {}

    def to_payload(self) -> Dict:
        return {
            "title": self.title,
            "ministry": self.ministry,
            "date": self.date,
            "source": self.source,
            "url": self.url,
            "text": self.text,
            "cleaned_text": self.cleaned_text,
            "category": self.category,
            "pdfs": self.pdfs,
            "metadata": self.metadata,
        }