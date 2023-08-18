from sqlalchemy import Column, String

from rest_fastapi.bases import EnhancedModel


class Demo(EnhancedModel):
    """demo"""
    __tablename__ = 'demo'
    name = Column(String(255), nullable=True, default='', comment='名字')
