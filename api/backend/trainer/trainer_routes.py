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