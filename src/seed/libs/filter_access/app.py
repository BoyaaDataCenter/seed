class FilterAccess(object):
    def __init__(self, db, conditions, query,  *args, **kwargs):
        self.db_instance = db
        self.sql = conditions
        self.query = query

    def query_datas(self):
        sql = self.sql.format(**self.query)
        rows = self.db_instance.query(sql)
        return rows
