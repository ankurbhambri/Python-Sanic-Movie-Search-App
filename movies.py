import ast
import os

import aiofiles
from sanic import response
from sanic.exceptions import InvalidUsage, SanicException
from sanic_jwt.decorators import protected

from auth import retrieve_user
from main import app
from models import Movie, Users
from utils import try_or, user_isAdmin


# One time activity
# @protected()
async def upload_movies(request):

    dd = request.files["file"][0].body
    aa = dd.decode("UTF-8")
    data = ast.literal_eval(aa)
    for i in data:
        await Movie.create(
            movie_name=i.get('name', ''),
            popularity=i.get('99popularity', ''),
            imdbScore=i.get('imdb_score', ''),
            genre=i.get('genre', ''),
            director=i.get('director', ''),
        )

    return response.json({'data': data})


# @protected()
async def search_movies_id(request, *args, **kwargs):

    movie_id = try_or(lambda: int(request.path.split("/")[2]), None)

    if movie_id:
        movies = await Movie.filter(id=movie_id).first()
        data = {
            "movie_name": movies.movie_name,
            "popularity": movies.popularity,
            "imdbScore": movies.imdbScore,
            "genre": movies.genre,
            "director": movies.director,
        }
        return response.json({'response': str(data)})

    else:
        data = await Movie.all().values_list(
            "movie_name",
            "popularity",
            "imdbScore",
            "releaseDate",
            "genre",
            "director",
        )
        return response.json({'response': str(data)})


@protected()
async def add_movies(request, *args, **kwargs):

    user_id = retrieve_user(request, *args, **kwargs)
    if user_isAdmin(user_id):
        await Movie.create(
            movie_name=request.json.get('movie_name', ''),
            popularity=request.json.get('popularity', 0.0),
            imdbScore=request.json.get('imdbScore', 0.0),
            genre=request.json.get('genre', ''),
            director=request.json.get('director', ''),
        )

        return response.HTTPResponse(status=201)
    else:
        raise InvalidUsage("Not eligible to add movies !!")


@protected()
async def update_movies(request, *args, **kwargs):

    user_id = retrieve_user(request, *args, **kwargs)
    id = request.json.get('id', None)

    if user_isAdmin(user_id) and id:
        obj = await Movie.filter(id=id).first()
        await Movie.filter(id=id).update(
            movie_name=request.json.get('movie_name', obj.movie_name),
            popularity=request.json.get('popularity', obj.popularity),
            imdbScore=request.json.get('imdbScore', obj.imdbScore),
            genre=request.json.get('genre', obj.genre),
            director=request.json.get('director', obj.director),
        )
        return response.HTTPResponse(status=201)
    else:
        raise InvalidUsage("Not eligible to add movies or movie not found !!")
