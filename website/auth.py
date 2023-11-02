from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Barber_detail
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# This file is used for authenticating users who try to log in, or making new account

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract data from the form
        email = request.form.get('email')
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

# This section is for creating a new user.
# First it requests a user's email, name, and password.
# Then it goes through and checks to make sure all of the inputs are valid.
# Finally, if they all are within parameters, it will make a new user with their entered information.

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')

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
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', 'success')
            # Check if role is 'barber' and add to Barber_detail table
            if role =='barber':
                new_barber = Barber_detail(user_id=new_user.user_id)
                db.session.add(new_barber)
                db.session.commit()
            return redirect(url_for('views.home'))


    return render_template("sign_up.html",user=current_user)
