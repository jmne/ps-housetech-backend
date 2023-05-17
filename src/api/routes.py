from flask_restful import Api
from flask_restful import Resource

from src.resources.bustracker import BusTracker
from src.resources.cris import CrisTracker
from src.resources.mensa import MensaTracker

# initializing Flask API
api = Api()


class Bus(Resource):
    """
    Class for the Bus API.

    method: GET
    """

    def get(self):
        """
        Creates an BusTracker instance.

        Runs get_future_rides() method.

        Args:
            self

        Returns:
            Future Rides in the next 30 Minutes (max three
            per direction -> six in total) as List of dicts.

        """
        return BusTracker().get_future_rides()


class Mensa(Resource):
    """
    Class for the Mensa XML file.

    method: GET
    """

    def get(self):
        """
        Creates an MensaTracker instance.

        Runs get_current_meals() method.

        Args:
            self

        Returns:
            tbd.
        """
        return MensaTracker().get_current_meals()


class Cris(Resource):
    """
    Class for Cris-API of Uni-Muenster.

    Receiving information about employees of the
    Department of Information Systems

    method: GET
    """

    def get(self):
        """
        Creates an CrisTracker instance.

        Runs xyz() method.

        Args:
            self

        Returns:
            tbd.
        """
        return CrisTracker().xyz()


# API endpoints
api.add_resource(Bus, '/api/bus')
api.add_resource(Cris, '/api/cris')
api.add_resource(Mensa, '/api/mensa')
