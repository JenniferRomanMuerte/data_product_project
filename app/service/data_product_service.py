"""
Servicio para la gestión de productos de datos.
"""

from sqlalchemy.exc import IntegrityError

from app.models.data_product import DataProduct
from app.models.domain import Domain
from app.config.database import SessionLocal

def create_data_product(name: str, domain_ids: list[int] = None):
    """
    Crea un nuevo producto de datos con los dominios proporcionados.

    Args:
        name (str): Nombre del producto de datos.
        domain_ids (list[int], optional): Lista de IDs de dominios a asignar al producto de datos.

    Returns:
        DataProduct: El producto de datos creado.

    Raises:
        ValueError: Si el producto de datos ya existe.
    """
    db = SessionLocal()
    try:
        new_data_product = DataProduct(name=name)
        if domain_ids:
            for domain_id in domain_ids:
                domain = db.get(Domain, domain_id)
                if domain:
                    new_data_product.domains.append(domain)
        db.add(new_data_product)
        db.commit()
        db.refresh(new_data_product)
        return new_data_product
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Data product with this name already exists") from exc
    finally:
        db.close()

def get_data_product(data_product_id: int):
    """
    Recupera un producto de datos por su ID.

    Args:
        data_product_id (int): ID del producto de datos.

    Returns:
        DataProduct: El producto de datos correspondiente al ID proporcionado, o None si no se encuentra.
    """
    db = SessionLocal()
    data_product = db.query(DataProduct).filter(DataProduct.id == data_product_id).first()
    db.close()
    return data_product

def get_all_data_products():
    """
    Recupera todos los productos de datos.

    Returns:
        list[DataProduct]: Lista de todos los productos de datos.
    """
    db = SessionLocal()
    data_products = db.query(DataProduct).all()
    db.close()
    return data_products

def update_data_product(data_product_id: int, name: str = None, domain_ids: list[int] = None):
    """
    Actualiza un producto de datos existente.

    Args:
        data_product_id (int): ID del producto de datos.
        name (str, optional): Nuevo nombre del producto de datos.
        domain_ids (list[int], optional): Nueva lista de IDs de dominios a asignar al producto de datos.

    Returns:
        DataProduct: El producto de datos actualizado, o None si no se encuentra.
    """
    db = SessionLocal()
    data_product = db.query(DataProduct).filter(DataProduct.id == data_product_id).first()
    if not data_product:
        db.close()
        return None
    if name:
        data_product.name = name
    if domain_ids is not None:
        data_product.domains = []
        for domain_id in domain_ids:
            domain = db.get(Domain, domain_id)
            if domain:
                data_product.domains.append(domain)
    db.commit()
    db.refresh(data_product)
    db.close()
    return data_product

def delete_data_product(data_product_id: int):
    """
    Elimina un producto de datos por su ID.

    Args:
        data_product_id (int): ID del producto de datos a eliminar.

    Returns:
        DataProduct: El producto de datos eliminado, o None si no se encuentra.
    """
    db = SessionLocal()
    data_product = db.query(DataProduct).filter(DataProduct.id == data_product_id).first()
    if not data_product:
        db.close()
        return None
    db.delete(data_product)
    db.commit()
    db.close()
    return data_product

def delete_all_data_products():
    """
    Elimina todos los productos de datos.

    Returns:
        int: El número de filas eliminadas.
    """
    db = SessionLocal()
    try:
        num_rows_deleted = db.query(DataProduct).delete()
        db.commit()
        return num_rows_deleted
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
