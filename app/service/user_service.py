from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.models.user import User
from app.models.role import Role
from app.config.database import SessionLocal
from app.utils.security import hash_password, verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    Genera un hash seguro para una contraseña dada.
    """
    return pwd_context.hash(password)

def create_user(name: str, email: str, plain_password: str, domain_id: int, roles: list[int] = None):
    """
    Crea un nuevo usuario con los roles proporcionados.

    Args:
        name (str): Nombre del usuario.
        email (str): Email del usuario.
        plain_password (str): Contraseña en texto plano del usuario.
        domain_id (int): ID del dominio al que pertenece el usuario.
        roles (list[int], optional): Lista de IDs de roles a asignar al usuario.

    Returns:
        User: El usuario creado.

    Raises:
        ValueError: Si el usuario ya existe.
    """
    db = SessionLocal()
    try:
        hashed_password = hash_password(plain_password)
        new_user = User(name=name, email=email, hashed_password=hashed_password, domain_id=domain_id)
        if roles:
            for role_id in roles:
                role = db.query(Role).get(role_id)
                if role:
                    new_user.roles.append(role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("User with this name or email already exists") from exc
    finally:
        db.close()

def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

def get_all_users():
    """
    Recupera todos los usuarios.

    Returns:
        list[User]: Lista de todos los usuarios.
    """
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def update_user(user_id: int, name: str = None, email: str = None, plain_password: str = None, domain_id: int = None, roles: list[int] = None):
    """
    Actualiza un usuario existente.

    Args:
        user_id (int): ID del usuario.
        name (str, optional): Nuevo nombre del usuario.
        email (str, optional): Nuevo email del usuario.
        plain_password (str, optional): Nueva contraseña en texto plano del usuario.
        domain_id (int, optional): Nuevo ID del dominio al que pertenece el usuario.
        roles (list[int], optional): Nueva lista de IDs de roles a asignar al usuario.

    Returns:
        User: El usuario actualizado, o None si no se encuentra.
    """
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return None
    if name:
        user.name = name
    if email:
        user.email = email
    if plain_password:
        user.hashed_password = get_password_hash(plain_password)
    if domain_id:
        user.domain_id = domain_id
    if roles is not None:
        user.roles = []
        for role_id in roles:
            role = db.query(Role).get(role_id)
            if role:
                user.roles.append(role)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def delete_user(user_id: int):
    """
    Elimina un usuario por su ID.

    Args:
        user_id (int): ID del usuario a eliminar.

    Returns:
        User: El usuario eliminado, o None si no se encuentra.
    """
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return None
    db.delete(user)
    db.commit()
    db.close()
    return user

def delete_all_users():
    """
    Elimina todos los usuarios.

    Returns:
        int: El número de filas eliminadas.
    """
    db = SessionLocal()
    try:
        num_rows_deleted = db.query(User).delete()
        db.commit()
        return num_rows_deleted
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def authenticate_user(email: str, plain_password: str):
    """
    Autentica un usuario por su email y contraseña en texto plano.

    Args:
        email (str): Email del usuario.
        plain_password (str): Contraseña en texto plano del usuario.

    Returns:
        User: El usuario autenticado, o None si la autenticación falla.
    """
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(plain_password, user.hashed_password):
        return user
    return None
