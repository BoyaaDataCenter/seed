from flask import request, g
from sqlalchemy.exc import InvalidRequestError

from seed.api.endpoints._base import RestfulBaseView, HttpMethods

from seed.models.filters import Filters as FiltersModel
from seed.api.endpoints.filters import FilterSchema
from seed.models.panels import Panels as PanelsModel
from seed.api.endpoints.panels import PanelSchema

from seed.utils.helper import common_batch_crud


class Pages(RestfulBaseView):
    """ 页面
    """
    access_methods = [HttpMethods.GET, HttpMethods.PUT]

    def get(self, page_id):
        global_filters = self._get_global_filters(page_id)
        panels = self._get_panels(page_id)

        data = {
            "global_filters": global_filters,
            "panels": panels
        }
        return self.response_json(self.HttpErrorCode.SUCCESS, data=data)

    def put(self, page_id):
        input_data = request.get_json()

        global_filters, panels = input_data['global_filters'], input_data['panels']
        for global_filter in global_filters:
            global_filter['bussiness_id'] = g.bussiness_id
        global_filters = common_batch_crud(FilterSchema, FiltersModel, global_filters)

        panels = self._panels_batch_crud(PanelSchema, panels)

        data = {'global_filters': global_filters, 'panels': panels}

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
        panels = panel_query_session.filter_by(page_id=page_id).order_by(PanelsModel.sort).all()
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

    def _panels_batch_crud(self, panel_schema, panels):
        schema_instance = panel_schema()

        # 删除panels
        saved_panels = []
        for panel in panels:
            one_panel, errors = schema_instance.load(panel)
            if errors:
                raise Exception(errors)

            if panel.get('status') == -1:
                # 删除对应的panel
                try:
                    one_panel.delete()
                except InvalidRequestError:
                    pass

            else:
                # 新增和修改对应的panel
                one_panel.save()
                panel_filters = panel.get('filters', [])

                for filter in panel_filters:
                    filter['belong_id'] = one_panel.id
                    filter['bussiness_id'] = g.bussiness_id
                    filter['page_id'] = one_panel.page_id

                panel_filters = common_batch_crud(FilterSchema, FiltersModel, panel_filters)
                panel, errors = panel_schema(exclude=PanelsModel.column_filter).dump(one_panel)
                panel['filters'] = panel_filters
                saved_panels.append(panel)
        return saved_panels
