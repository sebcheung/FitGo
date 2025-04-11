from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

client_routes = Blueprint('client_routes', __name__)

#------------------------------------------------------------
# GET: Retrieve the workout log for {client_id}
@client_routes.route('/workout_log/<client_id>', methods=['GET'])
def get_workout_log(client_id):

    query = f'''SELECT WorkoutLog_ID, 
                       User_ID, 
                       Total_Weight, 
                       Total_Time 
                FROM Workout_Logs 
                WHERE User_ID = {str(client_id)}
    '''
    
    current_app.logger.info(f'GET /workout_log/<client_id> query={query}')

    # get the database connection, execute the query, and 
    # fetch the results as a Python Dictionary
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    # Check if data received is what is expected.
    current_app.logger.info(f'GET /workout_log/<client_id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# POST: Add a new workout log for {client_id}
@client_routes.route('/workout_log/<client_id>', methods=['POST'])
def add_workout_log(client_id):
    
    # collect data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    total_weight = the_data['Total_Weight']
    total_time = the_data['Total_Time']
    
    query = f'''
        INSERT INTO Workout_Logs (User_ID,
                              Total_Weight, 
                              Total_Time)
        VALUES ('{client_id}', '{total_weight}', '{total_time}')
    '''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added workout log")
    response.status_code = 201
    return response