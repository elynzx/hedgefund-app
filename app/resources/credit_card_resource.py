from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.schemas.credit_card_schema import CreditCardCreateSchema, CreditCardUpdateSchema
from app.services.credit_card_service import credit_card_service
from app.utils.security import CryptoHelper

def get_current_user_id() -> int:
    crypto = CryptoHelper()
    hashed_id = get_jwt_identity()
    return int(crypto.decrypt(hashed_id))

class CreditCardResource(Resource):
    @jwt_required()
    @swag_from('../docs/get_credit_cards.yml')
    def get(self):
        try:
            user_id = get_current_user_id()
            cards_list = credit_card_service.get_all_by_user(user_id)
            return [card.to_json() for card in cards_list], 200
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500
            
    @jwt_required()
    @swag_from('../docs/create_credit_card.yml')
    def post(self):
        try:
            user_id = get_current_user_id()
            data = request.get_json()
            validated_data = CreditCardCreateSchema.model_validate(data)

            credit_card = credit_card_service.create(validated_data, user_id)
            return credit_card.to_json(), 201

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
            
class ManageCreditCardResource(Resource):
    @jwt_required()
    @swag_from('../docs/update_credit_card.yml')    
    def put(self, card_id: int):
        try:
            user_id = get_current_user_id()
            data = request.get_json()
            validated_data = CreditCardUpdateSchema.model_validate(data)

            updated_card = credit_card_service.update(card_id, validated_data, user_id)
            return updated_card.to_json(), 200
        
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
    @swag_from('../docs/delete_credit_card.yml')
    def delete(self, card_id: int):
        try:
            user_id = get_current_user_id()
            credit_card_service.delete(card_id, user_id)
            return {
                'mensaje': 'Tarjeta de credito desactivada con exito.'
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
