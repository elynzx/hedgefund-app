from flask import Flask
from config import Config
from db import db
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app.models import (user, category, bank_account, credit_card, transaction)

from flask_jwt_extended import JWTManager
from app.router import api

migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    return app
