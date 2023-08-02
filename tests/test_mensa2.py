import pytest

from src.resources import mensa


class TestMensa:

    # cafeterias = [
    #     'davinci', 'aasee', 'ring', 'bispinghof',
    # ]
    # languages = ['de', 'en']
    # for language in languages:
    #     for mensa in cafeterias:
    #         response = client.get(f'/api/mensa/{mensa}/{language}')
    #         data = response.get_json()
    #         assert response.status_code == 200

    @pytest.fixture(scope='class')
    def tracker(self):
        return mensa.MensaTracker()

    @pytest.mark.parametrize(
        'mensa',
        ['davinci', 'aasee', 'ring', 'bispinghof'],
    )
    def test_get_current_meals(self, tracker, mensa):
        result = tracker.get_current_meals(mensa)

        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)
        assert all(
            all(key in item for key in ['date', 'weekday', 'item'])
            for item in result
        )
        assert all(
            item['weekday'] in [
                'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday',
                'Sunday',
            ] for item in result
        )

    @pytest.mark.parametrize(
        'day_of_meals, output_data, foodicons, meal, price1, price3',
        [
            (
                [
                    {
                        'category': 'Tagesaktion',
                        'meal': 'Mediterraner Nudelsalat mit Hähnchenbrust (4,AWE,C,G,N,Gfl)',  # noqa: E501
                        'foodicons': 'Gfl',
                        'price1': '4,20',
                        'price3': '6,30',
                        'weight_unit': [],
                    },
                    {
                        'category': 'Speisenangebot',
                        'meal': 'Grünkern-Gemüsepfanne (ADI,I) mit Kressesauce (F)',
                        'foodicons': 'Vgn',
                        'price1': '1,65',
                        'price3': '2,50',
                        'weight_unit': [],
                    },
                ],
                [
                    {
                        'foodicons': ['Gfl'],
                        'allergens': ['4', 'AWE', 'C', 'G', 'N', 'Gfl'],
                        'meal': 'Mediterraner Nudelsalat mit Hähnchenbrust',
                        'price1': 4.2,
                        'price3': 6.3,
                    },
                    {
                        'foodicons': ['Vgn'],
                        'allergens': ['ADI', 'I'],
                        'meal': 'Grünkern-Gemüsepfanne mit Kressesauce',
                        'price1': 1.65,
                        'price3': 2.5,
                    },
                ],
                [
                    ['Gfl'], ['Vgn'],
                ],
                [
                    'Mediterraner Nudelsalat mit Hähnchenbrust',
                    'Grünkern-Gemüsepfanne mit Kressesauce',
                ],
                [4.2, 1.65],
                [6.3, 2.5],
            ),
            # Add more test cases for other dates...
        ],
    )
    def test_get_meal_info(
        self,
        tracker,
        day_of_meals,
        output_data,
        foodicons,
        meal,
        price1,
        price3,
    ):
        result = tracker.get_meal_info(day_of_meals)

        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)
        assert all(
            all(
                key in item for key in [
                    'foodicons', 'allergens', 'meal', 'price1', 'price3',
                ]
            )
            for item in result
        )

        # assert all(result['date'] IS IN THE FORMAT 'YYYY-MM-DD')
