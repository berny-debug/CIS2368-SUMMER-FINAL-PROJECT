from flask import Flask, request, jsonify
from db import DBConnection, execute_read_query, execute_query
from creds import creds

app = Flask(__name__)

con = DBConnection(creds.connectionstring, creds.username, creds.password, creds.database)

LOGIN_USER = "admin"
LOGIN_PASS = "admin123"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if username == LOGIN_USER and password == LOGIN_PASS:
        return jsonify({"success": True, "message": "Login successful"}), 200
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/floors", methods=["GET"])
def get_floors():
    rows = execute_read_query(con, "SELECT id, level, name FROM floor ORDER BY id")
    return jsonify(rows), 200

@app.route("/floors/<int:floor_id>", methods=["GET"])
def get_floor(floor_id):
    rows = execute_read_query(con, "SELECT id, level, name FROM floor WHERE id = %s", (floor_id,))
    return jsonify(rows[0] if rows else {}), 200 if rows else 404

@app.route("/floors", methods=["POST"])
def create_floor():
    data = request.get_json(silent=True) or {}
    level = data.get("level")
    name = data.get("name")
    
    # Validate required fields
    if level is None or not name:
        return jsonify({"error": "Missing required fields: level, name"}), 400
    
    query = "INSERT INTO floor (level, name) VALUES (%s, %s)"
    params = (level, name)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Floor created"}), 201
    else:
        return jsonify({"error": "Failed to create floor"}), 500

@app.route("/floors/<int:floor_id>", methods=["PUT"])
def update_floor(floor_id):
    data = request.get_json(silent=True) or {}
    level = data.get("level")
    name = data.get("name")
    
    # Validate required fields
    if level is None or not name:
        return jsonify({"error": "Missing required fields: level, name"}), 400
    
    query = "UPDATE floor SET level = %s, name = %s WHERE id = %s"
    params = (level, name, floor_id)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Floor updated"}), 200
    else:
        return jsonify({"error": "Failed to update floor"}), 500

@app.route("/floors/<int:floor_id>", methods=["DELETE"])
def delete_floor(floor_id):
    query = "DELETE FROM floor WHERE id = %s"
    params = (floor_id,)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Floor deleted"}), 200
    else:
        return jsonify({"error": "Failed to delete floor"}), 500

@app.route("/rooms", methods=["GET"])
def get_rooms():
    rows = execute_read_query(con, "SELECT id, capacity, number, floor FROM room ORDER BY id")
    return jsonify(rows), 200

@app.route("/rooms/<int:room_id>", methods=["GET"])
def get_room(room_id):
    rows = execute_read_query(con, "SELECT id, capacity, number, floor FROM room WHERE id = %s", (room_id,))
    return jsonify(rows[0] if rows else {}), 200 if rows else 404

@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json(silent=True) or {}
    capacity = data.get("capacity")
    number = data.get("number")
    floor_id = data.get("floor")
    
    # Validate required fields
    if capacity is None or number is None or floor_id is None:
        return jsonify({"error": "Missing required fields: capacity, number, floor"}), 400
    
    # Validate floor exists
    floor_query = "SELECT level FROM floor WHERE id = %s"
    floor_result = execute_read_query(con, floor_query, (floor_id,))
    
    if not floor_result:
        return jsonify({"error": "Floor does not exist"}), 404
    
    floor_level = floor_result[0]['level']
    
    # Validate room number starts with floor level
    room_prefix = str(floor_level) if floor_level >= 0 else str(abs(floor_level))
    if not str(number).startswith(room_prefix):
        return jsonify({"error": f"Room number must start with floor level {floor_level}"}), 400
    
    query = "INSERT INTO room (capacity, number, floor) VALUES (%s, %s, %s)"
    params = (capacity, number, floor_id)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Room created"}), 201
    else:
        return jsonify({"error": "Failed to create room"}), 500

