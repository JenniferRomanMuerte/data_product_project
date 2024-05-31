from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import get_base

# Tabla de asociación para la relación muchos-a-muchos entre User y Role
user_role_association = Table('user_roles', get_base().metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# Tabla de asociación entre los dominios y los dataProduct
domain_data_product = Table('domain_data_product', get_base().metadata,
    Column('domain_id', Integer, ForeignKey('domains.id'), primary_key=True),
    Column('data_product_id', Integer, ForeignKey('data_products.id'), primary_key=True)
)

# Tabla de asociación para la relación muchos-a-muchos entre Role y Policy
role_policy_association = Table('role_policies', get_base().metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('policy_id', Integer, ForeignKey('policies.id'), primary_key=True)
)
