from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
from config import Config

app = Flask(__name__)
api = Api(app)

# Simuliamo un database in memoria
orders = {}

class OrderResource(Resource):
    def get(self, order_id):
        if order_id in orders:
            return orders[order_id]
        return {'message': 'Order not found'}, 404

    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        
        # Verifica che l'utente esista
        response = requests.get(f'{Config.USER_SERVICE_URL}/users/{user_id}')
        if response.status_code == 404:
            return {'message': 'User not found'}, 404
            
        order_id = str(len(orders) + 1)
        orders[order_id] = {
            'id': order_id,
            'user_id': user_id,
            'items': data['items'],
            'total': data['total']
        }
        return orders[order_id], 201

api.add_resource(OrderResource, '/orders', '/orders/<string:order_id>')

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)