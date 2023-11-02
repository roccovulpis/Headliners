from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .helpers import allowed_file, save_picture
from .models import Barber_detail, User
from werkzeug.utils import secure_filename
from . import db
import os

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def home():
    if current_user.role == 'barber':
        return render_template('barber_dashboard.html',user=current_user)
    elif current_user.role == 'client':
        return render_template('client_dashboard.html',user=current_user)
    else:
        return redirect(url_for('views.home'))
    

@dashboard.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role != 'barber':
        flash('This feature is only available to barbers.', 'danger')
        return redirect(url_for('views.home'))  # redirect non barbers home

    if request.method == 'POST':
        # Extract data from the form
        name = request.form.get('name')
        phone = request.form.get('phone')
        profile_picture = request.files.get('profile_picture') if 'profile_picture' in request.files else None
        email = request.form.get('email')
        existing_user = User.query.filter_by(email=email).first()

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', 'danger')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', 'danger')

        # Check if the email is already taken and it's not the current user's email
        if existing_user and existing_user.user_id != current_user.user_id:
            flash('This email is already in use. Please use a different one.', 'danger')
            return render_template('edit_profile.html', barber=current_user, user=current_user)

        # If a new profile picture is uploaded
        if profile_picture and allowed_file(profile_picture.filename):
            filename = save_picture(profile_picture)
            current_user.barber_detail.picture_filename = filename

        # Update other details
        current_user.name = name
        current_user.email = email
        current_user.barber_detail.phone = phone

        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('dashboard.home'))  # or wherever you want to redirect after successful update

    # If GET or any other method, render the edit-profile template
    return render_template('edit_profile.html', barber=current_user, user=current_user)


@dashboard.route('/upload-picture', methods=['GET', 'POST'])
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