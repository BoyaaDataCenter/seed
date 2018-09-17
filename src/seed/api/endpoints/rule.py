from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.rule import Rule


class RuleSchema(BaseSchema):
    class Meta:
        model = Rule

class Rule(RestfulBaseView):
    """ rule
    """
    model_class = Rule
    schema_class = RuleSchema

    rule = {
        'get': {
            'single_columns': [model_class],
            'list_columns': [model_class.id, model_class.rule]
        },
    }
