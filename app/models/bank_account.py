from db import db
from sqlalchemy import Integer, String, Boolean, Numeric, ForeignKey, CheckConstraint, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime as PyDateTime

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    account_name: Mapped[str] = mapped_column(String(50), nullable=False)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    current_balance: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0.00)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("account_type IN ('checking', 'savings', 'investment')", name='chk_account_type'),
        CheckConstraint("current_balance >= 0.00", name='chk_bank_account_positive_balance'),
    )

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'current_balance': float(self.current_balance),
            'is_active': self.is_active,
            'updated_at': str(self.updated_at)
        }