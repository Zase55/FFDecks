from flask import Blueprint, request

bp_cards = Blueprint("cards", __name__)

cards = []


@bp_cards.route("/", methods=["POST"])
def add_card():
    data = request.get_json()
    cards.append(data)
    return cards


@bp_cards.route("/", methods=["GET"])
def get_cards():
    return cards
