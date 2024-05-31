from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import get_base
from .associations import domain_data_product

class DataProduct(get_base()):
    __tablename__ = 'data_products'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    

    # Relación con Domain a través de la tabla intermedia
    domains = relationship('Domain', secondary=domain_data_product, back_populates='data_products')
