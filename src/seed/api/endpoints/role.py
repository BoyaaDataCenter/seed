from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.role import Role as RoleModel
from seed.utils.auth import api_require_admin


class RoleSchema(BaseSchema):
    class Meta:
        model = RoleModel
        include_fk = True


class Role(RestfulBaseView):
    """ role
    """
    model_class = RoleModel
    schema_class = RoleSchema

    decorators = [api_require_admin]