from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from .routes import api
from .routes import cache


def create_app():
    """Initialize the Flask app.

    Returns: An instance of the Flask app
    """
    app = Flask(__name__, template_folder='../resources/template')  # initialize
    # Flask APP
    cache.init_app(app)  # initialize cache
    cache.clear()  # clear cache
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1,
    )  # fix for proxy
    CORS(
        app, origins=[
            'ps-housetech.uni-muenster.de', 'ml-de.zivgitlabpages.uni-muenster.de',
            'http://localhost:3000',  # remove localhost for production
        ],
    )  # enable CORS
    api.init_app(app)  # connecting api from routes.py with app

    return app