@app.route("/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data = request.get_json(silent=True) or {}
    capacity = data.get("capacity")
    number = data.get("number")
    floor_id = data.get("floor")
    
    # Validate required fields
    if capacity is None or number is None or floor_id is None:
        return jsonify({"error": "Missing required fields: capacity, number, floor"}), 400
    
    # Validate floor exists
    floor_query = "SELECT level FROM floor WHERE id = %s"
    floor_result = execute_read_query(con, floor_query, (floor_id,))
    
    if not floor_result:
        return jsonify({"error": "Floor does not exist"}), 404
    
    floor_level = floor_result[0]['level']
    
    # Validate room number starts with floor level
    room_prefix = str(floor_level) if floor_level >= 0 else str(abs(floor_level))
    if not str(number).startswith(room_prefix):
        return jsonify({"error": f"Room number must start with floor level {floor_level}"}), 400
    
    query = "UPDATE room SET capacity = %s, number = %s, floor = %s WHERE id = %s"
    params = (capacity, number, floor_id, room_id)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Room updated"}), 200
    else:
        return jsonify({"error": "Failed to update room"}), 500

@app.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    query = "DELETE FROM room WHERE id = %s"
    params = (room_id,)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Room deleted"}), 200
    else:
        return jsonify({"error": "Failed to delete room"}), 500

@app.route("/residents", methods=["GET"])
def get_residents():
    rows = execute_read_query(con, "SELECT id, firstname, lastname, age, room FROM resident ORDER BY id")
    return jsonify(rows), 200

@app.route("/residents/<int:resident_id>", methods=["GET"])
def get_resident(resident_id):
    rows = execute_read_query(con, "SELECT id, firstname, lastname, age, room FROM resident WHERE id = %s", (resident_id,))
    return jsonify(rows[0] if rows else {}), 200 if rows else 404

@app.route("/residents", methods=["POST"])
def create_resident():
    data = request.get_json(silent=True) or {}
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    age = data.get("age")
    room_id = data.get("room")
    
    # Validate required fields
    if not firstname or not lastname or age is None or room_id is None:
        return jsonify({"error": "Missing required fields: firstname, lastname, age, room"}), 400
    
    # Validate room exists
    room_query = "SELECT id FROM room WHERE id = %s"
    room_result = execute_read_query(con, room_query, (room_id,))
    
    if not room_result:
        return jsonify({"error": "Room does not exist"}), 404
    
    query = "INSERT INTO resident (firstname, lastname, age, room) VALUES (%s, %s, %s, %s)"
    params = (firstname, lastname, age, room_id)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Resident created"}), 201
    else:
        return jsonify({"error": "Failed to create resident"}), 500

@app.route("/residents/<int:resident_id>", methods=["PUT"])
def update_resident(resident_id):
    data = request.get_json(silent=True) or {}
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    age = data.get("age")
    room_id = data.get("room")
    
    # Validate required fields
    if not firstname or not lastname or age is None or room_id is None:
        return jsonify({"error": "Missing required fields: firstname, lastname, age, room"}), 400
    
    # Validate room exists
    room_query = "SELECT id FROM room WHERE id = %s"
    room_result = execute_read_query(con, room_query, (room_id,))
    
    if not room_result:
        return jsonify({"error": "Room does not exist"}), 404
    
    query = "UPDATE resident SET firstname = %s, lastname = %s, age = %s, room = %s WHERE id = %s"
    params = (firstname, lastname, age, room_id, resident_id)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Resident updated"}), 200
    else:
        return jsonify({"error": "Failed to update resident"}), 500

@app.route("/residents/<int:resident_id>", methods=["DELETE"])
def delete_resident(resident_id):
    query = "DELETE FROM resident WHERE id = %s"
    params = (resident_id,)
    success = execute_query(con, query, params)
    
    if success:
        return jsonify({"message": "Resident deleted"}), 200
    else:
        return jsonify({"error": "Failed to delete resident"}), 500

if __name__ == "__main__":
    app.run(debug=True)
