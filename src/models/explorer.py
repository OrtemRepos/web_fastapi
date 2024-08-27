from pydantic import BaseModel, Field
from typing import Optional


class Explorer(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    country: str = Field(min_length=2, max_length=2)
    description: Optional[str] = ""
