import pytest
from API import app  

@pytest.fixture
def mock_db(mocker):
    mock_conn = mocker.patch('flask_mysqldb.MySQL.connection')
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_cursor

# Test the root endpoint
def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Inventory Control for Sports Centers API!" in response.data

# Tests for Inventory
def test_get_inventory_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/inventory')
    
    assert response.status_code == 404
    assert b"No inventory items found" in response.data

def test_get_inventory_success(mock_db):
    mock_db.fetchall.return_value = [
        (1, "Ball", "Sports Equipment", 20, 5)
    ]
    
    client = app.test_client()
    response = client.get('/api/inventory')
    
    assert response.status_code == 200
    assert b"Ball" in response.data
    assert b"Sports Equipment" in response.data

def test_post_inventory_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/inventory', json={}) 
    
    assert response.status_code == 400
    assert b"Missing required field" in response.data

def test_post_inventory_success(mock_db):
    mock_db.rowcount = 1  
    
    client = app.test_client()
    response = client.post('/api/add/inventory', json={
        "item_code": 1,
        "item_description": "Basketball",
        "item_type_name": "Sports Equipment",
        "quantity_in_stock": 50,
        "reorder_level": 10
    })
    
    assert response.status_code == 201
    assert b"Inventory item created successfully" in response.data

# Tests for Suppliers
def test_get_suppliers_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/suppliers')
    
    assert response.status_code == 404
    assert b"No suppliers found" in response.data

def test_get_suppliers_success(mock_db):
    mock_db.fetchall.return_value = [
        (1, "ABC Supplies", "123-456-7890")
    ]
    
    client = app.test_client()
    response = client.get('/api/suppliers')
    
    assert response.status_code == 200
    assert b"ABC Supplies" in response.data
    assert b"123-456-7890" in response.data

def test_post_supplier_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/suppliers', json={}) 
    
    assert response.status_code == 400
    assert b"Missing required field" in response.data

def test_post_supplier_success(mock_db):
    mock_db.rowcount = 1  
    
    client = app.test_client()
    response = client.post('/api/add/suppliers', json={
        "supplier_code": 1,
        "supplier_name": "XYZ Supplies",
        "supplier_phone": "987-654-3210"
    })
    
    assert response.status_code == 201
    assert b"Supplier created successfully" in response.data

# Delete and Update Tests
def test_delete_inventory_not_found(mock_db):
    mock_db.rowcount = 0
    
    client = app.test_client()
    response = client.delete('/api/delete/inventory/999')
    
    assert response.status_code == 404
    assert b"Item not found" in response.data

def test_delete_inventory_success(mock_db):
    mock_db.rowcount = 1  
    
    client = app.test_client()
    response = client.delete('/api/delete/inventory/1')
    
    assert response.status_code == 200
    assert b"Item with code 1 deleted successfully" in response.data

def test_update_inventory_not_found(mock_db):
    mock_db.rowcount = 0  
    
    client = app.test_client()
    response = client.put('/api/update/inventory/999', json={})
    
    assert response.status_code == 400
    assert b"No data provided for update" in response.data

def test_update_inventory_success(mock_db):
    mock_db.rowcount = 1  
    
    client = app.test_client()
    response = client.put('/api/update/inventory/1', json={
        "item_description": "Updated Basketball",
        "quantity_in_stock": 60
    })
    
    assert response.status_code == 200
    assert b"Item with code 1 updated successfully" in response.data

# Tests for Activities
def test_update_activity_not_found(mock_db):
    mock_db.rowcount = 0 
    
    client = app.test_client()
    response = client.put('/api/update/activities/999', json={})
    
    assert response.status_code == 404
    assert b"Item not found" in response.data

def test_update_activity_success(mock_db):
    mock_db.rowcount = 1 
    
    client = app.test_client()
    response = client.put('/api/update/activities/1', json={
        "activity_description": "Updated Soccer Match",
        "item_code": 101,
        "average_monthly_usage": 25
    })
    
    assert response.status_code == 200
    assert b"Activity with code 1 updated successfully" in response.data


def test_delete_activity_not_found(mock_db):
    mock_db.rowcount = 0 
    
    client = app.test_client()
    response = client.delete('/api/delete/activities/999')
    
    assert response.status_code == 404
    assert b"Item not found" in response.data

def test_delete_activity_success(mock_db):
    mock_db.rowcount = 1 
    
    client = app.test_client()
    response = client.delete('/api/delete/activities/1')
    
    assert response.status_code == 200
    assert b"Item with code 1 deleted successfully" in response.data

def test_get_inventory_suppliers_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/inventory_suppliers')
    
    assert response.status_code == 404
    assert b"No inventory-supplier relationships found" in response.data


# Tests for Inventory-Supplier Relationships
def test_get_inventory_suppliers_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/inventory_suppliers')
    
    assert response.status_code == 404
    assert b"No activities found" in response.data  

def test_get_inventory_suppliers_success(mock_db):
    mock_db.fetchall.return_value = [
        (1, 101)
    ]
    
    client = app.test_client()
    response = client.get('/api/inventory_suppliers')
    
    assert response.status_code == 200
    assert b"1" in response.data
    assert b"101" in response.data

def test_post_inventory_supplier_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/inventory_suppliers', json={}) 
    
    assert response.status_code == 400
    assert b"Missing required field" in response.data

def test_post_inventory_supplier_success(mock_db):
    mock_db.rowcount = 1 
    
    client = app.test_client()
    response = client.post('/api/add/inventory_suppliers', json={
        "item_code": 1,
        "supplier_code": 101 
    })
    
    assert response.status_code == 201
    assert b"Inventory supplier created successfully" in response.data


if __name__ == "__main__":
    pytest.main()
