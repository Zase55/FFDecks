from flask import render_template, request, Blueprint, jsonify # type: ignore
from app.schemas import UserRegisterSchema, UserLoginSchema
from app.models import User
from app.services import create_user
from pydantic import ValidationError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request

cards = []

api = Blueprint('api', __name__)

# Definir un menú con enlaces y nombres
menu_items = [
    {'name': 'Login', 'url': '/'},
    {'name': 'Inicio', 'url': '/'},
    {'name': 'Buscador', 'url': '/card_finder'},
    {'name': 'Decks', 'url': '/decks'},
    {'name': 'Editor', 'url': '/deck_editor'},
    {'name': 'Torneos', 'url': '/tournaments'},
    {'name': 'Crear Torneo', 'url': '/submit_tournament'},
    {'name': 'Formatos', 'url': '/formats'}
]

menu_items_login = [
    {'name': 'Inicio', 'url': '/'},
    {
        'name': 'Perfil', 'url': '#',
        'submenu': [
            {'name': 'Decks', 'url': '/profile/my_decks'},
            {'name': 'Torneos', 'url': '/profile/my_tournaments'},
            {'name': 'Mis Cartas', 'url': '/profile/card_binder'},
            {'name': 'Favoritos', 'url': '/profile/favs'}
        ]
     },
    {'name': 'Buscador', 'url': '/card_finder'},
    {'name': 'Decks', 'url': '/decks'},
    {'name': 'Editor', 'url': '/deck_editor'},
    {'name': 'Torneos', 'url': '/tournaments'},
    {'name': 'Crear Torneo', 'url': '/submit_tournament'},
    {'name': 'Formatos', 'url': '/formats'}
]

@api.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    menu = menu_items_login if current_user else menu_items
    return render_template('menu.html', menu=menu, title="Inicio")

@api.route('/profile')
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

@api.route('/card_finder')
def card_finder():
    return render_template('menu.html', menu=menu_items, title="Buscador de Cartas")

@api.route('/decks')
def decks():
    return render_template('menu.html', menu=menu_items, title="Decks")

@api.route('/deck_editor')
def deck_editor():
    return render_template('menu.html', menu=menu_items, title="Editor de Decks")

@api.route('/tournaments')
def tournaments():
    return render_template('menu.html', menu=menu_items, title="Torneos")

@api.route('/submit_tournament')
def submit_tournament():
    return render_template('menu.html', menu=menu_items, title="Crear Torneo")

@api.route('/formats')
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

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_register = UserRegisterSchema(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    user = create_user(user_register)
    return jsonify({"message": "Usuario creado correctamente.", "user_id": user.id}), 201

@api.route('/login', methods=['POST'])
def login():
    try:
        user_login = UserLoginSchema(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400
    user: User = User.query.filter_by(username = user_login.username).first()
    if user and check_password_hash(user.password, user_login.password):
        access_token = create_access_token(identity=user_login.username)
        return jsonify({"message": "Usuario logueado correctamente.", "access_token": access_token}), 200

        #return jsonify({"message": "Usuario logueado correctamente."}), 200
    return jsonify({"message": "Error, la contraseña es errónea."}), 401

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200