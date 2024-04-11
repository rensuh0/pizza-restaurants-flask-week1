#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
ma = Marshmallow(app)

class PizzaSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "ingredients")
       

class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "address", "pizzas")

    pizzas = ma.Nested(PizzaSchema, many=True)

class RestaurantPizzaSchema(ma.Schema):
    class Meta:
        fields = ("id", "price", "restaurant_id", "pizza_id")

class Index(Resource):

    def get(self):
        response_dict = {
            "index": "Welcome to the Pizza-Restaurant RESTful API",
        }
        response = make_response(
            response_dict,
            200,
        )
        return response

api.add_resource(Index, '/')

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurant_schema = RestaurantSchema(many=True)
        serialized_restaurants = restaurant_schema.dump(restaurants)
        print(serialized_restaurants)
        return make_response(jsonify(serialized_restaurants), 200)

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_schema = RestaurantSchema()
            serialized_restaurant = restaurant_schema.dump(restaurant)
            return make_response(jsonify(serialized_restaurant), 200)
        else:
            return make_response({"error": "Restaurant not found"}, 404)

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            return make_response({"error": "Restaurant not found"}, 404)

api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_schema = PizzaSchema(many=True)
        serialized_pizzas = pizza_schema.dump(pizzas)
        return make_response(jsonify(serialized_pizzas), 200)

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    def get(self):
        restaurant_pizzas = RestaurantPizza.query.all()
        restaurant_pizza_schema = RestaurantPizzaSchema(many=True)
        serialized_restaurant_pizzas = restaurant_pizza_schema.dump(restaurant_pizzas)
        return make_response(jsonify(serialized_restaurant_pizzas), 200)
    
    def post(self):
        data = request.get_json()
        new_restaurant_pizza = RestaurantPizza(
            price=int(data['price']),
            pizza_id=int(data['pizza_id']),
            restaurant_id=int(data['restaurant_id'])
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        restaurant_pizza_schema = RestaurantPizzaSchema()
        serialized_new_restaurant_pizza = restaurant_pizza_schema.dump(new_restaurant_pizza)
        return make_response(jsonify(serialized_new_restaurant_pizza), 201)

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
