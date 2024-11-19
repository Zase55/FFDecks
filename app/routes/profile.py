from flask import Blueprint

bp_profile = Blueprint("profile", __name__)


@bp_profile.route("/")
def profile():
    pass


@bp_profile.route("/my_decks")
def my_decks():
    pass


@bp_profile.route("/my_tournaments")
def my_tournaments():
    pass


@bp_profile.route("/card_binder")
def card_binder():
    pass


@bp_profile.route("/favs")
def favs():
    pass
