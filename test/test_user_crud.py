import time

def test_create_user(client):
    """
    Prueba la creación de un nuevo usuario.
    """
    # Crear un dominio primero
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    assert response.status_code == 200
    domain_id = response.json()["id"]  # Ajustado para obtener "id" directamente

    # Generar un sufijo único
    unique_suffix = str(int(time.time()))

    # Ahora crear el usuario con valores únicos
    response = client.post("/api/v1/users/", json={
        "name": f"testuser_{unique_suffix}",
        "email": f"testuser_{unique_suffix}@example.com",
        "plain_password": "testpassword",
        "domain_id": domain_id
    })
    if response.status_code != 200:
        print(response.json())  # Imprime el contenido de la respuesta de error para más detalles
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_get_user(client):
    """
    Prueba la lectura de un usuario por ID.
    """
    # Crear un dominio primero
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    assert response.status_code == 200
    domain_id = response.json()["id"]

    # Generar un sufijo único
    unique_suffix = str(int(time.time()))

    # Crear un usuario
    response = client.post("/api/v1/users/", json={
        "name": f"testuser_{unique_suffix}",
        "email": f"testuser_{unique_suffix}@example.com",
        "plain_password": "testpassword",
        "domain_id": domain_id
    })
    assert response.status_code == 200
    user_id = response.json()["user"]["id"]

    # Obtener el usuario por ID
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == f"testuser_{unique_suffix}"

def test_get_all_users(client):
    """
    Prueba la recuperación de todos los usuarios.
    """
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user(client):
    """
    Prueba la actualización de un usuario existente.
    """
    # Crear un dominio primero
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    assert response.status_code == 200
    domain_id = response.json()["id"]

    # Generar un sufijo único
    unique_suffix = str(int(time.time()))

    # Crear un usuario
    response = client.post("/api/v1/users/", json={
        "name": f"testuser_{unique_suffix}",
        "email": f"testuser_{unique_suffix}@example.com",
        "plain_password": "testpassword",
        "domain_id": domain_id
    })
    user_id = response.json()["user"]["id"]

    # Actualizar el usuario
    response = client.put(f"/api/v1/users/{user_id}", json={
        "name": "updateduser",
        "email": f"updateduser_{unique_suffix}@example.com",
        "plain_password": "updatedpassword",
        "domain_id": domain_id
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["user"]["name"] == "updateduser"

def test_delete_user(client):
    """
    Prueba la eliminación de un usuario por ID.
    """
    # Crear un dominio primero
    response = client.post("/api/v1/domains/", json={
        "name": "testdomain",
        "description": "test domain description"
    })
    assert response.status_code == 200
    domain_id = response.json()["id"]

    # Generar un sufijo único
    unique_suffix = str(int(time.time()))

    # Crear un usuario
    response = client.post("/api/v1/users/", json={
        "name": f"testuser_{unique_suffix}",
        "email": f"testuser_{unique_suffix}@example.com",
        "plain_password": "testpassword",
        "domain_id": domain_id
    })
    user_id = response.json()["user"]["id"]

    # Eliminar el usuario
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_delete_all_users(client):
    """
    Prueba la eliminación de todos los usuarios.
    """
    response = client.delete("/api/v1/users/")
    assert response.status_code == 200
    assert response.json()["message"] == "All users deleted successfully"
