from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import get_base # para llamar a la función y crear el objeto base sin importaciones circulares
from .associations import role_policy_association # archivo donde están todas las tablas intermedias


class Policy(get_base()):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    description = Column(String(250), index=True)

    # Relación con Role
    roles = relationship("Role", secondary=role_policy_association, back_populates="policies")
