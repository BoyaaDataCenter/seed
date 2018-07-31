from flask import request

from seed.models import db
from seed.api.common import _MethodView


class RestfulBaseView(_MethodView):
    """ BaseView for Restful style
    """
    __abstrcut__ = True

    pk = 'model_id'
    pk_type = 'string'

    session = db.session

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
            data = session.query(*self.rule['get']['single_columns']).filter_by(id=model_id).first_or_404()
            data = data.row2dict()
            return self.response_json(self.HttpErrorCode.SUCCESS, data={'data': data})
        
        # try:
        #     page = int(request.args.get('page', 1)) - 1
        #     size = int(request.args.get('szie', 20))

        #     if page < 0 or size < 0:
        #         return self.response_json(self.HttpErrorCode.ERROR, 'page and size params is wrong')
        # except ValueError:
        #     return self.response_json(self.HttpErrorCode.ERROR, 'page and size params is wrong')
        
        query_session = session.query(*self.rule['get']['list_columns'])
        data = query_session.all()
        return self.response_json(self.HttpErrorCode.ERROR, data={'data': data})
        
    def post(self):
        """ POST
        """
        pass
    
    def put(self, model_id):
        """ PUT
        
        Arguments:
            model_id {int} -- resource id
        """
        pass
    
    def delete(self, model_id):
        """ DELETE

        Arguments:
            model_id {int} -- resource id
        """
        model = self.models.query.filter_by(id=model_id).first()
        model.delete()

    @classmethod
    def register_api(cls, app):
        url = '/' + cls.__name__.lower()
        view_func = cls.as_view(cls.__name__.lower())

        app.add_url_rule(
            url, defaults={cls.pk: None},
            view_func=view_func, method=['GET'],
        )
        app.add_url_rule(url, view_func=view_func, method=['POST'])
        app.add_url_rule(
            '%s/<%s:%s>' % (url, cls.pk_type, cls.pk),
            view_func=view_func,
            method=['GET', 'PUT', 'DELETE']
        )

        return app