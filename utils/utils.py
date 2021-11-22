from models import Genre, Movie, Users
from sanic.log import logger


def try_or(fn, default):
    try:
        return fn()
    except Exception:
        return default


async def insert_movie(movie_obj):
    if (
        len(movie_obj.get('name')) == 0
        and len(movie_obj.get('year_release')) == 0
        and len(movie_obj.get('director')) == 0
        and movie_obj.get('genre') == []
    ):
        return False
    try:
        movie = await Movie.create(
            movie_name=movie_obj.get('name', ''),
            popularity=movie_obj.get('99popularity', ''),
            year_release=movie_obj.get('year_release', ''),
            imdbScore=movie_obj.get('imdb_score', ''),
            director=movie_obj.get('director', ''),
        )
        genre_objs = []
        for g_name in movie_obj.get('genre', []):
            genre_idk = await Genre.create(genre_name=g_name)
            genre_objs.append(genre_idk)

        await movie.genre.add(*genre_objs)
        return True

    except Exception as e:
        logger.info('Error while inserting movie %s', e)
        return False


async def reterive_movie(movie_objs):

    data = []
    for i in movie_objs:
        ctx_data = {
            'movie_name': i.movie_name,
            "popularity": i.popularity,
            "imdbScore": i.imdbScore,
            "year_release": i.year_release,
            "genre_name": try_or(
                lambda: [obj.genre_name for obj in i.genre.related_objects], []
            ),
            "director": i.director,
        }
        data.append(ctx_data)

    return data


async def reterive_genre(genre_objs):

    data = []
    for i in genre_objs:
        movies = i.movies.related_objects
        for obj in movies:
            ctx_data = {
                'movie_name': obj.movie_name,
                "popularity": obj.popularity,
                "imdbScore": obj.imdbScore,
                "year_release": obj.year_release,
                "genre_name": i.genre_name,
                "director": obj.director,
            }
            data.append(ctx_data)

    return data


async def user_isAdmin(user_id):
    user = await Users.filter(id=user_id).first()
    if user.is_admin:
        return True
    else:
        return False
