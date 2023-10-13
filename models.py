from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# This file is used for formmating and creating the diffrent tables needed for the database
# Our website will use tables for users, barbers, appointments, services, reviews, 
# barbers services, and client details. 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.String)

class Barber_detail(db.Model):
    __tablename__ = 'barber_details'
    barber_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Float)


class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber_details.barber_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client_details.client_id'))
    time = db.Column(db.Time)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))

class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber_details.barber_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client_details.client_id'))
    stars = db.Column(db.Integer)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

class Client_detail(db.Model):
    __tablename__ = 'client_details'
    client_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    preferred_barber_id = db.Column(db.Integer, db.ForeignKey('barber_details.barber_id'))

class Barber_service(db.Model):
    __tablename__ = 'barber_services'
    barber_service_id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber_details.barber_id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    price = db.Column(db.Integer)
    duration = db.Column(db.Integer)