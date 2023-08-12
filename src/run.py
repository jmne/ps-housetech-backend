from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from src.api.routes import api
from src.api.routes import cache


def create_app():
    """Initialize the core Flask application."""
    load_dotenv()
    app = Flask(__name__)  # initialize
    app.config['JSON_AS_ASCII'] = False  # enable UTF-8
    app.register_blueprint(api, url_prefix='/api')  # register cache blueprint

    cache.init_app(app)  # initialize cache
    cache.clear()  # clear cache

    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1,
    )  # fix for proxy

    CORS(app)  # enable CORS
    return app


app = create_app()

if __name__ == '__main__':
    # run app on port 8000
    app.run(debug=True, port=8000)
