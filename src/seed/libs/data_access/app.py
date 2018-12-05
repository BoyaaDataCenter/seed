from seed.libs.data_access.dataware.base import DataModel
from seed.libs.data_access.middledata.base import MiddleData
from seed.libs.data_access.formatters.base import FormatterFactory


class DataAccess(object):
    def __init__(self, dtype, db, *args, **kwargs):
        # self.dtype = dtype
        self.db = db

        self.sql = kwargs['sql']
        if not self.sql:
            raise Exception("SQL不能为空！")

        self.indexs = kwargs['indexs']
        if not self.indexs:
            raise Exception("指标不能为空！")

        self.dimensions = kwargs['dimensions']
        if not self.dimensions:
            raise Exception("维度不能为空！")

        self.query = kwargs.get('query', {})

        self.charttype = kwargs.get('charttype', 'chart')

        self.format_args = {'vth_columns': kwargs.get('vth_columns', [])}

    def get_datas(self):
        # 获取原数据
        try:
            source_data, sql_info = self.get_source_data()
            middle_data = self.transfer_middle_data(source_data)
        except Exception as e:
            raise Exception('数据库取数错误: %s' % str(e))

        # 格式化
        try:
            format_data = self.format_data(middle_data)
        except Exception as e:
            raise Exception('数据格式化出错: %s' % str(e))

        return format_data

    def get_source_data(self):
        source_data, sql_info = DataModel(
            self.db, self.sql, self.query, self.dimensions, self.indexs
        ).query_data()
        return source_data, sql_info

    def transfer_middle_data(self, source_data):
        middle_data = MiddleData(
            source_data, self.dimensions, self.indexs
        ).convert()
        return middle_data

    def format_data(self, middle_data):

        formatter = FormatterFactory(self.charttype).formatter_class()
        format_data = formatter(
            self.indexs, self.dimensions, middle_data, self.format_args
        ).format_data()

        return format_data
