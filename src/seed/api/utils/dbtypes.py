
from flask import request

# from seed.api.common import _MethodView
from seed.api.endpoints._base import RestfulBaseView, HttpMethods

class DatabaseTypes(RestfulBaseView):
    url = 'database_types'

    access_methods = [HttpMethods.GET]

    def get(self):

        data = [
            {'value': 'MySQL', 'label': 'MySQL'},
            {'value': 'PostgreSQL', 'label': 'PostgreSQL'}
        ]

        return self.response_json(self.HttpErrorCode.SUCCESS, data=data)