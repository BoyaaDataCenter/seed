from flask import request

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models import BUser as BUserModel

from seed.utils.auth import api_require_admin

class BUserSchema(BaseSchema):
    class Meta:
        model = BUserModel

class Buser(RestfulBaseView):
    """ 用户业务映射关系添加
    """
    model_class = BUserModel
    schema_class = BUserSchema
    deccorators = [api_require_admin]

    def put(self, bussiness_id):
        input_json = request.get_json()

        # 删除多余的数据
        delete_data = [data for data in input_json if data.get('status') == -1]
        datas, errors = self.schema_class().load(delete_data, many=True)
        [data.delete() for data in datas]

        # 新增和修改数据
        modify_data = [data for data in input_json if data.get('status') != -1]

        for data in modify_data:
            data['bussiness_id'] = bussiness_id

        datas, errors = self.schema_class().load(modify_data, many=True)
        [data.save() for data in datas]
        datas = [data.row2dict() for data in datas]

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)

    post = put