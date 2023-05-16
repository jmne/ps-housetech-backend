from flask_restful import Api
from flask_restful import Resource

from src.resources.exchange import ExchangeCalendar

# initializing Flask API
api = Api()


class Calendar(Resource):
    """
    Calendar route for the API.

    method: GET
    """

    def get(self):  # dead: disable
        """
        Creates a CalendarTracker instance and runs get_calendar_items() method.

        Args:
            self

        Returns:
            List of calendar items
        """
        return ExchangeCalendar().get_calendar_items()


# API endpoints
api.add_resource(Calendar, '/api/calendar')
