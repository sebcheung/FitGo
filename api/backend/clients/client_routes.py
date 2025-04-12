########################################################
# Client blueprint 
########################################################

# Import libraries and modules
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
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

    # extract specific values
    total_weight = the_data['Total_Weight']
    total_time = the_data['Total_Time']
    
    query = f'''
        INSERT INTO Workout_Logs (User_ID,
                              Total_Weight, 
                              Total_Time)
        VALUES ({int(client_id)}, {int(total_weight)}, {int(total_time)})
    '''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added workout log")
    response.status_code = 201
    return response

#------------------------------------------------------------
# GET: Retrieve leaderboard position for {client_id}
@client_routes.route('/leaderboard/<client_id>', methods=['GET'])
def get_leaderboard_position(client_id):
    
    query = f'''
        SELECT Leaderboard_ID, 
               User_ID, 
               Username, 
               Ranks, 
               Total_Points, 
               Region, 
               Profile_Pic
        FROM Leaderboard
        WHERE User_ID = {str(client_id)}
    '''
    
    current_app.logger.info(f'GET /leaderboard/<client_id> query={query}')
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /leaderboard/<client_id> Result of query = {theData}')
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# POST: Add leaderboard position for {client_id}
@client_routes.route('/leaderboard/<client_id>', methods=['POST'])
def add_leaderboard_position(client_id):
    
    the_data = request.json
    current_app.logger.info(the_data)

    # extract values, use defaults for optional values
    username = the_data['Username']
    ranks = the_data.get('Ranks', None)
    total_points = the_data.get('Total_Points', 0)
    region = the_data.get('Region', 'UNKNOWN')
    profile_pic = the_data.get('Profile_Pic', None)

    query = f'''
        INSERT INTO Leaderboard (User_ID, Username, Ranks, Total_Points, Region, Profile_Pic)
        VALUES ('{client_id}', '{username}', '{ranks}', '{total_points}', '{region}', '{profile_pic}')
    '''

    current_app.logger.info(f'POST /leaderboard/<client_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added leaderboard position")
    response.status_code = 201
    return response

#------------------------------------------------------------
# PUT: Update leaderboard position for {client_id}
@client_routes.route('/leaderboard/<client_id>', methods=['PUT'])
def update_leaderboard_position(client_id):
    
    the_data = request.json
    current_app.logger.info(the_data)

    # update clause only for fields that are in the request
    update_fields = []
    if 'Username' in the_data: update_fields.append(f"Username = '{the_data['Username']}'")
    if 'Ranks' in the_data: update_fields.append(f"Ranks = '{the_data['Ranks']}'")
    if 'Total_Points' in the_data: update_fields.append(f"Total_Points = '{the_data['Total_Points']}'")
    if 'Region' in the_data: update_fields.append(f"Region = '{the_data['Region']}'")
    if 'Profile_Pic' in the_data: update_fields.append(f"Profile_Pic = '{the_data['Profile_Pic']}'")

    # invalid fields provided
    if not update_fields:
        response = make_response("No fields to update")
        response.status_code = 400
        return response

    update_clause = ', '.join(update_fields)
    query = f'''
        UPDATE Leaderboard
        SET {update_clause}
        WHERE User_ID = {str(client_id)}
    '''

    current_app.logger.info(f'PUT /leaderboard/<client_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully updated leaderboard position")
    response.status_code = 200
    return response

#------------------------------------------------------------
# GET: Retrieve reminders for {client_id}
@client_routes.route('/reminders/<client_id>', methods=['GET'])
def get_reminders(client_id):
    
    query = f'''
        SELECT Reminder_ID, 
               Creator_ID, 
               Duration, 
               Date, 
               Time
        FROM Reminders
        WHERE Creator_ID = {str(client_id)}
    '''
    
    current_app.logger.info(f'GET /reminders/<client_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reminders/<client_id> Result of query = {theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


#------------------------------------------------------------
# POST: Add a reminder for {client_id}
@client_routes.route('/reminders/<client_id>', methods=['POST'])
def add_reminder(client_id):
    the_data = request.json
    current_app.logger.info(the_data)

    # get the required and optional fields
    duration = the_data.get('Duration', None)
    date = the_data['Date']
    time = the_data['Time']

    query = f'''
        INSERT INTO Reminders (Creator_ID, Duration, Date, Time)
        VALUES ('{client_id}', {'NULL' if duration is None else duration}, '{date}', '{time}')
    '''

    current_app.logger.info(f'POST /reminders/<client_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added reminder")
    response.status_code = 201
    return response


#------------------------------------------------------------
# PUT: Update a reminder for {client_id}
@client_routes.route('/reminders/<client_id>/<reminder_id>', methods=['PUT'])
def update_reminder(client_id, reminder_id):
    
    the_data = request.json
    current_app.logger.info(the_data)

    # create update fields
    updates = []
    if 'Duration' in the_data:
        updates.append(f"Duration = {'NULL' if the_data['Duration'] is None else the_data['Duration']}")
    if 'Date' in the_data:
        updates.append(f"Date = '{the_data['Date']}'")
    if 'Time' in the_data:
        updates.append(f"Time = '{the_data['Time']}'")

    if not updates:
        response = make_response("No fields to update")
        response.status_code = 400
        return response

    update_clause = ', '.join(updates)
    query = f'''
        UPDATE Reminders
        SET {update_clause}
        WHERE Reminder_ID = {str(reminder_id)} AND Creator_ID = {str(client_id)}
    '''

    current_app.logger.info(f'PUT /reminders/<client_id>/<reminder_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully updated reminder")
    response.status_code = 200
    return response


#------------------------------------------------------------
# DELETE: Delete a reminder for {client_id}
@client_routes.route('/reminders/<client_id>/<reminder_id>', methods=['DELETE'])
def delete_reminder(client_id, reminder_id):
    
    query = f'''
        DELETE FROM Reminders
        WHERE Reminder_ID = {str(reminder_id)} AND Creator_ID = {str(client_id)}
    '''

    current_app.logger.info(f'DELETE /reminders/<client_id>/<reminder_id> query={query}')

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted reminder")
    response.status_code = 200
    return response
