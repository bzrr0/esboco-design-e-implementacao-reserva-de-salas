import os

# Define the project folder path
project_folder = 'project_folder'
app_folder = os.path.join(project_folder, 'app')
static_folder = os.path.join(app_folder, 'static')
templates_folder = os.path.join(app_folder, 'templates')

# Create directories
os.makedirs(static_folder, exist_ok=True)
os.makedirs(os.path.join(static_folder, 'css'), exist_ok=True)
os.makedirs(os.path.join(static_folder, 'js'), exist_ok=True)
os.makedirs(templates_folder, exist_ok=True)

# Define file content with comments
files = {
    'config.py': '''import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Read from .env file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
''',

    'populate.py': '''# populate_database.py
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
''',

    'resetdb.py': '''# reset_database.py
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
''',

    'run.py': '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''',

    'app/__init__.py': '''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
''',

    'app/.env': '''SECRET_KEY=hackersdobem
DATABASE_URL=sqlite:///site.db''',

    'app/forms.py': '''from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    title = SelectField('Title', choices=[('professor', 'Professor'), ('student', 'Student'), ('medic', 'Medic'), ('maintenance', 'Maintenance')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ReservationForm(FlaskForm):
    room = SelectField('Room', choices=[('Room 1', 'Room 1'), ('Room 2', 'Room 2'), ('Room 3', 'Room 3')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Reserve')
''',

    'app/models.py': '''from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    contact_phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    reservations = db.relationship('Reservation', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    reservations = db.relationship('Reservation', back_populates='room')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    canceled = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    user = db.relationship('User', back_populates='reservations')
    room = db.relationship('Room', back_populates='reservations')
''',

    'app/routes.py': '''from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Reservation, Room
from app.forms import LoginForm, ResetPasswordForm, ReservationForm, RegistrationForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('main.admin_panel'))
        else:
            return redirect(url_for('main.user_reservations'))
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
    
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    form = ReservationForm()
    if form.validate_on_submit():
        room = Room.query.filter_by(name=form.room.data).first()
        
        if room is None:
            flash('Selected room does not exist.', 'danger')
            return redirect(url_for('main.reserve'))

        existing_reservation = Reservation.query.filter_by(
            room_id=room.id,
            date=form.date.data,
            time=form.time.data,
            canceled=False
        ).first()
        
        if existing_reservation:
            flash('This room is already reserved for the selected date and time.', 'danger')
        else:
            reservation = Reservation(
                user_id=current_user.id,
                room_id=room.id,
                date=form.date.data,
                time=form.time.data
            )
            db.session.add(reservation)
            try:
                db.session.commit()
                flash('Room reserved successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while saving the reservation.', 'danger')
            return redirect(url_for('main.index'))
    return render_template('reserve.html', form=form)

@bp.route('/reservations')
@login_required
def user_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id, canceled=False).all()
    return render_template('user_reservations.html', reservations=reservations)

@bp.route('/admin_panel')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    
    reservations = db.session.query(Reservation, User, Room).join(User).join(Room).filter(Reservation.canceled == False).all()
    return render_template('admin.html', reservations=reservations)

@bp.route('/admin/cancel_reservation', methods=['POST'])
@login_required
def cancel_reservation():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    
    reservation_id = request.form.get('reservation_id')
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        reservation.canceled = True
        db.session.commit()
        flash('Reservation canceled successfully.', 'success')
    else:
        flash('Reservation not found.', 'danger')
    
    return redirect(url_for('main.admin_panel'))

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Handle password reset logic here
            flash('Password reset link sent to your email.', 'info')
            return redirect(url_for('main.login'))
        else:
            flash('Email not found.', 'danger')
    return render_template('reset_password.html', form=form)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = RegistrationForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact_phone = form.phone.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)

@bp.route('/explore')
def explore():
    return render_template('explore.html')
''',

    'app/static/css/styles.css': '''/* Base Styles */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    background-color: #fff;
    color: #000;
}

body.dark-mode {
    background-color: #000;
    color: #000000;
}

/* Header */
header {
    background-color: #f0f0f0;
    padding: 10px;
    text-align: center;
    position: relative;
}

header.dark-mode {
    background-color: #333;
}

header nav {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
}

header a {
    color: #000;
    text-decoration: none;
    font-weight: bold;
    font-size: 16px;
    transition: color 0.3s ease;
}

header a:hover {
    color: #007bff;
}

/* Dark Mode Toggle Button */
.dark-mode-toggle {
    background-color: #000000;
    color: #fff;
    border: none;
    padding: 5px 15px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
    position: absolute;
    top: -8px;
    left: 3px;
    z-index: 10;
    /* Align with header elements */
    height: 35px; /* Adjust height to match header items */
    line-height: 25px; /* Adjust line height to center text vertically */
}

.dark-mode-toggle:hover {
    background-color: #0056b3;
}

/* Main Content */
main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
}

/* Container */
.container, .explore-container {
    width: 90%;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    /* Ensure container background color adapts to dark mode */
    border: 1px solid #ddd;
}

.container {
    background-color: #ffffff;
}

.container.dark-mode {
    background-color: #1a1a1a;
    border-color: #444;
    color: #fff;
}

.explore-container {
    background-color: #ffffff;
}

.explore-container.dark-mode {
    background-color: #1a1a1a;
    border-color: #444;
    color: #fff;
}

.explore-title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

.explore-content {
    font-size: 18px;
    line-height: 1.6;
}

/* Buttons */
button, .btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
    display: inline-block;
    margin-top: 10px;
}

button:hover, .btn:hover {
    background-color: #0056b3;
}

/* Links */
a {
    color: #007bff;
    text-decoration: none;
    font-size: 16px;
    transition: color 0.3s ease;
}

a:hover {
    color: #0056b3;
}

/* Forms */
form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

input[type="text"], input[type="password"], input[type="email"], input[type="date"], input[type="time"], select {
    width: 100%;
    max-width: 300px;
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
}

input.dark-mode, select.dark-mode {
    background-color: #333;
    color: #fff;
    border-color: #444;
}

/* Input adjustments for login page */
input[type="text"].login, input[type="password"].login {
    max-width: 200px; /* Shorter width for login inputs */
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    text-align: center; /* Center content in table */
}

table th, table td {
    border: 1px solid #ddd;
    padding: 10px;
}

table th {
    background-color: #f4f4f4;
    font-weight: bold;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container, .explore-container {
        padding: 15px;
    }

    button, .btn {
        width: 100%;
        padding: 12px;
        font-size: 18px;
    }
}

@media (max-width: 480px) {
    body {
        font-size: 14px;
    }

    header {
        font-size: 18px;
    }

    button, .btn {
        padding: 15px;
        font-size: 20px;
    }
}
''',

    'app/static/js/script.js': '''function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');

    // Save the user's preference in local storage
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

// Apply saved theme on page load
window.onload = function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.classList.add(savedTheme === 'dark' ? 'dark-mode' : 'light-mode');
    }

    // Display any existing messages (errors, reservations, etc.)
    displayMessages();
}

// Function to collect and display messages (e.g., error messages or reservation confirmation)
function displayMessages() {
    const errorMessage = document.querySelector('.error-message');
    if (errorMessage) {
        alert(errorMessage.textContent); // Show an alert with the error message
    }

    const reservationMessage = document.querySelector('.reservation-message');
    if (reservationMessage) {
        alert(reservationMessage.textContent); // Show an alert with the reservation message
    }
}
''',

    'app/templates/admin.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.logout') }}">Logout</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="container">
        <h2>Admin Panel</h2>
        
        <!-- Reservation List -->
        <h3>Reservation List</h3>
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Room</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for reservation, user, room in reservations %}
                <tr>
                    <td>{{ user.username }}</td>
                    <td>{{ reservation.date.strftime('%Y-%m-%d') }}</td>
                    <td>{{ reservation.time.strftime('%H:%M') }}</td>
                    <td>{{ room.name }}</td>
                    <td>
                        <form method="POST" action="{{ url_for('main.cancel_reservation') }}">
                            <input type="hidden" name="reservation_id" value="{{ reservation.id }}">
                            <button type="submit" class="btn btn-danger">Cancel</button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5">No reservations found</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/cancel.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cancel a Reservation</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <h2>Cancel a Reservation</h2>
        <form method="POST" action="{{ url_for('main.cancel_reservation') }}">
            <label for="reservation">Select Reservation:</label>
            <select id="reservation" name="reservation_id" required>
                {% for reservation in reservations %}
                    <option value="{{ reservation.id }}">{{ reservation.room.name }} - {{ reservation.date }} at {{ reservation.time }}</option>
                {% endfor %}
            </select>
            
            <button type="submit" class="btn btn-danger">Cancel Reservation</button>
        </form>
    </div>
