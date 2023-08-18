from pathlib import Path

import uvicorn

from rest_fastapi.core import engine, Base
from rest_fastapi.demo_api.controllers import router
from rest_fastapi.builder_api import BuilderSettings, builder_fastapi
from rest_fastapi.log_settings import LOGGING_CONFIG

base_dir = Path(__file__).resolve().parent.parent

settings = BuilderSettings(base_dir, 'rest_fastapi/settings.conf')

fastapi_config = settings.settings.Fastapi.config

app = builder_fastapi()

app.include_router(router, prefix='/v1')

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    service_config = settings.settings.Service
    uvicorn.run(service_config.app, host=service_config.host, port=service_config.port, reload=True,
                log_config=LOGGING_CONFIG)
