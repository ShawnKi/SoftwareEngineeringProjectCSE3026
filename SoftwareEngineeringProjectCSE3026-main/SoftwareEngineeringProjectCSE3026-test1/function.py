def sets_rep_calculation(bodytype, goal):
    rest = "1 minute" 
    reps = ""
    if bodytype == "Ectomorph":
        if goal == "Get fit":
            reps = "8-10"
            rest = "1 minute 30 seconds" 
        elif goal == "Lose weight" :
            reps = "13"
        elif goal == "Build muscle":
            reps = "3-5"
            rest =  "2 minutes"
    elif bodytype == "Endomorph":
        if goal == "Get fit":
            reps = "8-10"
            rest = "1 minute 30 seconds" 
        elif goal == "Lose weight":
            reps = "12-14"
        elif goal == "Build muscle":
            reps = "3-5"
            rest =  "2 minutes"
    elif bodytype == "Mesomorph":
        if goal == "Get fit":
            reps = "9"
            rest = "1 minute 30 seconds" 
        elif goal == "Lose weight":
            reps = "12"
        elif goal == "Build muscle":
            reps = "3-6"
            rest =  "2 minutes" 
    sets = 3  # All body types and goals have the same default number of sets
    return reps, sets, rest

def update_workout_plan(data,exerfreq):
    if not any(data.values()): 
        if exerfreq == "Twice a week":
            data.update({'tuesday':UpperBodyStrength})
            data.update({'friday':LowerBodyStrength})
        elif exerfreq == "Three times a week":
            data.update({'tuesday':FullBody})
            data.update({'thursday':UpperBodyStrength})
            data.update({'friday':LowerBodyStrength})
        elif exerfreq == "4-5 times a week":
            data.update({'monday': ChestandTricep})
            data.update({'tuesday': BackandBicep})
            data.update({'wednesday':LegsandShoulders})
            data.update({'friday': CardioandCore})
                
    return data

#endomorph
ChestandTricep = [{'name': 'BenchPress', 'reps': '10', 'sets': '3', 'type': 'ChestTricep', 'image': 'http://127.0.0.1:5000/static/images/BenchPress.jpg'}, 
                {'name': 'Incline BenchPress', 'reps': '12', 'sets': '4', 'type': 'ChestTricep', 'image': 'http://127.0.0.1:5000/static/images/InclineBenchPress.jpg'},
                {'name': 'Chest Flyes', 'reps': '12', 'sets': '3', 'type': 'Chest', 'image': 'http://127.0.0.1:5000/static/images/ChestFlyes.jpg'},
                {'name': 'Tricep Dips', 'reps': '10', 'sets': '3', 'type': 'Triceps', 'image': 'http://127.0.0.1:5000/static/images/TricepDips.jpg'}]
BackandBicep = [{'name': 'Deadlift', 'reps': '8', 'sets': '4', 'type': 'Core', 'image': 'http://127.0.0.1:5000/static/images/Deadlift.jpg'},
                {'name': 'Bent Over Rows', 'reps': '8', 'sets': '3', 'type': 'Back', 'image': 'http://127.0.0.1:5000/static/images/BentOverRows.jpg'}, 
                {'name': 'Lat Pulldowns', 'reps': '12', 'sets': '3', 'type': 'Back', 'image': 'http://127.0.0.1:5000/static/images/LatPulldowns.jpg'}, 
                {'name': 'Bicep Curls', 'reps': '10', 'sets': '3', 'type': 'BackBicep', 'image': 'http://127.0.0.1:5000/static/images/BicepCurls.jpg'}, 
                {'name': 'Hammer Curl', 'reps': '12(each side)', 'sets': '4', 'type': 'Biceps', 'image': 'http://127.0.0.1:5000/static/images/HammerCurl.jpg'}]
LegsandShoulders = [{'name': 'Squat', 'reps': '10', 'sets': '3', 'type': 'Legs', 'image': 'http://127.0.0.1:5000/static/images/Squat.jpg'}, 
                    {'name': 'Barbell Lunges', 'reps': '10', 'sets': '3', 'type': 'Legs', 'image': 'http://127.0.0.1:5000/static/images/BarbellLunge.jpg'}, 
                    {'name': 'Leg Press', 'reps': '10', 'sets': '3', 'type': 'Quads', 'image': 'http://127.0.0.1:5000/static/images/LegPress.jpg'}, 
                    {'name': 'Shoulder Press', 'reps': '12', 'sets': '3', 'type': 'Shoulders', 'image': 'http://127.0.0.1:5000/static/images/ShoulderPress.jpg'}, 
                    {'name': 'Lateral Raises', 'reps': '15', 'sets': '3', 'type': 'Shoulders', 'image': 'http://127.0.0.1:5000/static/images/LateralRaises.jpg'}]
