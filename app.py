from flask import Flask, render_template

# Create the Flask application and specify the templates directory
app = Flask(__name__, template_folder='test1/templates')

print("Template folder (relative):", app.template_folder)
print("Template folder (absolute):", os.path.join(app.root_path, app.template_folder))

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
