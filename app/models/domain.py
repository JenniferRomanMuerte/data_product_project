"""
Módulo que define la clase Domain y sus asociaciones.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import get_base

class Domain(get_base()):
    """
    Clase que representa el dominio en la base de datos.

    Atributos:
    id: Identificador único del dominio.
    name: Nombre del dominio.
    description: Descripción del dominio.
    user: Relación con el usuario.
    data_product: Relación con los productos de datos, usando la tabla intermedia domain_data_product.
    """
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    description = Column(String(250), index=True)

    # Relación con User
    user = relationship("User", back_populates="domain")

    # Relación con DataProduct
    data_product = relationship('DataProduct', secondary='domain_data_product', back_populates='domains')

# Fin del archivo
