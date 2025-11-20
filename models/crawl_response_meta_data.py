from typing import List, Optional
from pydantic import BaseModel
from models.topic import Topic


class MetadataResponse(BaseModel):
    url: str
    domain: str
    title: str
    description: str
    body_text: str
    topics: List[Topic]
    images: List[str]
    links: List[str]
    crawl_timestamp: str
    content_hash: str
    word_count: int
    error: Optional[str] = None
    processing_time: float
