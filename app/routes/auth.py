from flask import (  # type: ignore
    Blueprint,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_access_cookies,
)
from pydantic import ValidationError

from app.routes.constants import menu_items
from app.routes.utils import get_data_by_request_type
from app.schemas import UserLoginSchema, UserRegisterSchema
from app.services import check_password, create_user

bp_auth = Blueprint("auth", __name__)


@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form_data = get_data_by_request_type(request)

            # Validar los datos
            user_register = UserRegisterSchema(**form_data)
        except ValidationError as e:
            # Manejo de errores en función del tipo de solicitud
            if request.content_type == "application/json":
                return jsonify({"errors": e.errors()}), 400
            else:
                flash(e.errors())
                return redirect(url_for("auth.register"))

        # Crear el usuario
        create_user(user_register)
        # Responder en función del tipo de solicitud
        if request.content_type == "application/json":
            return jsonify({"message": "Usuario creado correctamente."}), 201
        else:
            flash("Usuario creado correctamente.")
            return redirect(url_for("auth.login"))

    # Manejo para solicitudes GET
    return render_template("register.html", menu=menu_items, title="Registro")


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            form_data = get_data_by_request_type(request)

            # Validar los datos
            user_login = UserLoginSchema(**form_data)
        except ValidationError as e:
            # Manejo de errores en función del tipo de solicitud
            if request.content_type == "application/json":
                return jsonify({"errors": e.errors()}), 400
            else:
                flash(e.errors())
                return redirect(url_for("auth.login"))
        # Devolver el token.
        access_token = check_password(user_login)
        # Responder en función del tipo de solicitud
        if request.content_type == "application/json":
            if access_token:
                return jsonify(
                    {
                        "message": "Usuario logueado correctamente.",
                        "access_token": access_token,
                    }
                ), 201
            return jsonify({"message": "Error, la contraseña es errónea."}), 400
        else:
            if access_token:
                flash("Usuario logueado correctamente.")
                response = make_response(redirect(url_for("home.home")))
                set_access_cookies(response, access_token)
                return response
            flash("Error, la contraseña es errónea.")
            return redirect(url_for("auth.login"))
    return render_template("login.html", menu=menu_items, title="Login")


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@bp_auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@bp_auth.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = make_response(redirect(url_for("home.home")))
    unset_access_cookies(response)
    return response
