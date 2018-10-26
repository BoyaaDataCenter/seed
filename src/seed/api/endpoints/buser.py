from flask import request

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView
from seed.models import BUser as BUserModel
from seed.models import Account as AccountModel

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

    def get(self, bussiness_id):
        users = self.session.query(BUserModel.id, AccountModel)\
            .join(AccountModel, AccountModel.id==BUserModel.user_id)\
            .filter(BUserModel.bussiness_id==bussiness_id)\
            .all()

        datas = []
        for user in users:
            data = user.Account.row2dict()
            data['account_id'], data['id'] = data['id'], user.id
            datas.append(data)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)