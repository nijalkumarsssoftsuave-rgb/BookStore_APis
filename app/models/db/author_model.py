from pydantic import Field
from typing import List
<<<<<<< HEAD
from app.models.db.base_model import CreateScchema

class Author(CreateScchema):
=======
from app.models.db.base_model import CreateSchema

class Author(CreateSchema):
>>>>>>> f38e70b (Final Commit)
    name: str = Field(...)
    age: int = Field(None)
    awards: List[str] = Field(None)
    gender: str = Field(...)