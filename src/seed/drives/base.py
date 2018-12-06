
class BaseDrive(object):
    def __init__(self, ip, port, name, user, password):
        self.ip = ip
        self.port = port
        self.name = name
        self.user = user
        self.password = password
        self._connect()

    def query(self, sql, params=[], retry_count=1):
        raise NotImplementedError("Need to implemented!")

    def execute(self, sql, params=[]):
        raise NotImplementedError("Need to implemented!")

    def test_connection(self):
        rows = self.query("SELECT 1")
        return len(rows) == 1

    def _connect(self):
        raise NotImplementedError("Need to implemented!")

    def _raise_retry_count(self, retry_count):
        if retry_count < 0:
            raise Exception("Retry time out")


class Row(dict):

    """访问对象那样访问dict,行结果"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
