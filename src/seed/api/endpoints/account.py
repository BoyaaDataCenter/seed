from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView

from seed.models.account import Account as AccountModel
from seed.utils.auth import api_require_admin


class AccountSchema(BaseSchema):
    class Meta:
        model = AccountModel

class Account(RestfulBaseView):
    """ Account
    """
    decorators = [api_require_admin]

    model_class = AccountModel
    schema_class = AccountSchema