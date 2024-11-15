from flask import Flask
from app.config import Config
from app.routes import blueprints
from app.models import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__, 
                template_folder='./../templates', 
                static_folder='./../static'
            )
    app.config.from_object(Config)
    db.init_app(app)
    #Setup the Flask-JWT-Extended extension
    JWTManager(app)

    with app.app_context():
        db.create_all()

    for blueprint in blueprints:
        app.register_blueprint( blueprint["bp"], url_prefix=blueprint["url_prefix"] )

    return app
