# import the Flask class from the flask module
from flask import Flask, render_template
import dikkysbrain

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
    return render_template('faslaan.html')  # render a template

@app.route('/punjabFeedback')
def punjabFeedback():
    s = dikkysbrain.main()
    text_file = open("output.txt", "w")
    text_file.write(s)
    text_file.close()
    return render_template('punjabFeedback.html')  # render a template

@app.route('/dhamaalFeedback')
def dhamaalFeedback():
    return render_template('dhamaalFeedback.html')  # render a template

@app.route('/faslaanFeedback')
def faslaanFeedback():
    return render_template('faslaanFeedback.html')  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
