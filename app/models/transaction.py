from db import db
from sqlalchemy import Integer, String, Numeric, Date, ForeignKey, CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime as PyDateTime, date as PyDate
from enum import Enum

class TransactionType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
    CREDIT_CARD_PAYMENT = 'credit_card_payment'    

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(String(25), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date: Mapped[PyDate] = mapped_column(Date, nullable=False, server_default=func.current_date())
    source_account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('bank_accounts.id', ondelete='SET NULL'), nullable=True)
    source_card_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('credit_cards.id', ondelete='SET NULL'), nullable=True)
    destination_account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('bank_accounts.id', ondelete='SET NULL'), nullable=True)
    destination_card_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('credit_cards.id', ondelete='SET NULL'), nullable=True)
    created_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            f"transaction_type IN ('{TransactionType.INCOME}', '{TransactionType.EXPENSE}', '{TransactionType.TRANSFER}', '{TransactionType.CREDIT_CARD_PAYMENT}')", 
            name='chk_transaction_type'
        ),
        CheckConstraint("amount > 0.00", name='chk_transaction_positive_amount'),
    )

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'transaction_type': self.transaction_type,
            'amount': float(self.amount),
            'description': self.description,
            'date': str(self.date),
            'source_account_id': self.source_account_id,
            'source_card_id': self.source_card_id,
            'destination_account_id': self.destination_account_id,
            'destination_card_id': self.destination_card_id,
            'created_at': str(self.created_at)
        }