<<<<<<< HEAD
from pydantic import BaseModel,Field,EmailStr
from app.models.db.base_model import CreateScchema

class User(CreateScchema):
=======
from pydantic import EmailStr,Field
from app.models.db.base_model import CreateSchema


class User(CreateSchema):
>>>>>>> f38e70b (Final Commit)
    email : EmailStr = Field(...)
    password: str = Field(...)
