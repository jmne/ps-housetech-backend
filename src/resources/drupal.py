import json

from flask import abort

from .tracker import Tracker


class DrupalTracker(Tracker):
    """DrupalTracker class using the Drupal URLS."""

    def __init__(self):
        """
        Initialization of DrupalTracker class.

        Args:
            self.
        """
        super().__init__()
        self.event_url = '''https://www.wi.uni-muenster.de/ws/informationdisplays/events'''  # noqa: E501
        self.overlay_url = '''https://www.wi.uni-muenster.de/ws/informationdisplays/overlays'''  # noqa: E501

    def get_content(self, url):
        """Response method returning data."""
        response = self.session.get(url, timeout=5)
        if response.status_code != 200:
            abort(404, description='Could not request data from Drupal.')
        response = response.text
        return json.loads(response)
