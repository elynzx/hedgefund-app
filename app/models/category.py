from db import db
from sqlalchemy import Integer, String, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category_type: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "category_type IN ('income', 'fixed_expense', 'variable_expense', 'system')", 
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
