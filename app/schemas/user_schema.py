from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    monthly_income: Optional[float] = Field(None, ge=0.00)
    
    @field_validator('currency')
    def validate_currency(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        value = value.upper().strip()
        allowed_currencies = ["PEN", "USD", "EUR"]
        
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
