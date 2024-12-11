from flask import Flask, jsonify, request
from http import HTTPStatus
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'minimized_inventory_control_for_sports_centers'
app.config['SECRET_KEY'] = 'darwin'
mysql = MySQL(app)

USER_DATA_FILE = 'users.json'

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)

# Error handling
def handle_error(message, status_code):
    return jsonify({"success": False, "error": message}), status_code

@app.route("/", methods=["GET"])
def welcome():
    return "Welcome to the Inventory Control for Sports Centers API!", HTTPStatus.OK

# JWT ROLES
def create_jwt(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_jwt(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Security
def token_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return handle_error('Token is missing', HTTPStatus.UNAUTHORIZED)

            token = token.split(" ")[1] if " " in token else token
            payload = verify_jwt(token)
            if not payload:
                return handle_error('Token is invalid or expired', HTTPStatus.UNAUTHORIZED)

            if roles and payload['role'] not in roles:
                return handle_error('You do not have permission to access this resource', HTTPStatus.FORBIDDEN)

            request.user = payload
            return f(*args, **kwargs)

        return decorated_function

    return decorator

def load_users():
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

# Authentication Register and Login
@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not email or not password or not role:
            return handle_error("Email, password, and role are required", HTTPStatus.BAD_REQUEST)

        users = load_users()
        if email in users:
            return handle_error("User already exists", HTTPStatus.BAD_REQUEST)

        hashed_password = generate_password_hash(password)
        users[email] = {
            "password": hashed_password,
            "role": role
        }
        save_users(users)

        return jsonify({"success": True, "message": "User registered successfully"}), HTTPStatus.CREATED
    except Exception as e:
        return handle_error(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return handle_error("Email and password are required", HTTPStatus.BAD_REQUEST)

        users = load_users()
        user = users.get(email)

        if user and check_password_hash(user["password"], password):
            token = create_jwt(email, user["role"])
            return jsonify({"success": True, "token": token}), HTTPStatus.OK

        return handle_error("Invalid email or password", HTTPStatus.UNAUTHORIZED)
    except Exception as e:
        return handle_error(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

#GET METHODS
@app.route("/api/inventory", methods=["GET"])
@token_required(roles=["admin"])
def get_inventory():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Inventory")
        inventory_items = cursor.fetchall()

        if not inventory_items:
            return handle_error("No inventory items found", 404)

        inventory_list = [
            {
                "item_code": item[0],
                "item_description": item[1],
                "item_type_name": item[2],
                "quantity_in_stock": item[3],
                "reorder_level": item[4],
            }
            for item in inventory_items
        ]

        return jsonify({"success": True, "data": inventory_list, "total": len(inventory_list)}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/suppliers", methods=["GET"])
@token_required(roles=["admin" , "user"])
def get_suppliers():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Suppliers")
        suppliers = cursor.fetchall()

        if not suppliers:
            return handle_error("No suppliers found", 404)

        suppliers_list = [
            {
                "supplier_code": supplier[0],
                "supplier_name": supplier[1],
                "supplier_phone": supplier[2],
            }
            for supplier in suppliers
        ]

        return jsonify({"success": True, "data": suppliers_list, "total": len(suppliers_list)}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/activities", methods=["GET"])
@token_required(roles=["admin", "user"])
def get_activities():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Activities")
        activities = cursor.fetchall()

        if not activities:
            return handle_error("No activities found", 404)

        activities_list = [
            {
                "activity_code": activity[0],
                "activity_description": activity[1],
                "item_code": activity[2],
                "average_monthly_usage": activity[3],
            }
            for activity in activities
        ]

        return jsonify({"success": True, "data": activities_list, "total": len(activities_list)}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/inventory_suppliers", methods=["GET"])
@token_required(roles=["admin"])
def get_inventory_suppliers():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM inventory_suppliers")
        inventory_suppliers = cursor.fetchall()

        if not inventory_suppliers:
            return handle_error("No activities found", 404)

        inventory_suppliers_list = [
            {
                "item_code": inventory_supplier[0],
                "supplier_code": inventory_supplier[1],
            }
            for inventory_supplier in inventory_suppliers
        ]

        return jsonify({"success": True, "data": inventory_suppliers_list, "total": len(inventory_suppliers_list)}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
#POST METHODS
@app.route("/api/add/inventory", methods=["POST"])
@token_required(roles=["admin"])
def create_inventory():
    try:
        data = request.get_json()
        required_fields = ["item_code", "item_description", "item_type_name", "quantity_in_stock", "reorder_level"]

        for field in required_fields:
            if field not in data:
                return handle_error(f"Missing required field: {field}", 400)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Inventory (item_code, item_description, item_type_name, quantity_in_stock, reorder_level)
            VALUES (%s, %s, %s, %s, %s)
        """, (data["item_code"], data["item_description"], data["item_type_name"], data["quantity_in_stock"], data["reorder_level"]))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "Inventory item created successfully"}), 201
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/add/suppliers", methods=["POST"])
@token_required(roles=["admin", "user"])
def create_supplier():
    try:
        data = request.get_json()
        required_fields = ["supplier_code", "supplier_name", "supplier_phone"]

        for field in required_fields:
            if field not in data:
                return handle_error(f"Missing required field: {field}", 400)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Suppliers (supplier_code, supplier_name, supplier_phone)
            VALUES (%s, %s, %s)
        """, (data["supplier_code"], data["supplier_name"], data["supplier_phone"]))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "Supplier created successfully"}), 201
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/add/activities", methods=["POST"])
@token_required(roles=["admin"])
def create_activity():
    try:
        data = request.get_json()
        required_fields = ["activity_code", "activity_description", "item_code", "average_monthly_usage"]

        for field in required_fields:
            if field not in data:
                return handle_error(f"Missing required field: {field}", 400)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Activities (activity_code, activity_description, item_code, average_monthly_usage)
            VALUES (%s, %s, %s, %s)
        """, (data["activity_code"], data["activity_description"], data["item_code"], data["average_monthly_usage"]))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "Activity created successfully"}), 201
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/add/inventory_suppliers", methods=["POST"])
@token_required(roles=["admin"])
def create_inventory_supplier():
    try:
        data = request.get_json()
        required_fields = ["item_code", "supplier_code"]

        for field in required_fields:
            if field not in data:
                return handle_error(f"Missing required field: {field}", 400)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO inventory_suppliers (item_code, supplier_code)
            VALUES (%s, %s)
        """, (data["item_code"], data["supplier_code"]))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "Inventory supplier created successfully"}), 201
    except Exception as e:
        return handle_error(str(e), 500)

# DELETE METHODS
@app.route("/api/delete/inventory/<int:item_code>", methods=["DELETE"])
def delete_inventory_item(item_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE item_code = %s", (item_code))
        item = cursor.fetchone()

        if cursor.rowcount == 0:
            return handle_error("Item not found", 404)

        cursor.execute("DELETE FROM inventory WHERE item_code = %s", (item_code))
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Item with code {item_code} deleted successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)

@app.route("/api/delete/suppliers/<int:supplier_code>", methods=["DELETE"])
def delete_suppliers_item(supplier_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE supplier_code = %s", (supplier_code,))
        item = cursor.fetchone()

        if cursor.rowcount == 0:
            return handle_error("Item not found", 404)

        cursor.execute("DELETE FROM suppliers WHERE supplier_code = %s", (supplier_code,))
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Item with code {supplier_code} deleted successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/delete/activities/<int:activity_code>", methods=["DELETE"])
def delete_activities_item(activity_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM activities WHERE activity_code = %s", (activity_code,))
        item = cursor.fetchone()

        if cursor.rowcount == 0:
            return handle_error("Item not found", 404)

        cursor.execute("DELETE FROM activities WHERE activity_code = %s", (activity_code,))
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Item with code {activity_code} deleted successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
@app.route("/api/delete/inventory_suppliers/<int:item_code>", methods=["DELETE"])
def delete_inventory_suppliers_item(item_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM inventory_suppliers WHERE item_code = %s", (item_code,))
        item = cursor.fetchone()

        if cursor.rowcount == 0:
            return handle_error("Item not found", 404)

        cursor.execute("DELETE FROM inventory_suppliers WHERE item_code = %s", (item_code,))
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Item with code {item_code} deleted successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)
    
#UPDATE METHODS
@app.route("/api/update/inventory/<int:item_code>", methods=["PUT"])
def update_inventory_item(item_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Inventory WHERE item_code = %s", (item_code,))
        item = cursor.fetchone()

        if not item:
            return handle_error("Item not found", 404)

        data = request.get_json()

        if not data:
            return handle_error("No data provided for update", 400)

        update_query = """
        UPDATE Inventory 
        SET item_description = %s, item_type_name = %s, quantity_in_stock = %s, reorder_level = %s 
        WHERE item_code = %s
        """
        values = (
            data.get("item_description", item[1]),  
            data.get("item_type_name", item[2]),
            data.get("quantity_in_stock", item[3]),
            data.get("reorder_level", item[4]),
            item_code
        )

        cursor.execute(update_query, values)
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Item with code {item_code} updated successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)

@app.route("/api/update/suppliers/<int:supplier_code>", methods=["PUT"])
def update_suppliers_item(supplier_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Suppliers WHERE supplier_code = %s", (supplier_code,))
        item = cursor.fetchone()

        if not item:
            return handle_error("Item not found", 404)

        data = request.get_json()

        if not data:
            return handle_error("No data provided for update", 400)

        update_query = """
        UPDATE Suppliers 
        SET supplier_name = %s, supplier_phone = %s 
        WHERE supplier_code = %s
        """
        values = (
            data.get("supplier_name", item[1]),  
            data.get("supplier_phone", item[2]),
            supplier_code
        )

        cursor.execute(update_query, values)
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Supplier with code {supplier_code} updated successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)

@app.route("/api/update/activities/<int:activity_code>", methods=["PUT"])
def update_activities_item(activity_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Activities WHERE activity_code = %s", (activity_code,))
        item = cursor.fetchone()

        if cursor.rowcount == 0:
            return handle_error("Item not found", 404)

        data = request.get_json()

        if not data:
            return handle_error("No data provided for update", 400)

        update_query = """
        UPDATE Activities 
        SET activity_description = %s, item_code = %s, average_monthly_usage = %s 
        WHERE activity_code = %s
        """
        values = (
            data.get("activity_description", item[1]),  
            data.get("item_code", item[2]),
            data.get("average_monthly_usage", item[3]),
            activity_code
        )

        cursor.execute(update_query, values)
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Activity with code {activity_code} updated successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)

@app.route("/api/update/inventory_suppliers/<int:item_code>", methods=["PUT"])
def update_inventory_suppliers_item(item_code):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM inventory_suppliers WHERE item_code = %s", (item_code,))
        item = cursor.fetchone()

        if not item:
            return handle_error("Item not found", 404)

        data = request.get_json()

        if not data:
            return handle_error("No data provided for update", 400)

        update_query = """
        UPDATE inventory_suppliers 
        SET supplier_code = %s
        WHERE item_code = %s
        """
        values = (
            data.get("supplier_code", item[1]), 
            item_code
        )

        cursor.execute(update_query, values)
        mysql.connection.commit()

        return jsonify({"success": True, "message": f"Inventory supplier record with item code {item_code} updated successfully"}), 200
    except Exception as e:
        return handle_error(str(e), 500)

if __name__ == "__main__":
    app.run(debug=True)