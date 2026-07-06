from pydantic import BaseModel, Field, ConfigDict
from datetime import date as PyDate
from app.models.transaction import TransactionType

class TransactionCreateSchema(BaseModel):
    category_id: int
    transaction_type: TransactionType
    amount: float = Field(..., gt=0.0)
    description: str | None = Field(None, max_length=200)
    date: PyDate | None = None

    source_account_id: int | None = None
    source_card_id: int | None = None
    destination_account_id: int | None = None
    destination_card_id: int | None = None

class TransactionResponseSchema(BaseModel):
    id: int
    category_id: int
    transaction_type: str
    amount: float
    description: str | None
    date: PyDate
    source_account_id: int | None
    source_card_id: int | None
    destination_account_id: int | None
    destination_card_id: int | None
    
    model_config= ConfigDict(from_attributes=True)
