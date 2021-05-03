from db import db


class SponsorListModels(db.Model):
    __tablename__ = 'sponsors_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image = db.Column(db.Text())

    def __init__(self, name, image='NONE'):
        self.name = name
        self.image = image

    def sponspor_json(self):
        return {
            'name': self.name,
            'image': self.image
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
