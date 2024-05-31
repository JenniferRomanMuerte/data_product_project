"""
Módulo de pruebas para el CRUD de productos de datos.
"""

def test_create_data_product(client):
    """
    Prueba la creación de un nuevo producto de datos.
    """
    response = client.post("/api/v1/data_products/", json={
        "name": "testdataproduct",
        "domain_ids": [1]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Data product created successfully"

def test_get_data_product(client):
    """
    Prueba la lectura de un producto de datos por ID.
    """
    response = client.post("/api/v1/data_products/", json={
        "name": "testdataproduct",
        "domain_ids": [1]
    })
    data_product_id = response.json()["data_product"]["id"]
    response = client.get(f"/api/v1/data_products/{data_product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "testdataproduct"

def test_get_all_data_products(client):
    """
    Prueba la recuperación de todos los productos de datos.
    """
    response = client.get("/api/v1/data_products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_data_product(client):
    """
    Prueba la actualización de un producto de datos existente.
    """
    response = client.post("/api/v1/data_products/", json={
        "name": "testdataproduct",
        "domain_ids": [1]
    })
    data_product_id = response.json()["data_product"]["id"]
    response = client.put(f"/api/v1/data_products/{data_product_id}", json={
        "name": "updateddataproduct",
        "domain_ids": [1]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Data product updated successfully"
    assert response.json()["data_product"]["name"] == "updateddataproduct"

def test_delete_data_product(client):
    """
    Prueba la eliminación de un producto de datos por ID.
    """
    response = client.post("/api/v1/data_products/", json={
        "name": "testdataproduct",
        "domain_ids": [1]
    })
    data_product_id = response.json()["data_product"]["id"]
    response = client.delete(f"/api/v1/data_products/{data_product_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Data product deleted successfully"

def test_delete_all_data_products(client):
    """
    Prueba la eliminación de todos los productos de datos.
    """
    response = client.delete("/api/v1/data_products/")
    assert response.status_code == 200
    assert response.json()["message"] == "All data products deleted successfully"
