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
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))  # Links the instance of an ingredient to its recipe

# Database model for recipes containing descriptive information for recipe, and the user who created it
# Recipe --> RecipeIngredient is one-to-many
class Recipe(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) 
    description = db.Column(db.String(1000))
    vegetarian = db.Column(db.Boolean)  # Dietary requirements
    vegan = db.Column(db.Boolean)
    pescatarian = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Which user created the recipe

# Database model for food nutritional information (same as in add-food-to-database.py)
class Foods(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    energy = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrate = db.Column(db.Float)
    aoac = db.Column(db.Float)
    satd = db.Column(db.Float)
    n_6 = db.Column(db.Float)
    n_3 = db.Column(db.Float)
    mono = db.Column(db.Float)
    poly = db.Column(db.Float)
    trans = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    sodium = db.Column(db.Float)
    potassium = db.Column(db.Float)
    calcium = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    iron = db.Column(db.Float)
    copper = db.Column(db.Float)
    zinc = db.Column(db.Float)
    chloride = db.Column(db.Float)
    manganese = db.Column(db.Float)
    selenium = db.Column(db.Float)
    iodine = db.Column(db.Float)
    retinol = db.Column(db.Float)
    carotene = db.Column(db.Float)
    retinol_equivalent = db.Column(db.Float)
    d = db.Column(db.Float)
    e = db.Column(db.Float)
    k1 = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    niacin = db.Column(db.Float)
    tryptophan_60 = db.Column(db.Float)
    niacin_equivalent = db.Column(db.Float)
    b6 = db.Column(db.Float)
    b12 = db.Column(db.Float)
    folate = db.Column(db.Float)
    pantothenate = db.Column(db.Float)
    biotin = db.Column(db.Float)
    c = db.Column(db.Float)
    alpha_carotene = db.Column(db.Float)
    beta_carotene = db.Column(db.Float)
    lutein = db.Column(db.Float)
    lycopene = db.Column(db.Float)

    def __repr__(self):
        return '''<Foods(id='{0}', name='{1}', energy='{2}', protein='{3}', 
        fat='{4}', carbohydrate='{5}', aoac='{6}', satd='{7}', n_6='{8}', 
        n_3='{9}', mono='{10}', poly='{11}', trans='{12}', cholesterol='{13}', 
        sodium='{14}', potassium='{15}', calcium='{16}', magnesium='{17}', 
        phosphorus='{18}', iron='{19}', copper='{20}', zinc='{21}', chloride='{22}', 
        manganese='{23}', selenium='{24}', iodine='{25}', retinol='{26}', 
        carotene='{27}', retinol_equivalent='{28}', d='{29}', e='{30}', k1='{31}', 
        thiamin='{32}', riboflavin='{33}', niacin='{34}', tryptophan_60='{35}', 
        niacin_equivalent='{36}', b6='{37}', b12='{38}', folate='{39}', 
        pantothenate='{40}', biotin='{41}', c='{42}', alpha_carotene='{43}', 
        beta_carotene='{44}', lutein='{45}', lycopene='{46}')>'''.format(
            self.id, self.name, self.energy, self.protein, self.fat, self.carbohydrate, 
            self.aoac, self.satd, self.n_6, self.n_3, self.mono, self.poly, self.trans, 
            self.cholesterol, self.sodium, self.potassium, self.calcium, self.magnesium, 
            self.phosphorus, self.iron, self.copper, self.zinc, self.chloride, 
            self.manganese, self.selenium, self.iodine, self.retinol, self.carotene, 
            self.retinol_equivalent, self.d,  self.e, self.k1, self.thiamin, 
            self.riboflavin, self.niacin, self.tryptophan_60, self.niacin_equivalent,  
            self.b6, self.b12, self.folate, self.pantothenate, self.biotin, self.c, 
            self.alpha_carotene, self.beta_carotene, self.lutein, self.lycopene)