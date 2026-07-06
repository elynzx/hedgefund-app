from pydantic import BaseModel, Field, field_validator
from app.models.bank_account import AccountType

class BankAccountCreateSchema(BaseModel):
    account_name: str = Field(..., min_length=2, max_length=50)
    account_type: AccountType
    current_balance: float = Field(0.00, ge=0.0)

    @field_validator('account_name')
    def name_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('El nombre de la cuenta bancaria no puede estar vacio')
        return value.strip()

class BankAccountUpdateSchema(BaseModel):
    account_name: str | None = Field(None, min_length=2, max_length=50)
    account_type: AccountType | None = None
    current_balance: float | None = Field(None, ge=0.0)

    @field_validator('account_name')
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.strip():
            raise ValueError('El nombre de la cuenta bancaria no puede estar vacio')
        return value.strip()
