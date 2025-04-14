from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

trainers = Blueprint('trainers', __name__)

#------------------------------------------------------------
# Retrieve workout plan for client
@trainers.route('/workout_plans/<clientID>', methods=['GET'])
def get_workout_plans(clientID):
    current_app.logger.info('GET /workout_plans/<clientID> route')
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM Workout_Plans WHERE Client_ID = {0}'.format(clientID)
    cursor.execute(query, (clientID))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

#-------------------------------------
# Add a new workout plan for a client
@trainers.route('/workout_plans/<clientID>', methods=['POST'])
def add_workout_plan(clientID):
    current_app.logger.info('POST /workout_plans/<clientID> route')
    workout_info = request.json
    trainer_id = workout_info['trainer_id']
    goal = workout_info['goal']
    exercise_list = workout_info['exercise_list']
    duration = workout_info['duration']

    query = '''
            INSERT INTO Workout_Plans (Client_ID, Trainer_ID, Goal, Exercise_List, Duration)
            VALUES (%s, %s, %s, %s, %s)
            '''
    data = (clientID, trainer_id, goal, exercise_list, duration)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'Workout plan added!'

#-------------------------------------
# Edit an existing workout plan for a client
@trainers.route('/workout_plans/<clientID>', methods=['PUT'])
def update_workout_plan(clientID):
    current_app.logger.info('PUT /workout_plans/<clientID> route')
    workout_info = request.json
    goal = workout_info['goal']
    exercise_list = workout_info['exercise_list']
    duration = workout_info['duration']

    query = '''
            UPDATE Workout_Plans
            SET Goal = %s, Exercise_List = %s, Duration = %s
            WHERE Client_ID = %s
            '''
    data = (goal, exercise_list, duration, clientID)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'Workout plan updated!'

#-------------------------------------
# Delete a workout plan for a client
@trainers.route('/workout_plans/<clientID>', methods=['DELETE'])
def delete_workout_plan(clientID):
    current_app.logger.info('DELETE /workout_plans/<clientID> route')
    cursor = db.get_db().cursor()
    query = 'DELETE FROM Workout_Plans WHERE Client_ID = {0}'.format(clientID)
    cursor.execute(query)
    db.get_db().commit()
    return 'Workout plan deleted!'

