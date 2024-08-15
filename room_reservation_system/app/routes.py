from flask import Blueprint, render_template, redirect, url_for, flash, request
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
