

class FormatterFactory(object):
    def __init__(self, charttype):
        self.charttype = charttype

    def formatter_class(self):
        from seed.libs.data_access.formatters.chart import ChartFormatter
        from seed.libs.data_access.formatters.table import TableFormatter
        if self.charttype == 'table':
            return TableFormatter
        return ChartFormatter


class BaseFormatter(object):
    def __init__(self, indexs, dimensions, data):
        self.indexs = indexs
        self.dimensions = dimensions
        self.data = data