class FilterAccess(object):
    def __init__(self, db, conditions, query,  *args, **kwargs):
        self.db_instance = db
        self.sql = conditions
        self.query = query

    def query_datas(self):
        for key, value in self.query.items():
            if isinstance(value, list):
                self.query[key] = '(%s)' % ', '.join([str(item) for item in value])

        sql = self.sql.format(**self.query)
        print(sql)

        rows = self.db_instance.query(sql)
        return rows
