from flask import Flask
from config import Config
from db import db
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app.models import (user, category, bank_account, credit_card, transaction)

migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
