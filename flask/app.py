from flask import Flask

app = Flask(__name__) # Create a Flask application instance

@app.route('/') # Website decorator to define the home route
def home(): #defining a home function
    return "Hello, Flask!"