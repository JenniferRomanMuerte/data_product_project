"""
Router para la gestión de roles.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.role_service import (
    create_role,
    get_role,
    get_all_roles,
    update_role,
    delete_role,
    delete_all_roles
)

router = APIRouter()

class RoleCreate(BaseModel):
    """
    Esquema para la creación de un rol.
    """
    name: str
    description: str
    user_ids: Optional[List[int]] = None
    policy_ids: Optional[List[int]] = None

class RoleUpdate(BaseModel):
    """
    Esquema para la actualización de un rol.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    user_ids: Optional[List[int]] = None
    policy_ids: Optional[List[int]] = None

@router.post("/roles/")
async def create_new_role(role: RoleCreate):
    """
    Crea un nuevo rol.

    Args:
        role (RoleCreate): Esquema para crear un rol.

    Returns:
        dict: Mensaje de éxito y el rol creado.
    """
    try:
        new_role = create_role(role.name, role.description, role.user_ids, role.policy_ids)
        return {"message": "Role created successfully", "role": new_role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/roles/{role_id}")
async def read_role(role_id: int):
    """
    Recupera un rol por su ID.

    Args:
        role_id (int): ID del rol.

    Returns:
        Role: El rol correspondiente al ID proporcionado.
    """
    role = get_role(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/roles/")
async def read_all_roles():
    """
    Recupera todos los roles.

    Returns:
        list[Role]: Lista de todos los roles.
    """
    roles = get_all_roles()
    return roles

@router.put("/roles/{role_id}")
async def update_existing_role(role_id: int, role: RoleUpdate):
    """
    Actualiza un rol existente.

    Args:
        role_id (int): ID del rol.
        role (RoleUpdate): Esquema para actualizar un rol.

    Returns:
        dict: Mensaje de éxito y el rol actualizado.
    """
    updated_role = update_role(role_id, role.name, role.description, role.user_ids, role.policy_ids)
    if updated_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role updated successfully", "role": updated_role}

@router.delete("/roles/{role_id}")
async def delete_existing_role(role_id: int):
    """
    Elimina un rol por su ID.

    Args:
        role_id (int): ID del rol.

    Returns:
        dict: Mensaje de éxito.
    """
    deleted_role = delete_role(role_id)
    if deleted_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}

@router.delete("/roles/")
async def delete_all_roles_route():
    """
    Elimina todos los roles.

    Returns:
        dict: Mensaje de éxito y el número de roles eliminados.
    """
    num_rows_deleted = delete_all_roles()
    return {"message": "All roles deleted successfully", "deleted_count": num_rows_deleted}
