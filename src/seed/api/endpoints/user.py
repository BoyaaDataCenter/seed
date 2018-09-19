from flask import current_app, g

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.account import Account as AccountModel
from seed.utils.auth import api_require_login

class UserSchema(BaseSchema):
    class Meta:
        model = AccountModel

class User(RestfulBaseView):
    """ 用户相关
    """
    model_class = AccountModel
    schema_class = UserSchema
    decorators = [api_require_login]

    def get(self, model_id=None):
        """ 获取用户信息, 如果是SSO的校验
        成功后自动添加用户信息到用户列表
        """
        user = g.user.row2dict()
        return self.response_json(self.HttpErrorCode.SUCCESS, data=user)


class Menu(RestfulBaseView):
    """ 获取当前用户的菜单
    """
    url = '/user/menu'

    def get(self):
        pass