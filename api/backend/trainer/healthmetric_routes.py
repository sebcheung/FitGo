from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

health_metrics = Blueprint('health_metrics', __name__)

#------------------------------------------------------------
# Retrieve health metrics for a particular client
@health_metrics.route('/health_metrics/<clientID>', methods=['GET'])
def get_health_metrics(clientID):
    current_app.logger.info(f'GET /health_metrics/{clientID} route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM health_metrics WHERE client_id = %s', (clientID,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add health metrics for a particular client
@health_metrics.route('/health_metrics', methods=['POST'])
def add_health_metrics():
    current_app.logger.info('POST /health_metrics route')
    health_info = request.json
    client_id = health_info['user_id']
    height = health_info['height']
    weight = health_info['weight']
    blood_pressure = health_info['blood_pressure']
    heart_rate = health_info['heart_rate']
    body_fat_percentage = health_info['body_fat_percentage']

    # Insert new health metrics into the database
    query = '''INSERT INTO health_metrics (client_id, height, weight, blood_pressure, heart_rate, body_fat_percentage)
               VALUES (%s, %s, %s, %s, %s, %s)'''
    data = (client_id, height, weight, blood_pressure, heart_rate, body_fat_percentage)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    return make_response(jsonify({"message": "Health metrics added successfully"}), 201)