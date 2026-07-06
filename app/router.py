from flask_restful import Api
from app import app
from app.resources.auth_resource import *

api = Api(app, prefix='/api/v1')

api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')