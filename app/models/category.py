from db import db
from sqlalchemy import Integer, String, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

class CategoryType(str, Enum):
    INCOME = 'income'
    FIXED_EXPENSE = 'fixed_expense'
    VARIABLE_EXPENSE = 'variable_expense'
    SYSTEM = 'system'

_CATEGORY_TYPE_VALUES = ', '.join(f"'{t.value}'" for t in CategoryType)

class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint(
             f"category_type IN ({_CATEGORY_TYPE_VALUES})", 
            name='chk_category_type'
        ),
    )

    def to_json(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'category_type': self.category_type,
            'is_active': self.is_active
        }
