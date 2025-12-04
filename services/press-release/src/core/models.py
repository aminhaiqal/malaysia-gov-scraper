from pydantic import BaseModel
from typing import Optional, Dict


class Document(BaseModel):
    id: str
    title: Optional[str]
    ministry: Optional[str]
    date: Optional[str]
    source: Optional[str]
    url: str
    text: str
    metadata: Optional[Dict] = {}