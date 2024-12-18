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
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_access_cookies,
)
from pydantic import ValidationError

from app.celery_worker import send_without_attachment
from app.routes.constants import menu_items
from app.routes.utils import get_data_by_request_type
from app.schemas import UserLoginSchema, UserRegisterSchema
from app.services import create_user, grant_access_token, update_confirmed_email

bp_auth = Blueprint("auth", __name__)

redis_client = redis.StrictRedis(
    host=environ.get("REDIS_HOST", "localhost"), port=6379, decode_responses=True
)


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

        # Generar un token único
        token = str(uuid.uuid4())

        # Almacenar el token en Redis con una expiración (por ejemplo, 1 hora)
        redis_client.setex(token, 3600, user_register.email)

        # Crear la URL de confirmación
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)

        # Enviar el correo de confirmación de manera asíncrona
        subject = "Confirma tu registro"
        message = f"""
        Hola {user_register.username},

        Gracias por registrarte. Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:
        <a href='{confirm_url}'><button>Confirmar Correo</button></a>

        Este enlace será válido por 1 hora.
        """

        # Crear el usuario
        create_user(user_register)
        task = send_without_attachment.apply_async(
            args=("sergiocobo90@hotmail.es", subject, message)
        )
        # Responder en función del tipo de solicitud
        if request.content_type == "application/json":
            return jsonify(
                {
                    "message": "Registro exitoso. Correo de confirmación enviado.",
                    "task_id": task.id,
                }
            ), 201
        else:
            flash("Registro exitoso. Correo de confirmación enviado.")
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
        access_token = grant_access_token(user_login)
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


@bp_auth.route("/confirm/<token>", methods=["GET"])
def confirm_email(token):
    email = redis_client.get(token)

    if not email:
        return jsonify({"error": "Token inválido o expirado"}), 400

    # Aquí puedes registrar al usuario en tu base de datos
    # Por ejemplo, guardar el email en una tabla de usuarios confirmados

    funcion = update_confirmed_email(email)
    print(f"{funcion} {email}")
    if update_confirmed_email(email) == 0:
        return jsonify({"error": "Se produjo un error al confirmar el registro."}), 400

    # Eliminar el token de Redis
    redis_client.delete(token)

    return jsonify({"message": f"Correo {email} confirmado con éxito"}), 200


@bp_auth.route("/task_status/<task_id>", methods=["GET"])
def get_task_status(task_id):
    """Consulta el estado de una tarea de Celery"""
    task_result = AsyncResult(task_id, app=send_without_attachment)
    return jsonify({"task_id": task_id, "status": task_result.status}), 200
