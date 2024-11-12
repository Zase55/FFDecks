from app.models import db, User
from werkzeug.security import generate_password_hash
from app.schemas import UserRegisterSchema

def create_user(user_data: UserRegisterSchema):
    hashed_password = generate_password_hash(user_data.password)
    user = User(username = user_data.username,
                email = user_data.email,
                password = hashed_password
            )
    db.session.add(user)
    db.session.commit()
    return user
