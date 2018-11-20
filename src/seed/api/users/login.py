from flask import request
from seed.api.endpoints._base import RestfulBaseView, HttpMethods


class Login(RestfulBaseView):
    """ 登录
    """
    access_methods = [HttpMethods.POST]

    def post(self):
        """ POST
        """
        input_json = request.get_json()
