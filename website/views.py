'''
views.py will store the standard routes for our websites, such as the home page, etc.
Note than the login page will NOT be in here and will isntead be in auth.py, since you need to authenticate the login
'''

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user # type: ignore
from .models import Note, Foods, Recipe, RecipeIngredient, NutrientUnit, RDADefault
from . import db  # type: ignore
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required  # Home page not accessible unless logged in
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("home.html", user=current_user)  # current_user is passed into template to detect if a user is logged in and change the navbar accordingly

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Takesin data from a POST request
    noteId = note['noteId']  # Loaded as json object and access the noteId attribute
    note = Note.query.get(noteId)  # Search for note with noteId
    if note:  # Checks if note with noteId exists
        if note.user_id == current_user.id:  # Checks if user assigned to note is currently signed in 
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/product-page')
def productPage():
    return render_template("my-landing-page/my-product-page.html")

@views.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def createRecipePage():
    if request.method == "POST":  # If recieved "POST"

        recipe_name = request.form.get('recipe-name')
        recipe_description = request.form.get('recipe-description')
        recipe_dietary_restrictions = request.form.get('recipe-dietary-restrictions')

        keys = request.form.keys()  # request form keys
        
        def isValidAmountInput(amount):
            try:
                amount_float = float(amount)
                if amount_float >= 0:
                    return True
                else:
                    return False
            except ValueError:
                return False
        
        def RecipeURLName(recipe_name):
                # Format name so that it's a valid URL makeURLRecipeName
                formatted_name = recipe_name.lower()
                for character in [" ", "    "]:
                    formatted_name = formatted_name.replace(character, "-")
                for character in ["'", '"', "<", ">", "!", "?", "=", "/", "\\"]:
                    formatted_name = formatted_name.replace(character, "")
                return formatted_name

        # for key in keys:
        #     if not key.startswith("recipe-"):  
        #         # If key doesn't start with "-recipe" i.e not recipe-dietary-restrictions, name, or description
        #         # Implies filters to keys that are grams inputs name=food_id since they're the only names not starting with recipe-
        #         print(key)
        #         grams = int(request.form.get(key))  # <input> has name=food_id, value=amount in grams
        #         if grams == None:  # If there's no inputted grams i.e. invalid input
        #             food_id = int(key)
        #             food_name = db.session.get(Foods, food_id).name
        #             break
                # Summary: it looks at ingredient inputs which have food_id as name and value as amount in grams
                #          and then checks if grams is None i.e. invalid input
        
        ingredient_inputs = []
        for key in keys:
            if not key.startswith("recipe-"):
                food_id = int(key)
                food_name = db.session.get(Foods, food_id).name
                food_amount = int(request.form.get(key))
                ingredient_inputs.append((food_id, food_name, food_amount))

        if len(ingredient_inputs) == 0:
            flash('Error: No ingredients added', category='error')
            return redirect(url_for('views.createRecipePage'))
        
        # for id, name, amount in ingredient_inputs:  # Form already ensures inputs are valid
        #     print("name: ", name)
        #     print("amount: ", amount)

        #     if not isValidAmountInput(amount):
        #         flash(f'Error: {name} ingredient has invalid amount {amount}', category='error')
        #         return redirect(url_for('views.createRecipePage'))
        
        if recipe_name is None:
            flash('Error: No recipe name added', category='error')
            return redirect(url_for('views.createRecipePage'))

        elif len(recipe_name) < 5:
            flash('Error: Recipe name is too short (minimum length 5)', category='error')
            return redirect(url_for('views.createRecipePage'))

        elif len(recipe_name) > 64:
            flash('Error: Recipe name too long (64 limit max)', category='error')
            return redirect(url_for('views.createRecipePage'))

        else:
            is_vegan = True
            is_vegetarian = True
            is_pescatarian = True

            if recipe_dietary_restrictions != "vegan":
                is_vegan = False
            if recipe_dietary_restrictions != "vegetarian":
                is_vegetarian = False
            if recipe_dietary_restrictions != "pescatarian":
                is_pescatarian = False
            
            recipe_name_formatted = RecipeURLName(recipe_name)

            new_recipe = Recipe(
                name=recipe_name, 
                formatted_name=recipe_name_formatted,
                description=recipe_description, 
                vegetarian=is_vegetarian,
                vegan=is_vegan,
                pescatarian=is_pescatarian,
                user_id=current_user.id)
            
            db.session.add(new_recipe)
            db.session.commit()

            new_recipe_id = Recipe.query.filter(
                Recipe.user_id == current_user.id,
                Recipe.name == recipe_name).first().id
            
            print("new_recipe_id: ", new_recipe_id)
            
            new_ingredients = []
            for id, name, amount in ingredient_inputs:  # Form already ensures inputs are valid
                print("food name: ", name)
                print("amount: ", amount)
                new_ingredient = RecipeIngredient(amount=amount, food_id=id, food_name=name, recipe_id=new_recipe_id)
                new_ingredients.append(new_ingredient)
            
            db.session.add_all(new_ingredients)
            db.session.commit()
            flash('Recipe added', category='success')
            return redirect(url_for("views.viewRecipePage", formatted_recipe_name=recipe_name_formatted, recipe_id=new_recipe_id))  # Redirect to nutrition page
    return render_template(
            "create-recipe.html", 
            user=current_user, 
            foods=db.session.query(Foods).all())

