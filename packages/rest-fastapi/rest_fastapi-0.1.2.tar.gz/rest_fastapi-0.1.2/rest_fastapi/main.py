import uvicorn

from rest_fastapi.core import engine, Base
from rest_fastapi.demo_api.controllers import router
from rest_fastapi.builder_api import InitFastApi, get_application
from rest_fastapi.log_settings import LOGGING_CONFIG

fast_api = InitFastApi()

fastapi_config = fast_api.settings.Fastapi.config

app = get_application()

app.include_router(router, prefix='/v1')

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    service_config = fast_api.settings.Service
    uvicorn.run(service_config.app, host=service_config.host, port=service_config.port, reload=True,
                log_config=LOGGING_CONFIG)
