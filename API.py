from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from http import HTTPStatus

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'minimized_inventory_control_for_sports_centers'

mysql = MySQL(app)

def handle_error(message, status_code):
    return jsonify({"success": False, "error": message}), status_code

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