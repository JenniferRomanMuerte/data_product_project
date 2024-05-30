from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.data_product_service import (
    create_data_product,
    get_data_product,
    get_all_data_products,
    update_data_product,
    delete_data_product,
    delete_all_data_products
)

router = APIRouter()

class DataProductCreate(BaseModel):
    name: str
    domain_id: int

class DataProductUpdate(BaseModel):
    name: str
    domain_id: int

@router.post("/data_products/")
async def create_new_data_product(data_product: DataProductCreate):
    try:
        new_data_product = create_data_product(data_product.name, data_product.domain_id)
        return {"message": "Data product created successfully", "data_product": new_data_product}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/data_products/{data_product_id}")
async def read_data_product(data_product_id: int):
    data_product = get_data_product(data_product_id)
    if data_product is None:
        raise HTTPException(status_code=404, detail="Data product not found")
    return data_product

@router.get("/data_products/")
async def read_all_data_products():
    data_products = get_all_data_products()
    return data_products

@router.put("/data_products/{data_product_id}")
async def update_existing_data_product(data_product_id: int, data_product: DataProductUpdate):
    updated_data_product = update_data_product(data_product_id, data_product.name, data_product.domain_id)
    if updated_data_product is None:
        raise HTTPException(status_code=404, detail="Data product not found")
    return {"message": "Data product updated successfully", "data_product": updated_data_product}

@router.delete("/data_products/{data_product_id}")
async def delete_existing_data_product(data_product_id: int):
    deleted_data_product = delete_data_product(data_product_id)
    if deleted_data_product is None:
        raise HTTPException(status_code=404, detail="Data product not found")
    return {"message": "Data product deleted successfully"}

@router.delete("/data_products/")
async def delete_all_data_products_route():
    num_rows_deleted = delete_all_data_products()
    return {"message": "All data products deleted successfully", "deleted_count": num_rows_deleted}
