import json
from datetime import datetime

import requests
from flask import abort


class BusTracker:
    """
    BusTracker class using the API of Stadtwerke Muenster.

    DOCS: https://api.busradar.conterra.de/#/
    bus station numbers for Leonardo-Campus: ,[Einwärts,Auswärts]
    """

    def __init__(self):
        """
        Initialization of BusTracker class.

        Args:
            self
        """
        self.stations = [4552102, 4552101]
        self.session = requests.session()
        self.start_time = ''

    def translate_to_english(self, direction):
        """
        Method to translate German directions to English.

        Args:
            self
            direction: str, direction in German

        Returns: str, direction in English
        """
        translations = {
            'ü.': 'via',
            'über': 'via',
            'üb.': 'via',
            'Hbf': 'Central Station',
            'Hauptbahnhof': 'Central Station',
            'ü.MS Hbf': 'via MS Central Station',
            'Bf': 'Train Station',
            'Bahnhof': 'Train Station',
        }
        words = direction.split()
        for i in range(len(words)):
            if words[i] in translations:
                words[i] = translations[words[i]]
        return ' '.join(words)

    def get_future_rides(self, language='de'):
        """
        Method that calls the API and transforms the data in the desired format.

        Args:
            self
            language (str): Language code ('de' for German, 'en' for English)
        Returns: List of dictionaries.
        Dictionaries contain data for the specific bus stations

        [{  "station": str, z.B. "Leonardo-Campus"
            "direction": str, # einwärts oder auswärts
            "line": str, # z.B. "9" oder "R72"
            "going_to": str, # z.B. "Hiltrup Franz-Marc-Weg"
            "planned_departure_time": time HH:MM, # z.B. "17:45"
            "actual_departure_time": time HH:MM, # z.B. "17:51"
            "minutes_delay": int, # z.B. "6"
            "minutes_until_departure": int, # z.B. "11"
            }]
        """
        result = []
        for station in self.stations:
            response = self.session.get(
                f'https://rest.busradar.conterra.de/prod/haltestellen/{station}'
                '/abfahrten?sekunden=5400&maxanzahl=3',
            )
            if response.status_code != 200:
                abort(404, description='Could not fetch data from BusAPI.')
            response = json.loads(response.text)
            try:
                for entry in response:
                    going_to = entry['richtungstext']
                    if language == 'en':
                        going_to = self.translate_to_english(going_to)
                    result.append({
                        'station': entry['lbez'],
                        'direction': 'Einwärts' if station == 4552102 else 'Auswärts',
                        'line': entry['linientext'],
                        'going_to': going_to,
                        'planned_departure_time': datetime
                        .fromtimestamp(entry['abfahrtszeit'])
                        .strftime('%H:%M'),
                        'actual_departure_time': datetime
                        .fromtimestamp(entry['tatsaechliche_abfahrtszeit'])
                        .strftime('%H:%M'),
                        'minutes_delay': int(entry['delay'] / 60),
                        'minutes_until_departure': int(
                            ((
                                datetime
                                .fromtimestamp(entry['tatsaechliche_abfahrtszeit']) -
                                datetime.now()
                            )
                                .total_seconds()) / 60,
                        ),
                    })
            except Exception as e:
                abort(404, description=e)
        return result
