from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .routes import api


def create_app():
    """Initialize the Flask app.

    Returns: An instance of the Flask app
    """
    app = Flask(__name__)  # initialize Flask APP
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1,
    )  # fix for proxy
    api.init_app(app)  # connecting api from routes.py with app

    return app
