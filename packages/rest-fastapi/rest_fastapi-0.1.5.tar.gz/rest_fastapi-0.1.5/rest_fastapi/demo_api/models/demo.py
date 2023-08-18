from sqlalchemy import Column, String

from rest_fastapi.bases.model import ModelHelper
from rest_fastapi.core import Base

model_helper = ModelHelper(Base)


class Demo(model_helper.get_enhanced_model):
    """demo"""
    __tablename__ = 'demo'
    name = Column(String(255), nullable=True, default='', comment='名字')
