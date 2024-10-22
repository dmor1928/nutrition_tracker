from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager  # type: ignore

# For importing food data into newly created database
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd


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

    from .models import User, Note, Foods, Recipe, RecipeIngredient, RDA

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # If user not logged in at entry, flask redirects to login page
    login_manager.init_app(app)  # Tells login manager whihc app is being used

    @login_manager.user_loader  # Tells flask how a user is loaded
    def load_user(id):
        return User.query.get(int(id))  # similar to the filter function. Filters for the primary key by default to check if it's equal to int(id)
    
    def toInteger(x):  # for view-recipe table page, turns floating amount into integer to look neater
         return int(x)
    
    app.jinja_env.globals.update(toInteger=toInteger)

    return app

def create_database(app):
    dir_path = path.dirname(path.realpath(__file__))
    instance_dir, _ = path.split(dir_path)
    instance_dir += "\\instance\\"

    if not path.exists(instance_dir + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database')

         # Importing csv data to models
        from .models import Foods, RDA, User, NutrientUnit
        engine = db.create_engine('sqlite:///instance/database.db', echo=False)
        Base = declarative_base()
        Base.metadata.create_all(engine)
        file_dir = 'database/clean-tables/'

        df = pd.read_csv(file_dir + 'complete_nutritional_data.csv')
        df.to_sql(con=engine, name=Foods.__tablename__, if_exists='replace', index=False)
        
        df = pd.read_csv(file_dir + 'RDA.csv')
        df.to_sql(con=engine, name=RDA.__tablename__, if_exists='replace', index=False)

        df = pd.read_csv(file_dir + 'nutrients_units.csv')
        df.to_sql(con=engine, name=NutrientUnit.__tablename__, if_exists='replace', index=False)

        print("Imported food and RDA data")

        import datetime
        from dateutil.relativedelta import relativedelta
        from werkzeug.security import generate_password_hash

        dob = datetime.datetime(2002, 8, 15)
        today = datetime.date.today()
        age = relativedelta(today, dob).years
        rda_id = 7

        sample_user = User(
            email='david@gmail.com', 
            password=generate_password_hash('password123', method='pbkdf2:sha256'), 
            firstName='David', 
            birthDate=dob,
            age=age,
            sex='male',
            isPregnant = False,
            isLactating = False,
            rda_id = rda_id)
        
        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()