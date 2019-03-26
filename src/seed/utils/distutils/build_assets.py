from __future__ import absolute_import

import os
import sys
import shutil
import traceback

from distutils import log

from .base import BaseBuildCommand


class BuildAssetsCommand(BaseBuildCommand):
    user_options = BaseBuildCommand.user_options + [

    ]

    description = 'build static media assets'

    def initialize_options(self):
        BaseBuildCommand.initialize_options(self)

    def _build(self):
        try:
            self._build_static()
        except Exception:
            traceback.print_exc()
            log.fatal(
                'unable to build Seed\'s static assets!\n'
            )
            sys.exit(1)

        self._move_statics()

    def _build_static(self):
        os.chdir('./seed_static')

        log.info('Seed static start install node modules.')
        self._run_command(['npm', 'install'])

        log.info('Seed static start build static files.')
        self._run_command(['npm', 'run', 'buildProd'])

        log.info('Seed static start build finish.')
        os.chdir('..')

    def _move_statics(self):
        source = os.path.join(*'./seed_static/dist'.split('/'))
        target = os.path.join(*'./src/seed/static'.split('/'))

        files = os.listdir(target)
        for file in files:
            if file in ['.gitignore']:
                continue

            if os.path.isdir(os.path.join(target, file)):
                shutil.rmtree(os.path.join(target, file))
            else:
                os.remove(os.path.join(target, file))

        files = os.listdir(source)
        for file in files:
            shutil.move(os.path.join(source, file), os.path.join(target, file))

        log.info('Move static files to seed finish.')
