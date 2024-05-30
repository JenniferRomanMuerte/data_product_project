from app.models.policy import Policy
from app.config.database import SessionLocal


def create_policy(name: str, description: str):
    db = SessionLocal()
    new_policy = Policy(name=name, description=description)
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    db.close()
    return new_policy


def get_policy(policy_id: int):
    db = SessionLocal()
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    db.close()
    return policy


def get_all_policies():
    db = SessionLocal()
    policies = db.query(Policy).all()
    db.close()
    return policies

def update_policy(policy_id: int, name: str, description: str):
    db = SessionLocal()
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        db.close()
        return None
    policy.name = name
    policy.description = description
    db.commit()
    db.refresh(policy)
    db.close()
    return policy

def delete_policy(policy_id: int):
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
