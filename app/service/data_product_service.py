from app.models.data_product import DataProduct
from app.config.database import SessionLocal
from sqlalchemy.exc import IntegrityError

def create_data_product(name: str, domain_id: int):
    db = SessionLocal()
    try:
        new_data_product = DataProduct(name=name, domain_id=domain_id)
        db.add(new_data_product)
        db.commit()
        db.refresh(new_data_product)
        return new_data_product
    except IntegrityError:
        db.rollback()
        raise ValueError("Data product with this name already exists")
    finally:
        db.close()


def get_data_product(data_product_id: int):
    db = SessionLocal()
    data_product = db.query(DataProduct).filter(DataProduct.id == data_product_id).first()
    db.close()
    return data_product


def get_all_data_products():
    db = SessionLocal()
    data_products = db.query(DataProduct).all()
    db.close()
    return data_products


def update_data_product(data_product_id: int, name: str, domain_id: int):
    db = SessionLocal()
    data_product = db.query(DataProduct).filter(DataProduct.id == data_product_id).first()
    if not data_product:
        db.close()
        return None
    data_product.name = name
    data_product.domain_id = domain_id
    db.commit()
    db.refresh(data_product)
    db.close()
    return data_product


def delete_data_product(data_product_id: int):
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
