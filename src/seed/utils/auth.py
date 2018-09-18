import functools
from datetime import datetime

from flask import session, current_app, jsonify

from seed.utils.response import response, HttpErrorCode
from seed.models.account import Account
from seed.cache import DefaultCache

class APIRequireRole(object):
    roles = {
        "new": 0,
        "user": 1,
        "admin": 2,
        "superadmin": 3
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

            if self.roles[g.user.role] <= self.roles[self.role]:
                # 没有足够的权限
                return jsonify(response(HttpErrorCode.FORBIDDEN))

            return method(*args, **kwargs)
        
        return wrapper

api_require_login = APIRequireRole(None)
api_require_new = APIRequireRole("new")
api_require_user = APIRequireRole("user")
api_require_admin = APIRequireRole("admin")
api_require_super_admin = APIRequireRole("super_admin")


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


class SessionAuth(BaseAuth):
    """ Session登录权限类
    """
    pass


class SSOAuth(BaseAuth):
    """ SSO权限校验登录类
    """
    def get_current_user(self):
        # 获取当前用户信息在redis中存储的信息
        uid = session.get('uid', None)
        uid_key = session.get('uid_key', None)

        if not (uid and uid_key):
            return None

        # 判断信息的有效性
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        login_data = self._get_login_cache(uid) 
        login_at = login_data['login_at']
        if today != login_at:
            # 去SSO中校验用户的有效性
            user_info = self._sso_verification(uid, uid_key)
            if not user_info:
                return None
            # 创建新用户 或者 获取用户的user_id
            user = self._get_user_id(user_info)
            # 存储用户信息到Redis中
            self._set_login_cache(uid, login_at)
        else:
            user = Account.query.filter_by(sso_id=int(uid)).first()
        return user

    def logout_user(self):
        session = []
    
    def cache(self):
        return DefaultCache(current_app.cache)

    def _get_user_id(self, user_info):
        account = Account.query.filter_by(sso_id=int(user_info['id'])).first()
        if not account:
            # 创建信息用户
            account = Account(
                sso_id=int(user_info['id']),
                account=user_info['username'],
                email=user_info['email'],
                name=user_info['cname'],
                role='user',
                status=1
            )
            account.save()
        return account
    
    def _sso_verification(self, uid, uid_key):
        check_sso_user_url = "http://sso.ifere.com:8871/api?do=getInfo&uid=%s&key=%s&appid=1172" % (uid, key)

        try:
            data_str = requests.get(check_sso_user_url, timeout=5)
            ret = json.loads(data_str.text)

            if "ret" not in ret or '1' != str(ret['ret']):
                logging.warning('user is invalid uid:%s key:%s' % (uid, key))
                return []

            return ret
        except Exception as e:

            logging.warning('error: %s' % e)
            return []
    
    def _set_login_cache(self, uid, login_at):
        self.cache().set(':'.join(uid, 'sso_login'), login_at)
    
    def _get_login_cache(self, uid):
        return self.cache().get(':'.join(uid, 'sso_login'))