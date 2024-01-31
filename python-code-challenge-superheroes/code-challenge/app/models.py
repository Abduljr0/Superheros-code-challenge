from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes_powers.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    powers = db.relationship('Power', secondary='hero_power', backref='heroes', lazy='dynamic')

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=False)

# Define the Many-to-Many relationship between Hero and Power through HeroPower
Hero.powers = db.relationship('Power', secondary='hero_power', backref='heroes', lazy='dynamic')
Power.heroes = db.relationship('Hero', secondary='hero_power', backref='powers', lazy='dynamic')
