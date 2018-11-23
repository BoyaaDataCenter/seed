import re
import json

from seed.libs.data_access.formatters.base import BaseFormatter


class LineFormatter(BaseFormatter):
    def __init__(self, *args, **kwargs):
        super(LineFormatter, self).__init__(*args, **kwargs)

    def format_data(self):
        # 得到分布项
        categories, series = self._get_chart_categories_and_series()

        # 获取series图形数据
        series = self._convert_series_data(categories, series)

        return {"categories": categories, "series": series}

    def _get_chart_categories_and_series(self):
        """
        获取categoies和series的维度
        """
        categories_dict = []
        series = []

        category_columns, series_columns = self._get_chart_columns()

        # 从数据中获取到对应的categories然后通过数据的维度进行组合
        for key in self.data.keys():
            key = json.loads(key)
            cateogry = {category_column: key[category_column] for category_column in category_columns}
            if cateogry not in categories_dict:
                categories_dict.append(cateogry)
            if series_columns:
                series_key = '-'.join([str(key[series_column]) for series_column in series_columns])
                if series_key not in series:
                    series.append(series_key)

        # categories排序
        for dimension in self.dimensions:
            if dimension['sort'] == 'desc':
                categories_dict.sort(key=lambda x: x[dimension['dimension']], reverse=True)
            if dimension['sort'] == 'asc':
                categories_dict.sort(key=lambda x: x[dimension['dimension']])

        categories = [
            '-'.join([str(category_dict[category_column]) for category_column in category_columns])
            for category_dict in categories_dict
        ]
        categories = self._get_categories_sort_type(categories, category_columns)

        if not series:
            series = [item['index'] for item in self.indexs]

        return categories, series

    def _get_chart_columns(self):
        category_columns, series_columns = [item['dimension'] for item in self.dimensions], []
        return category_columns, series_columns

    def _convert_series_data(self, categories, series):
        # 从数据中获取到趋势类型的数据
        category_columns, series_columns = self._get_chart_columns()
        series_map = {index['index']: index for index in self.indexs}

        middle_data = {}
        if series_columns:
            for key, value in self.data.items():
                key = json.loads(key)
                category_key = '-'.join([str(key[category_column]) for category_column in category_columns])
                if series_columns:
                    series_key = '-'.join([str(key[series_column]) for series_column in series_columns])
                    middle_data.setdefault(category_key, {})[series_key] = sum(value.values())
        else:
            middle_data = {
                '-'.join([str(json.loads(key)[category_column]) for category_column in category_columns]): value for
                key, value in self.data.items()}

        series_datas = []
        for serie in series:
            data = []
            for category in categories:
                data.append(middle_data.get(str(category), {}).get(serie, '-'))

            series_data = {'data': data, 'dim': serie}
            series_data.update(series_map.get(serie, {}))
            series_datas.append(series_data)

        return series_datas

    def _get_categories_sort_type(self, categories, category_columns):
        if not len(categories):
            return categories

        if any(index['sort'] in ('desc', 'asc') for index in self.indexs):
            # 按指标进行排序
            categories = self._categories_sort_by_value(category_columns)

        return categories

        # try:
        #     res = re.search(r"(\d{2}:\d{2})", categories[0])
        # except TypeError:
        #     # categories可能为空
        #     res = None
        # if all([category.isdigit() for category in categories]):
        #     categories.sort(key=int)
        # elif res or 'fdate' in [item['dimension'] for item in self.dimensions]:
        #     # 判断是否全部为数字 如果是 则按照数字进行排序
        #     categories.sort()
        # else:
        #     # 否则按照值进行排序
        #     categories = self._categories_sort_by_value()
        # return categories

    def _categories_sort_by_value(self, category_columns):
        middle_date = {}

        sort_index = None
        sort_reverse = None
        for index in self.indexs:
            if index['sort'] in ('desc', 'asc'):
                sort_index = index['index']
                sort_reverse = True if index['sort'] != 'desc' else False
                break

        for i, j in self.data.items():
            i = json.loads(i)
            middle_date.update(
                {'-'.join([str(i[category_column]) for category_column in category_columns]): j[sort_index]}
            )
        categories_data = sorted(middle_date.items(), key=lambda d: d[1] if d[1] else 0, reverse=sort_reverse)
        categories = [v[0] for v in categories_data]
        return categories
