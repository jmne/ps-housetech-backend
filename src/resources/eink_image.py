import io
import os

from flask import make_response
from html2image import Html2Image
from PIL import Image

from .html_factory import HTMLFactory


class EinkImage:
    """Create E-Ink image."""

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self

        """

    def get_image(self, room_number: str):
        """Return PNG doorsign for the correct room number."""
        hti = Html2Image(
            size=(648, 480), custom_flags=[
                '--default-background-color=ffffff', '--hide-scrollbars',
            ],
        )
        """making it the display size of the Eink
        calling the link for the respective room number to crate a png screenshot from it

        alternatively with a HTML and CSS file"""
        with open(
                os.path.dirname(
                    os.path.abspath(
                        __file__,
                    ),
                ) + '/template/index.html',
        ):
            html = HTMLFactory().return_html(room_number)
            # Replace the target string
            html = html.replace('RAUM XXX', room_number)
        hti.output_path = os.path.dirname(
            os.path.abspath(
                __file__,
            ),
        ) + '/image_cache'

        path = hti.screenshot(
            html_str=html,
            save_as='Raum-' + room_number + '.png',
        )

        byte_arr = io.BytesIO()
        image = Image.open(path[0])
        image = image.convert('RGB')
        image.save(byte_arr, format='JPEG', optimize=True, quality=100)
        response = make_response(byte_arr.getvalue())
        response.headers['Content-Type'] = 'image/jpeg'
        return response
