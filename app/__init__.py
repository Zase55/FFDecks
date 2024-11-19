from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.config import Config
from app.models import db
from app.routes import blueprints


def create_app():
    app = Flask(__name__, template_folder="./../templates", static_folder="./../static")
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)

    # Setup the Flask-JWT-Extended extension
    JWTManager(app)

    with app.app_context():
        pass

    for blueprint in blueprints:
        app.register_blueprint(blueprint["bp"], url_prefix=blueprint["url_prefix"])

    return app
