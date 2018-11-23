import bcrypt
from flask import request, Response, make_response

from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.schema.base import BaseSchema
from seed.models.account import Account
from seed.cache.session import SessionCache


class AccountSchema(BaseSchema):
    """  账户
    """
    class Meta:
        model = Account


class Register(RestfulBaseView):
    """ 注册
    """
    access_methods = [HttpMethods.POST]

    def post(self):
        """ POST
        """
        input_json = request.get_json()

        if input_json['password'] != input_json['confirm_password']:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='密码和确认密码不一致'
            )

        if self.session.query(Account).filter_by(account=input_json['account']).first():
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='账号已经被占用了'
            )

        if self.session.query(Account).filter_by(email=input_json['email']).first():
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='邮箱已经被注册了'
            )

        input_json['password'] = bcrypt.hashpw(input_json['password'].encode('utf-8'), bcrypt.gensalt())

        account, errors = AccountSchema().load(input_json, partial=True)
        if errors:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
        account.save()

        # TODO 发送出邮箱请求
        pass

        # TODO 登录, 写入cookie
        res = make_response(self.response_json(self.HttpErrorCode.SUCCESS))

        session_token = SessionCache().create_session(account.id)
        res.set_cookie('session_token', session_token, expires=24 * 60 * 60)

        return res


class Activate(RestfulBaseView):
    """ 激活账号
    """
    def get(self, activate_token):
        pass
