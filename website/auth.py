from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Barber_detail
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# This file is used for authenticating users.

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract data from the form
        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again', 'danger')
        else:
            flash('Email is not registered', 'danger')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

# Creats a new user.
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        # Extracts data from the form.
        email = request.form.get('email').lower()
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')

        # Validates inputs.

        # Checks if the email is already in use.
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email is already in use.', 'danger')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', 'danger')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', 'danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', 'danger')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters.', 'danger')
        else:
            # Creates new user and commits it to the database.
            new_user = User(email=email, name=name, phone_number=phone_number, password=generate_password_hash(password1, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', 'success')
            # Adds user to barber_details table if they are a barber
            if role =='barber':
                default_instagram_tag = 'headliners.eht'
                new_barber = Barber_detail(user_id=new_user.user_id, instagram_tag=default_instagram_tag)
                db.session.add(new_barber)
                db.session.commit()
            return redirect(url_for('views.home'))


    return render_template("sign_up.html",user=current_user)
