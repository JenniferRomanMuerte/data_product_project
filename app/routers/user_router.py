from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
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
    name: str
    email: str
    password: str
    domain_id: int

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str
    domain_id: int


# Crear
@router.post("/users/")
async def create_new_user(user: UserCreate):
    try:
        new_user = create_user(user.name, user.email, user.password, user.domain_id)
        return {"message": "User created successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Recuperar Usuario por su id
@router.get("/users/{user_id}")
async def read_user(user_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Recuperar todos 
@router.get("/users/")
async def read_all_users():
    users = get_all_users()
    return users

# Actualizar 
@router.put("/users/{user_id}")
async def update_existing_user(user_id: int, user: UserUpdate):
    updated_user = update_user(user_id, user.name, user.email, user.password, user.domain_id)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully", "user": updated_user}

# Borrar
@router.delete("/users/{user_id}")
async def delete_existing_user(user_id: int):
    deleted_user = delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.delete("/users/")
async def delete_all_data_products_route():
    num_rows_deleted = delete_all_users()
    return {"message": "All users deleted successfully", "deleted_count": num_rows_deleted}