from flask_restful import Resource
from flask import request
from pydantic import ValidationError
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.services.auth_service import auth_service

class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            validated_data= RegisterSchema.model_validate(data)
            
            user = auth_service.register(validated_data)
            
            return user.to_json(), 201

        except ValidationError as e:
            return {
                'error':'Datos invalidos', 
                'detalles': e.errors()
            }, 422
        except ValueError as e:
            return{
                'error': str(e)
            }, 403        
        except Exception as e:
            return {
                'error':'Error interno del servidor',
                'mensaje': str(e)
            }, 500


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            validated_data= LoginSchema.model_validate(data)

            auth_result = auth_service.login(validated_data)
            
            return {
                'access': auth_result['access'],
                'refresh': auth_result['refresh'],
                'user': auth_result['user'].to_json()
            },200
            
        except ValidationError as e:
            return {
                'error':'Datos invalidos', 
                'detalles': e.errors()
            }, 422
        except PermissionError as e:
            return {
                'error': str(e)
            }, 401
        except ValueError as e:
            return{
                'error': str(e)
            }, 403
        except Exception as e:
            return {
                'error': 'Error interno del servidor',
                'mensaje': str(e)
            }, 500