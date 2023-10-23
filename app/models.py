from sqlalchemy.orm import validates
from sqlalchemy import MetaData, ForeignKey
from flask_sqlalchemy import SQLAlchemy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    super_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('Hero_powers', back_populates='hero')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} super_name={self.super_name})'

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('Hero_powers', back_populates='power')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} description={self.description})'

    @validates('description')
    def checks_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be longer than 20 chars")
        else:
            return description
        
class Hero_powers(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    strength = db.Column(db.String(20))  # Add the 'strength' field here
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    def __repr__(self):
        return f'(id={self.id}, heroID={self.hero_id}, strength={self.strength}, powerID={self.power_id})'
    
    def __repr__(self):
        return f'(id={self.id}, heroID={self.hero_id} strength={self.strength}) powerID={self.power_id}'

    @validates('strength')
    def checks_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be a value either 'Strong', 'Weak' or 'Average'")
        else:
            return strength