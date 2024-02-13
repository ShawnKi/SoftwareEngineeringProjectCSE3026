from flask import Flask, render_template
import os

# Create the Flask application and specify the templates directory
app = Flask(__name__, template_folder='templates')

print("Template folder (relative):", app.template_folder)

print("Template folder (relative):", app.template_folder)

# Get the absolute path of the templates directory
templates_dir_abs = os.path.join(app.root_path, app.template_folder)

print("Template folder (absolute):", templates_dir_abs)

# Print the contents of the templates directory
print("Contents of the templates directory:")
for filename in os.listdir(templates_dir_abs):
    print(filename)

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
    app.run(host='localhost',, port='8080',debug=True)
