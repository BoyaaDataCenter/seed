from seed.libs.data_access.formatters.chart import ChartFormatter


class BarFormatter(ChartFormatter):
    def __init__(self, *args, **kwargs):
        super(ChartFormatter, self).__init__(*args, **kwargs)