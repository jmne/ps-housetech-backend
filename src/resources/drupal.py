import json

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

    def get_response(self, url):
        """Response method returning data."""
        response = self.session.get(url).text
        return json.loads(response)
