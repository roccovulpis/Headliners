from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# This file is used for formmating and creating the diffrent tables needed for the database
# Our website will use tables for users, barbers, appointments, services, reviews, 
# barbers services, and client details. 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    role = db.Column(db.String)

    barber_detail = db.relationship("Barber_detail", backref="user", uselist=False)

    def get_id(self):
        return str(self.user_id)

class Barber_detail(db.Model):
    __tablename__ = 'barber_details'
    barber_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Float)
    picture_filename = db.Column(db.String)
    instagram_tag = db.Column(db.String)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber_details.barber_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client_details.client_id'))
    time = db.Column(db.Time)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))

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
    name = db.Column(db.String)
    desc = db.Column(db.String)
    price = db.Column(db.Integer)
    duration = db.Column(db.Integer)

class Barber_availability(db.Model):
    __tablename__ = "barber_availability"
    barber_availability_id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber_details.barber_id'))
    week_day = db.Column(db.String)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)