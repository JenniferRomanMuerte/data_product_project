
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import get_base

class Domain(get_base()):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), index=True)
    description = Column(String(250), index=True)
    
    # Relación con User
    user = relationship("User", back_populates="domain")

    # Relación con DataProduct
    data_product = relationship('DataProduct', secondary='domain_data_product', back_populates='domains')