from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import get_base
from .associations import user_role_association



class User(get_base()):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String (60), index=True) 
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    domain_id = Column(Integer, ForeignKey('domains.id'))

    # Relación Domain
    domain = relationship("Domain", back_populates="users")

    # Relación con Role
    roles = relationship("Role", secondary=user_role_association, back_populates="users")

  