CardioandCore = [{'name': 'Plank', 'reps': '1 minutes', 'sets': '3', 'type': 'BackBicep', 'image': 'http://127.0.0.1:5000/static/images/Plank.jpg'},
                 {'name': 'Russian Twists', 'reps': '10(each side)', 'sets': '3', 'type': 'Core', 'image': 'http://127.0.0.1:5000/static/images/RussianTwists.jpg'},
                 {'name': 'Bicycle Crunches', 'reps': '10(each side)', 'sets': '3', 'type': 'Core', 'image': 'http://127.0.0.1:5000/static/images/BicycleCrunches.jpg'},
                 {'name': 'Leg Raises', 'reps': '10', 'sets': '3', 'type': 'Core', 'image': 'http://127.0.0.1:5000/static/images/LegRaises.jpg'}]

FullBody = [{'name': 'Squat', 'reps': '10', 'sets': '3', 'type': 'Legs', 'image': 'http://127.0.0.1:5000/static/images/Squat.jpg'}, 
            {'name': 'Deadlift', 'reps': '8', 'sets': '4', 'type': 'Core', 'image': 'http://127.0.0.1:5000/static/images/Deadlift.jpg'},
            {'name': 'BenchPress', 'reps': '10', 'sets': '3', 'type': 'ChestTricep', 'image': 'http://127.0.0.1:5000/static/images/BenchPress.jpg'},
            {'name': 'Bent Over Rows', 'reps': '8', 'sets': '3', 'type': 'Back', 'image': 'http://127.0.0.1:5000/static/images/BentOverRows.jpg'}, 
            {'name': 'Overhead Press', 'reps': '8', 'sets': '3', 'type': 'Shoulders', 'image': 'http://127.0.0.1:5000/static/images/OverheadPress.jpg'},
            {'name': 'Plank', 'reps': '1 minutes', 'sets': '3', 'type': 'BackBicep', 'image': 'http://127.0.0.1:5000/static/images/Plank.jpg'}]
UpperBodyStrength = [{'name': 'PullUp', 'reps': '12', 'sets': '4', 'type': 'BackBicep', 'image': 'http://127.0.0.1:5000/static/images/PullUp.jpg'}, 
                     {'name': 'Lat Pulldowns', 'reps': '12', 'sets': '3', 'type': 'Back', 'image': 'http://127.0.0.1:5000/static/images/LatPulldowns.jpg'},
                     {'name': 'BenchPress', 'reps': '10', 'sets': '3', 'type': 'ChestTricep', 'image': 'http://127.0.0.1:5000/static/images/BenchPress.jpg'}, 
                     {'name': 'Shoulder Press', 'reps': '12', 'sets': '3', 'type': 'Shoulders', 'image': 'http://127.0.0.1:5000/static/images/ShoulderPress.jpg'}, 
                     {'name': 'Tricep Dips', 'reps': '10', 'sets': '3', 'type': 'Triceps', 'image': 'http://127.0.0.1:5000/static/images/TricepDips.jpg'}, 
                     {'name': 'Bicep Curls', 'reps': '10', 'sets': '3', 'type': 'BackBicep', 'image': 'http://127.0.0.1:5000/static/images/BicepCurls.jpg'}]
LowerBodyStrength = [{'name': 'Squat', 'reps': '10', 'sets': '3', 'type': 'Legs', 'image': 'http://127.0.0.1:5000/static/images/Squat.jpg'},
                     {'name': 'Romanian Deadlift', 'reps': '8', 'sets': '3', 'type': 'Hamstrings', 'image': 'http://127.0.0.1:5000/static/images/RomanianDeadlift.jpg'}, 
                     {'name': 'Barbell Lunges', 'reps': '10', 'sets': '3', 'type': 'Legs', 'image': 'http://127.0.0.1:5000/static/images/BarbellLunge.jpg'}, 
                     {'name': 'Leg Press', 'reps': '10', 'sets': '3', 'type': 'Quads', 'image': 'http://127.0.0.1:5000/static/images/LegPress.jpg'}, 
                     {'name': 'Calf Raise', 'reps': '16', 'sets': '3', 'type': 'Calves', 'image': 'http://127.0.0.1:5000/static/images/CalfRaise.jpg'}]
#mesomorph
no_equip = ["Push-ups","Pull-ups","Lunges","Squats"]
dumbell = ["Push-ups","Bicep Curls","Dumbbell Bench Press","Lateral Raises"]
gym = ["Barbell Row","Lat Pulldown","Bicep Curls","Romanian Deadlift"]