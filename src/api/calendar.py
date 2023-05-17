from flask_restful import Api
from flask_restful import Resource

from src.resources.exchange import ExchangeCalendar

# initializing Flask API
api = Api()


class Exchange(Resource):
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
        return ExchangeCalendar().get_calendar_items()


# API endpoints

api.add_resource(Exchange, '/api/bus')
