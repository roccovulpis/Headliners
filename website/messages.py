from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from . import db
from .models import Message, User, Barber_detail, Appointment
import os
from datetime import datetime

messages = Blueprint('messages', __name__)

@messages.route('/')
@login_required
def home():
    # Create subqueries for sent and received messages
    sent_messages = db.session.query(Message.receiver_id.label("user_id")).filter(Message.sender_id == current_user.user_id).subquery()
    received_messages = db.session.query(Message.sender_id.label("user_id")).filter(Message.receiver_id == current_user.user_id).subquery()

    # Union the two subqueries and find unique user IDs
    conversation_partners_ids = db.session.query(sent_messages.c.user_id).union(db.session.query(received_messages.c.user_id)).distinct().all()

    # Fetch user details for each conversation partner
    conversation_partners = User.query.filter(User.user_id.in_([user_id for user_id, in conversation_partners_ids])).all()

    # Fetch the latest message for each conversation partner
    latest_messages = []
    for partner_id in conversation_partners_ids:
        latest_message = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.user_id, Message.receiver_id == partner_id[0]),
                db.and_(Message.receiver_id == current_user.user_id, Message.sender_id == partner_id[0])
            )
        ).order_by(Message.timestamp.desc()).first()
        latest_messages.append((User.query.get(partner_id[0]), latest_message))

    latest_messages_with_unread_flag = []
    for partner, latest_message in latest_messages:
        is_unread = latest_message and not latest_message.read_status and latest_message.receiver_id == current_user.user_id
        latest_messages_with_unread_flag.append((partner, latest_message, is_unread))

    return render_template('conversations.html', conversation_partners=conversation_partners, latest_messages=latest_messages_with_unread_flag, user=current_user)

@messages.route('/send_message', methods=['GET', 'POST'])
def send_message():
    reply_to = request.args.get('reply_to', type=int)
    preselected_recipient = None

    if reply_to:
        preselected_recipient = User.query.get(reply_to)

    if request.method == 'POST':
        all_past_clients = 'all_past_clients' in request.form
        all_clients = 'all_clients' in request.form
        receiver_ids = request.form.getlist('receivers')
        content = request.form.get('content')

        if not content:
            flash('Message cannot be empty!', 'error')
            return redirect(url_for('messages.send_message'))

        receiver_ids_set = set()
        
        if current_user.role == 'client':
            barber_id = request.form.get('receiver')  # Assuming 'receiver' is the name of the select field in your form
            if barber_id:
                receiver_ids_set.add(int(barber_id))    

        # Convert all client IDs from the database queries to integers and adding them to sets to ensure uniqueness (i.e. no duplicate messages)
        if all_clients:
            all_client_ids = db.session.query(User.user_id).filter(User.role == 'client').all()
            for id_tuple in all_client_ids:
                receiver_ids_set.add(int(id_tuple[0]))

        if all_past_clients:
            past_client_ids = db.session.query(Appointment.client_id).filter(
                Appointment.barber_id == current_user.barber_detail.barber_id
            ).distinct().all()
            for id_tuple in past_client_ids:
                receiver_ids_set.add(int(id_tuple[0]))

        # Convert specific client IDs from the form to integers and add them to the set
        specific_client_ids = request.form.getlist('receivers')
        for client_id in specific_client_ids:
            receiver_ids_set.add(int(client_id))

        # Now use receiver_ids_set for sending messages
        for receiver_id in receiver_ids_set:
            new_message = Message(sender_id=current_user.user_id, receiver_id=receiver_id, content=content)
            
            from .mail import send_email_notification    
            # Fetch recipient's email and name
            recipient = User.query.get(receiver_id)
            if recipient and recipient.email:
                send_email_notification(
                    recipient_email=recipient.email,
                    recipient_name=recipient.name,
                    sender_name=current_user.name,
                    message_content=content,
                    role=current_user.role
                )
                
            db.session.add(new_message)
            print("read?", new_message.read_status)
                        
        db.session.commit()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages.home'))

    if current_user.role == 'barber':
        client_ids = db.session.query(Appointment.client_id).filter(Appointment.barber_id == current_user.barber_detail.barber_id).distinct().all()
        clients = User.query.filter(User.user_id.in_([id[0] for id in client_ids])).all()
        return render_template('send_message.html', recipients=clients, preselected_recipient=preselected_recipient, user=current_user)
    else:
        barbers = Barber_detail.query.all()
        return render_template('send_message.html', recipients=barbers, preselected_recipient=preselected_recipient, user=current_user)

        
@messages.route('/conversation/<int:partner_id>')
@login_required
def conversation_detail(partner_id):
    # Fetch messages between the current user and the partner
    messages = Message.query.filter(
        (Message.sender_id == current_user.user_id) & (Message.receiver_id == partner_id) |
        (Message.sender_id == partner_id) & (Message.receiver_id == current_user.user_id)
    ).order_by(Message.timestamp.desc()).all()

    partner = User.query.get_or_404(partner_id)

    # Mark unread messages as read
    for message in messages:
        if not message.read_status and message.receiver_id == current_user.user_id:
            message.read_status = True
            db.session.commit()

    return render_template('conversation_detail.html', messages=messages, partner=partner, user=current_user)

