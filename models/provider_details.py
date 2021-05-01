from sqlalchemy import desc

from db import db


class ServiceProviderDetails(db.Model):
    __tablename__ = 'provider_details'

    id = db.Column(db.Integer, primary_key=True)
    provider_contact_number = db.Column(db.String(15), nullable=False)
    provider_name = db.Column(db.String(20), nullable=False)
    last_verified_date = db.Column(db.String(15), nullable=False)
    last_verified_time = db.Column(db.String(15), nullable=False)
    qty = db.Column(db.String(15))
    city = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    important_link = db.Column(db.Text, default='NONE')
    verification_by = db.Column(db.String(15), nullable=False)

    def __init__(self, provider_contact_number, provider_name, last_verified_date, last_verified_time,qty, city, category,
                 verification_by, important_link='NONE'):
        self.provider_contact_number = provider_contact_number
        self.provider_name = provider_name
        self.last_verified_date = last_verified_date
        self.last_verified_time = last_verified_time
        self.qty=qty
        self.city = city
        self.category = category
        self.important_link = important_link
        self.verification_by = verification_by

    def provider_details_json(self):
        return {
            'id': self.id,
            'providerContact': self.provider_contact_number,
            'providerName': self.provider_name,
            'lastVerifiedDate': self.last_verified_date,
            'lastVerifiedTime': self.last_verified_time,
            'qty' : self.qty,
            'providerCity': self.city,
            'serviceCategory': self.category,
            'importantLink' : self.important_link,
            'verificationBy': self.verification_by
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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_category_city(cls, category, city, pageIs):
        return cls.query.order_by(desc(cls.id)).filter_by(category=category, city=city).paginate(pageIs, 50)
