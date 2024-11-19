from flask import Blueprint

bp_decks = Blueprint("decks", __name__)


@bp_decks.route("/")
def decks():
    pass
