from decouple import config
import requests

class Weather: 
    """Weather class utilizing the OpenWeatherMap API"""


    def __init__(self, lat, lon):
        """Initialize of the Weather class"""
        self.lat = lat 
        self.lon = lon
        self.api_key = config('OPEN_WEATHER_APP_KEY')


    def is_rain(self):
        """function that returns "True" if it will rain in the next 3 hours 
        Otherwise return "False"

        :return: True or False
        """
        pass