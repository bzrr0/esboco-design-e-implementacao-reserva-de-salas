from flask_wtf import FlaskForm
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
