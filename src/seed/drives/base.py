DEFUALT_RETRY_COUNT = 3


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

    def _get_connection(self):
        if self.alive():
            self._connect()

    def _commit(self):
        """ 完成SQL执行
        """
        self.conn.commit()

    def _rollback(self):
        """ 回滚SQL
        """
        self.conn.rollback()

    def _gen_cursor(self):
        cursor = self.conn.cursor()
        return cursor

    def alive(self):
        """ 测试连接是否还存在
        """
        if self.conn:
            return True if self.conn.closed == 0 else False

        return False

    def close(self):
        """ 关闭连接
        """
        self.conn.close()
