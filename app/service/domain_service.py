from app.models.domain import Domain
from app.config.database import SessionLocal



def create_domain(name: str, description: str):
    db = SessionLocal()
    new_domain = Domain(name=name, description=description)
    db.add(new_domain)
    db.commit()
    db.refresh(new_domain)
    db.close()
    return new_domain


def get_domain(domain_id: int):
    db = SessionLocal()
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    db.close()
    return domain

def get_all_domains():
    db = SessionLocal()
    domains = db.query(Domain).all()
    db.close()
    return domains

def update_domain(domain_id: int, name: str, description: str):
    db = SessionLocal()
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        db.close()
        return None
    domain.name = name
    domain.description = description
    db.commit()
    db.refresh(domain)
    db.close()
    return domain

def delete_domain(domain_id: int):
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

