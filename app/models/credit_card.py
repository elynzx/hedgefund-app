from db import db
from sqlalchemy import Integer, String, Boolean, Numeric, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime as PyDateTime

class CreditCard(db.Model):
    __tablename__ = 'credit_cards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    card_name: Mapped[str] = mapped_column(String(50), nullable=False)
    credit_limit: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    debt_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0.00)
    closing_day: Mapped[int] = mapped_column(Integer, nullable=False)
    due_day: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("debt_amount >= 0.00", name='chk_credit_card_positive_debt'),
        CheckConstraint("debt_amount <= credit_limit", name='chk_credit_card_limit_exceeded'),
        CheckConstraint("closing_day BETWEEN 1 AND 31", name='chk_credit_card_closing_day'),
        CheckConstraint("due_day BETWEEN 1 AND 31", name='chk_credit_card_due_day'),
    )

    def to_json(self):
        credit_limit = float(self.credit_limit)
        debt_amount = float(self.debt_amount)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'card_name': self.card_name,
            'credit_limit': credit_limit,
            'debt_amount': debt_amount,
            'available_credit': round(credit_limit - debt_amount, 2),
            'closing_day': self.closing_day,
            'due_day': self.due_day,
            'is_active': self.is_active
        }