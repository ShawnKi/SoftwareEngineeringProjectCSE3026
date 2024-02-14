from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector
import getpass

# Create the Flask application and specify the templates directory
app = Flask(__name__, template_folder='templates')
def get_db_connection():
    #password = getpass.getpass()
    db = mysql.connector.connect(
        host="LAPTOP-0FMGT87M",  # replace with your host
        user="shawn",  # replace with your username
        password="root",  # replace with your password
        database="mysql"  # replace with your database name
    )
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255))")
    return db



# Get the absolute path of the templates directory
templates_dir_abs = os.path.join(app.root_path, app.template_folder)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        db.commit()
        print(username, password)
        
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
       
        password = request.form['password']
        print(username,password)
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
        
        user = cursor.fetchone()
        print(user)
        if user:
            if user[1] == password:  # In a real application, make sure to hash and salt passwords
                print("correct password")
                return redirect(url_for('success'))
            else:
                print("wrong password")
                return 'Wrong password'
        else:
            print('Username not found')
            return 'Username not found'
    else:
        return render_template('login.html')

@app.route('/success')
def success():
    return 'Logged in successfully'
if __name__ == "__main__":

    app.run(host='localhost', port='8080',debug=True)
