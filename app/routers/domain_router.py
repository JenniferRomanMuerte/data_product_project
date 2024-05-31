"""
Router para la gestión de productos de datos.
"""

from typing import List, Optional
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
    """
    Esquema para la creación de un producto de datos.
    """
    name: str
    domain_ids: Optional[List[int]] = None

class DataProductUpdate(BaseModel):
    """
    Esquema para la actualización de un producto de datos.
    """
    name: Optional[str] = None
    domain_ids: Optional[List[int]] = None

@router.post("/data_products/")
async def create_new_data_product(data_product: DataProductCreate):
    """
    Crea un nuevo producto de datos.

    Args:
        data_product (DataProductCreate): Esquema para crear un producto de datos.

    Returns:
        dict: Mensaje de éxito y el producto de datos creado.
    """
    new_data_product = create_data_product(data_product.name, data_product.domain_ids)
    return {"message": "Data product created successfully", "data_product": new_data_product}

@router.get("/data_products/{data_product_id}")
async def read_data_product(data_product_id: int):
    """
    Recupera un producto de datos por su ID.

    Args:
        data_product_id (int): ID del producto de datos.

    Returns:
        DataProduct: El producto de datos correspondiente al ID proporcionado.
    """
    data_product = get_data_product(data_product_id)
    if data_product is None:
        raise HTTPException(status_code=404, detail="Data product not found")
    return data_product

@router.get("/data_products/")
async def read_all_data_products():
    """
    Recupera todos los productos de datos.

    Returns:
        list[DataProduct]: Lista de todos los productos de datos.
    """
    data_products = get_all_data_products()
    return data_products

@router.put("/data_products/{data_product_id}")
async def update_existing_data_product(data_product_id: int, data_product: DataProductUpdate):
    """
    Actualiza un producto de datos existente.

    Args:
        data_product_id (int): ID del producto de datos.
        data_product (DataProductUpdate): Esquema para actualizar un producto de datos.

    Returns:
        dict: Mensaje de éxito y el producto de datos actualizado.
    """
    updated_data_product = update_data_product(data_product_id, data_product.name, data_product.domain_ids)
    if updated_data_product is None:
        raise HTTPException(status_code=404, detail="Data product not found")
    return {"message": "Data product updated successfully", "data_product": updated_data_product}

@router.delete("/data_products/{data_product_id}")
async def delete_existing_data_product(data_product_id: int):
    """
    Elimina un producto de datos por su ID.

    Args:
        data_product_id (int): ID del producto de datos.

    Returns:
        dict: Mensaje de éxito.
    """
    deleted_data_product = delete_data_product(data_product_id)
    if deleted_data_product is None:
        raise HTTPException(status_code=404, detail="Data product not found")
    return {"message": "Data product deleted successfully"}

@router.delete("/data_products/")
async def delete_all_data_products_route():
    """
    Elimina todos los productos de datos.

    Returns:
        dict: Mensaje de éxito y el número de productos de datos eliminados.
    """
    num_rows_deleted = delete_all_data_products()
    return {"message": "All data products deleted successfully", "deleted_count": num_rows_deleted}
