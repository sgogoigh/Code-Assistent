from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class ReviewCreate(BaseModel):
    filename: Optional[str]
    language: Optional[str]
    code: str

class ReviewOut(BaseModel):
    id: int
    filename: Optional[str]
    language: Optional[str]
    code_excerpt: Optional[str]
    parsed_report: Optional[Any]
    raw_response: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
