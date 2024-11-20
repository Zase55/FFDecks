from os import environ

DATABASE_HOST = environ.get("DATABASE_HOST")


class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://admin:1234@{DATABASE_HOST}:5432/root"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "super-secret-key"
    JWT_SECRET_KEY = "super-secret"
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600
