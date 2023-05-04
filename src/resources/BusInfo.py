import json
import urllib.request


class BusInfo:
    """Class for getting bus data from Stadtwerke Muenster."""

    def __init__(self):
        """Initialize the BusInfo class and save data."""
        self.bus_data = self.get_bus_data()
        self.stop_data = self.get_stop_data()

    def get_bus_data(self) -> dict:
        """Return the bus data."""
        with urllib.request.urlopen(
                'https://rest.busradar.conterra.de/prod/fahrzeuge',
        ) as url:
            return json.load(url)

    def get_stop_data(self) -> dict:
        """Return the bus data."""
        with urllib.request.urlopen(
                'https://rest.busradar.conterra.de/prod/haltestellen',
        ) as url:
            return json.load(url)

    def data(self) -> dict:
        """Get data from the bus and stops."""
        return {'bus_data': self.bus_data, 'stop_data': self.stop_data}
