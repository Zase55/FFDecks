from flask import Flask
from app.config import Config
from app.routes import api, api_profile, profile_my_decks, profile_my_tournaments, profile_card_binder, profile_favs, api_card_finder, api_decks, api_deck_editor, api_tournaments, api_submit_tournament, api_formats, api_login, api_register
from app.models import db
from flask_jwt_extended import JWTManager
#from flask_login import LoginManager

def create_app():
    app = Flask(__name__, 
                template_folder='./../templates', 
                static_folder='./../static'
            )
    app.config.from_object(Config)
    db.init_app(app)
    #Setup the Flask-JWT-Extended extension
    JWTManager(app)

    #Initialize login manager.
    #lm = LoginManager()
    #lm.init_app(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(api_register, url_prefix='/register')
    api.register_blueprint(api_login, url_prefix='/login')
    api.register_blueprint(api_formats, url_prefix='/formats')
    api.register_blueprint(api_submit_tournament, url_prefix='/submit_tournament')
    api.register_blueprint(api_tournaments, url_prefix='/tournaments')
    api.register_blueprint(api_deck_editor, url_prefix='/deck_editor')
    api.register_blueprint(api_decks, url_prefix='/decks')
    api.register_blueprint(api_card_finder, url_prefix='/card_finder')
    api_profile.register_blueprint(profile_my_decks, url_prefix='/my_decks')
    api_profile.register_blueprint(profile_my_tournaments, url_prefix='/my_tournaments')
    api_profile.register_blueprint(profile_card_binder, url_prefix='/card_binder')
    api_profile.register_blueprint(profile_favs, url_prefix='favs')
    api.register_blueprint(api_profile, url_prefix='/profile')
    app.register_blueprint(api, url_prefix='/api')
    return app
