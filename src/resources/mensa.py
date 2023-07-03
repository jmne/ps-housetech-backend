import json
import re
from datetime import datetime

import xmltodict
from flask import make_response

from .tracker import Tracker


class MensaTracker(Tracker):
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
        super().__init__()
        self.url_de = 'https://speiseplan.stw-muenster.de/mensa_da_vinci.xml'
        self.url_en = ''  # tbd

    # TODO: appropiate adoptions for frontend implementations

    def get_current_meals(self):
        """
        Method that requests XML file for the Mensa meals.

        Converts the data in the desired format.

        Args:
            self
        Returns: Dict with keys "menue", "@location" and "date".
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

        response = self.session.get(self.url_de).text
        response_list = xmltodict.parse(response)
        response_list = response_list['menue']['date']
        for day in response_list:
            day['date'] = datetime.fromtimestamp(
                int(day['@timestamp']),
            ).strftime('%Y-%m-%d')
            day['weekday'] = weekdays[
                str(
                    datetime.fromtimestamp(int(day['@timestamp'])).weekday(),
                )
            ]
            try:
                del day['@timestamp']
            except Exception as e:
                print('There is not @timestamp key', e)
            for entry in day['item']:
                entry['foodicons'] = [entry['foodicons'].split(',')]
                allergens = re.findall(r'\((.*?)\)', entry['meal'])
                entry['allergens'] = allergens[0].split(
                    ',',
                ) if allergens else None
                entry['meal'] = re.sub(
                    r'\([^)]*\)', '',
                    entry['meal'],
                ).replace('  ', ' ').strip()  # filter out allergens
                try:
                    entry['price1'] = float(entry['price1'].replace(',', '.'))
                    entry['price3'] = float(entry['price3'].replace(',', '.'))
                except Exception as e:
                    print('couldnt convert prices to float', e)
                try:
                    del entry['weight_unit']
                    del entry['prodgrp_id']
                except Exception as e:
                    print("couldnt delete key 'prodgrp_id'/'weight_unit", e)

        return make_response(
            json.dumps(response_list, ensure_ascii=False), 200,
            {'Content-Type': 'application/json', 'charset': 'utf-8'},
        )
