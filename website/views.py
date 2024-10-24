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

def validRecipeName(recipe_name):
    if recipe_name is None:
        flash('Error: No recipe name added', category='error')
        return False
    elif len(recipe_name) < 5:
        flash('Error: Recipe name is too short (minimum length 5)', category='error')
        return False
    elif len(recipe_name) > 64:
        flash('Error: Recipe name too long (64 limit max)', category='error')
        return False
    else:
        return True

def RecipeURLName(recipe_name):
    # Format name so that it's a valid URL makeURLRecipeName
    formatted_name = recipe_name.lower()
    for character in [" ", "    "]:
        formatted_name = formatted_name.replace(character, "-")
    for character in ["'", '"', "<", ">", "!", "?", "=", "/", "\\"]:
        formatted_name = formatted_name.replace(character, "")
    return formatted_name

@views.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def createRecipePage():
    if request.method == "POST":  # If recieved "POST"

        recipe_name = request.form.get('recipe-name')
        recipe_description = request.form.get('recipe-description')
        recipe_dietary_restrictions = request.form.get('recipe-dietary-restrictions')

        keys = request.form.keys()  # request form keys
    
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
        
        if not validRecipeName(recipe_name):
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
    else:
        return render_template(
                "create-recipe.html", 
                user=current_user, 
                foods=db.session.query(Foods).all())

