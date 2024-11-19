from flask import Blueprint

bp_tournaments = Blueprint("tournaments", __name__)


@bp_tournaments.route("/")
def submit_tournament():
    pass
