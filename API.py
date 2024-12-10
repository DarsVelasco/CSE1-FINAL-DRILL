from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from http import HTTPStatus

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'minimized_inventory_control_for_sports_centers'

mysql = MySQL(app)

# Error handling
def handle_error(message, status_code):
    return jsonify({"success": False, "error": message}), status_code

#GET METHODS
@app.route("/api/inventory", methods=["GET"])
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
def create_activity():
    try:
        data = request.get_json()
        required_fields = ["activity_code", "activity_description", "item_code", "average_monthly_usage"]

        # Check for missing fields
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
def create_inventory_supplier():
    try:
        data = request.get_json()
        required_fields = ["item_code", "supplier_code"]

        # Check for missing fields
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


if __name__ == "__main__":
    app.run(debug=True)