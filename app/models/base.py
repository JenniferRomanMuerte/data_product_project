"""
Módulo que define la base para los modelos de SQLAlchemy.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_base():
    """
    Función para obtener la base declarativa de SQLAlchemy.

    Returns:
    Base: La base declarativa de SQLAlchemy.
    """
    return Base

# Fin del archivo
