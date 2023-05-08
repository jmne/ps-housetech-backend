import requests
import json

class BusTracker:
    """ BusTracker class using the API of Stadtwerke Münster:
        DOCS: https://api.busradar.conterra.de/#/
        bus station numbers for Leonardo-Campus: [4552102,4552101],[Einwärts,Auswärts]
        """

    def __init__(self, stations):
        """
        Initilization of BusTracker class.

        Args:
            self,
            stations: List of station numbers to monitor 
            """
        self.stations = stations
        self.session = requests.session()
    
    def get_future_rides(self):
        """
        Method that calls the API and transforms the data in the desired format

        Args:
            self
        Returns: List of dictionaries. Dictionaries contain data for the specific bus stations 

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
            response = self.session.get(f"https://rest.busradar.conterra.de/prod/haltestellen/{station}/abfahrten?sekunden=1800&maxanzahl=3")
            response = json.loads(response.text)
            for entry in response:
                result.append({
                    "station": entry["lbez"],
                    "direction": "Einwärts" if station == 4552102 else "Auswärts",
                    "line": entry["linientext"],
                    "going_to": entry["richtungstext"],
                    "planned_departure_time": entry["abfahrtszeit"],
                    "actual_departure_time": entry["tatsaechliche_abfahrtszeit"],
                    "minutes_delay":entry["delay"],
                    "minutes_until_departure": "Not yet implemented"
                }) 
        print(result)
        return result

if __name__ == "__main__": 
    bustracker1 = BusTracker(stations=[4552102,4552101])
    bustracker1.get_future_rides()

