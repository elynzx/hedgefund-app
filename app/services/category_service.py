from app.models.category import Category

class CategoryService:
    def get_all_active(self) -> list[Category]:
        return Category.query.filter_by(is_active=True).all()

category_service = CategoryService()