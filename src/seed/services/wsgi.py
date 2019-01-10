import os
import sys


def convert_options_to_uwsgi_env(options):
    for key, value in options.items():
        key = 'UWSGI_' + key.upper().replace('-', '_')

        if isinstance(value, int):
            value = str(value)

        yield key, value


class SeedWSGIHttpServer(object):
    def __init__(self, debug=False, workers=None):

        options = {}
        options.setdefault('module', 'seed.services.app:application')
        options.setdefault('protocol', 'http')
        options.setdefault('workers', 3)
        options.setdefault('threads', 4)
        options.setdefault('http-timeout', 60)
        options.setdefault('need-app', True)
        options.setdefault('virtualenv', sys.prefix)
        options.setdefault('die-on-term', True)
        options.setdefault(
            'log-format',
            '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)" "%(uagent)"'
        )

        from seed.services.app import application
        options.setdefault('%s-socket' % options['protocol'], '%s:%s' % (application.config['HOST'], application.config['PORT']))

        options['master'] = True
        options['enable-threads'] = True

        self.options = options

    def prepare_environment(self, env=None):
        if not env:
            env = os.environ

        for key, value in convert_options_to_uwsgi_env(self.options):
            env.setdefault(key, value)

        # virtualenv_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        # current_path = str(os.path.realpath(__file__))
        # if virtualenv_path not in current_path:
        #     env['PATH'] = '%s:%s' % (virtualenv_path, current_path)

    def run(self):
        self.prepare_environment()
        os.execvp('uwsgi', ('uwsgi', ))
