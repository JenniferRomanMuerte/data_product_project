"""
Servicio para la gestión de dominios.
"""
from app.config.database import SessionLocal

from app.models.domain import Domain
from app.models.user import User
from app.models.data_product import DataProduct

def create_domain(name: str, description: str, user_ids: list[int] = None, data_product_ids: list[int] = None):
    """
    Crea un nuevo dominio con los usuarios y productos de datos proporcionados.

    Args:
        name (str): Nombre del dominio.
        description (str): Descripción del dominio.
        user_ids (list[int], optional): Lista de IDs de usuarios a asignar al dominio.
        data_product_ids (list[int], optional): Lista de IDs de productos de datos a asignar al dominio.

    Returns:
        Domain: El dominio creado.
    """
    db = SessionLocal()
    try:
        new_domain = Domain(name=name, description=description)
        if user_ids:
            for user_id in user_ids:
                user = db.query(User).get(user_id)
                if user:
                    new_domain.users.append(user)
        if data_product_ids:
            for data_product_id in data_product_ids:
                data_product = db.query(DataProduct).get(data_product_id)
                if data_product:
                    new_domain.data_products.append(data_product)
        db.add(new_domain)
        db.commit()
        db.refresh(new_domain)
        return new_domain
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_domain(domain_id: int):
    """
    Recupera un dominio por su ID.

    Args:
        domain_id (int): ID del dominio.

    Returns:
        Domain: El dominio correspondiente al ID proporcionado, o None si no se encuentra.
    """
    db = SessionLocal()
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    db.close()
    return domain

def get_all_domains():
    """
    Recupera todos los dominios.

    Returns:
        list[Domain]: Lista de todos los dominios.
    """
    db = SessionLocal()
    domains = db.query(Domain).all()
    db.close()
    return domains

def update_domain(domain_id: int, name: str = None, description: str = None, user_ids: list[int] = None, data_product_ids: list[int] = None):
    """
    Actualiza un dominio existente.

    Args:
        domain_id (int): ID del dominio.
        name (str, optional): Nuevo nombre del dominio.
        description (str, optional): Nueva descripción del dominio.
        user_ids (list[int], optional): Nueva lista de IDs de usuarios a asignar al dominio.
        data_product_ids (list[int], optional): Nueva lista de IDs de productos de datos a asignar al dominio.

    Returns:
        Domain: El dominio actualizado, o None si no se encuentra.
    """
    db = SessionLocal()
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        db.close()
        return None
    if name:
        domain.name = name
    if description:
        domain.description = description
    if user_ids is not None:
        domain.users = []
        for user_id in user_ids:
            user = db.query(User).get(user_id)
            if user:
                domain.users.append(user)
    if data_product_ids is not None:
        domain.data_products = []
        for data_product_id in data_product_ids:
            data_product = db.query(DataProduct).get(data_product_id)
            if data_product:
                domain.data_products.append(data_product)
    db.commit()
    db.refresh(domain)
    db.close()
    return domain

def delete_domain(domain_id: int):
    """
    Elimina un dominio por su ID.

    Args:
        domain_id (int): ID del dominio a eliminar.

    Returns:
        Domain: El dominio eliminado, o None si no se encuentra.
    """
    db = SessionLocal()
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        db.close()
        return None
    db.delete(domain)
    db.commit()
    db.close()
    return domain

def delete_all_domains():
    """
    Elimina todos los dominios.

    Returns:
        int: El número de filas eliminadas.
    """
    db = SessionLocal()
    try:
        num_rows_deleted = db.query(Domain).delete()
        db.commit()
        return num_rows_deleted
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
