from db import db


class IndiaCitiesStates(db.Model):
    __tablename__ = 'india_cities_states'

    id = db.Column(db.Integer, primary_key=True)
    cities_states = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, cities_states):
        self.cities_states = cities_states

    def cities_json(self):
        return {
            'indiaCitiesStates': self.cities_states
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
    def find_by_city(cls, cities_states):
        return cls.query.filter_by(cities_states=cities_states).first()
