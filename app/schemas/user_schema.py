from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    currency: str | None = Field(None, min_length=3, max_length=3)
    monthly_income: float | None = Field(None, ge=0.00)
    
    @field_validator('currency')
    def validate_currency(cls, value:str | None) -> str | None:
        if value is None:
            return value

        value = value.strip().upper()
        allowed_currencies = {"PEN", "USD", "EUR"}
        
        if value not in allowed_currencies:
            raise ValueError(f"Moneda no soportada. Permitidas: {', '.join(allowed_currencies)}")
        return value

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    currency: str
    monthly_income: float
    is_active: bool
    created_at: datetime
    
    model_config= ConfigDict(from_attributes=True)
