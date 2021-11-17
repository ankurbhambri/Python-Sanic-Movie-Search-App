import bcrypt
import jwt
from config import app
from models import Token, Users

# from sanic import response
from sanic_jwt import Claim, exceptions


def encrypt(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(14))


# Authentication
async def authenticate(request, *args, **kwargs):
    if request.json is None:
        raise exceptions.AuthenticationFailed("missing payload")

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await Users.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")
    else:
        data = {
            'user_id': user.id,
            'username': user.username,
            'name': user.name,
            'password': user.password,
        }
        return data


def password_validator(password):
    return (
        False
        if not any(char.isdigit() for char in password)
        or not any(char.islower() for char in password)
        or not any(char.isupper() for char in password)
        else True
    )


# Token Management
async def store_refresh_token(user_id, refresh_token, *args, **kwargs):
    await Token.create(user_id=user_id, token=refresh_token)
    return True


async def retrieve_refresh_token(request, user_id, *args, **kwargs):
    found_token = await Token.filter(user_id=user_id).first()
    return found_token.token


def retrieve_user(request, *args, **kwargs):

    data = jwt.decode(request.token, options={"verify_signature": False})
    user_id = data.get('user_id', None)
    return user_id


class NameClaim(Claim):
    key = "name"

    def setup(self, payload, user):
        return user.name if hasattr(user, "name") else None

    def verify(self, value):
        return True


class EmailClaim(Claim):
    key = "username"

    def setup(self, payload, user):
        return user.username if hasattr(user, "username") else None

    def verify(self, value):
        return True
