from flask import Blueprint, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.routes.constants import menu_items, menu_items_login

cards = []

api = Blueprint("api", __name__)
api_profile = Blueprint("profile", __name__)
profile_my_decks = Blueprint("my_decks", __name__)
profile_my_tournaments = Blueprint("my_tournaments", __name__)
profile_card_binder = Blueprint("card_binder", __name__)
profile_favs = Blueprint("favs", __name__)
api_card_finder = Blueprint("card_finder", __name__)
api_decks = Blueprint("decks", __name__)
api_deck_editor = Blueprint("deck_editor", __name__)
api_tournaments = Blueprint("tournaments", __name__)
api_submit_tournament = Blueprint("submit_tournament", __name__)
api_formats = Blueprint("formats", __name__)
api_login = Blueprint("login", __name__)
api_register = Blueprint("register", __name__)


@api.route("/")
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    print(current_user)
    menu = menu_items_login if current_user else menu_items
    return render_template("menu.html", menu=menu, title="Inicio")


@api_profile.route("/")
def profile():
    return render_template("menu.html", menu=menu_items, title="Perfil")


@profile_my_decks.route("/")
def my_decks():
    return render_template("menu.html", menu=menu_items, title="Decks")


@profile_my_tournaments.route("/")
def my_tournaments():
    return render_template("menu.html", menu=menu_items, title="Torneos")


@profile_card_binder.route("/")
def card_binder():
    return render_template("menu.html", menu=menu_items, title="Mis Cartas")


@profile_favs.route("/")
def favs():
    return render_template("menu.html", menu=menu_items, title="Favoritos")


@api_card_finder.route("/")
def card_finder():
    return render_template("menu.html", menu=menu_items, title="Buscador de Cartas")


@api_decks.route("/")
def decks():
    return render_template("menu.html", menu=menu_items, title="Decks")


@api_deck_editor.route("/")
def deck_editor():
    return render_template("menu.html", menu=menu_items, title="Editor de Decks")


@api_tournaments.route("/")
def tournaments():
    return render_template("menu.html", menu=menu_items, title="Torneos")


@api_submit_tournament.route("/")
def submit_tournament():
    return render_template("menu.html", menu=menu_items, title="Crear Torneo")


@api_formats.route("/")
def formats():
    return render_template("menu.html", menu=menu_items, title="Formatos")


@api.route("/cards", methods=["POST"])
def add_card():
    data = request.get_json()
    cards.append(data)
    return cards


@api.route("/cards", methods=["GET"])
def get_cards():
    return cards
