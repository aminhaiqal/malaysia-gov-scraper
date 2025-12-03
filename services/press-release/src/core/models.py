from pydantic import BaseModel
from typing import List, Optional

class PressRelease(BaseModel):
    id: str
    title: str
    ministry: str
    date: str
    source: str  # HTML or PDF
    url: str
    text: str
    chunk_id: Optional[int] = None
    metadata: Optional[dict] = None
