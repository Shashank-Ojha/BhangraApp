# import the Flask class from the flask module
from flask import Flask, render_template

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/index')
def index():
    return render_template('index.html')  # render a template

@app.route('/menu')
def menu():
    return render_template('menu.html')  # render a template

@app.route('/punjab')
def punjab():
    return render_template('punjab.html')  # render a template

@app.route('/dhamaal')
def dhamaal():
    return render_template('dhamaal.html')  # render a template

@app.route('/faslaan')
def faslaan():
    return render_template('faslaan.html')  # render a templat3

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
