from flask import Flask
from app.config import Config
from app.routes import api
from app.models import db

def create_app():
    app = Flask(__name__, 
                template_folder='./../templates', 
                static_folder='./../static'
            )
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api, url_prefix='/api')
    return app