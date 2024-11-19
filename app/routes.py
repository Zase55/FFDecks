from flask import Blueprint, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.routes.constants import menu_items, menu_items_login

cards = []

api = Blueprint("api", __name__)


@api.route("/")
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    print(current_user)
    menu = menu_items_login if current_user else menu_items
    return render_template("menu.html", menu=menu, title="Inicio")


@api.route("/cards", methods=["POST"])
def add_card():
    data = request.get_json()
    cards.append(data)
    return cards


@api.route("/cards", methods=["GET"])
def get_cards():
    return cards
