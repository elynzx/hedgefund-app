from db import db
from app.models.category import Category

def seed_categories():
    if Category.query.first() is None:
        categories = [
            Category(category_name='Salary', category_type='income'),
            Category(category_name='Freelance', category_type='income'),
            Category(category_name='Investments', category_type='income'),

            Category(category_name='Rent', category_type='fixed_expense'),
            Category(category_name='Utilities', category_type='fixed_expense'),
            Category(category_name='Insurance', category_type='fixed_expense'),
            Category(category_name='Debt & Loans', category_type='fixed_expense'),
            
            Category(category_name='Groceries', category_type='variable_expense'),
            Category(category_name='Transportation', category_type='variable_expense'),
            Category(category_name='Dining Out', category_type='variable_expense'),
            Category(category_name='Entertainment', category_type='variable_expense'),
            Category(category_name='Shopping', category_type='variable_expense'),
            Category(category_name='Others', category_type='variable_expense'),
            
            Category(category_name='Credit Card Payment', category_type='system'),
            Category(category_name='Internal Transfer', category_type='system')
        ]
        db.session.add_all(categories)
        db.session.commit()
        print("Categorias insertadas con exito")
