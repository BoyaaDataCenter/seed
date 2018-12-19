from flask import g
from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView, HttpMethods

from seed.models.account import Account as AccountModel
from seed.utils.auth import api_require_user, require_super_admin


class AccountSchema(BaseSchema):
    class Meta:
        model = AccountModel


class Account(RestfulBaseView):
    """ Account
    """
    model_class = AccountModel
    schema_class = AccountSchema

    access_methods = [HttpMethods.GET, HttpMethods.PUT, HttpMethods.DELETE]

    decorators = [api_require_user]

    def put(self, model_id=None):
        if not require_super_admin() and g.user.id != int(model_id): 
            return self.response_json(self.HttpErrorCode.FORBIDDEN)

        return super(Account, self).put(model_id=model_id)

    def delete(self, model_id):
        if not require_super_admin():
            return self.response_json(self.HttpErrorCode.FORBIDDEN)

        return super(Account, self).delete(model_id=model_id)
