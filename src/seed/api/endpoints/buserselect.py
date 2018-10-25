from flask import request, g, current_app
 
from seed.schema.base import BaseSchema
from seed.cache.user_bussiness import UserBussinessCache
from seed.api.endpoints._base import RestfulBaseView

from seed.utils.permissions import has_bussiness_permission


class BUserSelect(RestfulBaseView):
    """ 用户当前选择业务
    """
    def get(self):
        current_bussiness_id = g.bussiness_id
        return self.response_json(
            self.HttpErrorCode.SUCCESS,
            data={'bussiness_id': current_bussiness_id}
        )

    def post(self):
        input_json = request.get_json()
        bussiness_id = input_json['bussiness_id']
        if not has_bussiness_permission(g.user, bussiness_id):
            return self.response_json(self.HttpErrorCode.FORBIDDEN)

        UserBussinessCache().set(g.user.id, bussiness_id)
        return self.response_json(self.HttpErrorCode.SUCCESS)