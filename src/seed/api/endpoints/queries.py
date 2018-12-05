
from flask import request

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView, HttpMethods

from seed.api.endpoints.panels import PanelSchema, PanelsModel
from seed.api.endpoints.filters import FilterSchema, FiltersModel
from seed.api.endpoints.databases import DatabasesSchema

from seed.models._base import session
from seed.models.databases import Databases

from seed.utils.auth import api_require_login
from seed.utils.database import get_db_instance

from seed.libs.data_access.app import DataAccess
from seed.libs.filter_access.app import FilterAccess


class QueryData(RestfulBaseView):
    """ 获取数据
    """
    url = 'query_data'
    decorators = [api_require_login]

    access_methods = [HttpMethods.POST]

    def post(self, panel_id=None):
        try:
            query_params = request.get_json()
        except:
            query_params = {}

        if panel_id:
            panel_data = self.session.query(PanelsModel).filter_by(id=panel_id).first()
            panel_data, errors = PanelSchema(exclude=PanelsModel.column_filter).dump(panel_data)
            if errors:
                return self.response_json(self.HttpErrorCode.ERROR, msg=str(errors))
        else:
            panel_data = {}

        panel_data.update(query_params)

        try:
            dtype, db = get_db_by_id(panel_data['db_source'])
            query_datas = DataAccess(dtype, db, **panel_data).get_datas()
        except Exception as e:
            error_message = str(e)
            return self.response_json(self.HttpErrorCode.ERROR, msg=error_message)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=query_datas)


class QueryFilters(RestfulBaseView):
    """ 获取Filters数据
    """
    url = 'query_filters'
    decorators = [api_require_login]

    access_methods = [HttpMethods.POST]

    def post(self, filter_id=None):
        try:
            query_params = request.get_json()
        except:
            query_params = {}

        if filter_id:
            filter_data = self.session.query(FiltersModel).filter_by(id=filter_id).first()
            filter_data, errors = FilterSchema(exclude=FiltersModel.column_filter).dump(filter_data)
            if errors:
                return self.response_json(self.HttpErrorCode.ERROR, msg=str(errors))
        else:
            filter_data = {}

        filter_data.update(query_params)

        if not filter_data:
            return self.response_json(self.HttpErrorCode.ERROR, msg='过滤设置不能为空')

        if filter_data['condition_type'] in ('sql'):
            try:
                dtype, db = get_db_by_id(filter_data['db_source'])
            except Exception as e:
                error_message = str(e)
                return self.response_json(self.HttpErrorCode.ERROR, msg=error_message)

            filter_data['conditions'] = FilterAccess(db, filter_data['conditions'], filter_data.get('query', {})).query_datas()

        return self.response_json(self.HttpErrorCode.SUCCESS, data=filter_data)


def get_db_by_id(db_source):
    db_data = session.query(Databases).filter_by(id=db_source).first()
    db_conf, errors = DatabasesSchema().dump(db_data)
    if errors:
        raise Exception(errors)

    db = get_db_instance(**db_conf)
    return db_conf['dtype'], db