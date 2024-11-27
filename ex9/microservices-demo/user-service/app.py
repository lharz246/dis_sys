from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from config import Config

app = Flask(__name__)
api = Api(app)

# Simuliamo un database in memoria
users = {}

class UserResource(Resource):
    def get(self, user_id):
        if user_id in users:
            return users[user_id]
        return {'message': 'User not found'}, 404

    def post(self):
        data = request.get_json()
        user_id = str(len(users) + 1)
        users[user_id] = {
            'id': user_id,
            'name': data['name'],
            'email': data['email']
        }
        return users[user_id], 201

api.add_resource(UserResource, '/users', '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)