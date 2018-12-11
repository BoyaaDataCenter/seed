import bcrypt
from flask import request

from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.cache.active_account import ActiveAccountCache
from seed.schema.base import BaseSchema
from seed.models.account import Account
from seed.utils.mail import send_active_email


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

        if 'active_url' not in input_json:
            return self.response_json(
                self.HttpErrorCode.PARAMS_VALID_ERROR,
                msg='active_url缺失'
            )
        active_url = input_json['active_url']

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

        active_token = ActiveAccountCache().create_active_token(account.id)
        redirect_url = '{active_host}/users/active_account&active_token={active_token}'.format(active_host=request.host, active_token=active_token)
        try:
            send_active_email(account.email, active_url, redirect_url)
        except Exception as e:
            # 如果邮件发送失败，则放弃邮件验证
            print(e)
            account.role = 'user'
            account.save()

        return self.response_json(self.HttpErrorCode.SUCCESS)
