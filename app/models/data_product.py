from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import get_base

class DataProduct(get_base()):
    __tablename__ = 'data_products'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    domain_id = Column(Integer, ForeignKey('domains.id'))

    # Relación con Domain a través de la tabla intermedia
    domains = relationship('Domain', secondary='domain_data_product')