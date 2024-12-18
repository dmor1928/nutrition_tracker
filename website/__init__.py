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

    from .models import User, Note, Recipe, RecipeIngredient, RDAProfile, RDAValues, UserPersonalRDA#, Foods
   #  from .fdc_models import FDCFood, FDCFoodNutrition, FDCFoodPortion#, FDCFoodPreparationOptions, FDCFoodPreparationFactors

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

        engine = db.create_engine('sqlite:///instance/database.db', echo=False)
        Base = declarative_base()
        Base.metadata.create_all(engine)

        with app.app_context():
            db.create_all()
        
        print('Created New Database')
        # Importing csv data to models
        fdc_file_dir = 'fdc-database/fdc-reduced/'
        addFDC(engine, fdc_file_dir)

        rda_profiles_dir = 'database/clean-tables/rda-profiles/'
        addRDAProfiles(engine, rda_profiles_dir)

        rda_values_dir = 'database/clean-tables/rda-values/'
        addRDAValues(engine, rda_values_dir)

        # Adding sample user
        from .models import User
        import datetime
        from dateutil.relativedelta import relativedelta
        from werkzeug.security import generate_password_hash

        birthDate = datetime.datetime(2002, 8, 15)
        today = datetime.date.today()
        age = relativedelta(today, birthDate).years
        rda_id = 11

        sample_user = User(
            email='david@gmail.com', 
            password=generate_password_hash('password123', method='pbkdf2:sha256'), 
            firstName='David', 

            birthDate=birthDate,
            age=age,
            sex='male',
            weight_kg=63,
            isPregnant = False,
            isLactating = False,
            # RDADefault_id = rda_id,
            rda_profile_id = rda_id,
            isCustomRDA = False)

        with app.app_context():
            db.session.add(sample_user)
            db.session.commit()
    
    # cofid_file_dir = 'database/clean-tables/'
    # addCoFID(engine, cofid_file_dir)
    # addRDADefaults(engine, cofid_file_dir) # Updates RDADefault based on RDA_defaults.csv table every launch
        
        

def addCoFID(engine, cofid_file_dir):
    from .models import Foods, NutrientUnit

    df = pd.read_csv(cofid_file_dir + 'complete_nutritional_data.csv')
    df.to_sql(con=engine, name=Foods.__tablename__, if_exists='replace', index=False)
    
    df = pd.read_csv(cofid_file_dir + 'nutrients_units.csv')
    df.to_sql(con=engine, name=NutrientUnit.__tablename__, if_exists='replace', index=False)

    print("Imported CoFID food data")

# def addRDADefaults(engine, rda_file_dir):
#     from .models import RDADefault
#     df = pd.read_csv(rda_file_dir + 'RDA_defaults.csv')
#     df.to_sql(con=engine, name=RDADefault.__tablename__, if_exists='replace', index=False)
#     print("Imported default RDA data")

def addFDC(engine, FDC_file_dir):
    from .fdc_models import FDCFood, FDCFoodNutrition, FDCNutrients#, FDCFoodPortion, FDCFoodPreparationOptions, FDCFoodPreparationFactors

    # df = pd.read_csv(FDC_file_dir + 'food.csv')
    df = pd.read_csv(FDC_file_dir + 'sr_legacy_food.csv')
    df.to_sql(con=engine, name=FDCFood.__tablename__, if_exists='replace', index=False)
    
    # df = pd.read_csv(FDC_file_dir + 'food_nutrient.csv')
    df = pd.read_csv(FDC_file_dir + 'sr_legacy_food_nutrient.csv')
    df.to_sql(con=engine, name=FDCFoodNutrition.__tablename__, if_exists='replace', index=False)

    df = pd.read_csv(FDC_file_dir + 'nutrient.csv')
    df.to_sql(con=engine, name=FDCNutrients.__tablename__, if_exists='replace', index=False)
    
    # df = pd.read_csv(FDC_file_dir + 'food_portion.csv')
    # df.to_sql(con=engine, name=FDCFoodPortion.__tablename__, if_exists='replace', index=False)

    # df = pd.read_csv(FDC_file_dir + '')
    # df.to_sql(con=engine, name=FDCFoodPreparationFactors.__tablename__, if_exists='replace', index=False)

    print("Imported FDC food, nutrients and portion data")

def addRDAProfiles(engine, rda_files_dir):
    from .models import RDAProfile
    df = pd.read_csv(rda_files_dir + 'rda_profiles.csv')
    df.to_sql(con=engine, name=RDAProfile.__tablename__, if_exists='replace', index=False)
    print("Imported RDAProfile")

def addRDAValues(engine, rda_files_dir):
    from .models import RDAValues
    df = pd.read_csv(rda_files_dir + 'rda_values.csv')
    df.to_sql(con=engine, name=RDAValues.__tablename__,  if_exists='replace', index=False)
    print("Imported RDAValues")
