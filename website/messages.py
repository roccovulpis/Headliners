from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Message
import os

messages = Blueprint('messages', __name__)

@messages.route('/')
@login_required
def home():
    messages = Message.query.filter_by(receiver_id=current_user.user_id).all()
    return render_template('inbox.html', messages=messages, user=current_user)
