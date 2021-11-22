from environs import Env
from sanic import response
from sanic_jwt import Initialize
from sqlalchemy.ext.asyncio import create_async_engine
from tortoise.contrib.sanic import register_tortoise

from authentication.auth import (
    EmailClaim,
    NameClaim,
    authenticate,
    retrieve_refresh_token,
    retrieve_user,
    store_refresh_token,
)
from config import app
from routes.movies import add_movies, search_movies, update_movies
from routes.users import delete_user, register, update_user

env = Env()
env.read_env()

# sanic jwt
custom_claims = [NameClaim, EmailClaim]
Initialize(
    app,
    authenticate=authenticate,
    custom_claims=custom_claims,
    store_refresh_token=store_refresh_token,
    retrieve_refresh_token=retrieve_refresh_token,
    retrieve_user=retrieve_user,
    debug=True,
    claim_iat=True,
    refresh_token_enabled=True,
)


@app.route("/")
def run(request):
    return response.text("Welcome :)")


# user routes
app.add_route(register, "/register", methods=["POST"])
app.add_route(delete_user, "/users/<user_id>", methods=["DELETE"])
app.add_route(update_user, "/update_user/<user_id>", methods=["POST"])

# movies routes
app.add_route(search_movies, "/search_movies", methods=["POST"])
app.add_route(add_movies, "/add_movies", methods=["POST"])
app.add_route(update_movies, "/update_movies", methods=["POST"])


register_tortoise(
    app,
    db_url=env.str('db_url'),
    modules={"models": ["models"]},
    generate_schemas=True,
)
