from app import app
from models import Power, Hero, hero_powers, db
import random

with app.app_context():
    # Remove data from the tables
    db.session.query(Hero).delete()
    db.session.query(Power).delete()

    print("🦸‍♀️ Seeding powers...")

    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for data in powers_data:
        power = Power(**data)
        db.session.add(power)

    print("🦸‍♀️ Seeding heroes...")

    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    
    ]

    for data in heroes_data:
        hero = Hero(**data)
        db.session.add(hero)

    print("🦸‍♀️ Adding powers to heroes...")

    strengths = ["Strong", "Weak", "Average"]

    heroes = Hero.query.all()
    powers = Power.query.all()

    for hero in heroes:
        for _ in range(random.randint(1, 3)):
            power = random.choice(powers)
            strength = random.choice(strengths)

            hero_power = hero_powers.insert().values(hero_id=hero.id, power_id=power.id, strength=strength)
            db.session.execute(hero_power)

    # Commit the changes only once at the end
    db.session.commit()

    print("🦸‍♀️ Done seeding!")
