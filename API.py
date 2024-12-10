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