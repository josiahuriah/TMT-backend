from create_app import create_app, db
from models import Car, CarCategory

app = create_app()
with app.app_context():
    db.session.query(CarCategory).delete()
    db.session.commit()

    cars = [
        Car(name="Ford Focus", model="2023", category="Economy", price_per_day=70, quantity=3),
        Car(name="Chevy Cruze", model="2023", category="Economy", price_per_day=70, quantity=3),
        Car(name="Kia Forte", model="2023", category="Economy", price_per_day=70, quantity=1),
        Car(name="Ford Fusion", model="2023", category="Sedan", price_per_day=80, quantity=2),
        Car(name="Dodge Caravan", model="2023", category="Van", price_per_day=120, quantity=3),
        Car(name="Chevy Orlando", model="2023", category="Van", price_per_day=120, quantity=1),
        Car(name="Dodge Journey", model="2023", category="SUV", price_per_day=90, quantity=8),
        Car(name="Suburban", model="2023", category="Luxury", price_per_day=165, quantity=1),
        Car(name="Lincoln MKT", model="2023", category="Luxury", price_per_day=165, quantity=1),
        Car(name="Audi Q7", model="2023", category="Luxury", price_per_day=165, quantity=1),
    ]

    categories = [
        (1, 'Economy', '/assets/economy.png', 'Chevy Cruze, Kia Forte, Ford Focus', 70),
        (2, 'Sedan', '/assets/sedan.png', 'Ford Fusion', 80),
        (3, 'Van', '/assets/van.png', 'Dodge Caravan, Chevy Orlando', 120),
        (4, 'SUV', '/assets/suv.png', 'Dodge Journey', 90),
        (5, 'Luxury', '/assets/luxury.png', 'Suburban, Lincoln MKT, Audi Q7', 165)
    ]

    for id, title, image, description, rate in categories:
        car_category = CarCategory(
            id=id,
            title=title,
            image=image,
            description=description,
            rate=rate
        )
        db.session.add(car_category)

    db.session.bulk_save_objects(cars)
    db.session.commit()
    print(f"Seeded database with {len(cars)} unique cars and categories")
    db.session.bulk_save_objects(cars)
    db.session.commit()
    print("Database seeded with cars.")