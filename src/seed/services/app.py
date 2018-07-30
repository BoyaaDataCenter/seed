import os

import flask_migrate
from flask import Flask
from flask_migrate import Migrate

from seed.models import db, migrate


class SeedHttpServer(object):
    def __init__(
        self, host, port, workers, config_file, extra_options=None
    ):
        self.host, self.port = host, port
        self.workers = workers

        self.app = self.create_app(config_file)
        self.debug = False

        self.register_databases()

    def create_app(self, config_file):
        app = Flask(__name__)

        app.config.from_pyfile(config_file)

        return app

    def register_databases(self):
        db.init_app(self.app)
        migrate.init_app(app=self.app, db=db)

    def register_endpoint(self):
        pass

    def register_hook(self):
        pass

    def run(self):
        self.app.run(self.host, self.port, debug=self.debug)

    def upgrade(self):
        directory = self.app.extensions['migrate'].directory
        with self.app.app_context():
            if not os.path.exists(os.path.join(directory, 'alembic.ini')):
                flask_migrate.init()
            flask_migrate.migrate()
            flask_migrate.upgrade()
