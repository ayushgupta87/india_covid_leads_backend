from db import db


class ServiceTypeCategories(db.Model):
    __tablenamee__ = 'service_category'

    id = db.Column(db.Integer, primary_key=True)
    service_category = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, service_category):
        self.service_category = service_category

    def service_json(self):
        return {
            'serviceCategory': self.service_category
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

    @classmethod
    def find_by_service(cls, service_category):
        return cls.query.filter_by(service_category=service_category).first()
