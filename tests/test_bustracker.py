from datetime import datetime
from datetime import timedelta

import regex as re


def test_bustracker(client):
    """
    The function checks the following test cases.

    1. The response status code is 200 (OK).
    2. The response is a list of dictionaries.
    3. Each dictionary in the response contains the expected keys.
    4. The response contains both "Einwärts" and "Auswärts" directions.
    5. The "minutes_until_departure" value is greater than or equal to 0 for each item.
    6. The "minutes_delay" value is greater than or equal to 0 for each item.
    7. The actual_departure_time and planned_departure_time are in the format "HH:MM".
    8. The actual_departure_time is consistent with the minutes_delay.
    """
    response = client.get('/api/bus')
    data = response.get_json()
    # Test the response status code
    assert response.status_code == 200
    # Test the response contains a list of dictionaries
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # Test each dictionary contains the expected keys
    expected_keys = {
        'station', 'direction', 'line', 'going_to',
        'planned_departure_time', 'actual_departure_time',
        'minutes_delay', 'minutes_until_departure',
    }
    for item in data:
        assert set(item.keys()) == expected_keys

    # Test the response contains both "Einwärts" and "Auswärts" directions
    directions = {item['direction'] for item in data}
    assert 'Einwärts' in directions and 'Auswärts' in directions

    # Test the "minutes_until_departure" is greater than or equal to 0 for each item
    assert all(item['minutes_until_departure'] >= 0 for item in data)

    # Test the "minutes_delay" is greater than or equal to 0 for each item
    assert all(item['minutes_delay'] >= 0 for item in data)

    # Test that actual_departure_time and planned_departure_time
    # are in the format "HH:MM"
    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    for item in data:
        assert time_pattern.match(item['planned_departure_time'])
        assert time_pattern.match(item['actual_departure_time'])

    # Test the actual_departure_time is consistent with minutes_delay
    for item in data:
        planned = datetime.strptime(item['planned_departure_time'], '%H:%M')
        actual = datetime.strptime(item['actual_departure_time'], '%H:%M')
        delay = timedelta(minutes=item['minutes_delay'])
        assert actual == planned + delay
