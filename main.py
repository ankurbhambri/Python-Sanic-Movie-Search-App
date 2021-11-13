# this is our 'main.py' file
from controller import my_bp
from sanic import Sanic, response
from sanic.log import logger

app = Sanic("My First Sanic App")

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337, debug=True, workers=2)
