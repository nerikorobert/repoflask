#!/usr/bin/env python3
from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the models (in models.py)

# Hero-Power association table
hero_powers = db.Table('hero_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('power.id'), primary_key=True),
    db.Column('strength', db.String(10))
)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    super_name = db.Column(db.String(80), nullable=False)
    powers = db.relationship('Power', secondary=hero_powers, back_populates='heroes')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "powers": [power.to_dict() for power in self.powers]
        }

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

    heroes = db.relationship('Hero', secondary=hero_powers, back_populates='powers')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

@app.route('/')
def home():
    return make_response(jsonify({"msg": "Welcome to Hero/Power API"}), 200)

@app.route("/heroes")
def heroes():
    heroes = [hero.to_dict() for hero in Hero.query.all()]
    return make_response(jsonify({"heroes": heroes}), 200)

@app.route("/heroes/<int:id>")
def heroes_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return make_response(jsonify({"error": "Hero not found"}), 404)
    return make_response(jsonify(hero.to_dict()), 200)

@app.route("/powers")
def powers():
    powers = [power.to_dict() for power in Power.query.all()]
    return make_response(jsonify({"powers": powers}), 200)

@app.route("/powers/<int:id>", methods=["GET", "PATCH"])
def powers_by_id(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)
    
    if request.method == "GET":
        return make_response(jsonify(power.to_dict()), 200)
    elif request.method == "PATCH":
        description = request.form.get("description")
        if description and len(description) >= 20:
            setattr(power, "description", description)
            db.session.commit()
            return make_response(jsonify(power.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Validation errors"}), 400)

@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    if request.method == "POST":
        strength = request.form.get("strength")
        power_id = request.form.get("power_id")
        hero_id = request.form.get("hero_id")
        
        if strength not in ["Strong", "Weak", "Average"]:
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)
        
        new_hp = hero_powers.insert().values(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id,
        )
        db.session.execute(new_hp)
        db.session.commit()
        
        updated_hero = Hero.query.get(hero_id)
        response_data = {
            "id": updated_hero.id,
            "name": updated_hero.name,
            "super_name": updated_hero.super_name,
            "powers": [power.to_dict() for power in updated_hero.powers]
        }
        return make_response(jsonify(response_data), 201)

if __name__ == '__main__':
    app.run(port=5555)
