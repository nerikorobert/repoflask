from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, Hero, Power, Hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Define a common response function
def create_response(data, status_code):
    return make_response(jsonify(data), status_code)

# Home route
class Home(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO THE SUPER HEROES API."
        }
        return create_response(response_message, 200)

# Heroes routes
class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        hero_list = [
            {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
            }
            for hero in heroes
        ]
        return create_response(hero_list, 200)

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if not hero:
            return create_response({"error": "Hero not found"}, 404)

        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description,
                }
                for hero_power in hero.powers
            ]
        }
        return create_response(hero_dict, 200)

# Powers routes
class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        power_list = [
            {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            for power in powers
        ]
        return create_response(power_list, 200)

class PowerByID(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if not power:
            return create_response({"error": "Power not found"}, 404)

        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
        }
        return create_response(power_dict, 200)

class UpdatePowerDescription(Resource):
    def patch(self, id):
        data = request.get_json()
        new_description = data.get("description")

        power = Power.query.get(id)
        if not power:
            return create_response({"error": "Power not found"}, 404)

        if new_description is not None:
            power.description = new_description
            db.session.commit()
            updated_power = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            return create_response(updated_power, 200)
        else:
            return create_response({"errors": ["No description provided"]}, 400)

# Hero Powers route
class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        required_keys = ["strength", "hero_id", "power_id"]

        if not all(key in data for key in required_keys):
            return create_response({"errors": ["Validation error: Include all required keys"]}, 400)

        strength = data["strength"]
        power_id = data["power_id"]
        hero_id = data["hero_id"]

        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if not power or not hero:
            return create_response({"errors": ["Validation error: Power or Hero doesn't exist"]}, 400)

        hero_power = Hero_powers(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id
        )

        db.session.add(hero_power)
        db.session.commit()

        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }

        return create_response(power_data, 201)

# Register routes
api.add_resource(Home, '/')
api.add_resource(Heroes, '/heroes')
api.add_resource(HeroByID, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowerByID, '/powers/<int:id>')
api.add_resource(UpdatePowerDescription, '/powers/<int:id>')
api.add_resource(HeroPowers, '/hero_powers')

# Handle Not Found errors
@app.errorhandler(NotFound)
def handle_not_found(e):
    return make_response("Not Found: The requested resource does not exist.", 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
