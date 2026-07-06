from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger

bcrypt = Bcrypt()
jwt = JWTManager()
swagger = Swagger()