</body>
</html>
''',

    'app/templates/edit_profile.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <h2>User Profile</h2>
        <p><strong>Username
''',

    'app/templates/explore.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explore</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.login') }}">Login</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="explore-container">
        <h1 class="explore-title">Welcome to Our Institution</h1>
        <div class="explore-content">
            <p>Our institution offers a range of rooms that can be reserved for various events and meetings. You can easily check availability and make reservations using our platform.</p>
            <p>To make a reservation, navigate to the reservation page where you can select the room, date, and time that fits your needs. Our system ensures that the rooms are available and confirms your booking immediately.</p>
            <p>Explore more features and get to know how our reservation system can help streamline your event planning.</p>
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/index.html': '''{% extends "main.base.html" %}

{% block title %}Welcome{% endblock %}

{% block content %}
<div class="container">
    <h1>Welcome to the Room Reservation System</h1>
    <a href="{{ url_for('main.explore') }}" class="btn">Explore</a>
</div>
{% endblock %}
''',

    'app/templates/list_reservations.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Reservations</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.logout') }}">Logout</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="container">
        <h2>My Reservations</h2>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Room</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for reservation in reservations %}
                <tr>
                    <td>{{ reservation.date.strftime('%Y-%m-%d') }}</td>
                    <td>{{ reservation.time.strftime('%H:%M') }}</td>
                    <td>{{ reservation.room.name }}</td>
                    <td>{{ reservation.status }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4">No reservations found</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/login.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <style>
        .error-message {
            color: #721c24;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.reset_password') }}">Forgot Password?</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="container">
        <h2>Login</h2>

        {% if error_message %}
            <div class="error-message">{{ error_message }}</div>
        {% endif %}

        <form method="POST" action="{{ url_for('main.login') }}">
            {{ form.hidden_tag() }}
            <div>
                <label for="username">Username:</label>
                {{ form.username(class="form-control", id="username") }}
                {% if form.username.errors %}
                    <div class="error">{{ form.username.errors[0] }}</div>
                {% endif %}
            </div>
            <div>
                <label for="password">Password:</label>
                {{ form.password(class="form-control", id="password") }}
                {% if form.password.errors %}
                    <div class="error">{{ form.password.errors[0] }}</div>
                {% endif %}
            </div>
            <div>
                {{ form.remember_me() }}
                <label for="remember_me">Remember Me</label>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/main.base.html': '''<!DOCTYPE html>
