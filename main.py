from aredis import StrictRedis
from environs import Env

# from sanic import Sanic, response
# from sanic.log import logger
from sanic_jwt import Initialize
from tortoise.contrib.sanic import register_tortoise

from auth import (
    EmailClaim,
    NameClaim,
    authenticate,
    retrieve_refresh_token,
    retrieve_user,
    store_refresh_token,
)
from config import app
from movies import add_movies, search_movies_id, update_movies, upload_movies
from users import delete_user, register, update_user

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

# user routes
app.add_route(register, "/register", methods=["POST"])
app.add_route(delete_user, "/users/<user_id>", methods=["DELETE"])
app.add_route(update_user, "/update_user/<user_id>", methods=["POST"])

# movies routes
app.add_route(upload_movies, "/upload", methods=['POST'])
app.add_route(
    search_movies_id, "/search_movies_id/<movie_id>", methods=["POST"]
)
app.add_route(add_movies, "/add_movies", methods=["POST"])
app.add_route(update_movies, "/update_movies", methods=["POST"])

register_tortoise(
    app,
    db_url="postgres://mhkhhony:FCJtWpSnS6vlRcSFNzLq1m_uWOidbh4q@fanny.db.elephantsql.com:5432/mhkhhony",
    modules={"models": ["models"]},
    generate_schemas=True,
)
