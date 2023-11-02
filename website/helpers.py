from .models import Barber_detail
from flask import abort, current_app
import os
import secrets
from werkzeug.utils import secure_filename

def get_barber_by_id(barber_id):
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

def save_picture(form_picture):
    """
    Save the uploaded picture to the designated upload folder.
    """
    # Create a random hex name for the picture to avoid filename conflicts
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(secure_filename(form_picture.filename))
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, 'static/photos/profile_pictures/', picture_filename)

    # Save the picture
    form_picture.save(picture_path)

    return picture_filename