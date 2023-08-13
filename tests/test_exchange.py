from datetime import datetime

import pytest
from coverage.annotate import os

from src.resources.exchange import ExchangeCalendar

# Fetch the credentials from environment variables
username = os.getenv('CAL_USERNAME')
password = os.getenv('CAL_PASSWORD')
email = [room['email'] for room in ExchangeCalendar.ROOMS]

# Use pytest's fixture feature to set up and tear down a calendar for each test


@pytest.fixture(scope='module')
def calendar():
    calendar = ExchangeCalendar()
    return calendar


@pytest.mark.parametrize('adress', email)
def test_response_is_list_of_dictionaries(calendar, adress):
    """
    The function checks the following test cases.

    1. The response is a list of dictionaries.
    """

    data = calendar.get_calendar_items(adress)

    # Test the response contains a list of dictionaries
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)


@pytest.mark.parametrize('adress', email)
def test_each_dictionary_contains_expected_keys(calendar, adress):
    """Test each dictionary contains the expected keys"""

    data = calendar.get_calendar_items(adress)
    expected_keys = {
        'title', 'start', 'end', 'duration',
        'location', 'organizer_name', 'organizer_email',
    }
    for item in data:
        assert set(item.keys()) == expected_keys


@pytest.mark.parametrize('adress', email)
def test_start_and_end_are_in_ISO_format(calendar, adress):
    """Test 'start' and 'end' are in ISO format"""

    data = calendar.get_calendar_items(adress)
    for item in data:
        try:
            datetime.fromisoformat(item['start'])
            datetime.fromisoformat(item['end'])
        except ValueError:
            pytest.fail(f'Invalid ISO format: {item}')


@pytest.mark.parametrize('adress', email)
def test_duration_is_valid_time_duration(calendar, adress):
    """Test 'duration' is a valid time duration"""

    data = calendar.get_calendar_items(adress)
    for item in data:
        try:
            duration = item['duration']
            if duration.startswith('PT'):
                duration = duration[2:]  # Remove the 'PT' prefix
                hours = 0
                minutes = 0
                seconds = 0
                if 'H' in duration:
                    hours_index = duration.index('H')
                    hours = int(duration[:hours_index])
                    duration = duration[hours_index + 1:]
                if 'M' in duration:
                    minutes_index = duration.index('M')
                    minutes = int(duration[:minutes_index])
                    duration = duration[minutes_index + 1:]
                if 'S' in duration:
                    seconds_index = duration.index('S')
                    seconds = int(duration[:seconds_index])
                assert 0 <= hours < 24
                assert 0 <= minutes < 60
                assert 0 <= seconds < 60
            else:
                raise ValueError(
                    f"Invalid duration format: {item['duration']}",
                )
        except (ValueError, AssertionError):
            pytest.fail(f'Invalid duration format: {item}')


@pytest.mark.parametrize('adress', email)
def test_string_fields_are_strings(calendar, adress):
    """
    Test 'title',  'location',
    'organizer_name', and 'organizer_email' are strings

    """

    data = calendar.get_calendar_items(adress)
    for item in data:
        assert isinstance(item['title'], str)
        assert isinstance(item['location'], str)
        assert isinstance(item['organizer_name'], str)
        assert isinstance(item['organizer_email'], str)

# test for get_calendar_results method


def test_get_calendar_results():
    """
        Test 'title',  'location',
        'organizer_name', and 'organizer_email' are strings

    """

    calendar = ExchangeCalendar()
    for room in ExchangeCalendar.ROOMS:
        results = calendar.get_calendar_results(room['name'])
        assert isinstance(results, list)
        for item in results:
            assert item['title']
            assert item['start']
            assert item['end']
            assert item['duration']
            assert item['location']
            assert item['organizer_name']
            assert item['organizer_email']
