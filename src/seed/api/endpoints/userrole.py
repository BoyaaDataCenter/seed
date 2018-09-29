from flask import request

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models.userrole import UserRole as UserRoleModel
from seed.utils.auth import api_require_login


class UserRoleSchema(BaseSchema):
    class Meta:
        model = UserRoleModel

class UserRole(RestfulBaseView):
    """ 用户角色
    """
    model_class = UserRoleModel
    schema_class = UserRoleSchema
    decoraters = [api_require_login]

    def get(self, model_id):
        query_session = self.session.query(self.model_class)
        datas = query_session.filter(self.model_class.user_id==model_id).all()
        datas = [row.row2dict() for row in datas] if datas else []

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)

    def put(self, model_id):
        input_json = request.get_json()

        # 删除旧数据
        query_session = self.session.query(self.model_class)
        query_session.filter(self.model_class.user_id==model_id).delete()
        self.session.commit()

        # 添加新数据
        datas, errors = self.schema_class().load(input_json, many=True)
        if errors:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
        [data.save() for data in datas]

        datas = [row.row2dict() for row in datas] if datas else []

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)