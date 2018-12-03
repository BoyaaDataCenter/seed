import json
import logging
import functools
from datetime import datetime

import requests
from flask import current_app, jsonify, g, request

from seed.utils.response import response, HttpErrorCode
from seed.models.account import Account
from seed.models.bmanager import BManager
from seed.cache import DefaultCache
from seed.cache.session import SessionCache
from seed.cache.user_bussiness import UserBussinessCache


class APIRequireRole(object):
    roles = {
        "new": 0,
        "user": 1,
        "admin": 2,
        "super_admin": 3
    }

    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                # 未登录
                return jsonify(response(HttpErrorCode.UNAUTHORIZED))

            if g.user.status == -1:
                # 废弃账号
                return jsonify((response(HttpErrorCode.FORBIDDEN)))

            if not self.role or g.user.id == 1:
                return method(*args, **kwargs)

            if self.roles[g.user.role] < self.roles[self.role]:
                # 没有足够的权限
                return jsonify(response(HttpErrorCode.FORBIDDEN))

            return method(*args, **kwargs)

        return wrapper


api_require_login = APIRequireRole(None)
api_require_new = APIRequireRole("new")
api_require_user = APIRequireRole("user")
api_require_admin = APIRequireRole("admin")
api_require_super_admin = APIRequireRole("super_admin")


class RequireRole(object):
    roles = {
        "new": 0,
        "user": 1,
        "admin": 2,
        "super_admin": 3
    }

    def __init__(self, role):
        self.role = role

    def __call__(self):
        if not g.user:
            # 未登录
            return False

        if g.user.status == -1:
            # 废弃账号
            return False

        if not self.role or g.user.id == 1:
            return True

        if self.roles[g.user.role] < self.roles[self.role]:
            # 没有足够的权限
            return False

        return True


require_login = RequireRole(None)
require_new = RequireRole("new")
require_user = RequireRole("user")
require_admin = RequireRole("admin")
require_super_admin = RequireRole("super_admin")


class BaseAuth(object):
    """ 验证基础类
    """
    def get_current_user(self):
        """ 获取当前用户
        """
        raise NotImplementedError("Not Implemented")

    def login_user(self, user):
        """ 登录用户
        """
        raise NotImplementedError("Not Implemented")

    def logout_user(self):
        """ 登出用户
        """
        raise NotImplementedError("Not Implemented")

    def debbuger_user(self):
        if not require_super_admin() or 'debugger' not in request.args:
            return g.user

        user = Account.query.filter_by(id=int(request.args['debugger'])).first()

        if user:
            bussiness_id = UserBussinessCache().get(user.id) or 1
            if self._is_bussiness_admin(user.id, bussiness=bussiness_id):
                user.role = 'admin'

        return user if user else None

    def _is_bussiness_admin(self, uid, bussiness=1):
        roles = BManager.query.filter_by(bussiness_id=bussiness, user_id=uid).all()
        return True if roles else False


class SessionAuth(BaseAuth):
    """ Session登录权限类
    """
    def get_current_user(self):
        session_token = request.cookies.get('session_token', '')
        user_id = SessionCache().get_user_id_by_token(session_token)
        if not user_id:
            return None

        user = Account.query.filter_by(id=user_id).first()
        if user:
            bussiness_id = UserBussinessCache().get(user.id) or 1
            # TODO 需要修复db.model自动保存的问题
            if self._is_bussiness_admin(user.id, bussiness=bussiness_id) and user.role != 'super_admin':
                user.role = 'admin'

            user.role = 'super_admin' if user.id == 1 else user.role

        return user


class SSOAuth(BaseAuth):
    """ SSO权限校验登录类
    """
    def get_current_user(self):
        # 获取当前用户信息在redis中存储的信息
        uid = request.cookies.get('admin_uid', None)
        uid_key = request.cookies.get('admin_key', None)

        if not (uid and uid_key):
            return None

        # 判断信息的有效性
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        login_at = self._get_login_cache(uid)
        if today != login_at:
            # 去SSO中校验用户的有效性
            user_info = self._sso_verification(uid, uid_key)
            if not user_info:
                return None

            # 创建新用户 或者 获取用户的user_id
            user = self._get_user_id(user_info)

            self._account_valid(user)

            # 存储用户信息到Redis中
            self._set_login_cache(uid, today)
        else:
            user = Account.query.filter_by(sso_id=int(uid)).first()

        if user:
            bussiness_id = UserBussinessCache().get(user.id) or 1
            if self._is_bussiness_admin(user.id, bussiness=bussiness_id) and user.role != 'super_admin':
                user.role = 'admin'

            user.role = 'super_admin' if user.id == 1 else user.role

        return user

    def logout_user(self):
        session = []

    def cache(self):
        return DefaultCache(current_app.cache)

    def _account_valid(self, user):
        if user.status == -1:
            raise Exception("账号已经被注销")

    def _get_user_id(self, user_info):
        account = Account.query.filter_by(sso_id=int(user_info['id'])).first()
        if not account:
            # 创建信息用户
            account = Account(
                sso_id=int(user_info['id']),
                account=user_info['username'],
                email=user_info['email'],
                avatar='http://oahead-static.17c.cn/oahead/' + str(int(user_info['code'])) + '.png',
                name=user_info['cname'],
                role='user',
                status=1
            )
        else:
            account.login_at = datetime.utcnow()
        account.save()
        return account

    def _sso_verification(self, uid, uid_key):
        check_sso_user_url = "http://sso.ifere.com:8871/api?do=getInfo&uid=%s&key=%s&appid=1172" % (uid, uid_key)

        try:
            data_str = requests.get(check_sso_user_url, timeout=5)
            ret = json.loads(data_str.text)

            if "ret" not in ret or '1' != str(ret['ret']):
                logging.warning('user is invalid uid:%s uid_key:%s' % (uid, uid_key))
                return []

            return ret
        except Exception as e:

            logging.warning('error: %s' % e)
            return []

    def _set_login_cache(self, uid, login_at):
        self.cache().set(':'.join([uid, 'sso_login']), login_at)

    def _get_login_cache(self, uid):
        return self.cache().get(':'.join([uid, 'sso_login']))
