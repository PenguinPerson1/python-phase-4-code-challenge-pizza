#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get("/restaurants")
def get_restaurants():
    return [rest.to_dict(rules=("-restaurant_pizzas",)) for rest in Restaurant.query.all()], 200

@app.get("/restaurants/<int:id>")
def get_restaurant(id):
    rest = Restaurant.query.where(Restaurant.id == id).first()
    if rest:
        return rest.to_dict(), 200
    return {'error': 'Restaurant not found'}, 404

@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    rest = Restaurant.query.where(Restaurant.id == id).first()
    if rest:
        db.session.delete(rest)
        db.session.commit()
        return {}, 204
    return {'error': 'Restaurant not found'}, 404


@app.get("/pizzas")
def get_pizzas():
    return [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in Pizza.query.all()], 200

@app.get("/pizzas/<int:id>")
def get_pizza(id):
    pizza = Pizza.query.where(Pizza.id == id).first()
    if pizza:
        return pizza.to_dict(), 200
    return {'error': 'Pizza not found'}, 404

@app.delete("/pizzas/<int:id>")
def delete_pizza(id):
    pizza = Pizza.query.where(Pizza.id == id).first()
    if pizza:
        db.session.delete(pizza)
        db.session.commit()
        return {}, 204
    return {'error': 'Pizza not found'}, 404

@app.post('/restaurant_pizzas')
def make_new():
    try:
        restaurant_pizza = RestaurantPizza( 
            pizza_id=request.json.get('pizza_id'),
            restaurant_id = request.json.get('restaurant_id'),
            price = request.json.get('price')
            )
        db.session.add(restaurant_pizza)
        db.session.commit()
        return restaurant_pizza.to_dict(rules=('-pizza.restaurant_pizzas','-restaurant.restaurant_pizzas')), 201
    except:
        return {'errors': ['validation errors']}, 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
