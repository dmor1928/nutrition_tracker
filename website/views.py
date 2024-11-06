'''
views.py will store the standard routes for our websites, such as the home page, etc.
Note than the login page will NOT be in here and will isntead be in auth.py, since you need to authenticate the login
'''

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user # type: ignore
from .models import Note, Recipe, RecipeIngredient, NutrientUnit, RDAValues, UserPersonalRDA#, RDADefault
from .fdc_models import FDCFood, FDCFoodNutrition, FDCNutrients, FDCFoodPortion, FDCFoodPreparationOptions, FDCFoodPreparationFactors
from . import db  # type: ignore
import pandas as pd
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
                # food_name = db.session.get(Foods, food_id).name
                food_name = db.session.get(FDCFood, food_id).name
                print(food_name)
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
                # foods=db.session.query(Foods).all())
                foods = db.session.query(FDCFood).all())

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
            foods=db.session.query(FDCFood).all())
    
    elif request.form.get('delete-recipe'):
        print("DELETE-RECIPE: ", request.form.get('delete-recipe'))

        recipe_ingredients = db.session.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()
        # For ingredient in recipe ingredients: 
        for ingredient in recipe_ingredients:
            db.session.delete(ingredient)
        db.session.commit()

        recipe = db.session.query(Recipe).filter(Recipe.id == recipe_id, Recipe.user_id == current_user.id).first()
        db.session.delete(recipe)
        db.session.commit()
        
        print("Recipe deleted")
        return redirect(url_for('views.myRecipesPage'))


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
                food_name = db.session.get(FDCFood, food_id).name
                food_amount = float(request.form.get(key))
                new_ingredient_inputs.append((food_id, food_name, food_amount))
                print("new_ingredient_inputs: ", new_ingredient_inputs)
        
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
    recipe_ingredients = db.session.query(RecipeIngredient).filter_by(recipe_id=recipe_id).all()

    # Loading nutrition RDA data
    file = open('fdc-database/clean_fdc_nutrients_dictionary.json')
    nutrient_name_from_id = dict((v,k) for k,v in json.load(file).items())

    filtered_fdc_nutrition = db.session.query(FDCFoodNutrition).filter(
        FDCFoodNutrition.nutrient_id.in_(list(nutrient_name_from_id.keys())))

    user_rda_nutrients = db.session.query(UserPersonalRDA.nutrient).filter_by(user_id=current_user.id).all()
    user_rda_nutrients = [x[0] for x in user_rda_nutrients]
    user_rda_amounts = db.session.query(UserPersonalRDA.rda).filter_by(user_id=current_user.id).all()
    user_rda_amounts = [x[0] for x in user_rda_amounts]

    user_rda = dict(zip(user_rda_nutrients, user_rda_amounts))
    print("user_rda before placeholders: ", user_rda)

    for nutrient in nutrient_name_from_id.values():
        if nutrient not in user_rda:
            if nutrient in ['lycopene', 'lutein_zeaxanthin', 'quercetin', 'flavonoids', 'myricetin']: # 'resveratrol' removed for now
                user_rda[nutrient] = 100
            elif nutrient in ['energy']:
                user_rda[nutrient] = 2000
            elif nutrient in ['total_polyunsaturated', 'total_monounsaturated']:
                user_rda[nutrient] = 20
            elif nutrient == 'total_sugar':
                user_rda[nutrient] = 80
            elif nutrient == 'added_sugars':
                user_rda[nutrient] = 20
            else:
                continue
            print(f"{nutrient} not in user_rda. Adding placeholder")

    print("user_rda after placeholders: ", user_rda)

    ingredients_raw_data_per100g = []
    for ingredient in recipe_ingredients:

        ingredient_nutrient_data = {}
        for key in nutrient_name_from_id.values():  # Initialising to 0 in case values are missing
            ingredient_nutrient_data[key] = 0

        ingredient_nutrient_data['food_id'] = ingredient.food_id
        
        for nutrient in filtered_fdc_nutrition.filter(FDCFoodNutrition.fdc_id == ingredient.food_id).all():
            nutrient_name = nutrient_name_from_id[nutrient.nutrient_id]
            ingredient_nutrient_data[nutrient_name] = nutrient.amount

        ingredients_raw_data_per100g.append(ingredient_nutrient_data)

    def nutrientRDAisPercent(key):
        """Returns if the key for a nutrient is for a percent key e.g. carbohydrate_max_percent --> True"""
        if "_percent" in key:
            return True
        else:
            return False
        
    ingredients_refined_data_per_100g = []
    for ingredient in ingredients_raw_data_per100g:

        nutrition_per_100g = {}
        nutrition_per_100g['food_id'] = ingredient['food_id']

        for key in user_rda:

            if nutrientRDAisPercent(key):
                continue

            elif key == "vit_a":
                nutrition_per_100g[key] = ingredient['vit_a_RAE']

            elif key == "vit_d":
                nutrition_per_100g[key] = ingredient['vit_d2_d3_UG']

            elif key == "vit_e":
                nutrition_per_100g[key] = ingredient['vit_e_mg']

            elif key == "vit_k":
                nutrition_per_100g[key] = ingredient['vit_k2'] + ingredient['vit_k1']

            elif key == "omega_3":
                nutrition_per_100g[key] = sum([ingredient[o_3] for o_3 in ['omega_3_ALA', 'omega_3_EPA', 'omega_3_DHA']])

            elif key == "omega_6":
                nutrition_per_100g[key] = sum([ingredient[o_6] for o_6 in ['omega_6_20_2', 'omega_6_18_2', 'omega_6_18_3', 'omega_6_20_3', 'omega_6_20_4']])

            elif key == "methionine_and_cysteine":
                nutrition_per_100g[key] = ingredient['methionine'] # + ingredient['cysteine']

            elif key == "phenylalanine_and_tyrosine":
                nutrition_per_100g[key] = ingredient['phenylalanine'] + ingredient['tyrosine']

            else:
                nutrition_per_100g[key] = ingredient[key]
        
        ingredients_refined_data_per_100g.append(nutrition_per_100g)
    

    total_recipe_nutrient_data = {}
    total_recipe_user_rda_percent = {}
    for key in user_rda:
        if nutrientRDAisPercent(key):
            print(f"Error for key {key}: percentages not yet implemented")
            continue

        total_nutrient_amount = 0
        for ingredient_index, ingredient in enumerate(recipe_ingredients):
            nutrient_amount = ingredients_refined_data_per_100g[ingredient_index][key]
            total_nutrient_amount += round(float(nutrient_amount / 100) * ingredient.amount, 2) 
            
        if user_rda[key] != 0:
            percentage = 100 * total_nutrient_amount / float(user_rda[key])
            total_recipe_user_rda_percent[key] = round(percentage, 2)
        else:
            if total_nutrient_amount == 0:
                total_recipe_user_rda_percent[key] = 0
            else:
                total_recipe_user_rda_percent[key] = 100
    
        total_recipe_nutrient_data[key] = round(total_nutrient_amount, 2)

    nutrient_units = {}
    for row in FDCNutrients.query.all():
        if row.id in nutrient_name_from_id.keys():
            if row.unit_name in ['G', 'MG', 'UG']:
                unit = row.unit_name.lower()
            elif row.unit_name in ['KCAL']:
                unit = row.unit_name.title()
            else:
                unit = row.unit_name
            nutrient_units[nutrient_name_from_id[row.id]] = unit

    
    total_recipe_nutrition_json = json.dumps(ingredients_refined_data_per_100g)
    ingredients_raw_data_per100g_json = json.dumps([ob for ob in ingredients_raw_data_per100g])
    user_rda_json = json.dumps(user_rda)
    total_recipe_user_rda_percent_json = json.dumps(total_recipe_user_rda_percent)

    print("total_recipe_nutrient_data: ", total_recipe_nutrient_data)
    print("recipe_foods_nutrition_json: ", ingredients_raw_data_per100g)

    return render_template(
        "view-recipe.html", 
        user=current_user, 
        recipe=recipe,  # Recipe information
        recipe_ingredients = recipe_ingredients,  # Full name of ingredients list and amounts

        # Initial filled html data
        total_recipe_nutrition=total_recipe_nutrient_data,
        total_recipe_user_rda_percent=total_recipe_user_rda_percent,

        # Total recipe and ingredients data js data
        total_recipe_nutrition_json=total_recipe_nutrition_json,
        recipe_foods_nutrition_json=ingredients_raw_data_per100g_json,  # Per 100g
        user_rda_json=user_rda_json,
        total_recipe_user_rda_percent_json=total_recipe_user_rda_percent_json,

        nutrient_units=nutrient_units,
        )  # Goes to view-recipe.html

