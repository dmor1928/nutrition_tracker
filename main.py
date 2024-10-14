'''
the file than is run to start the website
'''

from website import create_app

app = create_app()

if __name__ == '__main__':  # Ensures it doesn't run if this is imported anywhere
    app.run(debug=True)  # Automatically updates the webserver when changes are made

