from datetime import datetime

import pytest

from src.resources.exchange import ExchangeCalendar


def test_response_is_list_of_dictionaries():
    """
    The function checks the following test cases.

    1. The response is a list of dictionaries.
    """

    calendar = ExchangeCalendar()
    data = calendar.get_calendar_items()

    # Test the response contains a list of dictionaries
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)


def test_each_dictionary_contains_expected_keys():
    """Test each dictionary contains the expected keys"""

    calendar = ExchangeCalendar()
    data = calendar.get_calendar_items()
    expected_keys = {
        'title', 'body', 'start', 'end', 'duration',
        'location', 'organizer_name', 'organizer_email',
    }
    for item in data:
        assert set(item.keys()) == expected_keys


def test_start_and_end_are_in_ISO_format():
    """Test 'start' and 'end' are in ISO format"""
    calendar = ExchangeCalendar()
    data = calendar.get_calendar_items()
    for item in data:
        try:
            datetime.fromisoformat(item['start'])
            datetime.fromisoformat(item['end'])
        except ValueError:
            pytest.fail(f'Invalid ISO format: {item}')


def test_duration_is_valid_time_duration():
    """Test 'duration' is a valid time duration"""

    calendar = ExchangeCalendar()
    data = calendar.get_calendar_items()
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


def test_string_fields_are_strings():
    """
    Test 'title', 'body', 'location',
    'organizer_name', and 'organizer_email' are strings

    """
    calendar = ExchangeCalendar()
    data = calendar.get_calendar_items()
    for item in data:
        assert isinstance(item['title'], str)
        assert item['body'] is None or isinstance(item['body'], str)
        assert isinstance(item['location'], str)
        assert isinstance(item['organizer_name'], str)
        assert isinstance(item['organizer_email'], str)
