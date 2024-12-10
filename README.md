# CSE1-FINAL-DRILL

# PROJECT TITLE: Inventory control for sports centers.

## Description
A RESTful API designed to manage inventory, suppliers, activities, and inventory-supplier relationships for sports centers. The system enables CRUD operations for managing the inventory and its associated entities, ensuring efficient control and tracking.

## Installation
``` bash
pip install -r requirements.txt
```

## Configuration
To configure the database:
1. Upload the ```minimized_inventory_control_for_sports_centers``` MySQL database to your server or local machine.
2. Update the database configuration in the Flask app with your database connection details.

Environment variables needed:
- ```MYSQL_HOST=""``` : Your Host name
- ```MYSQL_USER=""``` : Your User name
- ```MYSQL_PASSWORD=""``` : Your Password
- ```MYSQL_DB=""``` : Your Database Name
- ```SECRET_KEY=""``` : Your Secret Key

## API Endpoints
## API Endpoints

| Endpoint                                     | Method   | Description                                    |
|---------------------------------------------|----------|------------------------------------------------|
| /api/inventory                              | GET      | List all inventory                            |
| /api/suppliers                              | GET      | List all suppliers                            |
| /api/activities                             | GET      | List all activities                           |
| /api/inventory_suppliers                    | GET      | List all inventory_suppliers                  |
| /api/add/inventory                          | POST     | Add items to inventory                        |
| /api/add/suppliers                          | POST     | Add items to suppliers                        |
| /api/add/activities                         | POST     | Add items to activities                       |
| /api/add/inventory_suppliers                | POST     | Add items to inventory_suppliers              |
| /api/delete/inventory/<int:item_code>       | DELETE   | Delete chosen item code number                |
| /api/delete/suppliers/<int:supplier_code>   | DELETE   | Delete chosen supplier code number            |
| /api/delete/activities/<int:activity_code>  | DELETE   | Delete chosen activity code number            |
| /api/delete/inventory_suppliers/<int:item_code> | DELETE   | Delete chosen item code number                |
| /api/update/inventory/<int:item_code>       | PUT      | Update chosen item code number                |
| /api/update/suppliers/<int:supplier_code>   | PUT      | Update chosen supplier code number            |
| /api/update/activities/<int:activity_code>  | PUT      | Update chosen activity code number            |
| /api/update/inventory_suppliers/<int:item_code> | PUT      | Update chosen item code number                |

## Testing
 Instructions for running tests:
 1. Install the Required Packages: ``` pip install -r requirements.txt ```
 2. Ensure your test file ```API_TEST.py``` is set up correctly.
 3. Run pytest from the Command Line ```pytest API_TEST.py```
## Git Commit Guidelines
Use conventional commits:
```bash
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add user registration tests
```
