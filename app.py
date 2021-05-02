import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///coviddata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kaizenCovidHelp'
api = Api(app)

jwt = JWTManager(app)


class HomePage(Resource):
    def get(self):
        return 'Hello world'


api.add_resource(HomePage, '/')

if __name__ == '__main__':
    # Flutter error of Connection closed while receiving data > windows OS
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True, port=5000)
