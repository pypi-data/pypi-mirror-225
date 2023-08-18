from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.base import Engine
from sqlalchemy.pool import NullPool


# todo 如果使用配置文件中的配置需要添加路径
# from fastapi_assistant import set_settings_module
#
# set_settings_module('settings.conf')

class BuilderDbEngine:

    def __init__(self, engine_: Engine = None, settings_=None, **kwargs):
        self.engine = self.generate_engine(engine_, settings_, **kwargs)
        self.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @staticmethod
    def generate_url(settings=None, **kwargs):
        """
        生成db url, 优先级 默认sqlit3 > kwargs > settings
        :param settings:
        :param kwargs:
        :return:
        """
        if kwargs:
            return URL.create(
                drivername="mysql+pymysql",
                username=kwargs.get('username', ''),
                password=kwargs.get('password', ''),
                host=kwargs.get('host', ''),
                port=kwargs.get('port', ''),
                database=kwargs.get('database', ''),
            )
        if settings and hasattr(settings, 'Mysql'):
            Mysql = settings.Mysql
            if kwargs:
                Mysql.username = kwargs.get('username', '')
                Mysql.password = kwargs.get('password', '')
                Mysql.host = kwargs.get('host', '')
                Mysql.port = kwargs.get('port', '')
                Mysql.database = kwargs.get('database', '')

            return URL.create(
                drivername="mysql+pymysql",
                username=Mysql.username,
                password=Mysql.password,
                host=Mysql.host,
                port=Mysql.port,
                database=Mysql.database,
            )
        else:
            path = settings.Sqlit.path if hasattr(settings, 'Sqlit') else '/sqlit3.db'
            return 'sqlite://{}?check_same_thread=False'.format(path)

    def generate_engine(self, _engine: Engine = None, settings_=None, **kwargs):
        if _engine:
            return _engine
        db_url = self.generate_url(settings_, **kwargs)
        return create_engine(db_url, poolclass=NullPool)

    @property
    def get_base(self):
        return declarative_base(bind=self.engine)

    def get_database(self):
        db = self.session_maker()
        try:
            yield db
        finally:
            db.close()
