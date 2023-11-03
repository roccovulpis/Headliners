from flask import abort, current_app
import os
import secrets
from werkzeug.utils import secure_filename
from PIL import Image

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