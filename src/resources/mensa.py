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
        response = self.session.get(self.url_de).text
        return xmltodict.parse(response)
