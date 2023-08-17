import pytest

from src.resources import weather


class TestWeather:

    @pytest.fixture(scope='class')
    def tracker(self):
        return weather.WeatherTracker()

    def test_get_cleaned_weather(self, tracker):
        result = tracker.get_cleaned_weather()

        assert isinstance(result, dict)
        assert all(key in result for key in ['daily', 'hourly', 'current'])
        assert all(
            all(
                key in item for key in [
                    'day', 'weekday', 'temp', 'icon', 'pop',
                ]
            ) for item in result['daily']
        )
        assert all(
            all(
                key in item for key in [
                    'time', 'temp', 'icon', 'pop',
                ]
            ) for item in result['hourly']
        )
        assert all(
            all(
                key in item for key in [
                    'temp', 'icon',
                ]
            ) for item in result['current']
        )
