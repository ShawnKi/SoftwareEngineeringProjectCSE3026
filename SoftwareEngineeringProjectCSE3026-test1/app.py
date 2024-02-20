from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
import mysql.connector
import bcrypt
import getpass

app = Flask(__name__, template_folder='templates')
app.secret_key = '123456'  # change this for new testing instances

def get_db_connection():
    #password = getpass.getpass()
    db = mysql.connector.connect(
        host="LAPTOP-0FMGT87M",  # replace with your host
        user="shawn",  # replace with your username
        password="root",  # replace with your password
        database="mysql"  # replace with your database name
    )
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, userdata JSON, PRIMARY KEY (username))")
    return db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json()
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET userdata = %s WHERE username = %s", (json.dumps(data), session['username']))
        db.commit()
        return jsonify({'message': 'Thank you for completing the survey'}), 200

    return render_template('quiz.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
        db.commit()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['username'] = username
            return redirect(url_for('quiz'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/thankyou')
def thankyou():
    return 'Thank you for completing the survey'

if __name__ == "__main__":
    app.run(host='localhost', port='8080',debug=True)
