
class BaseDrive(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def query(self, sql, params=[]):
        raise NotImplementedError("Need to implemented!")

    def execute(self, sql, params=[]):
        raise NotImplementedError("Need to implemented!")
