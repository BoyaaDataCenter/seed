

class FormatterFactory(object):
    def __init__(self, charttype, indexs, dimensions):
        self.charttype = charttype
        self.indexs = indexs
        self.dimensions = dimensions

    def formatter_instnace(self):
        from seed.libs.data_access.formatters.chart import ChartFormatter
        return ChartFormatter(self.indexs, self.dimensions)


class BaseFormatter(object):
    def __init__(self, indexs, dimensions):
        self.indexs = indexs
        self.dimensions = dimensions