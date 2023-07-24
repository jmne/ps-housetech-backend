from flask import Blueprint
from flask import current_app as app
from flask import jsonify
from flask import make_response
from flask import redirect
from flask_caching import Cache

from src.resources.bustracker import BusTracker
from src.resources.cris import CrisTracker
from src.resources.drupal import DrupalTracker
from src.resources.einkgenerator import EInkGenerator
from src.resources.event import EventManager
from src.resources.exchange import ExchangeCalendar
from src.resources.instagram import InstagramTracker
from src.resources.mensa import MensaTracker
from src.resources.picture import PictureTracker
from src.resources.weather import WeatherTracker

api = Blueprint('api', __name__)

# initializing Flask API
cache = Cache(
    config={
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300,
    },
)


@api.get('/bus')  # type: ignore[attr-defined]
@cache.cached(15)
def bus():  # dead: disable
    """
    Creates an BusTracker instance.

    Runs get_future_rides() method.

    Returns:
        Future Rides in the next 30 Minutes (max three
        per direction -> six in total) as List of dicts.

    """
    return make_response(BusTracker().get_future_rides(), 200)


@api.get('/cris')  # type: ignore[attr-defined]
@cache.cached(3600)
def cris():
    """
    Creates a CrisTracker instance.

    Runs get_cris_data() method.

    Returns:
        Events of the current day as List of dicts.

    """
    return make_response(CrisTracker().get_cris_data(), 200)


@api.get('/mensa/<mensa_name>')  # type: ignore[attr-defined]
@cache.cached(86400)
def mensa(mensa_name):
    """
    Creates a MensaTracker instance.

    Runs get_current_meals() method.

    Args:
        mensa_name: Name of the mensa.

    Returns:
        Menu of the current day as List of dicts.

    """
    return make_response(MensaTracker().get_current_meals(mensa_name), 200)


@api.get('/eink/<room_number>')  # type: ignore[attr-defined]
@cache.cached(86400)
def eink(room_number):  # dead: disable
    """
    Creates an EInkGenerator instance.

    Runs generate() method.

    Args:
        room_number: Nr of the room.

    Returns:
        E-Ink image as hex.

    """
    return make_response(EInkGenerator().get_data(room_number), 200)


@api.get('/calendar')  # type: ignore[attr-defined]
@cache.cached(300)
def calendar():
    """
    Creates an ExchangeCalendar instance.

    Runs get_calendar_items() method.

    Returns:
        Calendar of the current day as List of dicts.

    """
    return make_response(ExchangeCalendar().get_calendar_items(), 200)


@api.get('/drupal/<content_type>')  # type: ignore[attr-defined]
@cache.cached(300)
def drupal(content_type):  # dead: disable
    """
    Creates a DrupalTracker instance.

    Runs get_content() method.

    Args:
        content_type: Type of the content.

    Returns:
        Content of the current day as List of dicts.

    """
    drupal_object = DrupalTracker()
    if content_type == 'event':
        url = drupal_object.event_url
    elif content_type == 'overlay':
        url = drupal_object.overlay_url
    else:
        return make_response("No valid input; choose 'event' or 'overlay'", 400)

    return make_response(drupal_object.get_content(url), 200)


@api.get('/picture/<image_id>')  # type: ignore[attr-defined]
@cache.cached(86400)
def picture(image_id):  # dead: disable
    """
    Creates a PictureTracker instance.

    Runs get_picture() method.

    Args:
        image_id: ID of the image.

    Returns:
        Image as bytes.

    """
    return PictureTracker().get_picture(image_id)


@api.get('/instagram')  # type: ignore[attr-defined]
@cache.cached(3600)
def instagram():  # dead: disable
    """
    Creates an InstagramTracker instance.

    Runs get_pictures() method.

    Returns:
        List of Instagram pictures as List of dicts.

    """
    return make_response(InstagramTracker().get_latest_posts(5), 200)


@api.get('/weather')  # type: ignore[attr-defined]
@cache.cached(1800)
def weather():  # dead: disable
    """
    Creates a WeatherTracker instance.

    Runs get_cleaned_weather() method.

    Returns:
        Weather forecast for the next 24 hours / days as List of dicts.

    """
    return make_response(WeatherTracker().get_cleaned_weather(), 200)


@api.get('/event')  # type: ignore[attr-defined]
@cache.cached(3600)
def event():  # dead: disable
    """
    Creates an EventManager instance.

    Runs determine_event() method.

    Returns:
        Events of the current day as List of dicts.

    """
    return make_response(EventManager().determine_event(), 200)


# Helper routes
@api.get('/')  # type: ignore[attr-defined]
def redirect_to_docs():  # dead: disable
    """Redirect to API documentation."""
    return redirect(
        '/api/help',  # noqa: E501
        code=302,
    )


@api.app_errorhandler(404)  # type: ignore[attr-defined]
def page_not_found():  # dead: disable
    """Redirect to API documentation."""
    return redirect(
        '/api/help',  # noqa: E501
        code=302,
    )


@api.get('/help')  # type: ignore[attr-defined]
def site_map():  # dead: disable
    """
    Print available API endpoints.

    Returns:
        List of available endpoints.

    """
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    for key in func_list:
        func_list[key] = func_list[key].replace('\n', '').replace(
            '    ', '',
        ).replace('method', ' | method')
    return make_response(jsonify(func_list), 200)
