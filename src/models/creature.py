from pydantic import BaseModel, Field
from typing import Optional


class Creature(BaseModel):
    name: str
    country: str
    area: Optional[str] = "*"
    description: Optional[str] = ""
    aka: Optional[str] = ""
