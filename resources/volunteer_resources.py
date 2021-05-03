import re

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jti
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.volunteer_models import VolunteerModel

_volunteer_parser = reqparse.RequestParser()
_volunteer_parser.add_argument('AppLoginPassword',
                               type=str,
                               required=False)  # covidApp
_volunteer_parser.add_argument('volunteer_name',
                               type=str,
                               required=True,
                               help='Name is required')
_volunteer_parser.add_argument('volunteer_username',
                               type=str,
                               required=True,
                               help='Username is required')
_volunteer_parser.add_argument('volunteer_contact',
                               type=str,
                               required=False)
_volunteer_parser.add_argument('volunteer_emailAddress',
                               type=str,
                               required=False)
_volunteer_parser.add_argument('password',
                               type=str,
                               required=True,
                               help='Password is required')
_volunteer_parser.add_argument('confirm_password',
                               type=str,
                               required=True,
                               help='Confirm password is required')
_volunteer_parser.add_argument('keep_private',
                               type=str,
                               required=False,
                               default='1')


class RegisterNewVolunteer(Resource):
    def post(self):
        data = _volunteer_parser.parse_args()

        if data['AppLoginPassword'] != 'covidApp':
            return {'message': 'Request from unknown source'}, 400

        # length error
        if len(data['volunteer_name']) > 16:
            return {'message': 'Name character exceeds'}, 400
        if len(data['volunteer_username']) > 16:
            return {'message': 'Username character exceeds'}, 400
        if len(data['volunteer_contact']) > 15:
            return {'message': 'Contact character exceeds'}, 400
        if len(data['volunteer_contact']) > 15:
            return {'message': 'Contact character exceeds'}, 400
        if len(data['volunteer_emailAddress']) > 30:
            return {'message': 'Email address character exceeds'}, 400
        if len(data['password']) > 15:
            return {'message': 'Email address character exceeds'}, 400
        if len(data['keep_private']) > 2:
            return {'message': 'Is private character exceeds'}, 400

        if len(data['volunteer_name']) < 5:
            return {'message': 'Name length must be five or more than five character'}, 400
        if len(data['password']) < 6:
            return {'message': 'Password length must be six or more than six character'}, 400

        if " " in data['volunteer_username']:
            return {'message': 'please enter single character in username'}, 400
        regex_username = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if not regex_username.search(data['volunteer_name']) is None:
            return {'message': 'Special character not accepted in username'}, 400

        regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if str(data['volunteer_emailAddress']).lower().strip() != '':
            if not re.search(regex_email, str(data['volunteer_emailAddress']).lower().strip()):
                return {'message': 'Email id seems invalid, please check it!'}, 400

        if str(data['volunteer_name']).strip() == '':
            return {'message': 'Name can\'t be empty'}, 400
        if str(data['volunteer_username']).strip() == '':
            return {'message': 'Username can\'t be empty'}, 400
        if str(data['password']).strip() == '':
            return {'message': 'Password can\'t be empty'}, 400

        # password checks
        if str(data['password']) != str(data['confirm_password']):
            return {'message': 'Password and confirm password not matching'}, 400

        if VolunteerModel.find_by_username(str(data['volunteer_username']).lower().strip()):
            return {'message': f'{data["volunteer_username"]} username already taken'}, 400

        try:
            newVolunteer = VolunteerModel(
                str(data['volunteer_name']).title().strip(),
                str(data['volunteer_username']).lower().strip(),
                str(data['password']).strip(),
                str(data['volunteer_contact']).strip(),
                str(data['volunteer_emailAddress']).strip(),
                str(data['keep_private']).strip(),
                '1'
            )
            newVolunteer.save_to_db()
            return {'message': 'registered successfully'}, 200
        except Exception as e:
            print(f'Error while registering new volunteer {e}')
            return {'message': 'Internal server error'}, 500


class LoginVolunteer(Resource):
    def post(self):
        _customer_login = reqparse.RequestParser()
        _customer_login.add_argument('AppLoginPassword',
                                     type=str,
                                     required=False)  # covidHelp
        _customer_login.add_argument('username',
                                     type=str,
                                     required=True,
                                     help='Username is required')
        _customer_login.add_argument('password',
                                     type=str,
                                     required=True,
                                     help='Password is required')
        data = _customer_login.parse_args()

        if data['AppLoginPassword'] != 'covidHelp':
            return {'message': 'Request from unknown source'}, 400

        check_username = VolunteerModel.find_by_username(str(data['username']).lower().strip())

        if check_username:
            if check_username.is_active != '1':
                return {'message': 'Your account disabled by admin'}, 400
            if check_username and safe_str_cmp(check_username.password, data['password']):
                access_token = create_access_token(identity=check_username.volunteer_username, fresh=True)
                refresh_token = create_refresh_token(check_username.volunteer_username)
                return {
                           'access_token': access_token,
                           'refresh_token': refresh_token
                       }, 200
            return {'message': 'Invalid credentials'}, 401
        return {'message': 'Invalid credentials'}, 401


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        check_username = VolunteerModel.find_by_username(get_jwt_identity())

        if not check_username:
            return {'message': 'Unauthorized'}, 401
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=True)
        return {'access_token': access_token}, 200


class GetCurrentUserDetails(Resource):
    @jwt_required()
    def get(self):
        check_username = VolunteerModel.find_by_username(get_jwt_identity())

        if not check_username:
            return {'userName': 'None'}, 400

        if check_username.is_active != '1':
            return {'userName': 'Disabled'}, 400

        current_user_customer = get_jwt_identity()
        return {'userName': current_user_customer}, 200


class GetVolunteerByUsername(Resource):
    def get(self, username):
        checkUser = VolunteerModel.find_by_username(str(username).lower().strip())

        if not checkUser:
            return {'message': 'Requested volunteer not found'}, 400

        if checkUser.keep_private == '1':
            return {'name': checkUser.volunteer_name,
                    'contactinfo': 'Private'}, 200

        return {'name': checkUser.volunteer_name, 'contactinfo': checkUser.volunteer_emailAddress}, 200
