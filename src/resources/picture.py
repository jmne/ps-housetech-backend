import base64
from io import BytesIO

import xmltodict
from flask import abort
from flask import make_response
from PIL import Image
from PIL import ImageFile

from .tracker import Tracker

ImageFile.LOAD_TRUNCATED_IMAGES = True


class PictureTracker(Tracker):
    """Class that handles the picture requests."""

    def __init__(self):
        """Initialize the PictureTracker class."""
        super().__init__()

    def get_picture(self, image_id):
        """Function that adds picture base 64 blob for every employee.

        The function overwrites the image value with the base 64 blob.
        """
        if image_id is None:
            return None
        response = self.session.get(
            f'''https://www.uni-muenster.de/converis/ws/public/infoobject/get/Picture/{str(image_id)}''',  # noqa: E501
        )
        if response.status_code != 200:
            abort(404, description='Could not request data for picture.')
        response_list = xmltodict.parse(response.text)
        for attr in response_list['infoObject']['attribute']:
            if attr['@name'] != 'File data':
                continue
            image = Image.open(
                BytesIO(
                    base64.urlsafe_b64decode(attr['data'].replace('"', '')),
                ),
            )
            aspect_ratio = image.height / image.width
            new_width = 1000
            new_height = int(new_width * aspect_ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            byte_arr = BytesIO()
            image.save(byte_arr, format='JPEG', optimize=True, quality=90)
            response = make_response(byte_arr.getvalue())
            response.headers['Content-Type'] = 'image/jpeg'
            return response
        return None
