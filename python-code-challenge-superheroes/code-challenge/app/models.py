# models.py
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    powers = db.relationship('Power', secondary='hero_powers', backref='heroes')

    def __repr__(self):
        return f'<Hero {self.name}>'

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    @validates('description')
    def validate_description(self, key, value):
        # if value is a string
        if not isinstance(value, str):
            raise ValueError("Description must be a string.")

        #  if the length of the string is between 5 and 255 characters
        if not (5 <= len(value) <= 255):
            raise ValueError("Description must be a string with length between 5 and 255 characters.")

        return value

    def __repr__(self):
        return f'<Power {self.name}, Description={self.description}'

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.Integer, nullable=False)

    @validates('strength')
    def validate_strength(self, key, value):
        # Check if strength is an integer
        if not isinstance(value, int):
            raise ValueError("Strength must be an integer.")

        # Check if strength is a positive integer
        if value < 0:
            raise ValueError("Strength must be a positive integer.")

        return value

    def __repr__(self):
        return f'<HeroPower hero_id={self.hero_id}, power_id={self.power_id}, strength={self.strength}'



      
