import logging
import os
from typing import Union, Dict
from configparser import ConfigParser
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logging.basicConfig(format=f'%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

FASTAPI_SETTINGS_MODULE = 'FASTAPI_SETTINGS_MODULE'


def set_settings_module(module: str = 'settings.conf'):
    os.environ.setdefault(FASTAPI_SETTINGS_MODULE, module)


def get_application(deploy: Union[Dict, FastAPI] = None):
    if deploy is not None:
        if isinstance(deploy, FastAPI):
            return deploy
        _app = FastAPI(**deploy)
    else:
        _app = FastAPI(**InitFastApi().settings.Fastapi.config)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @_app.exception_handler(RequestValidationError)
    async def handle_param_unresolved(request: Request, ex: RequestValidationError):
        """
        参数校验异常处理器
        """
        logging.warning('request body [%s]', ex.body)
        return JSONResponse(
            content={
                'msg': '参数校验失败',
                'code': -1,
                'data': ex.errors()
            },
            status_code=200
        )

    @_app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

    @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)

    return _app


class InitFastApi:
    base_dir = None
    default_setting = 'rest_fastapi/settings.conf'

    def __new__(cls, *args, **kwargs):
        cls.base_dir = Path(__file__).resolve().parent.parent
        cls.conf_path = os.path.join(cls.base_dir, cls.base_dir, cls.default_setting)
        cls.parser = ConfigParser()
        return super(InitFastApi, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        self.engine = None
        self.replace_configuration()
        self.settings = self.mount_configuration()

    def replace_configuration(self):
        self.parser.read(self.conf_path)
        new_settings = os.getenv(FASTAPI_SETTINGS_MODULE, None)
        if new_settings is None:
            return
        try:
            new_parser = ConfigParser()
            new_conf_path = os.path.join(self.base_dir, self.base_dir, new_settings)
            new_parser.read(new_conf_path)
            for section in new_parser.sections():
                if self.parser.has_section(section):
                    for option in new_parser.options(section):
                        if self.parser.has_option(section, option):
                            value = new_parser.get(section, option)
                            self.parser.set(section, option, value)
                            logger.info('加载配置 {}.{}={} 成功'.format(section, option, value))
                        else:
                            logger.warning('配置异常 异常信息:{}- {}'.format(section, option))
                else:
                    self.parser.add_section(section)
                    [self.parser.set(section, option, new_parser.get(section, option)) for option in
                     new_parser.options(section)]
        except Exception as e:
            logger.error('配置文件异常 错误信息:{}'.format(e))
        return

    def mount_configuration(self):

        class BaseSettings:

            class Service:
                app = self.parser.get('service', 'app')
                host = self.parser.get('service', 'host')
                port = self.parser.getint('service', 'port')

            class Fastapi:
                config = {}
                section = 'fastapi'
                if self.parser.has_section(section):
                    for option in self.parser.options(section):
                        value = self.parser.get(section, option)
                        if value in ['true', 'false']:
                            value = bool(value)
                        elif value == 'null':
                            value = None
                        config[option] = value

            if self.parser.has_section('mysql'):
                class Mysql:
                    username = self.parser.get('mysql', 'username')
                    password = self.parser.get('mysql', 'password')
                    host = self.parser.get('mysql', 'host')
                    port = self.parser.getint('mysql', 'port')
                    database = self.parser.get('mysql', 'database')
            else:
                class Sqlit:
                    path = '/sqlit.db'
                    if self.parser.has_section('sqlit') and self.parser.has_option('sqlit', 'path'):
                        path = self.parser.get('sqlit', 'path')

        class Settings(BaseSettings):
            ...

        return Settings()
