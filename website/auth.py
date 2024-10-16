'''
for managing logins and authentication.

Has the login(), logout(), and signup() functions, routed to ./login, ./logout, ./sing-up respectively

'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user # type: ignore

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): # if inputted password from form (password) equals saved password in User database (user.password)
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email is not registered', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required  # Ensures this function is not accessible if you are not logged in
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        
        user = User.query.filter_by(email=email).first()
        if user:  # Checking if user with same email is already registered
            flash('Email already registered', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 8:
             flash('Password must be at least 8 characters long', category='error')
        else:
            # add user to database
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account registered', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)
