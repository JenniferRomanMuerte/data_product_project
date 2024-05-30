from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.policy_service import (
    create_policy, 
    get_policy, 
    get_all_policies, 
    update_policy, 
    delete_policy,
    delete_all_policies)

router = APIRouter()

class PolicyCreate(BaseModel):
    name: str
    description: str

class PolicyUpdate(BaseModel):
    name: str
    description: str


# Crear una nueva politica
@router.post("/policies/")
async def create_new_policy(policy: PolicyCreate):
    new_policy = create_policy(policy.name, policy.description)
    return {"message": "Policy created successfully", "policy": new_policy}


# Recuperamos uno por su Id
@router.get("/policies/{policy_id}")
async def read_policy(policy_id: int):
    policy = get_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

# Recuperamos todos
@router.get("/policies/")
async def read_all_policies():
    policies = get_all_policies()
    return policies

# Actualizar
@router.put("/policies/{policy_id}")
async def update_existing_policy(policy_id: int, policy: PolicyUpdate):
    updated_policy = update_policy(policy_id, policy.name, policy.description)
    if updated_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"message": "Policy updated successfully", "policy": updated_policy}


# Borrar uno por su ID
@router.delete("/policies/{policy_id}")
async def delete_existing_policy(policy_id: int):
    deleted_policy = delete_policy(policy_id)
    if deleted_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"message": "Policy deleted successfully"}


@router.delete("/policies/")
async def delete_all_policies():
    num_rows_deleted = delete_all_policies()
    return {"message": "All policies deleted successfully", "deleted_count": num_rows_deleted}