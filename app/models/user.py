from db import db
from sqlalchemy import Integer, String, Boolean, Numeric, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime as PyDateTime

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='PEN')
    monthly_income: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[PyDateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'currency': self.currency,
            'monthly_income': float(self.monthly_income) if self.monthly_income is not None else None,
            'is_active': self.is_active,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
