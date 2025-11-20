from pydantic import BaseModel


class URLRequest(BaseModel):
    url: str
    enable_topic_classification: bool = False
    timeout: int = 30
