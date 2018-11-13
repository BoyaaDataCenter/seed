import json
# from seed.libs.data_access.formatters.base import BaseFormatter

from seed.libs.data_access.formatters.chart import ChartFormatter


class LineStackFormatter(ChartFormatter):
    def __init__(self, *args, **kwargs):
        super(ChartFormatter, self).__init__(*args, **kwargs)

    def _get_chart_categories_and_series(self):
        """
        获取categoies和series的维度
        """
        categories = []
        series = []

        category_columns, series_columns = self._get_chart_columns()

        # 从数据中获取到对应的categories然后通过数据的维度进行组合
        for key in self.data.keys():
            key = json.loads(key)
            categories.append('-'.join([str(key[category_column]) for category_column in category_columns]))
            if series_columns:
                series_key = '-'.join([str(key[series_column]) for series_column in series_columns])
                if series_key not in series:
                    series.append(series_key)

        categories = list(set(categories))
        categories = self._get_categories_sort_type(categories)

        if not series:
            series = [item['index'] for item in self.indexs]

        return categories, series

    def _get_chart_columns(self):
        category_columns = ['fdate']

        series_columns = [item['dimension'] for item in self.dimensions if item['dimension'] not in category_columns]

        return category_columns, series_columns
