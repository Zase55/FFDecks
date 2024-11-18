from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    username: constr(strip_whitespace=True, min_length=3)  # type: ignore


class UserLoginSchema(UserBaseSchema):
    password: constr(min_length=8)  # type: ignore


class UserRegisterSchema(UserLoginSchema):
    email: EmailStr
