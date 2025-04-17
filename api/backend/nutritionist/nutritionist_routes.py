from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


nutritionist = Blueprint('nutritionist', __name__)


# Get all meal plans for a specific client
@nutritionist.route('/meal-plans/<int:client_id>', methods=['GET'])
def get_meal_plans(client_id):
    query = f"SELECT * FROM Meal_Plans WHERE User_ID = {client_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# Add a new meal plan for a specific client
@nutritionist.route('/meal-plans/<int:client_id>', methods=['POST'])
def add_meal_plan(client_id):
    data = request.json
    end_date = data['End_Date']
    query = f"INSERT INTO Meal_Plans (User_ID, End_Date) VALUES ({client_id}, '{end_date}')"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Meal plan created", 201)


# Update a specific meal plan for a client
@nutritionist.route('/meal-plans/<int:client_id>', methods=['PUT'])
def update_meal_plan(client_id):
    data = request.json
    plan_id = data['Plan_ID']
    fiber = data['Fiber_Goal']
    fat = data['Fat_Goal']
    carb = data['Carb_Goal']
    protein = data['Protein_Goal']
    calories = data['Calories']
    query = f"""
        UPDATE Meal_Plans
        SET Fiber_Goal = {fiber}, Fat_Goal = {fat}, Carb_Goal = {carb},
            Protein_Goal = {protein}, Calories = {calories}
        WHERE Plan_ID = {plan_id} AND User_ID = {client_id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Meal plan updated", 200)


# Delete a specific meal plan for a client
@nutritionist.route('/meal-plans/<int:client_id>', methods=['DELETE'])
def delete_meal_plan(client_id):
    plan_id = request.args.get('plan_id')
    query = f"DELETE FROM Meal_Plans WHERE Plan_ID = {plan_id} AND User_ID = {client_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Meal plan deleted", 200)


# Get all meal logs for a client
@nutritionist.route('/meals_logs/<int:client_id>', methods=['GET'])
def get_meal_logs(client_id):
    query = f"""
        SELECT ml.*, m.Name FROM Meal_Logs ml
        JOIN Meals m ON ml.Meal_ID = m.Meal_ID
        WHERE ml.User_ID = {client_id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# Get dietary restrictions for a client
@nutritionist.route('/restrictions/<int:client_id>', methods=['GET'])
def get_restrictions(client_id):
    query = f"""
        SELECT r.Restriction FROM Medical_Restriction r
        JOIN Medical_Record mr ON r.MedicalRecord_ID = mr.MedicalRecord_ID
        WHERE mr.Client_ID = {client_id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# Add a dietary restriction for a client
@nutritionist.route('/restrictions/<int:client_id>', methods=['POST'])
def add_restriction(client_id):
    data = request.json
    restriction = data['restriction']
    find_record = f"SELECT MedicalRecord_ID FROM Medical_Record WHERE Client_ID = {client_id}"
    cursor = db.get_db().cursor()
    cursor.execute(find_record)
    record = cursor.fetchone()
    if not record:
        return make_response("Medical record not found", 404)
    insert = f"INSERT INTO Medical_Restriction (MedicalRecord_ID, Restriction) VALUES ({record['MedicalRecord_ID']}, '{restriction}')"
    cursor.execute(insert)
    db.get_db().commit()
    return make_response("Restriction added", 201)


# Remove a dietary restriction for a client
@nutritionist.route('/restrictions/<int:client_id>', methods=['DELETE'])
def delete_restriction(client_id):
    restriction = request.args.get('restriction')
    find_record = f"SELECT MedicalRecord_ID FROM Medical_Record WHERE Client_ID = {client_id}"
    cursor = db.get_db().cursor()
    cursor.execute(find_record)
    record = cursor.fetchone()
    if not record:
        return make_response("Medical record not found", 404)
    delete = f"DELETE FROM Medical_Restriction WHERE MedicalRecord_ID = {record['MedicalRecord_ID']} AND Restriction = '{restriction}'"
    cursor.execute(delete)
    db.get_db().commit()
    return make_response("Restriction removed", 200)


# Get all available meals
@nutritionist.route('/meals', methods=['GET'])
def get_meals():
    query = "SELECT * FROM Meals"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# Add a new meal
@nutritionist.route('/restrictions/<client_id>', methods=['POST'])
def add_restriction(client_id):
    cursor = db.get_db().cursor()
    data = request.get_json()
    restriction = data.get("restriction")

    cursor.execute("SELECT MedicalRecord_ID FROM Medical_Record WHERE Client_ID = %s", (client_id,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("""
            INSERT INTO Medical_Record (Client_ID, Nutritionist_ID, Date_created)
            VALUES (%s, %s, NOW())
        """, (client_id, 1))
        db.get_db().commit()

        cursor.execute("SELECT MedicalRecord_ID FROM Medical_Record WHERE Client_ID = %s", (client_id,))
        result = cursor.fetchone()

    medical_record_id = result[0]

    cursor.execute("""
        INSERT INTO Medical_Restriction (MedicalRecord_ID, Restriction)
        VALUES (%s, %s)
    """, (medical_record_id, restriction))
    db.get_db().commit()

    return make_response(jsonify({"message": "Restriction added successfully"}), 201)



# Update an existing meal
@nutritionist.route('/meals', methods=['PUT'])
def update_meal():
    data = request.json
    meal_id = data['Meal_ID']
    name = data['Name']
    type_ = data['Type']
    recipe = data['Recipe']
    ingredients = data['Ingredients']
    query = f"""
        UPDATE Meals
        SET Name = '{name}', Type = '{type_}', Recipe = '{recipe}', Ingredients = '{ingredients}'
        WHERE Meal_ID = {meal_id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Meal updated", 200)


# Delete a meal
@nutritionist.route('/meals', methods=['DELETE'])
def delete_meal():
    meal_id = request.args.get('meal_id')
    query = f"DELETE FROM Meals WHERE Meal_ID = {meal_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Meal deleted", 200)
