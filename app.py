from flask import Flask, render_template

app = Flask(__name__)


@app.route('/templates')
def index():
    return render_template('index.html')


@app.route('/templates')
def about():
    return render_template('about.html')


@app.route('/templates')
def quiz():
    return render_template('quiz.html')


@app.route('/templates')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    print("Starting application")
    app.run(debug=True)