@views.route('/my-recipes', methods=['GET', 'POST'])
@login_required
def myRecipesPage():
    if request.method == "POST":
        formatted_recipe_name = request.form['recipe-name']
        recipe_id = request.form['recipe-id']
        if request.form["view-or-edit"] == "view":
            return redirect(url_for("views.viewRecipePage", formatted_recipe_name=formatted_recipe_name, recipe_id=recipe_id))
        if request.form["view-or-edit"] == "edit":  # TO-DO: Redirect to create recipe page, with list and amounts prefilled with recipe data
            return redirect(url_for)
        
    return render_template(
            "my-recipes.html",  # If you click on an 'open recipe' button in my-recipes.html it sends you to /my-recipes/<recipe_name>
            user=current_user,
            my_recipes=db.session.query(Recipe).filter(Recipe.user_id == current_user.id))

@views.route('/my-recipes/<formatted_recipe_name>')
@login_required
def viewRecipePage(formatted_recipe_name):
    recipe_id=request.args.get('recipe_id')
    recipe = db.session.get(Recipe, recipe_id)  # TO-DO: Add authentication for user before viewing view-recipe page
    recipe_ingredients = db.session.query(RecipeIngredient).filter_by(recipe_id=recipe_id)

    # user_rda = db.session.get(RDA, rda_id)
    # print(user_rda)
    
    nutrient_units = {}
    for row in NutrientUnit.query.all():
        nutrient_units[row.nutrient] = row.unit

    def NutrientEntry():
        # missing_entries = ["water", "choline", "chromium", "fluoride", "molybdenum"]
        if key in ["name", "_sa_instance_state", "age", "category", "sex"] or "_percent" in key:
            return False
        # elif key in missing_entries:
        #     print(f"{key} is a missing entry")
        #     return False
        else:
            return True
    def NutrientEntryIsNone():
        if ingredient_nutrition_per100g[key] == None or ingredient_nutrition_per100g[key] == "NULL":
            return True
        else:
            return False
    def NutrientEntryIsUnknown():  # Not zero but not known
        if ingredient_nutrition_per100g[key] == "N":
            return True
        else:
            return False
    def NutrientEntryIsTrace():
        if ingredient_nutrition_per100g[key] == "Tr":
            return True
        else:
            return False
    
    recipe_foods_nutrition = []
    total_recipe_nutrition = {}
    for ingredient in recipe_ingredients:

        recipe_ingredient_nutrition = {}
        ingredient_nutrition_per100g = db.session.get(Foods, ingredient.food_id).__dict__

        for key in ingredient_nutrition_per100g:

            if NutrientEntry():

                if key not in total_recipe_nutrition:
                    total_recipe_nutrition[key] = 0

                if NutrientEntryIsNone() or NutrientEntryIsTrace(): 
                    continue

                elif NutrientEntryIsUnknown():  # TO-DO: Track which nutrients have inaccuracies / unknown
                    pass

                else:
                    recipe_ingredient_nutrition[key] = round(float(ingredient_nutrition_per100g[key]) * (ingredient.amount / 100), 2)
                    total_recipe_nutrition[key] += recipe_ingredient_nutrition[key]
        
        recipe_foods_nutrition.append(recipe_ingredient_nutrition)

    
    # Calculate percentages before rounding total_recipe_nutrition to avoid rounding errors
    if current_user.isCustomRDA:
        pass
    else:
        # print(total_recipe_nutrition)
        user_rda = db.session.get(RDADefault, current_user.RDADefault_id).__dict__
        user_rda_percent = {}
        for key in user_rda:
            if NutrientEntry():

                if key in ["water", "choline", "chromium", "fluoride", "molybdenum", "sugar"]:  # Missing entry
                    user_rda_percent[key] = -1

                elif user_rda[key] != 0:
                    percentage = 100 * total_recipe_nutrition[key] / float(user_rda[key])
                    user_rda_percent[key] = round(percentage, 2)
                else:
                    if total_recipe_nutrition[key] == 0:
                        user_rda_percent[key] = 0
                    else:
                        user_rda_percent[key] = 100
    
    for key in total_recipe_nutrition:
        total_recipe_nutrition[key] = round(total_recipe_nutrition[key], 2)
    
    print(user_rda_percent)

    # food_name = db.session.get(Foods, food_id).name
    return render_template(
        "view-recipe.html", 
        user=current_user, 
        recipe=recipe,  # Recipe name, description
        recipe_ingredients = recipe_ingredients,  # Full name ingredients list and amount
        recipe_foods_nutrition=recipe_foods_nutrition,
        total_recipe_nutrition=total_recipe_nutrition,
        nutrient_units=nutrient_units,
        user_rda_percent=user_rda_percent)  # Goes to view-recipe.html