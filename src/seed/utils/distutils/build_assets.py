from __future__ import absolute_import

from distutils import log

from .base import BaseBuildCommand


class BuildAssetsCommand(BaseBuildCommand):
    user_options = BaseBuildCommand.user_options + [

    ]

    description = 'build static media assets'

    def initialize_options(self):
        BaseBuildCommand.initialize_options(self)

    def _build(self):
        pass