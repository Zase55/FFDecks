from flask import flash, jsonify, make_response, redirect, url_for  # type: ignore
from flask_jwt_extended import set_access_cookies


def message_confirm_email(username, confirm_url):
    return f"""
        Hola {username},

        Gracias por registrarte. Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:
        <a href='{confirm_url}'><button>Confirmar Correo</button></a>

        Este enlace será válido por 1 hora.
        """


def control_request_content_type_error(request, e, url_for_path):
    if request.content_type == "application/json":
        return jsonify({"errors": e.errors()}), 400
    else:
        flash(e.errors())
        return redirect(url_for(url_for_path))


def control_request_content_type_register(request, task):
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


def control_request_content_type_login(request, access_token):
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
