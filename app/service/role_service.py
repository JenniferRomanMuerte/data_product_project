from app.models.role import Role
from app.config.database import SessionLocal



def create_role(name: str, description: str):
    db = SessionLocal()
    new_role = Role(name=name, description=description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    db.close()
    return new_role


def get_role(role_id: int):
    db = SessionLocal()
    role = db.query(Role).filter(Role.id == role_id).first()
    db.close()
    return role


def get_all_roles():
    db = SessionLocal()
    roles = db.query(Role).all()
    db.close()
    return roles

def update_role(role_id: int, name: str, description: str):
    db = SessionLocal()
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        db.close()
        return None
    role.name = name
    role.description = description
    db.commit()
    db.refresh(role)
    db.close()
    return role

def delete_role(role_id: int):
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