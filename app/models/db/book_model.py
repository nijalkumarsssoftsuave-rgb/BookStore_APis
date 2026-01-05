from pydantic import Field
from app.models.db.base_model import CreateUpdateSchema

class Book(CreateUpdateSchema):
    name: str = Field(...)
    description: str = Field(...)
    # author: BaseSchema = Field(...)
    # is_published: bool = Field(False)
    # category: CategoryResponse = Field(...)
