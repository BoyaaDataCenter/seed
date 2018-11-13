import json
# from seed.libs.data_access.formatters.base import BaseFormatter

from seed.libs.data_access.formatters.chart import ChartFormatter


class LineStackFormatter(ChartFormatter):
    def __init__(self, *args, **kwargs):
        super(ChartFormatter, self).__init__(*args, **kwargs)

    def _get_chart_columns(self):
        category_columns = ['fdate']

        series_columns = [item['dimension'] for item in self.dimensions if item['dimension'] not in category_columns]

        return category_columns, series_columns
