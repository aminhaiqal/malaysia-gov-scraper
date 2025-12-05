from pydantic import BaseModel
from typing import Optional, Dict


class Article(BaseModel):
    id: str
    title: Optional[str]
    ministry: Optional[str]
    date: Optional[str]
    source: Optional[str]
    url: str
    text: str
    cleaned_text: Optional[str] = None
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
            "metadata": self.metadata,
        }