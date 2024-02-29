from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import json
import os
import mysql.connector
import bcrypt
import getpass

app = Flask(__name__, template_folder='templates')
app.secret_key = '123456789'  # change this for new testing instances

#replace with your own info mysql+mysqlconnector://username:password@hostname:port/database_name.
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Exom2O01@localhost:3306/fitness"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Defines model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), primary_key=False)
    password = db.Column(db.String(255), nullable=False)
    userdata = db.Column(db.JSON)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Creates tables if they don't exist
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
# To get a database connection:
# db.session.execute("SELECT * FROM users")
'''
def get_db_connection():
    #password = getpass.getpass()
    db = mysql.connector.connect(
        host="localhost",  # replace with your host
        user="root",  # replace with your username
        password="Ex@m2O01",  # replace with your password
        database="fitness"  # replace with your database name
    )
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, userdata JSON, PRIMARY KEY (username))")
    return db

class User():
    db = get_db_connection()
    cursor = db.cursor()
    username=cursor.execute("SELECT * FROM users WHERE username=(username)")
    user_data = cursor.fetchone()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    def __init__(self, username):
        self.username = username
'''

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
        data = request.get_json()
        '''
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET userdata = %s WHERE username = %s", (json.dumps(data), session['username']))
        db.commit()
        '''
        user = User.query.filter_by(username=session['username']).first()
        user.userdata = data
        db.session.commit()
        return jsonify({'message': 'Thank you for completing the survey'}), 200

    return render_template('quiz.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        '''
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
        db.commit()
        newuser = User(request.form['username'])
        '''
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        '''
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        '''
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            session['loggedin'] = True
            #session['username'] = username
            return redirect(url_for('quiz'))
        
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')
    
@app.route('/profile/<username>')
@login_required
def profile(username):
    '''
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    user = session.get('username')
    '''
    user = User.query.filter_by(username=username).first()
    if User is None:
        return redirect(url_for('signup'))
    else:
        return render_template('profile.html', username=username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/thankyou')
def thankyou():
    return 'Thank you for completing the survey'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080',debug=True)
