import os

from flask import make_response

from .tracker import Tracker


class WeatherTracker(Tracker):
    """
    Weather class using the API of OpenWeatherMap.

    DOCS: https://openweathermap.org/api/one-call-api
    """

    def __init__(self):
        """
        Initialization of Weather class.

        Args:
            self,
        """
        super().__init__()
        self.appid = os.getenv('WEATHER_API_KEY')

    def get_future_weather(self):
        """
        Call weather api and return result.

        Args:
            self
        Returns: List of dictionaries.
        Dictionaries contain data for the specific weather stations


        """
        response = self.session.get(
            'https://api.openweathermap.org/data/2.5/'
            'forecast?lat=51.97&lon=7.60&units=metric&lang=de'
            f'&appid={self.appid}',
        )

        return make_response(response.text, 200, {'Content-Type': 'application/json'})
