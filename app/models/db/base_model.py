<<<<<<< HEAD
import uuid

from pydantic import BaseModel,Field
from datetime import datetime

class CreateScchema(BaseModel):
=======
from pydantic import BaseModel,Field
from datetime import datetime

class CreateSchema(BaseModel):
>>>>>>> f38e70b (Final Commit)
    created_at: datetime = Field(default_factory=datetime.now)

class CreateUpdateSchema(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class BookBaseSchema(BaseModel):
    id:  str = Field(...)
    name: str = Field(...)