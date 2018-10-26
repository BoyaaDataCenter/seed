from sqlalchemy import and_
from flask import current_app, g

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.models.account import Account as AccountModel
from seed.models.role import Role
from seed.models.buserrole import BUserRole
from seed.models.rolemenu import RoleMenu
from seed.models.menu import Menu as MenuModel
from seed.utils.auth import api_require_login, require_admin

class UserSchema(BaseSchema):
    class Meta:
        model = AccountModel

class User(RestfulBaseView):
    """ 用户相关
    """
    model_class = AccountModel
    schema_class = UserSchema
    decorators = [api_require_login]

    access_methods = [HttpMethods.GET]

    def get(self):
        """ 获取用户信息, 如果是SSO的校验
        成功后自动添加用户信息到用户列表
        """
        user = g.user.row2dict()
        user['brole'] = self._get_role(g.user.id)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=user)

    def _get_role(self, uid):
        roles = self.session.query(Role.role)\
            .join(BUserRole, and_(BUserRole.role_id==Role.id, BUserRole.user_id==uid, BUserRole.bussiness_id==1))\
            .all()
        return roles


class UserMenu(RestfulBaseView):
    """ 获取当前用户的菜单
    """
    url = '/user/menu'

    decorators = [api_require_login]

    access_methods = [HttpMethods.GET]

    def get(self):
        if require_admin():
            # 如果是业务管理员以上，返回当前业务的所有菜单
            query_session = self.session.query(MenuModel).filter(MenuModel.bussiness_id==g.bussiness_id)
        else:
            # 其他角色通过关联用户角色表来获取到当前的菜单
            # TODO 测试
            query_session = self.session.query(MenuModel)\
                .join(RoleMenu, and_(MenuModel.id==RoleMenu.menu_id, RoleMenu.bussiness_id==g.bussiness_id))\
                .join(BUserRole, and_(RoleMenu.role_id==BUserRole.role_id, BUserRole.bussiness_id==g.bussiness_id, BUserRole.user_id==g.user.id))\
                .all()

        menu_data = query_session.all()
        menus = self._encode_menus(menu_data)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=menus)

    def _encode_menus(self, menu_data):
        menu_data = {'-'.join([str(row.parent_id), str(row.left_id)]): row.row2dict() for row in menu_data}

        menus = {'id': 0}
        middle_menu = [menus]
        while middle_menu:
            current_menu = middle_menu.pop()
            parent_id, left_id = current_menu['id'], 0

            while True:
                current_key = '-'.join([str(parent_id), str(left_id)])
                if current_key not in menu_data:
                    break
                current_menu.setdefault('sub_menus', []).append(menu_data[current_key])
                middle_menu.append(menu_data[current_key])
                left_id = menu_data[current_key]['id']

        return menus.get('sub_menus', [])