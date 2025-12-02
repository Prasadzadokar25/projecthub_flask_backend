import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prasad258956652382')
    BASE_URL = os.environ.get('BASE_URL', 'http://192.168.167.228:5000')
    # Database URL (SQLAlchemy style). Override with env var in production.
    DATABASE_URL = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:##Prasad25@localhost/projecthubdb')
    # Public paths that don't require authentication
    PUBLIC_PATHS = ['/', '/checkLogin','/users/checkNumber','/users/create']
