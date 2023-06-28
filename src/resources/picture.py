import base64

import xmltodict
from flask import make_response

from .tracker import Tracker


class PictureTracker(Tracker):
    """Class that handles the picture requests."""

    def __init__(self, image_id):
        """Initialize the PictureTracker class."""
        super().__init__()
        self.image_id = image_id

    def __repr__(self) -> str:
        """Repr function used for the cache."""
        return f'{self.__class__.__name__}({self.image_id})'

    def get_picture(self):
        """Function that adds picture base 64 blob for every employee.

        The function overwrites the image value with the base 64 blob.
        """
        if self.image_id is None:
            return None
        response = self.session.get(
            f'''https://www.uni-muenster.de/converis/ws/public/infoobject/get/Picture/{str(self.image_id)}''',  # noqa: E501
        )
        response_list = xmltodict.parse(response.text)
        for attr in response_list['infoObject']['attribute']:
            if attr['@name'] != 'File data':
                continue
            response = make_response(
                base64.urlsafe_b64decode(attr['data'].replace('"', '')),
            )
            response.headers['Content-Type'] = 'image/jpg'
            return response
        return None
