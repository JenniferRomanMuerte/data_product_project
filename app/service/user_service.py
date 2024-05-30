from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.models.user import User
from app.models.role import Role
from app.config.database import SessionLocal
from app.utils.security import hash_password, verify_password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)



def create_user(name: str, plain_password: str, domain_id: int):
    db = SessionLocal()
    try:
        hashed_password = hash_password(plain_password)
        new_user = User(name=name, hashed_password=hashed_password, domain_id=domain_id)
        for role_id in role:
            role = db.query(Role).get(role_id)
            if role:
                new_user.roles.append(role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this name already exists")
    finally:
        db.close()



def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user


def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users


def update_user(user_id: int, name: str, email: str, password: str, domain_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        return None
    user.name = name
    user.email = email
    user.hashed_password = get_password_hash(password)
    user.domain_id = domain_id
    db.commit()
    db.refresh(user)
    db.close()
    return user


def delete_user(user_id: int):
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

# Para el control de las contraseñas
def authenticate_user(name: str, plain_password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.name == name).first()
    if user and verify_password(plain_password, user.hashed_password):
        return user
    return None