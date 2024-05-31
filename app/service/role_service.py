"""
Servicio para la gestión de roles y sus asociaciones.
"""

from app.models.role import Role
from app.models.user import User
from app.models.policy import Policy
from app.config.database import SessionLocal

def create_role(name: str, description: str, user_ids: list[int] = None, policy_ids: list[int] = None):
    """
    Crea un nuevo rol con las asociaciones proporcionadas.

    Args:
        name (str): Nombre del rol.
        description (str): Descripción del rol.
        user_ids (list[int], optional): Lista de IDs de usuarios a asociar con el rol.
        policy_ids (list[int], optional): Lista de IDs de políticas a asociar con el rol.

    Returns:
        Role: El rol creado.
    """
    db = SessionLocal()
    try:
        new_role = Role(name=name, description=description)
        if user_ids:
            for user_id in user_ids:
                user = db.query(User).get(user_id)
                if user:
                    new_role.users.append(user)
        if policy_ids:
            for policy_id in policy_ids:
                policy = db.query(Policy).get(policy_id)
                if policy:
                    new_role.policies.append(policy)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_role(role_id: int):
    """
    Recupera un rol por su ID.

    Args:
        role_id (int): ID del rol.

    Returns:
        Role: El rol correspondiente al ID proporcionado, o None si no se encuentra.
    """
    db = SessionLocal()
    role = db.query(Role).filter(Role.id == role_id).first()
    db.close()
    return role

def get_all_roles():
    """
    Recupera todos los roles.

    Returns:
        list[Role]: Lista de todos los roles.
    """
    db = SessionLocal()
    roles = db.query(Role).all()
    db.close()
    return roles

def update_role(role_id: int, name: str = None, description: str = None, user_ids: list[int] = None, policy_ids: list[int] = None):
    """
    Actualiza un rol existente.

    Args:
        role_id (int): ID del rol.
        name (str, optional): Nuevo nombre del rol.
        description (str, optional): Nueva descripción del rol.
        user_ids (list[int], optional): Nueva lista de IDs de usuarios a asociar con el rol.
        policy_ids (list[int], optional): Nueva lista de IDs de políticas a asociar con el rol.

    Returns:
        Role: El rol actualizado, o None si no se encuentra.
    """
    db = SessionLocal()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        db.close()
        return None
    if name:
        role.name = name
    if description:
        role.description = description
    if user_ids is not None:
        role.users = []
        for user_id in user_ids:
            user = db.query(User).get(user_id)
            if user:
                role.users.append(user)
    if policy_ids is not None:
        role.policies = []
        for policy_id in policy_ids:
            policy = db.query(Policy).get(policy_id)
            if policy:
                role.policies.append(policy)
    db.commit()
    db.refresh(role)
    db.close()
    return role

def delete_role(role_id: int):
    """
    Elimina un rol por su ID.

    Args:
        role_id (int): ID del rol a eliminar.

    Returns:
        Role: El rol eliminado, o None si no se encuentra.
    """
    db = SessionLocal()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        db.close()
        return None
    db.delete(role)
    db.commit()
    db.close()
    return role

def delete_all_roles():
    """
    Elimina todos los roles.

    Returns:
        int: El número de filas eliminadas.
    """
    db = SessionLocal()
    try:
        num_rows_deleted = db.query(Role).delete()
        db.commit()
        return num_rows_deleted
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
