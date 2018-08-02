from flask import request

from marshmallow import ValidationError

from seed.models import db
from seed.api.common import _MethodView


class RestfulBaseView(_MethodView):
    """ BaseView for Restful style
    """
    __abstract__ = True

    pk = 'model_id'
    pk_type = 'string'

    session = db.session

    model_class = None
    schema_class = None

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
        if model_id:
            data = self.session.query(*self.rule['get']['single_columns']).filter_by(id=model_id).first()
            data = data.row2dict() if data else {}
        else:
            query_session = self.session.query(*self.rule['get']['list_columns'])
            data = query_session.all()
            data = [row._asdict() for row in data] if data else []
        
        return self.response_json(self.HttpErrorCode.SUCCESS, data=data)
        
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
            return self.response_json(self.HttpErrorCode.ERROR, msg=errors)
        
        if isinstance(datas, list):
            [m.save() for m in datas]
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
            datas, errors = self.schema_class().load(input_json, instance=self.model_class.query.get(model_id))
            if errors:
                return self.response_json(self.HttpErrorCode.ERROR, msg=errors)

            datas.save()
        else:
            # TODO not finish
            raise NotImplementedError('No finish')
        
        return self.response_json(self.HttpErrorCode.SUCCESS)
    
    def delete(self, model_id):
        """ DELETE

        Arguments:
            model_id {int} -- resource id
        """
        data = self.model_class.query.get(model_id).first()
        if data:
            data.delete()
            return self.response_json(self.HttpErrorCode.SUCCESS, 'Success!')
        return self.response_json(self.HttpErrorCode.ERROR, 'The data is not exists!')

    @classmethod
    def register_api(cls, app):
        url = '/' + cls.__name__.lower()
        view_func = cls.as_view(cls.__name__.lower())

        app.add_url_rule(
            url, defaults={cls.pk: None},
            view_func=view_func, methods=['GET', 'PUT'],
        )
        app.add_url_rule(url, view_func=view_func, methods=['POST'])
        app.add_url_rule(
            '%s/<%s:%s>' % (url, cls.pk_type, cls.pk),
            view_func=view_func,
            methods=['GET', 'PUT', 'DELETE']
        )

        return app