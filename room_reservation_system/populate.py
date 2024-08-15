# populate_database.py
from app import create_app, db
from app.models import User, Room, Reservation
from werkzeug.security import generate_password_hash
from datetime import date, time
import random

# Initialize the Flask app
app = create_app()

# List of popular animal names for users
animal_names = [
    "ronaldinho", "garrincha", "abelha", "carlos", "rogerio", "mlkz1k4", "alvenaria", "albert_einstein", "meninoney", "hackerdobem"
]

# List of room names
room_names = ["Room 1", "Room 2", "Room 3"]

def create_admin_user():
    admin = User(username='admin', email='admin@example.com')
    admin.set_password('hackersdobem')  # Use a strong password here
    admin.is_admin = True
    db.session.add(admin)
    db.session.commit()

def create_random_users(count=8):
    for i in range(count):
        username = animal_names[i % len(animal_names)]  # Use animal names
        email = f"{username.lower()}@example.com"
        password = animal_names[i % len(animal_names)].lower()  # Password same as username for simplicity
        contact_phone = f"555-{random.randint(1000, 9999)}"
        user = User(username=username, email=email, contact_phone=contact_phone)
        user.set_password(password)
        db.session.add(user)
    db.session.commit()

def populate_rooms():
    # Check if rooms already exist
    existing_rooms = Room.query.filter(Room.name.in_(room_names)).all()
    existing_room_names = {room.name for room in existing_rooms}
    
    for name in room_names:
        if name not in existing_room_names:
            room = Room(name=name)
            db.session.add(room)
    db.session.commit()

def populate_reservations():
    users = User.query.all()
    rooms = Room.query.filter(Room.name.in_(room_names)).all()
    
    if not users or not rooms:
        print("No users or rooms found. Please ensure they are populated.")
        return
    
    # Create reservations
    for i in range(10):  # Create 10 reservations as an example
        user = random.choice(users)
        room = random.choice(rooms)
        reservation_date = date.today()
        reservation_time = time(random.randint(9, 17), random.choice([0, 15, 30, 45]))  # Random time within 9 AM to 5 PM
        
        # Check for existing reservation
        existing_reservation = Reservation.query.filter_by(
            user_id=user.id,
            room_id=room.id,
            date=reservation_date,
            time=reservation_time
        ).first()

        if existing_reservation:
            continue  # Skip if reservation already exists

        reservation = Reservation(
            user_id=user.id,
            room_id=room.id,
            date=reservation_date,
            time=reservation_time
        )
        db.session.add(reservation)
    db.session.commit()

def populate_database():
    with app.app_context():
        create_admin_user()
        create_random_users()
        populate_rooms()
        populate_reservations()
        print("Database populated successfully!")

if __name__ == "__main__":
    populate_database()
