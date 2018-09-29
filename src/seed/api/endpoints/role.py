from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.role import Role as RoleModel


class RoleSchema(BaseSchema):
    class Meta:
        model = RoleModel

class Role(RestfulBaseView):
    """ role
    """
    model_class = RoleModel
    schema_class = RoleSchema

    decorators = [api_require_super_admin]