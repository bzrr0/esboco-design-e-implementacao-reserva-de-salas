# reset_database.py
from app import create_app, db

app = create_app()

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Recreate all tables
        db.create_all()
        print("Database reset successfully!")

if __name__ == "__main__":
    reset_database()
