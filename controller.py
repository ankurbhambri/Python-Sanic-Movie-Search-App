from sanic import Blueprint, response

my_bp = Blueprint('my_blueprint')


@my_bp.route('/my_bp')
def my_bp_func(request):
    return response.text('My First Blueprint')
