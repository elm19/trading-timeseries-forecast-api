from flask import Blueprint

test = Blueprint('test', __name__)

@test.route('/test')
def see():
    return "<h1>Hello from a Blueprint test yeeee!<h1>"
