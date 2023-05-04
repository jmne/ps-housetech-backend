from flask_restful import Api
from flask_restful import Resource

from src.resources import BusInfo

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
            Live bus data from Stadtwerke Muenster

        """
        return BusInfo().data()


# API endpoints

api.add_resource(Bus, '/api/bus')
