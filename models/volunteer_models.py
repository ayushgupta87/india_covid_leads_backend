from db import db


class VolunteerModel(db.Model):
    __tablename__ = 'volunteer_table'

    id = db.Column(db.Integer, primary_key=True)
    volunteer_name = db.Column(db.String(16), nullable=False)
    volunteer_username = db.Column(db.String(16), unique=True, nullable=False)
    volunteer_contact = db.Column(db.String(15))
    volunteer_emailAddress = db.Column(db.String(30))
    password = db.Column(db.String(15))
    keep_private = db.Column(db.String(2))
    is_active = db.Column(db.String(2), default='1')

    def __init__(self, volunteer_name, volunteer_username, password, volunteer_contact='NONE',
                 volunteer_emailAddress='NONE', keep_private='NONE', is_active='1'):
        self.volunteer_name = volunteer_name
        self.volunteer_username = volunteer_username
        self.password = password
        self.volunteer_contact = volunteer_contact
        self.volunteer_emailAddress = volunteer_emailAddress
        self.keep_private = keep_private
        self.is_active=is_active

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, volunteer_username):
        return cls.query.filter_by(volunteer_username=volunteer_username).first()

