#!/usr/bin/env python3

from flask import Flask, make_response ,jsonify, request
from flask_migrate import Migrate

from models import db, Hero ,Power,HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.serialize() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.serialize())
    return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.serialize() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.serialize())
    return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.json
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.serialize())
        return jsonify({"errors": ["Description is required"]}), 400
    return jsonify({"error": "Power not found"}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    required_fields = ['strength', 'power_id', 'hero_id']
    if not all(field in data for field in required_fields):
        return jsonify({"errors": ["Strength, Power ID, and Hero ID are required"]}), 400
    hero_id = data['hero_id']
    power_id = data['power_id']
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if hero and power:
        hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=data['strength'])
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero.serialize())
    return jsonify({"errors": ["Hero or Power not found"]}), 404

if __name__ == '__main__':
    app.run(debug=True,port=5555)