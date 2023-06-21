import json

import requests

from .proxy_config import proxies


class DrupalTracker:
    """DrupalTracker class using the Drupal URLS."""

    def __init__(self):
        """
        Initialization of DrupalTracker class.

        Args:
            self.
        """
        self.event_url = '''https://www.wi.uni-muenster.de/ws/
                            informationdisplays/events'''
        self.overlay_url = '''https://www.wi.uni-muenster.de/ws/
                            informationdisplays/overlays'''
        self.session = requests.session()
        self.session.proxies.update(proxies)

    def get_response(self, url):
        """Response method returning data."""
        response = self.session.get(url).text
        return json.loads(response)
