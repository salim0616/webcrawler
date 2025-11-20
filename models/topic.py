from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    confidence: float
