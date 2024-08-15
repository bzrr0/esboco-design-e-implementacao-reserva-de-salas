import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Read from .env file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
