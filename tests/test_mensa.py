import re


def test_mensa(client):
    """
    The function checks the following test cases.

    1. The response status code is 200 (OK).
    2. The response is a list of dictionaries.
    3. Each dictionary in the response contains the expected keys.
    4. Each item in the "item" list contains the expected keys.
    5. The "date" is in the format "YYYY-MM-DD".
    6. The "price1" and "price3" values are in the correct
    format and convertible to float.
    """
    response = client.get('/api/mensa')
    data = response.get_json()
    # Test the response status code
    assert response.status_code == 200
    # Test the response contains a list of dictionaries
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # Test each dictionary contains the expected keys
    expected_keys = {
        'item', 'date', 'weekday',
    }
    for item in data:
        assert set(item.keys()) == expected_keys

    # Test each item in the "item" list contains the expected keys
    item_keys = {
        'category', 'meal', 'foodicons',
        'price1', 'price3', 'allergens',
    }
    for meal_item in item['item']:
        assert set(meal_item.keys()) == item_keys

    # Test that "date" is in the format "YYYY-MM-DD"
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    for item in data:
        assert date_pattern.match(item['date'])

    # Test that foodicons are returned as list
    # Test that the price is a float
    for day in data:
        for meal in day['item']:
            assert isinstance(meal['foodicons'], list)
            assert isinstance(meal['price1'], float)
            assert isinstance(meal['price3'], float)
