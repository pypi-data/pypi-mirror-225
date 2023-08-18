from rest_fastapi.bases import BasicDao
from rest_fastapi.demo_api.models import Demo


class DemoDao(BasicDao):
    Model = Demo
