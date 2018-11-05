from seed.libs.data_access.dataware.base import DataModel

class DataAccess(object):
    def __init__(self, dtype, db, *args, **kwargs):
        # self.dtype = dtype
        self.db = db

        self.sql = kwargs['sql']
        self.indexs = kwargs['indexs']
        self.dimensions = kwargs['dimensions']
        self.query = kwargs.get('query', {})

        self.charttype = kwargs.get('charttype', 'chart')

    def get_datas(self):
        # 获取原数据
        source_data, sql_info = self.get_source_data()
        middle_data = self.transfer_middle_data(source_data)

        # 格式化
        format_data = self.format_data(middle_data)

        return format_data

    def get_source_data(self):
        source_data, sql_info = DataModel(self.db, self.sql, self.query).query_data()
        return source_data, sql_info

    def transfer_middle_data(self, source_data):
        return {}

    def format_data(self, middle_data):
        return data