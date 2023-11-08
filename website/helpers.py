from flask import abort, current_app, request, flash, redirect, url_for
import os
import secrets
from datetime import datetime, timedelta

def get_barber_by_id(barber_id):
    from .models import Barber_detail

    barber_detail= Barber_detail.query.get_or_404(barber_id)
    user = barber_detail.user
    if user is None:
        abort(404)
    return user

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(image):
    """
    Save the provided image bytes to the designated upload folder.
    """
    # Create a random hex name for the picture to avoid filename conflicts
    random_hex = secrets.token_hex(8)
    picture_filename = random_hex + ".png"
    picture_path = os.path.join(current_app.root_path, 'static/photos/profile_pictures/', picture_filename)

    # Save the picture
    image.save(picture_path, 'PNG')

    return picture_filename

def set_availability(current_user):
    from . import db
    from .models import Barber_availability                               
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        start_time = request.form[f'{day}Start']
        end_time = request.form[f'{day}End']
        if not start_time and not end_time:
            start_time = None
            end_time = None
        else:
            if not start_time or not end_time:
                flash('One of your starts or ends did not have an accompanying time.', 'danger')
                return redirect(url_for('dashboard.edit_availability'))
            
            start_time = datetime.strptime(start_time, '%I:%M %p').time()
            end_time = datetime.strptime(end_time, '%I:%M %p').time()
            
        current_availability=Barber_availability.query.filter_by(barber_id=current_user.barber_detail.barber_id,
                                                                    week_day=day).first()
        if current_availability:
            current_availability.start_time=start_time
            current_availability.end_time=end_time
        else:
            new_availability = Barber_availability(barber_id=current_user.barber_detail.barber_id,
                                                    week_day=day,
                                                    start_time=start_time,
                                                    end_time=end_time)
            db.session.add(new_availability)
            
    db.session.commit()
    flash('Your availability has been updated', 'success')


def generate_time_slots(start_time, end_time, interval_minutes):
    times = []
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time.strftime('%I:%M %p'))
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=interval_minutes)).time()
    return times