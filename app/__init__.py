from flask import Flask
from config import Config
from db import db
from flask_migrate import Migrate
from app.models import (user, category, bank_account, credit_card, transaction)

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
