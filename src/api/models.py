from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PictureMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer)
    blob = db.Column(db.Text)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)
