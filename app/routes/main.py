from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.routes.constants import menu_items, menu_items_login

bp_home = Blueprint("home", __name__)


@bp_home.route("/")
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    menu = menu_items_login if current_user else menu_items
    return render_template("menu.html", menu=menu, title="Inicio")
