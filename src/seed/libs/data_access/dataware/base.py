

class DataModel(object):
    def __init__(self, db, sql, query):
        self.db = db
        self.sql = sql
        self.query = query

    def gen_sql(self):
        for key, value in self.query.items():
            if isinstance(value, list):
                self.query[key] = '(%s)' % ', '.join([str(item) for item in value])

        return self.sql.format(**self.query)

    def query_data(self):
        sql = self.gen_sql()
        return self.db.query(sql), sql
