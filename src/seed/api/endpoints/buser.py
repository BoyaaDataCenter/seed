from flask import request, g
from sqlalchemy import and_

from seed.schema.base import BaseSchema
from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.models import BUser as BUserModel
from seed.models import Account as AccountModel
from seed.models import BManager as BManagerModel

from seed.models.role import Role
from seed.models.buserrole import BUserRole

from seed.utils.auth import api_require_admin


class BUserSchema(BaseSchema):
    class Meta:
        model = BUserModel
        include_fk = True


class Buser(RestfulBaseView):
    """ 用户业务映射关系添加
    """
    model_class = BUserModel
    schema_class = BUserSchema
    decorators = [api_require_admin]

    def get(self, bussiness_id):
        users = self.session.query(BUserModel.id, AccountModel)\
            .join(AccountModel, AccountModel.id == BUserModel.user_id)\
            .filter(BUserModel.bussiness_id == bussiness_id)\
            .all()

        datas = []
        for user in users:
            data = user.Account.row2dict()
            data['account_id'], data['id'] = data['id'], user.id
            data['brole'] = self._get_role(data['id'])

            datas.append(data)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)

    def _get_role(self, uid):
        roles = self.session.query(Role)\
            .join(BUserRole, and_(
                BUserRole.role_id == Role.id,
                BUserRole.user_id == uid,
                BUserRole.bussiness_id == g.bussiness_id)
            ).all()
        roles = [role.row2dict() for role in roles]
        return roles


class UnBuserList(RestfulBaseView):
    """ 不属于当前业务的用户名单
    """
    url = 'un_busers'
    decorators = [api_require_admin]
    access_methods = [HttpMethods.GET]

    def get(self):

        in_user_query = self.session.query(BUserModel.user_id)\
            .filter(BUserModel.bussiness_id == g.bussiness_id)

        b_managers_query = self.session.query(BManagerModel.user_id)\
            .filter(BManagerModel.bussiness_id == g.bussiness_id)

        users = self.session.query(AccountModel)\
            .filter(~AccountModel.id.in_(in_user_query))\
            .filter(~AccountModel.id.in_(b_managers_query))

        users = [user.row2dict() for user in users]
        return self.response_json(self.HttpErrorCode.SUCCESS, data=users)
