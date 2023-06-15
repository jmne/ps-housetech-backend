import flask
from flask import current_app
from flask import jsonify
from flask_restful import Api
from flask_restful import Resource

from src.resources.bustracker import BusTracker
from src.resources.cris import CrisTracker
from src.resources.einkgenerator import EInkGenerator
from src.resources.exchange import ExchangeCalendar
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
        return CrisTracker().get_cris_data()


class EInk(Resource):
    """Return E-Ink data from EInkGenerator API."""

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
    """Return Exchange data from Exchange API."""

    def get(self):  # dead: disable
        """
        Get the calendar items.

        Args:
            self

        Returns:
            "hello"

        """
        return ExchangeCalendar().get_calendar_items()


class ApiInfo(Resource):
    """Return API info."""

    def get(self):
        """
        Return API info.

        Args:
            self

        Returns:
            "hello"

        """
        func_list = {}
        for rule in current_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                func_list[rule.rule] = current_app.view_functions[rule.endpoint].__doc__
        for key in func_list:
            func_list[key] = func_list[key].replace('\n', '').replace(
                '    ', '',
            ).replace('method', ' | method')
        return jsonify(func_list)


# API endpoints
api.add_resource(Bus, '/api/bus')
api.add_resource(Cris, '/api/cris')
api.add_resource(Mensa, '/api/mensa')
api.add_resource(EInk, '/api/eink')
api.add_resource(Exchange, '/api/calendar')
api.add_resource(ApiInfo, '/api/help')
