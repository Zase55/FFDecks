from flask import render_template, request, Blueprint, jsonify, redirect, url_for, flash, make_response # type: ignore
from app.schemas import UserRegisterSchema, UserLoginSchema
from app.services import create_user, check_password
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies, unset_access_cookies
from app.routes.constants import menu_items, menu_items_login

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    menu = menu_items_login if current_user else menu_items
    return render_template('menu.html', menu=menu, title="Inicio")

@bp_auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        try:
            user_register = UserRegisterSchema(**data)
        except ValidationError as e:
            jsonify(e.errors()), 400
            return redirect(url_for('auth.register'))
        
        user = create_user(user_register)
        jsonify({"message": "Usuario creado correctamente.", "user_id": user.id}), 201
        return redirect(url_for('auth.login'))
    return render_template('register.html', menu=menu_items, title="Registro")

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            user_login = UserLoginSchema(**form_data)
        except ValidationError as e:
            flash(e.errors())
            return redirect(url_for('auth.login'))
        access_token = check_password(user_login)
        if access_token:
            flash('Usuario logueado correctamente.')
            response = make_response(redirect(url_for('auth.home')))
            set_access_cookies(response, access_token)
            return response
        flash('Error, la contraseña es errónea.')
        return redirect(url_for('auth.login'))
    return render_template('login.html', menu=menu_items, title="Login")

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@bp_auth.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@bp_auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    response = make_response(redirect(url_for('auth.home')))
    unset_access_cookies(response)
    return response
