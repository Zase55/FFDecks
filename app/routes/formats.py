from flask import Blueprint

bp_formats = Blueprint("formats", __name__)


@bp_formats.route("/")
def formats():
    pass
