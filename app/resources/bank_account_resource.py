from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.bank_account_schema import BankAccountCreateSchema, BankAccountUpdateSchema
from app.services.bank_account_service import bank_account_service
from app.utils.security import CryptoHelper

def get_current_user_id() -> int:
    crypto = CryptoHelper()
    hashed_id = get_jwt_identity()
    return int(crypto.decrypt(hashed_id))

class BankAccountResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_current_user_id()
            bank_accounts = bank_account_service.get_all_by_user(user_id)
            return [bank_account.to_json() for bank_account in bank_accounts], 200

        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500
            
    @jwt_required()
    def post(self):
        try:
            user_id = get_current_user_id()
            data = request.get_json()
            validated_data = BankAccountCreateSchema.model_validate(data)

            bank_account = bank_account_service.create(validated_data, user_id)
            return bank_account.to_json(), 201
        
        except ValidationError as e:
            return {
                'error': 'Datos invalidos',
                'detalles': e.errors()
            }, 422
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500

class ManageBankAccountResource(Resource):
    @jwt_required()
    def put(self, account_id: int):
        try:
            user_id = get_current_user_id()
            data = request.get_json()

            validated_data = BankAccountUpdateSchema.model_validate(data)

            updated_account = bank_account_service.update(account_id, validated_data, user_id)
            return updated_account.to_json(), 200
        
        except ValidationError as e:
            return {
                'error': 'Datos invalidos', 
                'detalles': e.errors()
            }, 422
        except LookupError as e:
            return {
                'error': str(e)
            }, 404
        except PermissionError as e:
            return {
                'error': str(e)
            }, 401
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500

    @jwt_required()
    def delete(self, account_id: int):
        try:
            user_id = get_current_user_id()
            bank_account_service.delete(account_id, user_id)
            return {
                'mensaje': 'Cuenta bancaria desactivada con exito'
            }, 200
        except LookupError as e:
            return {
                'error': str(e)
            }, 404
        except PermissionError as e:
            return {
                'error': str(e)
            }, 401
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500
