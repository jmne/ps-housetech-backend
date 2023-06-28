from api import create_app
from api.models import db, PictureMapping
from api.routes import Cris

import xmltodict
import requests 

def get_picture(image_id):
        """Function that adds picture base 64 blob for every employee.

        The function overwrites the image value with the base 64 blob.
        """
        if image_id is None: 
            return None    
        response = requests.get(
            f'''https://www.uni-muenster.de/converis/ws/public/infoobject/get/Picture/{str(image_id)}''',
            proxies = {
            'http': "http://wwwproxy.uni-muenster.de:3128",
            'https': "http://wwwproxy.uni-muenster.de:3128"}
        )
        response_list = xmltodict.parse(response.text)
        for attr in response_list['infoObject']['attribute']:
            if attr['@name'] != 'File data':
                continue
            return attr['data']
        return None

def update_picture_blobs():
    response = Cris().get()
    for person in response: 
        result =db.session.query(PictureMapping).filter(
            PictureMapping.image_id == person["image"]).first()
        if not result and person["image"] is not None: 
            entry_to_add = PictureMapping(image_id = int(person["image"]),blob= get_picture(int(person["image"])))
            db.session.add(entry_to_add)
    print("updated all pictures!")
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    update_picture_blobs()