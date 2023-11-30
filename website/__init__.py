from flask import Flask
import sqlite3 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from . import helpers

db = SQLAlchemy()

DB_NAME = "db.sqlite3"

def create_app():
    app = Flask(__name__)

    # Profile picture upload handling
    UPLOAD_FOLDER = 'static/photos/profile_pictures/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config['SECRET_KEY'] = 'testkey'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .dashboard import dashboard
    from .book import book
    from .messages import messages
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(book, url_prefix='/book')
    app.register_blueprint(messages, url_prefix='/inbox')

    from .models import User, Barber_detail, Appointment, Barber_service, Client_detail, Review, Barber_availability

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Creates any new database elements
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')