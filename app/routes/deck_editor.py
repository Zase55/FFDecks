from flask import Blueprint

bp_deck_editor = Blueprint("deck_editor", __name__)


@bp_deck_editor.route("/")
def decks():
    pass
