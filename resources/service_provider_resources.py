from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.city_models import IndiaCitiesStates
from models.provider_details import ServiceProviderDetails
from models.services_categories_models import ServiceTypeCategories
from resources.volunteer_resources import GetCurrentUserDetails

_lead_parser = reqparse.RequestParser()
_lead_parser.add_argument('provider_contact_number',
                          type=str,
                          required=True,
                          help='Contact number is required')
_lead_parser.add_argument('provider_name',
                          type=str,
                          required=True,
                          help='Provider name is required')
_lead_parser.add_argument('last_verified_date',
                          type=str,
                          required=True,
                          help='Last verified date is required')
_lead_parser.add_argument('last_verified_time',
                          type=str,
                          required=True,
                          help='Last verified time is required')
_lead_parser.add_argument('city',
                          type=str,
                          required=True,
                          help='City, State is required')
_lead_parser.add_argument('qty',
                          type=str,
                          required=False)
_lead_parser.add_argument('category',
                          type=str,
                          required=True,
                          help='Category is required')
_lead_parser.add_argument('important_link',
                          type=str,
                          required=False)


class AddNewLead(Resource):
    @jwt_required()
    def post(self):
        userJson = GetCurrentUserDetails.get(self)
        getUser = userJson[0]
        print(getUser['userName'])

        data = _lead_parser.parse_args()

        if not ServiceTypeCategories.find_by_service(str(data['category']).title().strip()):
            return {'message': 'Enter category present in dropdown'}, 400
        if not IndiaCitiesStates.find_by_city(str(data['city']).title().strip()):
            return {'message': 'Enter city present in dropdown'}, 400

        # length error
        if len(data['provider_contact_number']) > 15:
            return {'message': 'Contact number character exceeds'}, 400
        if len(data['provider_name']) > 20:
            return {'message': 'Name character exceeds, max 20 allowed'}, 400
        if len(data['last_verified_date']) > 15:
            return {'message': 'Date character exceeds'}, 400
        if len(data['last_verified_time']) > 15:
            return {'message': 'Time character exceeds'}, 400
        if len(data['city']) > 25:
            return {'message': 'City character exceeds'}, 400
        if len(data['category']) > 30:
            return {'message': 'Category character exceeds'}, 400

        if str(data['provider_contact_number']).strip() == '':
            return {'message': 'Contact can\'t be empty'}, 400
        if str(data['provider_name']).strip() == '':
            return {'message': 'Name can\'t be empty'}, 400
        if str(data['last_verified_date']).strip() == '':
            return {'message': 'Date can\'t be empty'}, 400
        if str(data['last_verified_time']).strip() == '':
            return {'message': 'Time can\'t be empty'}, 400
        if str(data['city']).strip() == '':
            return {'message': 'City can\'t be empty'}, 400
        if str(data['category']).strip() == '':
            return {'message': 'Category can\'t be empty'}, 400

        try:
            addNewLead = ServiceProviderDetails(
                str(data['provider_contact_number']).strip(),
                str(data['provider_name']).title().strip(),
                str(data['last_verified_date']).strip(),
                str(data['last_verified_time']).strip(),
                str(data['qty']).strip(),
                str(data['city']).title().strip(),
                str(data['category']).title().strip(),
                str(getUser['userName']),
                str(data['important_link']).lower().strip()
            )
            addNewLead.save_to_db()
            return {'message': 'Thank-you, your lead is live now, your help will save many lives'}, 200
        except Exception as e:
            print(f'Error while adding new lead {e}')
            return {'message': 'Internal server error'}, 500


class GetAllService(Resource):
    def get(self, service, cityState, pageNumber):

        if pageNumber.isnumeric():
            print('true, Is numeric')
            pageIs = int(pageNumber)
        else:
            print('False, Is not numeric')
            pageIs = 1

        if not ServiceTypeCategories.find_by_service(str(service).title().strip()):
            print('1')
            return {'message': 'Enter category present in dropdown'}, 400
        if not IndiaCitiesStates.find_by_city(str(cityState).title().strip()):
            print('2')
            return {'message': 'Enter city present in dropdown'}, 400

        try:
            products = ServiceProviderDetails.find_by_category_city(str(service).title().strip(),
                                                                    str(cityState).title().strip(), pageIs)
        except:
            return {'message': 'No more items to load'}, 400

        return {'leads': list(map(lambda x: x.provider_details_json(), products.items))}, 200
