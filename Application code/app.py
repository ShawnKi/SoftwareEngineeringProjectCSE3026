#Authors: Ariana Sanchez, Melissa Fusco, Cameron Rhea, Shawn Kingman, Hongrong Zhong
#This file manages the backend of our website, such as loading html pages and managing user data.
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import json
import bcrypt
import pymysql
import sqlalchemy
from flask_migrate import Migrate
from function import *
import os
from datetime import date
import calendar
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)  # change this for new testing instances

# get db info from injected environment variables
db_user = os.environ.get("DB_USER") 
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("DB_CONN_NAME")

host = '/cloudsql/{}'.format(cloud_sql_connection_name)
db_public_ip = os.environ.get("DB_IP")
db_port = 3306
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_pass}@{db_public_ip}:{db_port}/{db_name}" #db connection string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# Defines model
class User(db.Model, UserMixin):
    __tablename__ = db_name
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
        self.picture="pfp.png"
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


# Creates tables if they don't exist
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Format: "Exercise":[["Primary Muscles"],["Secondary Muscles"],["Equipment"],["Complexity"]]
#NOT USED IN CURRENT VERSION
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

    
    

@app.route('/')
def index():
    return render_template('index.html')

#Renders the workout page for non-logged in users. 
@app.route('/workout_lean')
def workout_lean():
    return render_template('workout_lean.html')


#Gets the quiz results and adds them to the userdata
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
        print(data)
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
        login_user(new_user) #logs in new user before they take the quiz
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
            session['answers'] = user.userdata #Sets the session answers to be correct for the user.
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

#returns the results of the quiz.
@app.route('/results/<username>')
def results(username):
    user = User.query.get(session.get('_user_id'))
    #print("Userdata:",user.userdata)
    return render_template('results.html', username=username)

#Shows the workouts page for the logged in user
@app.route('/workouts/<username>', methods=['GET', 'POST'])
@login_required
def workouts(username):
    
    if request.method == 'POST':
        data = request.json
        exercise_name = data['name']
        action = data['action']
        answers = session.get('answers', {})
        print("Answers now", answers)
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

#The schedule page for logged in users. 
@app.route('/schedule/<username>', methods=['GET', 'POST'])
@login_required
def schedule(username):
    
    if request.method=='POST':
        data = request.json
        print(data)
        print({'message': 'generate schedule'})
        if 'message' in data: #if the user clicked auto generate schedule
            user = User.query.get(session.get('_user_id'))
            user = User.query.filter_by(username=username).first()
            
            quiz_res = user.userdata.get('quiz_results', {})  
            exercisefreq = quiz_res['exerciseFrequency'] 
            print("made it here") 
            datas = {
                "monday": [],
                "tuesday": [],
                "wednesday": [],
                "thursday": [],
                "friday": [],
                "saturday": [],
                "sunday": []
            }
            datas = update_workout_plan(datas,exercisefreq) #Generates workout plan based off user quiz results.
            print(datas)

            answers = session.get('answers', {})
            answers.update({'schedule': datas})
            user.userdata=answers
            flag_modified(user, 'userdata')
            session['answers'] = answers
            try:
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()  
                print("Commit failed: ", e)
            return jsonify({"reload": True}), 200
        else: #if the user presses save changes
            user = User.query.get(session.get('_user_id'))
            user = User.query.filter_by(username=username).first()
             
            answers = session.get('answers', {})
            answers.update({'schedule': data})
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

@app.route('/planning/<username>',methods=['GET']) #gets the planning page for the specific day 
@login_required
def planning(username):
    user = User.query.get(session.get('_user_id'))
    user = User.query.filter_by(username=username).first()
    quiz_res = user.userdata.get('quiz_results', {}) 
    print(quiz_res)
    bodyt = quiz_res['bodyType']
    goals = quiz_res['goal']  
    equipmenthave = quiz_res['equipment'] 
    # workouts = user.userdata.get('workouts', [])
    exercises =[]
    rep,sets,rest = sets_rep_calculation(bodyt,goals)  
    
    weekData = user.userdata.get('schedule', {})
    print(weekData) 
    if bool(weekData) :
        my_date = date.today()
        today = calendar.day_name[my_date.weekday()]  #Today's date
        today_workout = weekData[today.lower()] 
        s = rep
        r = rest
        
        for x in today_workout:        
            if x['name'] == 'Plank':
                rep = x['reps']
                rest = '30 seconds'            
            info = {"name":x['name'], "sets": sets, "reps": rep, "rest": rest} 
            exercises.append(info)
            rep = s 
            rest = r 
    # If no workouts, provide default exercises
    if not any(weekData) : 
        if 'Dumbbells' in equipmenthave:
            for x in dumbell:         
                info = {"name":x, "sets": sets, "reps": rep, "rest": rest}
                exercises.append(info)
                break
        elif 'Barbell' or 'Kettlebell' in equipmenthave:
            for x in gym:           
                info = {"name":x, "sets": sets, "reps": rep, "rest": rest}
                exercises.append(info)
                break
        for x in no_equip:           
                info = {"name":x, "sets": sets, "reps": rep, "rest": rest}
                exercises.append(info)
                
                
    return render_template('planning.html', exercises=exercises)

#Clears the session data on logout and ensures that pressing the back key will not log the user back in. 
@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    response = make_response(redirect(url_for("index")))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=8080, debug=True)
