from flask import Flask, render_template
import os

# Get the absolute path of the directory where app.py is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define the templates directory
templates_dir = os.path.join(dir_path, 'tree', 'test1', 'templates')

# Create the Flask application and specify the templates directory
app = Flask(__name__, template_folder=templates_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    print("Starting application")
    app.run(debug=True)
