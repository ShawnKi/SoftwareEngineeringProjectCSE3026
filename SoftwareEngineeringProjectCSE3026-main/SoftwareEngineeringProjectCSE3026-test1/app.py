from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import json
import bcrypt
import pymysql
import sqlalchemy
from flask_migrate import Migrate
import os


# from google.cloud.sql.connector import Connector


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)  # change this for new testing instances

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
    picture = db.Column(db.String(255))
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

#Format: "Exercise":[["Primary Muscles"],["Secondary Muscles"],["Equipment"],["Complexity"]]
exercises = {
    "Push-ups": [["Chest", "Triceps"], ["Shoulders"], ["Bodyweight"], ["Beginner"]],
    "Sit-ups": [["Abs"], [], ["Bodyweight"], ["Beginner"]],
    "Squats": [["Quadriceps", "Glutes"], ["Hamstrings", "Calves"], ["Bodyweight"], ["Beginner"]],
    "Lunges": [["Quadriceps", "Glutes"], ["Hamstrings"], ["Bodyweight"], ["Beginner"]],
    "Plank": [["Abs"], ["Lower back"], ["Bodyweight"], ["Beginner"]],
    "Bench Press": [["Chest", "Triceps"], ["Shoulders"], ["Barbell"], ["Intermediate"]],
    "Deadlift": [["Hamstrings", "Glutes"], ["Lower back", "Forearms"], ["Barbell"], ["Intermediate"]],
    "Pull-ups": [["Back", "Biceps"], [], ["Bodyweight"], ["Intermediate"]],
    "Overhead Press": [["Shoulders", "Triceps"], [], ["Dumbbell"], ["Intermediate"]],
    "Barbell Row": [["Back", "Biceps"], [], ["Barbell"], ["Intermediate"]],
    "Bicep Curls": [["Biceps"], [], ["Dumbbell"], ["Beginner"]],
    "Tricep Dips": [["Triceps"], [], ["Bodyweight"], ["Beginner"]],
    "Leg Press": [["Quadriceps", "Glutes"], ["Hamstrings"], ["Machine"], ["Beginner"]],
    "Lat Pulldown": [["Back"], ["Biceps"], ["Machine"], ["Beginner"]],
    "Flyes": [["Chest"], [], ["Dumbbell"], ["Beginner"]],
    "Lateral Raises": [["Shoulders"], [], ["Dumbbell"], ["Beginner"]],
    "Crunches": [["Abs"], [], ["Bodyweight"], ["Beginner"]],
    "Leg Curls": [["Hamstrings"], [], ["Machine"], ["Beginner"]],
    "Calf Raises": [["Calves"], [], ["Bodyweight", "Dumbbell"], ["Beginner"]],
    "Mountain Climbers": [["Abs"], ["Quadriceps"], ["Bodyweight"], ["Intermediate"]],
    "Pistol Squats": [["Quadriceps", "Glutes"], ["Hamstrings", "Calves"], ["Bodyweight"], ["Advanced"]],
    "Muscle-ups": [["Back", "Biceps", "Chest", "Triceps"], ["Shoulders"], ["Pull-up bar"], ["Advanced"]],
    "Handstand Push-ups": [["Shoulders", "Triceps"], ["Chest"], ["Bodyweight"], ["Advanced"]],
    "Turkish Get-ups": [["Shoulders"], ["Core", "Glutes", "Legs"], ["Kettlebell"], ["Advanced"]],
    "Dragon Flags": [["Abs"], [], ["Bodyweight"], ["Advanced"]],
    "One Arm Push-ups": [["Chest", "Triceps"], ["Shoulders"], ["Bodyweight"], ["Advanced"]],
    "Front Lever Raises": [["Back", "Abs"], ["Biceps"], ["Pull-up bar"], ["Advanced"]],
    "Planche Push-ups": [["Chest", "Triceps"], ["Shoulders", "Back"], ["Bodyweight"], ["Advanced"]]
}


def calculate_workout_recomendations(username):
    user = User.query.filter_by(username=username).first()
    equipment=user.userdata["equipment"]
    
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        answers = session.get('answers', {})
        data = request.get_json()
        # Update the answers with the data from the current POST request
        answers.update({'quiz_results': data})
        user = User.query.get(session.get('_user_id'))
        user.userdata=answers
        #print(data)
        flag_modified(user, 'userdata')
        session['answers'] = answers
        #print(user.userdata)
        try:
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()  
            print("Commit failed: ", e)
        return jsonify({'message': 'Data received successfully!'})

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
        return redirect(url_for('quiz'))
        
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
    user = User.query.get(session.get('_user_id'))
    if request.method == 'POST':
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        email = request.form['inputEmailAddress']
        username = request.form['inputUsername']
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        db.session.commit()
    return render_template('profile.html', username=username)

@app.route('/pfp', methods=['POST'])
@login_required
def pfp():
    user = User.query.get(session.get('_user_id'))
    data = request.json
    image_url = data.get('image_url')

    if image_url:
        user.picture = image_url
        db.session.commit()  # Save changes to the database
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid image URL"}), 400

@app.route('/results/<username>')
def results(username):
    user = User.query.get(session.get('_user_id'))
    print("Userdata:",user.userdata)
    return render_template('results.html', username=username)

@app.route('/workouts/<username>', methods=['GET', 'POST'])
@login_required
def workouts(username):
    
    if request.method == 'POST':
        data = request.json
        exercise_name = data['name']
        action = data['action']
        answers = session.get('answers', {})
        print("Answers now", answers)
        # Ensure userdata is initialized
        if 'workouts' not in answers:
            workouts = []
        else:
            workouts = answers['workouts']
            
        if action == "add":
            if exercise_name not in workouts:
                workouts.append(exercise_name)
        elif action == "remove":
            if exercise_name in workouts:
                workouts.remove(exercise_name)
        
        # Reassign userdata to ensure changes are detected
        answers.update({'workouts': workouts})
        session['answers'] = answers
        print(answers)
        user = User.query.get(session.get('_user_id'))
        user.userdata=answers
        flag_modified(user, 'userdata')
        try:
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()  
            print("Commit failed: ", e)
        
       
        
        return jsonify({"status": "success", "message": f"Successfully {action}ed {exercise_name} for {username}."})
    user = User.query.filter_by(username=username).first()
    workouts = user.userdata.get('workouts', [])

    return render_template('workouts.html', username=username, workouts=workouts)

@app.route('/schedule/<username>', methods=['GET', 'POST'])
@login_required
def schedule(username):
    if request.method=='POST':
        #Takes in the data as a dictionary
        data = request.json
        print("made it here")
        print(data) 
        answers = session.get('answers', {})
        answers.update({'schedule': data})
        user = User.query.get(session.get('_user_id'))
        user.userdata=answers
        flag_modified(user, 'userdata')
        session['answers'] = answers
        try:
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()  
            print("Commit failed: ", e)
        return jsonify({'message': 'Data received successfully!'})
    
    user = User.query.filter_by(username=username).first()
    weekData = user.userdata.get('schedule', {})
    workoutInput=user.userdata.get('workouts', [])
    return render_template('schedule.html', username=username, weekData=jsonify(weekData).data.decode('utf-8'), workoutInput=workoutInput)

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
    app.run(debug=True)
