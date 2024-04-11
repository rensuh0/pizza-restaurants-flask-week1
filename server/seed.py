from flask import Flask
from faker import Faker
from random import choice as rc
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Seed Restaurants
        restaurants = []
        for _ in range(5):
            restaurant = Restaurant(name=fake.company(), address=fake.address())
            db.session.add(restaurant)
            restaurants.append(restaurant)
        db.session.commit()

        # Seed Pizzas
        pizzas = []
        for flavor in ['Margherita', 'Pepperoni', 'Veggie']:
            pizza = Pizza(name=flavor, ingredients='Tomato, Cheese')
            db.session.add(pizza)
            pizzas.append(pizza)
        db.session.commit()

        # Seed RestaurantPizza
        for restaurant in restaurants:
            for pizza in pizzas:
                restaurant_pizza = RestaurantPizza(
                    price=fake.random_int(min=10, max=20),
                    restaurant=restaurant,
                    pizza=pizza
                )
                db.session.add(restaurant_pizza)
        db.session.commit()

        print('Database seeded!')

if __name__ == '__main__':
    seed_data()
