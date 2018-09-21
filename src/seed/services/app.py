import os

import redis
import flask_migrate
from flask import Flask, g
from flask_migrate import Migrate
from flask_cors import CORS

from seed.models import db, migrate, session, ma
from seed.api.urls import register_api
from seed.utils.auth import SSOAuth


class SeedHttpServer(object):
    def __init__(
        self, host, port, workers, config_file, extra_options=None
    ):
        self.host, self.port = host, port
        self.workers = workers

        self.app = self.create_app(config_file)

        self.register_databases()
        self.register_cache()
        self.register_api()
        self.register_hook()
        self.register_cors()

    def create_app(self, config_file):
        app = Flask(__name__)

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
            decode_components=True
        )
        self.app.cache = redis.Redis(connection_pool=redis_pool)

    def register_api(self):
        register_api(self.app)

    def register_hook(self):
        """ 注册Hook
        """
        @self.app.before_request
        def login_user():
            g.user = SSOAuth().get_current_user()
            # TODO 第一版业务区域逻辑暂时不开发, 留接口等到以后更新
            g.bussiness_id = 1

    def register_cors(self):
        from flask_cors import CORS
        CORS(self.app, supports_credentials=True)

    def run(self):
        self.app.run(self.host, self.port)

    def upgrade(self, sql):
        directory = self.app.extensions['migrate'].directory
        with self.app.app_context():
            if not os.path.exists(os.path.join(directory, 'alembic.ini')):
                flask_migrate.init(directory)
            flask_migrate.migrate(sql=sql)
            flask_migrate.upgrade(sql=sql)
