from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.user_schema import UserUpdateSchema
from app.services.user_service import user_service
from app.utils.security import CryptoHelper

def get_current_user_id() -> int:
    crypto = CryptoHelper()
    hashed_id = get_jwt_identity()
    return int(crypto.decrypt(hashed_id))

class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_current_user_id()
            user = user_service.get_by_id(user_id)
            if not user:
                return {
                    'error': 'Usuario no encontrado'
                }, 404

            return user.to_json(), 200

        except Exception as e:
            return {
                'error': 'Error al cargar el perfil', 
                'mensaje': str(e)
            }, 500

    @jwt_required()
    def put(self):
        try:
            user_id = get_current_user_id()
            data = request.get_json()
            validated_data = UserUpdateSchema.model_validate(data)

            updated_user = user_service.update_profile(user_id, validated_data)
            return updated_user.to_json(), 200
            
        except ValidationError as e:
            return {
                'error': 'Datos invalidos',
                'detalles': e.errors()
            }, 422
        except KeyError as e:
            return {
                'error': str(e)
            }, 404
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500