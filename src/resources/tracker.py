import requests

from .proxy_config import proxies


class Tracker:
    """
    Parent Tracker class.

    All different Tracker shall inherit
    from this class, to keep proxies.
    """

    def __init__(self):
        """
        Initialization of Tracker class.

        Args:
            self.
        """
        self.session = requests.session()
        self.session.encoding = 'utf-8'
        self.session.proxies.update(proxies)
