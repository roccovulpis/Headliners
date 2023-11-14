from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .helpers import allowed_file, save_picture, set_availability, generate_time_slots
from .models import Barber_detail, User, Barber_availability, Barber_service
from werkzeug.utils import secure_filename
from datetime import time
from . import db
import os
from PIL import Image
from io import BytesIO
import base64


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
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        instagram_tag = request.form.get('instagram_tag')
        existing_user = User.query.filter_by(email=email).first()

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', 'danger')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', 'danger')

        # Check if the email is already taken and it's not the current user's email
        if existing_user and existing_user.user_id != current_user.user_id:
            flash('This email is already in use. Please use a different one.', 'danger')
            return render_template('edit_profile.html', barber=current_user, user=current_user)

        # Handle the cropped image
        cropped_data = request.form.get('cropped_image_data')  # This is a base64 encoded string
        
        if cropped_data:
            try:
                # Decode the base64 data
                base64_data = cropped_data.split(",")[1]
                decoded_image_data = base64.b64decode(base64_data)
                
                # Convert to an image (PIL Image)
                image = Image.open(BytesIO(decoded_image_data))
                
                # Use your utility function to save the picture
                filename = save_picture(image)
                
                # Update the user's picture_filename field
                current_user.barber_detail.picture_filename = filename
                db.session.commit()
            
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
                return redirect(request.url)

        # Update other details
        current_user.name = name
        current_user.email = email
        current_user.phone_number = phone_number
        current_user.barber_detail.instagram_tag = instagram_tag

        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('dashboard.home'))
    
    # If GET or any other method, render the edit-profile template
    return render_template('edit_profile.html', barber=current_user, user=current_user)

@dashboard.route('/edit-availability', methods=['GET', 'POST'])
@login_required
def edit_availability():
    if current_user.role != 'barber':
        flash('This feature is for barbers only!', 'danger')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        set_availability(current_user)
        redirect(url_for('dashboard.edit_availability'))
    time_slots = generate_time_slots(time(9,0), time(19,0), 30)
    return render_template("edit_availability.html", user=current_user, time_slots=time_slots, )


# service related
@dashboard.route('/your-services')
@login_required
def barber_services():
    return render_template("services.html", user=current_user, barber=current_user.barber_detail)


@dashboard.route('/add_service', methods=['GET', 'POST'])
@login_required
def add_service():
    barbers_only()
    if request.method == 'POST':
        price = request.form.get('price')
        if not price or not price.isnumeric():
            flash('Price was invalid. Try again', 'danger')
            return redirect(url_for('dashboard.barber_services'))
        
        name = request.form.get('service')
        desc = request.form.get('description')
        price = int(price)
        duration = int(request.form.get('duration'))

        service = Barber_service(
            name=name,
            desc=desc,
            price=price,
            duration=duration,
            barber_id=current_user.barber_detail.barber_id
        )

        db.session.add(service)
        db.session.commit()
        message = f"{name} added successfully!"
        flash(message, 'success')
        return redirect(url_for('dashboard.barber_services'))

    return render_template('add_service.html', user=current_user)


@dashboard.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Barber_service.query.get_or_404(service_id)

    if request.method == 'POST':

        price = request.form.get('price')
        if not price or not price.isnumeric():
            flash('Price was invalid. Try again', 'danger')
            return redirect(url_for('dashboard.barber_services'))

        service.name = request.form.get('service')
        service.desc = request.form.get('description')
        service.price = int(price)
        service.duration = int(request.form.get('duration'))

        db.session.commit()
        message = f"{service.name} updated successfully!"
        flash(message, 'success')
        return redirect(url_for('dashboard.barber_services'))

    return render_template('edit_service.html', service=service, user=current_user)


@dashboard.route('/delete_service/<int:service_id>', methods=['POST', 'GET'])
@login_required
def delete_service(service_id):
    service = Barber_service.query.get_or_404(service_id)
    if service:
        message = f"{service.name} deleted successfully!"
        db.session.delete(service)
        db.session.commit()
        flash(message, 'success')
    return redirect(url_for('dashboard.barber_services'))


@dashboard.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    return render_template("appointment.html", user=current_user)


@dashboard.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    return render_template("reviews.html", user=current_user)

@dashboard.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.role != 'client':
        flash('This feature is only available to clients.', 'danger')
        return redirect(url_for('views.home'))  # redirect non clients home

    if request.method == 'POST':
        # Extract data from the form
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        existing_user = User.query.filter_by(email=email).first()

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', 'danger')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', 'danger')

        # Check if the email is already taken and it's not the current user's email
        if existing_user and existing_user.user_id != current_user.user_id:
            flash('This email is already in use. Please use a different one.', 'danger')
            return render_template('settings.html', user=current_user)

        # Update details
        current_user.name = name
        current_user.email = email
        current_user.phone_number = phone_number
        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('dashboard.home')) 

    # If GET or any other method, render the edit-profile template
    return render_template('settings.html', user=current_user)


def barbers_only():
    if not current_user=='barber':
        return redirect(url_for('views.home'))