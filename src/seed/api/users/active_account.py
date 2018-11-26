from flask import request

from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.cache.active_account import ActiveAccountCache
from seed.models.account import Account


class ActiveAccount(RestfulBaseView):
    """ 激活账户
    """
    url = 'active_account'
    access_methods = [HttpMethods.GET]

    def get(self):
        active_token = request.args.get('active_token')
        if not active_token:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='激活token参数缺失'
            )

        user_id = ActiveAccountCache().get_user_by_active_token(active_token)
        if not user_id:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='激活token已经失效'
            )

        account = self.session.query(Account).filter_by(id=user_id).first()
        if not account:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='激活账户不存在'
            )

        account.role = 'user'
        account.status = 1
        account.save()

        return self.response_json(self.HttpErrorCode.SUCCESS)
