import inspect

from flask import request, g
from marshmallow import ValidationError

from seed.models import db
from seed.api.common import _MethodView
from seed.models._base import BussinessModel

RESTFUL_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


class HttpMethods(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class RestfulBaseView(_MethodView):
    """ BaseView for Restful style
    """
    __abstract__ = True

    pk_type = 'string'

    session = db.session

    model_class = None
    schema_class = None

    access_methods = [HttpMethods.GET, HttpMethods.POST, HttpMethods.PUT, HttpMethods.DELETE]

    def __init__(self, *args, **kwargs):
        super(RestfulBaseView, self).__init__(*args, **kwargs)

    def get(self, model_id=None):
        """ GET
        GET /base
        get paragraph node list

        GET /base/<model_id>
        get single node which id is model_id

        Arguments:
            model_id {int} -- resource id
        """
        query_session = self.session.query(self.model_class)

        if issubclass(self.model_class, BussinessModel):
            query_session = query_session.filter_by(bussiness_id=g.bussiness_id)

        if model_id:
            data = query_session.filter_by(id=model_id).first()
            data = self.schema_class(exclude=self.model_class.column_filter).dump(data)
        else:
            data = query_session.all()
            data = self.schema_class(many=True, exclude=self.model_class.column_filter).dump(data)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=data.data)

    def post(self):
        """ POST
        """
        input_json = request.get_json()

        if isinstance(input_json, list):
            schema = self.schema_class(many=True)
        else:
            schema = self.schema_class()
        datas, errors = schema.load(input_json)

        if errors:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)

        if isinstance(datas, list):
            [data.save() for data in datas]
        else:
            datas.save()
        return self.response_json(self.HttpErrorCode.SUCCESS)

    def put(self, model_id=None):
        """ PUT

        Arguments:
            model_id {int} -- resource id
        """
        input_json = request.get_json()
        if model_id:
            datas, errors = self.schema_class().load(
                input_json, instance=self.model_class.query.get(model_id), partial=True
            )
            if errors:
                return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
            datas.save()
            datas = self.schema_class().dump(datas)
        else:
            datas, errors = self.schema_class().load(input_json, many=True)
            if errors:
                return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)

            [data.save() for data in datas]
            datas = self.schema_class().dump(datas, many=True)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas.data)

    def delete(self, model_id):
        """ DELETE

        Arguments:
            model_id {int} -- resource id
        """
        data = self.model_class.query.get(model_id)
        if data:
            data.delete()
            return self.response_json(self.HttpErrorCode.SUCCESS, 'Success!')
        return self.response_json(self.HttpErrorCode.ERROR, 'The data is not exists!')

    @classmethod
    def register_api(cls, app):
        if hasattr(cls, 'url'):
            url = cls.url or '/' + cls.__name__.lower()
        else:
            url = cls.__name__.lower()

        view_func = cls.as_view(cls.__name__.lower())

        for method in RESTFUL_METHODS:
            if method not in cls.access_methods:
                continue

            method_params = inspect.signature(getattr(cls, method.lower())).parameters
            defaults = {
                param_key: param_value.default
                for param_key, param_value in method_params.items()
                if param_key != 'self' and param_value.empty is not param_value.default
            }
            pk = list(method_params.keys())[1] if len(method_params.keys()) > 1 else ''

            if defaults:
                app.add_url_rule(
                    url, defaults=defaults,
                    view_func=view_func,
                    methods=[method],
                )
                app.add_url_rule(
                    '%s/<%s:%s>' % (url, cls.pk_type, pk),
                    view_func=view_func,
                    methods=[method]
                )
            elif len(method_params) > 1:
                app.add_url_rule(
                    '%s/<%s:%s>' % (url, cls.pk_type, pk),
                    view_func=view_func,
                    methods=[method]
                )
            else:
                app.add_url_rule(
                    url,
                    view_func=view_func, methods=[method]
                )

        return app
