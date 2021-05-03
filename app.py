import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug.serving import WSGIRequestHandler

from resources.categories_resources import AddCategories, GetAllServices
from resources.city_state_resources import AddCityState, GetAlCitiesStates
from resources.service_provider_resources import AddNewLead, GetAllService
from resources.volunteer_resources import RegisterNewVolunteer, LoginVolunteer, RefreshToken, GetCurrentUserDetails, \
    GetVolunteerByUsername

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///coviddata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kaizenCovidHelp'
api = Api(app)

jwt = JWTManager(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()


api.add_resource(RegisterNewVolunteer, '/kaizen/api/covidLeads/registerVolunteer')
api.add_resource(LoginVolunteer, '/kaizen/api/covidLeads/loginVolunteer')
api.add_resource(RefreshToken, '/kaizen/api/covidLeads/refreshTokenVolunteer')
api.add_resource(GetCurrentUserDetails, '/kaizen/api/covidLeads/currentVolunteer')

# get single volunteer name
api.add_resource(GetVolunteerByUsername, '/kaizen/api/covidLeads/volunteerDetails/<string:username>')

# add category,admin
api.add_resource(AddCategories, '/kaizen/api/covidLeads/addCategory')
# get all category
api.add_resource(GetAllServices, '/kaizen/api/covidLeads/getAllServices')
# get all cities
api.add_resource(GetAlCitiesStates, '/kaizen/api/covidLeads/getAllCities')
# add city, state
api.add_resource(AddCityState, '/kaizen/api/covidLeads/addCityState')
# add new lead
api.add_resource(AddNewLead, '/kaizen/api/covidLeads/addNewLead')
# get all leads
api.add_resource(GetAllService, '/kaizen/api/covidLeads/getAll/<string:service>/<string:cityState>/<string:pageNumber>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    # Flutter error of Connection closed while receiving data > windows OS
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True, port=5000)
