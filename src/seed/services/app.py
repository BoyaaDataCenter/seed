import os
import sys

import redis
import flask_migrate
from flask import Flask, g
from flask_cors import CORS

from seed.runner.setting import discover_configs

from seed.models import db, migrate, session, ma
from seed.api.urls import register_api
from seed.utils.auth import SSOAuth, SessionAuth
from seed.cache.user_bussiness import UserBussinessCache
from seed.models.init import init_database_default_analogdata, init_database_default_datas, is_new_databases
from seed.utils.helper import template_folder_path, static_folder_path


class SeedHttpServer(object):
    def __init__(
        self, config_file, extra_options=None
    ):
        self.app = self.create_app(config_file)
        self.register_cors()

        self.register_databases()
        self.register_cache()
        self.register_api()
        self.register_hook()

    def create_app(self, config_file):
        app = Flask(
            __name__,
            static_url_path='/static',
            static_folder=static_folder_path,
            template_folder=template_folder_path
        )

        app.config.from_pyfile(config_file)

        return app

    def register_databases(self):
        db.init_app(self.app)
        migrate.init_app(app=self.app, db=db)
        ma.init_app(self.app)

        with self.app.app_context():
            session.configure(bind=db.engine)

    def register_cache(self):
        redis_pool = redis.ConnectionPool.from_url(
            self.app.config['REDIS_URL'],
            decode_responses=True,
            charset="utf-8",
        )
        self.app.cache = redis.Redis(connection_pool=redis_pool)

    def register_api(self):
        register_api(self.app)

        from seed.api import front
        self.app.register_blueprint(front.bp, url_prefix='')

    def register_hook(self):
        """ 注册Hook
        """
        @self.app.before_request
        def login_user():

            if self.app.config['AUTH_TYPE'] == 'SSO':
                auth = SSOAuth()
            else:
                auth = SessionAuth()

            g.user = auth.get_current_user()

            # debugger
            g.user = auth.debbuger_user()

            if g.user:
                g.bussiness_id = UserBussinessCache().get(g.user.id) or -1
            else:
                g.bussiness_id = -1

    def register_cors(self):
        CORS(self.app, supports_credentials=True)

    def run(self):
        self.app.run(self.app.config['HOST'], self.app.config['PORT'])

    def upgrade(self, sql):
        print('数据库开始初始化')
        with self.app.app_context():
            migrate_directory = self.app.extensions['migrate'].directory

            migrate_path, _, _ = discover_configs()
            migrate_path = os.path.join(migrate_path, migrate_directory)

            if not os.path.exists(os.path.join(migrate_path, 'alembic.ini')):
                # 判断是不是第一次初始化数据库
                is_empty = input('第一次初始化数据库，请确保你的数据库是空的。Y/N? ')
                if is_empty != 'Y':
                    return

                flask_migrate.init(migrate_path)

            flask_migrate.migrate(migrate_path, sql=sql)
            flask_migrate.upgrade(migrate_path, sql=sql)

            if is_new_databases():
                # 写入默认数据
                print('初始化模拟数据')
                init_database_default_analogdata()
                print('初始化默认业务模块')
                init_database_default_datas()

        print("数据库升级完成")


def apply_application():
    _, config_file, _ = discover_configs()
    http_server = SeedHttpServer(
        config_file=config_file
    )
    return http_server.app


application = apply_application()
