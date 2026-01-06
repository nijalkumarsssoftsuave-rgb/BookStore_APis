from pydantic import BaseModel, Field
from typing import List
from app.models.db.base_model import CreateUpdateSchema


class User(CreateUpdateSchema):
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    gender: str = Field(...)
    phone_number: str = Field(None)
    age: int = Field(...)
    role: List[str] = Field(None)
    is_deleted: bool = Field(False)
