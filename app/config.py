from os import environ

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///mydb.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "super-secret-key"
    JWT_SECRET_KEY = "super-secret"
