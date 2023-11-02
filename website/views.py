from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .helpers import get_barber_by_id, allowed_file, save_picture
from .models import Barber_detail
from werkzeug.utils import secure_filename
from . import db
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile/<int:barber_id>')
def profile(barber_id):
    barber = get_barber_by_id(barber_id)

    # Check if the barber's picture is set. if not, render a default.
    if not barber.barber_detail.picture_filename:
        barber.barber_detail.picture_filename = 'default.jpg'

    return render_template("profile.html", barber=barber, user=current_user)

@views.route('/upload-picture', methods=['GET', 'POST'])
def upload_picture():
    # Check if the user is a barber
    if current_user.role != 'barber':
        flash('This feature is for barbers only!', 'danger')
        return redirect(url_for('views.home'))
    
    # Handle form submission
    if request.method == 'POST':
        # Check if the request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser might submit an empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        # If the file is allowed
        if file and allowed_file(file.filename):
            # Use the utility function to save the picture
            filename = save_picture(file)
            
            # Update the user's picture_filename field
            current_user.barber_detail.picture_filename = filename
            db.session.commit()

            flash('Your profile picture has been updated!', 'success')
            return redirect(url_for('views.profile', barber_id=current_user.barber_detail.barber_id))
        
        else:
            flash('Invalid file type', 'danger')
            return redirect(request.url)

    # If it's a GET request or any other case, render the upload form.
    return render_template('upload_picture.html', user=current_user)

    

@views.route('/barbers')
def barbers():
    barbers = Barber_detail.query.all()
    print(barbers)
    return render_template("barber_list.html", user=current_user, barbers=barbers)

@views.route('/appointment', methods=['POST'])
def appointment():
    # if request.method == 'POST':

    return render_template("appointment.html", user=current_user)

@views.route('/availability', methods=['GET', 'POST'])
def availability():
    return render_template("availability.html", user=current_user)

@views.route('/book-an-appointment')
def book_an_appointment():
    return "Book an Appointment"

