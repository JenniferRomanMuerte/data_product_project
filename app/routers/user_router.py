from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr

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
    email: EmailStr
    plain_password: str
    domain_id: int
    roles: Optional[List[int]] = None

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    plain_password: Optional[str]
    domain_id: Optional[int]
    roles: Optional[List[int]] = None

@router.post("/users/")
async def create_new_user(user: UserCreate):
    try:
        new_user = create_user(user.name, user.email, user.plain_password, user.domain_id, user.roles)
        return {"message": "User created successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/")
async def read_all_users():
    users = get_all_users()
    return users

@router.put("/users/{user_id}")
async def update_existing_user(user_id: int, user: UserUpdate):
    updated_user = update_user(user_id, user.name, user.email, user.plain_password, user.domain_id, user.roles)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully", "user": updated_user}

@router.delete("/users/{user_id}")
async def delete_existing_user(user_id: int):
    deleted_user = delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.delete("/users/")
async def delete_all_users_route():
    num_rows_deleted = delete_all_users()
    return {"message": "All users deleted successfully", "deleted_count": num_rows_deleted}
