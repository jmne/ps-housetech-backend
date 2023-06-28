from datetime import datetime
import xmltodict

from .tracker import Tracker

class PictureTracker(Tracker): 
    def __init__(self, image_id):
        super().__init__()
        self.image_id = image_id    

    def __repr__(self) -> str:
        """repr function used for the cache."""
        return "%s(%s)"%(self.__class__.__name__,self.image_id)

    
    def get_picture(self):
        """Function that adds picture base 64 blob for every employee.

        The function overwrites the image value with the base 64 blob.
        """
        if self.image_id is None: 
            return None    
        response = self.session.get(
            f'''https://www.uni-muenster.de/converis/ws/public/infoobject/get/Picture/{str(self.image_id)}'''
        )
        response_list = xmltodict.parse(response.text)
        for attr in response_list['infoObject']['attribute']:
            if attr['@name'] != 'File data':
                continue
            return attr['data']
        return None
    

