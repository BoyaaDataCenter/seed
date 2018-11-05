import json
import collections


class MiddleData(object):
    """ 原始数据格式 转 中间数据格式
    row = [
        {'dau': 100, 'dsu': 200, 'fdate': '2017-01-01'},
        {'dau': 100, 'dsu': 200, 'fdate': '2017-01-02'},
    ]

    reuslt = {
        json.loads({'fdata': '2017-01-01'}): {'dau': 100, 'dsu': 200},
        json.loads({'fdata': '2017-01-02'}): {'dau': 200, 'dsu': 100},
    }
    """

    def __init__(self, source_data, dimensions, indexs):
        self.source_data = source_data
        self.dimensions = [item['dimension'] for item in dimensions]
        self.indexs = [item['index'] for item in indexs]

    def convert(self):
        middle_datas = {}

        for row in self.source_data:

            # 根据dimensions构造当前数据项的key
            row_keys = collections.OrderedDict()
            for dimension in self.dimensions:
                row_keys[dimension] = row[dimension]

            for index in self.indexs:
                middle_key = json.dumps(row_keys)
                if middle_datas.get(middle_key, {}).get(index) is None:
                    middle_datas.setdefault(middle_key, {})[index] = row.get(index, None)

        return middle_datas
