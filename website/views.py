'''
views.py will store the standard routes for our websites, such as the home page, etc.
Note than the login page will NOT be in here and will isntead be in auth.py, since you need to authenticate the login
'''

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user # type: ignore
from .models import Note, Foods, Recipe, RecipeIngredient
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
    if request.method == "POST":

        recipe_name = request.form.get('recipe-name')
        recipe_description = request.form.get('recipe-description')
        recipe_dietary_restrictions = request.form.get('recipe-dietary-restrictions')

        keys = request.form.keys()

        for key in keys:
            if not key.startswith("recipe-"):
                print(key)
                grams = int(request.form.get(key))
                if grams == None:
                    food_id = int(key)
                    food_name = db.session.get(Foods, food_id).name
                    break
        
        if recipe_name is None:
            flash('Error: No recipe name added', category='error')
        elif len(recipe_name) < 5:
            flash('Recipe name is too short', category='error')
        elif 'food_id' in locals():  # If in locals() then grams == None
            flash(food_name, ' in list has missing grams value', category='error')
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
            
            recipe_name_formatted = recipe_name.lower()
            for character in [" ", "    "]:
                recipe_name_formatted = recipe_name_formatted.replace(character, "-")
            for character in ["'", '"', "<", ">", "!", "?", "=", "/", "\\"]:
                recipe_name_formatted = recipe_name_formatted.replace(character, "")

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
            for key in keys:
                if not key.startswith("recipe-"):
                    food_id = key
                    food_name = db.session.get(Foods, food_id).name
                    print("food name: ", food_name)
                    grams = int(request.form.get(key))
                    new_ingredient = RecipeIngredient(amount=grams, food_id=food_id, food_name=food_name, recipe_id=new_recipe_id)
                    new_ingredients.append(new_ingredient)
                    # db.session.add(new_ingredient)
            db.session.add_all(new_ingredients)
            db.session.commit()
            flash('Recipe added', category='success')
            return render_template("home.html", user=current_user)
        return render_template(
            "create-recipe.html", 
            user=current_user, 
            foods=db.session.query(Foods).all())
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
        
    return render_template(
            "my-recipes.html",  # If you click on an 'open recipe' button in my-recipes.html it sends you to /my-recipes/<recipe_name>
            user=current_user,
            my_recipes=db.session.query(Recipe).filter(Recipe.user_id == current_user.id))

@views.route('/my-recipes/<formatted_recipe_name>')
@login_required
def viewRecipePage(formatted_recipe_name):
     recipe_id=request.args.get('recipe_id')
     recipe = db.session.get(Recipe, recipe_id)
     recipe_ingredients = db.session.query(RecipeIngredient).filter_by(recipe_id=recipe_id)
     print(recipe_ingredients)
     # food_name = db.session.get(Foods, food_id).name
     return render_template(
         "view-recipe.html", 
         user=current_user, 
         recipe=recipe, 
         recipe_ingredients=recipe_ingredients)  # Goes to view-recipe.html