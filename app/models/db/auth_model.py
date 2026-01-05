from pydantic import BaseModel,Field,EmailStr
from app.models.db.base_model import CreateScchema

class User(CreateScchema):
    email : EmailStr = Field(...)
    password: str = Field(...)
