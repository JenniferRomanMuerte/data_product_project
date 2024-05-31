"""
Módulo de pruebas para el CRUD de dominios.
"""

def test_create_domain(client):
    """
    Prueba la creación de un nuevo dominio.
    """
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Domain created successfully"

def test_get_domain(client):
    """
    Prueba la lectura de un dominio por ID.
    """
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    domain_id = response.json()["domain"]["id"]
    response = client.get(f"/api/v1/domains/{domain_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "testdomain"

def test_get_all_domains(client):
    """
    Prueba la recuperación de todos los dominios.
    """
    response = client.get("/api/v1/domains/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_domain(client):
    """
    Prueba la actualización de un dominio existente.
    """
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    domain_id = response.json()["domain"]["id"]
    response = client.put(f"/api/v1/domains/{domain_id}", json={
        "name": "updateddomain",
        "description": "updated domain description"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Domain updated successfully"
    assert response.json()["domain"]["name"] == "updateddomain"

def test_delete_domain(client):
    """
    Prueba la eliminación de un dominio por ID.
    """
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    domain_id = response.json()["domain"]["id"]
    response = client.delete(f"/api/v1/domains/{domain_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Domain deleted successfully"

def test_delete_all_domains(client):
    """
    Prueba la eliminación de todos los dominios.
    """
    response = client.delete("/api/v1/domains/")
    assert response.status_code == 200
    assert response.json()["message"] == "All domains deleted successfully"
