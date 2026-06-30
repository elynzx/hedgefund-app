from dotenv import load_dotenv
import os
from datetime import timedelta
load_dotenv()

class Config():
    DEBUG=True
    SQLALCHEMIST_DATABASE_URI= os.getenv('DATABASE_URI')
    SECRET_KEY= os.getenv('SECRET_KEY')
    JWT_ACCES_TOKEN_EXPIRES=timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPPIRES=timedelta(days=30)
    