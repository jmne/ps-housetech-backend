import flask
from flask_restful import Api
from flask_restful import Resource

from src.resources.bustracker import BusTracker
from src.resources.einkgenerator import EInkGenerator
from src.resources.exchange import ExchangeCalendar

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


class EInk(Resource):
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
        return flask.make_response(EInkGenerator().get_data(), 200)


class Exchange(Resource):
    """
    Route for the calendar API.

    method: GET
    """

    def get(self):  # dead: disable
        """
        Get the calendar items.

        Args:
            self

        Returns:
            "hello"

        """
        return ExchangeCalendar().get_calendar_items()


# API endpoints

api.add_resource(Bus, '/api/bus')
api.add_resource(EInk, '/api/eink')
api.add_resource(Exchange, '/api/calendar')
