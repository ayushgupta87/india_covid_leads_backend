from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.services_categories_models import ServiceTypeCategories
from models.volunteer_models import VolunteerModel
from resources.volunteer_resources import GetCurrentUserDetails

_service_parser = reqparse.RequestParser()
_service_parser.add_argument('service_category',
                             type=str,
                             required=True,
                             help='Enter category')


class AddCategories(Resource):
    @jwt_required()
    def post(self):
        userJson = GetCurrentUserDetails.get(self)
        getUser = userJson[0]
        print(getUser['userName'])

        checkUser = VolunteerModel.find_by_username(getUser['userName'])

        if not checkUser.id == 1:
            return {'message': 'You are not admin user'}, 400

        data = _service_parser.parse_args()

        check_ExistingCategory = ServiceTypeCategories.find_by_service(str(data['service_category']).title().strip())

        if check_ExistingCategory:
            return {'message': 'This category already in database'}, 400

        try:
            newCategory = ServiceTypeCategories(
                str(data['service_category']).title().strip()
            )
            newCategory.save_to_db()
            return {'message': 'Category added successfully'}, 200
        except Exception as e:
            print(f'Error while adding category {e}')
            return {'message': 'Internal server error'}, 500


class GetAllServices(Resource):
    def get(self):
        return list(map(lambda x: x.service_json(), ServiceTypeCategories.find_all())), 200
