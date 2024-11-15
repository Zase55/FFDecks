from os import environ

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///mydb.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "super-secret-key"
    JWT_SECRET_KEY = "super-secret"
    JWT_TOKEN_LOCATION = ["cookies","headers"]
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600
