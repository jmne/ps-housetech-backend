import re
from datetime import datetime

import requests
import xmltodict


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
        self.url_de = 'https://speiseplan.stw-muenster.de/mensa_da_vinci.xml'
        self.url_en = ''  # tbd
        self.session = requests.session()

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
            # hier noch durch items loopen und mit regex einen die Allergien abdecken
            for entry in day['item']:
                allergens = re.findall(r'\((.*?)\)', entry['meal'])
                entry['allergens'] = allergens[0] if allergens else None
                entry['meal'] = re.sub(
                    r'\([^)]*\)', '',
                    entry['meal'],
                )  # filter out allergens
                try:
                    del entry['weight_unit']
                except Exception as e:
                    print("couldnt delete key 'weight_unit'", e)
                try:
                    del entry['prodgrp_id']
                except Exception as e:
                    print("couldnt delete key 'prodgrp_id'", e)

        return response_list
