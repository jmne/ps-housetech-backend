import io
import os
import shutil
import tempfile

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
        path = os.path.dirname(os.path.abspath(__file__))
        tempdir = tempfile.TemporaryDirectory(dir=path).name

        hti = Html2Image(
            size=(648, 480), temp_path=tempdir, custom_flags=[
                '--default-background-color=ffffff',
                '--hide-scrollbars',
                '--headless',
                '--disable-gpu',
                '--disable-audio-output',
                '--run-all-compositor-stages-before-draw',
                '--virtual-time-budget=10000',
            ],
        )
        """making it the display size of the Eink
        calling the link for the respective room number to crate a png screenshot from it

        alternatively with a HTML and CSS file"""
        hti.output_path = os.path.join(path, 'template')

        html = HTMLFactory().return_html(room_number)

        screenshot_path = hti.screenshot(
            html_str=html,
            save_as='Raum-' + room_number + '.png',
        )

        byte_arr = io.BytesIO()
        image = Image.open(screenshot_path[0])
        image.save(byte_arr, format='PNG')
        response = make_response(byte_arr.getvalue())
        response.headers['Content-Type'] = 'image/png'
        if os.path.exists(screenshot_path[0]):
            os.remove(screenshot_path[0])
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir, ignore_errors=True)
        return response
