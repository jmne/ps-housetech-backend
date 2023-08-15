def test_mensa(client):
    """
    The function checks the following test cases.

    1. Test the response status code
    2. Test the response contains a list of dictionaries
    3. Test each dictionary contains the expected keys
    """
    cafeterias = [
        'davinci', 'aasee', 'ring',
    ]
    languages = ['de', 'en']
    for language in languages:
        for mensa in cafeterias:
            response = client.get(f'/api/mensa/{mensa}/{language}')
            print(response)
            data = response.get_json()
            # Test the response status code
            if response.status_code == 302:
                continue
            elif response.status_code == 200:

                # Test the response contains a list of dictionaries
                assert isinstance(data, list)

                # Test each dictionary contains the expected keys
                expected_keys = {
                    'date', 'weekday', 'item',
                }
                for item in data:
                    assert set(item.keys()) == expected_keys

                # Test each item in the "item" list contains the expected keys
                item_keys = {
                    'meal', 'foodicons',
                    'price1', 'price3',
                }
                for day in data:
                    for meal in day['item']:
                        assert set(meal.keys()) == item_keys
