from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.service.domain_service import (
    create_domain,
    get_domain,
    get_all_domains,
    update_domain,
    delete_domain,
    delete_all_domains
)

router = APIRouter()

class DomainCreate(BaseModel):
    name: str
    description: str

class DomainUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

@router.post("/domains/")
async def create_new_domain(domain: DomainCreate):
    new_domain = create_domain(domain.name, domain.description)
    return {"message": "Domain created successfully", "id": new_domain.id,"domain": new_domain}

@router.get("/domains/{domain_id}")
async def read_domain(domain_id: int):
    domain = get_domain(domain_id)
    if domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain

@router.get("/domains/")
async def read_all_domains():
    domains = get_all_domains()
    return domains

@router.put("/domains/{domain_id}")
async def update_existing_domain(domain_id: int, domain: DomainUpdate):
    updated_domain = update_domain(domain_id, domain.name, domain.description)
    if updated_domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return {"message": "Domain updated successfully", "domain": updated_domain}

@router.delete("/domains/{domain_id}")
async def delete_existing_domain(domain_id: int):
    deleted_domain = delete_domain(domain_id)
    if deleted_domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return {"message": "Domain deleted successfully"}

@router.delete("/domains/")
async def delete_all_domains_route():
    num_rows_deleted = delete_all_domains()
    return {"message": "All domains deleted successfully", "deleted_count": num_rows_deleted}
