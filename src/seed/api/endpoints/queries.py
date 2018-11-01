from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView, HttpMethods

from seed.api.endpoints.panels import PanelSchema, PanelsModel
from seed.api.endpoints.filters import FilterSchema, FiltersModel

from seed.utils.auth import api_require_login

from seed.libs.data_access.app import DataAccess
from seed.libs.filter_access.app import FilterAccess


class QueriesData(RestfulBaseView):
    """ 获取数据
    """
    decorators = [api_require_login]

    access_methods = [HttpMethods.POST]

    def post(self, panel_id=None):
        query_params = request.get_json()

        if panel_id:
            panel_data = self.session.query(PanelsModel).filter_by(id=panel_id).first()
            panel_data = PanelSchema(exclude=PanelsModel.column_filter).dump(panel_data)
        else:
            panel_data = {}

        panel_data = panel_data.update(query_params)

        try:
            query_datas = DataAccess(**panel_data)
        except Exception as e:
            error_message = str(e)
            return self.response_json(self.HttpErrorCode.ERROR, msg=error_message)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=query_datas)



class QueriesFilter(RestfulBaseView):
    """ 获取Filter数据
    """
    decorators = [api_require_login]

    access_methods = [HttpMethods.GET]

    def get(self, filter_id=None):
        query_params = request.get_json()

        if filter_id:
            filter_data = self.session.query(FiltersModel).filter_by(id=filter_id).first()
            filter_data = FilterSchema(exclude=FiltersModel.column_filter).dump(filter_data)
        else:
            filter_data = {}

        if not filter_data:
            return self.response_json(self.HttpErrorCode.ERROR, msg='过滤设置不能为空')

        if filter_data['condition_type'] in ('sql'):
            filter_data['conditions'] = FilterAccess(filter_data['conditions'])

        return self.response_json(self.HttpErrorCode.SUCCESS, data=filter_data)