from flask import request, g

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.buserrole import BUserRole as BUserRoleModel
from seed.models.role import Role as RoleModel
from seed.utils.auth import api_require_login


class BUserRoleSchema(BaseSchema):
    class Meta:
        model = BUserRoleModel
        include_fk = True


class BUserRole(RestfulBaseView):
    """ 用户角色
    """
    model_class = BUserRoleModel
    schema_class = BUserRoleSchema
    decorators = [api_require_login]

    def get(self, model_id):
        query_session = self.session.query(self.model_class)
        datas = query_session.filter(self.model_class.user_id == model_id).all()
        datas = [row.row2dict() for row in datas] if datas else []

        roles = RoleModel.get_roles(g.bussiness_id)
        role_id_map = {role.id: role.role for role in roles}

        for data in datas:
            data['role'] = role_id_map.get(data['role_id'], '未知')

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)

    def put(self, model_id):
        input_json = request.get_json()

        # 删除旧数据
        query_session = self.session.query(self.model_class)
        query_session.filter(self.model_class.user_id == model_id).delete()
        self.session.commit()

        # 添加新数据
        datas, errors = self.schema_class().load(input_json, many=True)
        if errors:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
        [data.save() for data in datas]

        datas = [row.row2dict() for row in datas] if datas else []

        roles = RoleModel.get_roles(g.bussiness_id)
        role_id_map = {role.id: role.role for role in roles}

        for data in datas:
            data['role'] = role_id_map.get(data['role_id'], '未知')

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)