from flask import request

from seed.api.endpoints._base import RestfulBaseView, HttpMethods
from seed.drives import ALL_DRIVES


class DatabaseTest(RestfulBaseView):
    url = 'database_test'

    access_methods = [HttpMethods.POST]

    def post(self):
        db_conf = request.get_json()

        try:
            drive = ALL_DRIVES[db_conf['dtype']]
            drive_instance = drive(
                db_conf['ip'], int(db_conf['port']), db_conf['name'],
                db_conf['user'], db_conf['password']
            )
            success = drive_instance.test_connection()
            message = '数据库连接成功!'
        except Exception as e:
            success = False
            message = str(e)

        if success:
            return self.response_json(self.HttpErrorCode.SUCCESS, msg=message)

        return self.response_json(self.HttpErrorCode.ERROR, msg=message)