<html lang="en" class="{{ 'dark-mode' if dark_mode else '' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Room Reservation System{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            {% if current_user.is_authenticated %}
                <a href="{{ url_for('main.reserve') }}">Reserve a Room</a>
                {% if current_user.is_admin %}
                    <a href="{{ url_for('main.admin_panel') }}">Admin Panel</a>
                {% endif %}
                <a href="{{ url_for('main.logout') }}">Logout</a>
            {% else %}
                <a href="{{ url_for('main.login') }}">Login</a>
            {% endif %}
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/profile.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <h2>User Profile</h2>
        <p><strong>Username
''',

    'app/templates/reserve.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reserve a Room</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.logout') }}">Logout</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="container">
        <h2>Reserve a Room</h2>

        {% if form %}
            <form method="POST" action="{{ url_for('main.reserve') }}">
                {{ form.hidden_tag() }}
                <div class="form-group">
                    {{ form.room.label }}
                    {{ form.room(class="form-control") }}
                </div>
                <div class="form-group">
                    {{ form.date.label }}
                    {{ form.date(class="form-control") }}
                </div>
                <div class="form-group">
                    {{ form.time.label }}
                    {{ form.time(class="form-control") }}
                </div>
                <div class="form-group">
                    {{ form.submit(class="btn btn-primary") }}
                </div>
            </form>
        {% endif %}

        {% if reservations %}
            <h2>Your Reservations</h2>
            <ul>
            {% for reservation in reservations %}
                <li>Room: {{ reservation.room.name }} | Date: {{ reservation.date }} | Time: {{ reservation.time }}</li>
            {% endfor %}
            </ul>
        {% elif not form %}
            <p>You have no reservations.</p>
        {% endif %}
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/reset_password.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Password</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.login') }}">Login</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="container">
        <h2>Reset Password</h2>
        <form method="POST" action="{{ url_for('main.reset_password') }}">
            {{ form.hidden_tag() }}
            <div>
                <label for="email">Email:</label>
                {{ form.email(class="form-control", id="email") }}
                {% if form.email.errors %}
                    <div class="error">{{ form.email.errors[0] }}</div>
                {% endif %}
            </div>
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </form>
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''',

    'app/templates/user_reservations.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Reservations</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('main.index') }}">Home</a>
            <a href="{{ url_for('main.logout') }}">Logout</a>
            <button class="dark-mode-toggle" onclick="toggleDarkMode()">Toggle Dark Mode</button>
        </nav>
    </header>
    <div class="container">
        <h2>Your Reservations</h2>

        {% if reservations %}
            <ul>
            {% for reservation in reservations %}
                <li>Room: {{ reservation.room.name }} | Date: {{ reservation.date }} | Time: {{ reservation.time }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>You have no reservations.</p>
        {% endif %}
    </div>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
'''
}

# Create and write files
for filename, content in files.items():
    file_path = os.path.join(project_folder, filename)
    with open(file_path, 'w') as file:
        file.write(content)
        print(f'Created {file_path}')
