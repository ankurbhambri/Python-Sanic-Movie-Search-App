import json
import random

import pytest
from models import Movies
from models import Users as User
from sanic import Sanic

username = None
access_token = None
refresh_token = None


@pytest.yield_fixture
def app():
    app = Sanic("test_sanic_app")
    app()
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):

    global username
    while username is None:
        i = random.randint(1, 10000)
        username = f"amichay.oren+{i}"
        if User.username_exists(username):
            username = None

    return loop.run_until_complete(sanic_client(app))


async def test_add_movies_(test_cli):
    data = {
        "movie_name": "Best movie",
        "popularity": 9,
        "imdbScore": 8.3,
        "genre": ["Action"],
        "director": "Best Driector",
    }
    resp = await test_cli.post("/add_movie", data=json.dumps(data))
    assert resp.status == 201


async def test_update_movie(test_cli):
    data = {
        "id": 109,
        "movie_name": "Test movie changed",
        "popularity": 9,
        "imdbScore": 8.3,
        "genre": ["Action"],
        "director": "Test",
    }
    resp = await test_cli.post("/update_movies", data=json.dumps(data))
    resp_json = await resp.json()
    print(resp_json)
    global access_token
    access_token = resp_json["access_token"]
    global refresh_token
    refresh_token = resp_json["refresh_token"]
    assert access_token is not None
    assert refresh_token is not None
    assert resp.status == 200
