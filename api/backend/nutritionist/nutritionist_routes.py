from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

nutritionist = Blueprint('nutritionist', __name__)


# GET meal plans for a client
@nutritionist.route('/meal-plans/<client_id>', methods=['GET'])
def get_meal_plans(client_id):
    query = f'''
        SELECT * FROM meal_plans WHERE client_id = {client_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# POST a new meal plan
@nutritionist.route('/meal-plans/<client_id>', methods=['POST'])
def create_meal_plan(client_id):
    the_data = request.json
    name = the_data['name']
    description = the_data['description']

    query = f'''
        INSERT INTO meal_plans (client_id, name, description)
        VALUES ({client_id}, '{name}', '{description}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added meal plan")
    response.status_code = 201
    return response

# PUT (update) a meal plan
@nutritionist.route('/meal-plans/<client_id>', methods=['PUT'])
def update_meal_plan(client_id):
    the_data = request.json
    plan_id = the_data['plan_id']
    name = the_data['name']
    description = the_data['description']

    query = f'''
        UPDATE meal_plans
        SET name = '{name}', description = '{description}'
        WHERE id = {plan_id} AND client_id = {client_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully updated meal plan")
    response.status_code = 200
    return response

@nutritionist.route('/meal-plans/<client_id>', methods=['DELETE'])
def delete_meal_plan(client_id):
    plan_id = request.args.get('plan_id')

    query = f'''
        DELETE FROM meal_plans WHERE id = {plan_id} AND client_id = {client_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted meal plan")
    response.status_code = 200
    return response

# GET meal logs for a client
@nutritionist.route('/meals_logs/<client_id>', methods=['GET'])
def get_meal_logs(client_id):
    query = f'''
        SELECT * FROM meal_logs WHERE client_id = {client_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# GET client restrictions
@nutritionist.route('/restrictions/<client_id>', methods=['GET'])
def get_restrictions(client_id):
    query = f'''
        SELECT * FROM restrictions WHERE client_id = {client_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# POST a new restriction
@nutritionist.route('/restrictions/<client_id>', methods=['POST'])
def add_restriction(client_id):
    the_data = request.json
    restriction = the_data['restriction']

    query = f'''
        INSERT INTO restrictions (client_id, restriction)
        VALUES ({client_id}, '{restriction}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added restriction")
    response.status_code = 201
    return response

# DELETE a restriction
@nutritionist.route('/restrictions/<client_id>', methods=['DELETE'])
def delete_restriction(client_id):
    restriction = request.args.get('restriction')

    query = f'''
        DELETE FROM restrictions WHERE client_id = {client_id}
        AND restriction = '{restriction}'
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted restriction")
    response.status_code = 200
    return response

# GET all meals
@nutritionist.route('/meals', methods=['GET'])
def get_meals():
    query = '''
        SELECT * FROM meals
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# POST a new meal
@nutritionist.route('/meals', methods=['POST'])
def add_meal():
    the_data = request.json
    name = the_data['name']
    ingredients = the_data['ingredients']

    query = f'''
        INSERT INTO meals (name, ingredients)
        VALUES ('{name}', '{ingredients}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added meal")
    response.status_code = 201
    return response

# PUT (update) a meal
@nutritionist.route('/meals', methods=['PUT'])
def update_meal():
    the_data = request.json
    meal_id = the_data['meal_id']
    name = the_data['name']
    ingredients = the_data['ingredients']

    query = f'''
        UPDATE meals SET name = '{name}', ingredients = '{ingredients}'
        WHERE id = {meal_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully updated meal")
    response.status_code = 200
    return response

# DELETE a meal
@nutritionist.route('/meals', methods=['DELETE'])
def delete_meal():
    meal_id = request.args.get('meal_id')

    query = f'''
        DELETE FROM meals WHERE id = {meal_id}
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted meal")
    response.status_code = 200
    return response

