from flask_restful import Api
from flask_restful import Resource

from ..resources import Exchange

# initializing Flask API
api = Api()


class TestRoute(Resource):
    """
    Test route for the API.

    method: GET
    """

    def get(self):  # dead: disable
        """
        Creates an Exchange instance and runs hello() method.

        Args:
            self

        Returns:
            "hello"

        """
        ex1 = Exchange()
        return ex1.hello()


# API endpoints

api.add_resource(TestRoute, '/api/hello')
