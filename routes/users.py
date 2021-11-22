from authentication.auth import encrypt, password_validator, retrieve_user
from models import Users
from sanic import response
from sanic.exceptions import InvalidUsage, SanicException
from sanic_jwt.decorators import protected


async def register(request, *args, **kwargs):
    if (
        request.json is None
        or "username" not in request.json
        or "password" not in request.json
    ):
        raise InvalidUsage("invalid payload (should be {email, password})")
    password = request.json["password"]
    if not password_validator(password):
        raise InvalidUsage("password does not match minimum requirements")
    name = request.json.get("name", '')
    username = request.json.get("username")
    is_admin = request.json.get('is_admin', False)

    if await Users.exists(username=username):
        raise response.HTTPResponse(status=401)

    user = await Users.create(
        name=name,
        username=username,
        password=encrypt(request.json["password"]),
        is_admin=is_admin,
    )
    return response.json({"User created successfuly": str(user)})


async def update_user(request, *args, **kwargs):

    try:
        requested_user_id = int(request.path.split("/")[2])
    except ValueError as e:
        raise InvalidUsage(e)

    token_user_id = retrieve_user(request, args, kwargs)
    user = await Users.filter(id=requested_user_id).first()
    name = request.json.get("name", user.name)
    username = request.json.get("username", user.username)
    password = encrypt(request.json.get("password", user.password))
    is_active = request.json.get("is_active", user.is_active)

    if not user.id != token_user_id:
        raise response.HTTPResponse(status=401)

    await Users.filter(id=requested_user_id).update(
        name=name, username=username, password=password, is_active=is_active
    )

    return response.HTTPResponse(status=201)


@protected()
async def delete_user(request, *args, **kwargs):

    try:
        requested_user_id = int(request.path.split("/")[2])
    except ValueError as e:
        raise InvalidUsage(e)

    user_id = retrieve_user(request, args, kwargs)
    token_user = await Users.filter(id=user_id).first()
    user = await Users.filter(id=requested_user_id).first()

    if not token_user.is_admin:
        raise response.HTTPResponse(status=401)

    if user is None:
        raise response.HTTPResponse(status=404)

    if not user.is_active:
        raise response.HTTPResponse(status=404)

    await Users.filter(id=requested_user_id).update(is_active=False)

    return response.HTTPResponse(status=201)
