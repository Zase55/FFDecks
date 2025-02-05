import uuid
from os import environ

import redis
from celery.result import AsyncResult
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
    jwt_required,
    unset_access_cookies,
)
from pydantic import ValidationError

from app.celery_worker import send_without_attachment
from app.routes.constants import menu_items
from app.routes.utils import get_data_by_request_type
from app.schemas import UserLoginSchema, UserRegisterSchema
from app.services.auth import create_user, grant_access_token, update_confirmed_email
from app.util_functions.routes_auth_utils import (
    control_request_content_type_error,
    control_request_content_type_login,
    control_request_content_type_register,
    message_confirm_email,
)

bp_auth = Blueprint("auth", __name__)

redis_client = redis.StrictRedis(
    host=environ.get("REDIS_HOST", "localhost"), port=6379, decode_responses=True
)


@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            form_data = get_data_by_request_type(request)
            user_register = UserRegisterSchema(**form_data)
        except ValidationError as e:
            control_request_content_type_error(request, e, "auth.register")

        token = str(uuid.uuid4())
        redis_client.setex(token, 3600, user_register.email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)

        subject = "Confirma tu registro"
        message = message_confirm_email(user_register.username, confirm_url)

        create_user(user_register)
        task = send_without_attachment.apply_async(
            args=("sergiocf2490@gmail.com", subject, message)
        )
        control_request_content_type_register(request, task)

    # Manejo para solicitudes GET
    return render_template("register.html", menu=menu_items, title="Registro")


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            form_data = get_data_by_request_type(request)
            user_login = UserLoginSchema(**form_data)
        except ValidationError as e:
            control_request_content_type_error(request, e, "auth.login")

        access_token = grant_access_token(user_login)
        control_request_content_type_login(request, access_token)

    return render_template("login.html", menu=menu_items, title="Login")


@bp_auth.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = make_response(redirect(url_for("home.home")))
    unset_access_cookies(response)
    return response


@bp_auth.route("/confirm/<token>", methods=["GET"])
def confirm_email(token):
    email = redis_client.get(token)

    if not email:
        return jsonify({"error": "Token inválido o expirado"}), 400

    if update_confirmed_email(email) == 0:
        return jsonify({"error": "Se produjo un error al confirmar el registro."}), 400

    redis_client.delete(token)

    flash(f"Correo {email} confirmado con éxito")
    return redirect(url_for("auth.login"))


@bp_auth.route("/task_status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    task_result = AsyncResult(task_id, app=send_without_attachment)
    return jsonify({"task_id": task_id, "status": task_result.status}), 200
