from rest_fastapi.bases import BasicService
from rest_fastapi.demo_api.daos import DemoDao
from rest_fastapi.demo_api.models import Demo


class DemoService(BasicService):

    def __init__(self, operator_id=0):
        super(DemoService, self).__init__(operator_id)
        self.Model = Demo
        self.dao = DemoDao(operator_id)
        self.dao.Model = Demo


demo_service = DemoService()
