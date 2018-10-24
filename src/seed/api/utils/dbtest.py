from flask import request

from seed.api.endpoints._base import RestfulBaseView, HttpMethods

class DatabaseTest(RestfulBaseView):
    url = 'database_test'

    access_methods = [HttpMethods.POST]

    def post(self):
        input_json = request.get_json()

        return self.response_json(self.HttpErrorCode.SUCCESS)
