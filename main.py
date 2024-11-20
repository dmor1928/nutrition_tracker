'''
the file than is run to start the website
'''

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

