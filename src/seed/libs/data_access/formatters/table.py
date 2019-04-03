import re
import json

from seed.libs.data_access.formatters.base import BaseFormatter


class TableFormatter(BaseFormatter):
    def __init__(self, *args, **kwargs):
        super(TableFormatter, self).__init__(*args, **kwargs)

    def format_data(self):

        self._ver_to_hor()

        table_keys = [item['dimension'] for item in self.dimensions] + [item['index'] for item in self.indexs]

        # 得到table的表格数据
        table_datas = self._convert_table_data(table_keys, self.data)

        # 对表格数据进行排序
        table_datas = self._sort_table_column(table_datas)

        # 处理比率类型数据
        table_datas = self._convert_rate_data(table_keys, table_datas)

        # 计算总值均值数据
        table_datas = self._compute_total_and_mean(table_datas)

        # 得到table的显示项
        display_name = self._get_display_name(table_keys)

        return {"data": table_datas, "displayName": display_name}

    def _ver_to_hor(self):
        if not self.format_args.get('vth_columns'):
            return

        converted_data = {}

        index = self.indexs[0]['index']
        vth_columns = self.format_args.get('vth_columns')

        self.dimensions = [item for item in self.dimensions if item['dimension'] not in vth_columns]
        self.indexs = []

        for dimensions, values in self.data.items():
            dimensions = json.loads(dimensions)
            converted_dimensions, vth_dimensions = {}, []
            for key, value in dimensions.items():
                if key in vth_columns:
                    vth_dimensions.append(str(value))
                else:
                    converted_dimensions[key] = value
            if '-'.join(vth_dimensions) not in self.indexs:
                self.indexs.append('-'.join(vth_dimensions))
            converted_data.setdefault(json.dumps(converted_dimensions), {})['-'.join(vth_dimensions)] = values[index]

        self.indexs = [{'index': index, 'name': index} for index in self.indexs]
        self.data = converted_data

    def _convert_table_data(self, table_keys, datas):
        # 将数据从中间格式转换成表格格式
        table_datas = []

        for key, values in datas.items():
            values.update(json.loads(key))
            row = {}
            for key in table_keys:
                row[key] = values.get(key, '-')

            table_datas.append(row)

        return table_datas

    def _sort_table_column(self, data):
        # 进行table类型的排序
        dimen_indexs = self.dimensions + self.indexs

        field_list = []
        for di in dimen_indexs:
            tmp = {}
            if di.get("dimension"):
                tmp["field"] = di.get("dimension")
            elif di.get("index"):
                tmp["field"] = di.get("index")

            tmp["sort"] = di.get("sort")
            field_list.append(tmp)

        for field in field_list:
            if field['sort'] == 'desc':
                data.sort(key=lambda x: x[field["field"]] if isinstance(x[field["field"]], (float, int)) else 0,
                          reverse=True)
            if field['sort'] == 'asc':
                data.sort(key=lambda x: x[field["field"]] if isinstance(x[field["field"]], (float, int)) else 0)

        return data

    def _convert_rate_data(self, table_keys, datas):
        """处理比率类型指标的数据"""
        table_datas = []

        indexs = self.indexs[:]
        temp_indexs = [i['index'] for i in indexs]

        for tk in table_keys:
            if tk not in temp_indexs:
                indexs.append({"index": tk})

        for data in datas:
            row = {}
            for index in indexs:
                row[index['index']] = self._format_rate_data(index.get('rate'), data.get(index['index'], '-'))

            table_datas.append(row)

        return table_datas

    def _format_rate_data(self, israte, data):
        """转换比例数据"""
        if not israte:
            return data

        if isinstance(data, (float, int)):
            ratedata = str(round(data * 100, 2)) + '%'
            return ratedata

        return data

    def _compute_total_and_mean(self, datas):
        """计算总值均值数据"""

        rate_dimension = [item['dimension'] for item in self.dimensions] + [item['index'] for item in self.indexs if
                                                                            item["rate"]]
        num = len(datas)

        total_dict = {}
        mean_dict = {}

        for data in datas:
            for key, value in data.items():
                total_dict[key] = total_dict.setdefault(key, 0) + (
                value if value and isinstance(value, (int, float)) else 0)

        for k, v in total_dict.items():
            mean_dict[k] = round(v / float(num), 2)

        first_dimension = self.dimensions[0]["dimension"]

        for k, v in total_dict.items():
            if k in rate_dimension:
                total_dict[k] = '-'
            else:
                total_dict[k] = round(v, 2)

        total_dict[first_dimension] = "总值"

        for k, v in mean_dict.items():
            if k in rate_dimension:
                mean_dict[k] = '-'

        mean_dict[first_dimension] = "均值"

        datas.append(total_dict)
        datas.append(mean_dict)

        return datas

    def _get_display_name(self, keys):
        # 获取displayName格式的数据显示
        titles = []

        dim_display_map = {}

        for item in self.dimensions:
            dim_display_map[item['dimension']] = item['name']

        for item in self.indexs:
            dim_display_map[item['index']] = item['name']

        for key in keys:
            titles.append({"name": key, "displayName": dim_display_map[key]})

        return titles
