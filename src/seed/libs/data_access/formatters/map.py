import json
from seed.libs.data_access.formatters.base import BaseFormatter


class MapFormatter(BaseFormatter):
    def __init__(self, *args, **kwargs):
        super(MapFormatter, self).__init__(*args, **kwargs)

    def format_data(self):
        data = []
        for key, value in self.data.items():
            k = json.loads(key)
            k.update(value)
            data.append(k)

        return {"data": data}
