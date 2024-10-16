from . import db  # Importing the db created in __init__.py which is just the SQLAlchemy() object
from flask_login import UserMixin # type: ignore
from sqlalchemy.sql import func

#Database model for notes
class Note(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Database model for users
class User(db.Model, UserMixin):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user (since users can have the same name etc)
    email = db.Column(db.String(150), unique=True)  # no two users can have the same email
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')

# Database model for recipe ingredients
class RecipeIngredient(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # The id uniquely identifying each instance of an ingredient in a recipe (various amounts etc.)
    amount = db.Column(db.Float)  # In grams
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))  # Links the instance of an ingredient to its recipe
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))

# Database model for recipes
class Recipe(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) 
    description = db.Column(db.String(1000))
    vegetarian = db.Column(db.Boolean)  # Dietary requirements
    vegan = db.Column(db.Boolean)
    pescatarian = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Which user created the recipe