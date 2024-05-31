"""
Módulo que define la clase DataProduct y sus asociaciones.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import get_base

class DataProduct(get_base()):
    """
    Clase que representa el producto de datos en la base de datos.

    Atributos:
    id: Identificador único del producto de datos.
    name: Nombre del producto de datos.
    domain_id: Identificador del dominio asociado.
    domains: Relación con los dominios a través de la tabla intermedia domain_data_product.
    """
    __tablename__ = 'data_products'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    domain_id = Column(Integer, ForeignKey('domains.id'))

    # Relación con Domain a través de la tabla intermedia
    domains = relationship('Domain', secondary='domain_data_product', back_populates='data_product')

# Fin del archivo
