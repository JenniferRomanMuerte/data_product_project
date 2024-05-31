"""
Módulo que define la clase Policy y sus asociaciones.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import get_base  # para llamar a la función y crear el objeto base sin importaciones circulares
from .associations import role_policy_association  # archivo donde están todas las tablas intermedias

class Policy(get_base()):
    """
    Clase que representa la política en la base de datos.

    Atributos:
    id: Identificador único de la política.
    name: Nombre de la política.
    description: Descripción de la política.
    roles: Relación con los roles, usando la tabla intermedia role_policy_association.
    """
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    description = Column(String(250), index=True)

    # Relación con Role
    roles = relationship("Role", secondary=role_policy_association, back_populates="policies")

# Fin del archivo
