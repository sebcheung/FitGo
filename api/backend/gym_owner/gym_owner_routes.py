########################################################
# Gym owner blueprint of endpoints 
# NEED TO TEST TO SEE HOW TO HANDLE DATETIME VARIABLES
########################################################

# Import libraries and modules
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Initialize blueprint object
gym_owner = Blueprint('gym-owner', __name__)

# Create route to get employee roster
@gym_owner.route('/employees', methods=['GET'])
def get_employees():
    current_app.logger.info(f'GET /gym-owner/employees route')
    cursor = db.get_db().cursor()
    query = ''' SELECT *
                FROM Employee
                ORDER BY Employee_ID ASC; '''
    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Create route to get client roster
@gym_owner.route('/clients', methods=['GET'])
def get_clients():
    current_app.logger.info(f'GET /gym-owner/clients route')
    cursor = db.get_db().cursor()
    query = ''' SELECT *
                FROM Client
                ORDER BY Client_ID ASC; '''
    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Create route to get a list of all equipment from a specific gym 
@gym_owner.route('/equipments/<gym_id>', methods=['GET'])
def get_equipment(gym_id):
    current_app.logger.info(f'GET /gym-owner/equipments/{gym_id} route')
    cursor = db.get_db().cursor()
    query = ''' SELECT Equipment_ID, Name, Type, Brand, Purchase_Date, Status
                FROM Equipment
                WHERE Gym_ID = %s '''
    data = (gym_id)
    cursor.execute(query, data)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Create route to get a list of attendees at each event
@gym_owner.route('/events', methods=['GET'])
def get_participants():
    current_app.logger.info(f'GET /gym-owner/events route')
    cursor = db.get_db().cursor()
    query = ''' SELECT e.Event_ID, e.Event_Name, e.Event_Date, e.Host_Name, COUNT(ea.Client_ID) AS Attendees
                FROM Event e 
                    JOIN Event_Attendee ea ON e.Event_ID = ea.Event_ID
                GROUP BY e.event_id, e.event_name
                ORDER BY COUNT(ea.Client_ID) DESC '''
    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Create route to add a new employee to the roster
@gym_owner.route('/employees', methods = ['POST'])
def add_employee():
    the_data = request.json
    current_app.logger.info(the_data)

    boss_id = the_data['Boss_ID']
    first = the_data['FirstName']
    last = the_data['LastName']
    age = the_data['Age']
    ssn = the_data['SSN']
    address = the_data['Address']
    hire_date = the_data['Hire_Date']

    query = f''' INSERT INTO Employee (Boss_ID, FirstName, LastName, Age, SSN, Address, Hire_Date)
                 VALUES ({int(boss_id)}, '{first}', '{last}', {int(age)}, '{ssn}', '{address}', {hire_date});
            '''
  
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added employee!")
    response.status_code = 200
    return response

# Create route to add a new client to the roster
@gym_owner.route('/clients', methods = ['POST'])
def add_client():
    the_data = request.json
    current_app.logger.info(the_data)

    first = the_data['FirstName']
    last = the_data['LastName']
    email = the_data['Email']
    sex = the_data['Sex']
    age = the_data['Age']
    weight = the_data['Weight']
    height = the_data['Height']
    phone = the_data['Phone']
    join_date = the_data['Join_Date']
        
    query = f''' INSERT INTO Client (FirstName, LastName, Email, Sex, Age, Weight, Height, Phone_Number, Join_Date)
                 VALUES ('{first}', '{last}', '{email}', '{sex}', {int(age)}, {int(weight)}, {float(height)}, '{phone}', '{join_date}')
            '''
  
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added client!")
    response.status_code = 200
    return response

# Create route to add a new event
@gym_owner.route('/events', methods = ['POST'])
def add_event():
    the_data = request.json
    current_app.logger.info(the_data)

    location = the_data['Event_Location']
    description = the_data['Event_Description']
    host_name = the_data['Host_Name']
    sponsor = the_data['Sponsor']
    start_time = the_data['Start_Time']
    event_name = the_data['Event_Name']
    date = the_data['Event_Date']
        
    query = f''' INSERT INTO Event (Event_Location, Event_Description, Host_Name, Sponsor, Start_Time, Event_Name, Event_Date)
                 VALUES ('{location}', '{description}', '{host_name}', '{sponsor}', '{start_time}', '{event_name}', '{date}')

            '''
  
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added event!")
    response.status_code = 200
    return response


