from flask import render_template, request, Blueprint, jsonify # type: ignore
from app.schemas import UserRegisterSchema
from app.services import create_user
from pydantic import ValidationError

cards = []

api = Blueprint('api', __name__)

# Definir un menú con enlaces y nombres
menu_items = [
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
def home():
    return render_template('menu.html', menu=menu_items, title="Inicio")

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