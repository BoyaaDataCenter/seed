
from flask import request

# from seed.api.common import _MethodView
from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.drives import ALL_DRIVES


class DatabaseTypes(RestfulBaseView):
    url = 'database_types'

    access_methods = [HttpMethods.GET]

    def get(self):

        data = [{'value': drive, 'label': drive} for drive in ALL_DRIVES.keys()]
        return self.response_json(self.HttpErrorCode.SUCCESS, data=data)