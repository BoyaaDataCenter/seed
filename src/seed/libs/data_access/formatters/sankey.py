import json
from seed.libs.data_access.formatters.base import BaseFormatter


class SankeyFormatter(BaseFormatter):
    def __init__(self, *args, **kwargs):
        super(SankeyFormatter, self).__init__(*args, **kwargs)

    def format_data(self):
        links = []
        node_list = []
        nodes = []
        for key, value in self.data.items():
            data = json.loads(key)
            for _, v in data.items():
                node_list.append(v)

            tmp = {}
            for _, v in value.items():
                tmp['value'] = v

            data.update(tmp)
            links.append(data)

        node_list = list(set(node_list))
        for n in node_list:
            nodes.append({"name": n})

        return {"links": links, "nodes": nodes}
