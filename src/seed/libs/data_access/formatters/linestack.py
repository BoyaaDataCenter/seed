from seed.libs.data_access.formatters.line import LineFormatter


class LineStackFormatter(LineFormatter):
    def __init__(self, *args, **kwargs):
        super(LineFormatter, self).__init__(*args, **kwargs)

    def _get_chart_columns(self):
        category_columns = ['fdate']

        series_columns = [item['dimension'] for item in self.dimensions if item['dimension'] not in category_columns]

        return category_columns, series_columns
