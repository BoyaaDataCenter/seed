import json

from seed.libs.data_access.formatters.base import BaseFormatter


class PieFormatter(BaseFormatter):
    def format_data(self):
        result = {"series": []}

        middle_data = {}

        for dimension, values in self.data.items():
            for dim, value in values.items():
                middle_data.setdefault(dim, []).append({"fname": dimension, "value": value})

        for dim, dim_value in middle_data.items():
            info = {"data": [], "dim": dim, "name": dim}

            for data in dim_value:
                _d = {}
                _d['name'] = '-'.join(str(item) for item in json.loads(data['fname']).values())
                _d['value'] = data['value']
                info['data'].append(_d)

            info['data'] = sorted(info['data'], key=lambda k: k['value'], reverse=True)
            result["series"].append(info)

        return result
