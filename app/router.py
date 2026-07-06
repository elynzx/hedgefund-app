from flask_restful import Api
from app.resources.auth_resource import *

api = Api(prefix='/api/v1')

api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')