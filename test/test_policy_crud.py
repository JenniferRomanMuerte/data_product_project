"""
Módulo de pruebas para el CRUD de políticas.
"""

def test_create_policy(client):
    """
    Prueba la creación de una nueva política.
    """
    response = client.post("/api/v1/policies/", json={
        "name": "testpolicy",
        "description": "test policy description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Policy created successfully"

def test_get_policy(client):
    """
    Prueba la lectura de una política por ID.
    """
    response = client.post("/api/v1/policies/", json={
        "name": "testpolicy",
        "description": "test policy description"
    })
    policy_id = response.json()["policy"]["id"]
    response = client.get(f"/api/v1/policies/{policy_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "testpolicy"

def test_get_all_policies(client):
    """
    Prueba la recuperación de todas las políticas.
    """
    response = client.get("/api/v1/policies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_policy(client):
    """
    Prueba la actualización de una política existente.
    """
    response = client.post("/api/v1/policies/", json={
        "name": "testpolicy",
        "description": "test policy description"
    })
    policy_id = response.json()["policy"]["id"]
    response = client.put(f"/api/v1/policies/{policy_id}", json={
        "name": "updatedpolicy",
        "description": "updated policy description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Policy updated successfully"
    assert response.json()["policy"]["name"] == "updatedpolicy"

def test_delete_policy(client):
    """
    Prueba la eliminación de una política por ID.
    """
    response = client.post("/api/v1/policies/", json={
        "name": "testpolicy",
        "description": "test policy description"
    })
    policy_id = response.json()["policy"]["id"]
    response = client.delete(f"/api/v1/policies/{policy_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Policy deleted successfully"

def test_delete_all_policies(client):
    """
    Prueba la eliminación de todas las políticas.
    """
    response = client.delete("/api/v1/policies/")
    assert response.status_code == 200
    assert response.json()["message"] == "All policies deleted successfully"
