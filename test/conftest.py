import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import get_base
from app.main import app
from app.config.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Usa SQLite para pruebas

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

get_base().metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clean_tables():
    """
    Limpia las tablas de la base de datos antes de cada prueba.
    """
    get_base().metadata.drop_all(bind=engine)
    get_base().metadata.create_all(bind=engine)
