from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .helpers import generate_available_time_slots
from .models import Barber_detail, Barber_service, Barber_availability, Appointment
from . import db
from datetime import datetime, time

book = Blueprint('book', __name__)


@book.route('/<int:barber_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(barber_id):
    barber = Barber_detail.query.get_or_404(barber_id)
    services = barber.services

    selected_date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    if request.method == 'POST':
        client_only()
        service_id = request.form.get('service')
        time_slot = request.form.get('timeSlot')

        print("serviceid", service_id)

        appointment_datetime = datetime.combine(selected_date, datetime.strptime(time_slot, "%I:%M %p").time())

        # Create a booking record and update availability
        create_appointment(barber_id, service_id, appointment_datetime)
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('dashboard.home')) 

    # Get available time slots based on the barber's availability and booked appointments for the selected date
    available_time_slots = generate_available_time_slots(barber_id, selected_date)

    return render_template('book_appointment.html',user=current_user, barber=barber, services=services, available_time_slots=available_time_slots, selected_date=selected_date)


def create_appointment(barber_id, service_id, appointment_datetime):
    appointment = Appointment(
        barber_id=barber_id,
        service_id=service_id,
        datetime=appointment_datetime,
        client_id=current_user.user_id
    )

    try:
        db.session.add(appointment)
        db.session.commit()
        return True 
    except Exception as e:
        print("Error creating appointment: ", e)
        db.session.rollback()
        return False
    

@book.route('/delete-appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if (current_user.role == 'barber' and current_user.barber_detail.barber_id != appointment.barber_id) or (current_user.role == 'client' and current_user.user_id != appointment.client_id):
        flash('This is not your appointment! How did you even get here?', 'danger')
        return redirect(url_for('views.home'))
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the appointment.', 'danger')
        print(e) 

    return redirect(url_for('dashboard.home'))


def client_only():
    if not current_user.role == 'client':
            flash ('This is for clients only! Scram!', 'danger')
            return redirect(url_for('views.home'))