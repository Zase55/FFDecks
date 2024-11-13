from flask import render_template, request, Blueprint, jsonify # type: ignore
from app.schemas import UserRegisterSchema, UserLoginSchema
from app.models import User
from app.services import create_user, check_password
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

cards = []

api = Blueprint('api', __name__)
api_profile = Blueprint('profile', __name__)
profile_my_decks = Blueprint('my_decks', __name__)
api_card_finder = Blueprint('card_finder', __name__)
api_decks = Blueprint('decks', __name__)
api_deck_editor = Blueprint('deck_editor', __name__)
api_tournaments = Blueprint('tournaments', __name__)
api_submit_tournament = Blueprint('submit_tournament', __name__)
api_formats = Blueprint('formats', __name__)

# Definir un menú con enlaces y nombres
menu_items = [
    {'name': 'Login', 'url': '/api/login'},
    {'name': 'Inicio', 'url': '/api'},
    {'name': 'Buscador', 'url': '/api/card_finder'},
    {'name': 'Decks', 'url': '/api/decks'},
    {'name': 'Editor', 'url': '/api/deck_editor'},
    {'name': 'Torneos', 'url': '/api/tournaments'},
    {'name': 'Crear Torneo', 'url': '/api/submit_tournament'},
    {'name': 'Formatos', 'url': '/api/formats'}
]

menu_items_login = [
    {'name': 'Inicio', 'url': '/api'},
    {
        'name': 'Perfil', 'url': '#',
        'submenu': [
            {'name': 'Decks', 'url': '/api/profile/my_decks'},
            {'name': 'Torneos', 'url': '/api/profile/my_tournaments'},
            {'name': 'Mis Cartas', 'url': '/api/profile/card_binder'},
            {'name': 'Favoritos', 'url': '/api/profile/favs'}
        ]
     },
    {'name': 'Buscador', 'url': '/api/card_finder'},
    {'name': 'Decks', 'url': '/api/decks'},
    {'name': 'Editor', 'url': '/api/deck_editor'},
    {'name': 'Torneos', 'url': '/api/tournaments'},
    {'name': 'Crear Torneo', 'url': '/api/submit_tournament'},
    {'name': 'Formatos', 'url': '/api/formats'}
]

@api.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    menu = menu_items_login if current_user else menu_items
    return render_template('menu.html', menu=menu, title="Inicio")

@api_profile.route('/')
def profile():
    return render_template('menu.html', menu=menu_items, title="Perfil")

@api.route('/profile/my_decks')
def my_decks():
    return render_template('menu.html', menu=menu_items, title="Decks")

@api.route('/profile/my_tournaments')
def my_tournaments():
    return render_template('menu.html', menu=menu_items, title="Torneos")

@api.route('/profile/card_binder')
def card_binder():
    return render_template('menu.html', menu=menu_items, title="Mis Cartas")

@api.route('/profile/favs')
def favs():
    return render_template('menu.html', menu=menu_items, title="Favoritos")

@api_card_finder.route('/')
def card_finder():
    return render_template('menu.html', menu=menu_items, title="Buscador de Cartas")

@api_decks.route('/')
def decks():
    return render_template('menu.html', menu=menu_items, title="Decks")

@api_deck_editor.route('/')
def deck_editor():
    return render_template('menu.html', menu=menu_items, title="Editor de Decks")

@api_tournaments.route('/')
def tournaments():
    return render_template('menu.html', menu=menu_items, title="Torneos")

@api_submit_tournament.route('/')
def submit_tournament():
    return render_template('menu.html', menu=menu_items, title="Crear Torneo")

@api_formats.route('/')
def formats():
    return render_template('menu.html', menu=menu_items, title="Formatos")

@api.route('/cards', methods=['POST'])
def add_card():
    data = request.get_json()
    cards.append(data)
    return cards

@api.route('/cards', methods=['GET'])
def cards():
    return cards

@api.route('/register', methods=['GET','POST'])
def register():
    data = request.get_json()
    try:
        user_register = UserRegisterSchema(**data)
        if request.method == 'GET':
            return render_template('register.html', title='Registro')

    except ValidationError as e:
        return jsonify(e.errors()), 400
    #if data.validate_on_submit():
    user = create_user(user_register)
    return jsonify({"message": "Usuario creado correctamente.", "user_id": user.id}), 201
    

@api.route('/login', methods=['POST'])
def login():
    try:
        user_login = UserLoginSchema(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400
    access_token = check_password(user_login)
    if access_token:
        return jsonify({"message": "Usuario logueado correctamente.", "access_token": access_token}), 200
    return jsonify({"message": "Error, la contraseña es errónea."}), 401

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


#@lm.user_loader
def load_user(user_id):
    return User.get(user_id)