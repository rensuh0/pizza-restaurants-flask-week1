import pytest
from models import db, Restaurant, RestaurantPizza, Pizza

# Setup for the Tests
@pytest.fixture(scope='module')
def new_restaurant():
    restaurant = Restaurant(name="Test Restaurant", address="123 Test St")
    return restaurant

@pytest.fixture(scope='module')
def new_pizza():
    pizza = Pizza(name="Test Pizza", ingredients="Cheese, Tomato Sauce")
    return pizza

@pytest.fixture(scope='module')
def new_restaurant_pizza(new_restaurant, new_pizza):
    restaurant_pizza = RestaurantPizza(
        price=20, 
        restaurant=new_restaurant, 
        pizza=new_pizza
    )
    return restaurant_pizza

def test_create_new_restaurant(new_restaurant):
    assert new_restaurant.name == "Test Restaurant"
    assert new_restaurant.address == "123 Test St"

def test_create_new_pizza(new_pizza):
    assert new_pizza.name == "Test Pizza"
    assert new_pizza.ingredients == "Cheese, Tomato Sauce"

def test_create_new_restaurant_pizza(new_restaurant_pizza):
    assert new_restaurant_pizza.price == 20
