from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView

from seed.models.account import Account as AccountModel


class AccountSchema(BaseSchema):
    class Meta:
        model = AccountModel

class Account(RestfulBaseView):
    """ Account
    """
    model_class = AccountModel
    schema_class = AccountSchema