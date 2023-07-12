import json
import os
from datetime import datetime
from datetime import timedelta

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

    def get_cleaned_weather(self):
        """
        Call weather api and return result.

        Args:
            self
        Returns: List of dictionaries.
        Dictionaries contain data for the specific weather stations
        """
        now = datetime.now() - timedelta(hours=1)
        cutoff = timedelta(hours=10)

        # requesting hourly data
        response = self.session.get(
            'https://pro.openweathermap.org/data/2.5/forecast/hourly'
            '?lat=51.97&lon=7.60&units=metric&lang=de'
            f'&appid={self.appid}',
        ).text
        response_json = json.loads(response)
        hourly_data = []

        for hour in response_json['list']:
            if (
                datetime.fromtimestamp(hour['dt']) >= now
                and datetime.fromtimestamp(hour['dt']) < now + cutoff
            ):
                hourly_data.append(
                    {
                        'time': datetime.fromtimestamp(hour['dt']).strftime('%H:%M'),
                        'temp': hour['main']['temp'],
                        'icon': hour['weather'][0]['icon'],
                        'pop': hour['pop'],
                    },
                )
        # requesting daily data
        response = self.session.get(
            'https://pro.openweathermap.org/data/2.5/forecast/daily'
            '?lat=51.97&lon=7.60&units=metric&lang=de'
            f'&appid={self.appid}',
        ).text
        response_json = json.loads(response)
        daily_data = []

        for day in response_json['list']:
            daily_data.append(
                {
                    'day': datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'),
                    'weekday': datetime.fromtimestamp(day['dt']).strftime('%A'),
                    'temp': day['temp']['max'],
                    'icon': day['weather'][0]['icon'],
                    'pop': day['pop'],
                },
            )
        # requesting current data
        response = self.session.get(
            'https://api.openweathermap.org/data/2.5/'
            'weather?lat=51.97&lon=7.60&units=metric&lang=de'
            f'&appid={self.appid}',
        ).text
        response_json = json.loads(response)
        current_data = [{
            'temp': response_json['main']['temp'],
            'icon': response_json['weather'][0]['icon'],
        }]

        result = {
            'daily': daily_data,
            'hourly': hourly_data,
            'current': current_data,
        }

        return result
