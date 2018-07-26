from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config)


class SeedHttpServer(object):
    def __init__(
        self, host, port, workers, debug, extra_options=None
    ):
        self.app = Flask(__name__)

        self.host, self.port = host, port
        self.workers = workers
        self.debug = debug

    def register_endpoint(self):
        pass

    def register_hook(self):
        pass

    def run(self):
        self.app.run(self.host, self.port, debug=self.debug)
