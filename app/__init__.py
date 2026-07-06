from flask import Flask
from config import Config
from db import db
from flask_migrate import Migrate

from app.extensions import bcrypt, jwt
from app.utils.seed import seed_categories
from app.router import api

from app.models import (user, category, bank_account, credit_card, transaction)

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    
    @app.cli.command("seed-categories")
    def seed_categories_command():
        seed_categories()

    return app
