import pytest
from unittest import mock
from API import app 

@pytest.fixture
def mock_db(mocker):
    mock_conn = mocker.patch('flask_mysqldb.MySQL.connection')
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_cursor

# Inventory tests
def test_get_inventory_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/inventory')
    
    assert response.status_code == 404
    assert b"No inventory items found" in response.data

def test_get_inventory(mock_db):
    mock_db.fetchall.return_value = [(1, 'Football', 'Sports Equipment', 100, 10)]
    
    client = app.test_client()
    response = client.get('/api/inventory')
    
    assert response.status_code == 200
    assert b"Football" in response.data
    assert b"Sports Equipment" in response.data

def test_get_single_item_not_found(mock_db):
    mock_db.fetchone.return_value = None
    
    client = app.test_client()
    response = client.get('/api/inventory/999')
    
    assert response.status_code == 404
    assert b"Item not found" in response.data

def test_get_single_item(mock_db):
    mock_db.fetchone.return_value = (1, 'Football', 'Sports Equipment', 100, 10)
    
    client = app.test_client()
    response = client.get('/api/inventory/1')
    
    assert response.status_code == 200
    assert b"Football" in response.data

def test_create_inventory_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/inventory', json={})
    
    assert response.status_code == 400
    assert b"Missing required field: item_code" in response.data

def test_create_inventory_success(mock_db):
    mock_db.rowcount = 1
    
    client = app.test_client()
    response = client.post('/api/add/inventory', json={
        'item_code': 101, 'item_description': 'Basketball', 'item_type_name': 'Sports Equipment',
        'quantity_in_stock': 50, 'reorder_level': 5
    })
    
    assert response.status_code == 201
    assert b"Inventory item created successfully" in response.data

def test_delete_inventory_item_not_found(mock_db):
    mock_db.fetchone.return_value = None
    
    client = app.test_client()
    response = client.delete('/api/delete/inventory/999')
    
    assert response.status_code == 404
    assert b"Item not found" in response.data

def test_delete_inventory_item_success(mock_db):
    mock_db.fetchone.return_value = (1, 'Football', 'Sports Equipment', 100, 10)
    mock_db.rowcount = 1
    
    client = app.test_client()
    response = client.delete('/api/delete/inventory/1')
    
    assert response.status_code == 200
    assert b"Item with code 1 deleted successfully" in response.data

def test_update_inventory_item_not_found(mock_db):
    mock_db.fetchone.return_value = None
    
    client = app.test_client()
    response = client.put('/api/update/inventory/999', json={'item_description': 'Updated'})
    
    assert response.status_code == 404
    assert b"Item not found" in response.data

def test_update_inventory_item_success(mock_db):
    mock_db.fetchone.return_value = (1, 'Football', 'Sports Equipment', 100, 10)
    mock_db.rowcount = 1
    
    client = app.test_client()
    response = client.put('/api/update/inventory/1', json={'item_description': 'Updated Football'})
    
    assert response.status_code == 200
    assert b"Item with code 1 updated successfully" in response.data

# Suppliers tests
def test_get_suppliers_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/suppliers')
    
    assert response.status_code == 404
    assert b"No suppliers found" in response.data

def test_get_suppliers(mock_db):
    mock_db.fetchall.return_value = [(1, 'SportsCo', '123-456-7890')]
    
    client = app.test_client()
    response = client.get('/api/suppliers')
    
    assert response.status_code == 200
    assert b"SportsCo" in response.data

def test_create_supplier_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/supplier', json={})
    
    assert response.status_code == 400
    assert b"Missing required field: supplier_name" in response.data

def test_create_supplier_success(mock_db):
    mock_db.rowcount = 1
    
    client = app.test_client()
    response = client.post('/api/add/supplier', json={
        'supplier_name': 'SportsCo', 'contact_number': '123-456-7890'
    })
    
    assert response.status_code == 201
    assert b"Supplier created successfully" in response.data

# Activities tests
def test_get_activities_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/activities')
    
    assert response.status_code == 404
    assert b"No activities found" in response.data

def test_get_activities(mock_db):
    mock_db.fetchall.return_value = [(1, 'Basketball Practice')]
    
    client = app.test_client()
    response = client.get('/api/activities')
    
    assert response.status_code == 200
    assert b"Basketball Practice" in response.data

def test_create_activity_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/activity', json={})
    
    assert response.status_code == 400
    assert b"Missing required field: activity_name" in response.data

def test_create_activity_success(mock_db):
    mock_db.rowcount = 1
    
    client = app.test_client()
    response = client.post('/api/add/activity', json={
        'activity_name': 'Soccer Training'
    })
    
    assert response.status_code == 201
    assert b"Activity created successfully" in response.data

# Inventory-Supplier tests
def test_get_inventory_suppliers_empty(mock_db):
    mock_db.fetchall.return_value = []
    
    client = app.test_client()
    response = client.get('/api/inventory-suppliers')
    
    assert response.status_code == 404
    assert b"No inventory-supplier relationships found" in response.data

def test_get_inventory_suppliers(mock_db):
    mock_db.fetchall.return_value = [(1, 101, 'SportsCo')]
    
    client = app.test_client()
    response = client.get('/api/inventory-suppliers')
    
    assert response.status_code == 200
    assert b"SportsCo" in response.data

def test_create_inventory_supplier_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/api/add/inventory-supplier', json={})
    
    assert response.status_code == 400
    assert b"Missing required field: inventory_item_id" in response.data

def test_create_inventory_supplier_success(mock_db):
    mock_db.rowcount = 1
    
    client = app.test_client()
    response = client.post('/api/add/inventory-supplier', json={
        'inventory_item_id': 101, 'supplier_id': 1
    })
    
    assert response.status_code == 201
    assert b"Inventory-Supplier relationship created successfully" in response.data

if __name__ == "__main__":
    pytest.main()
