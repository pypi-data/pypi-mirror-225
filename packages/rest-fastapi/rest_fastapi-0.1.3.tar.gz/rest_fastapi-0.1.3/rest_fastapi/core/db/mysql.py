from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.base import Engine
from sqlalchemy.pool import NullPool


# todo 如果使用配置文件中的配置需要添加路径
# from rest_fastapi import set_settings_module
#
# set_settings_module('settings.conf')


class MysqlFactory:

    def __init__(self, _engine: Engine = None, **kwargs):
        self.engine = self.generate_engine(_engine, **kwargs)

    @staticmethod
    def generate_url(**kwargs):
        from rest_fastapi import BuilderFastApi
        settings = BuilderFastApi().settings
        if hasattr(settings, 'Mysql'):
            if kwargs:
                settings.Mysql.username = kwargs.get('username', '')
                settings.Mysql.password = kwargs.get('password', '')
                settings.Mysql.host = kwargs.get('host', '')
                settings.Mysql.port = kwargs.get('port', '')
                settings.Mysql.database = kwargs.get('database', '')
            return URL.create(
                drivername="mysql+pymysql",
                username=settings.Mysql.username,
                password=settings.Mysql.password,
                host=settings.Mysql.host,
                port=settings.Mysql.port,
                database=settings.Mysql.database,
            )
        else:
            path = settings.Sqlit.path if hasattr(settings, 'Sqlit') else '/sqlit3.db'
            return 'sqlite://{}?check_same_thread=False'.format(path)

    def generate_engine(self, _engine: Engine = None, **kwargs):
        if _engine:
            return _engine
        mysql_url = self.generate_url(**kwargs)
        return create_engine(mysql_url, poolclass=NullPool)

    @property
    def get_sessionLocal(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @property
    def get_base(self):
        return declarative_base(bind=self.engine)

    def get_database(self):
        db = self.get_sessionLocal()
        try:
            yield db
        finally:
            db.close()


mysql_factory = MysqlFactory()
Base = mysql_factory.get_base
engine = mysql_factory.engine
get_database = mysql_factory.get_database
