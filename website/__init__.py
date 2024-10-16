from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager  # type: ignore


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)  # initialising flask
    app.config['SECRET_KEY'] = "QUEEN OF MELROSE"  # Encrypt cookies and session data with a secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Setting the URI for the database
    db.init_app(app)  #Linking the database to app

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Foods

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # If user not logged in at entry, flask redirects to login page
    login_manager.init_app(app)  # Tells login manager whihc app is being used

    @login_manager.user_loader  # Tells flask how a user is loaded
    def load_user(id):
        return User.query.get(int(id))  # similar to the filter function. Filters for the primary key by default to check if it;s equal to int(id)


    return app

def create_database(app):
    dir_path = path.dirname(path.realpath(__file__))
    instance_dir, _ = path.split(dir_path)
    instance_dir += "\\instance\\"

    if not path.exists(instance_dir + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database')