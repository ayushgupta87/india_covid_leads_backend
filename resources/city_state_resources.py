from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.city_models import IndiaCitiesStates
from models.volunteer_models import VolunteerModel
from resources.volunteer_resources import GetCurrentUserDetails

_city_parser = reqparse.RequestParser()
_city_parser.add_argument('cities_states',
                          type=str,
                          required=True,
                          help='Enter City,State')


class AddCityState(Resource):
    @jwt_required()
    def post(self):
        userJson = GetCurrentUserDetails.get(self)
        getUser = userJson[0]
        print(getUser['userName'])

        checkUser = VolunteerModel.find_by_username(getUser['userName'])

        if not checkUser.id == 1:
            return {'message': 'You are not admin user'}, 400

        data = _city_parser.parse_args()

        check_cityEntry = IndiaCitiesStates.find_by_city(str(data['cities_states']).title().strip())

        if check_cityEntry:
            return {'message': f'{data["cities_states"]} already in database'}, 400

        try:
            newCity = IndiaCitiesStates(
                str(data['cities_states']).title().strip()
            )
            newCity.save_to_db()
            return {'message': 'City added successfully'}, 200
        except Exception as e:
            print(f'Error while adding city {e}')
            return {'message': 'Internal server error'}, 500


class GetAlCitiesStates(Resource):
    def get(self):
        return list(map(lambda x: x.cities_json(), IndiaCitiesStates.find_all())), 200
