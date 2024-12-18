from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.users import User, db
from app.schemas import UserLoginSchema, UserRegisterSchema


def create_user(user_data: UserRegisterSchema) -> User:
    hashed_password = generate_password_hash(user_data.password)
    user = User(username=user_data.username, email=user_data.email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()


def update_confirmed_email(email: str) -> int:
    row_count = User.query.filter_by(email=email).update({User.confirmed_email: True})
    db.session.commit()
    return row_count


def check_confirm_email(user: User) -> bool:
    return user.confirmed_email


def check_password(user_login: UserLoginSchema, user: User) -> bool:
    return check_password_hash(user.password, user_login.password)


def grant_access_token(user_login: UserLoginSchema) -> str | None:
    user: User = get_user_by_username(user_login.username)
    if user and check_confirm_email(user) and check_password(user_login, user):
        access_token = create_access_token(identity=user_login.username)
        return access_token
