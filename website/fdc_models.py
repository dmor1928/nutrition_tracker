from . import db  # Importing the db created in __init__.py which is just the SQLAlchemy() object
from flask_login import UserMixin # type: ignore
from sqlalchemy.sql import func

# Database model for FDCFood
class FDCFood(db.Model):
    fdc_id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(128))
    food_category_id = db.Column(db.String(64))
    nutritions = db.relationship('FDCFoodNutrition')

class FDCFoodNutrition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('fdc_food.fdc_id'))
    nutrient_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    # All nutrients...

class FDCNutrients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    unit_name = db.Column(db.String(8))

class FDCFoodPortion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('fdc_food.fdc_id'))
    name = db.Column(db.String(32))
    mass = db.Column(db.Float)

class FDCFoodPreparationOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('fdc_food.fdc_id'))
    name = db.Column(db.String(64))

class FDCFoodPreparationFactors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('fdc_food.fdc_id'))
    name = db.Column(db.String(64))