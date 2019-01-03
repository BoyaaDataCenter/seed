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
        self._run_command(['npm', 'install'])
        self._run_command(['npm', 'run', 'build'])

    def _move_statics(self):
        source = r'./dist'
        target = r'../src/seed/static'
        shutil.rmtree(target)

        files = os.listdir(source)
        for file in files:
            shutil.move(os.path.join(source, file), os.path.join(target, file))
