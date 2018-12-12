import json

from flask import request, g
from marshmallow import pre_load, post_dump

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView

from seed.models.panels import Panels as PanelsModel
from seed.utils.auth  import api_require_admin


class PanelSchema(BaseSchema):
    class Meta:
        model = PanelsModel
        include_fk = True

    @post_dump(pass_many=True)
    def dumps_indexs(self, in_data, many):
        if many:
            for data in in_data:
                data['indexs'] = json.loads(data['indexs'])
                data['dimensions'] = json.loads(data['dimensions'])
        else:
            in_data['indexs'] = json.loads(in_data['indexs'])
            in_data['dimensions'] = json.loads(in_data['dimensions'])

        return in_data

    @pre_load
    def loads_indexs(self, out_data):
        out_data['indexs'] = json.dumps(out_data['indexs'])
        out_data['dimensions'] = json.dumps(out_data['dimensions'])
        return out_data


class Panels(RestfulBaseView):
    """ 数据面板
    """
    model_class = PanelsModel
    schema_class = PanelSchema
    decorators = [api_require_admin]