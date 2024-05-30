from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import get_base
from .associations import user_role_association,role_policy_association


class Role(get_base()):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    description = Column(String(250), index=True)

    # Relación con User, usando la tabla intermedia
    users = relationship("User", secondary=user_role_association, back_populates="roles")

    # Relación con Policy, usando la tabla intermedia
    policies = relationship("Policy", secondary=role_policy_association, back_populates="roles")

    