# Create route to add a new piece of equipment
@gym_owner.route('/equipments', methods = ['POST'])
def add_equipment():
    the_data = request.json
    current_app.logger.info(the_data)

    gym_id = the_data['Gym_ID']
    type = the_data['Type']
    purchase_date = the_data['Purchase_Date']
    name = the_data['Name']
    status = the_data['Status']
    brand = the_data['Brand']
        
    query = f''' INSERT INTO Equipment (Gym_ID, Type, Purchase_Date, Name, Status, Brand)
                 VALUES ({int(gym_id)}, '{type}', '{purchase_date}', '{name}', {int(status)}, '{brand}');
             '''
  
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added piece of equipment!")
    response.status_code = 200
    return response

# Create route to update data for a specific employee
@gym_owner.route('/employees', methods = ['PUT'])
def update_employee():
    current_app.logger.info('PUT /gym-owner/employees route')
    emp_info = request.json
    emp_id = emp_info['Employee_ID']
    boss_id = emp_info['Boss_ID']
    first = emp_info['FirstName']
    last = emp_info['LastName']
    age = emp_info['Age']
    address = emp_info['Address']


    query = ''' UPDATE Employee 
                SET Boss_ID = %s, FirstName = %s, LastName = %s, Age = %s, Address = %s
                WHERE Employee_ID = %s '''
    data = (boss_id, first, last, age, address, emp_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Employee Record Updated!'

# Create route to update data for a specific client
@gym_owner.route('/clients', methods = ['PUT'])
def update_client():
    current_app.logger.info('PUT /gym-owner/clients route')
    client_info = request.json
    client_id = client_info['Client_ID']
    first = client_info['FirstName']
    last = client_info['LastName']
    email = client_info['Email']
    sex = client_info['Sex']
    age = client_info['Age']
    weight = client_info['Weight']
    height = client_info['Height']
    phone = client_info['Phone_Number']


    query = ''' UPDATE Client 
                SET FirstName = %s, LastName = %s, Email = %s, Sex = %s, Age = %s, Weight = %s, Height = %s, Phone_Number = %s
                WHERE Client_ID = %s '''
    data = (first, last, email, sex, age, weight, height, phone, client_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Client Record Updated!'

# Create route to update status for a specific piece of equipment
@gym_owner.route('/equipments', methods = ['PUT'])
def update_equipment():
    current_app.logger.info('PUT /gym-owner/equipments route')
    equip_info = request.json
    equip_id = equip_info['Equipment_ID']
    gym_id = equip_info['Gym_ID']
    status = equip_info['Status']

    query = ''' UPDATE Equipment 
                SET Status = %s
                WHERE Equipment_ID = %s AND Gym_ID = %s'''
    data = (status, equip_id, gym_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Equipment Status Updated!'

# Create route to delete an employee from the roster
@gym_owner.route('/employees/<employee_id>', methods = ['DELETE'])
def delete_employee(employee_id):
    current_app.logger.info(f'DELETE /gym-owner/employees/{employee_id} route')
    query = 'DELETE FROM Employee WHERE Employee_ID = %s'
    data = (employee_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return f'Employee {employee_id} deleted!'

# Create route to delete a client from the roster
@gym_owner.route('/clients/<client_id>', methods = ['DELETE'])
def delete_client(client_id):
    current_app.logger.info(f'DELETE /gym-owner/clients/{client_id} route')
    query = 'DELETE FROM Client WHERE Client_ID = %s'
    data = (client_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return f'Client {client_id} deleted!'

# Create route to delete an event 
@gym_owner.route('/events/<event_id>', methods = ['DELETE'])
def delete_event(event_id):
    current_app.logger.info(f'DELETE /gym-owner/events/{event_id} route')
    query = 'DELETE FROM Event WHERE Event_ID = %s'
    data = (event_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return f'Event {event_id} deleted!'

