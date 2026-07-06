from pydantic import BaseModel, Field, field_validator, model_validator

class CreditCardCreateSchema(BaseModel):
    card_name: str = Field(..., min_length=2, max_length=50)
    credit_limit: float = Field(..., gt=0.0)
    closing_day: int = Field(..., ge=1, le=31)
    due_day: int = Field(..., ge=1, le=31)
    debt_amount: float = Field(0.00, ge=0.0)

    @field_validator('card_name')
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('El nombre de la tarjeta no puede estar vacio')
        return value.strip()

    @model_validator(mode='after')
    def check_debt_limit(self) -> 'CreditCardCreateSchema':
        if self.debt_amount > self.credit_limit:
            raise ValueError('La deuda inicial no puede ser mayor al limite de credito')
        return self

class CreditCardUpdateSchema(BaseModel):
    card_name: str | None = Field(None, min_length=2, max_length=50)
    credit_limit: float | None = Field(None, gt=0.0)
    debt_amount: float | None = Field(None, ge=0.0)

    @field_validator('card_name')
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.strip():
            raise ValueError('El nombre de la tarjeta no puede estar vacio')
        return value.strip()
