import ast

from authentication.auth import retrieve_user
from models import Genre, Movie
from sanic import response

# from sanic.exceptions import InvalidUsage
from sanic_jwt.decorators import protected
from tortoise.functions import Q
from utils.utils import (
    insert_movie,
    reterive_genre,
    reterive_movie,
    try_or,
    user_isAdmin,
)


# Add one or many
@protected()
async def add_movies(request, *args, **kwargs):

    file_data = try_or(lambda: request.files["file"][0].body, None)
    if file_data:
        fst_dec = file_data.decode("UTF-8")
        sec_dec = ast.literal_eval(fst_dec)
        start, step, stop = (0, 100, len(sec_dec))
        count = 0
        while start <= stop:
            for i in sec_dec[start:stop]:
                if await insert_movie(i):
                    count += 1
            start = start + step

        return response.json({'Data inserted': count})
    else:
        user_id = retrieve_user(request, *args, **kwargs)
        if user_isAdmin(user_id):
            if await insert_movie(request.json):
                return response.json({'response': "Movies Added Successfully"})
            else:
                raise response.HTTPResponse(status=401)
        else:
            raise response.HTTPResponse(status=401)


async def search_movies(request, *args, **kwargs):

    data = {}

    if request.query_string:

        movies = await Movie.filter(
            id=request.query_string.split('=')[1]
        ).prefetch_related('genre')

        data = await reterive_movie(movies)

    elif request.json:
        if request.json.get('genre'):

            movies = await Genre.filter(
                genre_name__in=try_or(
                    lambda: list(request.json.get('genre')), []
                )
            ).prefetch_related('movies')
            data = await reterive_genre(movies)

        else:
            movies = await Movie.filter(
                Q(movie_name=request.json.get('name', None))
                | Q(popularity=request.json.get('popularity', None))
                | Q(year_release=request.json.get('year_release', None))
                | Q(imdbScore=request.json.get('imdbScore', None))
                | Q(director=request.json.get('director', None))
            ).prefetch_related('genre')

            if not movies:
                return response.json(
                    {'response': "No movies found with given attributes"}
                )
            data = await reterive_movie(movies)
    else:
        movies = await Movie.all().prefetch_related('genre')
        data = await reterive_movie(movies)

    return response.json({'response': data})


@protected()
async def update_movies(request, *args, **kwargs):

    user_id = retrieve_user(request, *args, **kwargs)
    id = request.json.get('id', None)

    if user_isAdmin(user_id) and id:
        obj = await Movie.filter(id=id).first()
        await Movie.filter(id=id).update(
            movie_name=request.json.get('movie_name', obj.movie_name),
            popularity=request.json.get('popularity', obj.popularity),
            year_release=request.json.get('year_release', ''),
            imdbScore=request.json.get('imdbScore', obj.imdbScore),
            genre=request.json.get('genre', obj.genre),
            director=request.json.get('director', obj.director),
        )
        return response.HTTPResponse(status=201)
    else:
        raise response.HTTPResponse(status=401)
