
class FilterAccess(object):
    def __init__(self, db, conditions,  *args, **kwargs):
        self.db_instance = db
        self.sql = conditions

    def query_datas(self):
        rows = self.db_instance.query(self.sql)
        return rows