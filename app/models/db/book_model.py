from pydantic import Field
from app.models.db.base_model import CreateUpdateSchema
from app.models.pydantics.book_pydantics import BaseSchema
from app.models.pydantics.category_pydantics import CategoryResponse

class Book(CreateUpdateSchema):
    name: str = Field(...)
    description: str = Field(...)
    author: BaseSchema = Field(...)
    is_published: bool = Field(False)
    category: CategoryResponse = Field(...)
