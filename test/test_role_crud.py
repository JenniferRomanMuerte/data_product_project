"""
Módulo de pruebas para el CRUD de roles.
"""

def test_create_role(client):
    """
    Prueba la creación de un nuevo rol.
    """
    response = client.post("/api/v1/roles/", json={
        "name": "testrole",
        "description": "test role description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Role created successfully"
    assert response.json()["role"]["name"] == "testrole"
    assert response.json()["role"]["description"] == "test role description"

def test_get_role(client):
    """
    Prueba la lectura de un rol por ID.
    """
    # Crear un rol primero
    response = client.post("/api/v1/roles/", json={
        "name": "testrole",
        "description": "test role description"
    })
    assert response.status_code == 200
    role_id = response.json()["role"]["id"]

    # Obtener el rol por ID
    response = client.get(f"/api/v1/roles/{role_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "testrole"
    assert response.json()["description"] == "test role description"

def test_get_all_roles(client):
    """
    Prueba la recuperación de todos los roles.
    """
    response = client.get("/api/v1/roles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_role(client):
    """
    Prueba la actualización de un rol existente.
    """
    # Crear un rol primero
    response = client.post("/api/v1/roles/", json={
        "name": "testrole",
        "description": "test role description"
    })
    assert response.status_code == 200
    role_id = response.json()["role"]["id"]

    # Actualizar el rol
    response = client.put(f"/api/v1/roles/{role_id}", json={
        "name": "updatedrole",
        "description": "updated role description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Role updated successfully"
    assert response.json()["role"]["name"] == "updatedrole"
    assert response.json()["role"]["description"] == "updated role description"

def test_delete_role(client):
    """
    Prueba la eliminación de un rol por ID.
    """
    # Crear un rol primero
    response = client.post("/api/v1/roles/", json={
        "name": "testrole",
        "description": "test role description"
    })
    assert response.status_code == 200
    role_id = response.json()["role"]["id"]

    # Eliminar el rol
    response = client.delete(f"/api/v1/roles/{role_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Role deleted successfully"

def test_delete_all_roles(client):
    """
    Prueba la eliminación de todos los roles.
    """
    response = client.delete("/api/v1/roles/")
    assert response.status_code == 200
    assert response.json()["message"] == "All roles deleted successfully"
