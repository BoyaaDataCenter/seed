from flask.views import MethodView
from flask import jsonify, request

from seed.utils.response import response, HttpErrorCode


class _MethodView(MethodView):
    """ MethodView base package
    """
    __abstract__ = True

    HttpErrorCode = HttpErrorCode

    def __init__(self, *args, **kwargs):
        super(_MethodView, self).__init__(*args, **kwargs)

    def response_json(self, code, msg=None, data={}):
        return jsonify(response(code, msg, data))

    @classmethod
    def register_api(cls, app):
        raise NotImplementedError()
