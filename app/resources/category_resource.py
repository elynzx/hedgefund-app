from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.services.category_service import category_service

class CategoryResource(Resource):
    @jwt_required()
    def get(self):
        try:
            categories = category_service.get_all_active()
            return [category.to_json() for category in categories], 200
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500