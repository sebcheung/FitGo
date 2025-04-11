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
    
    # Another example of logging for debugging purposes.
    # You can see if the data you're getting back is what you expect. 
    current_app.logger.info(f'GET /workout_log/<client_id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response