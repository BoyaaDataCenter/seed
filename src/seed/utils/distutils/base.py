from __future__ import absolute_import

import os
import sys

from distutils import log
from subprocess import check_output
from distutils.core import Command


class BaseBuildCommand(Command):
    user_options = [
        ('work-path', 'w', 'The working directory for source files. Default is .')
    ]

    def initialize_options(self):
        self.work_path = '.'

    def finalize_options(self):
        pass

    def update_mainfests(self):
        pass

    def _setup_git(self):
        work_path = self.work_path
        if os.path.exists(os.path.join(work_path, '.git')):
            log.info("initializing git submodules")
            self._run_command(['git', 'submodule', 'init'])
            self._run_command(['git', 'submodule', 'update'])

    def _setup_npm(self):
        node_version = []

        log.info("setup node and npm.....")
        for app in ['node', 'npm']:
            try:
                log.info('testing %s version.....' % app)
                node_version.append(self._run_command([app, '--version']).rstrip())
            except OSError as e:
                log.fatal(
                    'Cannot find {app} excutable. Please install {app}'
                    'and try again.'.format(app=app)
                )
                sys.exit(1)

        if node_version[0] >= b'v6.8.1':
            log.fatal('The node version need v6.8.1, the current node version is %s' % node_version[0])
            sys.exit(1)

        log.info('using node ({0}) and npm ({1})'.format(*node_version))
        self._run_command(['npm', 'install'])

    def _run_command(self, cmd, env=None):
        log.debug('running [%s]' % (' '.join(cmd), ))
        try:
            return check_output(cmd, cwd=self.work_path, env=env, shell=True)
        except Exception:
            log.error('command failed [%s] via [%s]' % (' '.join(cmd), self.work_path, ))
            raise

    def sub_commands(self):
        pass

    def run(self):
        self._setup_git()
        self._setup_npm()
        self._build()
        self.update_mainfests()
