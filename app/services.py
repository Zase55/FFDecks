from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from app.schemas import UserRegisterSchema, UserLoginSchema
from flask_jwt_extended import create_access_token

#función para crear los datos de registro.
def create_user(user_data: UserRegisterSchema):
    hashed_password = generate_password_hash(user_data.password)
    user = User(username = user_data.username,
                email = user_data.email,
                password = hashed_password
            )
    db.session.add(user)
    db.session.commit()
    return user

#Función para comprobar el password.
def check_password(user_login: UserLoginSchema):
    user: User = User.query.filter_by(username = user_login.username).first()
    if user and check_password_hash(user.password, user_login.password):
        access_token = create_access_token(identity=user_login.username)
        return access_token