from pydantic import Field
from typing import List
from app.models.db.base_model import CreateScchema

class Author(CreateScchema):
    name: str = Field(...)
    age: int = Field(None)
    awards: List[str] = Field(None)
    gender: str = Field(...)