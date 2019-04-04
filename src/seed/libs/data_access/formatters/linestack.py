from seed.libs.data_access.formatters.line import LineFormatter


class LineStackFormatter(LineFormatter):
    def __init__(self, *args, **kwargs):
        super(LineStackFormatter, self).__init__(*args, **kwargs)

    def _get_chart_columns(self):
        category_columns = ['fdate']

        series_columns = [item['dimension'] for item in self.dimensions if item['dimension'] not in category_columns]

        return category_columns, series_columns

    def _get_chart_categories_and_series(self):
        categories, series = super(LineStackFormatter, self)._get_chart_categories_and_series()
        categories = list(set(categories))

        # 全是数字
        is_num = all([isinstance(c, (int, float)) for c in categories]) if categories else False
        # 全是字符串数字
        is_strnum = all([isinstance(c, (str,)) and c.isdigit() for c in categories]) if categories else False

        if is_num or is_strnum:
            categories = sorted(categories, key=lambda k: float(k))
        else:
            categories = sorted(categories)

        return categories, series
