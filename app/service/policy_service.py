"""
Servicio para la gestión de políticas.
"""

from app.models.policy import Policy
from app.config.database import SessionLocal

from app.models.role import Role

def create_policy(name: str, description: str, role_ids: list[int] = None):
    """
    Crea una nueva política con los roles proporcionados.

    Args:
        name (str): Nombre de la política.
        description (str): Descripción de la política.
        role_ids (list[int], optional): Lista de IDs de roles a asignar a la política.

    Returns:
        Policy: La política creada.
    """
    db = SessionLocal()
    try:
        new_policy = Policy(name=name, description=description)
        if role_ids:
            for role_id in role_ids:
                role = db.query(Role).get(role_id)
                if role:
                    new_policy.roles.append(role)
        db.add(new_policy)
        db.commit()
        db.refresh(new_policy)
        return new_policy
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_policy(policy_id: int):
    """
    Recupera una política por su ID.

    Args:
        policy_id (int): ID de la política.

    Returns:
        Policy: La política correspondiente al ID proporcionado, o None si no se encuentra.
    """
    db = SessionLocal()
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    db.close()
    return policy

def get_all_policies():
    """
    Recupera todas las políticas.

    Returns:
        list[Policy]: Lista de todas las políticas.
    """
    db = SessionLocal()
    policies = db.query(Policy).all()
    db.close()
    return policies

def update_policy(policy_id: int, name: str = None, description: str = None, role_ids: list[int] = None):
    """
    Actualiza una política existente.

    Args:
        policy_id (int): ID de la política.
        name (str, optional): Nuevo nombre de la política.
        description (str, optional): Nueva descripción de la política.
        role_ids (list[int], optional): Nueva lista de IDs de roles a asignar a la política.

    Returns:
        Policy: La política actualizada, o None si no se encuentra.
    """
    db = SessionLocal()
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        db.close()
        return None
    if name:
        policy.name = name
    if description:
        policy.description = description
    if role_ids is not None:
        policy.roles = []
        for role_id in role_ids:
            role = db.query(Role).get(role_id)
            if role:
                policy.roles.append(role)
    db.commit()
    db.refresh(policy)
    db.close()
    return policy

def delete_policy(policy_id: int):
    """
    Elimina una política por su ID.

    Args:
        policy_id (int): ID de la política a eliminar.

    Returns:
        Policy: La política eliminada, o None si no se encuentra.
    """
    db = SessionLocal()
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        db.close()
        return None
    db.delete(policy)
    db.commit()
    db.close()
    return policy

def delete_all_policies():
    """
    Elimina todas las políticas.

    Returns:
        int: El número de filas eliminadas.
    """
    db = SessionLocal()
    try:
        num_rows_deleted = db.query(Policy).delete()
        db.commit()
        return num_rows_deleted
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
