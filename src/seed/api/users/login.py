import time
import bcrypt

from flask import request, make_response

from seed.models.account import Account
from seed.cache.session import SessionCache

from seed.api.endpoints._base import RestfulBaseView, HttpMethods


class Login(RestfulBaseView):
    """ 登录
    """
    access_methods = [HttpMethods.POST]

    def post(self):
        """ POST
        """
        input_json = request.get_json()
        if 'account' not in input_json:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, '账号不能为空')

        if 'password' not in input_json:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, '密码不能为空')

        account, password = input_json.get('account'), input_json.get('password')

        # 获取账号
        account = Account.query.filter_by(account=account).first()

        if not bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
            return self.response_json(self.HttpErrorCode.AUTHORIZED_ERROR)

        # Cookie设置
        res = make_response(self.response_json(self.HttpErrorCode.SUCCESS))

        session_token = SessionCache().create_session(account.id)
        res.set_cookie(
            'session_token',
            session_token,
            expires=time.time()+24*60*60,
            domain=request.host
        )

        return res


class Logout(RestfulBaseView):
    """ 登出
    """
    access_methods = [HttpMethods.GET]

    def get(self):
        session_token = request.cookies.get('session_token', None)
        if not session_token:
            return self.response_json(self.HttpErrorCode.SUCCESS)

        SessionCache().delete(session_token)

        res = make_response(self.response_json(self.HttpErrorCode.SUCCESS))
        res.set_cookie('session_token', session_token, expires=0)

        return res