@views.route('/add-rda')
@login_required
def addPersonalisedRDATest():
    profile_rda_values = db.session.query(RDAValues).filter_by(rda_profile_id=current_user.rda_profile_id).all()
    amino_acids = ['histidine','isoleucine','leucine','lysine','methionine_and_cysteine', 
                   'phenylalanine_and_tyrosine','threonine','tryptophan','valine']

    for row in profile_rda_values:
        if '_per_kg' in row.unit:
            weight_adjusted_value = row.value * current_user.weight_kg
        else:
            weight_adjusted_value = row.value
        
        if row.nutrient_name in amino_acids: # Convert amino acid RDAs from mg to g
            weight_adjusted_value = weight_adjusted_value / 1000
        
        # if row.nutrient_name == "carbohydrate_total":
        #     nutrient_name = "carbohydrate_by_diff"
        # else:
        #     nutrient_name = row.nutrient_name

        exists = db.session.query(UserPersonalRDA).filter_by(user_id=current_user.id, nutrient=row.nutrient_name).first() is not None
        if not exists:
            personal_rda = UserPersonalRDA(
                user_id = current_user.id,
                nutrient=row.nutrient_name,
                rda = weight_adjusted_value
            )
            db.session.add(personal_rda)
        else:
            if db.session.query(UserPersonalRDA).filter_by(user_id=current_user.id, nutrient=row.nutrient_name).first().rda == weight_adjusted_value:
                continue
            else:
                db.session.query(UserPersonalRDA).filter_by(user_id=current_user.id, nutrient=row.nutrient_name).first().rda = weight_adjusted_value
    db.session.commit()

    return render_template(
        "base.html",
        user=current_user
        )