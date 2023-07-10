from html2image import Html2Image

class EinkImage:

    def __init__(self):
        """
        Initialization of E-Ink class.

        Args:
            self

        """

    def get_data(self):

        hti = Html2Image(size=(648, 480))
        """making it the display size of the Eink"""
        """ calling the link for the respective room number to crate a png screenshot from it"""
        """hti.screenshot(url='https://www.link.de', save_as='Raumnrxx.png')"""

        """alternatively with a HTML and CSS file"""
        hti.screenshot(
        html_file='./static/imagegen/DoorsignSeed.html',
        save_as='Raumnrxx.png',
        )

        """Test method returning data."""
        return 'Raumnrxx.png'