@views.route('/my-recipes/<formatted_recipe_name>/edit', methods=['GET', 'POST'])
@login_required
def editRecipePage(formatted_recipe_name):
    recipe_id = request.args.get('recipe_id')
    print(recipe_id)
    old_recipe_ingredients = db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()

    if request.method != "POST":
        return render_template(
            "edit-recipe.html", 
            user=current_user, 
            recipe = db.session.query(Recipe).filter(Recipe.id == recipe_id).first(),
            recipe_ingredients=old_recipe_ingredients,
            foods=db.session.query(Foods).all())

    else:  # Save recipe
        # Similar checks to createRecipePage but delete any ingredients no longer included and add any that are now included
        new_recipe_name = request.form.get('recipe-name')
        new_recipe_description = request.form.get('recipe-description')
        new_recipe_dietary_restrictions = request.form.get('recipe-dietary-restrictions')

        keys = request.form.keys()  # request form keys
        new_ingredient_inputs = []
        for key in keys:
            if not key.startswith("recipe-"):
                food_id = int(key)
                food_name = db.session.get(Foods, food_id).name
                food_amount = float(request.form.get(key))
                new_ingredient_inputs.append((food_id, food_name, food_amount))
        
        if len(new_ingredient_inputs) == 0:
            flash('Error: No ingredients added', category='error')
            return redirect(url_for('views.createRecipePage'))
        
        if not validRecipeName(new_recipe_name):
            return redirect(url_for('views.createRecipePage'))

        else:

            is_vegan = True
            is_vegetarian = True
            is_pescatarian = True

            if new_recipe_dietary_restrictions != "vegan":
                is_vegan = False

            if new_recipe_dietary_restrictions != "vegetarian":
                is_vegetarian = False

            if new_recipe_dietary_restrictions != "pescatarian":
                is_pescatarian = False
            
            recipe_name_formatted = RecipeURLName(new_recipe_name)

            # new_recipe = Recipe(
            #     name=new_recipe_name, 
            #     formatted_name=recipe_name_formatted,
            #     description=new_recipe_description, 
            #     vegetarian=is_vegetarian,
            #     vegan=is_vegan,
            #     pescatarian=is_pescatarian,
            #     user_id=current_user.id)
            
            old_recipe = db.session.query(Recipe).filter(Recipe.id == recipe_id).first()
            
            old_recipe.name = new_recipe_name
            old_recipe.formatted_name = recipe_name_formatted
            old_recipe.description = new_recipe_description
            old_recipe.vegetarian = is_vegetarian
            old_recipe.vegan = is_vegan
            old_recipe.pescatarian = is_pescatarian
            db.session.commit()
            
            print("recipe_id: ", recipe_id)
            
            current_database_ingredients = []
            for ingredient in db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all():
                current_database_ingredients.append((ingredient.food_id, ingredient.food_name, ingredient.amount))
            
            ingredients_in_new_but_not_in_old = list(set(new_ingredient_inputs).difference(current_database_ingredients))
            ingredients_in_old_but_not_in_new = list(set(current_database_ingredients).difference(new_ingredient_inputs))

            print("current_database_ingredients: ", current_database_ingredients)
            print("new_ingredient_inputs: ", new_ingredient_inputs)
            print("ingredients_in_new_but_not_in_old: ", ingredients_in_new_but_not_in_old)
            print("ingredients_in_old_but_not_in_new: ", ingredients_in_old_but_not_in_new)

            def tupleListContains(list, given_char):
                for tuple in list:
                    for ch in tuple:
                        if ch == given_char:
                            return True
                return False

            # This will only work if there are NOT multiple entries for the same food_id
            for food_id, name, amount in ingredients_in_old_but_not_in_new:
                print("food_id: ", food_id)
                if tupleListContains(ingredients_in_new_but_not_in_old, food_id):  # Then only change amount
                    food_id_list = list(zip(*ingredients_in_new_but_not_in_old))[0]
                    index_with_food_id = food_id_list.index(food_id)
                    new_amount = ingredients_in_new_but_not_in_old[index_with_food_id][2]
                    print("Amount of", food_id, "changed")
                    print("old amount of", food_id,": ", amount)
                    print("new amount of", food_id,": ", new_amount)
                    db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id, RecipeIngredient.food_id == food_id).first().amount = new_amount # Edit change
                    ingredients_in_new_but_not_in_old.remove(ingredients_in_new_but_not_in_old[index_with_food_id]) # And then delete the tuple from ingredients_in_new_but_not_in_old
                    # So that at end of for loop, remaining tuples in ingredients_in_new_but_not_in_old are only the newly added ingredients
                else:  # if food_id isn't in 'ingredients_in_new_but_not_in_old' then it has been deleted
                    # Delete food_id in RecipeIngredient
                    deleted_ingredient = db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id, RecipeIngredient.food_id == food_id).first()
                    db.session.delete(deleted_ingredient)
            
            new_ingredients = []
            for food_id, food_name, amount in ingredients_in_new_but_not_in_old:
                new_ingredient = RecipeIngredient(amount=amount, food_id=food_id, food_name=food_name, recipe_id=recipe_id)
                new_ingredients.append(new_ingredient)
            db.session.add_all(new_ingredients)
            db.session.commit()

            # new_ingredients = []
            # for food_id, name, amount in new_ingredient_inputs:  # Form already ensures inputs are valid
            #     print("food name: ", name)
            #     print("amount: ", amount)
            #     new_ingredient = RecipeIngredient(amount=amount, food_id=id, food_name=name, recipe_id=new_recipe_id)
            #     new_ingredients.append(new_ingredient)

            # db.session.add_all(new_ingredients)
            # db.session.commit()

            flash('Recipe added', category='success')
            return redirect(url_for("views.viewRecipePage", formatted_recipe_name=recipe_name_formatted, recipe_id=recipe_id))  # Redirect to nutrition page
        pass

@views.route('/my-recipes', methods=['GET', 'POST'])
@login_required
def myRecipesPage():
    if request.method == "POST":
        formatted_recipe_name = request.form['recipe-name']
        recipe_id = request.form['recipe-id']
        print("myRecipesPage() recipe_id: ", recipe_id)
        view_or_edit = request.form["view-or-edit"]
        print("view_or_edit", view_or_edit)
        if view_or_edit == "view":
            return redirect(url_for("views.viewRecipePage", formatted_recipe_name=formatted_recipe_name, recipe_id=recipe_id))
        if view_or_edit == "edit":  # TO-DO: Redirect to create recipe page, with list and amounts prefilled with recipe data
            return redirect(url_for("views.editRecipePage", formatted_recipe_name=formatted_recipe_name, recipe_id=recipe_id))
        
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
