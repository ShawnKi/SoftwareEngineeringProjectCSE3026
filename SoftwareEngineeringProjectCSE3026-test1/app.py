from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import json
import bcrypt
import pymysql
import sqlalchemy
from flask_migrate import Migrate


# from google.cloud.sql.connector import Connector


app = Flask(__name__)
app.config["SECRET_KEY"] = '1234567899'  # change this for new testing instances

db_user = 'dbuser'
db_pass = 'dbuser'
db_name = 'users'
cloud_sql_connection_name = 'awesome-flash-416102:us-central1:fitness-app-db'

host = '/cloudsql/{}'.format(cloud_sql_connection_name)
db_public_ip = '34.29.30.210'
db_port = 3306
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_pass}@{db_public_ip}:{db_port}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# Defines model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    userdata = db.Column(db.JSON)

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Creates tables if they don't exist
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the user's answers from the session
        answers = session.get('answers', {})

        # Update the answers with the data from the current POST request
        answers.update(request.get_json())

        session['answers'] = answers
        print(answers)
        user = User.query.get(session.get('_user_id'))
        user.userdata = answers
        db.session.commit()
        return jsonify({'message': 'Thank you for completing the survey!'}), 200
        return jsonify({'message': 'Your answer has been saved'}), 200

    return render_template('quiz.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return render_template('quiz.html')
        
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            session['loggedin'] = True
            #session['username'] = username
            return render_template('profile.html', username=username)
        
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')
    
@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        email = request.form['inputEmailAddress']
        username = request.form['inputUsername']
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
    
    return render_template('profile.html', username=username)

@app.route('/results/<username>')
def results(username):
    user = User.query.filter_by(username=username).first()
    return render_template('results.html', username=username)

@app.route('/logout')
def logout():
    logout_user()
    response = make_response(redirect(url_for("index")))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/thankyou')
def thankyou():
    return 'Thank you for completing the survey'

if __name__ == "__main__":
    app.run()
