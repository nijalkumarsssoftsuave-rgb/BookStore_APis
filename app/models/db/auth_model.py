from pydantic import EmailStr,Field
from app.models.db.base_model import CreateSchema


class User(CreateSchema):
    email : EmailStr = Field(...)
    password: str = Field(...)
