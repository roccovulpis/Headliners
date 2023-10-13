from flask import Flask, render_template
import sqlite3 
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()

DB_NAME = "db.sqlite3"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'peepeepoopoo'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Barber_detail, Appointment, Barber_service, Service, Client_detail, Review

    create_database(app)

    return app

#This goes through and creates the databse if it does not yet exist when you run the app
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')