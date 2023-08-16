import json
import re
from datetime import datetime

import requests
import xmltodict
from flask import abort
from flask import make_response


class MensaTracker:
    """
    MensaTracker class using the website of stw-muenster.

    https://speiseplan.stw-muenster.de/mensa_da_vinci.xml
    Use this URL in order to retreive information about meals.
    """

    def __init__(self):
        """
        Initilization of MensaTracker class.

        Args:
            self
        """
        self.session = requests.Session()
        # Plans in German
        self.url_de = {
            'davinci': 'https://speiseplan.stw-muenster.de/mensa_da_vinci.xml',
            'aasee': 'https://speiseplan.stw-muenster.de/mensa_aasee.xml',
            'ring': 'https://speiseplan.stw-muenster.de/mensa_am_ring.xml',
            'bispinghof': 'https://speiseplan.stw-muenster.de/mensa_bispinghof.xml',
        }
        # Plans in English
        self.url_en = {
            'davinci': 'https://speiseplan.stw-muenster.de/mensa_da_vinci_en.xml',
            'aasee': 'https://speiseplan.stw-muenster.de/mensa_aasee_en.xml',
            'ring': 'https://speiseplan.stw-muenster.de/mensa_am_ring_en.xml',
            'bispinghof': 'https://speiseplan.stw-muenster.de/mensa_bispinghof_en.xml',
        }
        self.result = []

    def get_meal_info(self, day_of_meals):  # noqa: C901
        """Method that returns the meal information.

        Args:
            self,
            day_of_meals: list of dictionaries

        Returns: meal_data for one whole day.
        """
        result = []
        for entry in day_of_meals:
            try:
                if type(day_of_meals) is list:
                    if (
                            entry['category'] == 'Info'
                    ):
                        continue
            except Exception as e:
                print('Could not filter out Info entries', e)
            meal_data = {}
            try:
                if entry['foodicons'] is not None:
                    meal_data['foodicons'] = entry['foodicons'].split(',')
                else:
                    meal_data['foodicons'] = None
            except Exception as e:
                meal_data['foodicons'] = None
                print('There is no foodicons key', e)
            try:
                meal_data['meal'] = re.sub(
                    r'\([^)]*\)', '',
                    entry['meal'],
                ).replace('  ', ' ').strip()  # filter out allergens
            except Exception as e:
                meal_data['meal'] = None
                print('There is no meal key', e)
            try:
                meal_data['price1'] = float(
                    entry['price1'].replace(',', '.'),
                )
                meal_data['price3'] = float(
                    entry['price3'].replace(',', '.'),
                )
            except Exception as e:
                print('Couldnt convert prices', e)
                meal_data['price1'], meal_data['price3'] = None, None

            result.append(meal_data)

        return result

    def get_current_meals(self, mensa, language):
        """
        Method that requests XML file for the Mensa meals.

        Converts the data in the desired format.

        Args:
            self,
            mensa (str): Name of the mensa.
            language (str): Language code ('de' for German, 'en' for English)

        Returns:
            List of dicts with key "weekday,"
            "date" and "item."
        """
        weekdays = {
            '0': 'Monday',
            '1': 'Tuesday',
            '2': 'Wednesday',
            '3': 'Thursday',
            '4': 'Friday',
            '5': 'Saturday',
            '6': 'Sunday',
        }
        try:
            match language:
                case 'de':
                    response = self.session.get(self.url_de[mensa], timeout=5)
                case 'en':
                    response = self.session.get(self.url_en[mensa], timeout=5)

            if response.status_code != 200:
                abort(404, description='Could not fetch data from stw-muenster.')
        except Exception as e:
            abort(404, description=e)

        response = response.text
        response_list = xmltodict.parse(response)
        try:
            response_list = response_list['menue']['date']
            for day in response_list:
                data = {
                    'date': datetime.fromtimestamp(
                        int(day['@timestamp']),
                    ).strftime('%Y-%m-%d'),
                    'weekday': weekdays[
                        str(
                            datetime.fromtimestamp(
                                int(day['@timestamp']),
                            ).weekday(),
                        )
                    ],
                    'item': None,
                }
                meal_data = self.get_meal_info(day['item'])
                data['item'] = meal_data
                self.result.append(data)
        except Exception as e:
            abort(404, description=e)

        return make_response(
            json.dumps(self.result, ensure_ascii=False), 200,
            {'Content-Type': 'application/json', 'charset': 'utf-8'},
        )
