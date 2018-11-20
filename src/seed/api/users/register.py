from flask import request
from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.schema.base import BaseSchema

from seed.models.account import Account


class AccountSchema(BaseSchema):
    """  账户
    """
    class Meta:
        model = Account


class Register(RestfulBaseView):
    """ 注册
    """
    access_methods = [HttpMethods.POST]

    def post(self):
        """ POST
        """
        input_json = request.get_json()

        datas, errors = AccountSchema().load(input_json, partial=True)
        if errors:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
        datas.save()

        # 登录, 写入cookie

        return self.response_json(self.HttpErrorCode.SUCCESS)
