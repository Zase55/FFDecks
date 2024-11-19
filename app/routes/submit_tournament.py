from flask import Blueprint

bp_submit_tournament = Blueprint("submit_tournament", __name__)


@bp_submit_tournament.route("/")
def submit_tournament():
    pass
