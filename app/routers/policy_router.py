"""
Router para la gestión de políticas.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.policy_service import (
    create_policy,
    get_policy,
    get_all_policies,
    update_policy,
    delete_policy,
    delete_all_policies
)

router = APIRouter()

class PolicyCreate(BaseModel):
    """
    Esquema para la creación de una política.
    """
    name: str
    description: str
    role_ids: Optional[List[int]] = None

class PolicyUpdate(BaseModel):
    """
    Esquema para la actualización de una política.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    role_ids: Optional[List[int]] = None

@router.post("/policies/")
async def create_new_policy(policy: PolicyCreate):
    """
    Crea una nueva política.

    Args:
        policy (PolicyCreate): Esquema para crear una política.

    Returns:
        dict: Mensaje de éxito y la política creada.
    """
    new_policy = create_policy(policy.name, policy.description, policy.role_ids)
    return {"message": "Policy created successfully", "policy": new_policy}

@router.get("/policies/{policy_id}")
async def read_policy(policy_id: int):
    """
    Recupera una política por su ID.

    Args:
        policy_id (int): ID de la política.

    Returns:
        Policy: La política correspondiente al ID proporcionado.
    """
    policy = get_policy(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@router.get("/policies/")
async def read_all_policies():
    """
    Recupera todas las políticas.

    Returns:
        list[Policy]: Lista de todas las políticas.
    """
    policies = get_all_policies()
    return policies

@router.put("/policies/{policy_id}")
async def update_existing_policy(policy_id: int, policy: PolicyUpdate):
    """
    Actualiza una política existente.

    Args:
        policy_id (int): ID de la política.
        policy (PolicyUpdate): Esquema para actualizar una política.

    Returns:
        dict: Mensaje de éxito y la política actualizada.
    """
    updated_policy = update_policy(policy_id, policy.name, policy.description, policy.role_ids)
    if updated_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"message": "Policy updated successfully", "policy": updated_policy}

@router.delete("/policies/{policy_id}")
async def delete_existing_policy(policy_id: int):
    """
    Elimina una política por su ID.

    Args:
        policy_id (int): ID de la política.

    Returns:
        dict: Mensaje de éxito.
    """
    deleted_policy = delete_policy(policy_id)
    if deleted_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"message": "Policy deleted successfully"}

@router.delete("/policies/")
async def delete_all_policies_route():
    """
    Elimina todas las políticas.

    Returns:
        dict: Mensaje de éxito y el número de políticas eliminadas.
    """
    num_rows_deleted = delete_all_policies()
    return {"message": "All policies deleted successfully", "deleted_count": num_rows_deleted}
