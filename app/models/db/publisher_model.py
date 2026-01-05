from pydantic import Field,BaseModel
from app.models.db.base_model import BookBaseSchema
from typing import List

class Publisher(BaseModel):
    name : str = Field(...)
    location: str = Field(...)
    books: List[str] = Field(...)

