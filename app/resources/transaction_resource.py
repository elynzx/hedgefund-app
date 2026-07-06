from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.transaction_schema import TransactionCreateSchema
from app.services.transaction_service import transaction_service
from app.utils.security import CryptoHelper
from app.extensions import db

def get_current_user_id() -> int:
    crypto = CryptoHelper()
    hashed_id = get_jwt_identity()
    return int(crypto.decrypt(hashed_id))

class TransactionResource(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = get_current_user_id()
            data = request.get_json()
            validated_data = TransactionCreateSchema.model_validate(data)

            transaction = transaction_service.create(validated_data, user_id)
            return transaction.to_json(), 201
            
        except ValidationError as e:
            return {
                'error': 'Datos invalidos',
                'detalles': e.errors()
            }, 422
        except (ValueError, LookupError) as e:
            db.session.rollback()
            return {
                'error': str(e)
            }, 400
        except Exception as e:
            db.session.rollback()
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500