from inspect import isclass

from flask import Blueprint

from seed import api
from seed.utils.helper import get_package_members
from seed.api.common import _MethodView


def register_api(app):
    """ register api interface
    """
    
    predicate = lambda m: isclass(m) and issubclass(m, _MethodView) and m.__abstrcut__ == False
    members = get_package_members(api, predicate, '.')

    for pre_url, handlers in members.items():
        bp = Blueprint(pre_url, __name__)
        for handler in handlers:
            bp = handler.register_api(bp)
    
        app.register_blueprint(bp, url_prefix=pre_url)
    