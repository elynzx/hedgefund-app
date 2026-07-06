from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum

class CategoryType(str, Enum):
    INCOME = 'income'
    FIXED_EXPENSE = 'fixed_expense'
    VARIABLE_EXPENSE = 'variable_expense'
    SYSTEM = 'system'

class CategorySchema(BaseModel):
    category_name: str = Field(..., min_length=2, max_length=100)
    category_type: CategoryType

    @field_validator('category_name')
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('El nombre de la Categoria no puede estar vacia')
        return value.strip()

class UpdateCategorySchema(BaseModel):
    category_name: str | None = None
    category_type: str | CategoryType  = None
    is_active: bool | None = None
    
    @field_validator('category_name')
    def update_name_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.strip():
            raise ValueError('El nombre de la categoria no puede estar vacio')
        return value.strip()
    
class CategoryResponseSchema(BaseModel):
    id: int
    category_name: str
    category_type: CategoryType
    is_active: bool

    model_config = ConfigDict(from_attributes=True)