from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile')
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/barbers')
def barbers():
    return render_template("barbers.html", user=current_user)

@views.route('/appointment')
def appointment():
    return render_template("appointment.html", user=current_user)

@views.route('/availability')
def availability():
    return render_template("availability.html", user=current_user)

