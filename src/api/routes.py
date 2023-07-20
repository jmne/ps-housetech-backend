import flask
from flask import current_app
from flask import jsonify
from flask_caching import Cache
from flask_restful import Api
from flask_restful import Resource

from src.resources.bustracker import BusTracker
from src.resources.cris import CrisTracker
from src.resources.drupal import DrupalTracker
from src.resources.eink_image import EinkImage
from src.resources.einkgenerator import EInkGenerator
from src.resources.exchange import ExchangeCalendar
from src.resources.instagram import InstagramTracker
from src.resources.mensa import MensaTracker
from src.resources.picture import PictureTracker
from src.resources.weather import WeatherTracker

# initializing Flask API
api = Api(
    catch_all_404s=True, errors={
        'NotFound':
            {
                'message': 'The requested URL was not found on the server.'
                           ' Checkout /api/help for available endpoints.',
                'status': 404,
            },
    },
)
cache = Cache(
    config={
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300,
    },
)


class Bus(Resource):
    """
    Class for the Bus API.

    method: GET
    """

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(15)
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

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(30)
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

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(30)
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


class EinkImagePNG(Resource):
    """Return PNG doorsign for the correct room number."""

    def get(self):  # dead: disable
        """Return PNG doorsign for the correct room number."""
        return EinkImage().get_image('B20120301230')


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

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(30)
    def get(self):  # dead: disable
        """
        Get the calendar items.

        Args:
            self

        Returns:
            "hello"

        """
        return ExchangeCalendar().get_calendar_items()


class Drupal(Resource):
    """Return API info."""

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(30)
    def get(self, content_type):
        """
        Return API info.

        Args:
            self

        Returns:
            Drupal events or overlays.

        """
        drupal = DrupalTracker()
        url = None
        if content_type == 'event':
            url = drupal.event_url
        elif content_type == 'overlay':
            url = drupal.overlay_url
        else:
            return """no valid input; choose 'event' or 'overlay'"""

        return drupal.get_response(url)


class Picture(Resource):
    """Return Picture for image id."""

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(86400)
    def get(self, image_id):
        """
        Return Picture for image id.

        Args:
            self, image_id

        Returns:
            picture blob as base64.
        """
        return PictureTracker(image_id).get_picture()


class Instagram(Resource):
    """Return latest Instagram posts."""

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(3600)
    def get(self):
        """
        Return latest Instagram posts.

        Args:
            self

        Returns:
            media urls, timestamps and captions
        """
        return InstagramTracker().get_latest_posts(5)


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


class Weather(Resource):
    """Return Weather."""

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({1})'

    @cache.memoize(1)
    def get(self):
        """
        Return Weather.

        Args:
            self

        Returns:
            Future weather.
        """
        return WeatherTracker().get_future_weather()


# API endpoints
api.add_resource(Bus, '/api/bus')
api.add_resource(Cris, '/api/cris')
api.add_resource(Mensa, '/api/mensa')
api.add_resource(EInk, '/api/eink')
api.add_resource(Exchange, '/api/calendar')
api.add_resource(Drupal, '/api/drupal/<content_type>')
api.add_resource(ApiInfo, '/api/help')
api.add_resource(Picture, '/api/picture/<image_id>')
api.add_resource(Instagram, '/api/instagram')
api.add_resource(Weather, '/api/weather')
api.add_resource(EinkImagePNG, '/api/einkimage')