#------------------------------------------------------------
# Retrieve health metrics for a particular client
@trainers.route('/health_metrics/<clientID>', methods=['GET'])
def get_health_metrics(clientID):
    current_app.logger.info('GET /health_metrics/<clientID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM health_metrics WHERE client_id = %s', (clientID,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add health metrics for a particular client
@trainers.route('/health_metrics', methods=['POST'])
def add_health_metrics():
    current_app.logger.info('POST /health_metrics route')
    health_info = request.json
    user_id = health_info['user_id']
    heart_rate = health_info.get('heart_rate')
    calories_burned = health_info.get('calories_burned')
    sleep_duration = health_info.get('sleep_duration')
    blood_pressure = health_info.get('blood_pressure_level')
    water_intake = health_info.get('water_intake')
    caloric_intake = health_info.get('caloric_intake')
    body_fat = health_info.get('body_fat_percentage')

    query = '''
            INSERT INTO Health_Metrics (User_ID, Heart_Rate, Calories_Burned, Sleep_Duration,
                Blood_Pressure_Level, Water_Intake, Caloric_Intake, Body_Fat_Percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
    data = (user_id, heart_rate, calories_burned, sleep_duration,
              blood_pressure, water_intake, caloric_intake, body_fat)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'health metric added!'

#------------------------------------------------------------
# Update health metrics for a particular record
@trainers.route('/health_metrics/<recordID>', methods=['PUT'])
def update_health_metrics(recordID):
    current_app.logger.info('PUT /health_metrics/<recordID>')
    health_info = request.json
    heart_rate = health_info.get('heart_rate')
    calories_burned = health_info.get('calories_burned')
    sleep_duration = health_info.get('sleep_duration')
    blood_pressure = health_info.get('blood_pressure_level')
    water_intake = health_info.get('water_intake')
    caloric_intake = health_info.get('caloric_intake')
    body_fat = health_info.get('body_fat_percentage')

    query = '''
            UPDATE Health_Metrics
            SET Heart_Rate = %s, Calories_Burned = %s, Sleep_Duration = %s,
                Blood_Pressure_Level = %s, Water_Intake = %s,
                Caloric_Intake = %s, Body_Fat_Percentage = %s
            WHERE Record_ID = %s
            '''
    data = (heart_rate, calories_burned, sleep_duration,
              blood_pressure, water_intake, caloric_intake, body_fat, recordID)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'health metric updated successfully!'

# ----------------------------------------------
# Add a new training session for a client
@trainers.route('/training_session/<clientID>', methods=['POST'])
def add_training_session(clientID):
    current_app.logger.info('POST /training_session/<clientID> route')
    session_info = request.json
    trainer_id = session_info['trainer_id']
    status = session_info['status']
    date_time = session_info['date_time']
    description = session_info['class_description']
    max_participants = session_info.get('max_participants', 15)
    query = '''
            INSERT INTO Training_Session (Client_ID, Trainer_ID, Status, Date_time, Class_description, Max_participants)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
    data = (clientID, trainer_id, status, date_time, description, max_participants)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'training session created successfully!'

# ----------------------------------------------
# Cancel a training session for a client (by session ID)
@trainers.route('/training_session/<clientID>/<sessionID>', methods=['DELETE'])
def cancel_training_session(clientID, sessionID):
    current_app.logger.info('DELETE /training_session/<clientID>/<sessionID> route')
    query = '''DELETE FROM Training_Session WHERE Client_ID = %s AND Session_ID = %s'''
    data = (clientID, sessionID)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return f'training session {sessionID} for client {clientID} cancelled.'


# ----------------------------------------------
# Write a new message to a client
@trainers.route('/message/<clientID>', methods=['POST'])
def send_message_to_client(clientID):
    current_app.logger.info('POST /message/<clientID> route')
    message_info = request.json
    trainer_id = message_info['trainer_id']
    content = message_info['content']
    query = '''
            INSERT INTO Message (Content, Client_ID, Trainer_ID)
            VALUES (%s, %s, %s)
            '''
    data = (content, clientID, trainer_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'message sent to client.'########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
trainer = Blueprint('trainer', __name__)


#------------------------------------------------------------
# Get all resources the trainer has access to.
@trainer.route('/resources', methods=['GET'])
def get_resources():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT Resources_ID, Title, URL,
                    Type, Trainer_ID FROM Resources
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# This is a POST route for a trainer to add a new resource entry.
@trainer.route('/resources', methods=['POST'])
def add_new_resource():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    title = the_data['Title']
    url = the_data['URL']
    type = the_data['Type']
    trainer_id = the_data['Trainer_ID']
    
    query = f'''
        INSERT INTO Resources (Title,
                              URL,
                              Type, 
                              Trainer_ID)
        VALUES ('{title}', '{url}', '{type}', {trainer_id})
    '''
#------------------------------------------------------------

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
trainer = Blueprint('trainer', __name__)



#------------------------------------------------------------
# Get all resources the trainer has access to.
@trainer.route('/resources', methods=['GET'])
def get_resources():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT Resources_ID, Title, URL,
                    Type, Trainer_ID FROM Resources
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# ------------------------------------------------------------
# This is a POST route for a trainer to add a new resource entry.
@trainer.route('/resources', methods=['POST'])
def add_new_resource():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    title = the_data['Title']
    url = the_data['URL']
    type = the_data['Type']
    trainer_id = the_data['Trainer_ID']
    
    query = f'''
        INSERT INTO Resources (Title,
                              URL,
                              Type, 
                              Trainer_ID)
        VALUES ('{title}', '{url}', '{type}', {trainer_id})
    '''
#------------------------------------------------------------
