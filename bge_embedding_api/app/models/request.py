from typing import List, Optional, Union
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: Optional[str] = None
    embedding_type: Optional[str] = None


class RerankRequest(BaseModel):
    query: str
    documents: List[str]
