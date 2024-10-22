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

    birthDate = db.Column(db.Date)
    age = db.Column(db.Float)
    sex = db.Column(db.String(8)) # male or female
    isPregnant = db.Column(db.Boolean)
    isLactating = db.Column(db.Boolean)
    rda_id = db.column(db.Integer), db.ForeignKey('RDA')

# Database model for recipe ingredients
class RecipeIngredient(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # The id uniquely identifying each instance of an ingredient in a recipe (various amounts etc.)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))  # Links the instance of an ingredient to its recipe
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    food_name = db.Column(db.String(250), db.ForeignKey('foods.name'))
    amount = db.Column(db.Float)  # In grams

# Database model for recipes containing descriptive information for recipe, and the user who created it
# Recipe --> RecipeIngredient is one-to-many
class Recipe(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    formatted_name = db.Column(db.String(64))  # For html and URLs
    description = db.Column(db.String(1000))
    vegetarian = db.Column(db.Boolean)  # Dietary requirements
    vegan = db.Column(db.Boolean)
    pescatarian = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Which user created the recipe

# Database model for food nutritional information (same as in add-food-to-database.py)
class Foods(db.Model):  # type: ignore
    # TO-DO: Make more complete list of nutritional information from USDA database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))

    alpha_carotene = db.Column(db.Float)
    b12 = db.Column(db.Float)
    b6 = db.Column(db.Float)
    beta_carotene = db.Column(db.Float)
    biotin = db.Column(db.Float)
    c = db.Column(db.Float)
    calcium = db.Column(db.Float)
    carbohydrate = db.Column(db.Float)
    carotene = db.Column(db.Float)
    chloride = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    copper = db.Column(db.Float)
    d = db.Column(db.Float)
    e = db.Column(db.Float)
    energy = db.Column(db.Float)
    fat = db.Column(db.Float)
    fibre = db.Column(db.Float)
    folate = db.Column(db.Float)
    iodine = db.Column(db.Float)
    iron = db.Column(db.Float)
    k1 = db.Column(db.Float)
    lutein = db.Column(db.Float)
    lycopene = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    manganese = db.Column(db.Float)
    mono = db.Column(db.Float)
    n_3 = db.Column(db.Float)
    n_6 = db.Column(db.Float)
    niacin = db.Column(db.Float)
    niacin_equivalent = db.Column(db.Float)
    pantothenate = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    poly = db.Column(db.Float)
    potassium = db.Column(db.Float)
    protein = db.Column(db.Float)
    retinol = db.Column(db.Float)
    retinol_equivalent = db.Column(db.Float)
    riboflavin = db.Column(db.Float)
    satd = db.Column(db.Float)
    selenium = db.Column(db.Float)
    sodium = db.Column(db.Float)
    thiamin = db.Column(db.Float)
    trans = db.Column(db.Float)
    tryptophan_60 = db.Column(db.Float)
    zinc = db.Column(db.Float)

    def __repr__(self):
        return '''<Foods(id='{0}', name='{1}', alpha_carotene='{2}', b12='{3}', b6='{4}', 
        beta_carotene='{5}', biotin='{6}', c='{7}', calcium='{8}', carbohydrate='{9}', 
        carotene='{10}', chloride='{11}', cholesterol='{12}', copper='{13}', d='{14}', 
        e='{15}', energy='{16}', fat='{17}', fibre='{18}', folate='{19}', iodine='{20}', 
        iron='{21}', k1='{22}', lutein='{23}', lycopene='{24}', magnesium='{25}', 
        manganese='{26}', mono='{27}', n_3='{28}', n_6='{29}', niacin='{30}', 
        niacin_equivalent='{31}', pantothenate='{32}', phosphorus='{33}', poly='{34}', 
        potassium='{35}', protein='{36}', retinol='{37}', retinol_equivalent='{38}', 
        riboflavin='{39}', satd='{40}', selenium='{41}', sodium='{42}', thiamin='{43}', 
        trans='{44}', tryptophan_60='{45}', zinc='{46}')>'''.format(
            self.id, self.name, self.alpha_carotene, self.b12, self.b6, self.beta_carotene, 
            self.biotin, self.c, self.calcium, self.carbohydrate, self.carotene, 
            self.chloride, self.cholesterol, self.copper, self.d, self.e, self.energy, 
            self.fat, self.fibre, self.folate, self.iodine, self.iron, self.k1, self.lutein, 
            self.lycopene, self.magnesium, self.manganese, self.mono, self.n_3, self.n_6, 
            self.niacin, self.niacin_equivalent, self.pantothenate, self.phosphorus, 
            self.poly, self.potassium, self.protein, self.retinol, self.retinol_equivalent, 
            self.riboflavin, self.satd, self.selenium, self.sodium, self.thiamin, self.trans, 
            self.tryptophan_60, self.zinc)

# Nutrient units
class NutrientUnit(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    nutrient = db.Column(db.String(32))
    unit = db.Column(db.String(8))


# Nutrients
class RDA(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    category = db.Column(db.String(32))
    sex = db.Column(db.String(8))

    # TO-DO: Make more complete list of RDA for all nutrients
    # TO-DO: implement pregnancy and lactating RDAs

    b12 = db.Column(db.Integer)
    b6 = db.Column(db.Integer)
    biotin = db.Column(db.Integer)
    c = db.Column(db.Integer)
    calcium = db.Column(db.Integer)
    carbohydrate = db.Column(db.Integer)
    carbohydrate_max_percent = db.Column(db.Integer)
    carbohydrate_min_percent = db.Column(db.Integer)
    chloride = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    choline = db.Column(db.Integer)
    chromium = db.Column(db.Integer)
    copper = db.Column(db.Integer)
    d = db.Column(db.Integer)
    e = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    fat_max_percent = db.Column(db.Integer)
    fat_min_percent = db.Column(db.Integer)
    fibre = db.Column(db.Integer)
    fluoride = db.Column(db.Integer)
    folate = db.Column(db.Integer)
    iodine = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    k = db.Column(db.Integer)
    magnesium = db.Column(db.Integer)
    manganese = db.Column(db.Integer)
    molybdenum = db.Column(db.Integer)
    n_3 = db.Column(db.Integer)
    n_3_max_percent = db.Column(db.Integer)
    n_3_min_percent = db.Column(db.Integer)
    n_6 = db.Column(db.Integer)
    n_6_max_percent = db.Column(db.Integer)
    n_6_min_percent = db.Column(db.Integer)
    niacin = db.Column(db.Integer)  # b3
    pantothenate = db.Column(db.Integer)  # b5
    phosphorus = db.Column(db.Integer)
    potassium = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    protein_max_percent = db.Column(db.Integer)
    protein_min_percent = db.Column(db.Integer)
    retinol = db.Column(db.Integer)
    riboflavin = db.Column(db.Integer)  # b2
    satd = db.Column(db.Integer)
    selenium = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    thiamin = db.Column(db.Integer)  # b1
    trans = db.Column(db.Integer)
    water = db.Column(db.Integer)
    zinc = db.Column(db.Integer)