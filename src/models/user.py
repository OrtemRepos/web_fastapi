from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    hash: str = Field(min_length=6, max_length=20)
