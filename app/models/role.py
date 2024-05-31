"""
Módulo que define la clase Role y sus asociaciones.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import get_base
from .associations import user_role_association, role_policy_association

class Role(get_base()):
    """
    Clase que representa el rol en la base de datos.

    Atributos:
    id: Identificador único del rol.
    name: Nombre del rol.
    description: Descripción del rol.
    users: Relación con los usuarios, usando la tabla intermedia user_role_association.
    policies: Relación con las políticas, usando la tabla intermedia role_policy_association.
    """
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    description = Column(String(250), index=True)

    # Relación con User, usando la tabla intermedia
    users = relationship("User", secondary=user_role_association, back_populates="roles")

    # Relación con Policy, usando la tabla intermedia
    policies = relationship("Policy", secondary=role_policy_association, back_populates="roles")

# Fin del archivo
