from flask import Flask
from flask_cors import CORS

from .routes import api


def create_app():
    """Initialize the Flask app.

    Returns: An instance of the Flask app
    """
    app = Flask(__name__)  # initialize Flask APP
    api.init_app(app)  # connecting api from routes.py with app
    CORS(app)  #

    return app
