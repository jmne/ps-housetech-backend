import json
from datetime import datetime

import requests


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
            self,
            stations: List of station numbers to monitor
        """
        self.stations = [4552102, 4552101]
        self.session = requests.session()
        self.start_time = ''

    def get_future_rides(self):
        """
        Method that calls the API and transforms the data in the desired format.

        Args:
            self
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
                '/abfahrten?sekunden=1800&maxanzahl=3',
            )
            response = json.loads(response.text)
            for entry in response:
                result.append({
                    'station': entry['lbez'],
                    'direction': 'Einwärts' if station == 4552102 else 'Auswärts',
                    'line': entry['linientext'],
                    'going_to': entry['richtungstext'],
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
        return result
