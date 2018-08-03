from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models import Bussiness


class BussinessSchema(BaseSchema):
    class Meta:
        model = Rule
    

class Bussiness(RestfulBaseView):
    """ bussiness
    """
    model_class = Bussiness
    schema_class = BussinessSchema

    rule = {
        'get': {
            'single_columns': [model_class],
            'list_columns': [model_class],
        }
    }
