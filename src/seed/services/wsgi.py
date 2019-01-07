import os
import sys

from seed.runner.setting import discover_configs


def convert_options_to_uwsgi_env(options):
    for key, value in options.items():
        key = 'USWGI_' + key.upper().replace('-', '_')

        if isinstance(value, int):
            value = str(value)

        yield key, value


class SeedWSGIHttpServer(object):
    def __init__(self, debug=False, workers=None):
        _, config_file, _ = discover_configs()

        options = {}
        options.setdefault('model', 'seed.services.app:application')
        options.setdefault('protocol', 'http')
        options.setdefault('workers', 3)
        options.setdefault('threads', 4)
        options.setdefault('http-timeout', 60)

        options.setdefault('%-socket' % options['protocol'], '%s:%s' % ('127.0.0.1', '5000'))

        self.options = options

    def prepare_environment(self, env=None):
        if not env:
            env = os.environ

        for key, value in convert_options_to_uwsgi_env(self.options):
            env.setdefault(key, value)

        virtualenv_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        current_path = env.get('PATH', '')
        if virtualenv_path not in current_path:
            env['PATH'] = '%s:%s' % (virtualenv_path, current_path)

    def run(self):
        self.prepare_environment()
        os.execvp('uwsgi', ('uwsgi', ))
