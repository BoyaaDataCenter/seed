import bcrypt
from flask import request

from seed.models.account import Account
from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.cache.reset_password import ResetPasswordCache
from seed.utils.mail import send_reset_password_email


class ForgetPassword(RestfulBaseView):
    """ 忘记密码, 发送重置密码的邮件
    """
    access_methods = [HttpMethods.POST]
    url = 'forget_password'

    def post(self):
        input_json = request.get_json()
        if 'account' not in input_json:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='account参数缺失'
            )
        account = input_json['account']

        if 'reset_url' not in input_json:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='reset_url参数缺失'
            )
        reset_url = input_json['reset_url']

        account_session = self.session.query(Account)

        if '@' in account:
            account = account_session.filter_by(email=account).first()
        else:
            account = account_session.filter_by(account=account).first()

        if not account:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='该账户不存在，请查证后再试'
            )

        reset_token = ResetPasswordCache().create_active_token(account.id)
        reset_redirect_url = '{active_host}/users/reset_password&reset_token={reset_token}'.format(active_host=request.host, reset_token=reset_token)
        send_reset_password_email(account.email, reset_url, reset_redirect_url)

        return self.response_json(self.HttpErrorCode.SUCCESS)


class ResetPasssword(RestfulBaseView):
    """ 重置密码
    """
    access_methods = [HttpMethods.POST]
    url = 'reset_password'

    def post(self):
        input_json = request.get_json()
        if input_json['password'] != input_json['confirm_password']:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='密码和确认密码不一致'
            )

        if 'reset_token' not in input_json:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='reset_token参数不存在'
            )

        reset_account_id = ResetPasswordCache().get_user_by_active_token(input_json['reset_token'])
        account = self.session.query(Account).filter_by(id=reset_account_id).first()

        password = bcrypt.hashpw(input_json['password'].encode('utf-8'), bcrypt.gensalt())
        account.password = password
        account.save()

        return self.response_json(self.HttpErrorCode.SUCCESS)
