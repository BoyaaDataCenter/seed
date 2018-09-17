from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.api.endpoints.rule import Rule
from seed.models import Bussiness as BussinessModel


class BussinessSchema(BaseSchema):
    class Meta:
        model = BussinessModel


class Bussiness(RestfulBaseView):
    """ bussiness
    """
    model_class = BussinessModel
    schema_class = BussinessSchema

    rule = {
        'get': {
            'single_columns': [model_class],
            'list_columns': [model_class],
        }
    }
