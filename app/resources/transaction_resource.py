from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.schemas.transaction_schema import TransactionCreateSchema
from app.services.transaction_service import transaction_service
from app.utils.security import CryptoHelper
from db import db

def get_current_user_id() -> int:
    crypto = CryptoHelper()
    hashed_id = get_jwt_identity()
    return int(crypto.decrypt(hashed_id))

class TransactionResource(Resource):
    @jwt_required()
    @swag_from('../docs/get_transactions.yml')
    def get(self):
        try:
            user_id = get_current_user_id()
            transactions = transaction_service.get_all_by_user(user_id)

            return [transaction.to_json() for transaction in transactions], 200
            
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500
    
    @jwt_required()
    @swag_from('../docs/create_transaction.yml')
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