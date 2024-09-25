from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class PINGResource(Resource):

    def get(self):
        return {"response": "pong"}


class UsersResource(Resource):

    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {'hello': 'world'}


api.add_resource(PINGResource, '/ping')
api.add_resource(UsersResource, '/users')