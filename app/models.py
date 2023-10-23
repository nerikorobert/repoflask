from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

hero_powers = db.Table(
    "hero_power",
    db.Column("hero_id", db.ForeignKey("heroes.id"), primary_key=True),
    db.Column("power_id", db.ForeignKey("powers.id"), primary_key=True),
    db.Column("strength", db.String),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column("updated_at", db.DateTime, onupdate=db.func.now())
)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    powers = db.relationship("Power", secondary=hero_powers, back_populates="heroes")
    serialize_rules = ("-powers.heroes",)

    def __repr__(self):
        return f"Hero {self.name} has {self.super_name}."

class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    heroes = db.relationship("Hero", secondary=hero_powers, back_populates="powers")
    serialize_rules = ("-heroes.powers",)
