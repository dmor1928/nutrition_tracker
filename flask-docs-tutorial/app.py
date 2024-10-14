# app.py
from flask import Flask  # Import Flask class, which will be our WSGI app
from markupsafe import escape  # Adding this when running user-inputted strings ensures they are treated as text and not as a script that could be executed on the server host's computer

app = Flask(__name__)  # Create instance of Flask class. first argument is the name of the app's module or package __name__ is appropriate in most cases

@app.route("/")  # route() decorator tells Flask which URL should trigger the function 'app' to run
def index():
    return "Index Page"  # Returns the message we want to display, default type HTML hence <p> tags

@app.route("/hello")
def hello():
    return "Hiya, world!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

# The filepath for the style.css is url_for('static', filename='style.css')

