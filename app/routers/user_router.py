"""
Router para la gestión de usuarios.
"""
from typing import List, Optional  # Importar estándar antes de otros imports
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.service.user_service import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
    delete_all_users
)

router = APIRouter()

class UserCreate(BaseModel):
    """
    Modelo para la creación de usuarios.
    """
    name: str = Field(..., example="John Doe")
    plain_password: str = Field(..., example="strongpassword")
    domain_id: int = Field(..., example=1)
    roles: Optional[List[int]] = Field(None, example=[1, 2])

class UserUpdate(BaseModel):
    """
    Modelo para la actualización de usuarios.
    """
    name: Optional[str] = Field(None, example="John Doe")
    plain_password: Optional[str] = Field(None, example="newpassword")
    domain_id: Optional[int] = Field(None, example=1)
    roles: Optional[List[int]] = Field(None, example=[1, 2])

@router.post("/users/")
async def create_new_user(user: UserCreate):
    """
    Crea un nuevo usuario.
    """
    try:
        new_user = create_user(user.name, user.plain_password, user.domain_id, user.roles)
        return {"message": "User created successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    """
    Recupera un usuario por su ID.
    """
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/")
async def read_all_users():
    """
    Recupera todos los usuarios.
    """
    users = get_all_users()
    return users

@router.put("/users/{user_id}")
async def update_existing_user(user_id: int, user: UserUpdate):
    """
    Actualiza un usuario existente.
    """
    updated_user = update_user(user_id, user.name, user.plain_password, user.domain_id, user.roles)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully", "user": updated_user}

@router.delete("/users/{user_id}")
async def delete_existing_user(user_id: int):
    """
    Elimina un usuario por su ID.
    """
    deleted_user = delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.delete("/users/")
async def delete_all_data_products_route():
    """
    Elimina todos los usuarios.
    """
    num_rows_deleted = delete_all_users()
    return {"message": "All users deleted successfully", "deleted_count": num_rows_deleted}
