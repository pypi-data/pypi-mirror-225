from datetime import datetime
from orjson import dumps
from sqlalchemy import Column, TIMESTAMP, text, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declared_attr

from rest_fastapi.core import Base


class BasicModel(Base):
    """
    model 基础类，定义了共用字段和共用方法
    """
    __abstract__ = True

    _the_prefix = 'someprefix_'

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(TIMESTAMP, default=datetime.now, nullable=True, server_default=text('CURRENT_TIMESTAMP'))

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        model_dict = {}
        for _ in self.__table__.columns:
            value = getattr(self, _.name)
            if value is None:
                value = 0 if isinstance(_.type, Integer) else ''
            model_dict[_.name] = value
        return model_dict

    def __str__(self):
        return str(dumps(self.to_dict()), 'utf-8')

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__


class EnhancedModel(BasicModel):
    """
    增加了 update_time 、is_deleted 字段
    """
    __abstract__ = True

    _the_prefix = 'someprefix_'

    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now, comment='更新时间')
    is_deleted = Column(Boolean, default=False, comment='是否删除')

    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__
