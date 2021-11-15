# this is our 'main.py' file
from asyncpg import create_pool
from sanic import Sanic, response
from sanic.log import logger
from tortoise.contrib.sanic import register_tortoise

from controller import my_bp
from models import Users

app = Sanic("My First Sanic App Oh God")

app.listener('before_server_start')


async def register_db(app, loop):
    # Create a database connection pool
    conn = "postgres://{ylfzllnk}:{9nwFIiaN4mqNdfIsJ97TxLI6owSGQoqV}@{fanny.db.elephantsql.com}:{5432}/{ylfzllnk}".format(
        user='postgres',
        password='secret',
        host='localhost',
        port=5432,
        database='some_database',
    )
    app.config['pool'] = await create_pool(
        dsn=conn,
        min_size=10,  # in bytes,
        max_size=10,  # in bytes,
        max_queries=50000,
        max_inactive_connection_lifetime=300,
        loop=loop,
    )


app.listener('after_server_stop')


async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


# registering route defined by blueprint
app.blueprint(my_bp)


# webapp path defined used 'route' decorator
@app.route("/")
def run(request):
    return response.text("Hello World !")


@app.route("/post", methods=['POST'])
def on_post(request):
    try:
        return response.json({"content": request.json})
    except Exception as ex:
        import traceback

        logger.error(f"{traceback.format_exc()}")


@app.route("/user")
async def add_user(request):
    user = await Users.create(name="New User")
    return response.json({"user": str(user)})


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
)
