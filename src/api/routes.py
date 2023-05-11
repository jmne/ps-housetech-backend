from flask_restful import Api
from flask_restful import Resource

from src.resources.bustracker import BusTracker

# initializing Flask API
api = Api()


class Bus(Resource):
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
        return BusTracker().get_future_rides()


# API endpoints

api.add_resource(Bus, '/api/bus')
