from flask import Blueprint

bp_card_finder = Blueprint("card_finder", __name__)


@bp_card_finder.route("/")
def card_finder():
    pass
