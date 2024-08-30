import requests
import json
from datetime import datetime

today = datetime.now()

date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")


GENDER = "female"
WEIGHT_KG = "65"
HEIGHT_CM = "165"
AGE = "35"

APP_ID = "171548f2"
API_KEY = "285679641d41c1ab9b131cfa691fd831"

nutrional_enpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/18c68a80643d1af4c188152fbc30390b/workoutTracking/workouts"

headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}


exercise_text = input("Tell me which exercise you did: ")

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=nutrional_enpoint, json=parameters, headers=headers)
response.raise_for_status()

exercise_data = json.loads(response.text)
exercises = exercise_data['exercises']
# print(exercise_data["exercises"][0]['user_input'])
# print(exercise_data["exercises"][0]['duration_min'])
# print(exercise_data["exercises"][0]['nf_calories'])

# for exercise in exercises:
#     print(exercise['user_input'])
#     print(exercise['duration_min'])
#     print(exercise['nf_calories'])

sheet_headers = {
    "Authorization": "Basic a29raWxhOlNhcmFueWFANg=="
}
for exercise in exercises:    
    workout_parameters = {
        'workout': {
            'date': date,
            'time': time,
            'name': exercise['user_input'],
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories'] 
        }
    }



    sheet_response = requests.post(url=sheet_endpoint, json=workout_parameters,headers=sheet_headers)

# Check if the request was successful
if sheet_response.status_code == 200:
    # Parse the JSON response
    data = sheet_response.json()
    
    # Do something with the data
    print(data['workout'])
else:
    # Print the error if something went wrong
    print(f"Request failed with status code {sheet_response.status_code}")
