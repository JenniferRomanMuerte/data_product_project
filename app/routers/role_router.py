from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.role_service import (
    create_role, 
    get_role, 
    get_all_roles, 
    update_role, 
    delete_role,
    delete_all_roles)

router = APIRouter()

class RoleCreate(BaseModel):
    name: str
    description: str

class RoleUpdate(BaseModel):
    name: str
    description: str

# Creamos un nuevo Rol
@router.post("/roles/")
async def create_new_role(role: RoleCreate):
    new_role = create_role(role.name, role.description)
    return {"message": "Role created successfully", "role": new_role}

# Recuperamos un rol por su id
@router.get("/roles/{role_id}")
async def read_role(role_id: int):
    role = get_role(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Recuperar todos 
@router.get("/roles/")
async def read_all_roles():
    roles = get_all_roles()
    return roles

# Actualizar 
@router.put("/role/{role_id}")
async def update_existing_role(role_id: int, role: RoleUpdate):
    updated_role = update_role(role_id, role.name, role.description)
    if updated_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role updated successfully", "role": updated_role}

# Borrar
@router.delete("/roles/{role_id}")
async def delete_existing_role(role_id: int):
    deleted_role = delete_role(role_id)
    if deleted_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}

@router.delete("/roles/")
async def delete_all_data_products_route():
    num_rows_deleted = delete_all_roles()
    return {"message": "All roles deleted successfully", "deleted_count": num_rows_deleted}