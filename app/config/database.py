"""
Módulo de configuración de la base de datos.
"""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models.base import get_base




# Conexión a una base de datos MySQL
USERNAME = 'root'
PASSWORD = ''
HOST = '127.0.0.1'
DATABASE_NAME = 'data_prodct_project'

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
print("Conectando a la base de datos en:", SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Función para la creación de las tablas en la base de datos.
    """
    try:
        from app.models.user import User
        from app.models.role import Role
        from app.models.policy import Policy
        from app.models.domain import Domain
        from app.models.data_product import DataProduct
        print("Intentando crear tablas en la base de datos...")
        get_base().metadata.create_all(bind=engine)

        # Inspeccionar y mostrar las tablas existentes
        inspector = inspect(engine)
        print("Tablas existentes en la base de datos después de la creación:", inspector.get_table_names())

    except (SQLAlchemyError, ConnectionError) as e:  # Aquí podrías ser más específico con el tipo de excepción
        print(f"Error al crear tablas: {e}")


if __name__ == "__main__":
    init_db()
