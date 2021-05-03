from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.sponsors_model import SponsorListModels
from models.volunteer_models import VolunteerModel
from resources.volunteer_resources import GetCurrentUserDetails

_sponsor_parser = reqparse.RequestParser()
_sponsor_parser.add_argument('name',
                             type=str,
                             required=True,
                             help='Name is required')
_sponsor_parser.add_argument('image',
                             type=str,
                             required=False)


class AddSponsor(Resource):
    @jwt_required()
    def post(self):
        userJson = GetCurrentUserDetails.get(self)
        getUser = userJson[0]
        print(getUser['userName'])

        checkUser = VolunteerModel.find_by_username(getUser['userName'])

        if not checkUser.id == 1:
            return {'message': 'You are not admin user'}, 400

        data = _sponsor_parser.parse_args()

        try:
            newSponsor = SponsorListModels(
                str(data['name']).title().strip(),
                data['image']
            )
            newSponsor.save_to_db()
            return {'message': 'Sponsor added'}, 200
        except Exception as e:
            print(f'Error in adding sponsor {e}')
            return {'message': 'Internal server error'}, 500


class GetAllSponsor(Resource):
    def get(self):
        return {'sponsors': list(map(lambda x: x.sponspor_json(), SponsorListModels.find_all()))}, 200
