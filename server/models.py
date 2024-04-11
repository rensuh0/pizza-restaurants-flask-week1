from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    
    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30.")
        return price
    
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
    
    @validates('name')
    def validate_name(self, key, name):
        if len(name.split()) > 50:
            raise ValueError("Name must be less than 50 words.")
        return name
    
    

class Pizza(db.Model):
    __tablename__ = 'pizza'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')