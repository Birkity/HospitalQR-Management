from flask import render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from ..models.user import User
from ..models.patient import Patient

from flask import Blueprint  

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.find_by_email(email):
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, password=password, name=name)
        user_id = user.save_to_db()
        
        # Create associated patient record
        Patient.create_from_user(user)
        
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password', 'error')
            return render_template('login.html')
        
        user_data = User.find_by_email(email)
        if user_data:
            try:
                user = User.create_from_db(user_data)
                if user and user.check_password(password):
                    login_user(user, remember=True)
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('main.index'))
            except Exception as e:
                print(f"Error during login: {e}")
                flash('An error occurred during login', 'error')
                return render_template('login.html')
                
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        session.clear()  # Clear all session data
    except Exception as e:
        print(f"Error during logout: {e}")
    return redirect(url_for('main.index'))
