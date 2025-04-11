########################################################
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

