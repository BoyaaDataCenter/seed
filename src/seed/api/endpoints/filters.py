import json

from flask import request, g
from marshmallow import pre_load, post_dump

from seed.schema.base import BaseSchema

from seed.api.endpoints._base import RestfulBaseView

from seed.models.filters import Filters as FiltersModel
from seed.utils.auth  import api_require_login


class FilterSchema(BaseSchema):
    class Meta:
        model = FiltersModel

    @post_dump(pass_many=True)
    def dumps_index(self, in_data, many):
        if many:
            for data in in_data:
                data['conditions'] = json.loads(data['conditions'])
                data['cascades'] = json.loads(data['cascades'])
        else:
            in_data['conditions'] = json.loads(in_data['conditions'])
            in_data['cascades'] = json.loads(in_data['cascades'])

        return in_data

    @pre_load(pass_many=True)
    def loads_conditions(self, out_data, many):
        if many:
            for data in out_data:
                data['conditions']  = json.dumps(data['conditions'])
                data['cascades'] = json.dumps(data['cascades'])
        else:
            out_data['conditions']  = json.dumps(out_data['conditions'])
            out_data['cascades'] = json.dumps(out_data['cascades'])
        return out_data

class Filters(RestfulBaseView):
    """ 过滤组件
    """
    model_class = FiltersModel
    schema_class = FilterSchema
    decorators = [api_require_login]