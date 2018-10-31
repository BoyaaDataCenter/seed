import json

from flask import request, g

from seed.api.endpoints._base import RestfulBaseView, HttpMethods

from seed.models.filters import Filters as FiltersModel
from seed.api.endpoints.filters import FilterSchema
from seed.models.panels import Panels as PanelsModel
from seed.api.endpoints.panels import PanelSchema

from seed.utils.auth import api_require_login


class Pages(RestfulBaseView):
    """ 页面
    """
    access_methods = [HttpMethods.GET]

    def get(self, page_id):
        global_filters = self._get_global_filters(page_id)
        panels = self._get_panels(page_id)

        data = {
            "global_filters": global_filters,
            "panels": panels
        }
        return self.response_json(self.HttpErrorCode.SUCCESS, data=data)

    def _get_global_filters(self, page_id):
        """ 获取页面全局过滤组件数据
        """
        query_session = self.session.query(FiltersModel)

        filters = query_session.filter_by(page_id=page_id, dtype='page').all()
        filters, errors = FilterSchema(many=True, exclude=FiltersModel.column_filter).dump(filters)

        return filters

    def _get_panels(self, page_id):
        """ 获取过滤组件数据
        """
        panel_query_session = self.session.query(PanelsModel)
        panels = panel_query_session.filter_by(page_id=page_id).all()
        panels, errors = PanelSchema(many=True, exclude=PanelsModel.column_filter).dump(panels)

        filter_query_session = self.session.query(FiltersModel)
        filters = filter_query_session.filter_by(page_id=page_id, dtype='model').all()
        filters, errors = FilterSchema(many=True, exclude=FiltersModel.column_filter).dump(filters)

        filters_pid_map = {}
        for filter in filters:
            filters_pid_map.setdefault(filter['belong_id'], []).append(filter)

        for panel in panels:
            panel['filters'] = filters_pid_map.get(panel['id'], [])

        return panels