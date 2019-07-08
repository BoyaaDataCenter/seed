import json
from flask import request, g
from sqlalchemy import and_

from seed.schema.base import BaseSchema
from seed.api._base import RestfulBaseView, HttpMethods
from seed.models.rolemenu import RoleMenu as RoleMenuModel
from seed.models.menu import Menu as MenuModel
from seed.utils.auth import api_require_admin


class RoleMenuSchema(BaseSchema):
    class Meta:
        model = RoleMenuModel
        include_fk = True


class RoleMenu(RestfulBaseView):
    """ 角色菜单设置
    """
    model_class = RoleMenuModel
    schema_class = RoleMenuSchema

    decorators = [api_require_admin]

    access_methods = [HttpMethods.GET, HttpMethods.PUT]

    def get(self, role_id):
        """ GET
        """
        role_menu = self._get_role_menu(role_id)

        menus = self._encode_menus(role_menu)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=menus)

    def put(self, role_id):
        request_json = request.get_json()
        menus = request_json['menu']
        self._decode_menus(menus, role_id)
        return self.response_json(self.HttpErrorCode.SUCCESS)

    def _get_role_menu(self, model_id):
        role_datas = self.session.query(RoleMenuModel)\
            .filter(RoleMenuModel.role_id == model_id, RoleMenuModel.bussiness_id == g.bussiness_id).all()
        role_data_map = {role_data.menu_id: role_data for role_data in role_datas}

        menu_datas = self.session.query(MenuModel)\
            .filter(MenuModel.bussiness_id == g.bussiness_id).all()

        menu_datas_with_permission = {}

        for menu_data in menu_datas:
            menu_data = menu_data.row2dict()
            role_data = role_data_map[menu_data['id']] if menu_data['id'] in role_data_map else None

            menu_data['role_permission'] = role_data.role_permission if role_data else False
            menu_data['menu_id'] = menu_data['id']
            if role_data:
                menu_data['id'] = role_data.id
            else:
                menu_data['id'] = None

            menu_datas_with_permission['-'.join([str(menu_data['parent_id']), str(menu_data['left_id'])])] = menu_data

        return menu_datas_with_permission

    def _encode_menus(self, menu_data):
        menu_list = []
        for key, value in menu_data.items():
            if not value.get('id'):
                value.pop('id')

            menu_list.append(value)

        return menu_list

    def _decode_menus(self, menus, role_id, parent_id=0, left_id=0):
        if not menus:
            return

        for menu in menus:
            # 更新或插入新的菜单
            # 获取到菜单对应的ID
            # if menu.get('role_permission', False):
            self._insert_or_update_menu(menu, role_id, menu.get('role_permission', False))
            current_id = menu['menu_id']
            self._decode_menus(menu.get('sub_menus', []), role_id=role_id, parent_id=current_id, left_id=0)

    def _insert_or_update_menu(self, menu, role_id, role_permission):
        role_menu = {
            "role_id": role_id,
            "menu_id": menu['menu_id'],
            "role_permission": role_permission
        }
        if 'id' in menu:
            role_menu['id'] = menu['id']
        schema = self.schema_class()
        datas, errors = schema.load(role_menu)
        datas.save()
        return datas.id
