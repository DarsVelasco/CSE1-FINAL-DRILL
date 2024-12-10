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

@app.route("/", methods=["GET"])
def welcome():
    return "Welcome to the Minimized Inventory Control for Sports Centers API!", 200


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
        cursor.execute("SELECT * FROM inventory WHERE item_code = %s", (item_code,))
        item = cursor.fetchone()

        if not item:
            return handle_error("Item not found", 404)

        cursor.execute("DELETE FROM inventory WHERE item_code = %s", (item_code,))
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

        if not item:
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

        if not item:
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

        if not item:
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

        if not item:
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